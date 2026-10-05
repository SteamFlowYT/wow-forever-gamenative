# Compatibility

| GPU | Example device | Driver | Status |
|---|---|---|---|
| Adreno 840 | RedMagic 11 Pro | Patched Gen8 V32 | ✅ Confirmed in-world |
| Adreno 830 | AYN Odin 3 | Patched Gen8 V32 | ✅ Confirmed in-world |
| Adreno 740 | Retroid Pocket 6 | `turnip-wow-scheduler-test.zip` | ✅ Confirmed by original RP6 setup |
| Adreno 750 / 730 | Snapdragon 8 Gen 3 / 8 Gen 1 family | Not validated here | 🧪 Needs testing |
| Adreno 6xx | Snapdragon 865/888-era devices | Not validated here | 🧪 Needs testing |

## Important

The scheduler workaround is in common IR3 compiler code, but a driver that compiles shaders is not automatically a correct driver for every GPU family. The original A740-oriented driver compiled WoW shaders on A840 but produced stripe corruption. Use a base appropriate for the GPU generation and validate on real hardware.

whitebelyash Mainline Turnip V32 documents support for A8xx, upstream-supported A7xx, and upstream-supported A6xx. A830 has known GMEM issues and should use sysmem.
