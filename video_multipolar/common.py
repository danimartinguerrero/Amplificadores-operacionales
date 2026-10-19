"""Infraestructura común: estilo, sincronización con la narración y utilidades."""
import json
import os

import numpy as np
from manim import *

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO_DIR = os.path.join(ROOT, "audio")
SUBS_DIR = os.path.join(ROOT, "build", "subs")

with open(os.path.join(ROOT, "narration.json"), encoding="utf-8") as f:
    NARR = json.load(f)

_dur_path = os.path.join(AUDIO_DIR, "durations.json")
DURATIONS = json.load(open(_dur_path)) if os.path.exists(_dur_path) else {}

# ---------------------------------------------------------------- estilo
BG = "#0e1117"
FONT = "CMU Serif"
C_POS = "#FC6255"      # carga positiva / potencial positivo
C_NEG = "#58C4DD"      # carga negativa / potencial negativo
C_R = YELLOW           # punto campo
C_RP = TEAL            # punto fuente
C_RR = "#FF7EB6"       # vector R
C_GREY = "#8b93a1"
L_COLORS = [YELLOW, "#83C167", C_POS, "#9A72AC", C_NEG, ORANGE]

config.background_color = BG
Tex.set_default(color=WHITE)
MathTex.set_default(color=WHITE)

GAP = 0.45  # silencio entre frases (s)


def T(text, size=34, color=WHITE, **kw):
    return Text(text, font=FONT, font_size=size, color=color, **kw)


def seg_duration(scene, key):
    k = f"{scene}_{key}"
    if k in DURATIONS:
        return DURATIONS[k]
    return len(NARR[scene][key]) / 14.5  # estimación sin audio


class VScene(MovingCameraScene):
    """Escena que avanza al ritmo de la narración.

    ``self.say(k)`` lanza el audio del fragmento k y fija cuándo acaba; las
    animaciones que siguen se reproducen encima, y el siguiente ``say`` (o
    ``sync``) espera a que la frase termine.
    """

    def setup(self):
        super().setup()
        self._seg_end = 0.0
        self._subs = []

    @property
    def sname(self):
        return type(self).__name__

    def say(self, key):
        self.sync()
        dur = seg_duration(self.sname, key)
        path = os.path.join(AUDIO_DIR, f"{self.sname}_{key}.mp3")
        if os.path.exists(path):
            self.add_sound(path)
        start = self.time
        self._seg_end = start + dur + GAP
        self._subs.append({"key": key, "start": start, "end": start + dur,
                           "text": NARR[self.sname][key]})

    def remaining(self):
        return max(self._seg_end - self.time, 0)

    def sync(self):
        rem = self._seg_end - self.time
        if rem > 1 / 60:
            self.wait(rem)

    def end(self, tail=0.6):
        self.sync()
        self.wait(tail)
        os.makedirs(SUBS_DIR, exist_ok=True)
        with open(os.path.join(SUBS_DIR, f"{self.sname}.json"), "w") as f:
            json.dump({"total": self.time, "subs": self._subs}, f,
                      ensure_ascii=False, indent=1)

    def clear(self, run_time=0.8):
        mobs = [m for m in self.mobjects]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)


def section_label(num, text):
    lab = VGroup(T(f"{num}", 24, C_GREY), T(text, 24, C_GREY)).arrange(RIGHT, buff=0.25)
    return lab.to_corner(UL, buff=0.4)


# ---------------------------------------------------------------- objetos
def _blob_params(seed):
    rng = np.random.default_rng(seed)
    return rng.uniform(0.08, 0.2, 3), rng.uniform(0, TAU, 3)


def _blob_r(ts, seed):
    a, ph = _blob_params(seed)
    return 1 + a[0] * np.sin(2 * ts + ph[0]) + a[1] * np.cos(3 * ts + ph[1]) + a[2] * np.sin(5 * ts + ph[2])


def blob_points(center=ORIGIN, scale=1.0, seed=0, n=200):
    ts = np.linspace(0, TAU, n, endpoint=False)
    r = _blob_r(ts, seed)
    pts = np.stack([r * np.cos(ts) * 1.15, r * np.sin(ts), 0 * ts], axis=1)
    return pts * scale + np.array(center)


def make_blob(center=ORIGIN, scale=1.0, seed=0, color=C_POS, n_dots=140, signs=False):
    pts = blob_points(center, scale, seed)
    shape = VMobject(color=color, stroke_width=2.5)
    shape.set_points_smoothly([*pts, pts[0]])
    shape.set_fill(color, opacity=0.12)
    rng = np.random.default_rng(seed + 7)
    dots = VGroup()
    c = np.array(center)
    while len(dots) < n_dots:
        u = rng.uniform(-1.4, 1.4, 2)
        ang = np.arctan2(u[1], u[0] / 1.15)
        rr = np.hypot(u[0] / 1.15, u[1])
        if rr > 0.92 * _blob_r(ang, seed):
            continue
        p = c + np.array([u[0], u[1], 0]) * scale
        col = color
        if signs:
            col = C_POS if rng.random() < 0.6 else C_NEG
        dots.add(Dot(p, radius=0.024 * scale ** 0.5, color=col,
                     fill_opacity=float(np.clip(1.0 - 0.6 * rr, 0.25, 1))))
    return VGroup(shape, dots)


def charge(sign, pos, r=0.2, label=None):
    col = C_POS if sign > 0 else C_NEG
    c = Circle(radius=r, color=col, fill_color=col, fill_opacity=0.9, stroke_width=2)
    c.move_to(pos)
    sym = MathTex("+" if sign > 0 else "-", font_size=int(80 * r), color=BLACK).move_to(c)
    g = VGroup(c, sym)
    if label:
        g.add(MathTex(label, font_size=30, color=col).next_to(c, RIGHT, buff=0.12))
    return g


def potential_image(f, center=ORIGIN, width=8.0, height=8.0, res=360, vmax=1.0,
                    alpha=0.6, rmin=0.0, edge=0.9):
    nx = res
    ny = int(res * height / width)
    xs = np.linspace(-width / 2, width / 2, nx)
    ys = np.linspace(height / 2, -height / 2, ny)
    X, Y = np.meshgrid(xs, ys)
    with np.errstate(all="ignore"):
        V = f(X, Y)
    V = np.nan_to_num(V)
    v = np.tanh(V / vmax)
    pos = np.array([252, 98, 85])
    neg = np.array([88, 196, 221])
    rgb = np.where(v[..., None] > 0, pos, neg)
    a = (np.abs(v) ** 0.9) * alpha * 255
    if rmin > 0:
        a = a * np.clip((np.hypot(X, Y) - rmin) / 0.15, 0, 1)
    if edge > 0:  # difumina los bordes del rectángulo
        de = np.minimum(width / 2 - np.abs(X), height / 2 - np.abs(Y))
        a = a * np.clip(de / edge, 0, 1) ** 1.5
    img = np.dstack([rgb, a]).astype(np.uint8)
    im = ImageMobject(img)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
    im.stretch_to_fit_width(width)
    im.stretch_to_fit_height(height)
    im.move_to(center)
    return im


def polar_curve(rfun, t0, t1, center=ORIGIN, scale=1.0, n=300, **kw):
    """Curva en el plano meridiano: (x, z) = r(θ)(sen θ, cos θ)."""
    ts = np.linspace(t0, t1, n)
    pts = []
    for t in ts:
        r = rfun(t)
        pts.append(np.array([r * np.sin(t), r * np.cos(t), 0]) * scale + np.array(center))
    m = VMobject(**kw)
    m.set_points_smoothly(pts)
    return m


def dipole_equipotentials(Ks, center=ORIGIN, scale=1.0, sw=2):
    g = VGroup()
    for K in Ks:
        for sgn, col in [(1, C_POS), (-1, C_NEG)]:
            def rf(t, K=K, sgn=sgn):
                return np.sqrt(max(K * sgn * np.cos(t), 0))
            if sgn > 0:
                c = polar_curve(rf, -PI / 2, PI / 2, center, scale, stroke_width=sw, color=col)
            else:
                c = polar_curve(rf, PI / 2, 3 * PI / 2, center, scale, stroke_width=sw, color=col)
            g.add(c)
    return g


def dipole_field_lines(Cs, center=ORIGIN, scale=1.0, rmin=0.35, sw=2, color=WHITE):
    g = VGroup()
    for C in Cs:
        s = np.sqrt(min(rmin / C, 1))
        t0 = np.arcsin(s)
        for side in (1, -1):
            def rf(t, C=C):
                return C * np.sin(t) ** 2
            c = polar_curve(rf, side * t0, side * (PI - t0), center, scale,
                            stroke_width=sw, color=color, stroke_opacity=0.85)
            g.add(c)
    return g


def quad_equipotentials(Ks, center=ORIGIN, scale=1.0, sw=2):
    th0 = np.arccos(1 / np.sqrt(3))
    g = VGroup()
    for K in Ks:
        def rp(t, K=K):
            return np.cbrt(max(K * (3 * np.cos(t) ** 2 - 1), 0))
        def rn(t, K=K):
            return np.cbrt(max(-K / 2 * (3 * np.cos(t) ** 2 - 1), 0))
        g.add(polar_curve(rp, -th0, th0, center, scale, stroke_width=sw, color=C_POS))
        g.add(polar_curve(rp, PI - th0, PI + th0, center, scale, stroke_width=sw, color=C_POS))
        g.add(polar_curve(rn, th0, PI - th0, center, scale, stroke_width=sw, color=C_NEG))
        g.add(polar_curve(rn, PI + th0, TAU - th0, center, scale, stroke_width=sw, color=C_NEG))
    return g


def quad_field_lines(Cs, center=ORIGIN, scale=1.0, rmin=0.35, sw=2, rmax=6):
    g = VGroup()
    for C in Cs:
        for q0 in (0, PI / 2, PI, 3 * PI / 2):
            ts = np.linspace(q0 + 1e-3, q0 + PI / 2 - 1e-3, 400)
            pts = []
            for t in ts:
                r = np.sqrt(C * np.sin(t) ** 2 * abs(np.cos(t)))
                if rmin < r < rmax:
                    pts.append(np.array([r * np.sin(t), r * np.cos(t), 0]) * scale + np.array(center))
                elif pts:
                    # tramo separado: guardamos y reiniciamos
                    if len(pts) > 3:
                        m = VMobject(stroke_width=sw, color=WHITE, stroke_opacity=0.8)
                        m.set_points_smoothly(pts)
                        g.add(m)
                    pts = []
            if len(pts) > 3:
                m = VMobject(stroke_width=sw, color=WHITE, stroke_opacity=0.8)
                m.set_points_smoothly(pts)
                g.add(m)
    return g
