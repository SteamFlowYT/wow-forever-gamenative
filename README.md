# WoW Forever Beta on GameNative — ARM64 / Adreno community guide

A clean GameNative setup for running the native Windows ARM64 WoW Forever Beta client on Snapdragon/Adreno Android devices.

## Confirmed

- ✅ Adreno 840 — RedMagic 11 Pro
- ✅ Adreno 830 — AYN Odin 3
- ✅ Adreno 740 — original RP6 setup, using its original A740-oriented Turnip build

## Start here

**[Full setup guide](GUIDE.md)**

Other docs:
- [Compatibility](docs/COMPATIBILITY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [YouTube video guide outline](docs/VIDEO-GUIDE.md)

## Architecture

```text
ONE GameNative card/container
        │
        ├── Battle.net on C:
        │       └── installs / updates
        │
        ├── World of Warcraft on C:
        │
        └── direct launch:
            WowB-ARM64.exe -d3d11
```

## Components

Release assets:
- `proton-11.0-90624-arm64ec.wcp`
- `dxvk-2.4.1-wow-aarch64-test.wcp`
- `Turnip-V32-RP6sched-A8xx.zip`
- `turnip-wow-scheduler-test.zip`

Source patches are kept in `patches/`.

Launch scripts are kept in `scripts/`.

## Driver

The A8xx driver is based on whitebelyash Mainline Turnip V32 / `turnip/gen8` at:

`9c7e022677dfa3abb356c2b6732cbd2e25783d01`

plus:
- the RP6 IR3 scheduler barycentric-block skip;
- Vulkan Android ICD exports for GameNative/Adrenotools.

## Original A740 driver

The original RP6 setup used `turnip-wow-scheduler-test.zip`.

That exact binary is included in the prepared release assets and has been verified against the original bundle manifest.

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
- RP6 all-in-one test work

Blizzard owns World of Warcraft and Battle.net. No Blizzard game files or account data are included.
