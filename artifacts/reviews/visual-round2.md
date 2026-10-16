# Independent visual review — round 2, 2026-10-15

**Verdict: visual gate FAIL; no Floorplanner win established.** Dollhouse is usable as a stylized spatial model. Interior output is materially below the fixed reference in composition, materials, object detail and lighting. Listing export is readable but schematic and exposes a blocked doorway. Functional test results belong to separate reports.

## Evidence and limits

Lead operated the real UI and downloaded `round2-dollhouse.png`, `round2-interior.png` (both 2036 × 1364) and `round2-listing.svg` (1200 × 980). `round2-editor.jpg` (2560 × 1440) shows the furnished demo in the app. Critic directly inspected both PNGs and editor screenshot using image viewing. Lead subsequently rendered the SVG in the browser as `round2-listing.jpg` (2400 × 1960 capture with actual SVG in upper-left and unused white margin). Critic inspected that rendering too; the capture margin is not counted as an SVG defect. This is independent pixel review of actual outputs, not independent UI execution: the critic browser had no available surfaces. No marketing claims or implementation code were used to infer appearance.

Compared to frozen `FP-DH-01` and `FP-IN-01` from `docs/quality-bar.md`. Non-blind: critic knows identities. Reference images are different scenes and 1200 × 738 / 1195 × 738; candidate was inspected fitted on screen and at its actual export aspect ratio. No random A/B or equal-scene benchmark was conducted, so this is a directional expert assessment rather than controlled perceptual superiority. App UI chrome is not counted against beauty exports. Inspecting thumbnails alone was avoided.

## V02 — Interior composition is the largest immediate gap

`round2-interior.png`: most of the upper half is a pale blank wall and opaque-looking pale window. The oven is clipped at left, the TV is clipped at right, and coffee table/chair fragments are cut by the bottom edge. The dining chairs dominate the foreground but neither the dining group nor seating group forms a complete focal composition. FP-IN-01 frames the furnished seating group, full sofa, two chairs, coffee table, window and decor as a cohesive room. This is a visual framing defect, not a demand to reproduce its exact furniture or palette.

Reproduce: load furnished demo and export the provided default interior camera view. Match the saved `round2-interior.png`.

Priority change: supply a usable interior camera preset framing a complete seating or dining group; keep main furniture inside the image with margin, preserve architectural context, and reduce blank wall area. Save the camera parameters. Retest the preset plus another user camera and export from current edited geometry. Adding more pixels or a different title will not fix the composition.

## V03 — Materials and geometry remain visibly schematic

Dollhouse chairs are slab backs/seats with straight simple legs; cushions/bedding have little soft deformation; plants are stacked smooth green ellipsoids; floor grain is nearly uniform yellow striping. The interior magnifies these features. Fabric, painted wood and upholstery are only weakly differentiated. FP-DH-01 visibly resolves upholstery, thin chair mechanisms, curtains, shelves and varied decorative materials; FP-IN-01 has visible tufting, cloth texture, detailed foliage and a transparent reflective vase.

Priority change: improve a small coherent asset set (sofa, chair, bed, plant, kitchen fixtures) with believable dimensions, soft transitions and fabric/wood/glass roughness. Use material variation at physical scale rather than merely changing base color. A stylized prototype can be attractive, but it has not met the photorealistic reference here.

## V04 — Lighting lacks interior depth

The interior walls/window and light furniture have similar pale values. Furniture contact and room-corner shading are weak, making the space flat. Dollhouse has recognizable directional cast shadows, but they are relatively hard and do not reproduce the reference's soft local grounding. FP-IN-01 shows a coherent bright window-side source with darker material/occlusion regions that articulate the furniture and room.

Priority change: establish a window-side daylight direction, soft but present contact shadows, and balanced fill. Avoid simply increasing exposure or globally darkening every surface. Validate wall/floor junctions, chair legs, table feet and sofa base at 100% output. No requirement for detailed exterior scenery is imposed by this reference.

## Scores against frozen rubric (0–4)

| Criterion | Dollhouse | Interior | Evidence |
|---|---:|---:|---|
| Architectural integrity | 2 | 2 | Apartment divisions/window openings visible; walls remain austere and front seams visible; interior enclosure readable but window treatment is flat |
| Furniture recognition/detail | 2 | 1 | Categories recognizable; simplified slabs/ellipsoid plants dominate at close range |
| Placement/support (visible only) | 3 | 3 | Viewed objects appear grounded; this does not test movement constraints or hidden collisions |
| Materials | 2 | 1 | Pleasant controlled palette, insufficient fabric/wood/glass distinction and fine geometry |
| Light/depth | 2 | 1 | Dollhouse directional shadows present; interior contact/corner depth weak |
| Composition/readability | 3 | 1 | Whole apartment fits comfortably; interior crops major objects and overweights blank wall |
| Interior plausibility | N/A | 2 | Human-scale room view present; highly schematic surfaces prevent convincing realism |
| Export finish | 3 | 2 | Actual clean PNG exports with no editor chrome/selection markers; interior composition remains incomplete |

These are evidence-based ordinal judgments, not measured renderer metrics. The strongest current candidate feature is readable dollhouse organization and a restrained palette. Neither offsets applicable scores below 3. No overall pass, parity or independent win is claimed.

## V05 — Cabinet blocks a doorway; label overlaps sink

`round2-listing.jpg` directly shows the TV/cabinet footprint along the living/hall partition extending across the door gap and door-swing arc. Lead separately confirmed model location x=5.42, z=4.2 and door gap z=3.55..4.5. The visible overlap is sufficient evidence: this is an unusable passage, not a styling preference. Relocate the cabinet and supported TV together to a solid wall section and verify the swing/circulation clearance in both 2D and 3D. Lead proposed z=5.4; that proposal is not yet a verified fix.

The “Ванная” room label sits directly over the sink icon in the bottom-right room. Move room labels into clear floor areas with collision avoidance. The plan otherwise has dark, legible architectural cuts, visible openings and recognizable furniture symbols. It is a cleaner schematic than the initial import screenshot, but does not match FP-2D-01's detailed timber/fabric/rug texture, object shading and fixture detail. Only a single overall horizontal dimension is shown; this is not a Floorplanner comparison failure because the frozen reference has no dimensions, but the export must not be described as comprehensively dimensioned.

Listing scores: architectural integrity 3; furniture recognition/detail 2; placement/circulation 1; materials 2; light/depth 2; composition/readability 2 (bathroom label collision); listing communication 2; export finish 3. The earlier 3D placement score was limited to visible grounded objects; the new top-down evidence finds a mandatory circulation defect in the same scene and prevents placement acceptance.

## Prior issue retest

V01 low-contrast labels: `round2-editor.jpg` shows darker text on light plaques, a visible improvement for room labels. The actual listing rendering also shows readable dark wall cuts and room labels. **Contrast defect corrected for inspected demo export**, but label placement remains faulty at the bathroom sink (V05). The original imported fixture's dimensions have not been independently retested.

## Next evidence required

Improved interior PNG plus camera values; cabinet/TV relocation and collision-free room labels; a second dollhouse/interior viewpoint to expose hidden defects. Repeat independent review before reporting any visual gate passed. Preserve this failed round.

## Artifact fingerprints

SHA-256: dollhouse `B8581027609CC44728D66CB915B7739DC353F6348DF36DE9CB2ED2A4DC4B24B0`; interior `EAF8232010AA36564D65DD7D1D39B15348CD968ECCEBA3509BCD620486AE06F6`; listing SVG `D7E87DE9AE8CA9284B2DF3AACF229988002F99D97EEC6B62935D9DF58E233520`; editor capture `C9336FC489F0BDA344A63EA3FECD7936FD65FC37ED85B38E15A8D2A5E2871003`. These fingerprints freeze assessed outputs even while implementation continues to change.
