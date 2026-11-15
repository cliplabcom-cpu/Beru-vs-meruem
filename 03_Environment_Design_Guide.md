# Rich Mentality — Module 03: Environment Design Guide

Status: **reference-grade environment kit, pending your review.** Not final production art.

## 0. Read this first (honest scope)

- **What the images are.** Flat-shaded 2.5D renders made by a small Python → SVG → PNG renderer I wrote for this module (source in `source_generator/`). They show layout, scale, palette, light, camera and prop placement. They are **not** final 3D-cartoon art and have no textures or soft global lighting.
- **Phase 2 character art was not available to me.** No Phase 2 image files exist in this workspace or the project (only the written correction report). The figures in the `*_scale_placement_test.png` images and the scale chart are **placeholder mannequins** built from documented heights, palettes and silhouette words. They have no faces. They are **not** the approved characters and must not be used as character references.
- **Characters were not redesigned.** Scale is 100 / 95 / 88 %.
- **No readable text is baked into any image.** Signs, boards, menus and screens are blank bands or abstract bars. Text is added in editing.
- **Premise.** Every environment is built for *everyone*, children and teens included. Nothing implies mindset alone produces money, schooling or opportunity. The visible mechanisms are work (the stall, the café), payment, transport and time.

### Scale used everywhere (metres)

| Character | Scale | Height | Note |
|---|---|---|---|
| Emeka | 100 % | 1.85 m (incl. cap) | ≈0.94 m arm-to-arm in the chunky build |
| Sam | 95 % | 1.76 m | |
| Asha | 88 % | 1.63 m | |

Chart: `03_Scale_Reference_Chart.png`.

### Shared tech facts (all four environments)

- Same renderer, camera model, key light and shadow rule (see `03_Global_Visual_Consistency_Guide.md`).
- 1920×1080 source renders. **Vertical 9:16 is a re-frame, not a crop.** `03_Vertical_9x16_Crop_Check.png` is only a centre-crop sanity check.
- Hero props are capped at 8 per location, with 3 depth layers: foreground, mid, background.

---

## A. City Street (main exterior)

**Folder:** `City_Street/`

| Image | File | Purpose |
|---|---|---|
| Main wide | `A1_street_main_day1.png` | Establishing frame, Day 1 state |
| Extra angle | `A2_street_along_sidewalk.png` | Walking-POV along the sidewalk |
| Same camera, later | `A3_street_main_year10_same_camera.png` | Same camera as A1, "Year 10" state, for the time-passing match cut |
| Scale test | `A4_street_scale_placement_test.png` | Placeholder figures, scale and placement |

### Identity guide

- **Name:** "Clock Street" (working name).
- **Mood:** calm, ordinary, warm morning. Not a showpiece; it should feel like somewhere people actually live and work.
- **Palette** (muted warm family): plaster `#E3D0AE`, sand `#D8C29C`, cream `#EEE2CA`, clay `#CB9873`, sage `#A3B99D`, deep sage `#728F7B`, slate `#7B8892`, pavement `#D2C9BA`, road `#908B85`, glass `#CADBD4`. Accent gold `#D9B25F` is used only in Year 10 (shop sign).
- **Light:** key from upper-left-front, camera-relative; sky `#BDD8E2` to `#F3E8CE`. Year 10 shifts the sky slightly warmer.
- **Camera:** A1 at (−2.4, 2.3, −15.0), yaw 0, pitch 0, fov 66, eye-level-plus (2.3 m), slightly looking across the road at the shopfronts. A2 at (−15.6, 1.75, 4.2), yaw 86, fov 62, human eye height. The bus-stop angle is in D3.
- **Architecture:** low two-storey plaster shopfronts with flat cornices and shallow cornice lip. Ground-floor glass, striped awnings, one door per shop. Road 7 m wide; sidewalk across the road.
- **Layout (x along the street):** grocer (−16 to −8.5), Asha's café frontage (−8.5 to −1.2), repair shop (−1.2 to 6.2), Market Lane gap with bunting and crosswalk (6.2 to 9.6), a fourth shop (9.6 to 17). Bus shelter at x −8.4 to −4.9; clock post at (0.2, −4.2); tree at (3.4, 5.2).
- **Hero props (≤8):** clock post, bus shelter with bench, street lamps (×4), tree with planter, Market Lane bunting, awnings, café frontage door, crosswalk.
- **Character interaction areas:** bus-stop bench (waiting, conversation); café door (arrivals and exits); clock post (meeting point, time motif); sidewalk strip in front of the shops (walk-and-talk).
- **Reusable assets:** `building`, `shop_front`, `awning`, `lamp`, `clock_post`, `tree`, `bench`, `bus_stop_shelter`, `flag_string` (all in `common.py` / `scene_street.py`).
- **Must stay consistent:** clock post position and its green, the shelter's blue-slate posts and deep-sage roof, awning colours per shop, lamp spacing, light from upper left.

### Time-passing states (A1 → A3)

Creative addition (marked **essential for the story arc**; the match-cut idea itself is optional): the same camera shows Day 1 and Year 10. Visible changes: larger tree plus two more trees, gold sign and deep-sage awning on the repair shop, one closed shutter on the end shop (not everything improves), a blank digital arrivals screen in the shelter, warmer sky. This shows a living street changing, not a transformation.

### Known issues

- A2 has an awning/tree clipping defect (a bite out of the tree). Treat A2 as an orientation reference only.
- Street is mostly empty; no crowds or traffic are modelled.

---

## B. Asha's Café (interior)

**Folder:** `Ashas_Cafe/`

| Image | File | Purpose |
|---|---|---|
| Main wide | `B1_cafe_main_corner.png` | Establishing corner view |
| Extra angle | `B2_cafe_counter_hero.png` | Straight-on counter (hero close shot) |
| Scale test | `B3_cafe_scale_placement_test.png` | Placeholder figures, scale and placement |

### Identity guide

- **Name:** Asha's café (working name; no sign text).
- **Mood:** small, warm, lived-in, quiet working place. Asha is behind the counter, the one place she controls.
- **Palette:** cream walls `#EEE2CA` / plaster `#E3D0AE`, wood `#BC8E62`, dark wood `#85624A`, clay wainscot `#CB9873`, checker floor `#D9C6A6` / `#CDB896`, slate equipment, glass jars, sage plant, pendant lamps warm `#F2DDB0`.
- **Light:** window light from the left (street) wall, key upper-left-front. Pendant lamps are warm secondary accents, not the key.
- **Camera:** main (2.95, 1.65, 0.5), yaw −36, fov 74, eye level from the front-right corner looking diagonally toward the counter. Counter hero (0.1, 1.8, 2.0), pitch 4.5, fov 58.
- **Architecture:** room X −3.4 to 3.4, Z 0 to 7.8, ceiling 3.0 m. Left wall has two windows plus a door to the street. Counter −1.9 to 2.4 at z 5.7–6.5, height 1.05 m.
- **Hero props (≤8):** counter, espresso machine, pastry case, register, tip jar, wall shelves with jars, blank menu chalkboard, Asha's **red notebook**. Supporting: round tables, chairs, plant, pendant lamps.
- **Character interaction areas:** counter front (customer talks to Asha), window tables (two-person conversation), door threshold (arrivals).
- **Reusable assets:** `build_cafe` counter module, table/chair set, pendant lamp, window.
- **Must stay consistent:** counter position and hero-prop order (machine left, pastry case centre, register right), the red notebook on the counter, left-wall windows, pendant lamps raised to ≈2.42 m so Emeka (1.85 m) clears them.

### Creative additions

- **Red notebook** on the counter (**essential**): recurring prop that can carry the "record and plan" idea visually without text.
- **Tip jar** (optional).

### Known issues

- Pendant lamps hang close to the frame top in B3; no collision, but keep Emeka off-centre under them.
- No people in the background; add one or two background silhouettes later only if the shot needs life.

---

## C. Market and Asha's Snack Stall

**Folder:** `Market_Snack_Stall/`

| Image | File | Purpose |
|---|---|---|
| Main wide | `C1_market_stall_main.png` | Asha's stall, hero view |
| Extra angle | `C2_market_row_month6.png` | Same stall module repeated six times, "Month 6" |
| Scale test | `C3_market_scale_placement_test.png` | Placeholder figures, scale and placement |

### Identity guide

- **Name:** Market Plaza / Asha's snack stall.
- **Mood:** open, busy-but-readable, daytime commerce.
- **Palette:** sage and cream striped canopy (Asha's stall), wood counter `#BC8E62`, dark wood back panel `#85624A`, sand counter top `#D8C29C`, baked goods in warm browns `#C98A58` / `#DDB46A`, plaza paving `#D3C9B8`, building plaster `#E3D0AE`, bunting in clay / sage / cream. Other stalls in Month 6 use clay, slate, sand, deep sage canopies.
- **Light:** open sky, key upper-left-front; bunting casts no heavy shadow.
- **Camera:** main (0.9, 1.7, −3.2), yaw −6, fov 60, standing eye level. Row view (0, 2.4, −9), pitch 1.5, fov 78, slightly raised.
- **Stall module (reusable):** 2.6 m wide × 1.6 m deep; counter 1.00 m; canopy front 2.15 m, back 2.45 m; blank hanging price board 1.50–1.95 m; two-tier display, trays, tins, payment stand with blank plate (no QR art, no text), crate and stool.
- **Hero props (≤8):** striped canopy, counter, display tiers with snacks, tins, price board, payment stand, red notebook (Asha's stall only), stool.
- **Character interaction areas:** in front of the counter (customer, 1.5–2 m), behind the counter (Asha), stall side (waiting, queue).
- **Reusable assets:** `stall()` with colour, `plaza()` backdrop, bunting, lamp.
- **Must stay consistent:** Asha's stall is **sage and cream** and has the red notebook; other Month 6 stalls reuse the same module in different canopy colours (the point is replication, not variety); canopy clearance ≥2.15 m for Emeka.

### Creative additions

- **Month 6 row** (C2): shows the same module repeated, so Asha's idea spreads without any "magic" money. Marked **essential if the story includes the spread beat**, otherwise optional.
- Fixed continuity during QC: the notebook was first placed on the wrong stall in C2; it is now on the sage stall.

### Known issues

- No customers or crowds are modelled in C2.
- The hanging price board covers the centre of the counter opening from the customer side. Asha must stand to the right of centre (as in C3) or the board must be moved; otherwise it hides her face.

---

## D. City Bus / Transport

**Folder:** `City_Bus_Transport/`

| Image | File | Purpose |
|---|---|---|
| Main wide | `D1_bus_interior_main.png` | Down the aisle |
| Extra angle | `D2_bus_interior_cab.png` | Driver's cab / front door area |
| Bus-stop view | `D3_bus_stop_exterior.png` | Shelter, bench, bus pulling in |
| Scale test | `D4_bus_scale_placement_test.png` | Placeholder figures in the aisle, staggered |

### Identity guide

- **Name:** City bus (route unnamed, no route text).
- **Mood:** steady, shared, public. Everyone is on the same ride; no one is isolated.
- **Palette:** sage seats `#A3B99D`, deep sage rails `#728F7B`, ceiling cream `#F1E8D6`, floor warm grey `#ABA397`, window glass pale `#CADBD4`, exterior body deep sage with clay stripe.
- **Light:** daylight through windows both sides, ceiling strip lights warm white; key still upper left.
- **Camera:** D1 at the rear looking forward down the aisle; D2 in the front section looking at the driver's area; D3 at (−9.8, 2.5, −14.8), yaw 28, pitch 3, fov 64 across the street toward the bus.
- **Dimensions:** body length 12 m, interior height 2.3 m, **aisle 1.06 m** (see deliberate stylisation below), seat cushion 0.50 m, handrail 2.0 m, door opening 2.02 m.
- **Hero props (≤8):** seat rows, overhead handrails, driver's seat, steering wheel, thermos, card validator, blank destination panel, front door.
- **Character interaction areas:** standing in the aisle (conversation), seats (two-person), front door (boarding, payment tap).
- **Reusable assets:** `seat_row`, `build_bus_interior`, `bus_exterior`, `bus_stop_shelter`.
- **Deliberate stylisation:** the bus is **wider than a realistic city bus** so Emeka's chunky 0.94 m arm-to-arm build fits the aisle. This is a scale choice for the characters; flag it if you prefer a realistic bus and a slimmer Emeka silhouette.

### Known issues (be honest about these)

- **D3 is the weakest composition.** The shelter and bus overlap awkwardly and the bus-stop sign crosses the bus door; a tree behind the bus reads as a green dome. Usable as a stage-setting reference, not as a hero shot.
- **D2 is cluttered**: the validator box, pole and windscreen view of the road compete. Reference only.

---

## Summary of creative additions

| Addition | Where | Status |
|---|---|---|
| Red notebook | B, C | Essential (recurring prop) |
| Same-camera Day 1 / Year 10 | A1 / A3 | Essential for the time arc; match cut optional |
| Month 6 stall row | C2 | Essential only if the spread beat is in the story |
| Closed shutter on the end shop (Year 10) | A3 | Optional (honesty about trade-offs) |
| Digital arrivals screen in the shelter (Year 10) | A3 | Optional |
| Tip jar | B | Optional |

## Not implemented (optional ideas)

- Weather / dusk lighting variants.
- Crowd silhouettes and traffic.
- School / classroom or home interiors (premise includes children and teens; these will be needed if the story shows them. Not in the ~4 environment scope).
- Native vertical re-framed versions of each hero shot.
- True 3D (Blender / cloud tool) models and textured materials.
