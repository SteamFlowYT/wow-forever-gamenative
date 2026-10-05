# Troubleshooting

## First launch is black for several minutes
The first WoW launch can sit on a black screen while shaders/cache are prepared. Give it time before assuming it has failed.

## `vkCreateGraphicsPipelines` / silent Proton abort
Confirm you selected the patched `Turnip-V32-RP6sched` driver, not stock V32.

## Stripe garbage / corrupted picture
You are likely using a Turnip base that does not render correctly on your GPU family.

For A830/A840 use the patched Gen8 V32 driver.

## A830 rendering issues
Use:

```text
TU_DEBUG=noconform,sysmem
```

## 1080p causes the pipeline assert again
Start at 1280×720. The A840 test found 1920×1080 triggered a different shader set and brought the pipeline failure back.

## Battle.net black/blank window
Battle.net's Chromium UI can be unreliable in Wine/GameNative.

Try, in this order:

1. `scripts/Launch-BattleNet.bat`
2. `scripts/Launch-BattleNet-disable-gpu.bat`
3. `scripts/Launch-BattleNet-in-process-gpu.bat`

If Battle.net launches but remains blank, also try launching `Battle.net.exe` rather than `Battle.net Launcher.exe`.

## Battle.net cannot update / folder-access error
Battle.net, Agent and WoW must live in the **same GameNative container/prefix**.

Recommended WoW path:

```text
C:\Program Files (x86)\World of Warcraft
```

Do not make a second GameNative card for Battle.net. Do not move the final install to Android shared storage if you want Battle.net to update it in place.
