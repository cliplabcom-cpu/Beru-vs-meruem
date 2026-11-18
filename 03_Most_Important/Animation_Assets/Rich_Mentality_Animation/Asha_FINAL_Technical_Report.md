# Asha café prototype — FINAL fix (v2 → FINAL)

**Deliverable:** `renders/Asha_Cafe_Prototype_FINAL_1080x1920.mp4` — 1080×1920, 24 fps, 168 frames, 7.000 s (verified with ffprobe). v1 and v2 folders are untouched.

## Root cause (found by inspecting v2 frames at full resolution, not by the overlap tests)
1. **P1 detached hand:** the hand piece was never placed on the grip target; the wrist was overwritten as the end of the sleeve, and the hand-to-elbow distance was often shorter than the hand itself, so the forearm collapsed and the hand floated beside it.
2. **P2 counter penetration:** the elbow hung well below the shoulder, below the counter's back edge, and the arm used an inconsistent per-pixel depth ramp, so the forearm looked as if it lay on or through the counter top while the upper arm was hidden.
3. The v2 automated overlap tests passed regardless, because they only measured hand/cup overlap, not whether the hand was connected or the arm was on the right side of the counter.

## What changed (only `armrig.py` and `anim.py`)
- **P1:** the hand centre now sits exactly on the grip target. The wrist is placed behind it along the hand axis, and the sleeve runs shoulder → elbow → wrist, so no gap is possible. The approved cuff and hand art are unchanged. The sleeve is a smooth tube in the approved sleeve and outline colours: slicing and squashing the art tore it and left jagged seams.
- **P2:** one counter rule. Everything below the counter's back-edge line is hidden, unless the hand is held out over the counter top, in which case the cut follows the bottom of the hand. The café layout is unchanged.
- **P3:** the cup now rests for 0.23 s under the hand (2.75 → 2.98 s) before it lifts. The hand stays on the grip point while the cup lifts and travels. At rest, the cup is drawn in front of her arm; the order is blended over 0.3 s as the hand engages.
- Unchanged: Asha's art, expressions, blinking, café, camera, timing and palette.

## Tested
- Hand centre vs. grip point, t = 2.75–5.75 s: **max error 0.0 px**.
- Re-composing 7 sampled frames reproduces the rendered PNGs exactly (max difference 0).
- All 168 frames were rendered. I checked at full resolution, every 4th frame from 1.5 to 6.2 s plus eight retreat frames (6.2–7.0 s), covering approach, contact, grip, lift, carry, handover and retreat.

## Not tested / known small imperfections (accepted)
- I did not review every frame individually. The sampled frames show no detached hand and no arm drawn through the counter.
- The sleeve is flat-shaded, with no fabric seams or folds.
- For ~3 frames around t = 2.3–2.5 s, the arm is slightly semi-transparent while the layer order blends.
- A tiny cuff fragment shows at the counter line for a few frames around t = 6.2 s as the hand retreats.
- The tests were not run in a clean-room rebuild this pass (only the exact re-render check above).

Source: `final/src`, `final/vendor`, `final/assets`, `final/tests`, `README_reproduce.md` (bundled in `Asha_FINAL_source_bundle.zip`). Nothing was uploaded to or changed in GitHub.
