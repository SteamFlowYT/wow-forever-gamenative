# Release assets

The large compatibility binaries should be uploaded to a GitHub **Release**, not committed directly to Git.

Use these asset names:

- `proton-11.0-90624-arm64ec.wcp`
- `dxvk-2.4.1-wow-aarch64-test.wcp`
- `Turnip-V32-RP6sched-A8xx.zip`
- `turnip-wow-scheduler-test.zip` (original A740/RP6 driver)
- `SHA256SUMS.txt`

The Proton WCP is over GitHub's normal 100 MB Git blob limit, so a Release is the appropriate place for it.

The GitHub Pages download buttons in `index.html` are configured for:

`https://github.com/SteamFlowYT/wow-forever-gamenative/releases/latest/download/<asset>`
