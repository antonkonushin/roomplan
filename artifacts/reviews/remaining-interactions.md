# Independent remaining interaction audit — 2026-10-16

**Two concrete defects found.** Production code was not edited; `scripts/critic_remaining_interactions.mjs` executes only the targeted checks below. It reuses the definitions of the earlier test harness without running its broad probe suite. Actual app/scene callbacks, real Three camera/groups and real localhost validation/ZIP APIs are exercised. DOM, rendering and pointer input remain substituted; no new browser observations are claimed.

Original evidence is preserved in [remaining-interactions-round1.json](remaining-interactions-round1.json), with source hashes; the current result is [remaining-interactions.json](remaining-interactions.json).

## Largest gap: malformed camera settings replace the working project before failing

Reproduction:

1. Start from a valid demo; retain the live project identity.
2. Create another valid project with a distinct name and `settings: {camera: {position: [1,2,3]}}`, deliberately omitting camera target.
3. Send to the real `/api/validate`: currently accepted.
4. Pass that validated project through actual `setProject`.

Observed: `Cannot read properties of undefined (reading '0')` when Three attempts to read the missing target. The live project has already changed to the malformed input; previous working project identity is lost. The UI import catch can display an error but cannot claim the working model was retained. This is a new verified F14 failure beyond the basic wrong-image/corrupt-ZIP/name cases that passed earlier.

Recommended fix: validate every known camera/settings structure at the backend boundary (finite 3D position/target vectors, positive bounded zoom, supported view/path enums, usable FOV, numeric light and booleans where applicable); retain unknown extension metadata only without letting it bypass known-field rules. Frontend project adoption should be transactional so a scene-build exception restores the previous model/state. Retest the exact missing-target case and a valid panned/zoomed project to guard against rejecting all settings. **Retest pending.**

## Wall inspector accepts unsaveable dimensions

Actual production numeric handlers use one `0 < value <= 30` check for all three wall fields. Python has stricter per-field limits. All rows below mutate the model and add an undo entry; actual validation then rejects the resulting project:

| Field | Entered value | Backend rejection |
|---|---:|---|
| Length | .005 m | Shorter than 1 cm |
| Height | .05 m | Outside .1–10 m |
| Height | 12 m | Outside .1–10 m |
| Thickness | .005 m | Outside .01–2 m |
| Thickness | 3 m | Outside .01–2 m |

Zero, negative, empty, nonnumeric and nonfinite length inputs are already rejected without model/undo mutation. Thus this is a specific UI/server constraint mismatch, not a blanket invalid-number failure. HTML attributes alone do not enforce correctness because the change handler does not validate them before mutation.

Recommended fix: explicit per-field limits and matching input min/max; reject before editing or atomically restore on validation failure. Give a field-specific actionable message. Do not report the old toast captured by the harness as a new rejection message: the failing handlers leave the previous toast untouched. **Retest pending.**

## Checks that did pass

- In both 2D and 3D, production master-toggle handlers change architecture/furniture to false and cloud/boxes/research/CG-camera flags to true; actual HTTP ZIP export/import followed by production applyLayers restores exactly those group visibilities. This confirms control/data/group behavior, not rendered visibility or pointer usability.
- Translated camera position and target restore in both modes; 2D also restores zoom1.7. Real OrbitControls math is included. No camera persistence defect was found for these valid settings.
- Actual `round4-edited-project.zip` loads into fresh app model state with wall w1 length9m/height3.1m. Its selected wall remains editable to9.5m/3.2m and passes real validation. This is meaningful archive/handler evidence, still not a new browser reopen screenshot.

Switching away from a view and back calls `fit()` and resets its pan to the project center. For example the panned 2D target `[7,0,4.25]` becomes `[5,0,3.25]`, while zoom1.7 persists. The 3D translated framing similarly resets. This is a reproducible UX limitation, not a new mandatory requirement: the frozen acceptance asks for stable movement/switching and save/load, not separate remembered framing for each view. It should not be misreported as the already repaired ZIP camera bug.

## Focused next actions

Fix the two verified input/adoption defects, rerun this narrow script and preserve the failing JSON. Then the lead can capture one real invalid wall edit plus one malformed-camera import to confirm visible recovery, reuse existing valid ZIP/camera evidence, and finish the already planned all-layer/2D-pan browser checks. No additional broad pass-count run is needed. Current physical-render/context diagnostics and visual acceptance remain separate.
