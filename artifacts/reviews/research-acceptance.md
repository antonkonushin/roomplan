# Independent research layers and custom-asset retest — 2026-10-16

**PASS within the executed contract/geometry scope. Full browser acceptance remains PARTIAL.** The new data-backed research layers and custom-GLB corrections materially close the implementation gaps identified in `acceptance-checkpoint.md`. No browser upload, rendered-pixel, picking, texture-fidelity or overall visual pass is claimed by this report.

Evidence is reproducible with `scripts/critic_research.py` and `scripts/critic_research.mjs`. Only critic scripts and review artifacts were written. Tests execute the production Python validator/archive code and actual Three.js `Points`, `LineSegments`, `GLTFLoader`, `RoomScene.rebuild`, `applyLayers`, `loadAsset`, `awaitAssets` and `screenshotAsync` methods. Scene construction is headless: no WebGL renderer is created; the readiness probe replaces only the final screenshot sink. Source hashes and detailed numerical results are recorded in [research-geometry.json](research-geometry.json).

## Contract and archive

The Python audit records 50 scoped checks in [research-contract.json](research-contract.json). This total is not a substitute for F05/F10 end-to-end acceptance.

- Version, ID, name, kind, visibility, units, coordinate frame, color, position shape, boolean coordinates, nonfinite/out-of-range coordinates, provenance type, source/asset references and duplicate references are checked with rejected inputs.
- Lines reject absent connectivity, out-of-range/equal endpoints, boolean/float indices and malformed pairs. Points reject line segments. Duplicate layer IDs, nonobject entries, excessive layers, per-layer points and aggregate point counts are rejected.
- A valid two-layer project is not mutated by validation. Changed per-layer visibility, camera-helper visibility, nested provenance metadata and the complete project survive direct ZIP save/load exactly.
- The current local HTTP server imports that same archive with equal project data. An invalid line index returns **400 application/json** with an actionable error.
- The archived PNG, MP4, GLB and JSON equal both their original fixture files and the independently re-exported archive bytes. [research-roundtrip.zip](research-roundtrip.zip) retains the combined project; [research-project.json](research-project.json) is the decoded comparison artifact.

| Original | Bytes | SHA-256 |
|---|---:|---|
| two-room-plan.png | 3937 | `d03cc8399f49e25e8afa40f4dc5be3c11d41bf0bc67f5b20d5953350a01a63da` |
| synthetic-walkthrough.mp4 | 49176 | `ad97a3993027c530f30d77b9e2dc7ff13e6fd878ef3c0009ec84a25fc0ff7239` |
| wide-test-object.glb | 988 | `e79fe7558c2f8ccaa71efb33518042ab8f76a79ed28e240c7552f331cb2de282` |
| research-layers.json | 1858 | `08abb816cfed3c5c710a606b9791a75bf1a54dab1e811e22f65fe2f6abf0c6db` |

## Real Three primitives and visibility

[research-geometry.json](research-geometry.json) records 20 scoped checks. Production `buildResearchLayers` creates an actual six-vertex `Points` object and actual `LineSegments` with the expected four positions and five explicit indexed segments. Coordinates agree within Float32 precision; IDs, asset references and nested provenance are copied. Production `rebuild` inserts both primitive types into the research group and a distinct `CameraHelper` into the CG-camera group.

Executed `applyLayers` in both `mode='2d'` and `mode='3d'`: one layer hidden and the other visible, research master off/on, and CG-camera helper off independently. Effective visibility of actual descendants follows the intended switches; architecture, furniture, cloud and bounds flags stay unchanged. This proves scene-graph behavior, not visible line width, depth occlusion, contrast or usability in a rasterized view.

Source inspection of `renderLayers`/`showResearchImport` shows separate master and per-layer controls, an explicit empty state, retained original JSON asset, validation of the staged project before `setProject`, and error text in the modal. Those UI handlers were **not driven in a browser in this retest**; malformed-import preservation of the visible working scene remains the lead's integrated check.

## GLB and asynchronous export

The real GLTFLoader parses the asymmetric fixture with intrinsic dimensions 3 × .5 × 1 m. Production placement with requested dimensions 1 × 1 × 1 m produces bounds `[-.5,0,-.5]` to `[.5,1,.5]`. Setting object base Y to `.48` produces mesh bottom `.48` and top `1.48`. The previous float caused by uniform scaling plus requested half-height is therefore repaired for this actual geometry. Current policy is per-axis dimension fitting, which can change proportions; it is not uniform physical-scale recovery.

Malformed GLB now sets an error, emits both the configured callback and asset-error event, and prevents `awaitAssets`/beauty screenshot completion. Stale successful parsing cannot attach to a replacement furniture group. Screenshot waits until the tracked pending resource settles.

Two additional genuine defects were found, sent to the implementer, repaired and retested:

1. **Awaiting stale generation.** Start screenshot while pending set A is unresolved; rebuild/project replacement supplies set B; resolve A while B stays pending. Previously the screenshot sink ran early. Current generation-aware loop waits for B. The regression uses controlled promises with the same deletion lifecycle as real tracked parse jobs; no browser timing assumption is required.
2. **Silent unsupported resource.** Link an object to an asset named `research.json` with MIME `application/json`. Previously `loadAsset` returned without a state/error and left an opaque proxy eligible for export. Current code emits the explicit unsupported-resource error and blocks readiness/export. Arbitrary JSON research assets remain valid archive assets; referencing one as rendered custom geometry no longer appears to succeed.

Initial failures are preserved in [research-geometry-round1.json](research-geometry-round1.json); final passing retest is [research-geometry.json](research-geometry.json). A test-harness ArrayBuffer realm mismatch was corrected before the first recorded geometry run; it was not a production GLB defect. No production files were modified by this critic.

## Remaining acceptance boundary

Largest remaining gap: **the combined archive has not been reopened and exercised in a fresh actual browser by this critic**. Reproduce with `artifacts/fixtures/asset-project.zip` or the retained roundtrip ZIP, verify the custom mesh and both research overlays visibly in 2D/3D, change each layer independently, move the mesh on a valid support, save, reopen and compare the current camera/support/layers/provenance. Use an invalid research JSON and invalid custom asset to confirm actionable UI errors and retention of the working scene. Record actual still/video exports following immediate import.

This fixture has a basic material and no texture image. Embedded texture loading, supported compression, external glTF dependencies and textured furniture recognizability remain untested. The proposed platform seam is now implemented for metric points/lines, not arbitrary neural representations. F05/F10 improve to implementation-and-contract verified but remain **PARTIAL** until browser evidence joins these data checks. F09 inference remains explicitly DEFERRED; this audit does not prove successful SF3D-provider inference or its fixture response route. Existing visual FAIL and two-route video evidence obligations remain separate.
