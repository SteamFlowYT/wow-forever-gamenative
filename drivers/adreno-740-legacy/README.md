# Original RP6 / Adreno 740 driver

Release asset:

`turnip-wow-scheduler-test.zip`

This is the **original binary from the RP6 all-in-one test bundle**, supplied later and verified against the bundle manifest.

Credit for the original RP6 all-in-one test work goes to Reddit user **[u/BryTheGuy06](https://www.reddit.com/user/BryTheGuy06/)**.

SHA-256:

`02384f692735515f73aad8a544bc640abe3f35fe18e8df2e667be712c442e54c`

Embedded metadata:

- name: `Turnip-WoW-scheduler-test`
- Mesa base: `fe067b17d9`
- driver version: `26.1.99-fe067b17d9-wow-test`
- patches: IR3 scheduler fix + diagnostic/ICD patches

This driver was the one used by the confirmed Retroid Pocket 6 / Adreno 740 setup.

## Important

Do **not** use this A740-oriented build on A830/A840. On A840 it could compile shaders but produced stripe corruption/stalls.

For Adreno 830/840, use:

`Turnip-V32-RP6sched-A8xx.zip`
