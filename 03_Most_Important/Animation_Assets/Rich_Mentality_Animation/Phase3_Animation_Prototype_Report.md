# Rich Mentality — Phase 3: First Animation Prototype — Evaluation Report

Deliverable: `Asha_Cafe_Prototype_v1_1080x1920.mp4` (7.0 s, 24 fps, 168 frames, 1080×1920, 9:16, H.264, 436 KB).
Nothing was uploaded to, or changed in, GitHub. All work is in a separate folder; original project files are untouched.

## A. Results

**What was created**
- One 7.0 s vertical clip. Asha is behind the counter, looks down (focused), notices the customer (curious, then a hopeful smile), reaches for the cup, lifts it, hands it toward camera with an open smile, retracts her arm and settles back to a hopeful smile.
- A 28-frame contact sheet and the full source scripts (`source/`), so the clip is reproducible.

**Method chosen: hybrid 2.5D** — the unmodified Module 03 café renderer for background and depth masks, plus a layered cut-out puppet of Asha built from her *approved* artwork, composited frame by frame.
- Why not true 3D: no approved 3D model or turnaround of Asha exists, and no 3D tool was available (offline, free plan).
- Why not AI video: it cannot guarantee identical faces, and the approved references must stay authoritative.
- Trade-off: the faces are exactly the approved drawings, but the body can only move as much as the cut-out allows.

**What was actually tested (rendered and inspected)**
- Background stability: all four static regions were pixel-identical across all 168 frames (max change 0). No flicker or morphing.
- Contact sheet (28 frames) and zoomed strips of arm, face and handover frames reviewed by eye.
- Encoding verified with ffprobe: 1080×1920, 24 fps, 168 frames, 7.000 s.

**Not tested:** real-time playback on a phone, any mobile editing pipeline, and any other character.

## B. Quality evaluation

| Area | Rating | Evidence |
|---|---|---|
| Character consistency | Strong | Faces are the approved expression-sheet heads (IoU 0.979 against the body-frame head). Hair, jacket colour and proportions are unchanged. |
| Movement quality | Limited | Head sway, blinks and expression changes read well. The right arm is now compact and foreshortened. It reads as a forward reach, but it is stiff. |
| Facial expressions | Good | Four approved expressions plus a synthetic blink. Swaps are near-instant cuts, because longer crossfades ghosted the eyes. |
| Object interaction | Acceptable | Grip, lift, carry and release read clearly. The cup is a new procedural prop (see C). |
| Environment consistency | Strong | Same camera and furniture as the corrected café. Counter occlusion is correct. |
| Lighting and shadows | Acceptable | Contact shadow under the cup, soft wall shadow behind Asha, steam. Flat shading on the arm and hand next to the head. |
| Camera and composition | Acceptable | Locked camera, centred subject. About 35% empty wall above and about 30% counter front below, which may suit subtitles. |

## C. Problems

1. **Counter height hides her body.** Only head and shoulders are visible. The "prepare" beat cannot be shown properly. The espresso machine is about 2 m away and she cannot reach it without the counter layout changing, which is not allowed.
2. **Left arm hidden for the whole clip** (a simplification).
3. **The customer exists only as point of view.** The cup travels toward the lens. No extra character was allowed.
4. **Arm/hand ghosting.** During the 0.3–0.5 s when the arm passes behind or in front of the counter edge, it turns slightly translucent (visible around 2.5 s and 5.9 s).
5. **No true foreshortening or elbow articulation.** A forward reach is faked with a squashed sleeve and an enlarged hand.
6. **Source art limits.** Resolution is about 1:1 with the source. The neutral no-apron Asha model sheet and the Module 02 source files were not available, so the body was cut from the approved group sheet. A notebook in the hand was removed from the art.
7. **Heads are front-view only.** Asha has no side or three-quarter head, so she cannot turn toward a customer.
8. **Environment source.** The corrected v2 café exists only in the Module 03 delivery folder, not on GitHub main.
9. **Emeka facing discrepancy** from Module 03 remains unresolved. It is unrelated to this clip.
10. **Manual work.** Every arm pose is hand-tuned with waypoints. Cost per additional scene is high.

## D. Production recommendation

**Approved with limitations.**

Evidence: consistency and environment stability are verified, and the clip is clean enough to use. The weak points are acting range and scalability.
- Use this method for close-up, mostly static dialogue or reaction shots in which a character is behind a counter.
- Do not use it for full-body acting, walking or turning, or scenes with several characters.
- For those, either commission a proper 2D rig or 3D model of each character, or restage shots (for example, keep characters seated or standing behind surfaces).

**Next step (needs your approval; Phase 4 not started):** decide whether to accept the limited acting range, or invest in a proper character rig before scaling to Emeka and Sam, who currently have only front, side and back views.
