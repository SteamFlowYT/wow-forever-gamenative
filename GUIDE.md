# Clean GameNative Guide — WoW Forever Beta on Snapdragon/Adreno ARM64

This guide keeps **Battle.net, the WoW install and the direct WoW launch in one GameNative container**.

That is the clean setup because Battle.net can update the same copy that GameNative launches.

## 0. Downloads

Get the release assets:
- `proton-11.0-90624-arm64ec.wcp`
- `dxvk-2.4.1-wow-aarch64-test.wcp`
- **Adreno 830/840:** `Turnip-V32-RP6sched-A8xx.zip`
- **Adreno 740 / RP6:** `turnip-wow-scheduler-test.zip`

Get Battle.net directly from Blizzard.

## 1. Import Proton

GameNative → **Settings → Wine/Proton Manager → Import WCP Package**

Select:

`proton-11.0-90624-arm64ec.wcp`

Expected installed name:

`proton-11.0-90624-arm64ec-1`

## 2. Import DXVK

GameNative → **Settings → Contents Manager → Import WCP Package**

Select:

`dxvk-2.4.1-wow-aarch64-test.wcp`

Expected installed name:

`2.4.1-wow-aarch64-test-1`

## 3. Import Turnip

GameNative → **Settings → Driver Manager → Import ZIP from device**

Select the driver for your GPU:

**Adreno 830 / 840**
`Turnip-V32-RP6sched-A8xx.zip`

Expected installed name:
`Turnip-V32-RP6sched`

**Adreno 740 / original RP6 setup**
`turnip-wow-scheduler-test.zip`

Expected installed name:
`Turnip-WoW-scheduler-test`

**Do not extract either ZIP first.**

## 4. Create ONE GameNative card

Add `Battle.net-Setup.exe` as a custom game.

From this point forward, keep Battle.net and WoW in this **same card/container**.

## 5. Configure the container BEFORE installing

| Setting | Value |
|---|---|
| Container Variant | `bionic` |
| Wine Version | `proton-11.0-90624-arm64ec-1` |
| FEXCore 32-bit | `2609-0` |
| FEXCore 64-bit | `2609-0` |
| Graphics Driver | `Wrapper` |
| Graphics Driver Version | `Turnip-V32-RP6sched` |
| Use Adrenotools Turnip | **ON** |
| Display Renderer | `Vulkan` |
| DX Wrapper | `DXVK` |
| DXVK Version | `2.4.1-wow-aarch64-test-1` |
| WINEESYNC | **OFF** |
| Screen Size | **1280×720** to start |

Environment variables:

```text
TU_DEBUG=noconform,sysmem
MESA_VK_WSI_PRESENT_MODE=mailbox
```

## 6. Install Battle.net

Launch the card and install Battle.net to the normal/default C: location:

`C:\Program Files (x86)\Battle.net`

Do not install it to D: or G:.

## 7. Open Battle.net in the SAME container

Use:

`scripts/Launch-BattleNet.bat`

If the launcher renders as a black/blank window, see [Troubleshooting](docs/TROUBLESHOOTING.md).

## 8. Install WoW Forever Beta

Inside Battle.net, install WoW to:

`C:\Program Files (x86)\World of Warcraft`

Do **not** move the final install onto D:, G:, Android Downloads or an SD-card junction if you want Battle.net Agent to patch it reliably.

Wait for Battle.net to finish completely.

Confirm:

`C:\Program Files (x86)\World of Warcraft\_classic_beta_\WowB-ARM64.exe`

## 9. Launch WoW directly

Use:

`scripts/Launch-WoW-Direct.bat`

It runs:

`WowB-ARM64.exe -d3d11`

The first launch can remain black for several minutes.

## 10. Updating later

Open Battle.net **inside the same GameNative card/container**, update WoW, close Battle.net, then direct-launch WoW again.

There is only one WoW installation.

## Notes for Odin 3 / Adreno 830

The patched A8xx driver used for Adreno 840 also works on the Odin 3's Adreno 830 in the tested setup.

Keep:

`TU_DEBUG=noconform,sysmem`

Start at 1280×720.

## Project status

This is an unofficial community compatibility project. It is not affiliated with Blizzard, Mesa, GameNative, Qualcomm or Valve.
