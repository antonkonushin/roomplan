# Independent listing review — round 7

Date: 2026-10-16. Reviewer: separate listing critic, fresh task context; implementation was not edited. **Non-blind review**: product names, branding and reference identity were supplied. This is a perceptual comparison of different apartments, not a controlled renderer benchmark.

**F12: PASS for the active revised requirement: an attractive furnished listing export faithful to the edited model.** This does not establish a blind preference win, overall superiority over Floorplanner, photorealistic parity, or acceptance of F13/video. The historical preference-win requirement is not claimed satisfied by this review.

## Evidence and comparison procedure

- Actual downloaded artifact: `artifacts/reviews/round7-final-listing.svg`, 1200 × 1080; independently parsed and regenerated from `round7-final-project.zip`.
- Native raster inspected: `artifacts/reviews/round7-final-listing.png`, 1200 × 1080. No external image dependencies exist in the SVG.
- Frozen Floorplanner output inspected: `artifacts/reference/floorplanner-full-color-01.jpg`, 1280 × 720, including the original retained browser margins. The historical gallery source resolution is different from this captured evidence; it was not substituted.
- Fair fit: both complete evidence images were proportionally fitted onto separate white 1200 × 738 canvases, with no crop, sharpening, saturation adjustment or upscaling. Candidate fit is 820 × 738 (about 0.6833 scale); reference fit is 1200 × 675 (0.9375 scale). Both fitted panels and the full original images were inspected.
- Comparison panels: `round7-critic-fit-round7-final-listing.png` and `round7-critic-fit-floorplanner-full-color-01.png`, in this directory. Candidate aspect ratio includes its title and dimension rail; this is part of its actual export, not removed to improve the comparison.

I read the active scope amendment in `docs/quality-bar.md` and the F12/completion requirements in `docs/acceptance.md`. Ordinary CG and an attractive listing presentation are the current target; photorealism is not required.

## Direct visual findings

The candidate is a credible listing plan, rather than an editor screenshot: coherent warm floor finishes, distinct bedroom and bathroom surfaces, clear dark wall cuts, visible window breaks, rounded upholstery, bed pillows/cover, chairs, stove burners, sink bowls, bathtub and plants. Living, dining, kitchen, sleeping and bathing uses are immediately understandable. Fine shadows separate furniture from the floor. The apartment, entry-door swing, title and dimension rail fit without clipping. No selection boxes or editor controls appear.

All four room labels occupy free floor areas. The kitchen/living label is clear of the armchair and TV cabinet; the bedroom label is below the bed; the hall label is below the bathroom door swing; the bathroom label is beside, rather than on, the sink. The exterior door swing clears the dimension rail. The smaller room-area text is legible at native size, although naturally small in the fitted preview.

Floorplanner retains more varied, less regular material appearance and furniture individuality, particularly the bedding, textured rugs and kitchen surfaces. The candidate has clearer contours and a calmer graphic hierarchy. I would choose the candidate for this particular clean, labeled listing presentation, but that conditional non-blind preference does not imply an overall win. I do not penalize either image for its apartment shape, room count, particular palette or absence of the other's assets. The reference has no room labels; no label capability is attributed to it.

| Applicable criterion | Score | Visible evidence |
|---|---:|---|
| Architectural integrity | 3 | Continuous perimeter/interior wall cuts, window breaks and door gaps; left wall is visibly thicker following the edit. No conspicuous gap or detached wall. |
| Furniture recognition/detail | 3 | Sofa cushions, bed bedding/pillows, chair backs, burner rings and bathroom fixtures are recognizable. Designs remain more regular than the reference. |
| Placement/support as observable in 2D | 3 | TV footprint lies on the cabinet; coffee table remains within the seating zone; circulation and room entry gaps remain readable. Vertical support cannot be proven from top view. |
| Materials | 3 | Board/tile scale, restrained grain, upholstery weave and ceramic shading distinguish surfaces; their regularity is the main remaining visual gap. |
| Light/depth appropriate to listing view | 3 | Soft local furniture shadows and graded upholstery/ceramics establish enough depth without obscuring boundaries. |
| Composition/readability | 3 | Entire furnished apartment fits; small labels remain secondary; title/scale occupy deliberate white margins. |
| Listing communication | 3 | Room use and circulation are clear; all labels and the dimension rail are unobstructed. |
| Export finish | 3 | Self-contained vector artifact, clean native raster, no clipped content or editor decoration, independently verified current model. |

No applicable row is below 3. Interior plausibility is not scored from this top-down image.

## Edited-model fidelity checks

The ZIP contains `project.json` and `README.txt`. SVG regeneration using the current exporter and that exact project is **byte-identical** to the downloaded SVG. SHA-256: `2e8af5e82ddb8a1c0d37986102bfba54faf46e235e42cb1743db60e541903ef4`.

- Coffee table `o3`: ZIP position `[2.9, 0, 4.1]`; SVG group `data-kind="coffeeTable"` has `translate(390.0 600.0)` at 100 px/m with origin `(100,190)`. Its 1.1 × 0.6 m footprint is rendered 110 × 60 px. The visible table has moved right of the rug centre, consistent with the saved edit.
- Wall `w5`: ZIP thickness `0.22`, height `3.1`; SVG left wall path `M100 840.0L100 190` has stroke width `22.00`, while the other 0.16 m wall cuts are 16 px. The wall and its window strip therefore reflect the thickness edit.
- Wall height 3.1 m is **saved but not geometrically observable in this top-down export**. The header's “Высота 2.80 м” matches the separate saved `ceilingHeight: 2.8`; it does not prove that every wall is 2.8 m. Clarifying that caption as ceiling height would remove ambiguity, but this is not evidence of a stale wall.
- The project has **24 objects and the SVG has 24 object groups**. Their kinds, names and x/z transforms all match, including rotation-aware symbol placement checked against the exporter. All are represented in the actual image. Furniture symbols, their internal ornament and materials are procedural representations of the corresponding model object; they are not an independent per-accessory inventory or a claim of exact mesh projection.
- No external raster references or authored replacement apartment image occurs in the SVG. Byte-identical regeneration plus the inspected object mapping supports model-driven output for this frozen project. This review does not independently replay the UI export click or establish behavior for every arbitrary future model.

## Biggest remaining gap and recommended next improvement

**Biggest visual gap: material and furniture individuality.** At native size, the sofa and bed use very regular repeated weave and smooth rectangular padding; timber grain and table ornaments are similarly regular. The Floorplanner reference has more varied textile/wood appearance and less schematic furnishing. This difference is visible but does not prevent an attractive ordinary-CG listing under the revised scope.

Highest-value optional refinement: improve the existing model-driven upholstery and timber symbol detail with restrained seam/fold variation and category-specific surface treatment, maintaining the saved object footprints, rotations and colors. Avoid adding scene-independent furnishing or accessory illustrations. Keep this a rendering refinement, not a requirement to copy the reference's layout or palette. A smaller communication refinement is to label the header explicitly “Высота потолка”.

Reproduction: open the frozen SVG independently; inspect the sofa/bed at native size, then fit it and the frozen reference proportionally into 1200 × 738 white panels; inspect the seating, bedding and floor material differences. To recheck edited-model fidelity, read `project.json` from the frozen ZIP and regenerate its SVG; compare bytes and the coffee-table/w5 values above.

**Retest result:** current round 7 passes F12's revised visual/export requirement on this frozen edited project. No blocking repair is requested for another listing round. Proposed material refinements have not been implemented or retested by this critic. Earlier failed review rounds remain untouched.
