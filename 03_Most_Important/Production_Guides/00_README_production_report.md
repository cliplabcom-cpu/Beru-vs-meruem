# Production report — Scene 01, 30-second pixel-art test

## What was actually created (all files verified on disk)
Root: `/home/claude/beru_vs_meruem/`

| File | What it is |
|------|-----------|
| `output/scene01_30s_test/scene01_pixel_test_1080p.mp4` | 30.0 s, 1080p, 24 fps, H.264 + AAC. Pixel-art animation with PROPOSED dialogue boxes |
| `output/scene01_30s_test/scene01_pixel_test_1080p_NO_TEXT.mp4` | Same animation, no text boxes, no typewriter blips (for your own dialogue/VO) |
| `output/scene01_30s_test/silent_video/*.mp4` | Both versions without audio |
| `output/audio/scene01_mix_with_text_blips.wav`, `scene01_mix_no_blips.wav` | Full mixes (44.1 kHz stereo) |
| `output/audio/scene01_stem_sfx / ambience / music / ui_blips.wav` | Separate stems for your editor |
| `output/sprites/beru_pose_sheet.png`, `meruem_pose_sheet.png` | Labelled pose sheets (22 Beru poses, 18 Meruem poses) |
| `output/sprites/beru/*.png`, `output/sprites/meruem/*.png` | Every pose as a transparent native-resolution PNG (facing right) |
| `output/review/scene01_contact_sheet_from_final_mp4.png` | 16 frames pulled from the final MP4 |
| `docs/01_scene01_storyboard_timing_and_cues.md` | Shot list, timing, sound cues, proposed dialogue |
| `assets/references/` | Your two reference images, copied untouched (originals in uploads were not modified) |
| `src/` | All code (rig, background, FX, choreography, audio, renderer) — rerunnable |

## How it was made
- Both fighters are drawn from a posed skeleton directly at native pixel resolution (no filter, no upscaled
  smooth art). Every frame is a fresh drawing from joint angles, so anatomy cannot drift between frames.
- Shared pixel density, outlines and limited palettes; palettes sampled from your reference images.
- Dithered (ordered) transparency for glows, auras, smoke and afterimages instead of alpha blending.
- Real choreography: keyframed poses, hit-stop, impact (invert/white) frames, screen shake, camera pans,
  2x punch-in zooms, afterimages, speed lines, shockwave rings, sparks, debris, dust, ground cracks,
  a destructible building (intact -> blasted hole + rubble).
- Audio is synthesized from scratch (original, no samples, no imitation of any actor or recording),
  with a different sound per impact type (block, kick-on-guard, knee, back-hand, tail whip, parry, building collapse).

## Tests performed on the exported files
- ffprobe: both MP4s are 1920x1080, 24 fps, 720 video frames, exactly 30.000 s, with an AAC audio track.
- Motion test on the decoded MP4: motion in every second of the clip; no run of more than 3 identical frames.
- Audio: 30.00 s, no NaN, peak 0.89, level peaks line up with the hit events (checked at land, block, kick, knee, blast, wall).
- Visual review of stills from the final MP4 and of both pose sheets.

## Character rules — status
- Beru: exactly TWO arms/hands, TWO wings, TWO antennae, TWO glowing eyes — confirmed on the pose sheet.
  NOTE: your reference image shows a second smaller pair of orange glows under the main eyes. I followed your
  written rule (exactly two eyes) — tell me if you want the reference's four-glow face instead.
- Meruem: ivory/mint body, dark-green core, purple markings, central head crest, thick tail, NO side horns — confirmed.

## Honest limitations
- This is rigged procedural pixel art, not hand-drawn frame-by-frame. Limbs are simpler/stiffer than your
  detailed references (no per-frame hand redraws), faces are small, and some poses (tail sweep, knee) are approximate.
- The 2x punch-in zooms enlarge pixels for a few frames (a deliberate camera effect, but pixel density changes briefly).
- Dust/smoke are dithered discs; a thin orange shockwave ring lingers around ~20 s (hit-stop delays its fade).
- The stand-off (6.5–12.7 s) is intentionally low-motion: breathing, tail sway, camera drift and typing text only.
- NO VOICE ACTING exists. The text-box blips are placeholders. Dialogue is a proposal awaiting your approval.
- Music is a simple synthesized cue (pads + drums + bass), not a finished score.
- Only this 30 s scene exists. The 3–4 minute battle is not made yet.
