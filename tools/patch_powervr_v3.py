from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src")

wow = root / "app/src/main/java/app/gamenative/ui/screen/wow/WoWForeverScreen.kt"
text = wow.read_text()

replacements = {
    'var shouldAutoLaunch = true': 'var shouldAutoLaunch = false',
    'statusText = "Configuring Adreno 740 container..."': 'statusText = "Configuring Pixel 11 PowerVR diagnostic profile..."',
    'put("screenSize", "1920x1080")': 'put("screenSize", "1280x720")',
    'put("graphicsDriver", "Wrapper")': 'put("graphicsDriver", "Wrapper-leegao")',
    'put("graphicsDriverVersion", "Turnip-WoW-scheduler-test")': 'put("graphicsDriverVersion", "System")',
    'put("graphicsDriverConfig", "version=Turnip-WoW-scheduler-test,adrenotoolsTurnip=1,resourceType=buffer,bcnEmulation=auto,quality=high")':
        'put("graphicsDriverConfig", "version=System,adrenotoolsTurnip=0,resourceType=auto,bcnEmulation=none,bcnEmulationType=software,bcnEmulationCache=0,quality=high,presentMode=fifo,vulkanVersion=1.3,gpuName=Device,blacklistedExtensions=,maxDeviceMemory=0,syncFrame=0,disablePresentWait=0")',
    'text = "Snapdragon 8 Gen 2 / Adreno 740 Edition"':
        'text = "Pixel 11 / Tensor G6 / PowerVR Diagnostic v3"',
    'CheckItem(label = "Turnip Driver & Proton 11 ARM64EC (Bundled)", ready = true)':
        'CheckItem(label = "PowerVR system Vulkan + leegao wrapper + BCn layer", ready = true)',
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"Expected text not found: {old}")
    text = text.replace(old, new)

env_prefix = 'put("envVars", "WRAPPER_MAX_IMAGE_COUNT=0 '
env_line = next((line for line in text.splitlines() if env_prefix in line), None)
if env_line is None:
    raise RuntimeError("WoW envVars line not found")
new_env = '                    put("envVars", "WRAPPER_MAX_IMAGE_COUNT=0 WINEESYNC=0 MESA_VK_WSI_PRESENT_MODE=fifo ENABLE_BCN_COMPUTE=1 BCN_COMPUTE_AUTO=0 DXVK_LOG_LEVEL=debug VKD3D_SHADER_MODEL=6_0 PULSE_LATENCY_MSEC=144")'
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
                text = "PowerVR v3 | leegao + bcn_layer | 720p",
                modifier = Modifier.padding(horizontal = 10.dp, vertical = 7.dp),
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
            )
        }
"""
xs = xs.replace(marker, emergency, 1)
xserver.write_text(xs)

print("PowerVR diagnostic v3 patch applied")
