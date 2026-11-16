"""Asha's café world (B-series). Room X -3.4..3.4, Z 0..7.8, ceiling 3.0. Counter z 5.7-6.5, 1.05 m high."""
import math
import numpy as np
from engine import Renderer, P, hx, mix, jit
import kit
from kit import *

XL, XR, ZB, ZC, H = -3.4, 3.4, 7.8, 0.0, 3.0
CZ0, CZ1, CH = 5.7, 6.5, 1.05
CX0, CX1 = -1.9, 2.4
WOOD = hx('BB8B5D'); DWOOD = hx('85624A'); TOP = hx('D9C297')
ASHA_X = 0.95          # clear gap behind the counter where Asha stands (between pastry case and terminal)


def cam_b1():
    return dict(pos=(2.95, 1.65, 0.5), yaw=-36.0, pitch=0.0, hfov=74.0)


def cam_b2():
    return dict(pos=(0.25, 1.50, 1.7), yaw=0.0, pitch=2.0, hfov=62.0)


def room(R):
    # ceiling
    R.yrect(XL, XR, ZC - 2, ZB, H, hx('E9DEC8'), n=(0, -1, 0), shade=False, cull=False)
    # floor: 0.6 m checker, two close creams
    t = 0.6
    ca, cb = hx('E3CFA8'), hx('D7C198')
    nx = int(round((XR - XL) / t)); nz = int(round((ZB - ZC) / t))
    for i in range(nx):
        for j in range(nz):
            c = ca if (i + j) % 2 == 0 else cb
            R.yrect(XL + i * t, XL + (i + 1) * t, ZC + j * t, ZC + (j + 1) * t, 0.0, jit(c, R.rng, 2), shade=False, cull=False)
    # back wall with clay wainscot + cap rail
    R.zrect(XL, XR, 0, H, ZB, hx('EDDEBF'), shade=False)
    R.zrect(XL, XR, 0, 1.0, ZB - 0.01, hx('CB966E'), shade=False)
    R.zrect(XL, XR, 1.0, 1.06, ZB - 0.02, hx('EDE6D2'), shade=False)
    # soft vertical gradient on the back wall (light falls off toward the ceiling)
    R.vgrad_poly([(XL, 1.06, ZB - 0.02), (XR, 1.06, ZB - 0.02), (XR, H, ZB - 0.02), (XL, H, ZB - 0.02)], hx('F0E2C4'), hx('E4D4B2'), 8, cull=False)
    # left wall (windows + door): cool, in shade
    wl = hx('CFC6B2')
    R.xrect(ZC, ZB, 0, H, XL, wl, n=(1, 0, 0), shade=False, cull=False)
    R.xrect(ZC, ZB, 0, 1.0, XL + 0.01, hx('B38A6C'), n=(1, 0, 0), shade=False, cull=False)
    R.xrect(ZC, ZB, 1.0, 1.06, XL + 0.02, hx('E2DAC6'), n=(1, 0, 0), shade=False, cull=False)
    # right wall
    R.xrect(ZC, ZB, 0, H, XR, hx('E6D7B6'), n=(-1, 0, 0), shade=False, cull=False)
    R.xrect(ZC, ZB, 0, 1.0, XR - 0.01, hx('C58F67'), n=(-1, 0, 0), shade=False, cull=False)
    R.xrect(ZC, ZB, 1.0, 1.06, XR - 0.02, hx('EDE6D2'), n=(-1, 0, 0), shade=False, cull=False)
    # windows (two panes each, light outside) and the street door
    def wwin(z0, z1, y0=0.95, y1=2.5):
        R.xrect(z0, z1, y0, y1, XL + 0.02, hx('E8E3D4'), n=(1, 0, 0), shade=False)
        zm = (z0 + z1) / 2
        for a, b in ((z0 + 0.07, zm - 0.03), (zm + 0.03, z1 - 0.07)):
            R.poly([(XL + 0.03, y0 + 0.07, a), (XL + 0.03, y0 + 0.07, b), (XL + 0.03, y1 - 0.07, b), (XL + 0.03, y1 - 0.07, a)],
                   hx('EAF3EE'), (1, 0, 0), shade=False, cull=False)
        # sill
        R.box(XL, y0 - 0.05, z0 - 0.04, XL + 0.18, y0, z1 + 0.04, hx('EDE6D2'))
    wwin(0.2, 1.7); wwin(2.0, 3.5)
    # door: z 4.0-5.1
    R.xrect(4.0, 5.1, 0, 2.15, XL + 0.02, hx('7E5A45'), n=(1, 0, 0), shade=False)
    R.poly([(XL + 0.03, 0.04, 4.12), (XL + 0.03, 0.04, 4.98), (XL + 0.03, 2.05, 4.98), (XL + 0.03, 2.05, 4.12)], hx('E6F0EB'), (1, 0, 0), shade=False, cull=False)
    R.line3d((XL + 0.035, 1.0, 4.9), (XL + 0.035, 1.22, 4.9), hx('C8B79B'), 0.03)
    # window light pools on the floor (warm, soft - sells 'window light from the left')
    for z0, z1 in ((0.2, 1.7), (2.0, 3.5)):
        R.shadow([(XL, 0.004, z0 + 0.4), (XL + 2.8, 0.004, z0 + 1.7), (XL + 2.8, 0.004, z1 + 1.5), (XL, 0.004, z1 + 0.2)], 0.20, 14, tint=(255, 246, 222))
    # ambient occlusion where walls meet floor
    R.shadow([(XL, 0.0, ZC), (XL + 0.25, 0.0, ZC), (XL + 0.25, 0.0, ZB), (XL, 0.0, ZB)], 0.12, 6)
    R.shadow([(XL, 0.0, ZB - 0.25), (XR, 0.0, ZB - 0.25), (XR, 0.0, ZB), (XL, 0.0, ZB)], 0.12, 6)
    # ceiling edge shade
    R.shadow([(XL, H, ZB - 0.3), (XR, H, ZB - 0.3), (XR, H, ZB), (XL, H, ZB)], 0.08, 8)


def back_wall_dressing(R):
    # one wooden shelf above head height (so Asha's face never sits on a prop) + blank chalkboard above
    zs = ZB - 0.02
    R.box(-1.75, 1.90, ZB - 0.28, 2.35, 1.96, ZB - 0.02, hx('8F6A50'), top=hx('A47E60'))
    R.shadow([(-1.75, 1.2, ZB - 0.02), (2.35, 1.2, ZB - 0.02), (2.35, 1.9, ZB - 0.02), (-1.75, 1.9, ZB - 0.02)], 0.06, 8)
    for k, x in enumerate((-1.45, -1.0, -0.55)):
        R.prism(x, ZB - 0.15, 1.96, 2.24, 0.095, mix(hx('C9D9CF'), (255, 255, 255), 0.0), n=12, rt=0.09)
        R.prism(x, ZB - 0.15, 2.24, 2.29, 0.10, hx('6F9A7C'), n=12)
    # plant
    R.prism(2.15, ZB - 0.15, 1.96, 2.20, 0.10, hx('C7946C'), n=12, rt=0.12)
    R.sphere((2.12, 2.37, ZB - 0.17), 0.17, hx('7FA382')); R.sphere((2.20, 2.30, ZB - 0.2), 0.13, hx('668F6B'))
    # chalkboard (abstract bars only)
    R.box(-1.0, 2.35, ZB - 0.06, 1.85, 2.95, ZB - 0.02, hx('7C5A43'))
    R.zrect(-0.95, 1.80, 2.40, 2.90, ZB - 0.07, hx('56605F'), shade=False)
    for (a, b, y) in ((-0.7, 0.2, 2.75), (-0.7, -0.1, 2.62), (-0.7, 0.2, 2.49), (1.0, 1.7, 2.75), (1.0, 1.7, 2.62), (1.0, 1.7, 2.49)):
        R.zrect(a, b, y, y + 0.05, ZB - 0.075, hx('E7DFCB'), shade=False)


def counter(R):
    # shadow on floor
    R.shadow([(CX0 - 0.1, 0, CZ0 - 0.2), (CX1 + 0.3, 0, CZ0 - 0.2), (CX1 + 0.3, 0, CZ0), (CX0 - 0.1, 0, CZ0)], 0.30, 9)
    # kick plinth
    R.box(CX0, 0, CZ0 + 0.02, CX1, 0.12, CZ0 + 0.06, hx('7A5640'))
    # body (vertical planks with tonal variation = wood grain)
    R.planks((CX0, 0.12, CZ0), (CX1, 0.12, CZ0), (CX1, CH - 0.06, CZ0), (CX0, CH - 0.06, CZ0), 15, WOOD, amt=7)
    R.line3d((CX0, CH - 0.07, CZ0), (CX1, CH - 0.07, CZ0), mix(WOOD, (60, 40, 28), 0.32), 0.03)
    # side cheeks
    R.box(CX1 - 0.02, 0, CZ0, CX1, CH - 0.06, CZ1, WOOD)
    R.box(CX0, 0, CZ0, CX0 + 0.02, CH - 0.06, CZ1, WOOD)
    # top slab with a slightly lighter front lip and a soft sheen band
    R.box(CX0 - 0.05, CH - 0.06, CZ0 - 0.08, CX1 + 0.05, CH, CZ1 + 0.04, TOP, top=mix(TOP, (255, 240, 205), 0.18), front=mix(TOP, (150, 118, 82), 0.18))
    R.yrect(CX0 + 0.02, CX1 - 0.02, CZ0 - 0.04, CZ0 + 0.10, CH + 0.002, mix(TOP, (255, 245, 220), 0.35), n=(0, 1, 0), shade=False, alpha=0.30)


def machine(R, x0=-1.85, x1=-0.80, z0=5.86, z1=6.42):
    y0 = CH
    steel, dsteel = hx('A2AAAB'), hx('7A868A')
    R.foot_shadow((x0 + x1) / 2, (z0 + z1) / 2, x1 - x0, z1 - z0, h=0.5, op=0.20, sig=3, y=y0)
    # drip tray with grill slots
    R.box(x0 + 0.06, y0, z0 - 0.12, x1 - 0.06, y0 + 0.05, z0, hx('5E656A'), top=hx('4A5055'))
    for k in range(7):
        xx = x0 + 0.14 + k * (x1 - x0 - 0.28) / 6
        R.line3d((xx, y0 + 0.052, z0 - 0.10), (xx, y0 + 0.052, z0 - 0.02), hx('8B9296'), 0.012)
    # body
    R.box(x0, y0 + 0.05, z0, x1, y0 + 0.62, z1, steel, top=mix(steel, (240, 245, 245), 0.2), left=mix(steel, (60, 70, 80), 0.1))
    # top cup-warmer rail + chrome strip
    R.box(x0 - 0.02, y0 + 0.62, z0 - 0.02, x1 + 0.02, y0 + 0.68, z1 + 0.02, dsteel, top=mix(dsteel, (235, 240, 240), 0.35))
    R.zrect(x0 + 0.04, x1 - 0.04, y0 + 0.57, y0 + 0.595, z0 - 0.003, hx('DADFDD'), shade=False)
    # sage accent panel + group heads (2) with portafilter handles
    R.zrect(x0 + 0.05, x1 - 0.05, y0 + 0.40, y0 + 0.51, z0 - 0.004, hx('6E8B76'))
    for gx in (x0 + 0.27, x1 - 0.27):
        R.prism(gx, z0 - 0.045, y0 + 0.17, y0 + 0.36, 0.07, hx('9BA3A6'), n=14, rt=0.065)
        R.prism(gx, z0 - 0.045, y0 + 0.12, y0 + 0.17, 0.075, hx('34363C'), n=14)
        R.box(gx - 0.02, y0 + 0.12, z0 - 0.30, gx + 0.02, y0 + 0.155, z0 - 0.04, hx('2F3036'))       # handle toward the barista
        R.box(gx - 0.035, y0 + 0.10, z0 - 0.10, gx + 0.035, y0 + 0.12, z0 - 0.04, hx('2F3036'))
        R.disc((gx, y0 + 0.46, z0 - 0.006), (0, 0, -1), 0.028, hx('E9E3D1'), n=14, shade=False)    # gauge
    # steam wand on the right side
    R.tube((x1 - 0.03, y0 + 0.36, z0 + 0.06), (x1 + 0.04, y0 + 0.20, z0 - 0.06), 0.014, hx('B8C0C2'), n=6)
    R.tube((x1 + 0.04, y0 + 0.20, z0 - 0.06), (x1 + 0.06, y0 + 0.05, z0 - 0.10), 0.014, hx('B8C0C2'), n=6)
    # cups on the warmer rail
    for k, cx in enumerate((x0 + 0.20, x0 + 0.36, x0 + 0.52)):
        R.prism(cx, (z0 + z1) / 2, y0 + 0.68, y0 + 0.78, 0.045, hx('F1EBDD') if k != 1 else hx('DCC9A4'), n=10, rt=0.055)
    # small milk jug beside
    R.prism(x1 + 0.20, z0 + 0.20, y0, y0 + 0.17, 0.05, hx('B8C0C2'), n=10, rt=0.06)


def pastry_case(R, x0=-0.55, x1=0.45, z0=5.90, z1=6.40):
    y0 = CH
    R.foot_shadow((x0 + x1) / 2, (z0 + z1) / 2, x1 - x0, z1 - z0, h=0.4, op=0.16, sig=3, y=y0)
    R.box(x0, y0, z0, x1, y0 + 0.05, z1, hx('8A6448'), top=hx('A47E60'))
    R.zrect(x0 + 0.03, x1 - 0.03, y0 + 0.05, y0 + 0.07, z0 - 0.004, hx('EEE7D3'), shade=False)
    # pastries on two tiers
    cols = [hx('C8946B'), hx('D9B46A'), hx('C8946B'), hx('D9B46A')]
    for k in range(4):
        px = x0 + 0.12 + k * (x1 - x0 - 0.24) / 3
        R.sphere((px, y0 + 0.12, (z0 + z1) / 2 - 0.05), 0.065, cols[k], squash=0.75)
    R.box(x0 + 0.04, y0 + 0.24, z0 + 0.06, x1 - 0.04, y0 + 0.255, z1 - 0.06, hx('E8E1CF'), top=hx('F3EEDD'))
    for k in range(3):
        px = x0 + 0.17 + k * (x1 - x0 - 0.34) / 2
        R.sphere((px, y0 + 0.31, (z0 + z1) / 2 - 0.02), 0.06, (hx('D9B46A'), hx('C8946B'), hx('E2C48A'))[k], squash=0.7)
    # glass (front, top, left face) + frame posts; soft streak = reflection
    for xx in (x0, x1):
        R.box(xx - 0.012, y0 + 0.05, z0 - 0.012, xx + 0.012, y0 + 0.46, z0 + 0.012, hx('8A6448'))
    R.box(x0, y0 + 0.455, z0 - 0.012, x1, y0 + 0.47, z1, hx('8A6448'), top=hx('A47E60'))
    R.poly([(x0, y0 + 0.07, z0 - 0.01), (x1, y0 + 0.07, z0 - 0.01), (x1, y0 + 0.455, z0 - 0.01), (x0, y0 + 0.455, z0 - 0.01)], hx('D5E6E0'), (0, 0, -1), shade=False, alpha=0.20, cull=False)
    R.poly([(x0 + 0.12, y0 + 0.07, z0 - 0.012), (x0 + 0.20, y0 + 0.07, z0 - 0.012), (x0 + 0.34, y0 + 0.455, z0 - 0.012), (x0 + 0.26, y0 + 0.455, z0 - 0.012)], (255, 255, 255), (0, 0, -1), shade=False, alpha=0.20, cull=False)
    R.xrect(z0, z1, y0 + 0.07, y0 + 0.455, x0, hx('D5E6E0'), shade=False, alpha=0.16, cull=False)
    R.xrect(z0, z1, y0 + 0.07, y0 + 0.455, x1, hx('D5E6E0'), shade=False, alpha=0.16, cull=False)


def terminal(R, x=1.60, z=6.05):
    """card/payment terminal on a short stand: screen + reader + keypad dots. Blank - no text, no QR."""
    y0 = CH
    R.foot_shadow(x, z, 0.5, 0.3, h=0.3, op=0.16, sig=3, y=y0)
    sl, ds = hx('7A868A'), hx('3E3C44')
    R.box(x - 0.17, y0, z - 0.10, x + 0.17, y0 + 0.035, z + 0.10, sl, top=mix(sl, (235, 240, 240), 0.2))
    R.box(x - 0.03, y0 + 0.035, z + 0.01, x + 0.03, y0 + 0.21, z + 0.07, sl)
    # tilted screen
    q = [(x - 0.15, y0 + 0.18, z + 0.07), (x + 0.15, y0 + 0.18, z + 0.07), (x + 0.15, y0 + 0.38, z + 0.01), (x - 0.15, y0 + 0.38, z + 0.01)]
    R.poly(q, hx('50525C'), (0, 0.4, -1), shade=False, cull=False)
    inner = [(x - 0.13, y0 + 0.195, z + 0.063), (x + 0.13, y0 + 0.195, z + 0.063), (x + 0.13, y0 + 0.365, z + 0.016), (x - 0.13, y0 + 0.365, z + 0.016)]
    R.poly(inner, ds, (0, 0.4, -1), shade=False, cull=False)
    R.poly([(x - 0.09, y0 + 0.30, z + 0.04), (x + 0.09, y0 + 0.30, z + 0.04), (x + 0.09, y0 + 0.315, z + 0.036), (x - 0.09, y0 + 0.315, z + 0.036)], hx('7FB6B2'), (0, 0.4, -1), shade=False, cull=False)
    # card reader to the right: slim box with a slot line + 3x2 keypad dots
    R.box(x + 0.22, y0, z - 0.07, x + 0.38, y0 + 0.07, z + 0.08, hx('5E656A'), top=hx('7A868A'))
    R.line3d((x + 0.235, y0 + 0.072, z - 0.0), (x + 0.365, y0 + 0.072, z - 0.0), hx('2F3036'), 0.012)
    for i in range(3):
        for j in range(2):
            R.disc((x + 0.255 + i * 0.045, y0 + 0.073, z + 0.025 - j * 0.04), (0, 1, 0), 0.012, hx('A8B0B2'), n=8, shade=False)


def small_props(R):
    y0 = CH
    # red notebook (recurring prop) just right of the pastry case, angled, in front of Asha's hands
    obox(R, ASHA_X - 0.05, 6.14, y0, y0 + 0.028, 0.11, 0.15, -12, hx('C4473B'), top=hx('D45A4C'), front=hx('A83B31'))
    R.line3d((ASHA_X - 0.12, y0 + 0.03, 6.20), (ASHA_X + 0.02, y0 + 0.03, 6.15), hx('EDE0C8'), 0.01)
    obox(R, ASHA_X + 0.17, 6.12, y0, y0 + 0.008, 0.03, 0.10, -12, hx('2F3036'))     # pen
    # tip jar: glass cylinder + a few gold coins (earned, modest)
    R.foot_shadow(2.18, 6.1, 0.25, 0.25, h=0.2, op=0.16, sig=3, y=y0)
    R.prism(2.18, 6.1, y0, y0 + 0.20, 0.075, hx('CFE0DA'), n=14)
    for k in range(3):
        R.disc((2.18 + (k - 1) * 0.03, y0 + 0.012 + k * 0.012, 6.1 - 0.03), (0, 1, 0), 0.022, hx('D9B25F'), n=10, shade=False)
    # a small folded napkin stack and two cups near the customer end of the counter
    R.box(2.02, y0, 5.84, 2.14, y0 + 0.08, 5.94, hx('F1EBDD'), top=hx('FAF5E8'))


def pendant(R, x, z, drop=0.55):
    yb = 2.42            # lamp bottom >= 2.10 (Emeka 1.85 + cap) - guide value
    R.line3d((x, H, z), (x, yb + 0.35, z), hx('3A3840'), 0.012)
    R.prism(x, z, H - 0.05, H, 0.07, hx('8A8F92'), n=10)
    R.sphere((x, yb + 0.17, z), 0.27, hx('F3E1B2'), squash=0.74)
    R.disc((x, yb + 0.02, z), (0, -1, 0), 0.08, hx('FFF3CF'), n=12, shade=False)


def furniture(R, plan):
    items = []
    campos = np.array([R.pos[0], R.pos[2]])
    for kind, x, z, ang in plan:
        d = (x - campos[0]) ** 2 + (z - campos[1]) ** 2
        items.append((d, kind, x, z, ang))
    items.sort(key=lambda t: -t[0])
    for d, kind, x, z, ang in items:
        if kind == 'table':
            round_table(R, x, z)
        else:
            chair(R, x, z, ang)


# default furniture plan (all pieces fully inside the B1 frame; nothing occupies the counter front or Asha's gap)
def plan_default():
    pl = []
    # window table (two-person conversation spot under the windows)
    pl += [('table', -2.3, 3.0, 0), ('chair', -3.0, 3.0, 90), ('chair', -1.6, 3.0, 270)]
    # mid-room table, kept well back from the counter front so customers can stand there
    pl += [('table', -0.4, 4.5, 0), ('chair', -1.1, 4.5, 90), ('chair', 0.3, 4.5, 270)]
    return pl


def plan_b3():
    return [('table', -2.3, 3.0, 0), ('chair', -3.0, 3.0, 90), ('chair', -1.6, 3.0, 270)]


def build(R, plan=None, pendants=((-1.6, 4.2), (0.4, 3.9), (1.9, 4.5)), behind=None):
    """behind: optional callable drawn after the room shell and before the counter (people standing behind the counter)"""
    room(R)
    back_wall_dressing(R)
    if behind:
        behind(R)
    counter(R)
    machine(R); pastry_case(R); terminal(R); small_props(R)
    furniture(R, plan if plan is not None else plan_default())
    for px, pz in pendants:
        pendant(R, px, pz)


def render(cam=None, **kw):
    cam = cam or cam_b1()
    R = Renderer(pos=cam['pos'], yaw=cam['yaw'], pitch=cam['pitch'], hfov=cam['hfov'], ss=2)
    build(R, **kw)
    return R


if __name__ == '__main__':
    SP = '/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    R = render(); kit.grade(R.finish(), vig=0.08).save(SP + 'b1_test.png')
    R = render(cam_b2()); kit.grade(R.finish(), vig=0.08).save(SP + 'b2_test.png')
