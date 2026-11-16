"""Rich Mentality - Module 03 correction: tiny flat-shaded 2.5D renderer.

WHY THIS EXISTS: the Module 03 generator (source_generator/) was never committed, only its flattened PNGs.
This renderer re-creates the SAME look (flat shaded boxes/prisms/spheres, upper-left-front key light, warm lit /
cool shadow, soft contact shadows) with the SAME camera model recovered from the guide:
  x right, y up, z forward (yaw 0); fov = HORIZONTAL fov; eye height as in the guide.
Check: A1 camera (-2.4, 2.3, -15) fov 66 puts a post at (0.2, -4.2) at screen x=1316 px - exactly the original.
Everything renders at 2x and is downsampled (anti-aliasing). Text is never drawn into scenes.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def jit(c, rng, amt=6):
    d = rng.uniform(-amt, amt)
    return tuple(int(max(0, min(255, v + d))) for v in c)


def _unit(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v) + 1e-12)


# --- palette (guide + values sampled from the approved originals) -------------------------------------------------
P = dict(
    plaster=hx('E3D0AE'), sand=hx('D8C29C'), cream=hx('EEE2CA'), clay=hx('CB9873'), sage=hx('A3B99D'),
    dsage=hx('728F7B'), slate=hx('7B8892'), pave=hx('D6CAB2'), road=hx('938B7F'), glass=hx('C1D0C6'),
    glass2=hx('A9C4C2'), wood=hx('BC8E62'), dwood=hx('85624A'), plinth=hx('805E45'), gold=hx('D9B25F'),
    white=hx('F5F1E8'), ink=hx('3E3C44'), teal=hx('7FB6B2'), grocer=hx('D9C6A2'), cafew=hx('E3D7BC'),
    repair=hx('CEB891'), sidew=hx('DECAA4'), door=hx('A1BAB5'), tree=hx('8EAB7E'), green=hx('6F8A73'),
)


class Renderer:
    LIGHT = _unit((-0.55, 0.78, -0.40))  # camera-relative, toward the light (upper-left-front)

    DEF_W, DEF_H = 1920, 1080

    def __init__(self, W=None, H=None, pos=(0, 1.7, 0), yaw=0.0, pitch=0.0, hfov=66.0, ss=2):
        W = W or Renderer.DEF_W; H = H or Renderer.DEF_H
        self.W, self.H, self.ss = W, H, ss
        self.w, self.h = W * ss, H * ss
        self.pos = np.array(pos, float)
        self.yaw, self.pitch = math.radians(yaw), math.radians(pitch)
        self.f = (self.w / 2) / math.tan(math.radians(hfov) / 2)
        self.im = Image.new('RGB', (self.w, self.h), (225, 225, 225))
        self.d = ImageDraw.Draw(self.im)
        self.near = 0.12
        cy, sy, cp, sp = math.cos(self.yaw), math.sin(self.yaw), math.cos(self.pitch), math.sin(self.pitch)
        self._cy, self._sy, self._cp, self._sp = cy, sy, cp, sp
        # world shadow direction (camera-relative: right + back), on the ground plane
        right = np.array([cy, -sy]); fwd = np.array([sy, cy])
        self.sdir = _unit(0.55 * right + 0.8 * fwd)
        self.rng = np.random.RandomState(7)
        self.boxes = []  # screen-space bounding boxes registered by billboards (QC)

    # ------------------------------------------------------------------ camera
    def rot(self, v):
        v = np.asarray(v, float)
        x = v[..., 0] * self._cy - v[..., 2] * self._sy
        z = v[..., 0] * self._sy + v[..., 2] * self._cy
        y = v[..., 1]
        y2 = y * self._cp - z * self._sp
        z2 = y * self._sp + z * self._cp
        return np.stack([x, y2, z2], axis=-1)

    def cam(self, p):
        return self.rot(np.asarray(p, float) - self.pos)

    def proj1(self, pc):
        return (self.w / 2 + self.f * pc[0] / pc[2], self.h / 2 - self.f * pc[1] / pc[2])

    def to_screen(self, p):
        """world point -> (u, v) at OUTPUT resolution (not supersampled), plus depth."""
        pc = self.cam(p)
        u, v = self.proj1(pc)
        return u / self.ss, v / self.ss, pc[2]

    def ppm(self, p):
        """output pixels per metre at the depth of world point p (frontal)."""
        return self.f / self.cam(p)[2] / self.ss

    def _clip(self, pcs):
        out = []
        n = len(pcs)
        for i in range(n):
            a, b = pcs[i], pcs[(i + 1) % n]
            ina, inb = a[2] > self.near, b[2] > self.near
            if ina:
                out.append(a)
            if ina != inb:
                t = (self.near - a[2]) / (b[2] - a[2])
                out.append(a + (b - a) * t)
        return out

    def screen_poly(self, pts):
        pcs = [self.cam(p) for p in pts]
        pcs = self._clip(pcs)
        if len(pcs) < 3:
            return None
        return [self.proj1(p) for p in pcs]

    # ------------------------------------------------------------------ shading
    def shade(self, col, n):
        nc = self.rot(n)
        dd = float(np.dot(nc, self.LIGHT))
        f = 1.0 + 0.24 * (dd - 0.386)
        c = np.array(col, float) * f
        if f < 1:
            c = c + (1 - f) * np.array([26, 32, 46]) * 0.9
        else:
            c = c + (f - 1) * np.array([14, 8, -4]) * 1.0
        return tuple(int(max(0, min(255, v))) for v in c)

    # ------------------------------------------------------------------ polygons
    def _fill(self, sp, col, alpha=1.0):
        if sp is None:
            return
        if alpha >= 0.999:
            self.d.polygon(sp, fill=col)
            return
        xs = [p[0] for p in sp]; ys = [p[1] for p in sp]
        x0, x1 = int(max(0, min(xs) - 1)), int(min(self.w, max(xs) + 2))
        y0, y1 = int(max(0, min(ys) - 1)), int(min(self.h, max(ys) + 2))
        if x1 <= x0 or y1 <= y0:
            return
        m = Image.new('L', (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).polygon([(p[0] - x0, p[1] - y0) for p in sp], fill=int(255 * alpha))
        self.im.paste(col, (x0, y0), m)

    def poly(self, pts, col, n=(0, 0, -1), shade=True, cull=True, alpha=1.0):
        n = _unit(n)
        if cull and float(np.dot(n, self.pos - np.asarray(pts[0], float))) <= 1e-6:
            return
        c = self.shade(col, n) if shade else col
        self._fill(self.screen_poly(pts), c, alpha)

    def zrect(self, x0, x1, y0, y1, z, col, n=(0, 0, -1), **k):
        self.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], col, n, **k)

    def xrect(self, z0, z1, y0, y1, x, col, n=(-1, 0, 0), **k):
        self.poly([(x, y0, z0), (x, y0, z1), (x, y1, z1), (x, y1, z0)], col, n, **k)

    def yrect(self, x0, x1, z0, z1, y, col, n=(0, 1, 0), **k):
        self.poly([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], col, n, **k)

    def box(self, x0, y0, z0, x1, y1, z1, col, top=None, front=None, back=None, left=None, right=None, skip=(), alpha=1.0):
        fs = {
            'front': ([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, -1), front or col),
            'back': ([(x1, y0, z1), (x0, y0, z1), (x0, y1, z1), (x1, y1, z1)], (0, 0, 1), back or col),
            'left': ([(x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1)], (-1, 0, 0), left or col),
            'right': ([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1, 0, 0), right or col),
            'top': ([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0), top or col),
            'bottom': ([(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)], (0, -1, 0), col),
        }
        for k, (pts, n, c) in fs.items():
            if k in skip:
                continue
            self.poly(pts, c, n, alpha=alpha)

    def prism(self, cx, cz, y0, y1, r, col, n=14, rt=None, rz=None, top=True, y_cap_col=None):
        rt = r if rt is None else rt
        rz = r if rz is None else rz
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            am = (a0 + a1) / 2
            nrm = (math.cos(am) * rz, 0.0, math.sin(am) * r)
            nrm = _unit((math.cos(am) / r, 0, math.sin(am) / rz))
            pts = [(cx + r * math.cos(a0), y0, cz + rz * math.sin(a0)), (cx + r * math.cos(a1), y0, cz + rz * math.sin(a1)),
                   (cx + rt * math.cos(a1), y1, cz + rz * (rt / r) * math.sin(a1)), (cx + rt * math.cos(a0), y1, cz + rz * (rt / r) * math.sin(a0))]
            self.poly(pts, col, nrm)
        if top:
            pts = [(cx + rt * math.cos(2 * math.pi * i / n), y1, cz + rz * (rt / r) * math.sin(2 * math.pi * i / n)) for i in range(n)]
            self.poly(pts, y_cap_col or col, (0, 1, 0))

    def tube(self, p0, p1, r, col, n=10, caps=True):
        p0, p1 = np.array(p0, float), np.array(p1, float)
        a = _unit(p1 - p0)
        t = np.array([0, 1, 0]) if abs(a[1]) < 0.9 else np.array([1, 0, 0])
        u = _unit(np.cross(a, t)); v = np.cross(a, u)
        ring = lambda i: math.cos(2 * math.pi * i / n) * u + math.sin(2 * math.pi * i / n) * v
        for i in range(n):
            r0, r1 = ring(i), ring(i + 1)
            nm = _unit(r0 + r1)
            self.poly([p0 + r * r0, p0 + r * r1, p1 + r * r1, p1 + r * r0], col, nm)
        if caps:
            for p, nn in ((p1, a), (p0, -a)):
                self.poly([p + r * ring(i) for i in range(n)], col, nn)

    def disc(self, c, nrm, r, col, n=30, **k):
        nrm = _unit(nrm)
        t = np.array([0, 1, 0]) if abs(nrm[1]) < 0.9 else np.array([1, 0, 0])
        u = _unit(np.cross(nrm, t)); v = np.cross(nrm, u)
        c = np.array(c, float)
        self.poly([c + r * (math.cos(2 * math.pi * i / n) * u + math.sin(2 * math.pi * i / n) * v) for i in range(n)], col, nrm, **k)

    def sphere(self, c, r, col, squash=1.0):
        pc = self.cam(c)
        if pc[2] <= self.near:
            return
        u, v = self.proj1(pc)
        R = r * self.f / pc[2]
        if R < 1:
            return
        Ri = int(math.ceil(R)) + 2
        ui, vi = int(round(u)), int(round(v))
        xa, xb = max(-Ri, -ui), min(Ri, self.w - ui - 1)
        ya, yb_ = max(-Ri, -vi), min(Ri, self.h - vi - 1)
        if xb < xa or yb_ < ya:
            return
        yy, xx = np.mgrid[ya:yb_ + 1, xa:xb + 1].astype(np.float32)
        yy = yy / squash
        dist = np.sqrt(xx ** 2 + yy ** 2)
        mask = np.clip((R - dist) * 1.0 + 0.5, 0, 1)
        hlx, hly = -0.33 * R, -0.36 * R
        t = np.clip(np.sqrt((xx - hlx) ** 2 + (yy - hly) ** 2) / (1.55 * R), 0, 1)
        light = np.array(col, np.float32) * 1.12 + np.array([12, 10, -2], np.float32)
        dark = np.array(col, np.float32) * 0.80 + np.array([-4, 4, 14], np.float32)
        arr = (light[None, None, :] * (1 - t[..., None]) ** 1.15 + dark[None, None, :] * (1 - (1 - t[..., None]) ** 1.15))
        arr = np.clip(arr, 0, 255).astype('uint8')
        patch = Image.fromarray(arr, 'RGB')
        m = Image.fromarray((mask * 255).astype('uint8'), 'L')
        self.im.paste(patch, (ui + xa, vi + ya), m)

    # ------------------------------------------------------------------ soft shadows / AO (multiplicative, blurred)
    def shadow(self, pts, op=0.30, sig=7, tint=(70, 62, 78)):
        pcs = [self.cam(p) for p in pts]
        pcs = self._clip(pcs)
        if len(pcs) < 3:
            return
        sp = [self.proj1(p) for p in pcs]
        pad = int(4 * sig * self.ss)
        xs = [p[0] for p in sp]; ys = [p[1] for p in sp]
        x0, x1 = int(max(0, min(xs) - pad)), int(min(self.w, max(xs) + pad))
        y0, y1 = int(max(0, min(ys) - pad)), int(min(self.h, max(ys) + pad))
        if x1 <= x0 or y1 <= y0:
            return
        m = Image.new('L', (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).polygon([(p[0] - x0, p[1] - y0) for p in sp], fill=255)
        m = m.filter(ImageFilter.GaussianBlur(sig * self.ss))
        a = (np.asarray(m, np.float32)[..., None] * np.float32(op / 255.0))
        reg = np.asarray(self.im.crop((x0, y0, x1, y1)), np.float32)
        reg = reg * (1 - a) + np.asarray(tint, np.float32) * a
        self.im.paste(Image.fromarray(np.clip(reg, 0, 255).astype('uint8')), (x0, y0))
        del a, reg, m

    def foot_shadow(self, x, z, w, d, h=0.0, op=0.30, sig=7, y=0.0):
        """contact shadow for an upright object with ground footprint w x d; h adds a cast toward lower-right."""
        sx, sz = self.sdir * (0.28 * h)
        a = [(x - w / 2, y, z - d / 2), (x + w / 2, y, z - d / 2), (x + w / 2 + sx, y, z - d / 2 + sz), (x + w / 2 + sx, y, z + d / 2 + sz),
             (x - w / 2 + sx, y, z + d / 2 + sz), (x - w / 2, y, z + d / 2)]
        self.shadow(a, op, sig)

    # ------------------------------------------------------------------ fills
    def sky(self, top, bottom, horizon_v=None):
        hv = int((horizon_v if horizon_v is not None else self.h / 2 / self.ss) * self.ss)
        hv = max(1, min(self.h, hv))
        t = np.linspace(0, 1, hv)[:, None, None] ** 0.9
        arr = np.array(top, float)[None, None] * (1 - t) + np.array(bottom, float)[None, None] * t
        arr = np.repeat(arr, self.w, axis=1).astype('uint8')
        self.im.paste(Image.fromarray(arr, 'RGB'), (0, 0))

    def fill_rows(self, v0, col):
        self.d.rectangle([0, int(v0 * self.ss), self.w, self.h], fill=col)

    def vgrad_poly(self, pts, c0, c1, bands=10, n=(0, 0, -1), vaxis=1, cull=True):
        """vertical gradient on a vertical quad ll,lr,ur,ul : drawn as bands (smooth enough at 2x)."""
        ll, lr, ur, ul = [np.array(p, float) for p in pts]
        for i in range(bands):
            t0, t1 = i / bands, (i + 1) / bands
            col = mix(c0, c1, (t0 + t1) / 2)
            a0, a1 = ll + (ul - ll) * t0, ll + (ul - ll) * t1
            b0, b1 = lr + (ur - lr) * t0, lr + (ur - lr) * t1
            self.poly([a0, b0, b1, a1], col, n, shade=False, cull=cull)

    def glass(self, pts, col=None, n=(0, 0, -1), streak=0.22, band=True):
        """glass quad (ll,lr,ur,ul) with a soft vertical tone shift and two diagonal highlight streaks."""
        col = col or P['glass']
        ll, lr, ur, ul = [np.array(p, float) for p in pts]
        if band:
            self.vgrad_poly(pts, mix(col, (235, 242, 238), 0.30), mix(col, (150, 175, 175), 0.18), 6, n, cull=False)
        else:
            self.poly(pts, col, n, shade=False, cull=False)
        if streak:
            def at(u, v):
                return ll + (lr - ll) * u + (ul - ll) * v
            for (u0, w) in ((0.18, 0.10), (0.34, 0.05)):
                q = [at(u0, 0.0), at(u0 + w, 0.0), at(u0 + w + 0.28, 1.0), at(u0 + 0.28, 1.0)]
                q = [np.clip(p, None, None) for p in q]
                # clip streak to the quad by param range (u within 0..1)
                if all(0 <= u0 + 0.28 + w <= 1.0 for _ in [0]):
                    self.poly(q, (255, 255, 255), n, shade=False, cull=False, alpha=streak)

    def planks(self, ll, lr, ur, ul, n, col, amt=7, n_vec=(0, 0, -1), vertical=True, seam=True):
        """face split into n strips with a slight tonal variation (wood grain / panels)."""
        ll, lr, ur, ul = [np.array(p, float) for p in (ll, lr, ur, ul)]
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            if vertical:
                q = [ll + (lr - ll) * t0, ll + (lr - ll) * t1, ul + (ur - ul) * t1, ul + (ur - ul) * t0]
            else:
                q = [ll + (ul - ll) * t0, lr + (ur - lr) * t0, lr + (ur - lr) * t1, ll + (ul - ll) * t1]
            self.poly(q, jit(col, self.rng, amt), n_vec)
        if seam:
            for i in range(1, n):
                t = i / n
                if vertical:
                    a, b = ll + (lr - ll) * t, ul + (ur - ul) * t
                else:
                    a, b = ll + (ul - ll) * t, lr + (ur - lr) * t
                self.line3d(a, b, mix(col, (40, 28, 20), 0.28), 0.012, n_vec)

    def line3d(self, a, b, col, wm, n=(0, 0, -1)):
        """thin strip of width wm (metres) between two world points, lying in a plane facing n (or on the ground)."""
        a, b = np.array(a, float), np.array(b, float)
        pa, pb = self.cam(a), self.cam(b)
        if pa[2] < self.near or pb[2] < self.near:
            return
        ua, va = self.proj1(pa); ub, vb = self.proj1(pb)
        wa = max(1.0, wm * self.f / pa[2]); wb = max(1.0, wm * self.f / pb[2])
        d = np.array([ub - ua, vb - va]); L = np.linalg.norm(d)
        if L < 1e-6:
            return
        nx, ny = -d[1] / L, d[0] / L
        self.d.polygon([(ua + nx * wa / 2, va + ny * wa / 2), (ub + nx * wb / 2, vb + ny * wb / 2),
                        (ub - nx * wb / 2, vb - ny * wb / 2), (ua - nx * wa / 2, va - ny * wa / 2)], fill=col)

    # ------------------------------------------------------------------ billboards (approved character art)
    def billboard(self, img, x, z, h_m, y=0.0, flip=False, shadow=True, shadow_op=0.34, tag=None):
        """img: RGBA cut-out whose bottom edge is the sole line. Scaled so that sole->top spans h_m metres at (x,z)."""
        pc0 = self.cam((x, y, z)); pc1 = self.cam((x, y + h_m, z))
        if pc0[2] <= self.near:
            return None
        u0, v0 = self.proj1(pc0); u1, v1 = self.proj1(pc1)
        hs = v0 - v1
        sc = hs / img.height
        w = max(2, int(img.width * sc)); h = max(2, int(img.height * sc))
        im2 = img.transpose(Image.FLIP_LEFT_RIGHT) if flip else img
        im2 = im2.resize((w, h), Image.LANCZOS)
        a = np.asarray(img.split()[-1])
        low = a[int(a.shape[0] * 0.88):]
        cols = np.where((low > 128).any(axis=0))[0]
        fx = (cols.min() + cols.max()) / 2 / img.width if len(cols) else 0.5
        if flip:
            fx = 1 - fx
        if shadow:
            fw = (0.20 * h_m / 1.85) * 2.2
            self.foot_shadow(x, z, fw, fw * 0.55, h=0.45 * h_m, op=shadow_op, sig=5, y=y)
        px = int(round(u0 - fx * w)); py = int(round(v0 - h + 1))
        self.im.paste(im2.convert('RGB'), (px, py), im2.split()[-1])
        bb = (px / self.ss, py / self.ss, (px + w) / self.ss, (py + h) / self.ss)
        self.boxes.append((tag, bb))
        return bb

    # ------------------------------------------------------------------ output
    def finish(self):
        return self.im.resize((self.W, self.H), Image.LANCZOS)
