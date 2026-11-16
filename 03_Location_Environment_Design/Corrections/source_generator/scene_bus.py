"""Neighbourhood bus (D-series). Interior: x +-1.2, z 0 (rear) .. 9.4 (windscreen), ceiling 2.3, aisle 1.06 m.
Exterior (D3): bus parked at the curb beside a bus shelter."""
import math
import numpy as np
from engine import Renderer, P, hx, mix, jit
import kit
from kit import *

SAGE = hx('9BB094'); DSAGE = hx('6F8F76'); CREAM = hx('EDE5D0')
AISLE = 0.53
HALFW = 1.2
CEIL = 2.3
ZW = 9.4          # windscreen plane
YOUT = -0.85      # road level seen outside (floor is 0.85 m above the road)


def cam_d1():
    return dict(pos=(0.0, 1.5, 0.35), yaw=0.0, pitch=0.0, hfov=70.0)


def cam_d2():
    return dict(pos=(0.12, 1.50, 5.2), yaw=-12.0, pitch=-3.0, hfov=66.0)


def cam_d4():
    return dict(pos=(0.0, 1.55, 0.35), yaw=0.0, pitch=0.0, hfov=70.0)


# --------------------------------------------------------------------------------------------- outside world seen through glass
def outside(R):
    R.sky(hx('BFD9E2'), hx('F2E8D0'), R.h / 2 / R.ss)
    # road + sidewalks
    R.yrect(-3.2, 3.2, ZW - 3, 120, YOUT, hx('958D80'), shade=False, cull=False)
    for xs in (-1, 1):
        R.yrect(xs * 3.2, xs * 6.0, ZW - 3, 120, YOUT + 0.12, hx('D9CDB4'), shade=False, cull=False)
        R.yrect(xs * 3.1, xs * 3.2, ZW - 3, 120, YOUT + 0.06, hx('E4DAC4'), shade=False, cull=False)
    for z in np.arange(ZW + 1, 100, 5.0):
        R.yrect(-0.06, 0.06, z, z + 2.4, YOUT + 0.004, hx('EDE5D2'), shade=False, cull=False)
    # long rows of hazy buildings, trees and lamps along both sides
    rng = np.random.RandomState(21)
    for xs in (-1, 1):
        z = -12
        while z < 110:
            d = rng.uniform(5, 9); h = rng.uniform(5.5, 9.5)
            c = mix([hx('DCC9A3'), hx('E3D2B0'), hx('D2BE96'), hx('E1CCA4')][rng.randint(4)], (205, 216, 214), min(0.5, 0.06 + max(0, z) / 140))
            x0, x1 = (6.2, 6.2 + 7.0) if xs > 0 else (-13.2, -6.2)
            R.box(x0, YOUT, z, x1, h + YOUT, z + d, c, top=mix(c, (240, 236, 224), 0.4), skip=('bottom', 'back'))
            xf = 6.2 if xs > 0 else -6.2
            nx = (-1, 0, 0) if xs > 0 else (1, 0, 0)
            for wz in np.arange(z + 0.9, z + d - 1.2, 2.3):
                for wy in (1.9, 4.6):
                    if wy + 1.3 < h:
                        R.xrect(wz, wz + 1.0, wy, wy + 1.3, xf - 0.02 * xs, mix(c, (170, 195, 195), 0.5), n=nx, shade=False, cull=False)
            z += d + rng.uniform(0, 0.4)
        for z in np.arange(-3, 100, 15.0):
            R.sphere((xs * 5.2, 2.5 + YOUT, z), 0.95, mix(P['tree'], (205, 216, 214), min(0.55, 0.28 + z / 150)))
            R.line3d((xs * 5.2, YOUT + 0.12, z), (xs * 5.2, 1.7 + YOUT, z), mix(hx('8C6B52'), (205, 216, 214), 0.35), 0.12)
        for z in np.arange(3, 100, 22.0):
            R.line3d((xs * 3.6, YOUT + 0.12, z), (xs * 3.6, 3.6 + YOUT, z), mix(hx('7B8892'), (205, 216, 214), 0.3), 0.09)
            R.sphere((xs * 3.6, 3.75 + YOUT, z), 0.16, hx('F1E6C0'))


# --------------------------------------------------------------------------------------------- interior
def shell(R):
    # floor: aisle runner + darker seat zones; soft window-light patches
    R.yrect(-HALFW, HALFW, -1, ZW, 0.0, hx('B4A892'), shade=False, cull=False)
    R.yrect(-AISLE, AISLE, -1, ZW, 0.002, hx('A99D87'), shade=False, cull=False)
    for z in np.arange(0.4, ZW, 0.9):          # anti-slip strips
        R.yrect(-AISLE + 0.06, AISLE - 0.06, z, z + 0.05, 0.004, hx('B9AE98'), shade=False, cull=False)
    for xs in (-1, 1):
        R.yrect(xs * (AISLE - 0.04), xs * AISLE, -1, ZW, 0.005, hx('D8C98E'), shade=False, cull=False)   # safety edge line
    for z in np.arange(0.9, ZW - 1, 2.4):
        R.shadow([(-0.35, 0.006, z), (0.45, 0.006, z + 0.5), (0.45, 0.006, z + 1.3), (-0.35, 0.006, z + 0.8)], 0.15, 9, tint=(255, 246, 222))
    # ceiling + warm light strips + side cove panels
    R.yrect(-HALFW, HALFW, -1, ZW, CEIL, hx('EDE6D2'), n=(0, -1, 0), shade=False, cull=False)
    for xs in (-1, 1):
        R.yrect(xs * 0.50, xs * 0.72, -1, ZW, CEIL - 0.003, hx('FFF5DA'), n=(0, -1, 0), shade=False, cull=False)
        R.poly([(xs * 0.92, CEIL, -1), (xs * 0.92, CEIL, ZW), (xs * HALFW, 2.02, ZW), (xs * HALFW, 2.02, -1)], hx('E6DEC8') if xs > 0 else hx('D9D2BF'), (-xs * 0.7, -0.7, 0), shade=False, cull=False)
    # side walls: lower panel, window band with pillars, upper return
    for xs in (-1, 1):
        wc = hx('E1D8C0') if xs > 0 else hx('C9C4B6')
        nx = (-xs, 0, 0)
        x = xs * HALFW
        R.xrect(-1, ZW, 0.0, 0.84, x, mix(wc, (150, 120, 96), 0.18), n=nx, shade=False, cull=False)
        R.xrect(-1, ZW, 0.84, 0.90, x, mix(wc, (255, 250, 238), 0.25), n=nx, shade=False, cull=False)
        # glass (light outside) + frames
        R.xrect(-1, ZW, 0.90, 2.02, x - xs * 0.01, hx('DDEBE8'), n=nx, shade=False, cull=False, alpha=0.30)
        for z in np.arange(-0.6, ZW, 1.1):
            R.xrect(z, z + 0.10, 0.84, 2.04, x - xs * 0.02, mix(wc, (245, 238, 218), 0.4), n=nx, shade=False, cull=False)
        # faint reflection streaks on the glass
        for z in np.arange(0.2, ZW - 1, 2.2):
            R.poly([(x - xs * 0.02, 1.0, z), (x - xs * 0.02, 1.0, z + 0.22), (x - xs * 0.02, 1.9, z + 0.62), (x - xs * 0.02, 1.9, z + 0.40)], (255, 255, 255), nx, shade=False, cull=False, alpha=0.10)
        R.xrect(-1, ZW, 0.0, 0.05, x - xs * 0.02, mix(wc, (80, 70, 60), 0.35), n=nx, shade=False, cull=False)
    # rear bulkhead is behind the camera. Front: windscreen frame (glass is the 'outside' showing through)
    R.zrect(-HALFW, HALFW, 0.0, 0.95, ZW, hx('B5A98F'), shade=False)               # cab front panel under the dash
    R.zrect(-HALFW, HALFW, 2.15, CEIL, ZW, hx('E4DCC6'), shade=False)               # header
    for xp in (-HALFW, -0.02, HALFW - 0.10):
        R.zrect(xp, xp + 0.10, 0.95, 2.15, ZW - 0.01, hx('E3D9BF'), shade=False)    # screen pillars
    # destination display (dark glass + one teal bar; no text)
    R.box(-0.55, 2.04, ZW - 0.10, 0.55, 2.28, ZW - 0.02, hx('3E4A4C'))
    R.zrect(-0.40, 0.15, 2.14, 2.18, ZW - 0.104, hx('7FB6B2'), shade=False)


def seats(R, n=6, z0=1.05, pitch=0.86, zmin=-99, zmax=99):
    rng = np.random.RandomState(4)
    for k in range(n):
        z = z0 + k * pitch
        if not (zmin <= z < zmax):
            continue
        for xs in (-1, 1):
            a, b = (xs * AISLE, xs * (HALFW - 0.03)) if xs > 0 else (xs * (HALFW - 0.03), xs * AISLE)
            col = jit(SAGE, rng, 3)
            # floor shadow
            R.shadow([(a, 0, z + 0.05), (b, 0, z + 0.05), (b, 0, z + 0.5), (a, 0, z + 0.5)], 0.22, 5)
            # riser under cushion
            R.box(a + 0.04, 0.0, z + 0.14, b - 0.04, 0.46, z + 0.50, hx('8E9A88'))
            # cushion
            R.box(a, 0.44, z + 0.10, b, 0.52, z + 0.54, mix(col, (255, 255, 240), 0.10), top=mix(col, (255, 255, 240), 0.18))
            # backrest with a quiet headrest inset and darker cap
            R.box(a, 0.50, z, b, 1.13, z + 0.12, col, top=mix(col, (70, 90, 70), 0.12), front=col)
            R.zrect(a + 0.07, b - 0.07, 0.86, 1.02, z - 0.004, mix(col, (255, 255, 240), 0.08))
            R.zrect(a + 0.04, b - 0.04, 0.55, 0.60, z - 0.004, mix(col, (60, 80, 60), 0.10))
            R.line3d(((a + b) / 2, 0.52, z - 0.006), ((a + b) / 2, 1.10, z - 0.006), mix(col, (60, 80, 60), 0.22), 0.012)   # seam between the two seats
            R.line3d((a, 1.12, z - 0.004), (b, 1.12, z - 0.004), mix(col, (70, 90, 70), 0.25), 0.012)


def rails(R, z0=0.4, z1=8.7, poles=(1.9,)):
    col = DSAGE
    for xs in (-1, 1):
        R.tube((xs * 0.66, 2.0, z0), (xs * 0.66, 2.0, z1), 0.022, col, n=10, caps=True)
        for zz in poles:                       # vertical poles at seat-block ends (aisle side)
            R.tube((xs * 0.58, 0.02, zz), (xs * 0.58, 2.0, zz), 0.024, col, n=10)
            R.tube((xs * 0.58, 2.0, zz), (xs * 0.66, 2.0, zz), 0.02, col, n=8)
        # hanging grab loops
        for zz in (2.9, 5.0, 7.1):
            R.tube((xs * 0.66, 2.0, zz), (xs * 0.66, 1.78, zz), 0.012, hx('4A4850'), n=6)
            R.disc((xs * 0.66, 1.72, zz), (1, 0, 0), 0.05, hx('7B8892'), n=14)


def cab(R, driver_x=-0.66, show_dash=True):
    # driver's seat: base, cushion, tall backrest with headrest, armrest - clearly a driver's chair
    sx, sz = driver_x, 8.10
    R.foot_shadow(sx, sz, 0.6, 0.6, h=0.9, op=0.25, sig=4)
    R.box(sx - 0.18, 0.0, sz - 0.14, sx + 0.18, 0.34, sz + 0.18, hx('4E555C'))                       # pedestal
    R.box(sx - 0.25, 0.34, sz - 0.20, sx + 0.25, 0.46, sz + 0.30, hx('6A737B'), top=hx('7F8991'))     # cushion
    R.box(sx - 0.24, 0.46, sz - 0.26, sx + 0.24, 1.22, sz - 0.15, hx('68727A'), top=hx('7F8991'))     # backrest
    R.box(sx - 0.15, 1.22, sz - 0.25, sx + 0.15, 1.50, sz - 0.16, hx('5E6870'), top=hx('7F8991'))     # headrest
    R.box(sx + 0.25, 0.62, sz - 0.18, sx + 0.31, 0.68, sz + 0.20, hx('4E555C'))                       # armrest
    # dashboard: ONE assembly (sand pad on a slate base) with a binnacle, centre stack and a small switch strip
    if show_dash:
        R.box(-HALFW, 0.60, 8.78, HALFW, 0.80, ZW, hx('B6AA92'), top=hx('C9BE9F'), front=hx('A99D86'))      # full-width lower panel
        R.box(-1.16, 0.80, 8.78, -0.30, 0.98, ZW, hx('B0A48B'), top=hx('C4B99A'), front=hx('A39780'))     # raised driver pod
        R.box(-0.96, 0.98, 8.98, -0.36, 1.16, 9.22, hx('3E3C44'))                           # instrument binnacle
        R.poly([(-0.94, 1.12, 9.16), (-0.38, 1.12, 9.16), (-0.38, 1.02, 9.0), (-0.94, 1.02, 9.0)], hx('4A4E58'), (0, 0.6, -0.8), shade=False, cull=False)
        R.poly([(-0.88, 1.10, 9.14), (-0.62, 1.10, 9.14), (-0.62, 1.04, 9.03), (-0.88, 1.04, 9.03)], hx('7FB6B2'), (0, 0.6, -0.8), shade=False, cull=False)
        R.disc((-0.52, 1.05, 9.0), (0, 0.6, -0.8), 0.045, hx('D9D2C0'), n=14, shade=False)
        R.box(-0.14, 0.80, 8.95, 0.44, 0.90, 9.22, hx('4A4E58'))                            # centre switch strip
        for i in range(4):
            R.disc((-0.08 + i * 0.12, 0.905, 9.0), (0, 1, 0), 0.026, (hx('C9D2CC'), hx('D9B25F'), hx('C9D2CC'), hx('C4473B'))[i], n=10, shade=False)
    # steering wheel: tilted ring + 3 spokes + hub + column to the dash (proportioned to a 0.40 m rim)
    c = np.array([driver_x, 1.00, 8.62]); rr = 0.20
    n_ = np.array([0.0, 0.55, -0.83]); n_ /= np.linalg.norm(n_)
    u = np.array([1.0, 0.0, 0.0]); v = np.cross(n_, u)
    col = hx('34363C')
    R.tube(c + np.array([0, -0.02, 0.04]), np.array([driver_x, 0.80, 8.84]), 0.03, hx('4A4E58'), n=10)       # column
    pts = [c + rr * (math.cos(2 * math.pi * i / 30) * u + math.sin(2 * math.pi * i / 30) * v) for i in range(31)]
    for i in range(30):
        R.tube(pts[i], pts[i + 1], 0.018, col, n=6, caps=False)
    for ang in (90, 210, 330):
        a = math.radians(ang)
        R.tube(c, c + rr * (math.cos(a) * u + math.sin(a) * v), 0.012, col, n=6)
    R.disc(c + n_ * 0.015, n_, 0.055, hx('4A4E58'), n=14)
    # ticket validator on a pole at the right of the entrance
    R.tube((1.02, 0.0, 8.5), (1.02, 1.15, 8.5), 0.025, DSAGE, n=10)
    R.box(0.92, 1.15, 8.42, 1.12, 1.40, 8.56, hx('7B8892'))
    R.zrect(0.95, 1.09, 1.28, 1.36, 8.415, hx('7FB6B2'), shade=False)


def interior(R, plan=None, driver=True, behind=None, split_z=None):
    outside(R)
    shell(R)
    cab(R)
    if behind is None:
        seats(R)
    else:                                   # characters stand in the aisle: seats nearer than them must draw after them
        seats(R, zmin=split_z)
        behind(R)
        seats(R, zmax=split_z)
    rails(R)


# --------------------------------------------------------------------------------------------- exterior (D3)
def bus_body(R, x0=-1.2, x1=7.2, z0=1.3, z1=3.7):
    h = 3.05
    door = (x1 - 1.95, x1 - 0.85)
    zf = z0 - 0.02
    R.foot_shadow((x0 + x1) / 2, (z0 + z1) / 2 + 0.3, x1 - x0 + 0.4, z1 - z0 + 0.5, h=1.0, op=0.28, sig=10)
    R.box(x0, 0.38, z0, x1, 1.00, z1, hx('66846F'), top=hx('7A9884'), right=hx('5E7A68'), skip=('bottom',))
    R.box(x0, 1.00, z0 - 0.005, x1, 1.26, z1, hx('D5956C'), top=hx('D5956C'), right=hx('BE805A'), skip=('bottom',))
    R.box(x0, 1.26, z0 - 0.01, x1, 2.62, z1, hx('E7DFC8'), top=hx('EDE5D0'), right=hx('D6CDB4'), skip=('bottom',))
    R.box(x0 - 0.02, 2.62, z0 - 0.03, x1 + 0.02, h, z1, hx('EDE5D0'), top=hx('F4EEDC'), right=hx('DDD4BC'), skip=('bottom',))
    # side windows between pillars, then the double door, then a small front window
    wx = x0 + 0.30
    pill = 1.35
    n = int((door[0] - 0.12 - wx) / pill)
    for k in range(n):
        a = wx + k * pill
        R.glass([(a, 1.42, zf - 0.01), (a + pill - 0.14, 1.42, zf - 0.01), (a + pill - 0.14, 2.50, zf - 0.01), (a, 2.50, zf - 0.01)], hx('9DB5B6'), streak=0.16)
    R.zrect(door[0], door[1], 0.40, 2.56, zf - 0.01, hx('6F8F76'))
    mid = (door[0] + door[1]) / 2
    for a, b in ((door[0] + 0.07, mid - 0.025), (mid + 0.025, door[1] - 0.07)):
        R.glass([(a, 0.52, zf - 0.02), (b, 0.52, zf - 0.02), (b, 2.48, zf - 0.02), (a, 2.48, zf - 0.02)], hx('A9C4C2'), streak=0.14)
    R.glass([(door[1] + 0.12, 1.42, zf - 0.01), (x1 - 0.12, 1.42, zf - 0.01), (x1 - 0.12, 2.50, zf - 0.01), (door[1] + 0.12, 2.50, zf - 0.01)], hx('9DB5B6'), streak=0.0)
    # route display above the front window (dark, one teal bar, no text)
    R.box(door[1] + 0.16, 2.70, zf - 0.04, x1 - 0.16, 2.92, zf - 0.005, hx('3E4A4C'))
    R.zrect(door[1] + 0.22, door[1] + 0.42, 2.79, 2.84, zf - 0.045, hx('7FB6B2'), shade=False)
    # wheels: dark arch + tyre + pale hub (rear axle behind the pillars, front axle before the door)
    for wxc in (x0 + 1.55, door[0] - 0.95):
        R.disc((wxc, 0.52, zf - 0.03), (0, 0, -1), 0.60, hx('3F4B45'), n=30, shade=False)
        R.disc((wxc, 0.46, zf - 0.07), (0, 0, -1), 0.46, hx('3A383F'), n=30)
        R.disc((wxc, 0.46, zf - 0.075), (0, 0, -1), 0.19, hx('A5ADB0'), n=22, shade=False)
        R.disc((wxc, 0.46, zf - 0.078), (0, 0, -1), 0.07, hx('6E767A'), n=12, shade=False)
    # mirror on a short arm at the front corner (clear of the door)
    return door


def build_d3(R):
    R.sky(hx('BDD8E2'), hx('F3E8CE'), R.h / 2 / R.ss)
    for (x0, x1, H, c) in ((-26, -10, 7.2, hx('D9C7A4')), (-10, 4, 9.0, hx('E3D2B0')), (4, 15, 6.8, hx('D0BB93')), (15, 30, 7.6, hx('DCC9A4'))):
        facade(R, x0, x1, H, 11.0, haze(c, 18), windows=3 if x1 - x0 > 11 else 2, win_w=1.3, left_wall=False)
    shop_ground(R, -10, 4, 11.0, -3.0, awn=(hx('CB9873'), hx('F0E4CB')), door_frame=hx('7E5A45'))
    shop_ground(R, 4, 15, 11.0, 10.0, awn=(hx('7B8892'), hx('E8DDC4')), door_frame=hx('7E5A45'))
    shop_ground(R, -26, -10, 11.0, -17.0, awn=(hx('A8BD9F'), hx('F0E4CB')), door_frame=hx('8A6A52'))
    shop_ground(R, 15, 30, 11.0, 22.0, awn=(hx('C48E68'), hx('EFE2C6')), door_frame=hx('7E5A45'))
    pave = hx('D6CAB2')
    R.yrect(-80, 80, 8.0, 60, 0.0, hx('938B7F'), shade=False, cull=False)
    R.yrect(-80, 80, 8.0, 11.0, 0.12, hx('D9CDB5'), shade=False, cull=False)
    R.yrect(-80, 80, -40, 0.2, 0.12, pave, shade=False, cull=False)
    R.yrect(-80, 80, 0.2, 0.4, 0.121, hx('E3D9C4'), shade=False, cull=False)
    R.poly([(-80, 0, 0.2), (80, 0, 0.2), (80, 0.12, 0.2), (-80, 0.12, 0.2)], mix(pave, (120, 110, 100), 0.2), (0, 0, -1), shade=False)
    R.yrect(-80, 80, 8.0, 8.1, 0.003, hx('EAE2CE'), shade=False, cull=False)
    for x in np.arange(-80, 80, 1.5):
        R.line3d((x, 0.125, -40), (x, 0.125, 0.0), mix(pave, (130, 118, 98), 0.10), 0.02)
    for z in np.arange(-30, 0.1, 1.5):
        R.line3d((-80, 0.125, z), (80, 0.125, z), mix(pave, (130, 118, 98), 0.10), 0.02)
    lamp(R, -17.0, 9.8, 4.4); lamp(R, 12.6, 9.8, 4.4)
    return bus_body(R)


def shelter_stop(R, x0=-5.0, x1=-2.2, z0=-3.6, z1=-2.7):
    ds = P['dsage']; slate = P['slate']
    R.foot_shadow((x0 + x1) / 2, (z0 + z1) / 2 + 0.2, x1 - x0, z1 - z0, h=2.4, op=0.20, sig=8)
    bench(R, (x0 + x1) / 2, (z0 + z1) / 2 + 0.05, w=(x1 - x0) - 0.55)
    for x in (x0 + 0.07, x1 - 0.07):
        for z in (z0 + 0.07, z1 - 0.07):
            R.box(x - 0.055, 0.0, z - 0.055, x + 0.055, 2.42, z + 0.055, slate)
    R.poly([(x0 + 0.13, 0.55, z0 + 0.03), (x1 - 0.13, 0.55, z0 + 0.03), (x1 - 0.13, 2.15, z0 + 0.03), (x0 + 0.13, 2.15, z0 + 0.03)], hx('CFE0DC'), (0, 0, -1), shade=False, alpha=0.20, cull=False)
    R.xrect(z0, z1, 0.55, 2.15, x0 + 0.05, hx('CFE0DC'), shade=False, alpha=0.30, cull=False)
    R.box(x0 - 0.18, 2.40, z0 - 0.20, x1 + 0.18, 2.52, z1 + 0.20, ds, top=mix(ds, (230, 240, 225), 0.20))
    R.box(x0 + 0.3, 1.02, z0 + 0.02, x1 - 0.3, 1.10, z0 + 0.10, hx('E8E0CC'))


def stop_sign_(R, x, z, h=2.75):
    R.foot_shadow(x, z, 0.3, 0.3, h=h * 0.4, op=0.16, sig=4)
    R.prism(x, z, 0, h, 0.045, P['slate'], n=8)
    R.disc((x, h + 0.30, z - 0.06), (0, 0, -1), 0.30, hx('9CB398'), n=30)
    R.disc((x, h + 0.30, z - 0.07), (0, 0, -1), 0.20, hx('EDE4CD'), n=30, shade=False)


def items_d3(R, sign_x=-1.55, planter_x=3.0, shelter=True):
    items = []
    if shelter:
        items.append((-3.6, -3.2, lambda: shelter_stop(R)))
    if sign_x is not None:
        items.append((sign_x, -2.4, lambda: stop_sign_(R, sign_x, -2.4)))
    c = np.array([R.pos[0], R.pos[2]])
    items.sort(key=lambda t: -((t[0] - c[0]) ** 2 + (t[1] - c[1]) ** 2))
    for _, _, fn in items:
        fn()


def cam_d3():
    return dict(pos=(0.0, 1.65, -13.0), yaw=0.0, pitch=1.5, hfov=62.0)


def render(which, cam=None, behind=None, **kw):
    cam = cam or {'d1': cam_d1, 'd2': cam_d2, 'd3': cam_d3, 'd4': cam_d4}[which]()
    R = Renderer(pos=cam['pos'], yaw=cam['yaw'], pitch=cam['pitch'], hfov=cam['hfov'], ss=2)
    if which == 'd3':
        build_d3(R); items_d3(R, **{k: v for k, v in kw.items() if k != 'split_z'})
    else:
        interior(R, behind=behind, split_z=kw.get('split_z'))
    return R


if __name__ == '__main__':
    SP = '/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    for k in ('d1', 'd2', 'd3'):
        R = render(k); kit.grade(R.finish(), vig=0.08).save(SP + k + '_test.png')
