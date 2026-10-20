from common_v import *


def surface_plane(y=0.0, w=8.2, depth=1.6, n_signs=9):
    """Plano cargado visto en perspectiva."""
    sk = 0.9
    p = Polygon([-w / 2 + sk, y + depth / 2, 0], [w / 2 + sk, y + depth / 2, 0],
                [w / 2 - sk, y - depth / 2, 0], [-w / 2 - sk, y - depth / 2, 0],
                color=C_POS, stroke_width=2).set_fill(C_POS, 0.18)
    signs = VGroup(*[M("+", 30, C_POS).move_to([x + 0.35 * ((i % 2) - 0.5), y + 0.3 * ((i % 2) * 2 - 1) * 0.5, 0])
                     for i, x in enumerate(np.linspace(-w / 2 + 0.6, w / 2 - 0.6, n_signs))])
    return VGroup(p, signs)


def region_labels(y=0.0, x=-3.7):
    return VGroup(VGroup(Circle(0.26, color=WHITE, stroke_width=2), M("2", 30)).move_to([x, y + 1.3, 0]),
                  VGroup(Circle(0.26, color=WHITE, stroke_width=2), M("1", 30)).move_to([x, y - 1.3, 0]))


class C07_Normal(VClip):
    idx = 7
    title = "Condición de contorno: E normal"

    def construct(self):
        self.header()
        y0 = -0.4
        pl = surface_plane(y0)
        rl = region_labels(y0)
        sig = M(r"\sigma", 44, C_POS).move_to([3.4, y0 - 1.15, 0])
        nar = Arrow([-2.7, y0, 0], [-2.7, y0 + 2.6, 0], buff=0, color=WHITE, stroke_width=4)
        nl = M(r"\hat n", 36).next_to(nar.get_end(), RIGHT, buff=0.1)
        self.play(FadeIn(pl, shift=0.3 * UP), FadeIn(rl), FadeIn(sig), run_time=0.7)
        self.play(GrowArrow(nar), FadeIn(nl), run_time=0.4)
        # campos a cada lado
        E2 = Arrow([1.6, y0 + 1.0, 0], [2.6, y0 + 3.6, 0], buff=0, color=YELLOW, stroke_width=6)
        E1 = Arrow([1.6, y0 - 3.4, 0], [2.4, y0 - 2.4, 0], buff=0, color=C_NEG, stroke_width=6)
        E2l = M(r"\vec E_2", 38, YELLOW).next_to(E2.get_end(), RIGHT, buff=0.1)
        E1l = M(r"\vec E_1", 38, C_NEG).next_to(E1.get_end(), RIGHT, buff=0.1)
        self.play(GrowArrow(E2), GrowArrow(E1), FadeIn(E2l), FadeIn(E1l), run_time=0.6)
        # cilindro gaussiano de altura h
        h = ValueTracker(2.6)
        cx = 0.0

        def pill():
            hh = h.get_value()
            top = Ellipse(width=2.2, height=0.6, color=WHITE, stroke_width=3).move_to([cx, y0 + hh / 2, 0]).set_fill(WHITE, 0.08)
            bot = DashedVMobject(Ellipse(width=2.2, height=0.6, color=WHITE, stroke_width=3).move_to([cx, y0 - hh / 2, 0]), num_dashes=24)
            sides = VGroup(Line([cx - 1.1, y0 - hh / 2, 0], [cx - 1.1, y0 + hh / 2, 0], color=WHITE, stroke_width=3),
                           Line([cx + 1.1, y0 - hh / 2, 0], [cx + 1.1, y0 + hh / 2, 0], color=WHITE, stroke_width=3))
            n2 = Arrow([cx, y0 + hh / 2, 0], [cx, y0 + hh / 2 + 1.0, 0], buff=0, color=YELLOW, stroke_width=4)
            n1 = Arrow([cx, y0 - hh / 2, 0], [cx, y0 - hh / 2 - 1.0, 0], buff=0, color=C_NEG, stroke_width=4)
            return VGroup(bot, sides, top, n2, n1)

        P = always_redraw(pill)
        hb = always_redraw(lambda: VGroup(
            DoubleArrow([cx - 1.6, y0 - h.get_value() / 2, 0], [cx - 1.6, y0 + h.get_value() / 2, 0], buff=0,
                        color=C_GREY, stroke_width=3, tip_length=0.15),
            M("h", 32, C_GREY).move_to([cx - 1.95, y0, 0])))
        self.play(FadeIn(P), FadeIn(hb), run_time=0.6)
        g1 = M(r"\Phi=E_{2n}\Delta S-E_{1n}\Delta S+\Phi_{\text{lat}}=\frac{\sigma\Delta S}{\varepsilon_0}", 46)
        g1.move_to(UP * 4.4)
        self.play(Write(g1), run_time=1.2)
        lat = T("h → 0: la cara lateral desaparece", 28, C_GREY).next_to(g1, DOWN, buff=0.35)
        self.play(FadeIn(lat), h.animate.set_value(0.12), run_time=2.0)
        self.play(Indicate(g1[0][16:21], color=C_GREY), run_time=0.6)
        self.wait(0.4)
        res = M(r"E_{2n}-E_{1n}=\frac{\sigma}{\varepsilon_0}", 76, YELLOW).move_to(DOWN * 5.0)
        box = SurroundingRectangle(res, color=YELLOW, buff=0.25)
        self.play(Write(res), run_time=0.9)
        self.play(Create(box), run_time=0.4)
        cap = T("la componente normal SALTA", 30, YELLOW).next_to(box, UP, buff=0.25)
        self.play(FadeIn(cap), h.animate.set_value(1.2), run_time=0.6)
        self.outro(1.8)


class C08_Tangencial(VClip):
    idx = 8
    title = "Condición de contorno: E tangencial"

    def construct(self):
        self.header()
        y0 = 0.2
        surf = Line([-4.4, y0, 0], [4.4, y0, 0], color=C_POS, stroke_width=6)
        signs = VGroup(*[M("+", 28, C_POS).move_to([x, y0 - 0.28, 0]) for x in np.linspace(-4, 4, 11)])
        rl = region_labels(y0, -3.8)
        self.play(Create(surf), FadeIn(signs), FadeIn(rl), run_time=0.6)
        h = ValueTracker(2.6)
        w = 3.4

        def loop():
            hh = h.get_value()
            pts = [[-w / 2, y0 - hh / 2, 0], [w / 2, y0 - hh / 2, 0], [w / 2, y0 + hh / 2, 0], [-w / 2, y0 + hh / 2, 0]]
            sq = Polygon(*pts, color=WHITE, stroke_width=3).set_fill(WHITE, 0.05)
            a_top = Arrow([0.6, y0 + hh / 2, 0], [-0.6, y0 + hh / 2, 0], buff=0, color=YELLOW, stroke_width=5)
            a_bot = Arrow([-0.6, y0 - hh / 2, 0], [0.6, y0 - hh / 2, 0], buff=0, color=C_NEG, stroke_width=5)
            return VGroup(sq, a_top, a_bot)

        L = always_redraw(loop)
        lt = always_redraw(lambda: M(r"\Delta\vec\ell_2", 34, YELLOW).move_to([0, y0 + h.get_value() / 2 + 0.45, 0]))
        lb = always_redraw(lambda: M(r"\Delta\vec\ell_1", 34, C_NEG).move_to([0, y0 - h.get_value() / 2 - 0.45, 0]))
        self.play(FadeIn(L), FadeIn(lt), FadeIn(lb), run_time=0.6)
        # punto que recorre el circuito
        s = ValueTracker(0)
        dot = always_redraw(lambda: glow_dot(L[0].point_from_proportion(s.get_value() % 1), YELLOW, 0.07))
        self.add(dot)
        g1 = M(r"\oint\vec E\cdot\mathrm d\vec\ell=(E_{2t}-E_{1t})\,\Delta\ell+O(h)=0", 46).move_to(UP * 4.4)
        self.play(Write(g1), s.animate.set_value(1), run_time=1.6, rate_func=linear)
        cap = T("en electrostática la circulación es nula", 26, C_GREY).next_to(g1, DOWN, buff=0.3)
        self.play(FadeIn(cap), s.animate.set_value(2), run_time=1.2, rate_func=linear)
        self.remove(dot)
        self.play(h.animate.set_value(0.12), run_time=1.6)
        res = M(r"E_{2t}=E_{1t}", 80, C_GREEN).move_to(DOWN * 5.0)
        box = SurroundingRectangle(res, color=C_GREEN, buff=0.25)
        self.play(Write(res), Create(box), run_time=0.8)
        self.wait(0.3)
        # descomposición: el campo «se quiebra»
        self.play(FadeOut(VGroup(L, lt, lb)), FadeOut(cap), run_time=0.4)
        P0 = np.array([0.3, y0, 0])
        Et = 1.8
        E2 = Arrow(P0, P0 + np.array([Et, 2.8, 0]), buff=0, color=YELLOW, stroke_width=6)
        E1 = Arrow(P0 + np.array([-Et, -1.0, 0]), P0, buff=0, color=C_NEG, stroke_width=6)
        self.play(GrowArrow(E1), run_time=0.5)
        self.play(GrowArrow(E2), run_time=0.5)
        t2 = Arrow(P0, P0 + np.array([Et, 0, 0]) + UP * 0.02, buff=0, color=C_GREEN, stroke_width=6)
        n2 = DashedLine(P0 + np.array([Et, 0, 0]), P0 + np.array([Et, 2.8, 0]), color=YELLOW)
        t1 = Arrow(P0 + np.array([-Et, -0.02, 0]), P0 + DOWN * 0.02, buff=0, color=C_GREEN, stroke_width=6)
        n1 = DashedLine(P0 + np.array([-Et, -1.0, 0]), P0 + np.array([-Et, 0, 0]), color=C_NEG)
        self.play(GrowArrow(t1), GrowArrow(t2), Create(n1), Create(n2), run_time=0.7)
        lbls = VGroup(M(r"E_t", 34, C_GREEN).next_to(t2, DOWN, buff=0.12).shift(RIGHT * 0.2),
                      M(r"E_t", 34, C_GREEN).next_to(t1, UP, buff=0.12).shift(LEFT * 0.2),
                      M(r"E_{2n}", 34, YELLOW).next_to(n2, RIGHT, buff=0.1),
                      M(r"E_{1n}", 34, C_NEG).next_to(n1, LEFT, buff=0.1))
        self.play(FadeIn(lbls), run_time=0.5)
        cap2 = VGroup(T("el campo se «quiebra»", 30, WHITE),
                      M(r"E_t\ \text{igual},\quad E_n\ \text{salta}\ \sigma/\varepsilon_0", 40)).arrange(DOWN, buff=0.2)
        cap2.move_to(UP * 3.1)
        self.play(FadeIn(cap2), Indicate(VGroup(t1, t2), color=C_GREEN), run_time=0.8)
        self.outro(1.8)


class C09_Potencial(VClip):
    idx = 9
    title = "Condición de contorno: el potencial"

    def construct(self):
        self.header()
        y0 = 2.0
        surf = Line([-4.4, y0, 0], [4.4, y0, 0], color=C_POS, stroke_width=6)
        rl = region_labels(y0, -3.8)
        h = ValueTracker(2.4)
        A = always_redraw(lambda: VGroup(Dot([0, y0 - h.get_value() / 2, 0], color=C_NEG, radius=0.1),
                                         M("A", 32, C_NEG).next_to([0, y0 - h.get_value() / 2, 0], LEFT, buff=0.15)))
        B = always_redraw(lambda: VGroup(Dot([0, y0 + h.get_value() / 2, 0], color=YELLOW, radius=0.1),
                                         M("B", 32, YELLOW).next_to([0, y0 + h.get_value() / 2, 0], LEFT, buff=0.15)))
        path = always_redraw(lambda: Arrow([0, y0 - h.get_value() / 2, 0], [0, y0 + h.get_value() / 2, 0], buff=0.1,
                                           color=WHITE, stroke_width=4))
        self.play(Create(surf), FadeIn(rl), FadeIn(A), FadeIn(B), FadeIn(path), run_time=0.7)
        g = M(r"\phi_2-\phi_1=-\int_A^B\vec E\cdot\mathrm d\vec\ell=-\langle E_n\rangle\,h\ \xrightarrow{h\to0}\ 0", 44)
        g.move_to(UP * 4.6)
        self.play(Write(g), run_time=1.2)
        self.play(h.animate.set_value(0.1), run_time=1.4)
        r = M(r"\phi_2=\phi_1", 66, C_PINK).move_to(UP * 0.4)
        self.play(Write(r), run_time=0.6)
        self.wait(0.3)
        # ejemplo: plano infinito
        self.play(FadeOut(VGroup(surf, rl, A, B, path, r)), g.animate.scale(0.8).shift(UP * 0.2), run_time=0.5)
        axE = Axes(x_range=[-3, 3, 1], y_range=[-1.4, 1.4, 1], x_length=7.6, y_length=3.2,
                   axis_config={"color": C_GREY, "include_tip": False}).move_to(UP * 1.4)
        axP = Axes(x_range=[-3, 3, 1], y_range=[-3.2, 0.4, 1], x_length=7.6, y_length=3.2,
                   axis_config={"color": C_GREY, "include_tip": False}).move_to(DOWN * 2.6)
        lE = M(r"E_z(z)", 34, YELLOW).next_to(axE, UP, buff=0.05).align_to(axE, LEFT)
        lP = M(r"\phi(z)", 34, C_PINK).next_to(axP, UP, buff=0.05).align_to(axP, LEFT)
        zE = M("z", 30, C_GREY).next_to(axE.x_axis.get_end(), DOWN, buff=0.1)
        zP = M("z", 30, C_GREY).next_to(axP.x_axis.get_end(), UP, buff=0.1)
        self.play(Create(axE), Create(axP), FadeIn(lE), FadeIn(lP), FadeIn(zE), FadeIn(zP), run_time=0.6)
        e_left = axE.plot(lambda z: -1, x_range=[-3, -0.001], color=YELLOW, stroke_width=5)
        e_right = axE.plot(lambda z: 1, x_range=[0.001, 3], color=YELLOW, stroke_width=5)
        phi = axP.plot(lambda z: -abs(z), x_range=[-3, 3, 0.01], color=C_PINK, stroke_width=5)
        self.play(Create(e_left), run_time=0.6)
        self.play(Create(e_right), run_time=0.6)
        jump = DoubleArrow(axE.c2p(0.25, -1), axE.c2p(0.25, 1), buff=0, color=WHITE, stroke_width=3, tip_length=0.18)
        jl = M(r"\frac{\sigma}{\varepsilon_0}", 40).next_to(jump, RIGHT, buff=0.1)
        self.play(GrowFromCenter(jump), FadeIn(jl), run_time=0.5)
        self.play(Create(phi), run_time=1.0)
        kink = glow_dot(axP.c2p(0, 0), C_PINK, 0.08)
        kl = T("continuo (con pico)", 26, C_PINK).next_to(axP.c2p(0, 0), RIGHT, buff=0.3).shift(DOWN * 0.2)
        self.play(FadeIn(kink), FadeIn(kl), run_time=0.5)
        self.wait(0.6)
        # tarjeta resumen
        self.play(FadeOut(VGroup(axE, axP, lE, lP, zE, zP, e_left, e_right, phi, jump, jl, kink, kl, g)), run_time=0.5)
        card = VGroup(M(r"E_{2n}-E_{1n}=\frac{\sigma}{\varepsilon_0}", 64, YELLOW),
                      M(r"E_{2t}=E_{1t}", 64, C_GREEN),
                      M(r"\phi_2=\phi_1", 64, C_PINK)).arrange(DOWN, buff=0.8).move_to(DOWN * 0.3)
        tit = T("Las tres condiciones", 36, WHITE).next_to(card, UP, buff=0.8)
        box = SurroundingRectangle(card, color=WHITE, buff=0.45, corner_radius=0.15)
        self.play(FadeIn(tit), LaggedStart(*[FadeIn(x, shift=0.3 * UP) for x in card], lag_ratio=0.35), run_time=1.3)
        self.play(Create(box), run_time=0.5)
        self.outro(2.0)


class C10_Anillo(VClip):
    idx = 10
    title = "Seminario: campo de un anillo"

    def construct(self):
        self.header()
        cy = -3.0
        a, k = 2.4, 0.3  # semieje y achatamiento de la perspectiva
        ring = Ellipse(width=2 * a, height=2 * a * k, color=C_POS, stroke_width=7)
        ring.move_to([0, cy, 0])
        zax = Arrow([0, cy - 1.0, 0], [0, 4.3, 0], buff=0, color=C_GREY, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        zl = M("z", 32, C_GREY).next_to(zax.get_end(), RIGHT, buff=0.1)
        Q = M("Q", 38, C_POS).next_to(ring, RIGHT, buff=0.15)
        self.play(Create(ring), GrowArrow(zax), FadeIn(zl), FadeIn(Q), run_time=0.8)
        zP = 2.0
        sc = 1.6  # unidades de pantalla por unidad de z
        P = np.array([0, cy + zP * sc, 0])
        pd = glow_dot(P, WHITE, 0.08)
        pl = M("P", 34).next_to(P, LEFT, buff=0.2)
        self.play(FadeIn(pd), FadeIn(pl), run_time=0.4)
        ph = ValueTracker(-0.3)

        def on_ring(t):
            return np.array([a * np.cos(t), cy + a * k * np.sin(t), 0])

        def contrib():
            g = VGroup()
            for t, col in [(ph.get_value(), C_GOLD), (ph.get_value() + PI, C_NEG)]:
                q = on_ring(t)
                g.add(Dot(q, radius=0.13, color=col))
                g.add(DashedLine(q, P, color=col, stroke_width=2, stroke_opacity=0.6))
                d = normalize(P - q)
                end = P + 1.6 * d
                g.add(Arrow(P, end, buff=0, color=col, stroke_width=5, max_tip_length_to_length_ratio=0.15))
                g.add(DashedLine(end, np.array([P[0], end[1], 0]), color=col, stroke_width=2))
            return g

        C = always_redraw(contrib)
        self.play(FadeIn(C), run_time=0.5)
        cap = T("las componentes horizontales se cancelan", 28, WHITE).move_to(UP * 4.3)
        self.play(FadeIn(cap), ph.animate.set_value(PI - 0.3), run_time=3.0, rate_func=linear)
        Ez = Arrow(P, P + UP * 2.2, buff=0, color=YELLOW, stroke_width=8, max_tip_length_to_length_ratio=0.15)
        Ezl = M(r"\vec E", 40, YELLOW).next_to(Ez.get_end(), RIGHT, buff=0.1)
        self.play(FadeOut(C), GrowArrow(Ez), FadeIn(Ezl), run_time=0.6)
        f = M(r"\vec E_{\text{anillo}}=\frac{Q\,z}{4\pi\varepsilon_0\,(a^2+z^2)^{3/2}}\,\hat u_z", 52).move_to(UP * 4.3)
        self.play(FadeOut(cap), Write(f), run_time=1.0)
        self.wait(0.5)
        # gráfica E(z)
        self.play(FadeOut(VGroup(ring, zax, zl, Q, pd, pl, Ez, Ezl)), run_time=0.4)
        ax = Axes(x_range=[-4, 4, 1], y_range=[-1.2, 1.2, 0.5], x_length=8.2, y_length=5.0,
                  axis_config={"color": C_GREY, "include_tip": False}).move_to(DOWN * 0.8)
        xl = M("z/a", 32, C_GREY).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        Emax = (1 / np.sqrt(2)) / (1.5) ** 1.5
        E = lambda z: z / (1 + z ** 2) ** 1.5 / Emax
        curve = ax.plot(E, x_range=[-4, 4, 0.01], color=YELLOW, stroke_width=5)
        self.play(Create(ax), FadeIn(xl), run_time=0.5)
        z = ValueTracker(-4)
        part = always_redraw(lambda: ax.plot(E, x_range=[-4, z.get_value(), 0.01], color=YELLOW, stroke_width=5))
        dot = always_redraw(lambda: glow_dot(ax.c2p(z.get_value(), E(z.get_value())), WHITE, 0.07))
        self.add(part, dot)
        self.play(z.animate.set_value(4), run_time=2.6, rate_func=smooth)
        zm = 1 / np.sqrt(2)
        mk = DashedLine(ax.c2p(zm, 0), ax.c2p(zm, 1), color=C_PINK)
        ml = M(r"z=\frac{a}{\sqrt2}", 38, C_PINK).next_to(ax.c2p(zm, 1), UR, buff=0.1)
        zc = T("0 en el centro", 26, C_GREY).next_to(ax.c2p(0, 0), DL, buff=0.2)
        self.play(Create(mk), FadeIn(ml), FadeIn(zc), run_time=0.6)
        far = M(r"|z|\gg a:\ E\to\frac{Q}{4\pi\varepsilon_0 z^2}", 46, C_GREY).move_to(DOWN * 4.9)
        self.play(Write(far), run_time=0.8)
        self.outro(1.8)


class C11_Disco(VClip):
    idx = 11
    title = "Seminario: del disco al plano"

    def construct(self):
        self.header()
        cy = -3.2
        k = 0.3
        a = ValueTracker(0.05)
        A0 = 2.4
        zax = Arrow([0, cy - 1.0, 0], [0, 3.3, 0], buff=0, color=C_GREY, stroke_width=2, max_tip_length_to_length_ratio=0.03)
        zP = 1.4
        sc = 1.6
        P = np.array([0, cy + zP * sc, 0])

        def disc():
            r = a.get_value()
            g = VGroup()
            n = 14
            for i in range(n, 0, -1):
                rr = r * i / n
                e = Ellipse(width=2 * rr + 1e-3, height=2 * rr * k + 1e-3, stroke_width=1.2, color=C_POS, stroke_opacity=0.6)
                e.set_fill(interpolate_color(ManimColor(C_POS), ManimColor(BG), 0.55 * i / n), 0.9)
                g.add(e.move_to([0, cy, 0]))
            return g

        D = always_redraw(disc)

        def Elen():
            r = a.get_value() / sc
            r = r * (1 + 4 * max(a.get_value() - A0, 0) ** 2)  # tamaño físico efectivo al «crecer a infinito»
            return 0.05 + 3.0 * (1 - zP / np.sqrt(r ** 2 + zP ** 2))

        Earr = always_redraw(lambda: Arrow(P, P + UP * Elen(), buff=0, color=YELLOW, stroke_width=8,
                                           max_tip_length_to_length_ratio=0.12))
        pd = glow_dot(P, WHITE, 0.08)
        self.add(D)
        self.play(GrowArrow(zax), FadeIn(pd), run_time=0.5)
        self.add(Earr)
        cap = T("un disco = muchos anillos", 30, WHITE).move_to(UP * 4.4)
        self.play(FadeIn(cap), a.animate.set_value(A0), run_time=2.2, rate_func=smooth)
        f = M(r"\vec E_{\text{disco}}=\frac{\sigma}{2\varepsilon_0}\left(1-\frac{z}{\sqrt{a^2+z^2}}\right)\hat u_z", 52)
        f.move_to(UP * 4.4)
        self.play(FadeOut(cap), Write(f), run_time=1.0)
        self.wait(0.4)
        lim = M(r"a\to\infty", 50, C_PINK).move_to(UP * 2.9)
        self.play(FadeIn(lim), run_time=0.3)
        self.play(a.animate.set_value(6.5), run_time=2.0, rate_func=rush_into)
        f2 = M(r"\vec E_{\text{plano}}=\frac{\sigma}{2\varepsilon_0}\,\frac{z}{|z|}\,\hat u_z", 60, YELLOW).move_to(f)
        self.play(ReplacementTransform(f, f2), run_time=0.8)
        cap2 = T("¡no depende de la distancia!", 30, YELLOW).move_to(UP * 2.9)
        self.play(FadeOut(lim), FadeIn(cap2), run_time=0.4)
        self.wait(0.6)
        # gráfica disco vs plano
        self.remove(Earr, D)
        self.play(FadeOut(VGroup(zax, pd, cap2)), run_time=0.4)
        ax = Axes(x_range=[-5, 5, 1], y_range=[-1.3, 1.3, 1], x_length=8.2, y_length=5.0,
                  axis_config={"color": C_GREY, "include_tip": False}).move_to(DOWN * 1.2)
        xl = M("z/a", 32, C_GREY).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        self.play(Create(ax), FadeIn(xl), run_time=0.5)
        disc_l = ax.plot(lambda z: -1 - z / np.sqrt(1 + z * z), x_range=[-5, -0.001], color=C_NEG, stroke_width=5)
        disc_r = ax.plot(lambda z: 1 - z / np.sqrt(1 + z * z), x_range=[0.001, 5], color=C_NEG, stroke_width=5)
        pl_l = DashedLine(ax.c2p(-5, -1), ax.c2p(0, -1), color=YELLOW)
        pl_r = DashedLine(ax.c2p(0, 1), ax.c2p(5, 1), color=YELLOW)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=C_NEG, stroke_width=5), T("disco", 26)).arrange(RIGHT),
                     VGroup(DashedLine(ORIGIN, RIGHT * 0.5, color=YELLOW), T("plano", 26)).arrange(RIGHT)
                     ).arrange(RIGHT, buff=0.6).next_to(ax, UP, buff=0.2)
        self.play(Create(pl_l), Create(pl_r), Create(disc_l), Create(disc_r), FadeIn(leg), run_time=1.4)
        jump = DoubleArrow(ax.c2p(-0.3, -1), ax.c2p(-0.3, 1), buff=0, color=WHITE, stroke_width=3, tip_length=0.18)
        jl = M(r"\text{salto }\frac{\sigma}{\varepsilon_0}", 40).next_to(jump, LEFT, buff=0.1)
        self.play(GrowFromCenter(jump), FadeIn(jl), run_time=0.6)
        cap3 = T("la condición de contorno, en acción", 28, C_GREY).move_to(DOWN * 4.9)
        self.play(FadeIn(cap3), run_time=0.4)
        self.outro(1.8)


class C12_Lineas(VClip):
    idx = 12
    title = "Líneas de campo y equipotenciales"

    def construct(self):
        self.header()
        c = np.array([0, -0.6, 0])
        box = (4.4, 5.0)
        configs = [
            ("carga puntual", [(1, c)]),
            ("dos cargas iguales", [(1, c + UP * 1.3), (1, c + DOWN * 1.3)]),
            ("dipolo", [(1, c + UP * 1.3), (-1, c + DOWN * 1.3)]),
        ]
        prev = None
        for i, (name, chs) in enumerate(configs):
            fl = field_lines(chs, n_per=18, box=box, center=c, rstart=0.28)
            lv = [0.35, 0.5, 0.7, 1.0, 1.5, 2.3] if all(q > 0 for q, _ in chs) else [-1.5, -0.8, -0.4, -0.15, 0.15, 0.4, 0.8, 1.5]
            if i == 1:
                lv = [0.7, 0.9, 1.1, 1.35, 1.6, 2.0, 3.0]
            eq = equipotentials(chs, lv, box=box, center=c)
            qs = VGroup(*[charge(q, p, 0.24) for q, p in chs])
            lab = T(name, 34, YELLOW).move_to(UP * 5.0)
            if prev is None:
                self.play(FadeIn(qs, scale=0.3), FadeIn(lab), run_time=0.5)
                self.play(LaggedStart(*[Create(x) for x in fl], lag_ratio=0.02), run_time=1.2)
                self.play(LaggedStart(*[Create(x) for x in eq], lag_ratio=0.05), run_time=1.0)
            else:
                pfl, peq, pqs, plab = prev
                self.play(ReplacementTransform(pqs, qs), ReplacementTransform(pfl, fl), ReplacementTransform(peq, eq),
                          ReplacementTransform(plab, lab), run_time=1.6)
            self.bring_to_front(qs)
            flashes = [ShowPassingFlash(x.copy().set_stroke(YELLOW, 4), time_width=0.35) for x in fl]
            self.play(LaggedStart(*flashes, lag_ratio=0.01), run_time=1.6)
            self.wait(0.5)
            prev = (fl, eq, qs, lab)
        props = VGroup(T("· nunca se cortan", 28), T("· salen de + y acaban en −", 28),
                       T("· perpendiculares a las equipotenciales", 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        props.move_to(DOWN * 6.0)
        bg = BackgroundRectangle(props, fill_color=BG, fill_opacity=0.9, buff=0.2)
        self.play(FadeIn(bg), LaggedStart(*[FadeIn(p, shift=0.2 * UP) for p in props], lag_ratio=0.3), run_time=1.2)
        self.outro(1.8)
