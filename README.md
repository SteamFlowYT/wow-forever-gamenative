# WoW Forever Beta on GameNative — ARM64 / Adreno community guide

A simple GameNative setup for running Blizzard's native Windows ARM64 WoW Forever Beta client locally on Snapdragon/Adreno Android devices.

## Confirmed

- ✅ Adreno 840
- ✅ Adreno 830 — AYN Odin 3
- ✅ Adreno 740 — original RP6 setup with its original A740 Turnip driver

> The steps below are for the **Adreno 830 / 840 setup**. If you are on Adreno 740, use `turnip-wow-scheduler-test.zip` instead of the A8xx driver.

# Setup guide

## 1. Install GameNative

Download and install **GameNative 1.2.1**.

## 2. Download the required files

From the [latest release](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest), download:

- `proton-11.0-90624-arm64ec.wcp`
- `dxvk-2.4.1-wow-aarch64-test.wcp`
- `Turnip-V32-RP6sched-A8xx.zip`

Also download the normal **Windows Battle.net installer** from Blizzard.

**Do not extract the Turnip ZIP.**

## 3. Import Proton

In GameNative:

```text
Settings → Wine / Proton Manager → Import WCP Package
```

Select:

```text
proton-11.0-90624-arm64ec.wcp
```

## 4. Import DXVK

Go to:

```text
Settings → Contents Manager → Import WCP Package
```

Select:

```text
dxvk-2.4.1-wow-aarch64-test.wcp
```

## 5. Import the Turnip driver

Go to:

```text
Settings → Driver Manager → Import ZIP from device
```

Select:

```text
Turnip-V32-RP6sched-A8xx.zip
```

These custom components are needed because the stock graphics path has issues with WoW on newer Adreno GPUs.

## 6. Create one GameNative container

Add:

```text
Battle.net-Setup.exe
```

as a custom game.

**Battle.net and WoW must stay inside the same GameNative container.**

Do not create a separate container for WoW later.

## 7. Use these settings

| Setting | Value |
|---|---|
| Container | `bionic` |
| Proton | `proton-11.0-90624-arm64ec-1` |
| FEXCore 32-bit | `2609-0` |
| FEXCore 64-bit | `2609-0` |
| Graphics Driver | `Wrapper` |
| Driver | `Turnip-V32-RP6sched` |
| Use Adrenotools Turnip | **ON** |
| Display Renderer | `Vulkan` |
| DX Wrapper | `DXVK` |
| DXVK | `2.4.1-wow-aarch64-test-1` |
| WINEESYNC | **OFF** |
| Resolution | `1280x720` |

Add these environment variables:

```text
TU_DEBUG=noconform,sysmem
MESA_VK_WSI_PRESENT_MODE=mailbox
```

Start at **720p** while getting everything working.

## 8. Install Battle.net

Launch the GameNative card and install Battle.net normally.

Keep it on the default C drive:

```text
C:\Program Files (x86)\Battle.net
```

Do **not** install it to D: or Android Downloads.

## 9. Install WoW Forever

Open Battle.net inside the **same GameNative container**, sign in and install WoW Forever to:

```text
C:\Program Files (x86)\World of Warcraft
```

Let Battle.net finish the full download and update.

The ARM64 executable should then be here:

```text
C:\Program Files (x86)\World of Warcraft\_classic_beta_\WowB-ARM64.exe
```

## 10. Launch WoW directly

Download:

**[Launch-WoW-Direct.bat](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/Launch-WoW-Direct.bat)**

It launches:

```text
WowB-ARM64.exe -d3d11
```

If you use the BAT file, leave GameNative's extra arguments field empty. `-d3d11` is already included.

## 11. First boot

The first launch can stay on a black screen for a few minutes.

Give it time before assuming it has crashed.

## Updating WoW

Use the same GameNative container.

1. Launch Battle.net with **[Launch-BattleNet.bat](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/Launch-BattleNet.bat)**.
2. Let Battle.net update the existing WoW installation.
3. Close Battle.net.
4. Launch WoW again with **[Launch-WoW-Direct.bat](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/Launch-WoW-Direct.bat)**.

## Quick troubleshooting

### WoW immediately exits / `vkCreateGraphicsPipelines`

Make sure this driver is selected:

```text
Turnip-V32-RP6sched
```

### Corrupted or striped graphics

You are probably using the wrong Turnip driver for the GPU.

### Battle.net opens black or blank

Try these in order:

1. [Launch-BattleNet.bat](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/Launch-BattleNet.bat)
2. [Launch-BattleNet-disable-gpu.bat](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/Launch-BattleNet-disable-gpu.bat)
3. [Launch-BattleNet-in-process-gpu.bat](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/Launch-BattleNet-in-process-gpu.bat)

The Battle.net black-screen issue is separate from the WoW graphics setup.

## Architecture

```text
ONE GameNative card/container
        │
        ├── Battle.net on C:\
        │       └── installs / updates
        │
        ├── World of Warcraft on C:\
        │
        └── direct launch:
            WowB-ARM64.exe -d3d11
```

## More information

- [Full setup guide](GUIDE.md)
- [Compatibility](docs/COMPATIBILITY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Latest release](https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest)

## Driver

The A8xx driver is based on whitebelyash Mainline Turnip V32 / `turnip/gen8` at:

`9c7e022677dfa3abb356c2b6732cbd2e25783d01`

plus:

- the RP6 IR3 scheduler barycentric-block skip;
- Vulkan Android ICD exports for GameNative/Adrenotools.

## Original A740 driver

Adreno 740 uses:

```text
turnip-wow-scheduler-test.zip
```

SHA-256:

`02384f692735515f73aad8a544bc640abe3f35fe18e8df2e667be712c442e54c`

See `drivers/adreno-740-legacy/README.md` for provenance and warnings.

## Sources / credits

- A840 work and notes: https://github.com/arusiasotto/wow-forever-a840
- whitebelyash Mesa: https://github.com/whitebelyash/mesa-unified/tree/turnip/gen8
- Mainline Turnip V32: https://github.com/whitebelyash/AdrenoToolsDrivers/releases/tag/tu_v32
- Mesa / Freedreno / Turnip
- Wine / Proton
- DXVK
- GameNative
- Original RP6 all-in-one test work by [u/BryTheGuy06](https://www.reddit.com/user/BryTheGuy06/)

Blizzard owns World of Warcraft and Battle.net. No Blizzard game files or account data are included.
