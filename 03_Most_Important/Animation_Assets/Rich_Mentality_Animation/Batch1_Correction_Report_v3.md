# Rich Mentality — Batch 1 Final Correction Pass (Report v3)
Shots 01–20 · 1080×1920 · 24 fps · 56.5 s · H.264 + AAC

**Deliverable:** `Batch1_S01-S20_1080x1920_FINAL_v3.mp4` (new file; the earlier `…_CORRECTED.mp4` and all v2 frames are untouched).
**Contact sheet:** `Batch1_Final_v3_ContactSheet.jpg` (two frames per shot, made from the final MP4).
**GitHub:** nothing in the repository was modified, uploaded, moved or deleted. Repo files were only read.

## 1. Completed (what changed, per problem)

**P1 – Expressions tied to events** (cross-fades of ~0.14–0.2 s, mostly hidden under a blink; subtle by design)
- Asha (expression timelines as rendered): S07 neutral → curious (0.95 s) → hopeful (1.6 s). S08 hopeful → curious (2.1 s) → hopeful (2.75 s). S09 hopeful → curious (1.75 s). S10 curious → worried (1.1 s) → disappointed (1.95 s). S13 curious → disappointed (1.75 s). S16 worried → curious (1.5 s) → hopeful (2.9 s). S19 exhausted → focused (1.35 s) → exhausted (2.35 s). All use the approved expression-sheet heads; no new faces were drawn.
- S11 Emeka: neutral → friendly at 0.9 s (blink-covered). S12 Sam: neutral → confident at ~1.15 s, glances at the board as it grows, then settles.
- Street characters (new brow / lid / mouth / blink / gaze controls): S01 shop-window customer curious → dismayed on reading the price; writer focused while writing, relieved when walking on; kerb woman tired; shopper tired. S03 teen: tired → envious/sad frown while scrolling. S04 worker worried while pacing → resigned/determined at the nod; nurse focused/tired. S06 man worried/sad when the pocket is empty. S14 man worried at pocket check → hungry/low at the stomach rub; second commuter tired.

**P2 – Asha head/neck.** Root cause: the old rig cut the head sprite at row ~262, which gave a flat chin and a thin neck stub. New rig (`cafe3.py`): round-chin head sprites (cut 270), body cut at 314, separately shaded neck piece behind the body (chin shadow), head pivots at the neck. Heads are now registered to the neutral head, and cross-fades keep the silhouette of the nearer head, so hair no longer doubles. Checked in crops at S07, S09, S10, S13, S16, S19 (including the extreme S19 poses).

**P3 – Emeka entrance.** S08: Emeka walks in from the left edge with a short, readable walk (bob, arm swing), is in position before the food/thermos handoff. S09: body is connected to the arm, thermos stays in the hand until it is set on the counter, then he walks out. No added duration. Thermos set-down is at frame 21 of S09 = 22.83 s; the SFX onset in the audio is at 22.85 s.

**P4 – Background pedestrians.** S01, S04, S14 silhouettes now have their own timing: walk cycles (S01 one strolls right, S04 one walks left), weight shifts, foot shuffles, arm sway, small head turns/nods. Phases differ per person. They remain flat, secondary silhouettes.

**P5 – ~30–32 s.** That window is S12 (29.5–32.5 s). Diagnosis: it is one continuous shot with one Sam and one board whose bars grow; the board used to fade in as a flat ghost rectangle, which can read as a second board / duplicate figure. I could not see the exact frame you saw in your own copy, so this is my reading of the cut, not a confirmed match. Fix: one board rises from the ground with a shadow and stays through the shot, Sam is the only figure, and he looks at the board as it grows. No characters were removed.

**P6 – Final café (S19).** Lighting, palette, composition unchanged. Added: kneading arm/shoulder rhythm, upper-body bob, small head movements, tired expression with heavy blinks, breathing.

## 2. Tested and verified
- ffprobe: 1080×1920, 24 fps, 1356 frames, 56.50 s, H.264 yuv420p + AAC 44.1 kHz.
- Frame-difference scan of the final MP4: largest inside-shot change 2.25 vs median 0.54 → no pops/duplicate/jump frames inside shots. Boundaries S08→S09 (0.7) and S09→S10 (0.2) are continuous.
- S02, S05, S15, S17, S18, S20 are pixel-identical to the previous cut (diff 0.000). Audio track is bit-identical to the previous cut (same MD5).
- Visual frame/crop inspection: head–neck in all café shots; expression transitions (strips); Emeka entrance/exit and handoff; S12 single board; street faces before/after; contact sheet.
- Frame counts per shot match the original timing; shot order and durations unchanged.

## 3. Not fully verified
- Real-time playback on a phone was not tested; checks were on extracted frames and numeric scans.
- Fine lip/eye details were judged at crop size, not on a phone screen; small expression changes may look subtler on a small display.
- The street-character expressions were checked in strips and before/after crops, not frame by frame for every frame.
- No independent reviewer pass (self-review only).

## 4. Remaining imperfections
- Blinks: closed lids show faint darker ovals around the eyes on some expressions (most visible at S19 full close). Brief (3–4 frames), reads as eyelids/eye bags in the 4 a.m. light.
- Expression cross-fades blur the hair interior detail very slightly for ~4 frames.
- Street characters are flat 2.5D puppets: expressions are simple (brows, lids, mouth line/curve); background silhouettes have no facial detail by design.
- Emeka/Sam use sprite swaps with cross-fade, not new drawn expressions; Emeka's S11 walk is a body sway, not a full cycle (he stands in S11).
- S12 diagnosis (P5) is unconfirmed against your original frame.

## 5. Next
If you approve, Batch 1 is closed and Batch 2 can start from this cut. Code for this pass is in the session workspace (`cafe3.py`, `shots3.py`, `busstop3.py`, `street3.py`, `l2.py`); nothing was pushed to GitHub.
