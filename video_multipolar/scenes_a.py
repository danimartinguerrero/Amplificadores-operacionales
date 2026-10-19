from common import *


class S01_Intro(VScene):
    def construct(self):
        title = T("Desarrollo multipolar", 72)
        sub = T("Electromagnetismo I  ·  Tema 2", 30, C_GREY).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.6)
        self.play(FadeIn(sub, shift=0.2 * UP))
        self.wait(1.2)
        self.play(FadeOut(title), FadeOut(sub))

        # (a) la nube de carga y el punto P
        bc = np.array([-3.2, -0.6, 0])
        blob = make_blob(bc, 1.5, seed=3)
        rho = MathTex(r"\rho(\vec r\,')", font_size=40, color=C_POS).next_to(blob, DOWN, buff=0.3)
        P = Dot([4.2, 1.6, 0], color=C_R, radius=0.08)
        Plab = MathTex("P", color=C_R).next_to(P, UR, buff=0.1)
        self.say("a")
        self.play(DrawBorderThenFill(blob[0]), run_time=1.5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in blob[1]], lag_ratio=0.01), run_time=2)
        self.play(Write(rho))
        self.play(FadeIn(P, scale=3), Write(Plab))

        # (b) cada trocito contribuye; integramos
        self.say("b")
        idx = np.random.default_rng(1).choice(len(blob[1]), 18, replace=False)
        srcs = [blob[1][i] for i in idx]
        lines = VGroup(*[
            always_redraw(lambda s=s: Line(s.get_center(), P.get_center(), stroke_width=1.3,
                                           color=C_RR, stroke_opacity=0.55))
            for s in srcs])
        for s in srcs:
            s.set_color(WHITE)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.08), run_time=2.5)
        integral = MathTex(r"\phi(\vec r)", "=", r"\frac{1}{4\pi\varepsilon_0}",
                           r"\int_{V'}", r"\frac{\rho(\vec r\,')}{\|\vec r-\vec r\,'\|}", r"\,\mathrm dV'",
                           font_size=46).to_edge(UP, buff=0.5)
        integral[0].set_color(C_R)
        integral[4].set_color(C_POS)
        self.play(Write(integral), run_time=2.5)

        # (c) hay que rehacerla para cada P
        self.say("c")
        self.play(Indicate(integral[4], color=C_RR))
        path = [np.array(p) for p in ([4.8, -2.4, 0], [1.5, 2.6, 0], [5.6, 0.2, 0], [4.2, 1.6, 0])]
        for p in path:
            self.play(P.animate.move_to(p), Plab.animate.next_to(p, UR, buff=0.1),
                      run_time=1.1, rate_func=smooth)
        q = T("¿una integral distinta para cada P?", 30, C_GREY).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(q, shift=0.2 * UP))

        # (d) desde lejos: una carga puntual
        self.say("d")
        self.play(FadeOut(lines), FadeOut(q), FadeOut(rho), run_time=0.8)
        for s in srcs:
            s.set_color(C_POS)
        pt = charge(1, bc, 0.16)
        Qlab = MathTex("Q", color=C_POS, font_size=40).next_to(pt, DOWN, buff=0.2)
        self.play(blob.animate.scale(0.12).set_opacity(0.0), FadeIn(pt, scale=0.2), run_time=2.2)
        self.play(Write(Qlab))
        far = MathTex(r"\phi(\vec r)", r"\approx", r"\frac{Q}{4\pi\varepsilon_0\, r}", font_size=46)
        far[0].set_color(C_R)
        far.move_to([3.4, -2.4, 0])
        self.play(Write(far))
        rline = DashedLine(pt.get_center(), P.get_center(), color=C_GREY)
        rlab = MathTex("r", color=C_GREY).next_to(rline.get_center(), UP, buff=0.15)
        self.play(Create(rline), FadeIn(rlab))

        # (e) entre ambos extremos
        self.say("e")
        self.play(FadeOut(VGroup(pt, Qlab, rline, rlab, P, Plab, far, blob)), integral.animate.scale(0.8).to_edge(UP, buff=0.4))
        left = T("conocer ρ punto a punto", 28, C_GREY)
        right = T("verla como un punto", 28, C_GREY)
        bar = Line(LEFT * 4.3, RIGHT * 4.3, color=C_GREY)
        left.next_to(bar.get_start(), DOWN, buff=0.3)
        right.next_to(bar.get_end(), DOWN, buff=0.3)
        self.play(Create(bar), FadeIn(left), FadeIn(right))
        moms = VGroup(MathTex("Q", color=C_POS), MathTex(r"\vec p", color=L_COLORS[1]),
                      MathTex(r"Q_{jk}", color=L_COLORS[3]), MathTex(r"\cdots")).scale(1.4).arrange(RIGHT, buff=0.8)
        moms.next_to(bar, UP, buff=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=0.3 * DOWN) for m in moms], lag_ratio=0.35), run_time=2.5)
        sub = T("unos pocos números, calculados una sola vez", 30).next_to(bar, DOWN, buff=1.3)
        self.play(Write(sub), run_time=1.5)
        self.wait(max(self.remaining() - 3.2, 0))
        name = T("Desarrollo multipolar", 60, YELLOW).move_to(DOWN * 0.2)
        self.play(FadeOut(VGroup(bar, left, right, sub, integral)), moms.animate.next_to(name, UP, buff=0.8),
                  FadeIn(name, scale=1.1), run_time=1.5)
        self.end(1.0)
        self.clear()


class S02_Geometria(VScene):
    def construct(self):
        lab = section_label("1", "Geometría")
        self.add(lab)
        O = np.array([-5.6, -2.7, 0])
        blob = make_blob(O + np.array([0.5, 1.0, 0]), 1.45, seed=5, n_dots=90)
        S = O + np.array([0.45, 2.1, 0])
        Pp = np.array([-0.4, 0.5, 0])
        odot = Dot(O, color=WHITE)
        olab = MathTex("O").next_to(odot, DL, buff=0.1)
        sdot = Square(0.16, color=WHITE, fill_opacity=0.9, fill_color=C_POS).move_to(S)
        dq = MathTex(r"\mathrm dq", font_size=32).next_to(sdot, UL, buff=0.08)
        pdot = Dot(Pp, color=C_R, radius=0.08)
        plab = MathTex("P", color=C_R).next_to(pdot, UR, buff=0.1)
        vrp = Arrow(O, S, buff=0, color=C_RP, stroke_width=5, max_tip_length_to_length_ratio=0.12)
        vr = Arrow(O, Pp, buff=0, color=C_R, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        vR = Arrow(S, Pp, buff=0, color=C_RR, stroke_width=5, max_tip_length_to_length_ratio=0.1)
        lrp = MathTex(r"\vec r\,'", color=C_RP).next_to(vrp.get_center(), LEFT, buff=0.15)
        lr = MathTex(r"\vec r", color=C_R).next_to(vr.get_center(), DOWN, buff=0.2)
        lR = MathTex(r"\vec R=\vec r-\vec r\,'", color=C_RR, font_size=36).next_to(vR.get_center(), UP, buff=0.25).shift(RIGHT * 0.4)
        a1 = np.arctan2(*(Pp - O)[1::-1])
        a2 = np.arctan2(*(S - O)[1::-1])
        arc = Arc(radius=0.8, start_angle=a1, angle=a2 - a1, arc_center=O, color=WHITE)
        th = MathTex(r"\theta'", font_size=34).move_to(O + 1.15 * np.array([np.cos((a1 + a2) / 2), np.sin((a1 + a2) / 2), 0]))

        self.say("a")
        self.play(FadeIn(blob), FadeIn(odot), Write(olab))
        self.play(FadeIn(sdot, scale=2), Write(dq))
        self.play(GrowArrow(vrp), Write(lrp))
        self.play(FadeIn(pdot, scale=2), Write(plab))
        self.play(GrowArrow(vr), Write(lr))
        self.play(Create(arc), Write(th))

        self.say("b")
        self.play(GrowArrow(vR), Write(lR))
        eq1 = MathTex(r"R^2", "=", r"r^2", "+", r"r'^2", "-", r"2rr'\cos\theta'", font_size=48)
        eq1.move_to([3.6, 2.0, 0])
        eq1[0].set_color(C_RR); eq1[2].set_color(C_R); eq1[4].set_color(C_RP)
        self.play(Write(eq1), run_time=2.5)
        self.play(Indicate(VGroup(arc, th)), Indicate(eq1[6]))

        self.say("c")
        eq2 = MathTex(r"\frac{1}{R}", "=", r"\frac{1}{r}", r"\Big(1-2", r"t", r"\cos\theta'+", r"t", r"^2\Big)^{-1/2}",
                      font_size=48).next_to(eq1, DOWN, buff=0.9)
        eq2[0].set_color(C_RR); eq2[4].set_color(YELLOW); eq2[6].set_color(YELLOW)
        self.play(TransformMatchingShapes(eq1.copy(), eq2), run_time=2)
        tdef = MathTex(r"t", "=", r"\frac{r'}{r}", r"\ll 1", font_size=48).next_to(eq2, DOWN, buff=0.8)
        tdef[0].set_color(YELLOW)
        box = SurroundingRectangle(tdef, color=YELLOW, buff=0.2)
        self.play(Write(tdef[:3]))
        self.play(Write(tdef[3]), Create(box))
        self.end()
        self.clear()


def legendre(l):
    return np.polynomial.legendre.Legendre.basis(l)


class S03_Legendre(VScene):
    def construct(self):
        lab = section_label("2", "Polinomios de Legendre")
        self.add(lab)
        self.say("a")
        g = MathTex(r"g(x,t)", "=", r"\frac{1}{\sqrt{1-2xt+t^2}}", font_size=52).move_to(UP * 1.8)
        self.play(Write(g), run_time=2)
        ser = MathTex("=", r"P_0(x)", "+", r"P_1(x)", r"\,t", "+", r"P_2(x)", r"\,t^2", "+",
                      r"P_3(x)", r"\,t^3", r"+\cdots", font_size=48)
        ser.next_to(g, DOWN, buff=0.7).align_to(g[1], LEFT).shift(LEFT * 1.5)
        for i, k in [(1, 0), (3, 1), (6, 2), (9, 3)]:
            ser[i].set_color(L_COLORS[k])
        self.play(Write(ser), run_time=3)

        self.say("b")
        polys = VGroup(
            MathTex(r"P_0(x)=1"), MathTex(r"P_1(x)=x"),
            MathTex(r"P_2(x)=\tfrac12(3x^2-1)"), MathTex(r"P_3(x)=\tfrac12(5x^3-3x)"),
            MathTex(r"P_4(x)=\tfrac18(35x^4-30x^2+3)"),
        ).scale(0.85).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        for k, p in enumerate(polys):
            p.set_color(L_COLORS[k])
        polys.to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        ax = Axes(x_range=[-1, 1, 0.5], y_range=[-1.25, 1.25, 0.5], x_length=5.6, y_length=4.6,
                  axis_config={"color": C_GREY, "include_tip": False},
                  x_axis_config={"numbers_to_include": [-1, 1], "font_size": 26, "decimal_number_config": {"num_decimal_places": 0}},
                  y_axis_config={"numbers_to_include": [-1, 1], "font_size": 26, "decimal_number_config": {"num_decimal_places": 0}})
        ax.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.4)
        curves = VGroup(*[ax.plot(lambda x, k=k: legendre(k)(x), color=L_COLORS[k], stroke_width=3.5)
                          for k in range(5)])
        self.play(FadeOut(g), FadeOut(ser), Create(ax))
        for k in range(5):
            self.play(Write(polys[k]), Create(curves[k]), run_time=1.1)
        self.sync()

        self.say("c")
        band = Rectangle(width=ax.x_length, height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1],
                         stroke_width=0, fill_color=YELLOW, fill_opacity=0.1).move_to(ax.c2p(0, 0))
        dl = VGroup(DashedLine(ax.c2p(-1, 1), ax.c2p(1, 1), color=YELLOW),
                    DashedLine(ax.c2p(-1, -1), ax.c2p(1, -1), color=YELLOW))
        bound = MathTex(r"|P_\ell(x)|\le 1", color=YELLOW, font_size=44).next_to(ax, UP, buff=0.2)
        self.play(FadeIn(band), Create(dl), Write(bound))
        ends = VGroup(*[Dot(ax.c2p(s, legendre(k)(s)), radius=0.07, color=WHITE)
                        for k in range(5) for s in (-1, 1)])
        self.play(LaggedStart(*[Flash(d, color=YELLOW, flash_radius=0.25) for d in ends], lag_ratio=0.1), FadeIn(ends))

        self.say("d")
        self.play(FadeOut(VGroup(polys, ax, curves, band, dl, bound, ends)))
        thm = MathTex(r"\frac{1}{\|\vec r-\vec r\,'\|}", "=", r"\sum_{\ell=0}^{\infty}",
                      r"\frac{r'^{\,\ell}}{r^{\ell+1}}", r"P_\ell(\cos\theta')", font_size=60)
        thm[0].set_color(C_RR); thm[3].set_color(YELLOW); thm[4].set_color(L_COLORS[1])
        cond = T("válido si r' < r", 28, C_GREY).next_to(thm, DOWN, buff=0.5)
        self.play(Write(thm), run_time=3)
        box = SurroundingRectangle(thm, color=YELLOW, buff=0.25)
        self.play(Create(box), FadeIn(cond))
        self.sync()

        self.say("e")
        self.play(VGroup(thm, box).animate.scale(0.6).to_corner(UR, buff=0.4), FadeOut(cond))
        ax2 = Axes(x_range=[0, TAU, PI / 2], y_range=[0.2, 0.55, 0.1], x_length=10, y_length=4.6,
                   axis_config={"color": C_GREY, "include_tip": False},
                   y_axis_config={"numbers_to_include": [0.3, 0.4, 0.5], "font_size": 24,
                                  "decimal_number_config": {"num_decimal_places": 1}})
        ax2.move_to(DOWN * 0.7)
        xl = VGroup(*[MathTex(s, font_size=30).next_to(ax2.c2p(v, 0.2), DOWN, buff=0.2)
                      for s, v in [(r"\pi/2", PI / 2), (r"\pi", PI), (r"3\pi/2", 3 * PI / 2), (r"2\pi", TAU)]])
        xlab = MathTex(r"\theta'", font_size=36).next_to(ax2.c2p(TAU, 0.2), RIGHT, buff=0.3)
        ratio = MathTex(r"\frac{r'}{r}=\frac13", font_size=40).to_corner(UL, buff=0.4).shift(DOWN * 0.7)
        exact = ax2.plot(lambda x: (10 - 6 * np.cos(x)) ** -0.5, color=WHITE, stroke_width=9, stroke_opacity=0.35)
        elab = T("exacta", 26, C_GREY).next_to(ax2.c2p(PI, 1 / 4), DOWN, buff=0.35)
        self.play(Create(ax2), FadeIn(xl), FadeIn(xlab), Write(ratio))
        self.play(Create(exact), FadeIn(elab), run_time=1.5)

        def partial(n):
            return ax2.plot(lambda x: sum((1 / 3) ** l / 3 * legendre(l)(np.cos(x)) for l in range(n + 1)),
                            color=L_COLORS[n], stroke_width=4)
        lbl = lambda n: MathTex(rf"\sum_{{\ell\le {n}}}", font_size=40, color=L_COLORS[n]).next_to(ax2, UP, buff=0.1)
        cur = partial(0)
        cl = lbl(0)
        self.play(Create(cur), Write(cl))
        self.wait(1.4)
        for n in (1, 2, 3):
            self.play(Transform(cur, partial(n)), Transform(cl, lbl(n)), run_time=1.5)
            self.wait(1.0)
        self.end()
        self.clear()
