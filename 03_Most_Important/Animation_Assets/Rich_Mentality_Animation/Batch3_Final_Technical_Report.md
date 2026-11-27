# Rich Mentality — Batch 3 (S41–S63) Final Technical Report

## 1. What was created
| Deliverable | File (in `Rich_Mentality_Batch3/delivery/`) |
|---|---|
| Final video | `Batch3_S41-S63_1080x1920_FINAL.mp4` — 23 shots, 1,692 frames, 70.5 s, 24 fps, 1080×1920, H.264 + AAC 44.1 kHz |
| Contact sheet (2 frames/shot) | `Batch3_Final_ContactSheet.jpg` |
| Individual shot renders | `Shots/S41_1080x1920.mp4` … `S63_1080x1920.mp4` |
| Narration / dialogue timing | `Batch3_Narration_Dialogue_Cues.srt` (16 cues, text matches storyboard V2.1) |
| Audio (synthesized ambience + SFX only) | `Audio/Batch3_SFX_Ambience_Mix.wav`, `Batch3_Ambience.wav`, `Batch3_SFX.wav` |
| Audio event timing | `Audio/Batch3_Audio_Event_Timing.json` / `.csv` (beds per shot, 40 SFX events, voice cues) |
| Source + assets | `Source/` (scripts, derived assets, 3 reference frames, README with regeneration commands) |
| QC | `Batch3_QC_Log.md`, `QC_Frames/` (full-res frames of S47, S48, S56, S57, S59, S61, S63) |

No existing project file or Batch 1/2 deliverable was modified, and nothing was pushed to GitHub (repo `git status` is clean).

## 2. How it was made
2.5D sprite-puppet compositing in Python (PIL/numpy/OpenCV) with ffmpeg encoding, in the Batch 1–2 style: approved character sheets → headless body + swappable expression heads (expression swaps hidden behind blinks), procedural props (sleeve + fist, capped thermos, cup with steam, bun, coin), flat navy silhouettes for crowds, a side-view walk rig for Sam, and rigged arms cut from Asha's sprite (left arm for the snack offer, right arm with two-bone IK for closing the notebook). Camera continuity with Batch 2 was recovered from its frames (plate transform x'=1.4x−216, y'=1.4y−400.5). Audio is synthesized (filtered noise beds, impacts, cloth/pen/paper noise), no voice or music.

## 3. Decisions and judgment calls
- Batch 1–2 source scripts/sprites were not available → sprites rebuilt from the approved sheets; props redrawn in the S9 style.
- Heights follow the sheets (Emeka 100 %, Sam 95 %, Asha 88 %); Sam's side view is not mirrored; Asha's hands are not enlarged.
- S57/S59/S61 use the unzoomed C1 plate with Sam's feet/heights as specified; S45/S46/S50 use the zoomed plaza framing from Batch 2.
- S52 uses the thermos drawn on Emeka's approved sheet; all stall shots use the procedural thermos.
- S53's bus engine is sound only (the A3 plate has no bus). S43's distant horn follows the storyboard.
- S52, S58, S59 have a 2 % slow push-in (not in the storyboard) because the shots would otherwise be near-frozen holds.
- SRT cue timings are proposals at ≤ 2.73 words/s inside each shot; S63's line starts 0.5 s in, after the ducked "silence beat".

## 4. QC summary (details in `Batch3_QC_Log.md`)
- **Tested by tool:** frame/duration counts (final and per shot), codec/resolution/fps, cut positions, fade to a black last frame, audio peak/RMS, SRT text vs storyboard, repo untouched.
- **Visually inspected at full resolution:** crops of S47, S48, S56, S57, S61, S63.
- **Inspected only via contact-sheet thumbnails/selected frames:** all other shots and the continuity items (thermos, Sam's path, proportions, expressions).
- **Not tested:** audio by ear, playback on a phone/real player, frame-by-frame review of every shot.

## 5. Known imperfections
See the QC log: simplified Sam side-view legs and no phone visible in side view; pale edge artifacts on Asha's rigged arms; blocky silhouettes (S55 queue overlaps); some near-static hold frames from pixel rounding; small S49 layout weakness; possible small mismatches with Batch 1–2 sprites.

## 6. Not done / next
- Listen to the audio and adjust levels (thermos/coin clinks are loud relative to the quiet beds); record the voice from the SRT.
- Review S55's queue spacing, Asha's arm edges, and Sam's side-view legs if you want a polish pass.
- Combine Batches 1–3 only when you approve this batch.
