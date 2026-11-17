# Module 03 - Layout readiness vs animation readiness

**No motion test was made and none of this was animation-tested.** This is an assessment of the stills only.

| Area | Layout readiness | Animation readiness |
|---|---|---|
| Movement space | Street, market: open floor. Café: space between door, tables and counter. Bus: only the aisle (1.06 m) and a vestibule near the door | Bus needs a decision on width for any two-abreast action |
| Foreground / background separation | Visible in the stills | **Not separated.** Each image is one flat layer; characters are composited in. Parallax or character movement would need layered renders; the generator could produce them, but this has not been done |
| Obstruction | Counters, seats and poles overlap characters in places (Asha behind the stall, D4 seats) | Overlaps are baked into the image, so a character cannot walk behind or in front of them without re-rendering |
| Contact shadows | Soft blurred shadows under characters and props | Baked into the image; shadows will not follow a moving character |
| Interaction areas | Stall counter (Asha), café door and counter, bus door and boarding zone, driver's seat | Positions are clear. Props in the hands (red notebook, cup) are fixed in the cut-outs |
| Characters | Correct placement references | Flat cut-outs from front/side/back views: no limbs, no turns, no expressions beyond the sheet. Not usable for animation as they are |

**Recommendation:** treat these as layout and look references. A real animation pipeline needs separated layers, rigged characters or fresh character renders from a specialist tool, and a short motion test before any Phase 4 decision. None of that is done.
