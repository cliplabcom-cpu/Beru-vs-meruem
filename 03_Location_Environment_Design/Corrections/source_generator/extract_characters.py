"""Cut the APPROVED character art out of the approved reference sheets (nothing is redrawn).
Sheets (repo root): Group_Comparison_Sheet.png -> front views of Sam/Asha/Emeka (ground row 1330);
Emeka_Model_Sheet.png, Sam_Model_Sheet (1).png, Asha_Model_Sheet_Stall_Apron.png -> front/side/back (ground row ~1340).
Method: colour-distance key against the flat sheet background, guide-line removal, shadow removal near the feet,
per-shoe convex hull (needed because Sam's white sneakers are almost the same colour as the sheet background).
Output: chars/*.png (RGBA) + chars.json {name: {h, w, foot_x}} in sheet pixels (1 character unit = 1 px, Emeka = 1000)."""
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.abspath(os.path.join(HERE, '..', '_work', 'chars'))
os.makedirs(OUT, exist_ok=True)
BG = np.array([244, 242, 238])

def load(path):
    return np.array(Image.open(os.path.join(ROOT, path)).convert('RGB')).astype(int)

def ground_row(diff):
    rows = [y for y in range(900, diff.shape[0]) if (diff[y, 60:260] > 25).mean() > 0.9]
    return float(np.mean(rows)) if rows else None

def figure_components(diff):
    er = ndi.binary_erosion(diff > 40, structure=np.ones((3, 3)), iterations=4)
    lab, n = ndi.label(er)
    sizes = ndi.sum(er, lab, range(1, n + 1))
    comps = []
    for i, s in enumerate(sizes):
        if s > 20000:  # whole figures only (skips label text, shadow blobs, shoes-only blobs)
            ys, xs = np.where(lab == i + 1)
            comps.append((xs.min(), xs.max(), ys.min(), ys.max()))
    return sorted(comps)

def extract(im, box, ground, name, bar_color=None, white_shoes=False):
    x0, x1 = box
    d = np.abs(im - BG).sum(axis=2)
    gy = int(round(ground))
    sub = im[:gy + 2, x0:x1]; dd = d[:gy + 2, x0:x1]
    raw = dd > 22
    er = ndi.binary_erosion(dd > 40, structure=np.ones((3, 3)), iterations=4)
    lab, n = ndi.label(er)
    sizes = ndi.sum(er, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 3000])
    M = ndi.binary_dilation(keep, structure=np.ones((3, 3)), iterations=6) & raw
    M = ndi.binary_closing(M, structure=np.ones((3, 3)), iterations=3)
    # fill interior holes (white shirt, eye whites...) only in the upper body; legs stay open between them
    hip = gy - 430
    Mf = ndi.binary_fill_holes(M)
    M = np.where(np.arange(M.shape[0])[:, None] < hip, Mf, M)
    lab, n = ndi.label(M)
    if n > 1:
        M = lab == (1 + int(np.argmax(ndi.sum(M, lab, range(1, n + 1)))))
    M[gy:, :] = False
    # ---- feet: drop shadow, rebuild each shoe as a hull
    band0 = gy - 95
    val = sub.max(axis=2)
    dark = M & (val < 150); dark[:band0] = False
    # split left/right leg at the gap seen well above the feet
    row = M[gy - 200]
    xs_ = np.where(row)[0]; xg = None
    if len(xs_):
        runs = np.split(xs_, np.where(np.diff(xs_) > 1)[0] + 1)
        if len(runs) >= 2:
            gaps = [(runs[i + 1][0] - runs[i][-1], (runs[i + 1][0] + runs[i][-1]) / 2) for i in range(len(runs) - 1)]
            xg = max(gaps)[1]
    groups = [dark] if xg is None else [dark & (np.arange(M.shape[1])[None, :] < xg), dark & (np.arange(M.shape[1])[None, :] >= xg)]
    bar = np.zeros_like(M)
    if bar_color is not None:
        rr = slice(gy - 9, gy - 7)
        bar[rr] = (np.abs(sub[rr] - np.array(bar_color)).sum(axis=2) < 12)
        bl_, bn_ = ndi.label(bar)
        if bn_:
            bar = bl_ == (1 + int(np.argmax(ndi.sum(bar, bl_, range(1, bn_ + 1)))))
    bar_xs = np.where(bar.any(axis=0))[0]
    bxl, bxr = (bar_xs.min(), bar_xs.max()) if len(bar_xs) else (None, None)
    depth = 9 if white_shoes else 48
    foot = np.zeros(M.shape, np.uint8)
    for k, g_ in enumerate(groups):
        ys, xs = np.where(g_)
        if len(ys) < 50: continue
        low = ys > ys.max() - depth
        pts = list(zip(xs[low], ys[low]))
        xl, xr = xs.min(), xs.max()
        if bxl is not None:
            lo = bxl if (xg is None or k == 0) else xg
            hi = bxr if (xg is None or k == len(groups) - 1) else xg
            xl, xr = min(xl, lo), max(xr, hi)
        pts += [(xl, gy - 1), (xr, gy - 1)]
        if white_shoes:  # sneaker sides bulge: add intermediate points measured from the zoomed shoe outline
            outer_l = (xg is None or k == 0); outer_r = (xg is None or k == len(groups) - 1)
            pts += [(xl + 4, gy - 18), (xl + 12, gy - 41)] if outer_l else [(xl, gy - 18), (xl, gy - 43)]
            pts += [(xr - 4, gy - 18), (xr - 12, gy - 41)] if outer_r else [(xr, gy - 18), (xr, gy - 43)]
        cv2.fillConvexPoly(foot, cv2.convexHull(np.array(pts, np.int32)), 1)
    F = foot.astype(bool)
    keepband = (M & (val < 150)) | F
    M2 = M.copy(); M2[band0:] = keepband[band0:]
    # ---- soft alpha + colour decontamination at the edge
    inner = ndi.binary_erosion(M2, structure=np.ones((3, 3)), iterations=2)
    idx = ndi.distance_transform_edt(~inner, return_distances=False, return_indices=True)
    rgb = sub.astype(np.uint8)[idx[0], idx[1]]
    rgb[inner] = sub.astype(np.uint8)[inner]
    alpha = ndi.gaussian_filter(M2.astype(float), 0.8)
    alpha = np.clip((alpha - 0.2) / 0.6, 0, 1)
    ys, xs = np.where(alpha > 0.5)
    t, b, l, r = ys.min(), ys.max(), xs.min(), xs.max()
    rgba = np.dstack([rgb, (alpha * 255).astype(np.uint8)])[t:b + 1, l:r + 1]
    Image.fromarray(rgba, 'RGBA').save(os.path.join(OUT, name + '.png'))
    return {'h': int(gy - t), 'w': int(r - l + 1), 'ground_off': int(gy - b)}

if __name__ == '__main__':
    meta = {}
    g = load('Group_Comparison_Sheet.png')
    gg = ground_row(np.abs(g - BG).sum(axis=2))
    for nm, (a, b), bc in [('sam_front', (400, 800), (214, 214, 208)), ('asha_front', (1130, 1560), None), ('emeka_front', (1700, 2200), None)]:
        # group-sheet view boxes in original px (sam 359-747, asha 985-1424, emeka 1566-2113)
        pass
    boxes = {'sam_front': (330, 780, (214, 214, 208)), 'asha_front': (960, 1450, None), 'emeka_front': (1540, 2140, None)}
    for nm, (a, b, bc) in boxes.items():
        meta[nm] = extract(g, (a, b), gg, nm, bc, white_shoes=(nm.startswith('sam')))
    for f, who, bc in [('Emeka_Model_Sheet.png', 'emeka', None), ('Sam_Model_Sheet (1).png', 'sam', (214, 214, 208)), ('Asha_Model_Sheet_Stall_Apron.png', 'asha_apron', None)]:
        im = load(f); d = np.abs(im - BG).sum(axis=2); gy = ground_row(d)
        comps = figure_components(d)
        print(f, 'ground', gy, 'comps', comps)
        for view, c in zip(['front', 'side', 'back'], comps):
            nm = f'{who}_{view}'
            if nm in ('sam_front', 'emeka_front'):
                nm += '_sheet'  # keep the group-sheet fronts as primary
            meta[nm] = extract(im, (max(c[0] - 45, 0), c[1] + 45), gy, nm, bc, white_shoes=(who == 'sam'))
    json.dump(meta, open(os.path.join(OUT, 'chars.json'), 'w'), indent=1)
    print(json.dumps(meta, indent=1))
