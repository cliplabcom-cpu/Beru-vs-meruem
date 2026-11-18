# Rich Mentality — Phase 3.1 Animation Refinement: Technical Report

Output: `Asha_Cafe_Prototype_v2_1080x1920.mp4` (1080×1920, 24 fps, 168 frames, 7.000 s). v1 is preserved unchanged in `v1_reference/`. GitHub was not touched.

## 1. Source inspection (v1)
- The six v1 scripts exist (`head_extract.py, asset_prep.py, plates.py, rig.py, anim.py, render_all.py`) and were byte-identical to what rendered v1. They were not sent earlier because only three files were delivered.
- They were **not self-contained**: hard-coded paths to `Module03_Delivery/.../source_generator`, `_work/chars/asha_front.png`, and `beru-vs-meruem/Asha_Expression_Sheet.png`, plus cwd-relative `scratch/` and `assets/` folders.
- Fix: v2 vendors copies of those three inputs (originals untouched) and uses relative paths (`paths.py`).
- Verified: starting from `src/` + `vendor/` only, a clean-room rebuild produced assets and frames 0/60/80/120/150 pixel-identical to the delivered v2 frames.
- Still missing (cannot be recreated): the Module 02 source SVG/generator and a neutral no-apron Asha model sheet. The body art is cut from the approved group sheet, as in v1.

## 2. What changed
| Area | v1 | v2 |
|---|---|---|
| Occlusion | two fixed masks blended by a depth factor | counter-edge line computed geometrically from each piece's depth (`occlusion.py`); per-pixel depth along the arm |
| Arm | 2 rigid pieces cut through the cuff, disc elbow | upper arm / forearm / elbow cap / cuff+hand rolling at the wrist; elbow rounding; foreshortening; restrained hand scaling; shoulder lift and 1.3° torso lean; hand rises from behind the counter on an arc with overshoot, drops back behind it |
| Cup | v1 prop | same design, drawn 1.25× larger to suit the approved (large, stylised) hands — this is a change to my own prop, not to any approved asset |
| Face | 0.125 s crossfade between heads (ghosted eyes) | swap hidden by a 0.2 s blink: heads swap while the lids are shut; no crossfaded frames; blink lid uses eye boxes measured per approved head and covers the eye outline |
| Left arm | hidden all clip | left hand rests on the counter behind the notebook with a slight settle |
| Structure | scripts depended on absolute paths | self-contained `v2/` with README, tests |

## 3. Fixed
- **P1 translucency**: v1 had 9 frames (60–63, 141–145) with up to 24,273 half-transparent arm pixels. v2: 0 translucent pixels away from the 1–2 px anti-aliased counter-edge line, on all 168 frames (`tests/test_arm_opacity.py`).
- **P4 ghosting**: 0 of 168 frames contain a crossfaded head (`test_contact_stability.py`).
- **P3 contact**: in all 69 carry frames (2.80–5.70 s) the hand overlaps the cup (min 4,385 px) and hand-to-cup slip is ≤3.7 px frame-to-frame.
- **Stability / consistency**: static background regions change by 0 across all frames. In frames without blink, swap or lean, the face region of v2 is pixel-identical to v1 (diff 0 at t = 0.5, 1.0, 1.5 s). All 18 approved-art assets are byte-identical to v1.
- **Format**: 1080×1920, 24 fps, 168 frames, 7.000 s (ffprobe).

## 4. Not fixed / imperfect
- **Arm still stiff**: rigid pieces; no true foreshortening. A foreshortened forearm shows as a thin sleeve wedge for a few frames (~2.7 s and ~5.9 s). Motion is better (arcs, overshoot, shoulder/torso) but not natural.
- **Smooth skinned sleeve tried and rejected**: it tore at the shoulder and elbow. Kept in `v2/review/armrig_strip_lbs_experiment.py` for the record.
- **Grip**: the approved hand is a mitt (no separate fingers). I improved contact and overlap but cannot position individual fingers without redrawing the hand, which I did not do.
- **Eyes**: closed-eye skin patch is slightly darker than the cheek in places; the hair silhouette pops by a few pixels at a swap (hidden by the blink, but real).
- **Three-quarter head: not feasible from the approved references.** Only front expression heads and one profile view exist. The profile has a different hair mass, ear and eye shape. A feature-shift test (5–9 px) was imperceptible, and anything stronger would mean inventing the hairstyle and face shape, so no head turn was forced (`review/threequarter_test.png`).
- **Left arm**: now visible, but it is a static hand on the counter edge, not acting; whether it reads well needs your eye.
- **Counter height** still hides her torso; the "prepare" beat is still not shown; the customer is still point-of-view only.
- v2 has more motion than v1 (mean frame difference 0.34 vs 0.26); the largest single step is 2.2 around 6.2 s, during the cup exit and arm retreat. It is smooth, not a pop.

## 5. What was actually tested vs not
Tested (scripted, all 168 frames): arm opacity, hand/cup contact and slip, background stability, crossfade check, format, clean-room reproducibility, asset identity, face-region identity vs v1.
Reviewed by eye: the 28-frame contact sheet, v1/v2 comparison crops, zoomed arm frames (2.0–6.6 s), and blink/swap frames. I did **not** inspect all 168 frames at full resolution.
Not tested: real-time playback on a phone, any mobile editing pipeline, other characters, viewer opinion of naturalness.

## 6. Honest v1 vs v2
v2 is clearly better on opacity, occlusion, arm size and cup contact, and has no eye ghosting. The arm is better but remains a cut-out limitation. Character acting range (no head turn, finger-less hand, front-only heads) did not change, and I do not think this method can go much further without a proper rig for each character.

## 7. Recommendation
Method status: **approved with limitations, same as v1 but now technically cleaner.** Before scaling to Emeka and Sam I recommend deciding whether to accept close-up counter shots in this style, or to invest in a real rig. Not started: Emeka/Sam animation, full video.
