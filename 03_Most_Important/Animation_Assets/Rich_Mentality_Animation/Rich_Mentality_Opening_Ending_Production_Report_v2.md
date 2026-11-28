# Rich Mentality — Opening & Ending: Production Report v2 (revision)

Supersedes the narration, silhouette and caption sections of the v1 report (kept as `Rich_Mentality_Opening_Ending_Production_Report.md`). v1 MP4s, Batch 1–3 and the 63-shot film were not modified.

## 1. Delivered
| File | Content | Spec |
|---|---|---|
| `Rich_Mentality_Opening_FINAL_v2.mp4` | O1–O2, spoken narration + word-synced captions | 1080×1920, 24 fps, 197 frames (8.208 s), H.264 yuv420p CRF 14, AAC 192k 44.1 kHz stereo |
| `Rich_Mentality_Ending_FINAL_v2.mp4` | E1–E5, spoken narration + word-synced captions | same, 410 frames (17.083 s) (v1 was 396; E5 extended 0.58 s so the wordmark can be held) |
| `Rich_Mentality_Opening_Voice.wav` / `Rich_Mentality_Ending_Voice.wav` | narration only, mono 44.1 kHz, on each clip's own timeline | 8.208 s / 17.083 s |

## 2. Narration (actual method)
- CleanAudio TTS was still blocked (free limit), so narration is generated **offline in the workspace**: Kokoro `kokoro-en-v0_19`, voice `am_michael`, speed 0.9, run through the sherpa-onnx v1.13.8 `offline-tts` binary (downloaded from GitHub releases). The same voice and the same processing chain are used on both clips.
- Script is unchanged. Chain: high-pass 75 Hz, +2 dB @180 Hz, −1.5 dB @8 kHz, light compression, one common gain. Voice-only loudness −19.2 / −19.3 LUFS (mono), peaks −2.3 / −2.1 dBFS.
- Timing (clip time): Opening L1 0.30–4.61 s, L2 5.15–7.41 s (before the 8.2 s cut). Ending L1 4.90–7.89 s, L2 9.80–12.26 s (cover closes 12.5–12.95 s). All inside the requested windows; nothing was rushed.
- Limitation: this is **synthetic** speech. It is calm and clear but has no breaths or human micro-variation. A recorded or premium voice could replace the two WAVs without any re-render of picture (timings above are the targets).

## 3. Mix
- Bed = v1 ambience/SFX/original synthesized music (no third-party licence). Opening bed +9 dB, eased back to the v1 level over 7.0→8.2 s so the join into S1 keeps the matched level. Ending bed +8 dB, tail fades moved to the new length (wordmark held, music/ambience fade 16.6–17.0 s).
- Bed is ducked 5 dB while the voice is present (80 ms attack, 350 ms release). Environmental SFX (lamp click, shutter, birds, bus, footsteps, page, pen, cover, coin tick) are kept.
- Measured: voice vs. ducked bed during speech = 26.5 / 24.6 dB (opening L1/L2), 21.0 / 20.1 dB (ending L1/L2). Mix integrated −16.1 LUFS (opening), −16.8 LUFS (ending; stereo-doubled mono voice, so ≈ +3 LU vs the mono figures above). Peaks −2.3 / −2.0 dBFS. 5 ms edge fades, no clipping.

## 4. Silhouettes (replaced)
- Flat stick-like shapes were replaced by outlined, shaded, jointed low-detail 3D-cartoon figures (FK walk cycle with knee flex, 2-bone IK for the crate carry, soft contact shadows, design-guide lighting).
- **Sam (E2 crate carrier):** head and spiky hair silhouette taken from the approved `sam_side.png` (face flattened), dark blazer/trouser body, lean shoulders, 95% of Emeka-scale at his depth.
- **Asha (E3):** the approved cut-out `asha_front.png` (no apron), used unmodified, scaled to the 88% ratio at her depth. Static with a 0.4% breathing scale.
- **Background people (E2 walkers, second carrier, E3 passer):** new original blank-face figures in the same construction (cropped hair, puff, bun, beanie, long hair) with new palettes, so none can be mistaken for Emeka/Asha/Sam.
- Emeka is not in either clip (not needed by the storyboard); no random insertion of the three leads.

## 5. Other visual changes
- Captions appear word by word on the narration, a 0.12 s fade per word, no motion; mobile-safe size/position, top scrim; gold underline draws across "rich mentality"; the opening hook starts with the first word at 0.3 s.
- Opening: dawn environment, café window, cool-to-warm grade, lamp click-off and S1 match kept from v1.
- Ending: Asha now present in E3; passer crosses in front after the line; notebook page uses 8 varied abstract marks (loops, zigzag, dashes, dots, underline) with different bullet types; coin enlarged and readable on the cover; wordmark visible ~2.7 s before the fade.

## 6. QC performed
- ffprobe: both files 1080×1920, 24 fps, 197 / 410 frames, H.264 + AAC stereo 44.1 kHz, video/audio durations equal within 1 ms.
- blackdetect: only intentional black (ending E1 0–1.125 s; last 0.083 s). Opening has none.
- Frame-jump scan: only planned events (fade-ups, E2→E3 cut, E3→E4 cut, cover open/close, final fade).
- Whisper base.en transcription of the audio extracted from each final MP4: opening "What if, overnight, everyone in the world developed a rich mentality? Not a fortune, a way of thinking." Ending "Ask someone what they own and they'll give you a number. Ask what they've built and you'll hear names." Matches the script.
- Contact sheets of both final files reviewed: silhouettes read as characters, Asha hair/jacket/proportions as in the approved cut-out, captions follow the spoken words, wordmark readable, no visible glitches.
- Opening end frame uses the same S1-fitted grade as v1; S63 fades to black into the black E1.

## 7. Not checked / limitations
- **I cannot listen.** Audio was measured and machine-transcribed, not heard. Naturalness, warmth and any slight artefacts need a human listen.
- Caption/word sync uses word times derived from pause detection and letter-weight allocation (approximate, ≈±0.1 s), not forced alignment.
- Neutral `Asha_Model_Sheet.png` is not in the repo; the approved cut-out (neutral expression, no apron) was used as the closest authorised source. Storyboard asks for a "Satisfied" expression, so the expression differs.
- Background people are simpler than the main animation by design but are new designs, not approved crowd art. Sam's face is deliberately blank in these shots.
- Not played on a phone or after YouTube/Instagram re-encoding. Pixel-level comparison of the join into S1 and from S63 was not re-run beyond the v1 fit.
- Bed is quiet (20+ dB under the voice): ambience and music are subtle, as the brief asked; raise bed gain in `build_audio_v2.py` if too faint.

## 8. Next steps
1. Listen to both clips; if the synthetic voice is not good enough, record/replace the two WAVs at the timings above and re-run the mux.
2. Approve silhouette style and Asha expression, then assemble with the 63-shot film.
