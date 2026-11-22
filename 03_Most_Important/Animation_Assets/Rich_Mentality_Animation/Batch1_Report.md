# Rich Mentality — Animation Batch 1 (S01–S20) — Report

**Delivered:** `Batch1_S01-S20_1080x1920.mp4` (56.5 s, 1356 frames, 24 fps, 1080×1920 H.264 + AAC) and 20 individual silent shot renders `S01_…` to `S20_…`.
**Verified (ffprobe):** every shot has its exact storyboard frame count; total = 56.5 s; vertical 9:16. Contact sheets of every shot were reviewed.
**GitHub:** untouched (read-only clone only).

## Genuine issues affecting the result
1. **No narration/dialogue audio.** The only voice tool available returned a "free processing limit reached" error. The track contains synthesized SFX (coin clinks, set-downs, thermos clink, sack/coin slides, ticks, flat thud on S20) and a quiet room/street bed only. Timed text cues are in `Batch1_Narration_Cues_NOT_VOICED.srt`. Narrator voice is also still an open project decision.
2. **Method is a 2.5D layered puppet, not true 3D.** No 3D engine or Asha/Emeka rig source exists in the repo, so rigs were rebuilt from the approved sheet art (same method family as the accepted prototypes). Asha, Emeka and Sam use the approved expression/model-sheet pixels (identity, colours, proportions preserved; heights Emeka 100 % / Sam 95 %). Motion is therefore economical: breathing, nods/tilts, blink-hidden expression swaps — no walking or full-body acting for the three leads.
3. **Crowd silhouettes are simple procedural flat shapes** (as the storyboard asks for flat silhouettes), but their anatomy is basic. Small actions (S06 pocket turn-out, S14 pocket check / stomach rub, S01 far-side price-card lean) read weakly at phone size.
4. **B2 café plate was reconstructed** from the accepted Asha prototype frame (the prototype's own close framing is not in the repo as a plate); the red notebook, cup, plate and thermos are redrawn props.
5. **Interpretations made where the brief was ambiguous:** S09 — the sleeve sets the thermos down, pauses, then lifts it away with it (so it is absent in S10); S15/S18 icon order is flour, coin, flame (S18's order, also used in S15); S17/S18 — Sam's larger stack comes from the right, Asha's smaller from the left; S01 price card sits on the far-side shop window.
6. In S09 the thermos briefly overlaps Asha's collar area; Emeka's/Sam's S11/S12 poses are static front views (no walking cycle).

## Not tested
Playback on an actual Android device; any edit-app import (the files are plain H.264/AAC).
## Next
Decide narrator voice → record/generate narration over the cues; then review Batch 1 for fixes before Batch 2.
