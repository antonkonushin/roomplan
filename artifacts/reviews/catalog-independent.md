# Independent catalog review — F07

Review date: 2026-10-16. Reviewer: independent fresh-context critic delegated by the lead; not the model implementer. This is **not a blind comparison**: filenames, category names and the Floorplanner reference were visible. No browser was operated and no production file was edited.

## Verdict

**F07: PARTIAL. The visual catalog gate does not pass.** The captures establish a categorized gallery containing 36 rendered entries across 18 categories, and many recognizable objects in isometric and top views. They do not establish two convincingly distinct examples for every category. The office-chair category visibly uses dining-chair construction. Several fixture silhouettes are weak, and numerous pairs differ chiefly in dimensions and color. This is a finding from rendered geometry, not entry counts or names.

Placement, selection and persistence are **NOT TESTED in this review**. Static catalog images cannot establish those F07 requirements. No overall visual win or Floorplanner parity is claimed.

## Evidence and inspection method

- Actual production-model capture evidence supplied by lead: `artifacts/reviews/catalog-page-1.png` through `catalog-page-6.png`, each 5060 × 3142. File timestamps span 08:41:20–08:41:52 on 2026-10-16 (filesystem local time).
- Inspected all six at full pixel detail using lossless crops: `artifacts/reviews/catalog-inspect-crop-1.png` through `catalog-inspect-crop-6.png`. Every crop is the identical rectangle x=1735, y=100, width=1600, height=1450; no scaling, enhancement or content edits. Original captures were preserved.
- Visible settings in each capture: both camera angles; all categories, three per page; scale shared within each pair; color enabled. Both members of a pair have the same view and lighting. This is sufficient to examine dimensional differences without automatically normalizing them away.
- Contract: `docs/acceptance.md`, F07; `docs/quality-bar.md`, furniture recognition and detail criterion.
- Inspected reference: `artifacts/reference/floorplanner-dollhouse-01.jpg` (1280 × 720 screenshot). Used for qualitative furniture-detail context only. Catalog cards are not a matched dollhouse scene and cannot support a controlled superiority score.
- Repository HEAD at review: `5ac0d789a14e88768be2bb94cc729595f3139c58`. The capture revision was not independently sealed to this hash; working-tree changes may exist.

## Per-category rendered findings

“Recognition” concerns category identity in the visible 3D/top views. “Pair distinction” concerns observable shape or construction, not names. A dimension difference can be real and useful, but does not automatically provide two distinct design references.

| Page / category | Recognition in 3D / top view | Pair distinction and finding |
|---|---|---|
| 1 — Sofas | Clear / clear: cushions, arms, feet and throw | Weak: same three-seat construction and same pillow/throw placement; width and color dominate. |
| 1 — Armchairs | Clear / clear | Weak: both are the same box armchair with the same loose cushion; minor proportions and colors. |
| 1 — Coffee tables | Clear / clear with tabletop accessories | Clear enough: rectangular versus square footprint, visible in both views; same leg/construction system. |
| 2 — Beds | Clear / clear: two pillows, mattress and cover | Weak: same bed construction and textile arrangement, mainly width and blanket color. |
| 2 — Storage | Clear wardrobe / top is a plain slab | Meaningful 3D difference: four doors versus two, substantial width change. Top view distinguishes footprints but cannot independently establish wardrobe identity. |
| 2 — Dining tables | Clear / clear through place settings | Moderate: obvious long versus compact rectangle at shared scale; construction and setting repeat. |
| 3 — Dining chairs | Clear / clear | Weak: same curved back, Y-like support, seat and legs; small size/color change. |
| 3 — Cabinets | Clear / top needs contextual interpretation | Strong: long low console with multiple fronts versus compact two-door unit. Different footprint and aspect ratio survive both views. |
| 3 — Desks | Clear through laptop / recognizable through laptop | Moderate: smaller footprint and different surface color, but same four-leg construction and laptop. |
| 4 — Office chairs | **Wrong/ambiguous category in both views:** renders look like the dining chairs on page 3 | **Fails category-specific recognition.** No task-chair base, casters, office back or arms; both repeat dining-chair design. Labels “Task” and “Mesh” add unsupported specificity. |
| 4 — Refrigerators | Clear / weak top recognition | Width differs meaningfully; same door/freezer construction. Top is an uninformative flat rectangle with small front marks. |
| 4 — Kitchen modules | Clear stove/oven / clear burners | Weak-to-moderate: wider versus narrower version of the same stove with oven. Both visibly contain both elements despite the differing labels. |
| 5 — Sinks | Faucet implies sink / faucet and rim imply sink | Weak: same closed block and flat blue-green inset at two sizes. Missing visibly recessed bowl makes fixture construction unconvincing, especially in 3D. |
| 5 — Toilets | Clear / clear | Weak: almost identical oval lid and cistern construction; slight size change is not a convincing second reference. |
| 5 — Bathtubs | Tentative / tentative | **Weak geometry and pair distinction:** two rectangular solids topped with pale flat panels. Neither reads as an open tub; “Oval” has no convincing visible oval basin. |
| 6 — Plants | Clear potted plant / clear foliage | Moderate: tall versus squat plant with different leaf outlines and pot proportions. Specific “Monstera” identification is unsupported by the unsplit leaves, but generic plant category is recognizable. |
| 6 — TVs | Clear / narrow bar is ambiguous alone | Size-only variant is visible at shared scale, with identical stand/construction. Top-down recognition depends on context. |
| 6 — Rugs | Clear / clear | Mainly dimensions and color; identical rectangular border construction. Weak design diversity, though footprints visibly differ. |

## Furniture quality criterion

**Provisional catalog-level score: 2/4 (usable but clearly below reference); office-chair category: 1/4.** These are isolated-object observations, not replacement scores for the required 2D listing, dollhouse and interior exports.

Positive evidence: sofa and bed cushions are modeled rather than represented by one cuboid; chairs have curved back supports and separate legs; tables include recognizable dishes/plants; stove burners and oven door are readable. Thus a blanket claim that all objects are generic boxes would be inaccurate.

The inspected Floorplanner dollhouse shows a clearly office-specific workstation chair, a recessed kitchen sink, differentiated storage with open shelves, and a furnished scene whose object identities remain clear at much smaller individual display sizes. The catalog's task chairs and filled sink/tub surfaces fall short of those construction cues. This observation does not credit Floorplanner merely for having more assets or a different layout.

## Biggest remaining gap and recommended change

The largest F07 gap is **semantic and structural diversity of the two entries per category**. It is most conspicuous in page 4's office chairs and page 5's sinks/bathtubs, where category-specific construction is absent or misleading. After those, repeated sofa/armchair/bed/chair/toilet geometry leaves much of the catalog functioning as a set of size/color presets.

Recommended implementation sequence:

1. Give Task and Mesh distinct, recognizable office-chair construction (e.g. upholstered task back/arms and a mesh-back alternative, appropriate bases), readable in both top and elevated views.
2. Model actual recessed sink and bath bowls; make the oval and straight tubs visibly distinct. Ensure the kitchen and bath sink differ in shape/construction, not just scale.
3. Introduce a visibly different silhouette or construction for weak pairs: e.g. sectional versus straight sofa, open-leg versus box armchair, different headboard/frame bed, solid versus open chair back, wall-hung versus floor toilet. These are examples, not mandated designs.
4. For naturally ambiguous top views such as refrigerator, wardrobe and TV, verify the actual plan representation in a furnished project; add an appropriate plan symbol/detail if the normal top view cannot communicate identity.

## Reproduction and retest

Open `web/catalog-review.html` through the running app's HTTP server. Keep “Оба ракурса”, shared pair scale and the same light/camera. Visit all six pages and inspect the named rows above. Also enable “Без цвета” to test whether shape differences survive removal of palette cues; that monochrome check was **not supplied and not tested here**. Capture the repaired production meshes under the same settings, preserving this failed round.

Then place two entries from every category in the actual editor, inspect both app views, select the placements, save and reopen in a fresh session. Record project/export evidence separately; catalog cards cannot pass this part.

**Retest result: not yet performed.** Current decision remains PARTIAL; the universal “two distinct recognizable references in every category” requirement is not met by this evidence.
