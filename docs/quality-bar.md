# Frozen visual acceptance bar

## Active scope amendment — user instruction, 2026-10-16

The user explicitly removed ray tracing and photorealism from the prototype: an ordinary Three.js walkthrough is sufficient; a separate generative-model module will supply photorealism later. This supersedes the original photorealistic interior gate below. It is a scope change requested by the user, not an inferred pass or a retroactive change to failed reviews.

FP-2D-01 remains the concrete comparison for an attractive furnished listing plan. FP-DH-01 remains a reference for architectural integrity, recognizable furnishing, support, framing and readable depth in ordinary CG. The prototype need not match its physically realistic lighting/material fidelity. Interior stills and walkthroughs must faithfully show the current model at usable eye-level viewpoints, with complete geometry, readable surfaces, stable controls, no clipping and playable exports. FP-IN-01 remains a future generative-rendering reference, not a blocking prototype test.

Critics continue inspecting real outputs, returning concrete functional or visual defects and repeating improvements. Any preference comparison must name the applicable criteria and disclose whether it was blind. Do not claim photorealistic parity or an overall win over Floorplanner from these narrower checks. The original reference selection, scores, failures and decision rule below are preserved as historical context; the active completion gate is all nondeferred functionality plus independent acceptance of these revised visual requirements.

## Original baseline (historical)

Status: references inspected and frozen on 2026-10-15; **no RoomPlan comparison has yet occurred**. The critic read SPEC.md before seeing builder reasoning or product output. This document defines a visual test, not a claim that the prototype passes it.

## Exact reference set

All three are the first numbered carousel image in the specified category, selected before opening RoomPlan. The section thumbnail is not the reference. Direct image URLs were obtained from the public gallery links and visually inspected in the browser. Browser screenshots, not downloaded originals, are retained in `artifacts/reference/`; they include browser image-viewer margins. Remote source images are copyright their owners and serve as evaluation references.

| ID | Gallery and category | Exact image | Inspected original dimensions | Frozen screenshot |
|---|---|---|---|---|
| FP-2D-01 | [2D gallery](https://floorplanner.com/2d-floorplan-examples), Full Color, carousel 01 | [full-color-01.8df211e4.png](https://static.floorplanner.com/_next/static/media/full-color-01.8df211e4.png) | 1200 × 738 | `artifacts/reference/floorplanner-full-color-01.jpg` |
| FP-DH-01 | [3D gallery](https://floorplanner.com/3d-floorplan-examples), Dollhouse Views, carousel 01 | [dollhouse-view-01.4e2c4cd9.png](https://static.floorplanner.com/_next/static/media/dollhouse-view-01.4e2c4cd9.png) | 1200 × 738 | `artifacts/reference/floorplanner-dollhouse-01.jpg` |
| FP-IN-01 | [Render gallery](https://floorplanner.com/3d-render-examples), Interiors, carousel 01 | [interior-01.87c540b4.png](https://static.floorplanner.com/_next/static/media/interior-01.87c540b4.png) | 1195 × 738 | `artifacts/reference/floorplanner-interior-01.jpg` |

### Observed features, not marketing claims

FP-2D-01 shows an irregular furnished apartment with heavy dark wall cuts, window breaks, door swing arcs, two bedrooms, bathroom fixtures, kitchen appliances and a dining set. Timber floor grain, rugs, bedding and soft local shadows differentiate objects. The whole plan fits on white with generous margins. This image has no room labels or dimensions; those must not be attributed to this reference. It is visibly softer than a vector plan at the inspected scale.

FP-DH-01 shows a compact studio from above with lowered/cut walls, a bathroom and entrance zone, bed/sofa, TV on a cabinet, workstation, kitchen and storage. Surfaces have differentiated materials; cushions, chair legs, kitchen fixtures, shelves, curtains, accessories and plants have recognizable geometry. Soft darkening where walls meet the floor and furniture touches surfaces makes depth readable. Some rear details are naturally occluded; a test should not demand simultaneous visibility of every object.

FP-IN-01 is an eye-level living-room composition: large bright window on the left, curtains, two upholstered chairs, brown tufted sofa, coffee table with glass vase, framed art, plants and a floor lamp. It shows fabric/wood/leather distinctions, modeled upholstery, contact shadows, plausible daylight and bright-but-readable surfaces. The window is largely white; demanding detailed outdoor scenery would exceed this reference.

## Fair comparison procedure

1. Freeze the candidate project archive, renderer/export settings and revision. Open the actual app and generate exports from its current model. Never substitute an authored illustration or externally retouched image. Keep screenshots and export files separate in the evidence manifest.
2. Compare three matched view classes independently: furnished top-down listing plan, furnished dollhouse, eye-level furnished interior. A top-down schematic cannot stand in for an interior. Missing view/export is a failure for that class, not a low score hidden in an average.
3. Use the same content display area, approximately 1200 × 738, fitting each image proportionally on the same neutral background. No unequal upscaling, sharpening, saturation adjustments or selective cropping. Record native dimensions and any scaling. Also inspect original exports at 100% for clipping/aliasing. Editor UI is excluded from aesthetic scoring but evaluated separately for usability.
4. Match apartment complexity reasonably: populated living area, kitchen, bedroom/sleeping area and bathroom. Do not award the reference points merely for being a different floor layout, having more rooms, a particular palette or owning assets unavailable to the prototype. Do score the visible completeness and fidelity required for a convincing populated apartment.
5. For camera fairness use an unobstructed elevated view for dollhouse, and an interior camera at plausible eye height with comparable field of view. Save camera parameters if exposed. Do not cherry-pick a frame that hides known major defects; include the default view and at least one second viewpoint.
6. Where an independent judge is available, randomize A/B order separately for each class, strip filenames/product branding from displayed panels, retain an answer key and ask for preference plus concrete reasons before revealing labels. The implementer must not serve as the independent judge. A critic who has already inspected these references or knows the UI is **not blind**; an A/B ordering alone does not establish blindness.
7. This set is not an identical-scene benchmark: source geometry, assets, render time, and resolution settings are not supplied by Floorplanner. Conclusions are perceptual reference comparisons with scene/content confounding, not controlled renderer superiority or measured photorealism.

## Observable rubric

Score each applicable row 0–4: 0 missing/broken; 1 major conspicuous defects; 2 usable but clearly below reference; 3 credible parity with only minor differences; 4 a clearly evidenced advantage. Cite image regions and defects with every score; do not derive a score from code existence. `N/A` is allowed only where the view genuinely does not expose that property.

| Criterion | Concrete things to inspect | Applies |
|---|---|---|
| Architectural integrity | Joined walls; believable thickness; usable doors/openings; windows; floor boundaries; no floating or intersecting slabs | All |
| Furniture recognition and detail | Distinct silhouettes and construction; visible furniture/appliance categories; cushions/legs/fixtures rather than generic cuboids | All |
| Placement and support | No visible floor/wall penetration; TV rests on cabinet; floor objects touch floor; furniture permits plausible circulation | All |
| Materials | Appropriate scale/orientation of timber, fabric, tile and glass; controlled repetition; distinct roughness rather than flat uniform colors | All, strongest interior |
| Light and depth | Contact shadows; coherent direction/softness; readable corners; no excessive darkness, floating objects or blown-out furniture | All, strongest 3D |
| Composition and readability | Apartment fits; coherent crop; useful angle; selected objects and geometry remain legible; no UI/selection boxes in beauty export | All |
| Listing communication | Clear room boundaries and furnishing use; uncluttered hierarchy; labels/dimensions, if included, are accurate and nonoverlapping | 2D |
| Interior plausibility | Credible human-scale view, full room enclosure, window/daylight structure, no obvious primitive/camera clipping artefacts | Interior |
| Export finish | Export opens; adequate native resolution; clean outlines; no clipping, missing textures, stale model or changed proportions | All |

### Decision rule

Mandatory functionality is judged separately in acceptance.md. Visual acceptance requires all three classes to have inspectable actual outputs, no critical architecture/support/camera defects, no applicable criterion below 3, and independent documented preference wins with concrete reasons in the compared classes. A tie, internal assertion, a win on only typography, or a non-blind judgment cannot be reported as independently established overall superiority. Report separately: functional status, per-class visual status, blindness limits, and unresolved gaps. Until those conditions are met the product is a partial prototype. Do not cap iterations arbitrarily or relax this frozen bar after seeing output.

Every review must state biggest remaining gap, evidence path, reproduction steps, recommended change, and retest result. Preserve earlier failed rounds.
