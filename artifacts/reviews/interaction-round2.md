# Independent interaction retest — 2026-10-15

Current outcome: all **17 behavioral probes pass**, plus one descriptive default-path observation. Executed `node scripts/critic_interaction.mjs`; immutable output with timestamps and source hashes: [interaction-round2-output.json](interaction-round2-output.json). Original failures remain in [interaction-independent.md](interaction-independent.md) and [interaction-round1-output.json](interaction-round1-output.json).

The harness executes production app inspector handlers and scene methods, real Three.js camera math and OrbitControls, with a minimal DOM and renderer substitute. Pointer ray intersections and timers are supplied by the harness; real app drag callbacks run. This establishes logic behavior only. It does not claim browser picking, GPU rendering, rendered visual quality, actual download or video playback.

| Requirement | Retested behavior | Result |
|---|---|---|
| F08 | Numeric Y for floor object constrained to zero | PASS |
| F08 | TV numeric X constrained to cabinet footprint/top | PASS |
| F08 | Wall mounting snaps to wall and removes stale surface link | PASS |
| F08 | Shrinking support smaller than child rejected/rolled back | PASS |
| F08 | Adding surface object without a support rejected with actionable toast | PASS |
| F08 | Cabinet translation and height edit propagate to supported TV | PASS |
| F08 | Pointer drag onto incompatible rotated support rejected; original valid support retained | PASS |
| F06/F02 | Demo shared corner follows wall resize | PASS |
| F06/F02 | Demo endpoint-to-interior T-junctions stay on their supporting walls after resize | PASS |
| F06/F02 | Recognized fixture wall resize moves corresponding floor corner | PASS |
| F06/F02 | Recognized fixture T-junctions remain connected after resize | PASS |
| Editing | No-op constrained edit and rejected undersized-support edit add no undo entries | PASS, two probes |
| F10 | Panned/zoomed 2D camera restores position, target, zoom | PASS |
| F11 route quality | Eye-level route through solid partition rejected with explicit warning | PASS |
| F11 route quality | Route through demo door gap accepted | PASS |
| F11 route quality | Default elevated overview route accepted | PASS |

An additional gap was discovered during retesting: rotating the outer wall after an adjacent wall length edit originally left interior partition T-junctions behind by approximately .5m. The new independent topology probe identifies every original endpoint lying inside another wall segment, then measures its distance from that segment after the edit. Builder corrected propagation; both demo and imported fixtures now pass. This is more discriminating than checking only coincident wall endpoints.

The route default remains an elevated exterior overview (Y=3–4m over demo's 2.8m walls). That is an explicit descriptive observation, not an indoor walkthrough or video-playback pass. The solid-wall warning now prevents the specific clipping case, and the positive door-gap route guards against a blanket rejection workaround.

Required remaining evidence belongs to the integrated UI/export checks: visible support/geometry behavior, browser save/reopen framing, archive byte integrity, and independently played generated videos. These behavioral passes alone do not establish complete F02/F06/F08/F10/F11 acceptance or overall visual completion.

No production files changed by this critic. Only `scripts/critic_interaction.mjs` and `artifacts/reviews/interaction*` were written.
