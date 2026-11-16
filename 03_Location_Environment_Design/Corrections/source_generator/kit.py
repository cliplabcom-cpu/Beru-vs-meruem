"""Shared set-dressing kit (street / café / market / bus) on top of engine.Renderer."""
import math
import numpy as np
from PIL import Image, ImageFilter
from engine import Renderer, P, hx, mix, jit

SKY_TOP = hx('BDD8E2')
SKY_BOT = hx('F3E8CE')


def haze(col, d, k=0.011, kmax=0.34, sky=(222, 226, 216)):
    t = min(kmax, max(0.0, (d - 12) * k))
    return mix(col, sky, t)


# ------------------------------------------------------------------ post grade (vignette + soft light falloff)
def grade(im, vig=0.10, warm=0.035, seed=0):
    a = np.asarray(im, float)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    # light falls from upper-left: brighten TL slightly, darken BR slightly (very restrained)
    g = 1.0 + warm * (0.5 - (xx / w * 0.45 + yy / h * 0.55)) * 1.6
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    g *= 1.0 - vig * np.clip(r - 0.55, 0, 1) ** 1.6
    a = a * g[..., None]
    # warm lights / cool shadows: tiny split-tone
    lum = a.mean(axis=2, keepdims=True) / 255.0
    a[..., 0] += (lum[..., 0] - 0.5) * 4
    a[..., 2] -= (lum[..., 0] - 0.5) * 5
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'))


# ------------------------------------------------------------------ building pieces (facade plane z = zf, facing -z, i.e. toward a camera at lower z)
def awning(R, x0, x1, zf, y_wall, y_front, proj, c1, c2, stripe=0.62, valance=0.34):
    n = max(2, int(round((x1 - x0) / stripe)))
    xs = np.linspace(x0, x1, n + 1)
    zfront = zf - proj
    # shadow cast on the facade below the awning
    R.shadow([(x0, y_front - 1.15, zf - 0.01), (x1, y_front - 1.15, zf - 0.01), (x1, y_front, zf - 0.01), (x0, y_front, zf - 0.01)], 0.17, 6)
    for i in range(n):
        c = c1 if i % 2 == 0 else c2
        a, b = xs[i], xs[i + 1]
        # sloped top
        R.poly([(a, y_wall, zf), (b, y_wall, zf), (b, y_front + valance, zfront), (a, y_front + valance, zfront)],
               c, (0, 0.6, -0.8))
        # valance (vertical front lip)
        R.poly([(a, y_front + valance, zfront), (b, y_front + valance, zfront), (b, y_front, zfront), (a, y_front, zfront)],
               mix(c, (60, 50, 44), 0.10), (0, 0, -1))
    # underside shade line
    R.line3d((x0, y_front, zfront), (x1, y_front, zfront), mix(c1, (60, 46, 38), 0.45), 0.035)


def window(R, x0, x1, y0, y1, z, glass=None, frame=None, inset=0.07):
    frame = frame or hx('EDE3CF')
    R.zrect(x0, x1, y0, y1, z, frame)
    R.glass([(x0 + inset, y0 + inset, z - 0.01), (x1 - inset, y0 + inset, z - 0.01), (x1 - inset, y1 - inset, z - 0.01), (x0 + inset, y1 - inset, z - 0.01)],
            glass or P['glass'], streak=0.18)
    # soft inner shadow at the top & left reveal (depth)
    R.shadow([(x0 + inset, y1 - inset - 0.16, z - 0.012), (x1 - inset, y1 - inset - 0.16, z - 0.012), (x1 - inset, y1 - inset, z - 0.012), (x0 + inset, y1 - inset, z - 0.012)], 0.14, 3)


def door(R, x0, x1, y1, z, frame=None, glass=None, handle=True):
    frame = frame or P['plinth']
    R.zrect(x0, x1, 0.0, y1, z, frame)
    R.glass([(x0 + 0.13, 0.04, z - 0.012), (x1 - 0.13, 0.04, z - 0.012), (x1 - 0.13, y1 - 0.14, z - 0.012), (x0 + 0.13, y1 - 0.14, z - 0.012)],
            glass or P['door'], streak=0.14)
    if handle:
        R.zrect(x1 - 0.30, x1 - 0.26, 1.0, 1.2, z - 0.02, hx('C8B79B'))


def facade(R, x0, x1, H, zf, wall, depth=9.0, roofc=None, windows=2, win_w=1.35, upper_y=(4.35, 6.0), cornice=True, band=True, d_haze=0.0, left_wall=True, right_wall=False, topline=0.45):
    roofc = roofc or hx('E8E2D2')
    wc = haze(wall, d_haze * 100) if d_haze else wall
    R.box(x0, 0, zf, x1, H, zf + depth, wc, top=roofc, skip=('bottom', 'back') + (() if left_wall else ('left',)) + (() if right_wall else ('right',)))
    if cornice:
        R.box(x0 - 0.12, H - 0.05, zf - 0.34, x1 + 0.12, H + 0.42, zf + 0.2, mix(wc, (245, 240, 228), 0.45), top=hx('EDE6D6'))
    if band:
        R.box(x0, 3.05, zf - 0.10, x1, 3.45, zf, mix(wc, (245, 240, 228), 0.50))
    # upper windows
    if windows:
        span = (x1 - x0)
        for i in range(windows):
            cx = x0 + span * (i + 0.5) / windows
            window(R, cx - win_w / 2, cx + win_w / 2, upper_y[0], min(upper_y[1], H - 0.9), zf - 0.04)


def plinth(R, x0, x1, zf, h=0.55, col=None):
    R.box(x0, 0, zf - 0.10, x1, h, zf, col or P['plinth'])


def shop_ground(R, x0, x1, zf, door_x, door_w=1.1, glass=None, awn=None, door_frame=None, awn_y=(3.0, 2.25), plinth_col=None, sign=None):
    """ground floor: plinth, big glass, door, awning. awn=(c1,c2)."""
    plinth(R, x0, x1, zf, col=plinth_col)
    # glass between pilasters, leaving the door gap
    pil = 0.28
    gl = [(x0 + pil, door_x - door_w / 2 - 0.12), (door_x + door_w / 2 + 0.12, x1 - pil)]
    for a, b in gl:
        if b - a > 0.5:
            window(R, a, b, 0.55, 2.15, zf - 0.05, glass=glass, inset=0.06)
    door(R, door_x - door_w / 2, door_x + door_w / 2, 2.18, zf - 0.05, frame=door_frame)
    if awn:
        awning(R, x0 + 0.1, x1 - 0.1, zf, awn_y[0], awn_y[1], 0.95, awn[0], awn[1])
    if sign:
        R.box(sign[0], 2.95, zf - 0.16, sign[1], 3.30, zf - 0.04, sign[2])


# ------------------------------------------------------------------ lamps / trees / benches
def lamp(R, x, z, h=4.4, col=None, lit=False):
    col = col or P['slate']
    R.foot_shadow(x, z, 0.5, 0.5, h=h * 0.55, op=0.20, sig=5)
    R.prism(x, z, 0.0, 0.12, 0.17, mix(col, (60, 60, 60), 0.2), n=10, rt=0.15)
    R.prism(x, z, 0.12, h, 0.065, col, n=8)
    R.sphere((x, h + 0.2, z), 0.24, hx('F1E6C0') if not lit else hx('F8E8A8'))


def tree(R, x, z, s=1.0, crown_y=3.0, trunk=hx('8C6B52'), leaf=None, planter=True, hs=1.0):
    leaf = leaf or P['tree']
    if planter:
        R.foot_shadow(x, z, 1.5 * s, 1.5 * s, h=0.5, op=0.25, sig=6)
        R.box(x - 0.6 * s, 0, z - 0.6 * s, x + 0.6 * s, 0.42, z + 0.6 * s, P['plinth'], top=mix(P['plinth'], (120, 100, 70), 0.3))
    R.prism(x, z, 0.4 if planter else 0.0, crown_y + 0.5 * s, 0.13 * s, trunk, n=8, rt=0.10 * s)
    cy = crown_y + 1.15 * s
    for dx, dy, dz, r, c in ((-0.55, -0.15, 0.05, 0.85, mix(leaf, (60, 90, 60), 0.18)), (0.6, -0.05, 0.1, 0.80, mix(leaf, (70, 100, 70), 0.12)),
                             (0.0, 0.40, 0.0, 1.05, leaf), (0.05, 0.05, -0.35, 0.78, mix(leaf, (170, 200, 140), 0.08))):
        R.sphere((x + dx * s, cy + dy * s * hs, z + dz * s), r * s, c)


def clock_post(R, x, z, h=3.9, col=None):
    col = col or hx('6E8C73')
    R.foot_shadow(x, z, 0.6, 0.6, h=h * 0.6, op=0.22, sig=5)
    R.prism(x, z, 0.0, 0.18, 0.22, mix(col, (50, 50, 50), 0.2), n=10, rt=0.2)
    R.prism(x, z, 0.18, h, 0.095, col, n=10)
    cy = h + 0.46
    r = 0.50
    # drum (axis along z): side quads + back cap, then front disc + face + marks
    n = 32
    zb, zf_ = z + 0.10, z - 0.10
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        am = (a0 + a1) / 2
        R.poly([(x + r * math.cos(a0), cy + r * math.sin(a0), zf_), (x + r * math.cos(a1), cy + r * math.sin(a1), zf_),
                (x + r * math.cos(a1), cy + r * math.sin(a1), zb), (x + r * math.cos(a0), cy + r * math.sin(a0), zb)],
               mix(col, (30, 40, 30), 0.12), (math.cos(am), math.sin(am), 0), cull=False)
    R.disc((x, cy, zf_ - 0.002), (0, 0, -1), r, mix(col, (230, 232, 220), 0.10), n=n)
    R.disc((x, cy, zf_ - 0.006), (0, 0, -1), r * 0.88, hx('EEE6D2'), n=n, shade=False)
    for k in range(12):
        a = k * math.pi / 6
        R.disc((x + 0.37 * math.sin(a), cy + 0.37 * math.cos(a), zf_ - 0.01), (0, 0, -1), 0.032 if k % 3 else 0.05, hx('4A5A4E'), n=8, shade=False)
    R.line3d((x, cy, zf_ - 0.012), (x + 0.24, cy + 0.14, zf_ - 0.012), hx('3E4A42'), 0.045)
    R.line3d((x, cy, zf_ - 0.012), (x - 0.05, cy + 0.30, zf_ - 0.012), hx('3E4A42'), 0.04)
    R.disc((x, cy, zf_ - 0.014), (0, 0, -1), 0.04, hx('3E4A42'), n=10, shade=False)


def bench(R, x, z, w=2.6, facing=+1, col=None, leg=None):
    """facing +1 = seat faces +z (back toward a camera at low z)."""
    col = col or hx('B5865A'); leg = leg or P['slate']
    R.foot_shadow(x, z, w, 0.6, h=0.6, op=0.22, sig=5)
    for sx in (-w / 2 + 0.2, w / 2 - 0.2):
        R.box(x + sx - 0.05, 0, z - 0.25, x + sx + 0.05, 0.46, z + 0.25, leg)
    R.box(x - w / 2, 0.44, z - 0.26, x + w / 2, 0.50, z + 0.26, col, top=mix(col, (255, 230, 190), 0.14))
    zb = z - 0.26 * facing
    R.box(x - w / 2, 0.62, zb - 0.03, x + w / 2, 1.02, zb + 0.03, col, top=mix(col, (255, 230, 190), 0.1))


def bunting(R, a, b, y, z, cols, sag=0.35, n=14, flag=0.30):
    a, b = np.array(a, float), np.array(b, float)
    pts = []
    for i in range(n + 1):
        t = i / n
        p = a + (b - a) * t
        p[1] = y - sag * 4 * t * (1 - t)
        pts.append(p)
    for i in range(n):
        R.line3d(pts[i], pts[i + 1], hx('4A4850'), 0.012)
    for i in range(n):
        p = (pts[i] + pts[i + 1]) / 2
        c = cols[i % len(cols)]
        w = flag * 0.5
        R.poly([(p[0] - w, p[1], p[2]), (p[0] + w, p[1], p[2]), (p[0], p[1] - flag, p[2])], c, (0, 0, -1), cull=False)


def bin_(R, x, z, col=None):
    col = col or P['dsage']
    R.foot_shadow(x, z, 0.6, 0.6, h=0.8, op=0.22, sig=4)
    R.prism(x, z, 0.0, 0.85, 0.28, col, n=12, rt=0.26)
    R.prism(x, z, 0.85, 0.92, 0.30, mix(col, (230, 230, 220), 0.25), n=12)


def planter(R, x, z, w=0.7, h=0.5, plants=True, cols=None):
    cols = cols or (hx('8AAE80'), hx('6F9A6E'))
    R.foot_shadow(x, z, w, w, h=0.5, op=0.22, sig=4)
    R.box(x - w / 2, 0, z - w / 2, x + w / 2, h, z + w / 2, hx('B8805C'), top=hx('7A5B44'))
    if plants:
        R.sphere((x - 0.12 * w, h + 0.25, z), 0.27 * w / 0.7, cols[0])
        R.sphere((x + 0.18 * w, h + 0.20, z + 0.05), 0.22 * w / 0.7, cols[1])


def crate(R, x, z, w=0.5, h=0.32, produce=None, col=None):
    col = col or hx('B28659')
    R.foot_shadow(x, z, w, w * 0.8, h=0.3, op=0.2, sig=3)
    R.box(x - w / 2, 0, z - w * 0.4, x + w / 2, h, z + w * 0.4, col, top=mix(col, (80, 60, 40), 0.3))
    if produce:
        for k, c in enumerate(produce):
            R.sphere((x - w * 0.3 + k * w * 0.3, h + 0.07, z), 0.095, c)


def bicycle(R, x, z, flip=False):
    """simple bike seen side-on, in the x-y plane at depth z"""
    s = -1 if flip else 1
    col = hx('5E6A72')
    R.foot_shadow(x, z, 1.5, 0.3, h=0.3, op=0.18, sig=3)
    for wx in (-0.55, 0.55):
        # wheel ring: 14 tiny quads
        for k in range(18):
            a0, a1 = 2 * math.pi * k / 18, 2 * math.pi * (k + 1) / 18
            R.line3d((x + s * wx + 0.34 * math.cos(a0), 0.34 + 0.34 * math.sin(a0), z), (x + s * wx + 0.34 * math.cos(a1), 0.34 + 0.34 * math.sin(a1), z), hx('44454C'), 0.045)
    pts = [(-0.55, 0.34), (-0.12, 0.34), (0.14, 0.78), (-0.30, 0.78), (0.55, 0.34), (0.38, 0.92)]
    P_ = lambda i: (x + s * pts[i][0], pts[i][1], z)
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (2, 5)):
        R.line3d(P_(a), P_(b), col, 0.05)
    R.line3d((x + s * 0.30, 0.95, z), (x + s * 0.46, 0.95, z), hx('2F3036'), 0.05)
    R.line3d((x - s * 0.40, 0.82, z), (x - s * 0.22, 0.82, z), hx('7A5B44'), 0.07)


# ------------------------------------------------------------------ oriented box (yaw about +y) -----------------------------------
def obox(R, cx, cz, y0, y1, hw, hd, ang, col, top=None, front=None, skip=(), alpha=1.0):
    """box centred at (cx,cz), half sizes hw (local x) hd (local z), rotated by `ang` degrees about y.
    local +z is the 'front' of the object (seat front, drawer front...)."""
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)

    def W(lx, lz):
        return (cx + lx * ca + lz * sa, cz - lx * sa + lz * ca)

    def N(nx, nz):
        return (nx * ca + nz * sa, 0.0, -nx * sa + nz * ca)
    c = [(-hw, -hd), (hw, -hd), (hw, hd), (-hw, hd)]
    sides = [(0, 1, (0, -1), 'back'), (1, 2, (1, 0), 'right'), (2, 3, (0, 1), 'front'), (3, 0, (-1, 0), 'left')]
    for i, j, nl, nm in sides:
        if nm in skip:
            continue
        (x0, z0), (x1, z1) = W(*c[i]), W(*c[j])
        colr = front if (nm == 'front' and front) else col
        R.poly([(x0, y0, z0), (x1, y0, z1), (x1, y1, z1), (x0, y1, z0)], colr, N(*nl), alpha=alpha)
    if 'top' not in skip:
        R.poly([(W(*p)[0], y1, W(*p)[1]) for p in c], top or col, (0, 1, 0), alpha=alpha)


def chair(R, x, z, ang, wood=None, dark=None):
    """café chair; ang = facing direction (degrees, 0 faces +z)."""
    wood = wood or hx('B98A5E'); dark = dark or hx('8A6448')
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    W = lambda lx, lz: (x + lx * ca + lz * sa, z - lx * sa + lz * ca)
    R.foot_shadow(x, z, 0.55, 0.55, h=0.7, op=0.20, sig=5)
    for lx, lz in ((-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)):
        px, pz = W(lx, lz)
        h = 0.93 if lz < 0 else 0.46
        obox(R, px, pz, 0.0, 0.46 if lz > 0 else 0.46, 0.022, 0.022, ang, dark)
    obox(R, x, z, 0.44, 0.50, 0.215, 0.215, ang, wood, top=mix(wood, (255, 235, 200), 0.16))
    bx, bz = W(0, -0.19)
    for lx in (-0.18, 0.18):
        px, pz = W(lx, -0.19)
        obox(R, px, pz, 0.50, 0.92, 0.022, 0.022, ang, dark)
    obox(R, bx, bz, 0.60, 0.70, 0.19, 0.016, ang, dark)
    obox(R, bx, bz, 0.78, 0.90, 0.19, 0.016, ang, wood, top=mix(wood, (255, 235, 200), 0.14))


def round_table(R, x, z, r=0.44, top_col=None, h=0.76, base=None):
    top_col = top_col or hx('F0E2C2'); base = base or hx('8A6448')
    R.foot_shadow(x, z, 1.0, 1.0, h=0.8, op=0.22, sig=6)
    R.prism(x, z, 0.0, 0.03, 0.26, base, n=18)
    R.prism(x, z, 0.03, h - 0.04, 0.045, base, n=10)
    R.prism(x, z, h - 0.045, h, r, mix(top_col, (190, 160, 120), 0.35), n=28, top=False)
    R.prism(x, z, h - 0.04, h, r, top_col, n=28, y_cap_col=mix(top_col, (255, 248, 230), 0.20))
