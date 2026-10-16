# Independent acceptance checkpoint — 2026-10-16

**Overall: PARTIAL. Mandatory functional acceptance is not yet complete.** Local GPU inference remains explicitly DEFERRED, not a defect. The existing visual FAIL remains in force; no new Floorplanner comparison or independent preference win is claimed here.

## Scope and evidence discipline

Fresh acceptance critic read `docs/USER_REQUIREMENTS.md`, `docs/acceptance.md` and `docs/quality-bar.md` before inspecting evidence. No builder conversation was provided. No production files were edited and broad tests were not rerun. This review distinguishes observations made now, prior independently recorded tests, and source-derived risks.

Current browser observations: a new background in-app browser session at `http://127.0.0.1:8765/` loaded the furnished demo successfully; its actual rendered canvas includes living area, sleeping area, kitchen appliances and bathroom. The gallery exposes 36 entries across 18 categories. Opening Layers exposes Architecture, Furniture, Point Cloud, 3D Object Bounds and **CG Camera Route**; the only empty-data explanation concerns point clouds. `/progress` loads, shows dated failed rounds and evidence links, but its summary currently says “функциональные проверки прошли”. This is too broad for the remaining scenario gaps below. Individual evidence HTTP links were not all traversed in this checkpoint.

Direct artifact inspection: `round4-edited-project.zip` opens as a ZIP; `project.json` contains w1 length **9 m**, height **3.1 m**, one retained plan source, no custom assets, and room polygon `[[0,0],[9,0],[8,5.9826],[0,5.9826]]`. This confirms the reported saved edit; it is not a combined asset project. Browser screenshot/current DOM observation is not being substituted for save/reopen or interaction evidence.

## F01–F15 map

Updated through round 5 where dated follow-up evidence is explicitly cited. Earlier issue descriptions below are retained as historical findings; the follow-up sections state which have since been repaired.

| ID | Checkpoint status | Actual evidence and remaining limit |
|---|---|---|
| F01 | PASS — supported synthetic baseline | First clean/noisy eight-segment fixture plus actual second six-segment layout are verified. `round5-assets-plan-recovery.md`: second downloaded model width9m, depth4.9807m vs5m, height2.9m, partition x6.0041m, gap1.0021m, worst endpoint error .01973m; originalPNG exact and zero furniture. Actual browser screenshot matches source layout. General photographed-plan robustness is not claimed. |
| F02 | PARTIAL | Browser save/edit failure retained in `round3-wall-edit-failure.zip`; successful fix in `round4-edited-project.zip`, plus `interaction-catalog-route.md` production-handler regression. Selected w1 edit is now directly persisted. Complete fresh-browser reopen of that corrected plan and failed-recognition retention of an existing edited scene still need a single explicit record. |
| F03 | PASS within agreed stub scope | `browser-checkpoint.md`, `round3-video-layers.jpg`, `round3-video-project.zip`, `round3-multiview-import.jpg`: explicit deterministic demo labels, furnished scene, synthetic point cloud and retained originals. MP4 byte equality and ZIP reopen are recorded. Multi-photo save/reopen byte check is not separately recorded, but no actual reconstruction claim is made. |
| F04 | PARTIAL | Current app renders a populated scene; previous UI records show both view modes and actual moving camera export. Repeated 2D/3D switching with demonstrated pan/orbit/zoom and stable picking has no complete scenario record. Do not infer this solely from presence of controls. |
| F05 | PARTIAL whole scenario; research-specific UI path PASS | `research-acceptance.md` verifies real Points/LineSegments and scene-graph independence. New screenshots show research line visible in 2D, then points-on/lines-off restored with actual GLB in 3D; downloaded ZIP preserves those states. Empty state is visible on second-plan screenshot. Independent browser toggling of every other master layer in both views remains less fully documented than the research path. |
| F06 | FAIL known UI/server dimension mismatch; prior topology repair verified | `remaining-interactions.md` proves length .005m, height .05/12m and thickness .005/3m mutate the UI model but fail server validation/save; per-field limits need repair. Zero/negative/nonfinite rejection works. Round4 ZIP loads9/3.1 and remains editable; prior connected-wall/T-junction tests remain valid. |
| F07 | PARTIAL | `interaction-catalog-route.md` constructs and places all 36 entries through production handlers; distinct geometry per pair and full data roundtrip recorded in `interaction-all-catalog.zip`. Current UI exposes these entries. **Recognizability in both rendered views for every pair** and actual browser selection are not established by geometry signatures. The combined fixture deliberately overlaps objects and cannot serve as visual evidence. |
| F08 | PASS — tested support sequence | Actual mouse-drag screenshots and downloaded project now verify floor table Y0, TV at cabinet top Y.48 with fitting footprint, then wall attachment at X5.67/Y1.2/Z5.6 on wall7 with no stale supportId. Wall-face gap is numerically zero. See `round5-functional-closure.md`; prior constraint regressions also pass. |
| F09 | PASS integration contract; GPU execution DEFERRED | `backend-provider-independent.md` executes real local API/wrapper with synthetic valid GLB, exact source/asset retention, first-image seam and portable ZIP; malformed results are rejected after a discovered structural-validation defect was fixed. Combined with browser unavailable state and actual viewer evidence, the permitted contract-fixture scope passes. Actual model inference remains deferred. |
| F10 | PASS — tested portable project and reload | Combined PNG/MP4/GLB/JSON project saved after zoom/orbit, page reloaded, ZIP opened and saved again. Independent project comparison differs only by cameraZ1.776e-15m; every other field and original file byte agrees. Before/after screenshots retain the changed camera and actual assets. See `round5-functional-closure.md`. |
| F11 | PASS — tested CG videos | Two actual distinct path videos decode45frames at1280×720/15fps/3s and have completed browser-playback evidence. New `round5-edited-overview.webm` has the same independently checked parameters; its extracted middle frame visibly contains the coffee table at its actual dragged position, closing model-edit propagation. Quality/physical-render gate stays separate. |
| F12 | FAIL visual / functional export exists | Actual SVG exports open and backend probes follow changed wall extents/openings; visual reviews identify remaining output shortcomings. No later independent visual pass. A final furnished listing after actual edit/move is still required by the frozen gate. |
| F13 | FAIL; path-traced output also functionally empty | Earlier actual stills exist and `visual-round3.md` fails the fixed bar. `round5-physical-interior.png` is 800×500 RGBA with **all four channels identically zero**: transparent empty output despite reported success. This is an unsuccessful render, not merely a low realism score. Builder correction remains under verification. |
| F14 | FAIL new malformed-camera case; basic failure set passed | Prior wrong-image/corrupt-ZIP/name cases preserve every archive byte. New `remaining-interactions.md` demonstrates missing camera target accepted by API, then actual setProject throws after replacing the working model. Known settings need validation and project adoption recovery. This supersedes the narrower earlier basic-failure pass without discarding its evidence. |
| F15 | PARTIAL; summary corrected | Initial live page loaded with history/evidence but overstated functional acceptance. Current `progress.json` at 00:26 says two videos are confirmed and end-to-end research/resource/render checks continue; it links the real playback page. This correction was read from the source, not reloaded in this critic's browser. Latest combined-asset results, empty physical-render failure and working evidence links still need final page inspection. |

Statuses describe the whole required scenario, not isolated passing subtests. A PARTIAL entry is often an evidence gap, not a newly reproduced defect.

## Highest-priority concrete issues beyond the known visual failure

### 1. Custom GLB can violate visible support; asynchronous readiness is not a portable-project pass

Evidence: source inspection of `web/scene.js`, `loadAsset()` at checkpoint. It centers mesh geometry, applies uniform `min(requestedDimension / intrinsicDimension)` scale, then places wrapper at **requested height / 2**. When width/depth limits scale, actual mesh height is smaller than requested height: the bottom floats. Example: intrinsic size `[2,1,1]`, requested `[1,1,1]` gives actual height `.5 m`, bottom `.25 m` above the object base. This is a mathematical consequence of the code, **not a newly recorded GLB browser rendering**.

Reproduction: import a portable project with a non-cubic embedded GLB, floor mount and cubic requested size; inspect side view and a still. Repeat supported placement on cabinet top. Recommended fix: define one truthful size policy (exact axis scaling or uniform scaling with effective dimensions), align transformed minimum Y to the support plane, update bounds/support footprint to the actual rendered dimensions. Verify custom mesh selection, transform edits and boxes after asynchronous replacement.

Also in inspected code: `loadAsset()` is asynchronous; rebuild does not collect its promises, screenshot does not wait, parse errors only `console.warn` and leave procedural fallback. Immediate export can therefore retain a proxy, and a corrupt GLB can look like successful loading. Add explicit pending/ready/error states, await readiness for still/video/path-traced export, discard stale loads after rebuild/project replacement, and show a labelled failure placeholder with retry/actionable detail. Avoid calling a fallback the reconstructed object.

Retest result: **NOT TESTED after fix**; lead has assigned repair separately. Require an asymmetric textured self-contained GLB, immediate export after import, fresh ZIP reopen, and malformed GLB. The existing planar triangle archive fixture proves bytes, not furniture-scale loading or material/support fidelity. Document supported embedded textures/compression; external `.gltf` resource URIs cannot be assumed portable merely because a root asset is archived.

### 2. Research output is presently only CG camera helpers

Evidence: current Layers UI, `renderLayers()` in `web/app.js`, `Scene.rebuild()` in `web/scene.js`. The `research` group is generated from `settings.walkPath` or the default route. There is no observed generic research-output import/render contract. The existing storage loop can retain arbitrary asset bytes, which is useful, but does not itself display a research result. This is a platform extension gap; future reconstruction algorithms remain intentionally stubbed.

Minimal recommended contract, independent of builder implementation:

```json
{
  "researchLayers": [{
    "id": "estimate-v1", "name": "Estimated geometry",
    "kind": "points", "visible": true,
    "units": "m", "coordinateFrame": "project-x-y-z",
    "positions": [[1, 0, 2]], "color": "#63a8a1",
    "sourceIds": ["photo-1"], "assetIds": ["research-json-1"],
    "provenance": {"method": "contract-fixture", "isSynthetic": true}
  }]
}
```

Use a documented version and explicit paired endpoints or validated indices for `kind: lines`; do not leave line connectivity implicit. Validate finite coordinates, counts, unique IDs, enum values, reference existence and color syntax. Preserve metadata and source assets in ZIP. Show independent per-layer visibility; keep CG route helpers separately named. Unknown kinds need explicit unsupported state or rejection; absence of data needs an understandable empty state. This is a proposed minimal seam, not an assertion that an expanded research framework was required.

Focused retest: two visually distinct layers (points and lines) in a furnished scene, with different visibility states. Import via supported UI/API, toggle independently in 2D and 3D while architecture/furniture/cloud/boxes stay unchanged. Save with original JSON research asset, photo, video and custom GLB; reopen in a fresh browser and inspect geometry, state, method/provenance and all byte hashes. Add one malformed coordinate/reference case proving old project retained. No broad test duplication is needed.

Retest result: **NOT TESTED**, feature being added after this checkpoint.

### 3. Close the two video routes with actual playback; retain clearance limitation

Evidence: `interaction-catalog-route.md` samples actual CatmullRom curves. Demo route moves 1.7066 m at 1.58 m eye height and has comfortable clearance; imported fixture path passes only .05389 m from a wall. The critic's .15 m clearance threshold is a quality recommendation, not a requirement retroactively added to SPEC. Record this limitation instead of calling it a proven wall collision. Generate and play both final routes after the cutaway repair; save settings and an edited project beside them. Compare chronological frames, complete scene, duration and edits. Retest result here: **pending lead's browser/video work**.

### 4. Reword progress to match demonstrated scope

Reproduction: open `/progress`; summary says “Раунд 3: функциональные проверки прошли”. Replace with wording such as “Серверные и отдельные проверки редактирования пройдены; полная функциональная приёмка продолжается”. Include F09 contract success, F10 complete fresh-session roundtrip, research overlays, F11 two-route playback and browser recovery among remaining actions, with latest dated evidence. Preserve earlier failures. Retest result: **not yet changed at this checkpoint**.

## Next acceptance checkpoint

The most efficient next evidence package is one fully populated portable project plus two videos and current exports, with a short browser record showing its new-session reopen, support movement, independent layer toggles and corrupt-import recovery. Supplement it with a genuinely different recognition layout and a readable two-view catalog contact sheet. Reuse the existing backend/handler evidence; do not replace missing integrated behavior with additional pass totals. Even successful functional closure will not close the separately failed visual gate.

## Follow-up evidence

The subsequent [research-layer and GLB retest](research-acceptance.md) verifies the implemented points/lines contract, actual Three scene-graph integration/visibility, combined archive byte identity, GLB support alignment and repaired async/error handling. It preserves two newly discovered failures and their successful retests. This is a dated follow-up, not a rewrite of the earlier checkpoint: browser end-to-end and visual gates remain separate.

## Round 5 evidence update — 2026-10-16

Inspected directly: `round5-interior.webm`, `round5-overview.webm`, first/last extracted frames for each, `round5-video-playback.jpg` and `round5-physical-interior.png`. Independent FFprobe with decoded frame counts returns the same parameters for both videos: VP9, 1280×720, 15/1 fps, 45 frames, 3.000000 s. Interior frames show eye-level parallax across sofa/table/chairs; overview frames show an elevated rotation with cut walls. The two path classes are meaningfully different. The inspected playback screenshot shows both players at the end; the lead actually operated those players, this critic did not replay them again.

Thus **the missing second actual playable route is closed**. Preserve the narrower F11 distinction: no specific wall/furniture edit was paired with these exports in the reviewed evidence, so edited-model propagation remains unproven for video. Existing routes should not be exported repeatedly merely to increase test counts; a single conspicuous edit in the next necessary capture can close this point.

The original imported-route clearance limitation has also been independently repaired: `interaction-catalog-route-round2.json` and its report record 7.6484 m motion, all 1001 samples inside the room and minimum wall-face clearance .29368 m using the unchanged .15 m critic threshold. The original .05389 m failure remains retained as history, not a current defect.

The physical still is an empty artifact: Pillow reports size 800×500, RGBA mode, extrema `[[0,0],[0,0],[0,0],[0,0]]`. Fully transparent pixels may appear black in an image viewer. Do not diagnose it as lighting from appearance alone. Reproduce with the same saved camera/project and physical-render settings, export, then independently open/check nonempty pixels and a visible scene. A success toast, elapsed samples or a valid PNG header is insufficient. Preserve this file after the repair; new output must use a new round filename. **Retest pending.**

### Remaining functional priorities, excluding the known visual comparison failure

1. **F10/F05 combined resource lifecycle — active lead check.** Complete the actual `asset-project.zip` browser open, per-layer toggles in 2D/3D, save and new-session reopen with original hashes. This is the largest still-unjoined evidence chain; contract/bytes/primitive tests already pass and should be reused.
2. **F08 direct movement/picking and support.** In that same furnished session, select and drag a floor item, a cabinet-supported TV and a wall-mounted item. Show support/cabinet rotation behavior and preserve final records. Numeric handler or injected ray tests cannot establish browser drag hit-testing. Couple this with repeated 2D/3D switches and pan/orbit/zoom for F04.
3. **F14/F02 user-visible recovery.** Start from a conspicuously edited project; attempt corrupt ZIP, missing-resource project, unsupported/failed plan image and malformed research JSON. Capture actionable UI errors and unchanged working geometry/source state. This is more valuable now than another server invalid-input matrix. Then reopen the corrected-wall ZIP and verify visible geometry in both views.
4. **F09 successful provider contract path, with inference still deferred.** The unavailable-state path is demonstrated; actual GLTF loading is demonstrated separately. A local deterministic service fixture should return a real valid GLB through `providers.reconstruct_object`, verify source/provenance retention and visible added object, then test malformed response recovery. Label fixture output synthetic. This does not require or imply installing/running SF3D inference.
5. **F01 second distinct layout — active lead check.** Finish the genuinely different plan with its known calibration and source retention. Clean/noisy variants of the first plan do not substitute. Do not broaden the claim to arbitrary real photographs.
6. **F07 complete catalog recognizability.** Two distinct geometry records per category are verified. Arrange the 36 items without overlap in two rendered views, or capture category pairs, so every item is recognizable/selectable rather than only counted. This is functional category coverage; Floorplanner realism remains a separate gate.

For F12/F11, use one conspicuous furniture/wall edit during the above work and retain the resulting listing/video, avoiding a new unrelated fixture. Refresh `/progress` with the latest links and current failures once the artifacts exist. **No overall completion claim is justified yet.**

### Later round 5 closure: second plan, combined resources and error retention

[round5-assets-plan-recovery.md](round5-assets-plan-recovery.md) independently verifies the new actual browser artifacts. F01's second-layout gap and F14's visible failure/retention gap are closed for the tested baseline. F05 research-specific toggling/display persistence and F10 combined-resource browser reopen now have direct screenshots joined with actual archive comparisons. The earlier active-gap list above is retained chronologically; those closed items should no longer be presented as pending. Full F10 still needs an explicit fresh-session/nondefault-camera execution record. General real-photo accuracy, untested glTF texture/compression cases and visual superiority remain unclaimed.

### Latest round 5 closure: direct support dragging, reload camera, edited video, provider

[round5-functional-closure.md](round5-functional-closure.md) closes F08, F09's nondeferred integration scope, F10's final camera/reload boundary and F11's edited-scene requirement using retained actual artifacts plus the provider critic's real HTTP/wrapper fixture test. The latest matrix above supersedes older pending statements in this chronological report. **Current browser stability is not asserted:** the lead reports later WebGL-context failures during physical-render diagnostics. Historical workflow passes must not mask that current regression or the unresolved visual gate.

### Subsequent focused input review

[remaining-interactions.md](remaining-interactions.md) finds two concrete new failures: mismatched wall-field bounds create unsaveable models (F06), and malformed camera settings replace the working project before a load error (F14). Those failures reopen the relevant whole scenarios while preserving earlier scoped successes. Master-layer state/ZIP/group restoration, valid 2D/3D translated camera restoration and corrected-wall ZIP editability pass in the executed nonbrowser scope. Repairs and exact retests are pending.
