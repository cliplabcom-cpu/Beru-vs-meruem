# Rich Mentality — Opening & Ending: Production Report

## 1. Delivered
| File | Content | Duration | Spec |
|---|---|---|---|
| `Rich_Mentality_Opening_FINAL.mp4` | O1–O2 | 8.208 s (197 frames) | 1080×1920, 24 fps, H.264 yuv420p (CRF 14) + AAC 44.1 kHz stereo |
| `Rich_Mentality_Ending_FINAL.mp4` | E1–E5 | 16.500 s (396 frames) | same |
| `Rich_Mentality_Opening_Ending_Production_Report.md` | this report | | |

**Not delivered: `Rich_Mentality_Opening_Voice.wav` and `Rich_Mentality_Ending_Voice.wav`.** No narration exists (see section 2). Opening and ending are separate files. The existing Batch 1/2/3 files and the 63-shot main video were not modified. The GitHub repo was cloned read-only and not changed.

## 2. Narration — NOT completed
- The only voice tool available in this session (CleanAudio Edge TTS) refused the request: *"You've reached your free processing limit. 0 minutes remaining."* No other voice-generation tool exists in this session, and the sandbox has no local TTS engine. I did not fake narration.
- Both videos carry **ambience, SFX and sparse music only**. Narration is **not synchronized, because it does not exist**.
- The picture, on-screen text and SFX are timed to the planned voice windows below, so a voice track can be dropped in:

| Line | Place it at (clip time) | Window it must fit |
|---|---|---|
| "What if, overnight, everyone in the world developed a rich mentality?" | Opening 0.4 s | ends by ≈4.7 s (lamps click off 4.2 s) |
| "Not a fortune. A way of thinking." | Opening 5.4 s | ends by ≈7.6 s (hard cut into S1 at 8.2 s) |
| "Ask someone what they own, and they'll give you a number." | Ending 4.9 s (E3 start + 0.4 s) | ends by ≈8.8 s |
| "Ask what they've built, and you'll hear names." | Ending 9.8 s (E4 start + 0.3 s) | ends by ≈12.8 s (cover closes 12.5–12.95 s) |

Spoken durations are my estimates, not measured. Voice direction: one voice for both clips, calm, warm, mature, slightly curious on the opening question and reflective on the ending; slow the rate about 5–8%. The ending's last 0.5 s is near-silent by design. Beds sit at −45.6 LUFS (opening) and −40.9 LUFS (ending), peak −28 dBFS, so there is headroom for a voice about 15–20 dB above them.

## 3. Phase 1 verification
- **Plates:** A1, A3 and C1 9:16 plates are present in the repo (`03_Most_Important/Environment_References/`) and were used as they are. Glow positions were measured on the actual plates.
- **Asha neutral no-apron design:** the sheet is **not in the repo**. Only the apron-variant sheet, the colour reference and the expression sheet exist. I used the documented fallback: **no Asha hold in E3**. E3 is the closed C1 stall at dusk. No Asha art was altered or reinvented.
- **Notebook, coin and clothing continuity:** the notebook and coin were redrawn as new flat art in the project palette (red #C8493A, gold #D9B25F, cream). No source files for the S62/S63 notebook exist in the repo, so these are matched by eye, not copied.
- **Grade match:** the end of the opening is fitted to the real S1 frame 0 (Batch 1). Background difference is about 5 grey levels. The scale difference is about 2%, because the opening pushes in and S1 starts at 100%. The audio level at the end of the opening is matched to S1's start (−43 → −40 dB mean).
- **S63 → E1:** S63's last frames fade to near-black and E1 is black, so the join is continuous.

## 4. Deviations from the approved storyboard
1. **One street lamp, not four.** Only one lamp is visible in the 9:16 plates, and I did not draw new ones. Its click-off is at 4.2 s with a short flicker.
2. **No Asha in E3** (fallback above). A terracotta-satchel silhouette walks past, as in the optional storyboard beat.
3. **New prop:** a wooden roller shutter drawn over the C1 stall opening, to read as "closed". It is an overlay in the video only, and the plate file is untouched.
4. **E1/E2 split:** E1 is 1.0 s of black with the evening bed fading up. The 0.5 s fade-up is the start of E2 (3.5 s). The total is 16.5 s as planned.
5. **Opening push is about 2%** (storyboard allowed up to 104%), to keep the cut into S1 close.
6. **Silhouettes** (crate carriers, walkers, passer) are flat navy shapes I drew to match the Batch crowd look. They are simpler than the approved crowd art, whose generators are not in the repo.
7. **Music is an original synthesized pad and a few plucks** made for this clip, so there is no third-party licence to log. It is simple, and a licensed track could replace it.
8. **The wood-coin tick** in E5 is re-synthesized, not the exact S2/S25/S56 sample.
9. **The "names" page** uses abstract looped scribbles with dots, so there are no readable letters.
10. **The wordmark** "Rich Mentality" is plain DM Sans Bold, not a final logo. The hook and O2 text are rendered into the video, so they are not editable layers.

## 5. QC performed
Checked with tools: frame counts, resolution, fps and audio format; loudness and peaks; black-frame scan (only intentional black: E1 and the final 0.08 s fade); frame-to-frame jump scan (the only large jumps are the planned cuts, the click-off and fades); contact sheets of both films, reviewed by me frame by frame.

**Not checked:** I cannot listen, so the audio was measured but not heard. I did not play the files on a phone or after YouTube/Instagram re-encoding. I did not review a true side-by-side of the hard cut into S1 beyond the numeric match. Text timing was not tested against real narration.

## 6. Remaining issues / risks
- **Narration** (section 2) is the blocker for a finished video.
- The silhouettes and crate carry are the weakest visual element. They are acceptable but crude next to the approved character art.
- The lit café glass on A1/A3 reads as a flat amber slab. This is a stylised look, and it is the first thing to polish.
- The "names" scribbles are somewhat repetitive.

## 7. Next steps
1. Generate the four narration lines (a paid or unlimited TTS or recorded voice), then mux them over the existing beds at the windows in section 2. Audio-only changes, with no re-render needed.
2. Approve or adjust the deviations (especially no Asha in E3) before the final assembly with the 63-shot film.
