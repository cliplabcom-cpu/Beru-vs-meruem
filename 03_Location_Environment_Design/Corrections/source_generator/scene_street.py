"""Clock Street world (A-series). One world, several cameras, two states (Day 1 / Year 10)."""
import math
import numpy as np
from engine import Renderer, P, hx, mix, jit
import kit
from kit import *

ZF = 6.5          # shopfront plane
CURB_N, CURB_F = -2.9, 4.1   # near / far curb (road = 7.0 m)
ZMAX = 60.0


def cam_main():
    return dict(pos=(-2.4, 2.3, -15.0), yaw=0.0, pitch=0.0, hfov=66.0)


def cam_along():
    return dict(pos=(-21.0, 1.75, 4.5), yaw=86.0, pitch=0.0, hfov=62.0)


# ---------------------------------------------------------------------------------------------------------------- state
def S(year):
    y10 = year >= 10
    d = dict(y10=y10)
    # muted warm walls; Year 10 = same family, fresher (repainted, not recoloured)
    f = 0.0 if y10 else 0.06
    dull = lambda c: mix(c, (190, 180, 160), f)
    d['dull'] = dull
    d['grocer'] = dull(hx('DCC9A3')); d['cafe'] = dull(hx('E4D3B0')); d['repair'] = dull(hx('D0BB93')); d['shop4'] = dull(hx('E1CCA4'))
    d['awn_grocer'] = (dull(hx('A8BD9F')), hx('F0E4CB'))
    d['awn_cafe'] = (dull(hx('CB9873')), hx('F0E4CB'))
    d['awn_repair'] = ((hx('729A82'), hx('F0E4CB')) if y10 else (dull(hx('7B8892')), hx('E8DDC4')))
    d['awn_shop4'] = (dull(hx('C48E68')), hx('EFE2C6'))
    return d


# ---------------------------------------------------------------------------------------------------------------- ground
def ground(R, year):
    y10 = year >= 10
    pave = hx('D6CAB2') if not y10 else hx('DCCFB4')
    pave2 = mix(pave, (150, 140, 120), 0.06)
    road = hx('938B7F') if not y10 else hx('8E8A82')
    curb = hx('E3D9C4')
    X0, X1 = -80, 80
    # base layers (unshaded, sampled colours)
    R.yrect(X0, X1, CURB_N, ZMAX, 0.0, road, shade=False)                      # road under everything
    R.yrect(X0, X1, -40, CURB_N, 0.12, pave, shade=False, cull=False)         # near sidewalk top
    R.yrect(X0, X1, CURB_F, ZF + 0.02, 0.12, pave2, shade=False, cull=False)   # far sidewalk top
    # lane mouth: pavement continues into Market Lane
    R.yrect(6.2, 9.6, ZF, ZMAX, 0.12, pave2, shade=False, cull=False)
    # curb faces
    R.poly([(X0, 0, CURB_N), (X1, 0, CURB_N), (X1, 0.12, CURB_N), (X0, 0.12, CURB_N)], mix(pave, (120, 110, 100), 0.20), (0, 0, -1), shade=False)
    R.poly([(X0, 0, CURB_F), (X1, 0, CURB_F), (X1, 0.12, CURB_F), (X0, 0.12, CURB_F)], mix(pave, (120, 110, 100), 0.22), (0, 0, 1), shade=False, cull=False)
    R.yrect(X0, X1, CURB_N - 0.18, CURB_N, 0.121, curb, shade=False, cull=False)   # lighter curb nosing
    R.yrect(X0, X1, CURB_F, CURB_F + 0.18, 0.121, curb, shade=False, cull=False)
    # road markings
    zc = (CURB_N + CURB_F) / 2
    for x in np.arange(-40, 40, 5.2):
        R.yrect(x, x + 2.4, zc - 0.07, zc + 0.07, 0.003, hx('EFE7D4'), shade=False, cull=False)
    for zz in (CURB_N + 0.35, CURB_F - 0.35):
        R.yrect(X0, X1, zz - 0.05, zz + 0.05, 0.003, mix(road, (235, 228, 210), 0.45), shade=False, cull=False)
    # zebra crossing at Market Lane mouth
    for k in range(8):
        x = 6.55 + k * 0.62
        R.yrect(x, x + 0.34, CURB_N + 0.55, CURB_F - 0.55, 0.004, hx('F0E8D6'), shade=False, cull=False)
    # paving joints (very low contrast) - gives the empty foreground scale + perspective
    jc = mix(pave, (130, 118, 98), 0.13)
    rows = [CURB_N - 0.18 - 1.2 * k for k in range(0, 9)]
    for k, z in enumerate(rows):
        R.line3d((-45, 0.125, z), (45, 0.125, z), jc, 0.022)
    for k in range(len(rows) - 1):
        zz0, zz1 = rows[k], rows[k + 1]
        for xj in np.arange(-44 + (0.6 if k % 2 else 0), 44, 1.2):
            R.line3d((xj, 0.125, zz0), (xj, 0.125, zz1), jc, 0.02)
    for x in np.arange(-44, 44, 1.2):    # far sidewalk joints
        R.line3d((x, 0.125, CURB_F + 0.18), (x, 0.125, ZF), jc, 0.02)
    R.line3d((-45, 0.125, 5.3), (45, 0.125, 5.3), jc, 0.02)
    # tactile strip beside the near curb (a modest accessibility cue)
    R.yrect(-30, 30, CURB_N - 0.75, CURB_N - 0.18, 0.124, mix(pave, (205, 175, 120), 0.35), shade=False, cull=False)
    for x in np.arange(-30, 30, 0.45):
        R.line3d((x, 0.126, CURB_N - 0.72), (x, 0.126, CURB_N - 0.21), mix(pave, (170, 140, 90), 0.4), 0.03)
    # drain grate + manhole (street furniture that doubles as foreground scale cues)
    for xg in (-9.0, 4.8):
        R.yrect(xg, xg + 0.9, CURB_N + 0.0, CURB_N + 0.4, 0.004, mix(road, (60, 56, 56), 0.55), shade=False, cull=False)
    R.disc((-0.4, 0.125, -8.4), (0, 1, 0), 0.38, mix(pave, (110, 100, 90), 0.28), n=24, shade=False)
    R.disc((-0.4, 0.126, -8.4), (0, 1, 0), 0.30, mix(pave, (110, 100, 90), 0.16), n=24, shade=False)
    if not y10:
        rng = np.random.RandomState(3)
        # worn asphalt patch + a couple of hairline pavement cracks = a street that has seen better days
        R.shadow([(-5.6, 0.0, 0.2), (-2.6, 0.0, 0.2), (-2.6, 0.0, 1.6), (-5.6, 0.0, 1.6)], 0.07, 12, tint=(120, 112, 104))
        for (a, b) in (((-12.0, 0.126, -4.5), (-11.1, 0.126, -5.5)), ((-11.1, 0.126, -5.5), (-10.9, 0.126, -6.6))):
            R.line3d(a, b, mix(pave, (90, 80, 70), 0.35), 0.03)
    else:
        # Year 10: one painted cycle lane on the far side of the road - a quiet, modest public-space gain
        R.yrect(-80, 80, CURB_F - 1.75, CURB_F - 0.20, 0.004, hx('9DB59A'), shade=False, cull=False)


def backdrop(R):
    """distant, hazy low-contrast skyline seen through the Market Lane gap and over the roofs"""
    rng = np.random.RandomState(11)
    x = -140
    while x < 140:
        w = rng.uniform(6, 12); h = rng.uniform(9, 17)
        c = mix(hx('D9D2BE'), (200, 214, 214), rng.uniform(0.25, 0.5))
        R.box(x, 0, 58, x + w, h, 70, c, top=mix(c, (240, 236, 224), 0.4), skip=('bottom', 'back'))
        # a few pale windows
        for wx in np.arange(x + 1, x + w - 1, 2.2):
            for wy in np.arange(3.0, h - 1.5, 3.1):
                R.zrect(wx, wx + 0.9, wy, wy + 1.4, 57.9, mix(c, (190, 205, 205), 0.55), shade=False)
        x += w + rng.uniform(0.0, 0.8)
    # mid-distance block rows (a little less hazy) behind the lane
    R.box(5, 0, 28, 14, 10.5, 40, mix(hx('DCCDAE'), (200, 214, 214), 0.30), top=hx('E8E0CC'), skip=('bottom', 'back'))
    R.box(-14, 0, 24, -3, 9.5, 36, mix(hx('DCCDAE'), (200, 214, 214), 0.34), top=hx('E8E0CC'), skip=('bottom', 'back'))


# ---------------------------------------------------------------------------------------------------------------- buildings
def buildings(R, year):
    s = S(year); y10 = s['y10']
    B = []   # (centre_x, draw_fn): drawn farthest-first (by x distance to the camera) so side walls overlap correctly

    def neighbour_l():
        facade(R, -34, -16, 7.0, ZF, haze(hx('D9C7A4'), 28), windows=3, win_w=1.3, left_wall=False)
        shop_ground(R, -34, -16, ZF, -25.0, awn=None, door_frame=hx('8A6A52'), plinth_col=hx('8A6850'))

    def neighbour_r():
        facade(R, 17, 36, 7.6, ZF, haze(hx('DCC9A4'), 28), windows=3, win_w=1.3)
        shop_ground(R, 17, 36, ZF, 28.0, awn=None, door_frame=hx('8A6A52'), plinth_col=hx('8A6850'))

    def grocer():
        facade(R, -16, -8.5, 7.2, ZF, s['grocer'], windows=2)
        shop_ground(R, -16, -8.5, ZF, -9.9, awn=s['awn_grocer'], door_frame=hx('8A6A52'))

    def cafe():
        facade(R, -8.5, -1.2, 8.7, ZF, s['cafe'], windows=2)
        shop_ground(R, -8.5, -1.2, ZF, -2.35, awn=s['awn_cafe'], door_frame=hx('7E5A45'))

    def repair():
        facade(R, -1.2, 6.2, 6.7, ZF, s['repair'], windows=2)
        shop_ground(R, -1.2, 6.2, ZF, 5.0, awn=s['awn_repair'], door_frame=hx('7E5A45'))
        if y10:   # earned gold, used once, as a sign band (guide: gold = earned success)
            R.box(0.2, 3.02, ZF - 0.20, 4.2, 3.40, ZF - 0.05, hx('D9B25F'), top=hx('E6C679'))
            R.box(0.4, 3.12, ZF - 0.215, 1.5, 3.30, ZF - 0.20, hx('EAD08A'))

    def gateway():
        awning(R, 6.45, 9.35, ZF, 3.1, 2.55, 0.5, hx('A8BD9F'), hx('F0E4CB'), stripe=0.5)

    def shop4():
        facade(R, 9.6, 17, 7.4, ZF, s['shop4'], windows=2)
        shop_ground(R, 9.6, 17, ZF, 15.0, awn=s['awn_shop4'], door_frame=hx('7E5A45'))
        if y10:   # shutter down on one unit: not everything improves
            R.zrect(10.2, 12.9, 0.1, 2.2, ZF - 0.07, hx('A9A396'))
            for k in range(14):
                R.line3d((10.2, 0.2 + k * 0.15, ZF - 0.08), (12.9, 0.2 + k * 0.15, ZF - 0.08), hx('8C867B'), 0.03)
        R.shadow([(9.58, 0, ZF), (9.58, 0, 26), (9.58, 0.5, 26), (9.58, 0.5, ZF)], 0.12, 7)

    for cx, fn in ((-25, neighbour_l), (26, neighbour_r), (-12.25, grocer), (-4.85, cafe), (2.5, repair), (13.3, shop4), (7.9, gateway)):
        B.append((cx, fn))
    camx = R.pos[0]
    B.sort(key=lambda t: -abs(t[0] - camx))
    for _, fn in B:
        fn()


def opposite_row(R, year):
    """hazy low buildings + trees far across the open plaza (only seen from along-street cameras)"""
    rng = np.random.RandomState(5)
    x = -90
    while x < 120:
        w = rng.uniform(7, 13); h = rng.uniform(4.2, 6.4)
        c = mix(hx('DCCFB2'), (205, 216, 214), 0.38)
        R.box(x, 0, -34, x + w, h, -26, c, top=mix(c, (240, 236, 224), 0.4), skip=('bottom', 'back'), front=c)
        R.box(x - 0.1, h - 0.1, -34.4, x + w + 0.1, h + 0.3, -25.8, mix(c, (245, 240, 228), 0.4))
        for wx in np.arange(x + 1.2, x + w - 1.2, 2.6):
            R.zrect(wx, wx + 1.2, 1.0, 2.4, -34.05, mix(c, (170, 195, 195), 0.5), shade=False)
        x += w + rng.uniform(0.3, 1.4)
    for tx in np.arange(-88, 118, 7.5):
        R.sphere((tx, 3.6, -22 + (tx % 3) * 0.3), 1.5, mix(P['tree'], (205, 216, 214), 0.45))
        R.line3d((tx, 0.0, -22), (tx, 2.6, -22), mix(hx('8C6B52'), (205, 216, 214), 0.4), 0.18)
    # street end block (terminates the long view)
    R.box(78, 0, -20, 96, 9.5, 40, mix(hx('DCCDAE'), (205, 216, 214), 0.45), top=hx('E8E0CC'), skip=('bottom', 'back'))


# ---------------------------------------------------------------------------------------------------------------- street furniture
def shelter(R, x0, x1, z0, z1, year, front_glass=True):
    y10 = year >= 10
    slate = P['slate']; ds = P['dsage']
    R.foot_shadow((x0 + x1) / 2, (z0 + z1) / 2 + 0.2, x1 - x0, z1 - z0, h=2.4, op=0.20, sig=8)
    # translucent back glass (camera side) kept very light so the shopfronts behind stay readable
    # bench first (inside), glass after so it softens the bench slightly like real glazing
    bench(R, (x0 + x1) / 2, (z0 + z1) / 2 + 0.05, w=(x1 - x0) - 0.55)
    for x in (x0 + 0.07, x1 - 0.07):
        for z in (z0 + 0.07, z1 - 0.07):
            R.box(x - 0.055, 0.0, z - 0.055, x + 0.055, 2.42, z + 0.055, slate)
    if front_glass:
        for xa, xb in ((x0 + 0.13, x1 - 0.13),):
            R.poly([(xa, 0.55, z0 + 0.03), (xb, 0.55, z0 + 0.03), (xb, 2.15, z0 + 0.03), (xa, 2.15, z0 + 0.03)], hx('CFE0DC'), (0, 0, -1), shade=False, alpha=0.20, cull=False)
        R.xrect(z0, z1, 0.55, 2.15, x0 + 0.05, hx('CFE0DC'), shade=False, alpha=0.30, cull=False)
        R.xrect(z0, z1, 0.55, 2.15, x1 - 0.05, hx('CFE0DC'), shade=False, alpha=0.30, cull=False)
    # thin roof slab
    R.box(x0 - 0.18, 2.40, z0 - 0.20, x1 + 0.18, 2.52, z1 + 0.20, ds, top=mix(ds, (230, 240, 225), 0.20))
    R.box(x0 - 0.18, 2.52, z0 - 0.20, x1 + 0.18, 2.58, z0 - 0.15, mix(ds, (230, 240, 225), 0.2))
    # route plate ledge on the camera side (blank)
    R.box(x0 + 0.3, 1.02, z0 + 0.02, x1 - 0.3, 1.10, z0 + 0.10, hx('E8E0CC'))
    if y10:     # arrivals screen on a short post at the shelter's right end: blank teal panel, no text
        R.box(x1 + 0.35, 0, z0 - 0.04, x1 + 0.45, 1.8, z0 + 0.06, slate)
        R.box(x1 + 0.12, 1.45, z0 - 0.10, x1 + 0.74, 2.02, z0 - 0.04, hx('3E3C44'))
        R.zrect(x1 + 0.17, x1 + 0.69, 1.50, 1.97, z0 - 0.105, hx('7FB6B2'), shade=False)


def stop_sign(R, x, z, h=2.75):
    R.foot_shadow(x, z, 0.3, 0.3, h=h * 0.4, op=0.16, sig=4)
    R.prism(x, z, 0, h, 0.045, P['slate'], n=8)
    R.disc((x, h + 0.30, z - 0.06), (0, 0, -1), 0.30, hx('9CB398'), n=30)
    R.disc((x, h + 0.30, z - 0.07), (0, 0, -1), 0.20, hx('EDE4CD'), n=30, shade=False)


def cafe_set(R, x, z):
    R.foot_shadow(x, z, 0.8, 0.8, h=0.76, op=0.2, sig=4)
    R.prism(x, z, 0.0, 0.74, 0.04, P['slate'], n=8)
    R.prism(x, z, 0.74, 0.78, 0.36, hx('E8DDC4'), n=20)
    for dx in (-0.62, 0.62):
        R.foot_shadow(x + dx, z, 0.45, 0.45, h=0.5, op=0.16, sig=3)
        R.box(x + dx - 0.2, 0.0, z - 0.2, x + dx + 0.2, 0.46, z + 0.2, hx('B8805C'), top=hx('C9966F'))
        R.box(x + dx - 0.2, 0.46, z + 0.17, x + dx + 0.2, 0.9, z + 0.2, hx('B8805C'))


def window_boxes(R, xs, y, z):
    for x in xs:
        R.box(x - 0.55, y - 0.28, z - 0.28, x + 0.55, y, z, hx('B8805C'), top=hx('7A5B44'))
        for k, dx in enumerate((-0.38, -0.12, 0.14, 0.38)):
            R.sphere((x + dx, y + 0.12, z - 0.12), 0.17, (hx('8AAE80'), hx('6F9A6E'))[k % 2])


def a_frame(R, x, z, col=None):
    col = col or hx('E8DDC4')
    R.foot_shadow(x, z, 0.7, 0.5, h=0.9, op=0.18, sig=3)
    R.poly([(x - 0.33, 0.12, z - 0.18), (x + 0.33, 0.12, z - 0.18), (x + 0.28, 0.98, z - 0.02), (x - 0.28, 0.98, z - 0.02)], col, (0, 0.3, -1))
    R.line3d((x - 0.33, 0.12, z - 0.19), (x - 0.28, 0.98, z - 0.03), P['dwood'], 0.04)
    R.line3d((x + 0.33, 0.12, z - 0.19), (x + 0.28, 0.98, z - 0.03), P['dwood'], 0.04)


# ---------------------------------------------------------------------------------------------------------------- composition
def build(R, year, variant='main', clock_x=2.3, tree_x=-0.9, lamps=(-17.5, -8.9, 3.3, 13.7), planters=True, near_bin=True):
    y10 = year >= 10
    R.sky(SKY_TOP if not y10 else hx('C2D8DC'), SKY_BOT if not y10 else hx('F7E6C6'), R.h / 2 / R.ss)
    # warm horizon glow band (sits behind the skyline)
    backdrop(R)
    opposite_row(R, year)
    ground(R, year)
    buildings(R, year)
    # --- far-side objects (z ~ 4-6) ---------------------------------------------------------------------------
    items = []
    # lamps along the far curb
    for lx in lamps:
        if variant == 'along' and abs(lx - R.pos[0]) < 8.5:
            continue
        items.append((lx, CURB_F - 0.25, lambda lx=lx: lamp(R, lx, CURB_F - 0.25, 4.5, lit=y10)))
    # trees (Year 10 = more, bigger, crowns raised so they never cover shop windows or awnings)
    trees = [(tree_x, 5.35, 0.82 if not y10 else 1.05)]
    if y10:
        trees += [(-11.0, 5.35, 0.92)]
    for tx, tz, ts in trees:
        items.append((tx, tz, lambda tx=tx, tz=tz, ts=ts: tree(R, tx, tz, ts, crown_y=2.95 + (0.15 if y10 else 0.0), hs=1.0)))
    # shop dressing
    items.append((-13.8, 5.9, lambda: (crate(R, -14.5, 5.8, produce=[hx('C98A58'), hx('DDB46A'), hx('C98A58')]), crate(R, -13.8, 5.8, produce=[hx('9FB48E'), hx('9FB48E')]),
                                         crate(R, -13.15, 5.85, produce=[hx('DDB46A')] * 3), crate(R, -14.15, 5.75, w=0.5, h=0.62))))
    items.append((-7.4, 5.9, lambda: bin_(R, -7.4, 5.8)))
    if planters:
        items.append((-1.8, 5.8, lambda: planter(R, -1.55, 5.75, 0.6, 0.45)))
        items.append((-3.2, 5.8, lambda: planter(R, -3.15, 5.75, 0.6, 0.45)))
    if y10:
        items.append((-4.6, 5.4, lambda: cafe_set(R, -4.6, 5.25)))
        items.append((14.3, 5.8, lambda: planter(R, 13.6, 5.8, 0.7, 0.55)))
        items.append((5.9, 5.8, lambda: planter(R, 6.0, 5.8, 0.55, 0.5)))
        items.append((-8.1, 5.8, lambda: planter(R, -8.0, 5.8, 0.6, 0.5)))
    else:
        items.append((6.0, 5.8, lambda: bicycle(R, 7.6, 5.7)))
    # --- near-side objects --------------------------------------------------------------------------------------
    sx0, sx1 = (-8.8, -6.2)
    items.append(((sx0 + sx1) / 2, -3.6, lambda: shelter(R, sx0, sx1, -3.95, -3.2, year)))
    items.append((-5.6, -3.4, lambda: stop_sign(R, -5.6, -3.4)))
    items.append((clock_x, -3.7, lambda: clock_post(R, clock_x, -3.7, 3.55)))
    if near_bin:
        items.append((3.4, -3.5, lambda: bin_(R, 3.6, -3.45)))
    if variant == 'main' and not y10:
        items.append((-10.9, -3.7, lambda: bicycle(R, -11.4, -3.7)))
    # lamp on near side (Year 10 adds a second row on the near sidewalk for a better lit public space)
    if y10:
        items.append((9.8, -3.6, lambda: lamp(R, 9.8, -3.6, 4.2, lit=True)))
    if y10:
        # window boxes under the upper windows: cheap, visible greening
        for (xa, xb, n) in ((-16.0, -8.5, 2), (-1.2, 6.2, 2)):
            span = xb - xa
            items.append((xa, ZF - 0.5, lambda xa=xa, span=span, n=n: window_boxes(R, [xa + span * (i + 0.5) / n for i in range(n)], 4.45, ZF - 0.05)))
    # distant bunting: Market Lane
    bunting(R, (6.4, 3.35, ZF - 0.30), (9.55, 3.35, ZF - 0.30), 3.35, ZF - 0.30, [hx('CB9873'), hx('A3B99D'), hx('F0E4CB')], sag=0.28, n=11, flag=0.25)
    campos = np.array([R.pos[0], R.pos[2]])
    items.sort(key=lambda it: -((it[0] - campos[0]) ** 2 + (it[1] - campos[1]) ** 2))
    for _, _, fn in items:
        fn()


def render_street(year=1, variant='main', cam=None, **kw):
    cam = cam or cam_main()
    R = Renderer(pos=cam['pos'], yaw=cam['yaw'], pitch=cam['pitch'], hfov=cam['hfov'], ss=2)
    build(R, year, variant, **kw)
    return R


if __name__ == '__main__':
    import sys
    SP = '/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    for yr, nm in ((1, 'a1_test'), (10, 'a3_test')):
        R = render_street(yr)
        kit.grade(R.finish()).save(SP + nm + '.png')
    R = render_street(1, 'along', cam=cam_along())
    kit.grade(R.finish()).save(SP + 'a2_test.png')
