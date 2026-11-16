"""Builds every Module-03 v2 environment reference (landscape 16:9) and the dedicated 9:16 compositions.
Run:  python3 build_all.py [landscape|portrait|all] [name ...]     Output: ../  (the Corrections folder)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
from engine import Renderer
import kit, chars
import scene_street as ss, scene_cafe as sc, scene_market as sm, scene_bus as sb
import a4_street, b3_cafe, c3_market, d4_bus

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
VOUT = os.path.join(OUT, 'vertical_9x16')
os.makedirs(VOUT, exist_ok=True)


def save(R, path, vig=0.08):
    kit.grade(R.finish(), vig=vig).save(path)


# ----------------------------------------------------------------------------- landscape (1920x1080)
def L_A1(p): save(ss.render_street(1), p, 0.10)
def L_A2(p): save(ss.render_street(1, 'along', cam=ss.cam_along()), p, 0.10)
def L_A3(p): save(ss.render_street(10), p, 0.10)
def L_A4(p): a4_street.a4(p)
def L_B1(p): save(sc.render(), p)
def L_B2(p): save(sc.render(sc.cam_b2(), plan=sc.plan_b3(), pendants=()), p)
def L_B3(p): b3_cafe.b3(p)
def L_C1(p): save(sm.render('c1'), p, 0.10)
def L_C2(p): save(sm.render('row'), p, 0.10)
def L_C3(p): c3_market.c3(p)
def L_D1(p): save(sb.render('d1'), p)
def L_D2(p): save(sb.render('d2'), p)
def L_D3(p): save(sb.render('d3'), p)
def L_D4(p): d4_bus.d4(p)

LAND = {
    'A1_street_main_day1_v2': L_A1, 'A2_street_along_sidewalk_v2': L_A2, 'A3_street_main_year10_v2': L_A3,
    'A4_street_character_placement_v2': L_A4, 'B1_cafe_main_corner_v2': L_B1, 'B2_cafe_counter_hero_v2': L_B2,
    'B3_cafe_character_placement_v2': L_B3, 'C1_market_stall_main_v2': L_C1, 'C2_market_row_month6_v2': L_C2,
    'C3_market_character_placement_v2': L_C3, 'D1_bus_interior_main_v2': L_D1, 'D2_bus_driver_cabin_v2': L_D2,
    'D3_bus_stop_exterior_v2': L_D3, 'D4_bus_character_placement_v2': L_D4,
}

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    only = sys.argv[2:]
    if mode in ('landscape', 'all'):
        for k, fn in LAND.items():
            if only and not any(k.startswith(o) for o in only): continue
            fn(os.path.join(OUT, k + '.png')); print('wrote', k, flush=True)


# ----------------------------------------------------------------------------- portrait (1080x1920): deliberately re-framed, NOT centre crops
# Rendered on a 1080x2300 canvas and cropped with a vertical lens-shift so the subject sits in the upper ~75 % and the bottom
# ~22 % stays calm for subtitles / platform UI.
PW, PH, PCH = 1080, 1920, 2300


def pcrop(R, path, top, vig=0.10):
    im = kit.grade(R.finish(), vig=vig)
    im.crop((0, top, PW, top + PH)).save(path)


def cm(pos, yaw, pitch, hfov): return dict(pos=pos, yaw=yaw, pitch=pitch, hfov=hfov)


# name: (builder(cam)->R, camera, crop_top)
def P_A1(c): return ss.render_street(1, 'main', cam=c)
def P_A2(c): return ss.render_street(1, 'along', cam=c)
def P_A3(c): return ss.render_street(10, 'main', cam=c)
def P_A4(c): return a4_street.a4(None, c, clock_x=0.8)
def P_B1(c): return sc.render(c)
def P_B2(c): return sc.render(c, plan=sc.plan_b3(), pendants=())
def P_B3(c): return b3_cafe.b3(None, c)
def P_C1(c): return sm.render('c1', cam=c)
def P_C2(c): return sm.render('row', cam=c)
def P_C3(c): return c3_market.c3(None, c)
def P_D1(c): return sb.render('d1', cam=c)
def P_D2(c): return sb.render('d2', cam=c)
def P_D3(c): return sb.render('d3', cam=c, shelter=False, sign_x=None)
def P_D4(c): return d4_bus.d4(None, cam=c)

PORT = {
    'A1_street_main_day1_9x16': (P_A1, cm((-2.4, 2.3, -15), 3.5, 1.0, 31), 370),
    'A2_street_along_sidewalk_9x16': (P_A2, cm((-21, 1.75, 4.5), 86, 0.0, 40), 370),
    'A3_street_main_year10_9x16': (P_A3, cm((-2.4, 2.3, -15), 3.5, 1.0, 31), 370),
    'A4_street_character_placement_9x16': (P_A4, cm((-2.55, 1.7, -12.5), 0, 0.5, 50), 370),
    'B1_cafe_main_corner_9x16': (P_B1, cm((2.95, 1.65, 0.5), -33, 0.5, 44), 370),
    'B2_cafe_counter_hero_9x16': (P_B2, cm((-0.55, 1.50, 1.2), 0, 1.5, 38), 370),
    'B3_cafe_character_placement_9x16': (P_B3, cm((-0.2, 1.6, 0.6), -15, 1.0, 58), 370),
    'C1_market_stall_main_9x16': (P_C1, cm((0.0, 1.45, -5.6), 0, 0.0, 36), 370),
    'C2_market_row_month6_9x16': (P_C2, cm((0.0, 1.6, -12.8), 0, 3.0, 32), 370),
    'C3_market_character_placement_9x16': (P_C3, cm((0.0, 1.5, -6.6), 0, 0.0, 58), 370),
    'D1_bus_interior_main_9x16': (P_D1, cm((0.0, 1.5, 0.35), 0, 0.0, 48), 300),
    'D2_bus_driver_cabin_9x16': (P_D2, cm((0.12, 1.50, 5.2), -12, -3.0, 54), 300),
    'D3_bus_stop_exterior_9x16': (P_D3, cm((3.6, 1.65, -13.0), 0, 1.5, 42), 370),
    'D4_bus_character_placement_9x16': (P_D4, cm((0.0, 1.55, 0.35), 0, 0.0, 46), 370),
}


def run_portrait(only):
    engine.Renderer.DEF_W, engine.Renderer.DEF_H = PW, PCH
    for k, (fn, cam, top) in PORT.items():
        if only and not any(k.startswith(o) for o in only): continue
        pcrop(fn(cam), os.path.join(VOUT, k + '.png'), top); print('wrote', k, flush=True)


if __name__ == '__main__' and mode in ('portrait', 'all'):
    run_portrait(only)
