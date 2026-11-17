# Module 03 - V2 Delivery Audit & Final Report

Scope: audit of the corrected environment references. Nothing here is Phase 4 / animation work.

## 1. Delivery audit

The supplied delivery folder contains 14 landscape images, 14 vertical images, four sheets, 14 generator files and reports. The manifest records file sizes and resolutions read back from disk. The report states that a clean copy of the source generator rebuilt all 28 images byte-identically. The v2 images are **procedural re-creations**, not pixel edits of the original PNGs. Original images were left untouched.

## 2. What changed

- C3: Sam's mirrored approved side view was replaced with his approved front view.
- D4: Emeka's mirrored approved side view was corrected to the approved facing.
- D2: hanging grab loops and a large near tree were removed to make the driver cabin clearer.
- D3: camera raised; shelter, stop sign, bus and boarding zone separated.
- Vertical compositions were re-framed per image, not centre-cropped.

## 3. Bus review

- **D1:** seats have gaps and the aisle reads, but seats remain plain boxes and still read somewhat like stacked green blocks. Layout reference, not final look.
- **D2:** driver's seat, wheel, dashboard and road ahead are understandable. Remaining weakness: seat is a grey-slate box and glass is very pale.
- **D3:** shelter, stop sign, bus and boarding zone are distinct. The boarding strip is plain.
- **D4:** character heights remain 100 / 95 / 88. Characters are staged in a staggered single-file line because the aisle is 1.06 m and two characters cannot stand abreast in front view.

Proposal in the report, not applied: keep the aisle and single-file staging; consider a wider ~1.8 m vestibule beside the door for shots with multiple people.

## 4. Character accuracy

The report says the cut-outs were checked against the approved character sheets:
- Asha: short dark curly hair and mustard jacket; faces left in side view.
- Emeka: cap, grey-streaked beard and navy uniform; faces right in side view.
- Sam: spiky hair, charcoal blazer and white sneakers; faces right in side view.
- Heights: Emeka 1.85 m, Sam 1.76 m, Asha 1.63 m (100 / 95 / 88).

A document/image mismatch is flagged: `02_APPROVED_Character_Designs.md` says Emeka's side view faces left, while the approved model-sheet image shows right. The image was followed. The supplied archive contains only front, side and back views; no three-quarter views.

## 5. Vertical 9:16 review

All 14 verticals are 1080×1920 and are re-framed renders, not centre crops. The report says no character or key prop is cut off and the bottom ~20% is kept calm for subtitles/platform UI. Weakness: wide scenes leave small subjects and substantial pavement/floor in A1, A3, C1 and C2; A4, C3 and D3 also have relatively small subjects.

## 6. Cross-location quality review

Palette (cream, sage, terracotta, slate), scale and soft warm light/cool shadows are harmonious across the four locations. Bus interior glass is hazier and its seats/cab are blockier than other locations.

## 7. Approval status

| Environment | Layout status | Remaining issue |
|---|---|---|
| Street A1–A4 | Provisionally approved layout references | Ready for user review |
| Café B1–B3 | Provisionally approved layout references | Ready for user review |
| Market C1–C3 | Provisionally approved layout references | Ready for user review |
| Bus D1–D4 | Usable as layout references, not approved as final look | D1 seat blockiness, D2 washed-out glass, aisle/vestibule decision |

## 8. Explicitly untested

No animation or motion, camera moves, layer separation, cut-out behaviour in motion, phone-hardware pipeline or full character lighting match was tested. **The package is not ready for Phase 4 animation approval.** It is ready for layout/look review only.
