# Module 03 - V2 Delivery Audit & Final Report

Scope: audit of the corrected environment references. Nothing here is Phase 4 / animation work.
All work was done in a delivery folder outside the repository. Nothing in this folder has been uploaded, committed or modified on GitHub by this audit.

## 1. Delivery audit (Part 1)

**Why the files were not visible on GitHub `main`:** they were never on `main`. They existed only in the sandbox working copy. Earlier in the session an automated stop-hook asked for a commit and push, and I pushed two commits to a separate branch, `module-03-environment-corrections`. That push happened before your instruction not to touch GitHub, and I should have asked first. `main` was not changed, and I have not deleted, rewritten or pushed anything since. That branch holds *older* versions of the files; the folder you are receiving is newer and supersedes it. I will delete the branch only if you ask.

| Question | Finding |
|---|---|
| Exists locally? | Yes: 14 landscape, 14 vertical, 4 sheets, 14 generator files, reports. See `03_Deliverables_Manifest.md` (sizes and resolutions read back from disk). |
| Rendered and inspected? | Yes. All 28 images were rendered and each was viewed in this audit (landscape in 2x2 sheets at 956 px wide, verticals as strips at 432 px wide, plus full-size views of D2, D3 and the changed images). Small details at that size were not pixel-peeped. |
| Missing? | Nothing from the requested list. |
| Does the generator rebuild the outputs? | **Verified.** A clean copy of `source_generator/` rebuilt all 28 images; every one is byte-identical (SHA-256) to the delivered file. |
| Originals | Untouched. The v2 images are **procedural re-creations**, not pixel edits of your original PNGs. |

## 2. What changed in this audit

Only genuine defects were changed. A1-A4, B1-B3, C1-C3 keep the same cameras, palette, character scale and story props. The red-notebook continuity and the Day 1 / Year 10 relationship (A1 vs A3) were not touched.

| Item | Defect found | Fix |
|---|---|---|
| C3 | Sam's approved side view was **mirrored** (flip), which changes his asymmetric details | Replaced with Sam's approved **front** view. Same position. Layout otherwise unchanged. |
| D4 | Emeka's approved side view was **mirrored** | Mirror removed; approved facing used. |
| D2 | Hanging grab loops and a huge near tree competed with the cab | Loops removed and the near tree pushed back, for D2 only. The driver's seat, wheel, dash and windscreen relationship is now the dominant read. |
| D3 | Shelter, door and boarding area were hard to separate; no clear boarding point | Camera raised; shelter on the left, stop sign centre, bus right; a painted yellow boarding zone in front of the door. |
| Verticals | Too much empty pavement / small subjects in some | Re-framed per image (crop and camera), including D3 (stop sign now present, as in the landscape). Details in section 5. |

## 3. Bus pass (Part 3)

- **D1:** seats are separated with gaps; trees thinned; central aisle, sage and cream palette kept. *Remaining weakness:* the seats are still plain boxes and the staggered row in perspective still reads somewhat as a stack of green blocks on the left. Acceptable as a layout reference, not as a final look.
- **D2:** driver's position is understandable at a glance (seat, wheel, dash, road ahead). *Remaining weakness:* the driver's seat is a grey-slate box set; the window glass is a very pale haze, so the cab looks washed out next to the other locations.
- **D3:** shelter, stop sign, bus and boarding zone are separate with no overlaps. The boarding strip is a flat painted rectangle at the bottom right: it works but is plain.
- **D4:** characters keep 100 / 95 / 88; none is shrunk or distorted. See the aisle finding below.

**Aisle finding.** The aisle is 1.06 m wide. Approved front-view widths are roughly Emeka 1.0 m, Sam 0.7 m, Asha 0.8 m, so no two can stand abreast in front view. D4 therefore stages them in a staggered single-file line (Asha front, Sam and Emeka behind), with side views for Sam and Emeka.
**Proposal (not applied, needs your decision):** keep the 1.06 m aisle and stage in single file, and add a wider vestibule area of about 1.8 m next to the door for any shot with two or three people side by side. Widening the whole aisle would change the D1 look you have provisionally approved.

## 4. Character accuracy (Part 4)

Checked against the actual approved sheets (`Emeka_Model_Sheet.png`, `Sam_Model_Sheet (1).png`, `Asha_Model_Sheet_Stall_Apron.png`), not the text.

- Asha: short dark curly hair, mustard jacket - matches. Faces left in side view.
- Emeka: cap, grey-streaked beard, navy uniform, broad shoulders - matches. Faces right in side view.
- Sam: spiky hair, charcoal blazer, lean; hairline over the ear - matches. Faces right in side view.
- Heights are set to Emeka 1.85 m, Sam 1.76 m, Asha 1.63 m (100 / 95 / 88%).
- **Mismatch found, not silently changed:** `02_APPROVED_Character_Designs.md` says Emeka's side view faces left. The approved model sheet image shows him facing **right**. I followed the image. Please decide whether the doc or the image is the intended truth.
- Limits: only front, side and back views exist. The figures are flat cut-outs from the sheets, placement references only, not animation-ready. No three-quarter views exist.

## 5. Vertical 9:16 check (Part 5)

All 14 are 1080x1920 (read back from disk). Each is a re-framed render, not a centre crop of the landscape.
- Headroom/footroom and cut-off props: no character or key prop is cut off. C3's Emeka was clipped at the left in one trial framing; that framing was discarded.
- Subtitle space: roughly the bottom 20% is calm in every frame.
- Same story as landscape: yes, including D3's stop sign.
- **Weakness:** wide scenes in 9:16 make subjects small (A4, C3, D3) and leave a lot of floor/pavement (A1, A3, C1, C2 still carry about 35-40% pavement). I reduced it where I could without cropping characters; further reduction would need a different (closer) camera, which would break the story match with the landscape. Left as is.

## 6. Cross-location QC (Part 7)

Visually checked, not measured: palette (cream, sage, terracotta, slate) is harmonious across street, café, market and bus; scale is consistent through the scale chart; soft warm light with cool shadows is similar in all four. The bus interior glass is hazier and lighter than the other locations, and its seats and cab are blockier. Perspective is consistent. No street, café or market image was regenerated for cosmetic reasons.

## 7. Approval table

| Environment | Layout approval | Remaining corrections | Status |
|---|---|---|---|
| Street (A1-A4) | Provisionally approved layout references | None required | Ready for your review |
| Café (B1-B3) | Provisionally approved layout references | None required | Ready for your review |
| Market (C1-C3) | Provisionally approved layout references | C3 Sam mirror fixed (declared above) | Ready for your review |
| Bus (D1-D4) | Not yet approvable as final look; usable as layout references | D1 seat blockiness, D2 washed-out glass, aisle decision | Needs your decision |

## 8. The seven questions

1. **All 28 corrected images available?** Yes: 14 landscape (1920x1080) and 14 vertical (1080x1920), listed in the manifest.
2. **Source generator available?** Yes, 14 files, rebuild verified byte-identical for all 28.
3. **Four environments consistent?** Street, café and market: yes. The bus is consistent in palette and scale but looks blockier and hazier.
4. **Approved characters accurate?** Yes against the model sheet images. One doc/image discrepancy (Emeka's facing) is flagged for your decision.
5. **Vertical compositions ready?** Ready as layout references; the wide scenes leave small subjects and empty floor.
6. **Untested:** any animation or motion; camera moves; layer separation; behaviour of the cut-outs in motion; anything on a phone-hardware pipeline; the characters' lighting match is only eyeballed.
7. **Ready for Phase 4?** **No, not yet.** The layouts are reviewable, but the bus needs your decision and nothing has been tested for animation. I have not started Phase 4 and will not without your explicit approval.
