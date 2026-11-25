# Rich Mentality — Batch 2 (Shots S21–S40) — Final Technical Report (v2, after the targeted correction pass)

Scope: S21–S40, 53.0 s, 1,272 frames at 24 fps, 1080×1920. Batch 2 was built as a separate production unit. Batch 1 files, the approved storyboard, the character and environment designs, and the GitHub repository were not modified, moved, deleted or uploaded to. The repository clone was used read-only.

All numbers below come from `Batch2_QC_log.txt`, which is produced by `source/final_qc.py` run against the final MP4.

---

## Corrections in this pass (v2)

A targeted pass, not a rebuild. Only S27, S29, S33 and S35 were re-rendered; S38 changed in audio and cue timing only. The v1 deliverables are kept in `previous_versions/v1/` (final MP4, contact sheet, report, SRT, QC log, v1 shot renders, audio, source, and `shots_md5_before.txt`). Nothing was deleted or overwritten outside `delivery/`.

| Shot | Problem | What was done | Inspected |
|---|---|---|---|
| **S27** | Arm went sideways toward the queue and the hand was a fist | New open-hand sprite (`source/hand.py`), skin colour sampled from the approved fist. The sleeve and arm are drawn in screen space with perspective: the arm lengthens and widens as it comes toward the camera, the palm turns up and the hand opens with fingers pointing down. The snack sits on the palm and is drawn with it on every frame. Asha's head, body, clothing, the plate and the camera are unchanged. The tray on the counter was moved left so it does not touch the hand. | Frames 0, 20, 30, 45, 60, 83 plus a full-resolution close-up of the hand at frame 45: open palm, snack on it, sleeve joined at the shoulder, motion from rest to reach is smooth. |
| **S29** | The box carrier faded in over ~8 frames | The fade is gone. He is already standing in the glass doorway at frame 0 (only seen through the door opening, with a slight glass tint), steps out onto the pavement, grows with the perspective, and walks off left holding the box. His step-out starts at 0.06 s, so the opening is not a frozen hold. The two other walkers are unchanged. | 8-frame montage (0, 6, 12, 18, 24, 30, 38, 48): no pop, box held throughout, foot-to-height ratio follows the shot's perspective. Frame-difference scan: only frame 0 is static. |
| **S33, S35** | Asha's small sprite broke the "adult silhouettes only" rule | Her sprite was removed from both shots. All silhouettes, their positions and animation, the stalls, the queues and the camera are unchanged. Nothing was added. The centre stall is still identified by the plate's sage and cream canopy; the plate's red notebook is visible between the queue silhouettes. | First and last frames of each shot, plus a crop of the centre counter. |
| **S38** | 8-word line in 2.45 s (about 3.3 words/s) | Cue 16 now runs **44.62–47.45 s (2.83 s, about 2.8 words/s)**, which is on the storyboard's ~2.75 guide. The cue starts 0.12 s after the shot starts and the end is unchanged. The dialogue is not changed. In `audio.py` the radio crackle is a short 0.14 s burst before the line (was 0.45 s) and the squelch moved from 46.90 s to 47.46 s (after the line, 0.08 s tail). The S38 video, its animation and its duration are unchanged (byte-identical render). | Measured in the final mux: burst at 44.5–44.66 s, nothing audible in 45.5–47.4 s apart from the ambience bed, squelch at 47.46 s. |

**Not fixed, on purpose** (per your list): S27 background softness from the 1.4× zoom, thin neck and shoulder seams, static holds in S25/S26/S36/S38, S30's small Emeka and simplified passengers, the flat leak patch in S36, and the small S37 drip.

**Checks on the final MP4 after the pass (all from `Batch2_QC_log.txt`):**
- H.264 High, 1080×1920, yuv420p, 24 fps, 1,272 frames, 53.000 s; AAC-LC 44.1 kHz mono, 53.000 s. Same as v1.
- All 20 shot renders have their expected frame counts.
- md5 of the 16 unaffected shot renders is identical to v1 (S21–S26, S28, S30–S32, S34, S36–S40). Only S27, S29, S33, S35 differ.
- The repository clone has no changes (`git status` empty). No Batch 1 file was touched. Nothing was uploaded.
- Cuts into and out of the four re-rendered shots show ordinary hard-cut differences (S26→S27 71.5, S27→S28 27.0, S28→S29 46.4, S29→S30 36.6, S32→S33 32.4, S33→S34 45.8, S34→S35 51.0, S35→S36 26.2); no new spikes inside any shot (the only flagged ones are the scripted S36 walk-in and the S24 dissolve).
- SFX onsets in the muxed AAC still match the script within 0–3 ms. Loudness integrated −27.0 LUFS, true peak −2.8 dBFS.

**Audio side effect:** regenerating the audio re-seeds the noise used by later synthetic events, so the ambience texture after S38 differs very slightly from v1. Event times and the structure of the track are unchanged.

---

## 0. Basis of the work (read this first)

- **The latest Batch 1 (v3) final MP4, its source project and its per-shot renders were not available** in anything I could access. What I could access was: the approved character model sheets and expression sheets, the 14 environment plates (A1–D4), the v3 contact sheet, a handful of cropped Batch 1 frames, and the storyboard (V2.1 FINAL).
- Batch 2 was therefore **rebuilt from the approved sheets and plates**, using the same 2.5D sprite-puppet method family as Batch 1. Nothing from a Batch 1 render was edited.
- Hero scale (Emeka 100 %, Sam 95 %, Asha 88 %) was taken from the approved relative heights and checked against the v3 contact sheet. It was **not** checked against the Batch 1 final MP4, because that file was not accessible. Continuity at the Batch 1 → Batch 2 cut is therefore judged from the contact sheet only.
- Three Batch 1 frames were used as plate sources, read-only: the café frame (Asha painted out for S21), the S20 tray frame (clean wall plate and tray art for S21/S22/S25/S27) and the S18 notebook frame (used directly as the page background in S26). The derived plates were written to the workspace `assets/` folder, which is not part of `delivery/`; the scripts in `source/` regenerate them from the Batch 1 frames.

---

## 1. Completed

**Deliverables (in `delivery/`)**

| File | What it is |
|---|---|
| `Batch2_S21-S40_1080x1920_FINAL.mp4` | H.264 High, 1080×1920, 24 fps, yuv420p, AAC-LC 44.1 kHz mono. 1,272 frames, 53.000 s. |
| `Batch2_Final_ContactSheet.jpg` | 40 frames (2 per shot) extracted from the final MP4, in the Batch 1 sheet layout (216 px cells, 4 rows, label strips). |
| `shots/S21…S40_*.mp4` | The 20 individual renders, silent, exact frame counts (60, 48, 72, 72, 60, 84, 84, 48, 72, 60, 48, 48, 84, 60, 72, 48, 48, 72, 72, 60). |
| `Batch2_Narration_Dialogue_Cues.srt` | 18 cues (narration and dialogue), absolute from S21 = 0:00. |
| `audio/Batch2_SFX_Ambience_44k1_mono.wav`, `audio/Batch2_SFX_event_times.json` | The synthetic sound track as a WAV and the list of every SFX event with its time. |
| `Batch2_QC_log.txt` | Raw QC output. |
| `source/` | All scripts that produced the video, for re-rendering. |
| `qc_frames/` | The review montages and close-ups I looked at while working. |

**What is in the picture.** All 20 shots follow the storyboard's shot order, durations, locations and acting names:

- **Café and bus-stop block (S21–S26):** café plate with the burnt then golden tray, bus-stop commuter beat, the flat coin and tape inserts.
- **Plaza block (S27–S28, S33–S35, S39–S40):** C1 and C2 plates with Asha, Sam, queue and stallholder silhouettes.
- **Bus block (S29–S32, S36–S38):** street, bus interior, the manual, bus stop, the leak chain.
- Characters use the approved heads (expression-sheet names), the approved body sprites, and the approved relative heights. No mirrored side views: Emeka's S36 side view is the approved right-facing sprite.
- The leak is one continuous fault: dark patch (S36) → drip under the wheel arch (S37) → mechanic's confirmation (S38, audio cue only). Emeka does not diagnose or repair.
- Screens are flat inset panels (S34). No text or timestamps are drawn into any image; the manual in S31 uses abstract grey bars, not letters.

**Audio, stated exactly.** The track contains synthesised sound effects and a low ambience bed only: steam hiss, sample pick, coin slide / land / bounce, tape press, bus rumble, brake hiss, engine hum, pencil scratch, a faint tone, tag flip, crate taps, panel slide, drips, radio click and crackle. **There is no voice**: no narration, no Sam / Asha / mechanic dialogue, and no synthetic speech. The SRT carries those lines as cues for whoever records or generates the voices.

---

## 2. Tested and verified

Each item was checked against the final MP4 unless stated.

- **Container / codec:** ffprobe reports H.264 High, 1080×1920, yuv420p, 24/1 fps, AAC-LC 44.1 kHz mono; counted frames = 1,272; duration 53.000 s (video and audio).
- **Per-shot frame counts:** all 20 individual renders match their expected counts exactly (log section "per-shot frame counts").
- **Shot boundaries:** 19 hard cuts show large frame differences (7–80), as expected for hard cuts. The two same-plate cuts are lower (S23→S24 5.79, S39→S40 7.37) because the background does not change. The one scripted transition, the S24→S25 dissolve, finishes inside S24's last 6 frames and the cut itself measures 0.13.
- **Pops / duplicates:** a frame-difference scan flags only S36 frames 4–15, which is the scripted ease-out walk-in, and the scripted S24 dissolve. No other spike above 6× the shot's median. Static holds (frames with essentially zero change) exist and are listed per shot; the longest are S26 (39 frames), S25 (35) and S38 (34). They are intended holds, but see §4.
- **Props never vanish or teleport (checked on the final MP4):**
  - S25 coin: colour-centroid tracking shows it reaches its final position (x = 770.5 px) at 0.667 s and then moves at most 0.58 px for the rest of the shot, including through the 6→5 snack dissolve.
  - S26: the coin is visible under the tape in the contact-sheet frame, and the tape's motion stops at frame 50 (diff drops from 0.18 to 0.01).
  - S35: the crate on the counter stays put while the panel comes down behind it.
  - S27: the snack is on the open palm from the first frame and rises from behind the counter edge with the arm; no pop-in.
  - S29: the box carrier is in the doorway from frame 0 and steps out; no fade and no pop.
- **Audio sync:** onsets detected in the muxed AAC match the scripted SFX times to within 0–3 ms for the sharp events (sample pick, coin land, tape press, tag flip, panel landing, both drips, radio click). The S25 coin lands on frame 17 visually and the sound sits at 11.22 s, which is the same instant to within one frame. Audio decodes to 53.011 s (AAC encoder padding); the container reports 53.000 s for both streams.
- **Loudness:** integrated about −27.1 LUFS, true peak −2.8 dBFS (SFX and ambience only).
- **Visual inspection** of rendered frames (montages and full-resolution crops, not only thumbnails): head-to-body connection and neck join (Sam, Asha, Emeka); S27 sleeve joined to the shoulder, open hand and snack connected (full-resolution close-up); S24 satchel commuter and crate overlap (fixed after the first render); S30 passenger sway and Emeka's back view; S31 pencil tip on the end of the line as it grows; thermos in Emeka's left hand in S32/S38 (it is part of the approved front sprite) and capped, no steam, in S31; S36 Emeka in the approved right-facing side view, never mirrored; S37 repeating drip; S39 and S40 expressions; no obvious clipping or floating props at the sizes viewed.
- **Preservation:** the repository clone shows no changes (`git status` empty); no Batch 1 file was written; no file was overwritten (new folders only).

---

## 3. Not fully verified

- **No real-time playback test.** I did not play the video on a phone or any player. All checks were decode-based or frame-based.
- **No independent review.** Everything above is my own check of my own output. No separate reviewer agent or human saw it.
- **Continuity with the Batch 1 final** (S20 → S21 cut, hero scale, palette match) is judged from the v3 contact sheet only, because the Batch 1 MP4 was not accessible (§0).
- **Per-frame visual checks were sampled, not exhaustive.** I viewed the 40 contact-sheet frames, the working montages and close-ups of the trickiest frames, not every one of the 1,272 frames. Anatomy artefacts that appear only on frames I did not view could remain.
- **Audio listening.** I analysed the audio (onset times, loudness) but did not listen to it. Whether the synthetic sounds read as pleasant or believable on a phone speaker is unverified.
- **S38 dialogue pace.** The cue now runs 44.62–47.45 s (about 2.8 wps for 8 words). A real recording has not been made, so whether the delivery feels natural is untested. If the voice still sounds rushed, the fallback is a slightly longer shot (about +0.4 s). That changes the total duration, so I have not done it; it is your call.
- **S27 hand and S29 doorway were judged on stills and frame-difference data**, not in real-time playback.
- **S26 narration** is 9 words in a 3.0 s cue (3.0 wps) and **S21 Sam's line** is 2.9 wps; both are at the fast end.

---

## 4. Remaining imperfections

1. **No voice and no music** (§1). The video is not publishable as a finished piece until narration and dialogue are added.
2. **S33 and S35 (resolved):** silhouettes only, as the storyboard says. The centre counter now has no figure behind it; the stall reads as Asha's through the plate's canopy and notebook. The two silhouettes in front of it are the existing queue.
3. **Judgment call, S27:** the C1 plate is zoomed 1.4× so that hero-scale characters fit the stall. It is slightly soft compared with the other plates. The reach is now toward the camera with an open hand (see the corrections section). The hand is a new sprite built to match the approved skin colour, not cut from the model sheet, because the sheet has only a fist.
4. **S28, S34, S39, S40 stand-in framing:** these use the C1 plate at the same 1.4× zoom, with Sam / Asha at hero scale in front of it. The stall behind them is empty (Asha is not drawn in those shots).
5. **S30:** Emeka at the wheel is small (the cab in D1 is far away) and seen from behind, as specified; the packed aisle is a cluster of flat silhouettes, so it reads as "crowded" more than as individual passengers. No reverse angle, as instructed.
6. **S36:** the leak patch is a flat graphic ellipse on the paving, not a perspective puddle (the storyboard allows this). The patch is visible from frame 0 and spreads about 16 % over the shot.
7. **S37:** the drip is small in the frame; at phone size it reads, but it is not dramatic. The patch under it grows slightly with each landed drop.
8. **Static holds:** S25, S26, S36 and S38 (S25 35 frames, S26 39, S36 17, S38 34) have long runs of identical frames (flat inserts and held poses). This is faithful to "no hand animation / pose only", but S38 in particular has no breathing or blink (Emeka's blink is deliberately off because his blink inpaint looked worse than none).
9. **Fine seams:** a very thin lighter neck line on Sam and a faint shoulder seam on Asha's arm are visible at full resolution. They were not visible at normal viewing size.
10. **Silhouettes overlap** in the S33 and S35 left-hand queue (five figures in single file); it reads as a queue but is dense. The centre stall is partly covered by its own two-person queue.
11. **Placeholder SFX** are synthesised, not recorded, and will sound clearly synthetic next to real recordings.

---

## 5. Next

1. Record or generate narration and dialogue from `Batch2_Narration_Dialogue_Cues.srt` (decide the narrator voice; this is still an open project decision). Settle the S38 line length first.
2. Add captions and any on-screen text in the editor (none are in the images).
3. Replace or mix the synthetic SFX with real recordings if wanted.
4. Play the final on the target phone and review before sign-off; ideally get an independent review of continuity against the actual Batch 1 final, once that file is available.
5. Confirm the S27 1.4× zoom and the S38 cue timing (or choose the +0.4 s extension). Batch 2 is then ready for approval.
6. Only after approval: place the files wherever you want them. I have not touched GitHub.
