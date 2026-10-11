from pathlib import Path
import shutil
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")
helper_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(".")

# 1) Use the same Pixel/System-Vulkan launch profile that previously reached WoW,
# but enable the compute BCn path expected by the WeHavePhones compatibility layer.
wow = root / "app/src/main/java/app/gamenative/ui/screen/wow/WoWForeverScreen.kt"
text = wow.read_text()

replacements = {
    'put("screenSize", "1920x1080")':
        'put("screenSize", "1280x720")',
    'put("graphicsDriverVersion", "Turnip-WoW-scheduler-test")':
        'put("graphicsDriverVersion", "System")',
    'put("graphicsDriverConfig", "version=Turnip-WoW-scheduler-test,adrenotoolsTurnip=1,resourceType=buffer,bcnEmulation=auto,quality=high")':
        'put("graphicsDriverConfig", "version=System,adrenotoolsTurnip=0,resourceType=buffer,bcnEmulation=auto,bcnEmulationType=compute,bcnEmulationCache=1,quality=high")',
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"Expected WoW profile text not found: {old}")
    text = text.replace(old, new, 1)

# TU_DEBUG is Turnip-specific; keep the rest of the known-good Pixel environment.
old_env = 'WRAPPER_MAX_IMAGE_COUNT=0 ZINK_DESCRIPTORS=lazy ZINK_DEBUG=compact,deck_emu MESA_SHADER_CACHE_DISABLE=false MESA_SHADER_CACHE_MAX_SIZE=512MB mesa_glthread=true WINEESYNC=0 MESA_VK_WSI_PRESENT_MODE=mailbox TU_DEBUG=noconform VKD3D_SHADER_MODEL=6_0 PULSE_LATENCY_MSEC=144'
new_env = 'WRAPPER_MAX_IMAGE_COUNT=0 ZINK_DESCRIPTORS=lazy ZINK_DEBUG=compact,deck_emu MESA_SHADER_CACHE_DISABLE=false MESA_SHADER_CACHE_MAX_SIZE=512MB mesa_glthread=true WINEESYNC=0 MESA_VK_WSI_PRESENT_MODE=mailbox VKD3D_SHADER_MODEL=6_0 PULSE_LATENCY_MSEC=144'
if old_env not in text:
    raise RuntimeError("Expected WoW envVars line not found")
text = text.replace(old_env, new_env, 1)
wow.write_text(text)

# 2) Add the WeHavePhones implicit Vulkan compatibility layer as an Android JNI library.
native_src = helper_root / "patches/wehavephones_vulkan_compat.c"
native_dst_dir = root / "app/src/main/cpp/wehavephones_vulkan_compat"
native_dst_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(native_src, native_dst_dir / "wehavephones_vulkan_compat.c")

cmake = root / "app/src/main/cpp/CMakeLists.txt"
cm = cmake.read_text()
anchor = "add_subdirectory(extras/adrenotools)\n"
addition = r'''
# WeHavePhones compatibility layer for system Vulkan on GPUs without native BCn.
# Source adapted from ashmerra/wehavephones (MIT), pinned in this build helper.
add_library(wehavephones_vulkan_compat SHARED
            wehavephones_vulkan_compat/wehavephones_vulkan_compat.c)
target_compile_options(wehavephones_vulkan_compat PRIVATE -fvisibility=hidden)
target_link_libraries(wehavephones_vulkan_compat dl)
target_link_options(wehavephones_vulkan_compat PRIVATE -Wl,-z,max-page-size=16384)

'''
if addition.strip() not in cm:
    if anchor not in cm:
        raise RuntimeError("CMake adrenotools anchor not found")
    cm = cm.replace(anchor, anchor + addition, 1)
cmake.write_text(cm)

# 3) Add a small installer that writes the implicit-layer manifest into imagefs
# and enables the same env flags used by WeHavePhones.
helper = root / "app/src/main/java/app/gamenative/utils/WeHavePhonesVulkanCompat.kt"
helper.parent.mkdir(parents=True, exist_ok=True)
helper.write_text(r'''package app.gamenative.utils

import android.content.Context
import com.winlator.core.envvars.EnvVars
import org.json.JSONObject
import java.io.File

/**
 * GameNative port of ashmerra/wehavephones' VulkanCompatLayer installer.
 *
 * The native layer bridges Vulkan 1.3 format/copy/shader paths used by DXVK
 * back through the wrapper's BCn and shader compatibility paths.
 */
object WeHavePhonesVulkanCompat {
    private const val ENABLE_ENV = "ENABLE_WEHAVEPHONES_VULKAN_COMPAT"
    private const val LIBRARY_NAME = "libwehavephones_vulkan_compat.so"
    private const val MANIFEST_PATH =
        "usr/share/vulkan/implicit_layer.d/wehavephones_vulkan_compat.json"

    fun install(context: Context, rootDir: File, envVars: EnvVars): Boolean {
        val library = File(context.applicationInfo.nativeLibraryDir, LIBRARY_NAME)
        if (!library.isFile) return false

        val functions = JSONObject()
            .put("vkGetInstanceProcAddr", "WeHavePhonesVulkanCompat_GetInstanceProcAddr")
            .put("vkGetDeviceProcAddr", "WeHavePhonesVulkanCompat_GetDeviceProcAddr")

        val layer = JSONObject()
            .put("name", "VK_LAYER_WEHAVEPHONES_vulkan_compat")
            .put("type", "GLOBAL")
            .put("library_path", library.absolutePath)
            .put("api_version", "1.3.0")
            .put("implementation_version", "1")
            .put("description", "Routes Vulkan 1.3 BCn/copy/shader paths through wrapper compatibility fixes")
            .put("functions", functions)
            .put("enable_environment", JSONObject().put(ENABLE_ENV, "1"))
            .put(
                "disable_environment",
                JSONObject().put("DISABLE_WEHAVEPHONES_VULKAN_COMPAT", "1"),
            )

        val manifest = JSONObject()
            .put("file_format_version", "1.0.0")
            .put("layer", layer)
            .toString(2)

        val target = File(rootDir, MANIFEST_PATH)
        target.parentFile?.mkdirs()
        if (!target.exists() || target.readText() != manifest) {
            target.writeText(manifest)
        }

        if (!envVars.has(ENABLE_ENV)) envVars.put(ENABLE_ENV, "1")
        // WeHavePhones disables the wrapper's unsafe OpConstantComposite pass
        // and performs a bounded replacement in the native layer.
        if (!envVars.has("WRAPPER_NO_PATCH_OPCONSTCOMP")) {
            envVars.put("WRAPPER_NO_PATCH_OPCONSTCOMP", "1")
        }
        return true
    }
}
''')

# 4) Enable the layer for non-Adreno GPUs after GameNative has configured its
# normal wrapper/BCn variables. This keeps the existing GameNative wrapper and
# system Vulkan driver instead of swapping in an unrelated driver binary.
xserver = root / "app/src/main/java/app/gamenative/ui/screen/xserver/XServerScreen.kt"
xs = xserver.read_text()

import_anchor = "import app.gamenative.utils.LsfgVkManager\n"
new_import = "import app.gamenative.utils.WeHavePhonesVulkanCompat\n"
if new_import not in xs:
    if import_anchor not in xs:
        raise RuntimeError("XServer import anchor not found")
    xs = xs.replace(import_anchor, import_anchor + new_import, 1)

install_anchor = '''        val wrapperQuality = graphicsDriverConfig.get("quality", "low")
        envVars.put("WRAPPER_ASTC_BLOCK", if (wrapperQuality.equals("high", ignoreCase = true)) "4x4" else "8x8")

'''
install_block = '''        val wrapperQuality = graphicsDriverConfig.get("quality", "low")
        envVars.put("WRAPPER_ASTC_BLOCK", if (wrapperQuality.equals("high", ignoreCase = true)) "4x4" else "8x8")

        // WeHavePhones' tested Tensor G3 / Mali path uses the phone's system
        // Vulkan driver plus an implicit BCn/shader compatibility layer.
        // Their device rules also apply the same path to other non-Adreno GPUs
        // (including PowerVR), although that case is marked untested upstream.
        val rendererForCompat = GPUInformation.getRenderer(null, null) ?: ""
        if (!rendererForCompat.contains("Adreno", ignoreCase = true)) {
            val installed = WeHavePhonesVulkanCompat.install(context, rootDir!!, envVars)
            Timber.i("WeHavePhones Vulkan compat layer installed=$installed renderer=$rendererForCompat")
        }

'''
if install_anchor not in xs:
    raise RuntimeError("BCn wrapper-quality anchor not found")
xs = xs.replace(install_anchor, install_block, 1)
# Keep Android system navigation visible on experimental non-Adreno builds so a
# bad Vulkan path can never trap the user inside the game surface.
old_ui = 'PluviaApp.events.emit(AndroidEvent.SetSystemUIVisibility(false))'
if old_ui in xs:
    xs = xs.replace(
        old_ui,
        'PluviaApp.events.emit(AndroidEvent.SetSystemUIVisibility(true)) // experimental Pixel safety',
        1,
    )

xserver.write_text(xs)

print("Applied WeHavePhones system-Vulkan compatibility layer to Pixel/non-Adreno profile.")
