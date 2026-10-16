# Independent visual review — round 3, 2026-10-15

**Verdict: visual gate FAIL, with substantial improvement over round 2. No Floorplanner win established.** Interior composition is now coherent. The largest remaining gap is lighting/material realism, including conspicuous contour halos and stretched material patterns. This is a new review of actual generated pixels, not a score inferred from the list of implementation changes.

## Evidence and review conditions

Directly inspected lead-operated UI exports `round3-dollhouse.png` and `round3-interior.png`, each 2036 × 1364. Compared with fixed `FP-DH-01` and `FP-IN-01` screenshots and the observed reference features in docs/quality-bar.md. These remain different scenes/aspect ratios; no claim of identical-scene renderer benchmarking. Product IDs are known, so this is non-blind independent image critique, not anonymous A/B. Critic did not operate these exports because its browser surfaces were unavailable. Backend/UI interactions are tested separately by lead/functional critic.

Fingerprints: dollhouse SHA-256 `DC6CF45EBC1C93B14820563E29A07683A5B6DF3A757C14194E882474210DEDE3`; interior SHA-256 `1551B2E8D1ECA1DB4CD4A6B4173974DCE51D3470C022F7CA453759C7FFE55771`. Captures saved approximately 23:53 MSK.

## What demonstrably improved

- Interior now centers a complete sofa, armchair and coffee table beneath a window, with framed art and a lamp. The blank-wall-dominated round-2 composition is fixed for this preset; modest cropping of right-hand dining furniture is acceptable secondary context.
- Sofa/chair shapes are visibly rounded; dining-chair backs have curved structure; leaf geometry replaces ellipsoid plants. Furniture remains clearly recognizable in dollhouse.
- Contact darkening, curtains, skirting and decor make room enclosure/depth clearer. Wood variation is now visible rather than a uniform yellow field.

## V06 — Excessive contour halos and muddy interior illumination (largest remaining gap)

In `round3-interior.png`, the lamp shade/stem has a broad gray ghost-like halo on the wall; framed art, curtain/window outlines and the armchair silhouette show diffuse dark contour bands. These screen-adjacent bands resemble a screen-space shading artefact rather than clean material boundaries with plausible contact shadows. The ceiling is a broad brown-gray plane, walls/furniture have a dull gray cast, while the window is nearly featureless pale blue-white. FP-IN-01 has a bright daylight atmosphere with differentiated furniture values and softer, more localized grounding, without such conspicuous contour haze.

In `round3-dollhouse.png`, a large hard-edged cast shadow extends far to the right of the apartment. It distracts from the model and is visually heavier than the reference's soft grounding. This is not a defect merely because the light direction differs; the concern is dominance and edge hardness.

Reproduce: load the furnished demo and export current default interior and dollhouse. Inspect lamp on left rear wall, art frame edges, window/curtain contours, armchair perimeter, and right-hand exterior ground shadow. These are visible in the frozen round-3 PNGs.

Next change: tune contact-occlusion radius/intensity and depth behavior so contact darkening stays near actual joints instead of broad silhouettes; balance window-side daylight and ambient fill/ceiling response; soften exterior shadow. Do not remove all shadows or fix this by uniformly raising exposure. Retest these exact regions at 100% output plus another viewpoint, because screen-space artefacts can depend on camera angle.

## V07 — Material scale and fidelity remain below reference

Wardrobe side/top in dollhouse has conspicuous stretched parallel stripes; similar streaks run continuously along dining-chair members and tabletop/wood edges. The floor is finely striped with little readable plank/joint structure. These patterns indicate wood but are not convincing at object scale. Sofa/armchair upholstery remains smooth and low-detail; bedding remains a near-flat segmented sheet. Reference upholstery, rugs, foliage and wood have richer construction and material variation. Current style is a stronger architectural illustration, still visibly synthetic.

Next change: calibrate wood texture orientation and repetition by physical size and mesh surface; add restrained roughness/fabric variation instead of increasing stripe contrast. Prioritize visible sofa/chair/coffee table surfaces and wardrobe, rather than more decorative object counts. Verify texture boundaries and avoid repeating identical grain across all sides.

## Rubric update (0–4)

| Criterion | Dollhouse | Interior | Rationale |
|---|---:|---:|---|
| Architectural integrity | 3 | 3 | Openings, enclosure, skirting and window context now credible in inspected views |
| Furniture recognition/detail | 2 | 2 | Rounded shapes and leaves improved, still visibly simplified upholstery/bedding/fixtures |
| Placement/support | 3 (visible) | 3 (visible) | Top-down retest confirms clear doorway; screenshots do not test support editing or all clearance dimensions |
| Materials | 2 | 2 | More variation, but stretched wood and smooth upholstery remain conspicuous |
| Light/depth | 2 | 2 | Better grounding, offset by broad contour haze and dull illumination |
| Composition/readability | 3 | 3 | Whole apartment fits; seating group now forms clear interior focal point |
| Interior plausibility | N/A | 2 | Credible room layout, material/light cues still below the photorealistic reference |
| Export finish | 3 | 3 | Actual PNGs with clean export framing and no editor decoration |

No applicable score of 4 is justified by this comparison. The below-3 material/light/detail rows keep the gate failed even though composition passes. No aggregate score is used to hide deficits.

## Listing retest — prior blockers fixed in inspected demo

Directly inspected `round3-listing.jpg`, the lead's actual browser rendering of the downloaded `round3-listing.svg`. The capture contains a large unused white viewport; that margin is not part of the SVG and is excluded from evaluation. The TV/cabinet is now below the living/hall door gap and the swing region is visually clear. The bathroom label is on clear floor to the right of the sink; other room labels do not overlap furniture in this export. **V05 corrected for the inspected demo.** This does not imply a general collision-avoidance system has passed.

Listing rubric: architecture 3; furniture detail 2; visible placement 3; materials 2; depth 2; composition/readability 3; listing communication 3; export finish 3. Clear architectural cuts, hierarchy and labels make this a usable listing schematic. It remains below FP-2D-01's textured furnishing/material detail and has not won the full-color aesthetic comparison. No penalty is applied for having labels absent in the reference. No claim of comprehensive dimensioning: only overall horizontal width is shown.

## Pending retests

Original imported-plan dimension fixture remains unverified after the contrast changes. A second interior and dollhouse viewpoint is still required. Successful wall edits, camera route validation and support constraints must be evidenced through interaction/geometry tests, not inferred from these beauty images.
