from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")

# 1) Recreate the exact Pixel profile from the FIRST APK that actually launched WoW.
wow = root / "app/src/main/java/app/gamenative/ui/screen/wow/WoWForeverScreen.kt"
text = wow.read_text()

replacements = {
    'statusText = "Configuring Adreno 740 container..."':
        'statusText = "Configuring Pixel 11 PowerVR container..."',
    'put("screenSize", "1920x1080")':
        'put("screenSize", "1280x720")',
    'put("envVars", "WRAPPER_MAX_IMAGE_COUNT=0 ZINK_DESCRIPTORS=lazy ZINK_DEBUG=compact,deck_emu MESA_SHADER_CACHE_DISABLE=false MESA_SHADER_CACHE_MAX_SIZE=512MB mesa_glthread=true WINEESYNC=0 MESA_VK_WSI_PRESENT_MODE=mailbox TU_DEBUG=noconform VKD3D_SHADER_MODEL=6_0 PULSE_LATENCY_MSEC=144${if (Build.MANUFACTURER.equals("samsung", ignoreCase = true)) " FD_DEV_FEATURES=enable_tp_ubwc_flag_hint=1" else ""}")':
        'put("envVars", "WRAPPER_MAX_IMAGE_COUNT=0 ZINK_DESCRIPTORS=lazy ZINK_DEBUG=compact,deck_emu MESA_SHADER_CACHE_DISABLE=false MESA_SHADER_CACHE_MAX_SIZE=512MB mesa_glthread=true WINEESYNC=0 MESA_VK_WSI_PRESENT_MODE=mailbox VKD3D_SHADER_MODEL=6_0 PULSE_LATENCY_MSEC=144")',
    'put("graphicsDriverVersion", "Turnip-WoW-scheduler-test")':
        'put("graphicsDriverVersion", "System")',
    'put("graphicsDriverConfig", "version=Turnip-WoW-scheduler-test,adrenotoolsTurnip=1,resourceType=buffer,bcnEmulation=auto,quality=high")':
        'put("graphicsDriverConfig", "version=System,adrenotoolsTurnip=1,resourceType=buffer,bcnEmulation=auto,quality=high")',
    'text = "Snapdragon 8 Gen 2 / Adreno 740 Edition"':
        'text = "Pixel 11 / Tensor G6 / PowerVR · first-launch profile + compat layer"',
    'CheckItem(label = "Turnip Driver & Proton 11 ARM64EC (Bundled)", ready = true)':
        'CheckItem(label = "System Vulkan + BCn/Vulkan 1.3 compatibility layer", ready = true)',
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"Expected WoW profile text not found: {old[:120]}")
    text = text.replace(old, new, 1)
wow.write_text(text)

# 2) Build the WeHavePhones compatibility layer into this GameNative APK.
cmake = root / "app/src/main/cpp/CMakeLists.txt"
c = cmake.read_text()
anchor = 'add_subdirectory(extras/adrenotools)\n'
addition = '''add_subdirectory(extras/adrenotools)

# WeHavePhones Vulkan 1.3/BCn compatibility shim.
# Source pinned from ashmerra/wehavephones commit 8866cb556b4dd5bcbe8248a363ba3286891cf681.
add_library(wehavephones_vulkan_compat SHARED
            wehavephones_vulkan_compat/wehavephones_vulkan_compat.c)
target_compile_options(wehavephones_vulkan_compat PRIVATE -fvisibility=hidden)
target_link_libraries(wehavephones_vulkan_compat dl)
target_link_options(wehavephones_vulkan_compat PRIVATE -Wl,-z,max-page-size=16384)
'''
if anchor not in c:
    raise RuntimeError("CMake insertion point not found")
c = c.replace(anchor, addition, 1)
cmake.write_text(c)

compat_src = Path("pixel11/compat/wehavephones_vulkan_compat.c")
if not compat_src.is_file():
    raise RuntimeError("Vendored WeHavePhones compatibility source is missing")
compat_dir = root / "app/src/main/cpp/wehavephones_vulkan_compat"
compat_dir.mkdir(parents=True, exist_ok=True)
(compat_dir / "wehavephones_vulkan_compat.c").write_bytes(compat_src.read_bytes())

# 3) Install the implicit layer at runtime AFTER the normal GameNative wrapper has
#    been extracted. This is the only graphics-path change from the first working APK.
xserver = root / "app/src/main/java/app/gamenative/ui/screen/xserver/XServerScreen.kt"
xs = xserver.read_text()

call_anchor = '''                            runBlocking {
                                extractGraphicsDriverFiles(
                                    context,
                                    xServerState.value.graphicsDriver,
                                    xServerState.value.dxwrapper,
                                    xServerState.value.dxwrapperConfig!!,
                                    container,
                                    envVars,
                                    firstTimeBoot,
                                    vkbasaltConfig,
                                )
                            }

                            changeWineAudioDriver'''
call_replacement = '''                            runBlocking {
                                extractGraphicsDriverFiles(
                                    context,
                                    xServerState.value.graphicsDriver,
                                    xServerState.value.dxwrapper,
                                    xServerState.value.dxwrapperConfig!!,
                                    container,
                                    envVars,
                                    firstTimeBoot,
                                    vkbasaltConfig,
                                )
                            }

                            installPixel11VulkanCompatLayer(context, envVars)

                            changeWineAudioDriver'''
if call_anchor not in xs:
    raise RuntimeError("XServer compat-layer call insertion point not found")
xs = xs.replace(call_anchor, call_replacement, 1)

func_anchor = '''private fun buildVkBasaltConfig(
'''
func = r'''private fun installPixel11VulkanCompatLayer(context: Context, envVars: EnvVars) {
    try {
        val rootDir = ImageFs.find(context).rootDir
        val library = File(context.applicationInfo.nativeLibraryDir, "libwehavephones_vulkan_compat.so")
        if (!library.isFile) {
            Timber.e("Pixel11 compat layer missing: %s", library.absolutePath)
            return
        }

        val layerDir = File(rootDir, "usr/share/vulkan/implicit_layer.d")
        layerDir.mkdirs()
        val manifest = File(layerDir, "wehavephones_vulkan_compat.json")

        val functions = org.json.JSONObject()
            .put("vkGetInstanceProcAddr", "WeHavePhonesVulkanCompat_GetInstanceProcAddr")
            .put("vkGetDeviceProcAddr", "WeHavePhonesVulkanCompat_GetDeviceProcAddr")

        val layer = org.json.JSONObject()
            .put("name", "VK_LAYER_WEHAVEPHONES_vulkan_compat")
            .put("type", "GLOBAL")
            .put("library_path", library.absolutePath)
            .put("api_version", "1.3.0")
            .put("implementation_version", "1")
            .put("description", "Routes Vulkan 1.3 BCn queries/uploads and inline shaders through GameNative wrapper fixes")
            .put("functions", functions)
            .put("enable_environment", org.json.JSONObject().put("ENABLE_WEHAVEPHONES_VULKAN_COMPAT", "1"))
            .put("disable_environment", org.json.JSONObject().put("DISABLE_WEHAVEPHONES_VULKAN_COMPAT", "1"))

        val json = org.json.JSONObject()
            .put("file_format_version", "1.0.0")
            .put("layer", layer)
            .toString(2)

        manifest.writeText(json)

        // These are the same two switches used by WeHavePhones when its layer is active.
        envVars.put("ENABLE_WEHAVEPHONES_VULKAN_COMPAT", "1")
        envVars.put("WRAPPER_NO_PATCH_OPCONSTCOMP", "1")

        // Logging only; do not alter the first APK's renderer/wrapper/BCn configuration.
        envVars.put("DXVK_LOG_LEVEL", "info")
        envVars.put("DXVK_LOG_PATH", "/sdcard/Download")

        Timber.i("Pixel11: WeHavePhones Vulkan compat layer enabled at %s", library.absolutePath)
    } catch (e: Exception) {
        Timber.e(e, "Pixel11: failed to install Vulkan compat layer")
    }
}

'''
if func_anchor not in xs:
    raise RuntimeError("Function insertion point not found")
xs = xs.replace(func_anchor, func + func_anchor, 1)

# Keep Android system navigation reachable during this experimental build.
old_ui = 'PluviaApp.events.emit(AndroidEvent.SetSystemUIVisibility(false))'
if old_ui in xs:
    xs = xs.replace(old_ui, 'PluviaApp.events.emit(AndroidEvent.SetSystemUIVisibility(true)) // Pixel 11 test safety', 1)

xserver.write_text(xs)

print("Applied Pixel 11 first-working-profile + WeHavePhones compat-layer patch")
