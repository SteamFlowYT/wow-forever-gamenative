from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")

wow = root / "app/src/main/java/app/gamenative/ui/screen/wow/WoWForeverScreen.kt"
text = wow.read_text()

replacements = {
    'var shouldAutoLaunch = true': 'var shouldAutoLaunch = false',
    'statusText = "Configuring Adreno 740 container..."': 'statusText = "Configuring Pixel 11 PowerVR diagnostic profile..."',
    'put("screenSize", "1920x1080")': 'put("screenSize", "1280x720")',
    'put("graphicsDriver", "Wrapper")': 'put("graphicsDriver", "Wrapper")',
    'put("graphicsDriverVersion", "Turnip-WoW-scheduler-test")': 'put("graphicsDriverVersion", "System")',
    'put("graphicsDriverConfig", "version=Turnip-WoW-scheduler-test,adrenotoolsTurnip=1,resourceType=buffer,bcnEmulation=auto,quality=high")':
        'put("graphicsDriverConfig", "version=System,adrenotoolsTurnip=1,resourceType=buffer,bcnEmulation=auto,quality=high")',
    'text = "Snapdragon 8 Gen 2 / Adreno 740 Edition"':
        'text = "Pixel 11 / Tensor G6 / PowerVR Diagnostic v5"',
    'CheckItem(label = "Turnip Driver & Proton 11 ARM64EC (Bundled)", ready = true)':
        'CheckItem(label = "PowerVR system Vulkan + known-good Wrapper path", ready = true)',
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"Expected text not found: {old}")
    text = text.replace(old, new)

env_prefix = 'put("envVars", "WRAPPER_MAX_IMAGE_COUNT=0 '
env_line = next((line for line in text.splitlines() if env_prefix in line), None)
if env_line is None:
    raise RuntimeError("WoW envVars line not found")
new_env = '                    put("envVars", "WRAPPER_MAX_IMAGE_COUNT=0 ZINK_DESCRIPTORS=lazy ZINK_DEBUG=compact,deck_emu MESA_SHADER_CACHE_DISABLE=false MESA_SHADER_CACHE_MAX_SIZE=512MB mesa_glthread=true WINEESYNC=0 MESA_VK_WSI_PRESENT_MODE=mailbox VKD3D_SHADER_MODEL=6_0 PULSE_LATENCY_MSEC=144 WRAPPER_LOG_LEVEL=debug DXVK_LOG_LEVEL=debug DXVK_LOG_PATH=/sdcard/Download")'
text = text.replace(env_line, new_env, 1)
wow.write_text(text)

xserver = root / "app/src/main/java/app/gamenative/ui/screen/xserver/XServerScreen.kt"
xs = xserver.read_text()

old_ui = 'PluviaApp.events.emit(AndroidEvent.SetSystemUIVisibility(false))'
if old_ui not in xs:
    raise RuntimeError("System UI hide call not found")
xs = xs.replace(old_ui, 'PluviaApp.events.emit(AndroidEvent.SetSystemUIVisibility(true)) // PowerVR diagnostic safety', 1)

marker = """        if (manualResumeMode && PluviaApp.isOverlayPaused && !showQuickMenu && !keepPausedForEditor) {
            ManualResumeOverlay(onResume = ::resumeFromManualButton)
        }
"""
if marker not in xs:
    raise RuntimeError("Overlay insertion marker not found")

emergency = marker + """
        Surface(
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = 14.dp, end = 14.dp)
                .clickable {
                    exit(
                        winHandler = xServerView?.getxServer()?.winHandler,
                        frameRating = frameRating,
                        container = container,
                        appId = appId,
                        onExit = onExit,
                        navigateBack = navigateBack,
                        reason = "Pixel 11 PowerVR emergency exit",
                    )
                },
            color = MaterialTheme.colorScheme.errorContainer,
            contentColor = MaterialTheme.colorScheme.onErrorContainer,
            shape = MaterialTheme.shapes.small,
            shadowElevation = 8.dp,
        ) {
            Text(
                text = "EXIT TEST",
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                fontWeight = FontWeight.Black,
                fontSize = 14.sp,
            )
        }

        Surface(
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(top = 14.dp, start = 14.dp),
            color = MaterialTheme.colorScheme.surface.copy(alpha = 0.86f),
            contentColor = MaterialTheme.colorScheme.onSurface,
            shape = MaterialTheme.shapes.small,
        ) {
            Text(
                text = "PowerVR v5 | known-good launch + PowerVR wrapper r5",
                modifier = Modifier.padding(horizontal = 10.dp, vertical = 7.dp),
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
            )
        }
"""
xs = xs.replace(marker, emergency, 1)

# Preserve the exact previously-working "Wrapper" selection, but replace only
# libvulkan_wrapper.so on PowerVR with upstream v0.0.5r5 after GameNative has
# extracted its normal wrapper component.
wrapper_hook = """        if (adrenoToolsDriverId !== "System") {
            val adrenotoolsManager: AdrenotoolsManager = AdrenotoolsManager(context)
            adrenotoolsManager.setDriverById(envVars, imageFs, adrenoToolsDriverId)
        }
"""
if wrapper_hook not in xs:
    raise RuntimeError("Wrapper hook insertion point not found")
wrapper_replace = wrapper_hook + """
        val rendererNameForPowerVr = GPUInformation.getRenderer(null, null) ?: ""
        val isPowerVrDevice = rendererNameForPowerVr.contains("PowerVR", ignoreCase = true) ||
            rendererNameForPowerVr.contains("Imagination", ignoreCase = true)
        if (isPowerVrDevice && graphicsDriver.equals("Wrapper", ignoreCase = true)) {
            try {
                val target = File(rootDir, "usr/lib/libvulkan_wrapper.so")
                target.parentFile?.mkdirs()
                context.assets.open("powervr/libvulkan_wrapper.so").use { input ->
                    target.outputStream().use { output -> input.copyTo(output) }
                }
                target.setExecutable(true, false)
                target.setReadable(true, false)
                Timber.i("Pixel11 PowerVR: installed bundled bionic-vulkan-wrapper v0.0.5r5")
            } catch (e: Exception) {
                Timber.e(e, "Pixel11 PowerVR: failed to install bundled wrapper r5")
            }
        }
"""
xs = xs.replace(wrapper_hook, wrapper_replace, 1)
xserver.write_text(xs)



boot = root / "app/src/main/java/app/gamenative/ui/components/BootingSplash.kt"
bs = boot.read_text()
needle = """            if (onAbort != null) {
                IconButton(
                    onClick = onAbort,
"""
if needle not in bs:
    raise RuntimeError("BootingSplash abort hook not found")
replacement = """            if (onAbort != null) {
                androidx.compose.material3.Button(
                    onClick = onAbort,
                    modifier = Modifier
                        .align(Alignment.TopEnd)
                        .padding(12.dp),
                    colors = androidx.compose.material3.ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.error,
                        contentColor = MaterialTheme.colorScheme.onError,
                    ),
                ) {
                    Text(
                        text = "ABORT LAUNCH",
                        fontWeight = FontWeight.Black,
                        fontSize = 12.sp,
                    )
                }

                IconButton(
                    onClick = onAbort,
"""
bs = bs.replace(needle, replacement, 1)
boot.write_text(bs)

print("PowerVR diagnostic v5 patch applied")
