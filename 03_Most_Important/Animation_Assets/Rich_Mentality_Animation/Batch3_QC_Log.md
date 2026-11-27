# Batch 3 (S41–S63) — QC log

Legend: **[T]** tested/measured by a tool on the exported files · **[V]** visually inspected (full-resolution crop or full frame) · **[S]** inspected only through selected/low-res frames · **[N]** not tested · **[K]** known imperfection

## Container / structure
- [T] `Batch3_S41-S63_1080x1920_FINAL.mp4` (ffprobe): H.264, yuv420p, 1080×1920, 24 fps, **1,692 frames (decoded count), 70.500 s**; AAC 44.1 kHz stereo, 70.500 s.
- [T] Per-shot MP4s decoded frame counts: S41 72, S42 48, S43 72, S44 48, S45 48, S46 48, S47 60, S48 72, S49 60, S50 72, S51 72, S52 84, S53 84, S54 72, S55 48, S56 96, S57 48, S58 108, S59 120, S60 60, S61 60, S62 84, S63 156 → sum 1,692, all match the storyboard durations.
- [T] Shot order / cuts: decoded the final MP4 at 108×192 and found a large frame-to-frame change at every expected shot boundary (22 of 23 transitions) — S45→S46 is a same-plate cut (only Sam leaves; diff 5.0, below the detector threshold), confirmed by position of the contact-sheet frames only. The only other large changes are the S62 cover swing and the final fade.
- [T] No dropped/duplicated frames from the pipeline: frame count equals the sum of shot counts and every shot's decoded count equals its requested count.
- [T] Fade to black: mean luminance of the last frame = 0.0; the fade runs over the last 34 frames of S63.
- [T] `git status` in the cloned project repo is clean (0 changes): nothing existing was modified; nothing was pushed.

## Visual checks
- [V] Full-resolution crops (1080×800 region) of S47 f30, S48 f40, S56 f90, S57 f24, S61 f45, S63 f60. Seen: sleeve/fist/thermos reads correctly; thermos lifts away in S48; thermos + coin + notebook on the counter in S56; Sam side-view walk faces right (not mirrored); Sam front view with cyan-screen phone in hand (S61); notebook closing with hand in S63.
- [S] All 23 shots via the contact sheet (2 frames per shot, 270×480 thumbnails) — S59, S63 f110/f155, S49, S50, S51–S55, S58, S60, S62 only at this size.
- [S] Thermos continuity: S47 set down; S48 stationary ~0.8 s then lifted away (code schedule + frames); S52 held by Emeka (the thermos is part of the approved Emeka sprite); S55 absent; S56 returned and stays; S58, S60, S63 beside the notebook (frames). Thermos never steams (only the cup does) — by code, and no steam seen in frames.
- [S] Sam's path: S57 feet (170,1290)→(300,1355) h540→600; S59 (430,1415) h660; S61 (560,1480) h730 on the unzoomed C1 plate. Sam and Asha never share a frame (Sam shots use the raw plate with no Asha; Asha shots have no Sam).
- [S] Proportions: Emeka/Sam/Asha share a common sprite scale (heights 100 / 95 / 88 %) because of the sheet heights; S51/S52 use the same sheet scale for Sam and Emeka. Verified from code and on screen at thumbnail size only.
- [S] Hands: Asha's hands are the approved sprite hands, not enlarged; the extended-arm rig uses the same sprite pieces (not scaled separately).
- [S] Expressions used exist on the sheets: exhausted, hopeful, determined, satisfied, neutral (Asha); envious, reflective, worried, confident (Sam); neutral, proud (Emeka). Swaps happen behind blinks.

## Audio
- [T] Final AAC decoded: no clipping (overall peak 0.88 of full scale); per-shot RMS: S58–S60 ≈ −36 to −38 dBFS (quiet holds), S43–S44 street only, S46 crowd bed.
- [T] Silence beats: S43–S44 contain only the street bed plus one distant bus horn in S43 (storyboard calls for it); S57 footsteps at 0.82 s and 1.69 s then the bed ducks; S60 bed only (−38 dBFS); last second of S62 → start of S63 ducked to ≈ −33 dBFS RMS; final 0.3 s of the file is silent (RMS 0.0015).
- [T] SRT: 16 cues; every line string-matched against the V2.1 storyboard text; fastest cue 2.73 words/s.
- [T] No voice/dialogue/music was generated — the WAVs are synthesized noise/tone SFX and beds only.
- [N] **The audio was never listened to** (no audio playback here) — only measured. Levels/balance are unverified by ear.

## Not tested
- [N] Playback in a real player or on an Android phone; only ffprobe/ffmpeg decode and frame inspection were done.
- [N] Frame-by-frame review of every shot; most of S59 and S63 were checked at thumbnail size or through measurements.

## Known imperfections
- [K] Sam's side-view legs/sneakers are simplified redraws; his phone is not visible in the side view (S45, S57) — it is visible in front view (S61).
- [K] Asha's extended arm (S56, S60) and right arm (S63): pale sliver/edge artifacts near the elbow where the arm was cut from the sprite; her jacket flank looks flat on the arm side.
- [K] Silhouette crowds are blocky; the S55 queue overlaps into one mass; the S52 driver has a simple cap accent.
- [K] Several long holds still have runs of near-identical frames because small breaths round to whole pixels (S41 53, S55 35, S56 35, S61 33, S43 29, S47 28, S62 26, S60 23, S46 22, S48 22, S49 14 near-static frames). S52, S58, S59 got a 2 % slow push-in to avoid a frozen look.
- [K] S49's day grid fills only the top half of the page; the oven margin icon is small.
- [K] Sprites, thermos, sleeve and sneakers were rebuilt from the approved sheets because the Batch 1–2 source scripts/sprites were not available; small mismatches with earlier batches are possible.
- [K] Asha's front-view eyes cannot turn, so "looking" is carried by head tilt/offset.
