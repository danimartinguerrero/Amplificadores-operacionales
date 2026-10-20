"""Estilo y utilidades para los clips verticales (1080x1920) del Tema 1."""
import numpy as np
from manim import *

# lienzo vertical: 9 x 16 unidades
config.frame_height = 16
config.frame_width = 9

BG = "#0e1117"
FONT = "CMU Serif"
C_POS = "#FC6255"
C_NEG = "#58C4DD"
C_GREY = "#8b93a1"
C_GOLD = "#F4D35E"
C_GREEN = "#83C167"
C_PINK = "#FF7EB6"
TOTAL = 12

config.background_color = BG


def T(text, size=34, color=WHITE, **kw):
    return Text(text, font=FONT, font_size=size, color=color, **kw)


def M(tex, size=48, color=WHITE, **kw):
    return MathTex(tex, font_size=size, color=color, **kw)


class VClip(Scene):
    idx = 1
    title = ""

    def header(self):
        kick = T(f"LEYES BÁSICAS DE LA ELECTROSTÁTICA  ·  {self.idx}/{TOTAL}", 22, C_GREY)
        kick.move_to(UP * 7.15)
        tit = T(self.title, 46, WHITE, weight=BOLD)
        if tit.width > 8.2:
            tit.scale_to_fit_width(8.2)
        tit.next_to(kick, DOWN, buff=0.3)
        line = Line(LEFT * 0.5, RIGHT * 0.5, color=YELLOW, stroke_width=4).next_to(tit, DOWN, buff=0.25)
        self.play(FadeIn(kick), Write(tit), GrowFromCenter(line), run_time=0.8)
        self.hdr = VGroup(kick, tit, line)
        return self.hdr

    # ritmo global: alarga un poco animaciones y pausas sin perder dinamismo
    SLOW = 1.25

    def play(self, *args, run_time=None, **kw):
        if run_time is None:
            run_time = max([getattr(a, "run_time", 1.0) for a in args if isinstance(a, Animation)] or [1.0])
        super().play(*args, run_time=run_time * self.SLOW, **kw)

    def wait(self, duration=1.0, **kw):
        super().wait(duration * 1.3, **kw)

    def outro(self, hold=1.8):
        self.wait(max(hold, 2.2))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


def charge(sign, pos, r=0.22, label=None, size=30):
    col = C_POS if sign > 0 else C_NEG
    c = Circle(radius=r, color=col, fill_color=col, fill_opacity=0.95, stroke_width=2).move_to(pos)
    sym = MathTex("+" if sign > 0 else "-", font_size=int(85 * r), color=BLACK).move_to(c)
    g = VGroup(c, sym)
    if label:
        g.add(MathTex(label, font_size=size, color=col).next_to(c, RIGHT, buff=0.12))
    return g


def glow_dot(pos, color=YELLOW, r=0.08):
    return VGroup(Dot(pos, radius=r * 2.6, color=color, fill_opacity=0.18),
                  Dot(pos, radius=r * 1.6, color=color, fill_opacity=0.35),
                  Dot(pos, radius=r, color=color))


def blob_pts(center, scale, seed=0, n=240, dent=0.0):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.06, 0.16, 3)
    ph = rng.uniform(0, TAU, 3)
    ts = np.linspace(0, TAU, n, endpoint=False)
    r = 1 + a[0] * np.sin(2 * ts + ph[0]) + a[1] * np.cos(3 * ts + ph[1]) + a[2] * np.sin(5 * ts + ph[2])
    r = r - dent * np.exp(-((ts - PI / 2 + 0.3) ** 2) / 0.08)
    pts = np.stack([r * np.cos(ts), r * np.sin(ts) * 1.1, 0 * ts], axis=1)
    return pts * scale + np.array(center)


def smooth_closed(pts, **kw):
    m = VMobject(**kw)
    m.set_points_smoothly([*pts, pts[0]])
    return m


def ray_hits(O, d, pts):
    """Parámetros t>0 de los cortes de la semirrecta O + t d con el polígono cerrado pts."""
    O = np.asarray(O)[:2]
    d = np.asarray(d)[:2]
    P = np.asarray(pts)[:, :2]
    Q = np.roll(P, -1, axis=0)
    e = Q - P
    den = d[0] * e[:, 1] - d[1] * e[:, 0]
    w = P - O
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (w[:, 0] * e[:, 1] - w[:, 1] * e[:, 0]) / den
        s = (w[:, 0] * d[1] - w[:, 1] * d[0]) / den
    ok = (np.abs(den) > 1e-12) & (t > 1e-6) & (s >= 0) & (s < 1)
    return np.sort(t[ok])


def field_lines(charges, n_per=16, box=(4.4, 5.6), step=0.02, center=ORIGIN, rstart=0.25, max_steps=3000,
                color=WHITE, sw=2.2, phase=0.0):
    """Líneas de campo integradas numéricamente desde las cargas positivas."""
    cs = [(q, np.array(p, dtype=float)[:2]) for q, p in charges]
    c0 = np.array(center)[:2]

    def E(x):
        v = np.zeros(2)
        for q, p in cs:
            r = x - p
            d = np.hypot(*r)
            v += q * r / max(d, 1e-6) ** 3
        return v

    lines = VGroup()
    for q, p in cs:
        if q <= 0:
            continue
        for k in range(n_per):
            a = TAU * (k + 0.5 + phase) / n_per
            x = p + rstart * np.array([np.cos(a), np.sin(a)])
            pts = [x.copy()]
            for _ in range(max_steps):
                v = E(x)
                n = np.hypot(*v)
                if n < 1e-9:
                    break
                k1 = v / n
                v2 = E(x + 0.5 * step * k1)
                k2 = v2 / max(np.hypot(*v2), 1e-9)
                x = x + step * k2
                pts.append(x.copy())
                if abs(x[0] - c0[0]) > box[0] or abs(x[1] - c0[1]) > box[1]:
                    break
                if any(qq < 0 and np.hypot(*(x - pp)) < rstart for qq, pp in cs):
                    break
            pts = np.array(pts)[::4]
            if len(pts) < 3:
                continue
            m = VMobject(stroke_color=color, stroke_width=sw, stroke_opacity=0.85)
            m.set_points_smoothly([np.array([*pp, 0]) for pp in pts])
            lines.add(m)
    return lines


def equipotentials(charges, levels, box=(4.4, 5.6), center=ORIGIN, res=400, sw=2):
    import contourpy
    xs = np.linspace(center[0] - box[0], center[0] + box[0], res)
    ys = np.linspace(center[1] - box[1], center[1] + box[1], int(res * box[1] / box[0]))
    X, Y = np.meshgrid(xs, ys)
    V = np.zeros_like(X)
    for q, p in charges:
        V += q / np.maximum(np.hypot(X - p[0], Y - p[1]), 1e-3)
    gen = contourpy.contour_generator(xs, ys, V)
    g = VGroup()
    for lv in levels:
        col = C_POS if lv > 0 else C_NEG if lv < 0 else WHITE
        for seg in gen.lines(lv):
            if len(seg) < 4:
                continue
            seg = seg[:: max(1, len(seg) // 120)]
            m = VMobject(stroke_color=col, stroke_width=sw, stroke_opacity=0.7)
            m.set_points_smoothly([np.array([x, y, 0]) for x, y in seg])
            g.add(m)
    return g
