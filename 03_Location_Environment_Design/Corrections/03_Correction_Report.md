# Module 03 – Environment Visual Correction & Quality Upgrade: Report

## Read this first (honest disclosure)
The repository contains **only flattened PNGs** of the 17 original references – no editable scene, no generator. Real editing of the originals was therefore impossible. The corrected images are **procedural re-creations** built in Python (a small 3D flat-shader, `source_generator/`) whose camera, palette and layout were matched to the originals. They were rendered and visually inspected here; they are **not** pixel edits of the originals. Characters are cut-outs of the approved Project reference views (front/side only), not new art.

## Files inspected
All 17 originals from commit `a9d8e76` (A1–A4, B1–B3, C1–C3, D1–D4, contact sheet, scale chart, vertical crop check), `03_Environment_Design_Guide.md`, `03_Global_Visual_Consistency_Guide.md`, and the approved character references.

## Files corrected (saved in this folder)
- 14 landscape images (1920×1080): `A1_street_main_day1_v2.png`, `A2_street_along_sidewalk_v2.png`, `A3_street_main_year10_v2.png`, `A4_street_character_placement_v2.png`, `B1_cafe_main_corner_v2.png`, `B2_cafe_counter_hero_v2.png`, `B3_cafe_character_placement_v2.png`, `C1_market_stall_main_v2.png`, `C2_market_row_month6_v2.png`, `C3_market_character_placement_v2.png`, `D1_bus_interior_main_v2.png`, `D2_bus_driver_cabin_v2.png`, `D3_bus_stop_exterior_v2.png`, `D4_bus_character_placement_v2.png`
- 14 deliberately re-framed 9:16 versions (1080×1920) in `vertical_9x16/` (`*_9x16.png`)
- `03_Environment_Contact_Sheet_v2.png`, `03_Vertical_9x16_Composition_Sheet_v2.png`, `03_Scale_Reference_Chart_v2.png`, `03_Before_After_Comparison.png`, `03_Environment_Consistency_Notes_v2.md`
- Source: `source_generator/` (`build_all.py` rebuilds everything; `make_sheets.py` builds the sheets).

## Not corrected, and why
- Original `03_Environment_Contact_Sheet.png`, `03_Scale_Reference_Chart.png`, `03_Vertical_9x16_Crop_Check.png`: kept untouched (preserve); v2 versions saved beside them under new names.
- No original file was overwritten or deleted.

## What changed per image (checked on the rendered output)
- **A1** shelter now a small element at the left, separated from shopfronts; clock and tree moved off shop details; lamp no longer clipped; sidewalk/road separated; restrained life (bin, bike, planters).
- **A2** perspective kept; lamp complete; tree no longer hides a storefront; kerb/sidewalk/road clearly separated.
- **A3** same camera as A1; visible but modest 10-year progress (trees, window boxes, planters, cycle lane, sign band, arrivals screen, café set, shutter, warmer sky). Nothing futuristic.
- **A4** Sam, Asha, Emeka at equal depth, no overlap, none covering a prop. **Measured:** pixel heights 364.5 / 337.5 / 383 → Sam 95.2 %, Asha 88.1 % of Emeka ✔.
- **B1** pendants and frames inside the frame; furniture moved away from the edges; counter has usable clear length.
- **B2** counter hero; foreground table/pendant clipping removed (found and fixed on final check); clear space behind counter for Asha.
- **B3** Emeka and Sam moved off the counter line; Asha's face and upper body visible behind the counter; machine and terminal clear.
- **C1/C2** product variety, calmer bunting, depth layers; C2 has several different independent stalls, Asha's recognisable by sage/cream canopy, blade sign, pot plants; bench/planter moved away from stall counters.
- **C3** Emeka and Sam small and at the sides; Asha visible at her stall; no product/counter hidden.
- **D1** (bus pass 2) camera pulled back so seats read as receding rows, not giant blocks; central aisle kept; entrance vestibule with a glass double door on the right (right side has 2 seat rows, left 5); outside trees pushed back and smaller; rails/reflections restrained.
- **D2** recognisable driver's chair, wheel sized (≈0.40 m) and mounted on a raised pod, one dashboard assembly, believable windscreen view.
- **D3** bus fully inside frame, shelter on the left, stop sign between shelter and bus, boarding area in front of the door clear.
- **D4** (bus pass 2) Sam and Emeka in profile facing each other at the front, Asha in the aisle ahead of them; Emeka now stands in the door vestibule so seat backs no longer hide his legs; no bounding-box overlaps visible on inspection; aisle remains visible.

## 9:16 compositions
Re-framed per scene (new camera, narrower lens, vertical lens-shift so subjects sit high, ~22 % calm at the bottom for subtitles). Not centre crops. D3 vertical omits the shelter/sign on purpose (otherwise they cut at the frame edge).

## Remaining weaknesses (be critical)
1. **Bus interiors (D1/D2/D4) are still the weakest, though improved in a second pass.** Seats are still simple boxy blocks (no curved backs/headrests) and the window glass looks milky; the lollipop trees outside are calmer but still stylised.
2. Characters are flat cut-outs, only front/side views; no seated, walking or turned poses.
3. Lighting is hand-tuned shading, not a real render; no true global illumination.
4. Material detail (wood grain etc.) is only suggested by seams and tone.
5. Portrait versions of wide scenes inevitably show large empty floor/pavement areas (the subtitle zone is generous, ~35–40 % in some).
6. Aisle fit: characters ~1.0 m wide in front view vs 1.06 m aisle (see consistency notes).
7. Not verified in motion; "supports simple animation" is judged from layering and negative space only.

## Technical limitations
Python/PIL renderer, sandbox with 8 GB RAM, no network/pip. No access to an image-generation or animation tool here, so nothing was generated by a specialist model.

## Recommendation
Phase 4 (storyboard) can start for **street, café and market** – these are usable as layout/scale/mood references. The **bus module** got a second pass (seats, camera, vestibule) and is now usable for layout; a specialist-tool paint-over is still advisable before hero shots. Per project rules I have **not** started Phase 4 or any animation; waiting for your approval.
