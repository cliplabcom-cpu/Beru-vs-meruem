"""Contact sheets (landscape + 9:16) and the updated scale reference chart, built from the real v2 files + approved cutouts."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
V = os.path.join(OUT, 'vertical_9x16'); CH = os.path.join(OUT, '_work', 'chars')
FP = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def F(sz, b=False):
    try: return ImageFont.truetype(FB if b else FP, sz)
    except Exception: return ImageFont.load_default()
BG = (244, 238, 224); INK = (62, 60, 68)
NAMES = ['A1_street_main_day1', 'A2_street_along_sidewalk', 'A3_street_main_year10', 'A4_street_character_placement',
         'B1_cafe_main_corner', 'B2_cafe_counter_hero', 'B3_cafe_character_placement',
         'C1_market_stall_main', 'C2_market_row_month6', 'C3_market_character_placement',
         'D1_bus_interior_main', 'D2_bus_driver_cabin', 'D3_bus_stop_exterior', 'D4_bus_character_placement']


def contact():
    cols, tw, th, pad, top = 3, 640, 360, 24, 120
    rows = -(-len(NAMES) // cols)
    W = cols * (tw + pad) + pad; H = top + rows * (th + 56) + pad
    sh = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sh)
    d.text((pad, 28), 'Module 03 - Environment Contact Sheet (v2 corrected references, 16:9)', font=F(34, True), fill=INK)
    d.text((pad, 78), 'Procedural re-creations of the 14 correctable references. Characters are cut-outs of the approved front/side views.', font=F(20), fill=INK)
    for i, n in enumerate(NAMES):
        r, c = divmod(i, cols); x = pad + c * (tw + pad); y = top + r * (th + 56)
        im = Image.open(os.path.join(OUT, n + '_v2.png')).convert('RGB').resize((tw, th), Image.LANCZOS)
        sh.paste(im, (x, y)); d.text((x, y + th + 8), n + '_v2', font=F(19, True), fill=INK)
    sh.save(os.path.join(OUT, '03_Environment_Contact_Sheet_v2.png'))


def contact_v():
    tw, th, pad, top = 288, 512, 20, 110
    cols = 7; rows = 2
    W = cols * (tw + pad) + pad; H = top + rows * (th + 52) + pad
    sh = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sh)
    d.text((pad, 26), 'Module 03 - 9:16 compositions (re-framed, not centre crops)', font=F(32, True), fill=INK)
    d.text((pad, 72), 'Subjects sit in the upper ~75 %; the bottom ~22 % is kept calm for subtitles / platform UI.', font=F(20), fill=INK)
    for i, n in enumerate(NAMES):
        r, c = divmod(i, cols); x = pad + c * (tw + pad); y = top + r * (th + 52)
        im = Image.open(os.path.join(V, n.split('_')[0] + '_' + '_'.join(n.split('_')[1:]) + '_9x16.png')).convert('RGB').resize((tw, th), Image.LANCZOS)
        sh.paste(im, (x, y)); d.text((x, y + th + 6), n.split('_')[0] + ' ' + '_'.join(n.split('_')[1:3]), font=F(15, True), fill=INK)
    # subtitle-safe overlay legend on first tile
    sh.save(os.path.join(OUT, '03_Vertical_9x16_Composition_Sheet_v2.png'))


def cut(name, h_m, ppm):
    im = Image.open(os.path.join(CH, name + '.png')).convert('RGBA'); bb = im.split()[-1].getbbox(); im = im.crop(bb)
    hh = int(round(h_m * ppm)); ww = int(round(im.width * hh / im.height)); return im.resize((ww, hh), Image.LANCZOS)


def scale_chart():
    ppm = 300; W, H = 4300, 1320; base = 960
    sh = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sh)
    d.text((56, 36), 'Module 03 - Scale Reference Chart v2  |  1 m = 300 px  |  Emeka 100% = 1.85 m  -  Sam 95% = 1.76 m  -  Asha 88% = 1.63 m', font=F(40, True), fill=INK)
    d.text((56, 96), 'Characters are the APPROVED cut-outs (front views) scaled sole-to-top to metres - same pipeline that places them in the v2 scenes.', font=F(26), fill=INK)
    for m in range(0, 6):
        y = base - m * ppm * 0.5
        d.line((40, y, W - 40, y), fill=(222, 214, 196), width=2); d.text((44, y - 30), '%.1f m' % (m * 0.5), font=F(22), fill=(130, 124, 112))
    x = 150
    for nm, hm, lab in (('emeka_front', 1.85, 'Emeka 100% / 1.85 m (incl. cap)'), ('sam_front', 1.76, 'Sam 95% / 1.76 m'), ('asha_front', 1.63, 'Asha 88% / 1.63 m')):
        im = cut(nm, hm, ppm); sh.paste(im, (x, base - im.height), im)
        d.ellipse((x - 10, base - 14, x + im.width + 10, base + 14), outline=(190, 184, 172))
        d.line((x + im.width + 24, base - im.height, x + im.width + 24, base), fill=INK, width=3)
        d.text((x + im.width + 34, base - im.height - 4), lab, font=F(20), fill=INK)
        d.text((x, base + 26), nm.split('_')[0].capitalize(), font=F(30, True), fill=INK); x += im.width + 255
    groups = [('CITY STREET', [('shop door', 2.10), ('bus-stop bench seat', .46), ('shelter roof, clear', 2.45), ('awning valance', 2.25), ('curb', .12)]),
              ("ASHA'S CAFE", [('entrance door', 2.15), ('counter', 1.05), ('table', .76), ('chair seat', .50), ('pendant bottom', 2.10)]),
              ('MARKET STALL', [('counter', 1.00), ('canopy front', 2.15), ('price board', 1.50), ('stool', .62)]),
              ('CITY BUS (interior)', [('ceiling', 2.30), ('handrail', 2.00), ('seat back', 1.13), ('seat cushion', .50), ('door opening', 2.02)])]
    cols = {'CITY STREET': (213, 190, 150), 'ASHA\'S CAFE': (196, 150, 104), 'MARKET STALL': (170, 188, 160), 'CITY BUS (interior)': (160, 184, 160)}
    x = 1720
    for g, items in groups:
        d.text((x, 160), g, font=F(32, True), fill=INK)
        for lab, hm in items:
            hpx = int(hm * ppm); w = 100
            d.rectangle((x, base - hpx, x + w, base), fill=cols[g], outline=INK, width=2)
            t = Image.new('RGBA', (300, 40), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 4), '%s %.2f' % (lab, hm), font=F(20), fill=INK)
            t = t.rotate(-90, expand=True); sh.paste(t, (x + 30, base + 16), t)
            x += w + 22
        x += 44
    d.text((56, H - 44), 'Clearances: bus aisle 1.06 m; Emeka arm-to-arm in the approved front view is ~1.0 m (so the aisle fits ONE character side-on or in single file) | doors 2.02-2.15 m vs tallest 1.85 m | cafe pendant bottom 2.10 m | market valance bottom 1.95 m.', font=F(24), fill=INK)
    sh.save(os.path.join(OUT, '03_Scale_Reference_Chart_v2.png'))


if __name__ == '__main__':
    contact(); contact_v(); scale_chart(); print('ok')


ORIG = {'A1_street_main_day1': 'A1_street_main_day1', 'A2_street_along_sidewalk': 'A2_street_along_sidewalk', 'A3_street_main_year10': 'A3_street_main_year10_same_camera',
        'A4_street_character_placement': 'A4_street_scale_placement_test', 'B1_cafe_main_corner': 'B1_cafe_main_corner', 'B2_cafe_counter_hero': 'B2_cafe_counter_hero',
        'B3_cafe_character_placement': 'B3_cafe_scale_placement_test', 'C1_market_stall_main': 'C1_market_stall_main', 'C2_market_row_month6': 'C2_market_row_month6',
        'C3_market_character_placement': 'C3_market_scale_placement_test', 'D1_bus_interior_main': 'D1_bus_interior_main', 'D2_bus_driver_cabin': 'D2_bus_interior_cab',
        'D3_bus_stop_exterior': 'D3_bus_stop_exterior', 'D4_bus_character_placement': 'D4_bus_scale_placement_test'}


def before_after(root):
    tw, th, pad = 480, 270, 16
    rows = 7; W = 4 * (tw + pad) + pad; H = 100 + rows * (th + 46) + pad
    sh = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sh)
    d.text((pad, 24), 'Module 03 - Before (original a9d8e76) vs After (v2). Left = BEFORE, right = AFTER in each pair.', font=F(26, True), fill=INK)
    for i, n in enumerate(NAMES):
        r, c = divmod(i, 2); x0 = pad + c * 2 * (tw + pad); y = 90 + r * (th + 46)
        a = Image.open(os.path.join(root, ORIG[n] + '.png')).convert('RGB').resize((tw, th), Image.LANCZOS)
        b = Image.open(os.path.join(OUT, n + '_v2.png')).convert('RGB').resize((tw, th), Image.LANCZOS)
        sh.paste(a, (x0, y)); sh.paste(b, (x0 + tw + pad, y))
        d.text((x0, y + th + 6), n.split('_')[0] + ' ' + '_'.join(n.split('_')[1:3]) + '   before | after', font=F(17, True), fill=INK)
    sh.save(os.path.join(OUT, '03_Before_After_Comparison.png'))


if __name__ == '__main__' and len(sys.argv) > 1:
    before_after(sys.argv[1])
