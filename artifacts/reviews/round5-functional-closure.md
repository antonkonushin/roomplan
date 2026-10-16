# Independent scoped functional closure — 2026-10-16

This review inspects retained actual UI screenshots, downloaded ZIPs/video and the independent provider report. It does not assert current browser/WebGL availability: the lead reports context-creation failures following later physical-render probes. Historical successful workflows remain evidence for the captured revision, while the current rendering regression must be tracked separately. Production files were not edited.

## F08: PASS, tested floor/surface/wall movement

The lead executed real mouse drags; this critic inspected `round5-floor-drag.png`, `round5-surface-drag.png`, `round5-wall-drag.png` and decoded `round5-dragged-project.zip`.

- Floor table Pebble moves from the lead-recorded `[2.35,0,4.1]` to `[3.65,0,4.3]`. Screenshot inspector and saved object `o3` agree; floor Y remains zero.
- Surface TV screenshot reads `[5.55,.48,5.3]`, mount surface, rotation90°. Cabinet `o5` is at `[5.42,0,5.4]`, size `[1.8,.48,.4]`, rotation90°. TV bottom equals cabinet top. In cabinet axes, horizontal offsets `.13` and `.10` plus TV half-extents `.05` and `.615` give `.18 <= .20` and `.715 <= .90`: its footprint fits the supporting top.
- After switching to wall and setting Y1.2, real drag yields `[5.67,1.2,5.6]`, rotation−90°, `mount=wall`, `wallId=w7`, no stale `supportId`. Wall7 lies at X5.8 with thickness .16. TV depth .10 gives wall-facing surface X=`5.67+.05=5.72`, exactly wall face `5.8-.08=5.72`; the numerical residual is ~1e-16 m. It moves along the wall and stays attached.

Together with prior rejection/propagation tests, this closes the missing actual picking/drag sequence for the stated three supports. The sequence was captured in 2D; it does not establish unrestricted collision-free furniture placement or every possible support geometry.

## F10: PASS, combined resources plus changed camera after reload

The lead changed the full-asset scene by zooming twice and orbiting, saved `round5-camera-saved.zip`, **reloaded the page**, opened the saved ZIP, then saved `round5-camera-reopened.zip`. The inspected before/after PNGs retain the same visibly nondefault framing and actual red GLB/research points.

Independent recursive comparison of both `project.json` files finds exactly one difference: camera Z `11.257491594303511` versus `11.257491594303513`, magnitude **1.7763568394002505e-15 m**. This is ordinary floating-point camera update noise, not meaningful drift. Every other field is identical: geometry, support links, research visibility/provenance, camera target/FOV, orthographic settings, scene settings and file records. All four PNG/MP4/GLB/JSON originals plus README are byte-identical between archives. Earlier comparison already establishes equality to standalone source fixtures.

Detailed independent comparison and saved drag records: [round5-camera-drag-audit.json](round5-camera-drag-audit.json). This closes the previously missing fresh-app-state/nondefault-camera portion of F10. It does not extend GLB support to untested textures/compression or arbitrary external glTF dependencies.

## F11: PASS, two routes and visible model-edit propagation

The previously verified interior/overview videos establish two different moving camera paths, full browser playback and fixed video parameters. The new actual `round5-edited-overview.webm` independently probes as VP9, 1280×720, 15 fps, 45 decoded frames, 3.000 s.

The inspected `round5-edited-overview-middle.png` shows the coffee table moved away from its original centered-on-rug location into the new position from the real drag; furniture/accessories move with it. Comparison with earlier overview frames and saved object coordinates makes the edit identifiable. This closes the previously narrow missing edited-model propagation evidence. The edited video's full browser playback is not repeated here; decoding and visible extracted scene are verified, and both prior path classes were actually played to completion.

## F09: PASS integration contract; actual GPU execution DEFERRED

`backend-provider-independent.md` records real app/API and service-wrapper execution on temporary loopback ports using a clearly synthetic fixture CLI, exact original-image and returned-GLB bytes, first-image forwarding, bound custom object, portable HTTP ZIP roundtrip and failure paths. The reviewer found acceptance of a truncated `glTF` prefix, reported it, and retested structural validation after repair. Its 21 probes cover these concrete contracts; they are not counted as GPU inference evidence.

Together with the actual browser unavailable-state/source-retention evidence and separately verified GLB viewer, this meets the explicitly permitted contract-fixture integration scope. **No model weights, installation, CUDA inference, reconstruction quality or GPU performance are claimed tested.** The user's deferred execution remains deferred.

## Current acceptance consequence

F08, F09's nondeferred contract, F10 and F11 can leave the active functional-gap list for the tested scope. Existing F01/F03/F14 baseline passes remain. Remaining work should focus on the current WebGL/physical-render regression, complete visible catalog coverage, final all-layer/camera interaction evidence and the still-failed visual/listing gate. Do not report the current application globally stable from these earlier successful captures. Physical-render success requires nonempty independently opened pixels and a working editor afterward.
