"""Market Lane world (C-series). Stalls stand with their counter front on z = 0, customers on z < 0."""
import math
import numpy as np
from engine import Renderer, P, hx, mix, jit
import kit
from kit import *

WALL_Z = 10.0
PAVE = hx('D8CCB4')
POST = hx('7E5C44')
WOODC = hx('B5885B')
BOARD = hx('56605F')


def cam_c1():
    return dict(pos=(0.0, 1.45, -5.6), yaw=0.0, pitch=1.0, hfov=60.0)


def cam_c2():
    return dict(pos=(0.0, 1.6, -12.8), yaw=0.0, pitch=4.5, hfov=66.0)


# ------------------------------------------------------------------------------------------------- products
def breads(R, x, y, z, n=4, seed=0, w=0.6):
    rng = np.random.RandomState(seed)
    R.prism(x, z, y, y + 0.025, w / 2, hx('F1ECDD'), n=16)
    cols = (hx('C8864F'), hx('D9B46A'), hx('B9763F'), hx('E2C48A'))
    for k in range(n):
        px = x - w * 0.32 + k * w * 0.64 / max(1, n - 1)
        R.sphere((px, y + 0.10, z + rng.uniform(-0.04, 0.04)), 0.075, cols[(k + seed) % 4], squash=0.8)


def fruit_crate(R, x, y, z, seed=0, w=0.55, cols=None):
    cols = cols or (hx('C95B45'), hx('D9A04A'), hx('8DAA6B'))
    R.box(x - w / 2, y, z - 0.18, x + w / 2, y + 0.12, z + 0.18, hx('A97C52'), top=hx('7A5B44'))
    rng = np.random.RandomState(seed)
    for k in range(5):
        R.sphere((x - w * 0.36 + k * w * 0.18, y + 0.18, z + rng.uniform(-0.08, 0.08)), 0.065, cols[(k + seed) % len(cols)])


def jars(R, x, y, z, n=2, lid=None, body=None):
    lid = lid or hx('6F9A7C'); body = body or hx('C9D9CF')
    for k in range(n):
        R.prism(x + k * 0.17, z, y, y + 0.2, 0.065, body if k % 2 == 0 else hx('EDE3CD'), n=12)
        R.prism(x + k * 0.17, z, y + 0.2, y + 0.24, 0.07, lid, n=12)


def fabric_rolls(R, x, y, z, cols):
    for k, c in enumerate(cols):
        R.prism(x + k * 0.17, z, y, y + 0.55, 0.075, c, n=12)


def pot_plants(R, x, y, z, n=3):
    for k in range(n):
        px = x + k * 0.22
        R.prism(px, z, y, y + 0.13, 0.07, hx('C7946C'), n=10, rt=0.09)
        R.sphere((px, y + 0.24, z), 0.13, (hx('7FA382'), hx('668F6B'), hx('93B28A'))[k % 3])


def basket(R, x, y, z, cols):
    R.prism(x, z, y, y + 0.22, 0.20, hx('B8956A'), n=14, rt=0.24)
    for k, c in enumerate(cols):
        R.sphere((x - 0.12 + k * 0.12, y + 0.26, z + (0.03 if k % 2 else -0.03)), 0.075, c)


# ------------------------------------------------------------------------------------------------- stall
def stall(R, x, z=0.0, w=3.0, awn=(hx('9CB398'), hx('E9DDC2')), stripe=0.55, kind='bread', asha=False, seed=1,
          aw_front=2.15, aw_back=2.5, depth=1.2, extras=True, board='chalk', back=None, behind=None):
    """counter front at z; the stall extends back to z+depth. x = centre."""
    x0, x1 = x - w / 2, x + w / 2
    zb = z + depth
    # ground shadow of the whole stall
    R.foot_shadow(x + 0.2, z + depth / 2 + 0.2, w, depth + 0.6, h=2.4, op=0.20, sig=10)
    # back panel (planked, dark) with side returns
    R.planks((x0 + 0.05, 0.0, zb), (x1 - 0.05, 0.0, zb), (x1 - 0.05, 2.30, zb), (x0 + 0.05, 2.30, zb), 12, back or POST, amt=5, n_vec=(0, 0, -1), seam=False)
    R.xrect(z + 0.05, zb, 0, 2.3, x0 + 0.05, mix(POST, (60, 40, 30), 0.1), n=(1, 0, 0))
    R.xrect(z + 0.05, zb, 0, 2.3, x1 - 0.05, mix(POST, (60, 40, 30), 0.1), n=(-1, 0, 0), cull=False)
    for px in (x0 + 0.04, x1 - 0.04):
        R.box(px - 0.04, 0.0, zb - 0.06, px + 0.04, aw_back, zb, POST)
    # soft occlusion inside the booth
    R.shadow([(x0 + 0.1, 1.0, zb - 0.02), (x1 - 0.1, 1.0, zb - 0.02), (x1 - 0.1, 2.3, zb - 0.02), (x0 + 0.1, 2.3, zb - 0.02)], 0.10, 14, tint=(40, 28, 20))
    # chalkboard + shelves are ABOVE head height of the stallholder (1.63 m) so a face never sits on a prop
    bx0, bx1 = x - 0.75, x + 0.35
    if board == 'chalk':
        R.box(bx0 - 0.04, 1.80, zb - 0.05, bx1 + 0.04, 2.24, zb - 0.01, hx('8A6A52'))
        R.zrect(bx0, bx1, 1.84, 2.20, zb - 0.055, BOARD, shade=False)
        for k, (a_, b_) in enumerate(((0.1, 0.9), (0.1, 0.65), (0.1, 0.9))):
            R.zrect(bx0 + a_ * (bx1 - bx0) * 0.95, bx0 + b_ * (bx1 - bx0) * 0.95, 2.09 - k * 0.11, 2.13 - k * 0.11, zb - 0.06, hx('E7DFCB'), shade=False)
    elif board == 'banner':           # painted cloth banner, abstract mark only
        R.zrect(bx0 + 0.1, bx1 - 0.1, 1.82, 2.22, zb - 0.05, mix(awn[0], (255, 255, 255), 0.1), shade=False)
        R.disc(((bx0 + bx1) / 2, 2.02, zb - 0.056), (0, 0, -1), 0.12, hx('EEE3CC'), n=20, shade=False)
    elif board == 'rail':             # hanging goods on a rail
        R.line3d((x0 + 0.2, 2.1, zb - 0.25), (x1 - 0.2, 2.1, zb - 0.25), hx('4A4850'), 0.025)
        for k in range(6):
            hxk = x0 + 0.45 + k * (w - 0.9) / 5
            R.poly([(hxk - 0.1, 2.1, zb - 0.25), (hxk + 0.1, 2.1, zb - 0.25), (hxk + 0.08, 1.72, zb - 0.25), (hxk - 0.08, 1.72, zb - 0.25)], (hx('C9826A'), hx('8FA9AE'), hx('E3C98A'), hx('A3B99D'))[k % 4], (0, 0, -1), cull=False)
    for sx0, sx1 in (() if board == 'rail' else ((x0 + 0.12, x - 0.82), (x + 0.45, x1 - 0.12))):
        R.box(sx0, 1.78, zb - 0.30, sx1, 1.82, zb - 0.01, hx('A9825F'), top=hx('BC946D'))
    if board != 'rail':
        jars(R, x + 0.55, 1.82, zb - 0.16, n=2)
        R.prism(x0 + 0.40, zb - 0.16, 1.82, 2.02, 0.07, hx('F1ECDD'), n=10)
        R.prism(x0 + 0.62, zb - 0.16, 1.82, 2.0, 0.07, hx('C7946C'), n=10)
    if behind:
        behind(R)
    # --- counter ---
    R.box(x0, 0.0, z + 0.02, x1, 0.10, z + 0.80, hx('6E4F3A'))
    R.planks((x0, 0.10, z), (x1, 0.10, z), (x1, 0.95, z), (x0, 0.95, z), max(4, int(w / 0.45)), hx('B5885B'), amt=6)
    R.box(x1 - 0.02, 0.0, z, x1, 0.95, z + 0.8, hx('A57B52'))
    R.box(x0, 0.95, z - 0.06, x1, 1.0, z + 0.85, hx('D9C297'), top=hx('E1CCA2'), front=hx('BFA477'))
    # display step with products (left of the stallholder's gap) - varied by stall kind
    R.box(x0 + 0.15, 1.0, z + 0.40, x0 + 1.55, 1.10, z + 0.74, hx('8F6B4F'), top=hx('A47E60'))
    items = {
        'bread': lambda: [breads(R, x0 + 0.45 + 0.46 * k, 1.10, z + 0.52, n=3, seed=seed + k, w=0.4) if k != 1 else fruit_crate(R, x0 + 0.91, 1.10, z + 0.55, seed=seed, w=0.42, cols=(hx('D9A04A'), hx('8DAA6B'), hx('C95B45'))) for k in range(3)],
        'fruit': lambda: [fruit_crate(R, x0 + 0.45 + 0.50 * k, 1.10, z + 0.55, seed=seed + k) for k in range(3)],
        'goods': lambda: fabric_rolls(R, x0 + 0.30, 1.10, z + 0.55, [hx('C9826A'), hx('8FA9AE'), hx('E3C98A'), hx('A3B99D'), hx('B36E58'), hx('E8DDC4')]),
        'plants': lambda: [pot_plants(R, x0 + 0.30 + 0.62 * k, 1.10, z + 0.55, n=2) for k in range(2)],
        'jars': lambda: [jars(R, x0 + 0.30 + 0.5 * k, 1.10, z + 0.55, n=2, lid=hx('C7946C')) for k in range(3)],
    }
    items[kind]()
    # right of the gap: jars + notebook (Asha's recurring red notebook only on her stall)
    if asha:
        jars(R, x1 - 0.55, 1.0, z + 0.45, n=2)
        obox(R, x + 0.10, z + 0.34, 1.0, 1.03, 0.10, 0.14, -10, hx('C4473B'), top=hx('D45A4C'))
    else:
        basket(R, x1 - 0.45, 1.0, z + 0.45, [hx('C98A58'), hx('D9B46A'), hx('9FB48E')])
    # card terminal at the far left end of the counter (customer side)
    tx = x0 + 0.22
    R.box(tx - 0.12, 1.0, z + 0.22, tx + 0.12, 1.03, z + 0.40, hx('7A868A'), top=hx('93A0A4'))
    R.box(tx - 0.025, 1.03, z + 0.28, tx + 0.025, 1.22, z + 0.34, hx('7A868A'))
    R.poly([(tx - 0.13, 1.20, z + 0.33), (tx + 0.13, 1.20, z + 0.33), (tx + 0.13, 1.38, z + 0.27), (tx - 0.13, 1.38, z + 0.27)], hx('3E3C44'), (0, 0.4, -1), shade=False, cull=False)
    # --- posts (front) ---
    for px in (x0 + 0.04, x1 - 0.04):
        R.box(px - 0.04, 0.0, z - 0.02, px + 0.04, aw_front + 0.02, z + 0.06, POST, left=mix(POST, (90, 70, 55), 0.15))
    # --- awning: striped top slope, front lip and a darker underside so it reads from below as well ---
    n = max(3, int(round(w / stripe)))
    xs = np.linspace(x0 - 0.1, x1 + 0.1, n + 1)
    zf = z - 0.38
    cs = [awn[0] if i % 2 == 0 else awn[1] for i in range(n)]
    for i in range(n):          # underside (only seen from below, kept light so it never turns muddy)
        a_, b_ = xs[i], xs[i + 1]
        R.poly([(a_, aw_front, zf), (b_, aw_front, zf), (b_, aw_back, zb), (a_, aw_back, zb)], mix(cs[i], (96, 82, 70), 0.30), (0, -1, 0), shade=False, cull=False)
    for i in range(n):          # sloped top
        a_, b_ = xs[i], xs[i + 1]
        R.poly([(a_, aw_front + 0.28, zf), (b_, aw_front + 0.28, zf), (b_, aw_back + 0.02, zb), (a_, aw_back + 0.02, zb)], cs[i], (0, 0.8, -0.6), cull=False)
    for i in range(n):          # front lip - the clear striped band that reads from the front
        a_, b_ = xs[i], xs[i + 1]
        R.poly([(a_, aw_front, zf), (b_, aw_front, zf), (b_, aw_front + 0.28, zf), (a_, aw_front + 0.28, zf)], cs[i], (0, 0, -1), cull=False)
    R.line3d((xs[0], aw_front, zf), (xs[-1], aw_front, zf), mix(awn[0], (50, 40, 34), 0.45), 0.03)
    R.line3d((xs[0], aw_front + 0.28, zf), (xs[-1], aw_front + 0.28, zf), mix(awn[0], (50, 40, 34), 0.25), 0.02)
    R.shadow([(x0, 1.9, z - 0.01), (x1, 1.9, z - 0.01), (x1, aw_front, z - 0.01), (x0, aw_front, z - 0.01)], 0.0, 3)
    if asha:
        # her stall's quiet identity: a round sage blade sign on the right outer post (never in front of the stallholder) + small pot
        sx = x1 + 0.28
        R.line3d((x1 + 0.04, 2.02, z - 0.03), (sx, 2.02, z - 0.03), hx('4A4850'), 0.02)
        R.line3d((sx, 2.02, z - 0.03), (sx, 1.90, z - 0.03), hx('4A4850'), 0.012)
        R.disc((sx, 1.66, z - 0.04), (0, 0, -1), 0.24, hx('9CB398'), n=30)
        R.disc((sx, 1.66, z - 0.045), (0, 0, -1), 0.185, hx('EEE3CC'), n=30, shade=False)
        R.sphere((sx - 0.04, 1.66, z - 0.06), 0.065, hx('C8864F'), squash=0.8)
        R.sphere((sx + 0.07, 1.69, z - 0.06), 0.04, hx('6F9A7C'))
        pot_plants(R, x0 - 0.30, 0.0, z - 0.25, n=1)
    elif extras:
        pass


# ------------------------------------------------------------------------------------------------- world
def ground(R, extent=40):
    R.yrect(-extent, extent, -40, 60, 0.0, PAVE, shade=False, cull=False)
    jc = mix(PAVE, (130, 118, 98), 0.12)
    for z in np.arange(-30, 20, 1.5):
        R.line3d((-extent, 0.003, z), (extent, 0.003, z), jc, 0.02)
    for x in np.arange(-extent, extent, 1.5):
        R.line3d((x, 0.003, -30), (x, 0.003, 20), jc, 0.02)


def backdrop(R, y10=False, wall_z=WALL_Z):
    R.sky(hx('BDD8E2'), hx('F3E8CE'), R.h / 2 / R.ss)
    # distant roofline (hazy)
    rng = np.random.RandomState(9)
    x = -90
    while x < 90:
        w = rng.uniform(6, 12); h = rng.uniform(15, 26)
        c = mix(hx('D9D2BE'), (200, 214, 214), rng.uniform(0.35, 0.55))
        R.box(x, 0, wall_z + 30, x + w, h, wall_z + 40, c, top=mix(c, (240, 236, 224), 0.4), skip=('bottom', 'back'))
        x += w + rng.uniform(0, 0.8)
    # lane buildings
    wallc = hx('DCC9A3')
    facade(R, -60, 60, 8.0, wall_z, mix(wallc, (210, 214, 208), 0.08), depth=6, windows=0, upper_y=(4.6, 6.4), left_wall=False)
    for wx in np.arange(-58, 58, 3.4):
        window(R, wx, wx + 1.3, 4.5, 6.2, wall_z - 0.04)
    # ground floor of the lane wall: quiet shopfronts (plinth, glass, door) so the far wall has depth and a use
    for wx in np.arange(-60, 60, 7.0):
        shop_ground(R, wx, wx + 7.0, wall_z, wx + 5.6, door_w=1.0, awn=None, door_frame=hx('8A6A52'))


def wall_bunting(R, x0, x1, y, z, sag=0.5, n=16):
    cols = [hx('CB9873'), hx('A3B99D'), hx('F0E4CB')]
    bunting(R, (x0, y, z), (x1, y, z), y, z, cols, sag=sag, n=n, flag=0.28)


def lamp_post(R, x, z, h=4.0):
    lamp(R, x, z, h)


def build_c1(R, y10=False, behind=None):
    backdrop(R)
    ground(R)
    # neighbours first (far -> near), softly hazy so the hero stall separates from them
    stall(R, -8.2, 2.6, 3.0, awn=(hx('B77B5A'), hx('E6D8BC')), kind='fruit', seed=3, board='banner')
    stall(R, 8.0, 2.2, 3.2, awn=(hx('7B8892'), hx('E6D8BC')), kind='goods', seed=5, board='rail')
    # light haze over the neighbours (atmospheric depth)
    # trees + lamps in the background
    tree(R, 6.6, 7.0, 0.85, crown_y=2.6, planter=False)
    lamp(R, -3.6, 4.4, 4.0)
    wall_bunting(R, -7.5, 7.5, 3.9, WALL_Z - 0.6, sag=0.7, n=18)
    # hero stall
    stall(R, 0.0, 0.0, 3.0, asha=True, kind='bread', seed=2, behind=behind)


def build_row(R, y10=False):
    backdrop(R)
    ground(R)
    # background: trees behind, lamps, a single bunting line along the wall
    tree(R, -9.5, 6.0, 1.15, crown_y=2.8, planter=False)
    tree(R, 9.8, 6.0, 1.2, crown_y=2.8, planter=False)
    lamp(R, -5.6, 4.0, 4.2); lamp(R, 5.6, 4.0, 4.2)
    wall_bunting(R, -14, 14, 4.2, WALL_Z - 0.6, sag=0.9, n=30)
    # stalls: independent traders, deliberately different widths / awnings / goods / heights
    spec = [
        (-11.4, 3.2, (hx('B77B5A'), hx('E6D8BC')), 0.60, 'fruit', 2.12, 2.45, 'banner', hx('6E5440')),
        (-7.6, 2.8, (hx('7B8892'), hx('E6D8BC')), 0.45, 'goods', 2.20, 2.55, 'rail', hx('8A6E58')),
        (-3.8, 3.0, (hx('C9B58A'), hx('E6D8BC')), 0.70, 'jars', 2.15, 2.50, 'chalk', hx('7E5C44')),
        (3.8, 3.4, (hx('5E8B76'), hx('E6D8BC')), 0.40, 'plants', 2.18, 2.45, 'banner', hx('6E5440')),
        (7.8, 2.9, (hx('C98A6A'), hx('E1D3B6')), 0.55, 'fruit', 2.12, 2.52, 'chalk', hx('76604C')),
        (11.8, 3.0, (hx('8EA4B0'), hx('E6D8BC')), 0.60, 'bread', 2.15, 2.48, 'rail', hx('7E5C44')),
    ]
    for i, (sx, sw, aw, st, kd, af, ab, bd, bk) in enumerate(spec):
        stall(R, sx, 0.0, sw, awn=aw, stripe=st, kind=kd, seed=i + 2, aw_front=af, aw_back=ab, board=bd, back=bk)
    stall(R, 0.0, 0.0, 3.0, asha=True, kind='bread', seed=2)       # Asha's stall (centre), sage + cream, hanging sign, planter
    # modest foreground life that does not block the stalls' fronts
    crate(R, -6.0, -1.3, produce=[hx('C95B45'), hx('D9A04A')]); crate(R, 6.2, -1.3, produce=[hx('8DAA6B')] * 2)
    bin_(R, 9.9, -1.6)
    bench(R, -1.6, -6.1, w=1.6, facing=+1)
    planter(R, 2.7, -4.6, 0.55, 0.42)
    # hand cart parked low in the left foreground (clear of every counter front)
    R.foot_shadow(-7.0, -6.2, 1.4, 0.9, h=0.8, op=0.2, sig=4)
    R.box(-7.6, 0.35, -6.5, -6.4, 0.70, -5.9, hx('A97C52'), top=hx('C29A6E'))
    for wx in (-7.4, -6.6):
        R.prism(wx, -6.5, 0.0, 0.05, 0.30, hx('4A4850'), n=14)
    R.line3d((-6.4, 0.7, -6.2), (-5.7, 0.95, -6.2), hx('4A4850'), 0.05)
    # paving inlay strips + manhole: quiet scale cues for the foreground
    for zz in (-7.5, -10.0):
        R.yrect(-30, 30, zz, zz + 0.30, 0.004, mix(PAVE, (240, 232, 212), 0.45), shade=False, cull=False)
    R.disc((3.6, 0.005, -7.8), (0, 1, 0), 0.38, mix(PAVE, (110, 100, 90), 0.28), n=24, shade=False)


def render(which='c1', cam=None, **kw):
    cam = cam or (cam_c1() if which == 'c1' else cam_c2())
    R = Renderer(pos=cam['pos'], yaw=cam['yaw'], pitch=cam['pitch'], hfov=cam['hfov'], ss=2)
    (build_c1 if which == 'c1' else build_row)(R, **kw)
    return R


if __name__ == '__main__':
    SP = '/tmp/claude-0/-home-claude/5dc6b3af-27dc-55b2-bf5f-19d08198bb85/scratchpad/'
    R = render('c1'); kit.grade(R.finish()).save(SP + 'c1_test.png')
    R = render('row'); kit.grade(R.finish()).save(SP + 'c2_test.png')
