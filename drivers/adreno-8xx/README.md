# Patched Gen8 Turnip for WoW Forever

Release asset:

`Turnip-V32-RP6sched-A8xx.zip`

Base:
- whitebelyash `mesa-unified`
- branch: `turnip/gen8`
- commit: `9c7e022677dfa3abb356c2b6732cbd2e25783d01`

WoW-specific changes:
- RP6 IR3 scheduler barycentric-block skip
- Vulkan ICD exports required by Adrenotools/GameNative

Driver metadata reports:

`26.3.0-devel-9c7e022+rp6sched`

Confirmed:
- Adreno 840 / RedMagic 11 Pro
- Adreno 830 / AYN Odin 3

For A830, use:

`TU_DEBUG=noconform,sysmem`
