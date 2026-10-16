# Independent catalog, route and save lifecycle review

Run: `node scripts/critic_interaction_catalog_route.mjs`. Latest result: **25/25 checks PASS** after the clearance correction. Production `app.js` handlers, actual Three.js geometry constructors and actual CatmullRom camera curves; immutable final evidence in [interaction-catalog-route-round2.json](interaction-catalog-route-round2.json). Texture canvases and GPU rendering are substituted; this does not establish visual recognizability, browser picking or video playback. The existing interaction probes are rerun as a prerequisite.

## Catalog placement and persistence

**PASS in executed model/geometry scope:** all 18 categories provide two entries, and all 36 production `makeFurniture()` constructions contain meshes with distinct transformed vertex geometry within each category. This is stronger than distinct IDs or names, but is not an aesthetic judgment.

Every entry was added through production `addObject()` and moved through its numeric inspector in a fresh demo. Floor objects remain at Y=0; both TVs acquire the real cabinet `o5` as support and fit its footprint/top. All 36 objects plus the required cabinet were combined into a persistence fixture, exported through the real ZIP API, imported, and loaded into app state. Full object records, including dimensions, positions, rotation and support links, match exactly. Artifact: [interaction-all-catalog.zip](interaction-all-catalog.zip).

The combined archive deliberately contains overlapping placements copied from independent tests; it is a persistence fixture, not a proposed apartment layout or rendered catalog sheet. F07's visible 2D/3D recognizability remains a separate visual check. Wall mounting is covered by the earlier actual inspector-handler test, since no catalog entry has wall as its default mount.

## Interior route

The production `#walkthrough-button` and `#interior-path` handlers create a real interior route, set full walls and FOV=58, and save `walkPathMode=interior`. Mode and points survive settings reload. The overview button produces a different elevated route.

The demo route travels **1.7066m** at eye height **1.58m**. Independently sampled at **1001 points on the actual CatmullRom curve**, it remains within the living room, has minimum wall-face clearance **1.07m** and minimum furniture-footprint clearance **.717m**. It is not a stationary-camera workaround.

The initial imported two-room fixture route travelled **7.9917m** and did not literally intersect a wall, but passed only **.05389m** from an internal wall face. It failed the critic's independently chosen **.15m minimum clearance** for a usable eye-level route. That margin is a quality criterion, not a numerical requirement stated in SPEC.md. Initial evidence is retained in [interaction-catalog-route-round1.json](interaction-catalog-route-round1.json).

After the builder added clearance checks against all internal wall segments, independently retested with the same criterion and 1001 actual-curve samples: the imported route travels **7.6484m**, remains within the floor polygon, and has minimum wall-face clearance **.29368m — PASS**. Demo route metrics remain unchanged. The path was changed to avoid the tight gap; the test threshold was not reduced. The imported fixture has no furniture, so its furniture-clearance field is explicitly null.

## Save → edit selected wall → save regression

The lead's real browser check uncovered a lifecycle defect absent from the earlier no-save geometry probes: validation replaced the live project object during save, leaving selected inspector/scene references stale. The builder changed save to export a validated snapshot without rebinding the live model.

Independent regression now **PASS**: select imported w1, invoke the actual Save handler, edit that same selection to length **9m** and height **3.1m**, then invoke Save again. Project, scene and selected-wall object identity remains consistent; generated inspector fields read **9.00 / 3.10**; live geometry and the second actual ZIP both contain the same **9m / 3.1m** wall. Only the download sink is intercepted; validate/export/import APIs execute normally. Artifact: [interaction-save-edit-wall.zip](interaction-save-edit-wall.zip).

This pass directly covers the new lifecycle regression. It does not retroactively turn earlier 17 probes into browser-save evidence; the missing scope and original browser failure remain explicit.
