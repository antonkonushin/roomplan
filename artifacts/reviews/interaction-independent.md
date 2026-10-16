# Independent interaction review — 2026-10-15

Executed `node scripts/critic_interaction.mjs` against the live local server at 20:47:28 UTC. Exact source hashes and full observations: [interaction-round1-output.json](interaction-round1-output.json). This is behavioral execution of the production `app.js` inspector handlers and `RoomScene` methods in a Node VM, using real Three.js math and OrbitControls, a minimal DOM, and a renderer substitute. It does **not** establish browser picking usability, visible rendering, download/playback, or GPU stability. No additional browser tabs were opened.

## Highest priority verified gaps

1. **F08 FAIL — numeric controls bypass all support constraints.** Select a floor object, set its Y field to 2: resulting position `[2.4,2,4.2]`, mount remains floor. Select the demo TV and set X to 20: it remains `mount=surface`, `supportId=o5`, Y=.48 while its cabinet remains at X=5.42. Change the TV mount to wall, set X=20: it stays off all walls and even retains its cabinet supportId. These are real registered input/change callbacks; not copied implementations.

2. **F06/F02 FAIL on recognized geometry — resizing a recognized boundary disconnects it from the floor and adjacent wall.** Live `/api/reconstruct` on `artifacts/fixtures/two-room-plan.png`, width 8m, height 2.7m returned w1 ending at `[7.9988,.0639]`, right wall w8 at X=7.9361, and the floor extent X=8. Increase w1 length by 1m through its production inspector handler: w1 end becomes `[8.9988,.0639]`, but w8 and all floor vertices remain unchanged. Recognition yields slightly offset centerline endpoints; editing only propagates exact .001m endpoint matches. By contrast the demo's exact shared w1/w2 endpoint propagates successfully. Passing the demo does not pass imported correction.

3. **F10 FAIL for 2D framing — orthographic camera position is lost.** After entering 2D, panning by `[2,0,1]`, zooming to 1.7 and saving settings, the ortho position is approximately `[7,25,4.251]`, target `[7,0,4.25]`. Reload through production `setProject` restores ortho approximately `[5,25,3.251]` and target `[7,0,4.25]`. `capturePoint()` serializes only the perspective position. Real OrbitControls update math is included, with event attachment and damping excluded. Main UI reproduction should pan, save ZIP, return to demo, reopen, and compare framing.

4. **F08 FAIL — support validity is not maintained for size/rotation/creation.** Shrink demo cabinet width to .1m: its TV remains 1.23m wide. With no existing support objects, adding a TV creates `mount=surface` at floor Y=0 with no supportId. Execute the real pointer drag handler with TV rotation 0 and supporting cabinet rotation π/2: drag is accepted at `[5.4,.48,4.2]` even though the TV's footprint is 1.23m along the cabinet's .4m depth. The drag check ignores child/support relative rotation. Its input ray intersection is supplied by the harness; browser hit testing is not exercised.

## Video route observation

The default path is an exterior elevated overview: its points have Y=3–4m while demo walls are 2.8m. That is valid ordinary CG overview, but does not demonstrate an indoor apartment walk.

An executed configured eye-level path `[2,1.6,2] → [8,1.6,2]` crosses the solid partition at X=5.8. The actual `walkthrough()` camera interpolation reaches `[5.822,1.6,2]` at t=.7, inside w6's wall volume. No warning or collision handling is invoked. This is a **verified route-quality gap**, not independent proof that F11's video export/playback fails: F11 accepts configured camera paths and does not explicitly require automatic navigation. If marketed as a walk through rooms, a collision warning or door-aware route is warranted. MediaRecorder and playback remain the main agent's separate check.

## Scope and suggested targeted UI reproduction

Use the existing main tab only. Reproduce the floor Y edit and imported w1 resize first; both produce unambiguous visible defects. For camera persistence, save/reopen a conspicuously panned 2D view. Current findings are production-handler output, not claims of browser UI execution. Render quality, assets/hash archive completeness, two video playback exports, and visual reference comparisons are outside this review.

No application files were changed. Critic owns only `scripts/critic_interaction.mjs` and `artifacts/reviews/interaction*`.
