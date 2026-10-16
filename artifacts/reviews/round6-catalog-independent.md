# Independent catalog retest — round 6, F07

Date: 2026-10-16. Reviewer: same independent critic as `catalog-independent.md`, separate from implementation. This is an informed, non-blind retest; neither filenames nor category labels were hidden. No browser was operated and no production code was edited.

## Decision

**F07: PARTIAL, substantially improved.** The office-chair category error and the flat sink/tub geometry reported in the first review are visibly repaired. The revised sofa, armchair, bed and dining-chair pairs now provide clear structural alternatives in both shown views. These are meaningful changes in actual rendered pixels.

The whole F07 scenario is not ready for a pass from these sheets alone: placed-object selection/persistence is not shown, and the actual furnished 2D view still needs to demonstrate recognition of geometries that collapse to slabs/bars from above. The second toilet is a particular remaining recognition problem: its top view is dominated by a rectangular closed lid with weak category cues. Some unchanged pairs remain size/color variants, so the evidence for two distinct design references across *every* category is still uneven.

This does not mean every pair must be a different product style. F07 specifies distinct references, not radically different designs. A clear dimensional/footprint difference is legitimate evidence; it is weaker than a construction difference and should not be described as a richer model library than it is.

## Evidence and comparison conditions

New evidence: `artifacts/reviews/round6-catalog-page-1.png` through `round6-catalog-page-6.png`, 5060 × 3142 each. Files dated 08:50:19–08:50:29 on 2026-10-16, filesystem local time. All six inspected in full-detail lossless crops `round6-catalog-inspect-crop-1.png` through `round6-catalog-inspect-crop-6.png`, using the same x=1735, y=100, width=1600, height=1450 rectangle as the first review. Original files preserved; no rescaling, recoloring or enhancement.

Baseline: `catalog-page-1.png` through `catalog-page-6.png`, previously inspected during this same review session. Pages 4 and 5 were reopened side by side in the inspection sequence for direct comparison of office chairs and sanitary fixtures. Reference reopened: `artifacts/reference/floorplanner-dollhouse-01.jpg`, 1280 × 720 screenshot.

Both rounds visibly use both camera angles, one shared scale per pair, fixed lighting and color enabled. No monochrome evidence was supplied. HEAD at review is `5ac0d789a14e88768be2bb94cc729595f3139c58`; captures are not independently sealed to a clean revision, and these changes may be in the working tree.

## Per-category retest

| Page / category | Actual new observation versus baseline | Catalog visual finding |
|---|---|---|
| 1 — Sofas | Moss is now an L-shaped chaise/sectional; Linen remains a straight three-seat sofa. The footprint change survives top view. | Recognition and pair distinction pass. |
| 1 — Armchairs | Lounge is now an open wooden frame/sling chair; Shell remains a box upholstered armchair. | Recognition and pair distinction pass. |
| 1 — Coffee tables | Unchanged rectangle/square footprint, same legs and accessories. | Recognizable; adequate footprint distinction, modest design diversity. |
| 2 — Beds | Second model now has an open slatted headboard, platform frame, bolsters and different bedding; top pillow/cover layout differs. | Recognition and pair distinction pass. |
| 2 — Storage | Unchanged four-door versus two-door wardrobe; obvious width difference. | 3D category/distinction pass; top view is a slab and needs furnished-plan context. |
| 2 — Dining tables | Unchanged long/compact rectangular variants with place settings. | Recognizable; visible aspect-ratio distinction, same construction. |
| 3 — Dining chairs | Form is now a padded solid-back chair with dark legs; Wish retains the open curved wooden back. | Recognition and pair distinction pass. |
| 3 — Cabinets | Unchanged long console versus compact two-door cabinet. | Good footprint/construction distinction; top identity benefits from context. |
| 3 — Desks | Unchanged compact versus larger four-legged tables with laptops. | Recognizable through laptop cue; footprint/material distinction is modest. |
| 4 — Office chairs | Both now have central pedestals, radial wheeled bases and arms. Task has a solid padded back; Mesh has an actual open grid back and headrest. Top silhouettes/back details differ. | Prior category failure repaired. Recognition and pair distinction pass. |
| 4 — Refrigerators | Unchanged tall/narrow versus shorter/wider construction. | Recognizable in 3D; size-only alternative is visible, but top identity remains weak. |
| 4 — Kitchen modules | Unchanged narrower/wider stove-and-oven units. Both have four identical burners and an oven. | Category recognizable in both views; pair difference mostly width. The two names do not imply a visible functional difference. |
| 5 — Sinks | Flat inset panels replaced by a deep metallic kitchen basin with drainboard and a round white vessel basin on an open wooden stand. | Prior cavity and pair failures repaired. Both views clearly differentiate the references. |
| 5 — Toilets | First has an open oval bowl, seat rim and cistern. Second is a distinct wall-hung-looking body with closed rectangular lid and separate flush plate. | Structural pair difference now clear in 3D. Second top view is weakly recognizable: broad rectangle dominates. “Oval” does not match the dominant visible lid shape. Support itself is outside this catalog-only review. |
| 5 — Bathtubs | Oval freestanding tub and rectangular apron tub now have visible internal bowls, drains and faucets. | Prior cavity and pair failures repaired. Recognition and distinction pass in both views. |
| 6 — Plants | Unchanged taller/narrower versus shorter/broader plant with different leaf forms. | Generic plant recognition and pair distinction adequate; specific Monstera identity remains weak. |
| 6 — TVs | Unchanged same design at two obvious sizes. | 3D recognition passes; pair distinction is size-only; top view is a bar needing context or an appropriate plan representation. |
| 6 — Rugs | Unchanged rectangular bordered rugs at different dimensions/colors. | Recognizable in both views; dimension/color alternatives, limited design diversity. |

## Reference-based furniture assessment

The original Floorplanner dollhouse has a clearly office-specific chair, recessed kitchen basin, storage openings and differentiated furniture silhouettes. Round 6 closes the two largest *category construction* gaps identified against that reference: the office chairs and sanitary cavities. The new models are no longer fairly described as disguised dining chairs or closed slabs in those categories.

For the revised isolated office-chair, sink and bathtub cards, **3/4 for recognition and construction detail** is supportable at this inspection scale. This is a scoped catalog judgment, not a Floorplanner scene parity score. The rest of the library is mixed: sofas/chairs/beds have useful new form differences, while appliances/storage/TVs retain simple construction and top-view ambiguity. Consequently I do not award a universal catalog-level 3 or any win for the required listing/dollhouse/interior classes.

Floorplanner's complete furnished scene and these isolated cards have different context, framing and object pixel size. No blind preference test, matched scene comparison or overall visual victory is established here.

## Biggest remaining gap

For F07, the biggest remaining gap is **proof that every category remains identifiable in the actual 2D placement view, together with complete placement/selection/save-reopen evidence**. Catalog isometric improvements do not prove that result. The highest-priority visible case is the second toilet's rectangular top, followed by refrigerator/wardrobe/TV silhouettes.

For library diversity specifically, the unchanged refrigerator, stove, TV and rug pairs are the weakest remaining alternatives. They are visibly different dimensions, but still essentially the same design. If the intended requirement is two *design* references rather than two dimensioned catalog entries, these need a second construction/silhouette (for example a side-by-side refrigerator, a meaningfully different cooking module, a different TV support, and a round/patterned rug). This interpretation must not silently replace the wording of F07.

## Recommended next check and retest result

1. Place the two toilets, refrigerators, wardrobes and TVs in their normal room context and capture the actual 2D app view at usable apartment scale. Keep ordinary visibility and selection conditions; do not rely on category labels in the review page to establish recognition. Refine the second toilet lid/seat outline if it remains a white rectangle.
2. Exercise all 36 placements, select them, save and reopen in a fresh session, and inspect both views. Record archive and UI evidence. This review did not perform those actions.
3. If design-level pair variety is the intended acceptance interpretation, revise the remaining size-only pairs and repeat the same shared-scale sheets, including monochrome inspection for geometry diversity.

**Retest result:** office-chair recognition, sink/bathtub cavities, and the requested revised seating/bed pair distinctions are repaired in actual pixels. F07 remains PARTIAL pending the above recognition/workflow evidence. First-round files and findings remain preserved.
