# Character Reference Correction — Report

Scope: corrected the existing Module 02 references. No redesign, no new characters, no palette, age, role or clothing changes, no animation. Originals of every regenerated file are in `_superseded_v1/`.

## 1. Height rule and measurements

**Rule:** ground (sole bottom) to the highest point of the head silhouette, including hair and **including Emeka's cap**. Props (notebook, thermos, phone) are excluded.
**Master units:** Emeka = 1000, Sam = 950, Asha = 880. Every sheet draws from these; no sheet resizes a character independently.

| Image / method | Emeka | Sam | Asha |
|---|---|---|---|
| Front, side and back figures (transparent render, 2×) | 1000.0 | 950.0 | 880.0 |
| Group Comparison Sheet (guide-free render, pixels) | 1000 = 100.0% | 950 = 95.0% | 880 = 88.0% |
| Silhouette Test, side by side (guide-free render, pixels) | 1000 = 100.0% | 950 = 95.0% | 880 = 88.0% |
| Silhouette Test overlay: tallest outline and Asha's outline | 1000 | not isolated | 880 |

All soles end at 0.0. Measurements of the group and silhouette images were taken on guide-free renders of the same drawing code, because the published PNGs carry guide lines and labels. The published model, colour and expression sheets were not measured as pixels, only visually checked, since they contain guide lines or mixed layouts.

**Honest note on the original problem.** The delivered front views were already at 100 / 95 / 88. What was wrong: side and back views drifted by up to about 0.7%, soles sat about 2 units below the ground line, and the colour and expression sheets scaled each character independently (colour sheet: each figure stretched to a fixed pixel height; Emeka's expression sheet at 1.12× vs 1.0×). The group and silhouette sheets were rebuilt on the shared units and now state the rule. If the perceived height difference looked wrong, the likely causes were Asha's puffy curls and Sam's spikes adding to different amounts of the total, plus the cap, so the rule is stated on every height sheet.

**Cap decision for you:** with the cap excluded (skull only), Emeka 949.6, Sam 903.8, Asha 842.2 units, i.e. 100 / 95.2 / 88.7%. The ratios hold either way (within 0.7%), so I kept the cap included.

## 2. What was corrected

| Item | Correction | Checked |
|---|---|---|
| Asha side hair | New curl field wraps the temple, ear and nape; same curls, colour and cap-of-curls shape as front and back | Viewed on the model sheet and the apron variant |
| Sam side hair | Complete side section: short sideburn, hairline over the ear, coverage to the nape; spike shape, colour and proportions unchanged | Viewed on the model sheet |
| Emeka cap | One shared cap drawing for all views (crown, band, colours); only the visible visor differs (front lip, side peak, back strap). The colour-sheet cap now uses the same drawing | Viewed on model, expression and colour sheets |
| Emeka hair | Grey hair behind the ear in side and back views, matching the grey temples in the front view | Viewed |
| Ears and face | Side-view ear size/position and nose/eye placement aligned with the front views | Viewed (head test strip and model sheets) |
| Props | Asha's red notebook, Emeka's thermos and Sam's phone are in the same hand in all views. Asha and Emeka side views face left, Sam's faces right, so the prop hand is the visible side | Viewed |
| Soles | Moved to exactly ground level | Measured |
| Lighting | Mirrored side views keep the light on the upper left | Viewed |
| Group and silhouette sheets | Same units, same ground line, height rule stated, percentage labels | Measured and viewed |
| Colour sheets | One master scale for all characters | Viewed |
| Expression sheets | One scale for all characters | Viewed |

## 3. Expressions

Expressions and their meanings are unchanged. Face proportions, eye shape and size, nose and face outline come from one shared spec across all expressions, so I made no change there. The only edit is the sheet scale (Emeka's sheet was drawn at 1.12×). I looked at all three expression sheets (Emeka at larger size). I did not run a pixel comparison of the faces.

## 4. Unresolved or not fully checked

- Emeka's side-view grey hair has a fairly straight back edge, and in the back view the grey area reads as a flat-topped block. Acceptable as reference, not polished.
- Asha's side curls are busy, and her notebook is mostly hidden behind her leg in the side view.
- Asha's back-view inner curl ring is a stylised pattern.
- Expression sheets show only front views.
- The silhouette overlay's Sam outline was not separately measured (his height is measured in the side-by-side image).
- Still open from the first pass: production method, setting and skin tones, "everyone" vs adults, head size, designer-added colours (see the guide, section 9).

## 5. Files updated

3 model sheets + Asha apron variant, 3 expression sheets, 3 colour references, Group Comparison Sheet, Group Silhouette Comparison, `source_svg/`, `source_generator/` (now includes `measure.py` and `dims.json`), `Character_Design_Guide.md`.
Unchanged: `External_3D_Generation_Prompts.md` (heights and designs it describes are still correct).
