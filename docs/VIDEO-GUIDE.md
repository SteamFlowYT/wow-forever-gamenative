# YouTube video guide outline

## Hook
> WoW Forever is running locally on the Odin 3 through GameNative using Blizzard's native Windows ARM64 client. In this guide I'm going to show the clean setup: Battle.net, updates and the game all inside one GameNative container, so there is no GameHub and no second 70 GB copy.

Show gameplay immediately.

## 1. What you need
On screen:
- GameNative 1.2.1
- Battle.net Windows installer from Blizzard
- `proton-11.0-90624-arm64ec.wcp`
- `dxvk-2.4.1-wow-aarch64-test.wcp`
- `Turnip-V32-RP6sched-A8xx.zip`
- `Launch-WoW-Direct.bat`
- `Launch-BattleNet.bat`

Explain:
> The Proton build contains the ARM64 Wine fixes, DXVK is a pure Windows ARM64 build for D3D11, and the Turnip driver is the Gen8 V32 base with the WoW scheduler workaround.

## 2. Import the components
Record each tap:

**Settings → Wine/Proton Manager → Import WCP Package**
- import Proton

**Settings → Contents Manager → Import WCP Package**
- import DXVK

**Settings → Driver Manager → Import ZIP**
- import Turnip; do not extract the ZIP

## 3. The one-container rule
On screen:

**ONE CARD — ONE CONTAINER — ONE WOW INSTALL**

Say:
> Battle.net and WoW must share the same GameNative container. A second Battle.net card creates a different C drive and Battle.net Agent cannot manage the game in the other prefix.

## 4. Create the card
Add `Battle.net-Setup.exe` as the first executable for the card.

Before launching, set:

- Container: bionic
- Wine: `proton-11.0-90624-arm64ec-1`
- FEXCore: `2609-0`
- Graphics Driver: Wrapper
- Driver Version: `Turnip-V32-RP6sched`
- Adrenotools Turnip: ON
- Renderer: Vulkan
- DX Wrapper: DXVK
- DXVK: `2.4.1-wow-aarch64-test-1`
- WINEESYNC: OFF
- Resolution: 1280×720

Environment:
- `TU_DEBUG=noconform,sysmem`
- `MESA_VK_WSI_PRESENT_MODE=mailbox`

## 5. Install Battle.net
Install Battle.net to the default C: location.

Do not put Battle.net on D: or G:.

## 6. Install WoW in the SAME container
Open Battle.net from the same card/container.

Install Forever to:

`C:\Program Files (x86)\World of Warcraft`

Do not move it afterward.

## 7. Direct launch
Use `Launch-WoW-Direct.bat`.

It starts:

`WowB-ARM64.exe -d3d11`

Keep GameNative's extra argument field empty if the BAT already contains `-d3d11`.

## 8. Updates
When Blizzard ships an update:
- use the same card/container
- launch Battle.net
- let Battle.net update the C: installation
- close Battle.net
- return to the direct WoW launcher

No copying and no second installation.

## 9. Closing warning
> This is an unofficial community compatibility setup. It is not supported by Blizzard, GameNative or Mesa. Keep backups of anything important, and expect beta/client updates to occasionally break compatibility.
