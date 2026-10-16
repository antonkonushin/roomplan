# Round 5 independent artifact audit — assets, second plan and recovery

Date: 2026-10-16. This critic independently opened the downloaded ZIPs, compared original bytes/project records, and viewed the actual browser screenshots supplied by the lead. The lead executed the UI interactions; this critic does not claim to have repeated them. Production files were read only.

## Second genuinely different layout: F01 supported baseline PASS

The fixture `wide-two-zone-plan.png` is a 9 × 5 m rectangle with a partition at x=6 m and a central 1 m gap. This differs from the first 8 × 6 m, eight-segment fixture. Expected centerlines were independently derived from the fixture drawing coordinates in `scripts/create_second_plan.py`, checked against the image and `wide-two-zone-plan.expected.json`, then matched to all six actual downloaded wall segments by minimum maximum endpoint error over possible assignments.

| Property | Expected | Downloaded `round5-second-plan.zip` |
|---|---:|---:|
| Wall segments | 6 | 6 |
| Width | 9 m | 9 m |
| Depth | 5 m | 4.9807 m |
| Partition x | 6 m | 6.0041 m |
| Gap | 1 m | 1.0021 m |
| Ceiling / every wall height | 2.9 m | 2.9 m |
| Furniture count | 0 | 0 |
| Worst matched endpoint error | Previous critic tolerance .15 m | **.0197307 m** |

The source PNG in the downloaded ZIP equals the original fixture bytes, SHA-256 `4f761a35c2aec3198af33c787ed3621eb19c30b9d6fd8825ba25f718bc73f14d`. Provenance names `threshold-axis-line-baseline-v1`, metric centerline calibration and `bounding-envelope-estimate`; the output is not a demo substitute. The actual browser screenshot `round5-second-plan.png` visibly matches the outer walls and gapped partition and shows ceiling 2.9 m. There is one approximate envelope floor, not claimed room segmentation.

Together with the first clean/noisy layout and explicit rejected skewed/blank inputs, this closes F01's **supported synthetic baseline**. It does not establish general photographed-plan accuracy, rotated walls, room segmentation or furniture recognition. Detailed wall matches and original byte evidence: [round5-independent-archive-audit.json](round5-independent-archive-audit.json).

## Combined asset archive: data and visible roundtrip confirmed

Direct comparison of `artifacts/fixtures/asset-project.zip` with the actual browser download `round5-assets-saved.zip` confirms:

- All four retained files (PNG, MP4, GLB, research JSON) equal both the original archive bytes and standalone fixture files. Hashes match the earlier independent research report.
- Walls, rooms, objects, openings, pointCloud, provenance, source records and asset records are unchanged. All 25 object records survive, including TV `o6` supported by cabinet `o5` at Y=.48 m.
- The research master is true, points layer `qa-observations` is true, lines layer `qa-wall-hypothesis` is false. Per-layer positions, connectivity and provenance remain intact.
- Saved view is 3D with explicit camera/orthographic camera, FOV, zoom, light, labels and cutaway settings. The artifact alone does not prove the camera was deliberately panned/zoomed away from its default before save.

The inspected `round5-research-2d.png` shows the actual custom red mesh footprint and blue line overlay; points are off and lines on. `round5-assets-reopened.png` shows the custom mesh in 3D after reopen, points on and lines off, matching saved state; scene furniture and architecture remain present. The 3D points are small and partly occluded, so this image is not a contrast/readability benchmark. Real GLTFLoader/primitive tests already establish that the custom fixture is loaded geometry rather than a procedural substitution.

**F05 research-specific import/display/toggle persistence: PASS within this fixture scope.** Its remaining whole-scenario gap is direct browser evidence for independently toggling every other layer in both views; real scene-graph checks already pass. **F10 combined data/asset/UI reopen path: PASS within the recorded roundtrip.** Lead clarification: the initial asset archive was loaded after a page reload; the subsequent saved archive was reopened within that same application session. Camera framing was not deliberately changed beyond switching views. Reload-before-reopen of the newly saved state and deliberate nondefault camera framing are the remaining narrow checks. No persistence failure was found.

## Recovery: F14 tested failure set PASS

The lead reports actual UI missing-file prompt, failed image decoding, corrupt ZIP and malformed project validation. This critic inspected:

- `round5-invalid-image.png`: existing second-plan scene remains behind a modal with explicit PNG/JPEG decoding error.
- `round5-corrupt-zip.png`: same scene/source remains, visible archive-open error.
- `round5-malformed-project.png`: same scene/source remains, visible project-name validation error.

Most decisively, the subsequent actual download `round5-after-errors.zip` has exactly the same entry names and **every entry's bytes equal** `round5-second-plan.zip`, including `project.json`, original PNG and README. This independently proves the working model and source remained intact after that failure sequence, beyond what screenshots alone show. Evidence: [round5-error-retention-audit.json](round5-error-retention-audit.json).

Combined with prior backend JSON-error and missing-asset rejection probes, the required basic failure/recovery behavior is supported. These are scoped fixture passes; exotic malformed archives and actual GPU-service errors are not newly tested. Malformed research JSON visible recovery remains an optional extension-specific confirmation, with its validator/HTTP rejection already independently tested.

## Remaining work

The prior requests for a second distinct layout and byte-backed recovery are now closed. Do not keep them in the active gap list. For the combined project only narrow the fresh-session/camera evidence boundary, rather than redoing bytes or geometry tests. Remaining functional focus: actual floor/surface/wall drag interaction, successful local-provider contract fixture, and visible catalog-pair coverage. Video edited-scene propagation and the empty physical-render output still need their already identified retests. No overall completion or visual acceptance is claimed.
