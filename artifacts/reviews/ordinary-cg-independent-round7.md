# Independent ordinary-CG and PNG review, round 7

Date: 2026-10-16. Verdict: **PASS for the revised ordinary-CG still gate / F13**, on the current four actual downloaded images. No critical architecture, support, blank-output or camera-clipping defect is visible. This is a deliberately bounded acceptance of ordinary Three.js output. It is not a photorealism pass, an overall Floorplanner preference win, or a walkthrough/video acceptance.

## Scope and independence

Read the active user amendment at the top of `docs/quality-bar.md` and F13 in `docs/acceptance.md` before judging pixels. Ray tracing and physically realistic lighting/material parity are excluded. The historical photorealistic rule is not reapplied as an ordinary-CG blocker.

This critic did not implement or modify the renderer. I opened the actual files independently, including the frozen `artifacts/reference/floorplanner-dollhouse-01.jpg`. The lead reports producing all four PNGs through the app after reload; I verified the resulting files and pixels, not the download gestures myself. The comparison is **non-blind**: names, project provenance and reference identity were known. Layouts/assets differ. Native exports were inspected at 1600 × 1000; the frozen reference is a 1280 × 720 browser screenshot with margins. These are qualitative comparisons, not equal-content-area A/B scores or proof of superiority. Restored UI captures are separate evidence and were displayed proportionally reduced by the image viewer.

## Frozen evidence

Source: `artifacts/reviews/round7-final-project.zip`, SHA-256 `daa1dbd39eadf7e01fa56878843d2da1be3d399986f9f994ccf9d871b8dccfa6`.

Independently read its `project.json`: 11 walls, 24 objects; coffee table `o3` at `[2.9, 0, 4.1]`; wall `w5` height 3.1 m and thickness 0.22 m. TV `o6` has `supportId: o5` and y = 0.48 m, matching the cabinet height. Saved interior camera height is approximately 1.55 m, FOV 58 degrees. The current stills visibly place the coffee table to the right of the rug centre and preserve the same furnished layout. Wall height itself cannot be inferred from a cutaway still; archive values provide that separate check.

| Actual PNG | Dimensions | SHA-256 |
|---|---|---|
| `round7-hires-dollhouse.png` | 1600 × 1000 | `705a2ac038a3b1e009e6f1c679bf6b509a48d6ce9cbc59cda9fd3546f2ed0b31` |
| `round7-hires-dollhouse-alt.png` | 1600 × 1000 | `85af6298915e2145aa7ce47f6ab2976f53098dce33f1ea5f063dbd2f47616c27` |
| `round7-hires-interior.png` | 1600 × 1000 | `440fe5e52da9ccbe61d31dc20e9c901fe3a907af036d9f3cc573897614a90fdb` |
| `round7-hires-top.png` | 1600 × 1000 | `b45b39dd103c07c7c4881e5ddbba8a2fad4e993da3c480f1f574b968f2e219ab` |

All filenames above are under `artifacts/reviews/`. Preceding `round7-final-*` portrait images remain historical evidence; they are not substituted for these final exports.

## Pixel findings

**Dollhouse, both angles: PASS.** Joined outer walls and internal partitions make the four room zones readable. Door gaps remain open. The bedroom bed, bedside cabinets, wardrobe, bathroom tub/toilet/basin, kitchen sink/stove/fridge and living/dining furniture are identifiable from their geometry. Cushions, chair backs/legs, appliance faces and basin interiors provide sufficient category detail for ordinary CG. There is no floating slab or visible furniture-through-floor failure. The first angle partly hides the TV with the hall wardrobe; the second angle exposes the screen and its supporting cabinet. That is ordinary occlusion, not missing geometry. The complete footprint stays inside both images.

**Interior: PASS.** The camera is plausibly at human eye level. Ceiling, two walls, floor, window and curtains form a complete enclosure. Sofa and chair cushions, lamp, plant, coffee table, books and tableware read clearly; furniture feet and surface support are visible. The clipped edges of the coffee table/art/dining furniture at the image boundary are normal framing, with no near-plane slice through the central furniture or wall/ceiling hole. Softer edge antialiasing and simple surfaces remain visible at native size, but the central subjects are usable and legible. No UI, helper boxes, dimension overlays or selection outline contaminates the export.

**Top PNG: PASS as a supplementary furnished overview.** The apartment, entrance swing and outer boundaries fit with margins. Room partitions, openings and furnishing use are clear. Refrigerator/wardrobe tops are plain blocks, while their identity is established by the two 3D angles; this is a top-view representation limitation. This review does not replace the separate SVG listing-plan acceptance.

**Reference comparison, restricted to the applicable criteria.** FP-DH-01 has a more balanced use of the frame and exposes its TV/desk/shelving more immediately. Current RoomPlan also supplies joined rooms, recognizable furniture, supported objects and readable depth. It does not need the reference's material or lighting realism for this gate. I do not establish a visual preference win: on framing alone I prefer the frozen reference; recognition and integrity are adequate in the candidate's paired views. Differences in scene complexity and furnishings prevent a controlled renderer ranking.

## Biggest remaining gap and concrete retest

The largest remaining visual weakness is **overview framing**, a nonblocking refinement. In both dollhouse PNGs the apartment occupies the lower part of the canvas: approximately the first quarter of the image is empty, while the lower boundary has a much smaller margin. The default angle also gives the tall hall wardrobe a prominent central silhouette. It is usable, but less composed than FP-DH-01. The alternate view substantially improves TV/living-area visibility.

Reproduce: reopen the frozen ZIP, enable cutaway, reset/orbit to the two recorded overview orientations, export PNG, and compare upper/lower visible-footprint margins. Recommended refinement: fit and vertically centre the projected visible footprint, with a stable small margin, and favour an overview angle that exposes the living zone. Preserve the full footprint and leave the interior pose unchanged. Retest result for the current implementation: the new independent-size PNG export **passes usable framing and complete-footprint checks** at both angles; unequal margins remain. No implementation change was made by this critic.

## Export and restoration checks

Independently ran `node tests/test_png_export.mjs`: **PASS**. It exercises production `screenshot()` with real Three.js camera/geometry maths and a renderer double, checking 1600 × 1000 default and 1920 × 1080 custom output, perspective/orthographic fit, unchanged interior pose/FOV, state restoration after success and PNG-encoder failure, immediate editor redraw, and the recording guard. This is not a GPU rendering test; actual pixels above supply that evidence.

Read `web/scene.js:65–94` and `renderFrame()`. Export uses a cloned camera and leaves the controls' original camera/target untouched. It saves/restores renderer dimensions and ratio, viewport/scissor/render target, composer size/ratio, helper visibility and camera references in `finally`; the final immediate redraw restores the visible editor and the original dirty flag. For 3D, the immediate redraw also refreshes SSAO projection uniforms from the restored camera. No material state-restoration defect found in the normal app path. Arbitrary WebGL/context-loss recovery is outside this test.

Inspected `round7-hires-restored-ui.png` and `round7-hires-restored-interior-ui.png`: both show populated restored portrait editor viewports and the successful PNG-download toast. The interior UI preserves its narrower portrait framing while its downloaded PNG has a useful landscape view. The lead additionally reports subsequent mode-switch/orbit/reset responsiveness; that interaction report is corroborative, not independently replayed here.

Renderer source SHA-256 at review: `ffee1295da429dc8f931598a8f3fbefae2cd81b9ddf01e6ad460e306f9b90cd3`.

Final status: **F13 ordinary-CG stills PASS; PNG export/restoration PASS within the tested paths; photorealistic parity and overall superiority not claimed.** Remaining framing polish is documented above. Video playability and other functional gates belong to their own reviews.
