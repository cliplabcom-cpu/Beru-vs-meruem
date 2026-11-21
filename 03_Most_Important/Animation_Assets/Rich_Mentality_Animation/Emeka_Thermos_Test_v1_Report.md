# Emeka Thermos Validation Test v1: Technical Report

**Deliverable:** `Emeka_Thermos_Test_v1_1080x1920.mp4`. H.264, 1080×1920, 24 fps, 7.0 s (168 frames), with a quiet synthesized contact sound (AAC).
**Storyboard reference:** Shot 9, "The thermos": Emeka sets the thermos down and withdraws. Test only, no story changes.
**GitHub:** read-only. Nothing was uploaded, modified, moved or deleted.

## What was built
- **Character:** Emeka's approved back view cut from `Emeka_Model_Sheet.png`. The original left arm was removed from the body art. The head, torso, right arm, belt, legs and shoes are the approved art, with no redraw.
- **Left arm rig:**
  - Procedural sleeve tubes (shoulder → elbow → cuff) with the approved navy, outline and light inner stripe.
  - The approved blue cuff and brown mitt hand cut from the sheet, rebuilt without the thermos.
  - The shoulder dome sits behind the torso, as in the sheet.
- **Mechanics:** The arm is a 3D two-bone IK chain (upper arm and forearm 0.245 m each) projected through a pinhole camera matched to the B2 plate. Foreshortening, depth scale and sleeve widths therefore come from the 3D positions, not hand-keyed.
- **Thermos:** a drawn prop in the approved steel and dark-cap colours. It is held behind the hand, in front of the cuff, as in the sheet. It is placed on the counter top in front of the machine and stays put after release.
- **Body:**
  - Legs and feet are static.
  - The upper body pivots at the belt (breathing, slight weight shift, 7° forward lean).
  - A soft floor shadow and a contact shadow under the thermos are added, plus a small settle wobble at contact.
- **Environment:** the B2 plate used unmodified as the background. Camera is locked.

## Timeline
| Time | Action |
|---|---|
| 0.0–0.7 s | Idle, thermos at his side |
| 0.7–2.0 s | Lean and reach, thermos carried up to the counter |
| 2.0–2.45 s | Lower onto counter, contact at 2.45 s |
| 2.45–2.85 s | Hold, thermos settles |
| 2.85–3.25 s | Hand clears sideways and down, thermos released |
| 3.25–4.7 s | Arm returns to rest, lean back |
| 4.7–7.0 s | Idle hold, thermos left standing |

## What was tested (checked on the encoded file)
- **Format:** ffprobe confirms h264, 1080×1920, 24 fps, 168 frames, 7.000 s, yuv420p, with an audio track.
- **Feet:** pixel difference of the shoe region across all 168 frames, max mean diff 0.024 / 255. No sliding or floating.
- **Bone lengths:** upper arm and forearm are constant at 0.245 m in every frame, so no stretching.
- **Thermos contact:** world position is identical from the contact frame to the last frame (0.000 m drift). It sits on the counter-top plane.
- **Pops:** no frame-to-frame discontinuity. The largest per-frame changes occur in the reach and are smooth. The hand speed peak is 0.94 m/s.
- **Visual review:** contact sheet and zoomed frames at idle, reach, contact, release, withdraw and rest.

## Limitations (stated plainly)
1. **Not true 3D.** No 3D engine or 3D Emeka model exists in this environment. This is a layered 2D puppet from the approved art, driven by a 3D arm solver. It follows the same method as the approved Asha prototype. It does not satisfy "no flat cut-outs" in the strict sense. A real 3D model would need a specialist or cloud tool.
2. **Back view only.** The approved sheets give Emeka's front, side and back views. The arm is drawn for a back view, so the face is never shown in this test. Any shot where he turns needs more art.
3. **Raised-arm pose reads slightly like a wave.** The counter top sits at roughly shoulder height for his stylized proportions, so the placing hand ends up beside his shoulder with a bent elbow. It is physically consistent but not elegant. A lower hand (a different counter spot or a rest-pose adjustment) or a cutaway on the sleeve alone would read better. This is the P4 risk from the storyboard.
4. **Hand is a rigid mitt.** There is no open or grip hand art, so release is shown by withdrawing the hand, not by opening it. Fingers are never shown.
5. **Cuff left edge is partly rebuilt.** The original left cuff was hidden by the thermos. I rebuilt its outline from the right cuff and mirrored the shape, so check it in close-ups.
6. **Foreshortening is a 2D approximation** (the cuff is compressed along its axis). Torso yaw is not modelled.
7. **Plate was not modified**, but I removed two annotations baked into the model-sheet sprite (the "100% (Emeka reference)" guide line and the "BACK" label).
8. **Asha was not included.** Her rig source isn't in the repository.
9. **Thermos is a redraw** in the approved colours and proportions, because the sheet's thermos is partly hidden by the hand. The steel cup near the pastry case is untouched. The plate has no separate plate/saucer.
10. **Audio is a synthesized placeholder**, not final sound design.

## Status
| | |
|---|---|
| **Completed** | Emeka thermos test render, format verified, contact sheet, source scripts |
| **Tested** | feet, bone lengths, thermos contact, pops, format, visual frame review |
| **Not tested** | playback on a phone, front/side views, facial acting, any other shot, Asha/Sam in the same frame |

## Recommendation
Review the video. If the pose and style are approved, I'll start Batch 1 of the 63-shot production using this same rig method. I'd prefer to confirm first whether you want to keep this puppet approach or move to a cloud 3D tool, since that affects every later shot.
