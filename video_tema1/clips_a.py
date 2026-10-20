from common_v import *


class C01_AnguloSolido(VClip):
    idx = 1
    title = "¿Qué es un ángulo sólido?"

    def construct(self):
        self.header()
        O = np.array([0, -3.4, 0])
        r1, r2 = 1.6, 3.5
        s1 = Circle(r1, color=C_NEG, stroke_width=2).move_to(O).set_fill(C_NEG, 0.08)
        s2 = Circle(r2, color=C_NEG, stroke_width=2, stroke_opacity=0.7).move_to(O).set_fill(C_NEG, 0.04)
        od = glow_dot(O, WHITE, 0.06)
        ol = M("O", 36).next_to(O, DL, buff=0.12)
        half = ValueTracker(0.2)
        mid = ValueTracker(PI / 2)

        def a0():
            return mid.get_value() - half.get_value()

        cone = always_redraw(lambda: Sector(radius=r2 + 0.7, start_angle=a0(), angle=2 * half.get_value(),
                                            arc_center=O, fill_color=YELLOW, fill_opacity=0.16, stroke_width=0))
        edges = always_redraw(lambda: VGroup(*[
            Line(O, O + (r2 + 0.7) * np.array([np.cos(a), np.sin(a), 0]), color=YELLOW, stroke_width=2, stroke_opacity=0.8)
            for a in (a0(), a0() + 2 * half.get_value())]))
        arc1 = always_redraw(lambda: Arc(radius=r1, start_angle=a0(), angle=2 * half.get_value(), arc_center=O,
                                         color=C_GOLD, stroke_width=9))
        arc2 = always_redraw(lambda: Arc(radius=r2, start_angle=a0(), angle=2 * half.get_value(), arc_center=O,
                                         color=ORANGE, stroke_width=9))
        l1 = always_redraw(lambda: M(r"\mathrm dS_1", 32, C_GOLD).move_to(
            O + (r1 - 0.45) * np.array([np.cos(mid.get_value()), np.sin(mid.get_value()), 0])))
        l2 = always_redraw(lambda: M(r"\mathrm dS_2", 34, ORANGE).move_to(
            O + (r2 + 0.45) * np.array([np.cos(mid.get_value()), np.sin(mid.get_value()), 0])))
        rl1 = VGroup(Line(O, O + r1 * np.array([np.cos(3.6), np.sin(3.6), 0]), color=C_GREY),
                     M("r_1", 30, C_GREY).move_to(O + 0.9 * np.array([np.cos(3.4), np.sin(3.4), 0])))
        rl2 = VGroup(Line(O, O + r2 * np.array([np.cos(3.9), np.sin(3.9), 0]), color=C_GREY),
                     M("r_2", 30, C_GREY).move_to(O + 2.6 * np.array([np.cos(3.78), np.sin(3.78), 0])))

        self.play(Create(s1), Create(s2), FadeIn(od), FadeIn(ol), run_time=0.8)
        self.play(FadeIn(cone), Create(edges), Create(arc1), Create(arc2), FadeIn(l1), FadeIn(l2),
                  FadeIn(rl1), FadeIn(rl2), run_time=0.9)
        f1 = M(r"\mathrm d\Omega", 64, YELLOW)
        f2 = M(r"=\frac{\mathrm dS_1}{r_1^2}=\frac{\mathrm dS_2}{r_2^2}", 64)
        f2[0][1:5].set_color(C_GOLD)
        f2[0][9:13].set_color(ORANGE)
        form = VGroup(f1, f2).arrange(RIGHT, buff=0.15).move_to(UP * 3.9)
        self.play(Write(form), run_time=1.0)
        cap = T("el mismo para todas las esferas", 30, C_GREY).next_to(form, DOWN, buff=0.35)
        self.play(FadeIn(cap, shift=0.2 * UP), half.animate.set_value(0.42), run_time=1.0)
        self.play(mid.animate.set_value(PI / 2 + 0.55), half.animate.set_value(0.14), run_time=1.0)
        self.play(mid.animate.set_value(PI / 2 - 0.45), half.animate.set_value(0.3), run_time=1.0)
        self.play(mid.animate.set_value(PI / 2), half.animate.set_value(0.25), run_time=0.7)
        # toda la esfera
        full = M(r"\Omega_{\text{total}}=\frac{4\pi r^2}{r^2}=4\pi\ \text{sr}", 54, YELLOW).move_to(cap)
        self.play(FadeOut(cap), FadeOut(rl1), FadeOut(rl2), FadeOut(l1), FadeOut(l2), run_time=0.4)
        self.play(half.animate.set_value(PI), FadeOut(edges), run_time=1.6, rate_func=smooth)
        self.play(Write(full), run_time=0.8)
        self.wait(0.6)
        # elemento inclinado
        self.play(FadeOut(VGroup(cone, arc1, arc2, s2, full)), half.animate.set_value(0.25), run_time=0.6)
        th = 0.75
        R = 3.0
        Pm = O + R * UP
        u = rotate_vector(RIGHT, th)
        nvec = rotate_vector(UP, th)
        dS = Line(Pm - 1.1 * u, Pm + 1.1 * u, color=C_PINK, stroke_width=10)
        na = Arrow(Pm, Pm + 1.8 * nvec, buff=0, color=C_PINK, stroke_width=5)
        nl = M(r"\mathrm d\vec S", 40, C_PINK).next_to(na.get_end(), RIGHT, buff=0.08)
        ur = DashedLine(Pm, Pm + 1.3 * UP, color=WHITE)
        ang = Angle(Line(Pm, Pm + UP), Line(Pm, Pm + nvec), radius=0.6, other_angle=True, color=WHITE)
        tl = M(r"\theta", 32).move_to(Pm + 0.85 * rotate_vector(UP, th / 2))
        hw = 1.1 * np.cos(th) / R
        proj = Arc(radius=R, start_angle=PI / 2 - hw, angle=2 * hw, arc_center=O, color=YELLOW, stroke_width=9)
        rays = VGroup(*[DashedLine(O, O + 3.6 * np.array([np.cos(a), np.sin(a), 0]), color=YELLOW, stroke_width=2)
                        for a in (PI / 2 - hw, PI / 2 + hw)])
        Rl = VGroup(Line(O, Pm, color=C_GREY), M("R", 32, C_GREY).next_to(O + 1.5 * UP, LEFT, buff=0.1))
        self.play(Create(dS), GrowArrow(na), FadeIn(nl), Create(Rl), run_time=0.8)
        self.play(Create(ur), Create(ang), FadeIn(tl), Create(rays), Create(proj), run_time=0.8)
        g = M(r"\mathrm d\Omega=\frac{\mathrm dS\cos\theta}{R^2}=\frac{\mathrm d\vec S\cdot\hat u_R}{R^2}", 58)
        g.move_to(UP * 3.9)
        self.play(ReplacementTransform(form, g), run_time=0.9)
        box = SurroundingRectangle(g, color=YELLOW, buff=0.2)
        self.play(Create(box), Indicate(proj, color=YELLOW), run_time=0.8)
        self.outro(2.4)


class C02_AnguloTotal(VClip):
    idx = 2
    title = "∮ dΩ: 4π dentro, 0 fuera"

    def construct(self):
        self.header()
        c = np.array([0, -0.6, 0])
        pts = blob_pts(c, 2.6, seed=4, dent=0.55)
        S = smooth_closed(pts, color=C_NEG, stroke_width=3).set_fill(C_NEG, 0.1)
        Sl = M("S", 40, C_NEG).move_to(c + np.array([2.4, -2.4, 0]))
        Op = c + np.array([-0.3, -0.4, 0])
        O = Dot(Op, color=WHITE, radius=0.09)
        self.play(DrawBorderThenFill(S), FadeIn(Sl), FadeIn(O), run_time=0.9)
        ang = ValueTracker(0.0)
        dense = S.copy().set_points_smoothly([*pts, pts[0]])
        poly = np.array([dense.point_from_proportion(k / 600) for k in range(600)])

        def ray_group(Opos, a, length=6.5):
            d = np.array([np.cos(a), np.sin(a), 0])
            ray = Line(Opos, Opos + length * d, color=YELLOW, stroke_width=3)
            g = VGroup(ray)
            for i, t in enumerate(ray_hits(Opos, d, poly)):
                p = Opos + t * d
                # salida (+) o entrada (-) según la paridad del cruce
                inside = len(ray_hits(Opos, d, poly)) % 2 == 1
                exit_ = (i % 2 == 0) if inside else (i % 2 == 1)
                col = C_POS if exit_ else C_NEG
                g.add(Dot(p, radius=0.11, color=col))
                g.add(M("+" if exit_ else "-", 34, col).next_to(p, rotate_vector(d, PI / 2), buff=0.12))
            return g

        sweep = always_redraw(lambda: Intersection(
            Sector(radius=6.5, start_angle=0, angle=max(ang.get_value(), 1e-3), arc_center=O.get_center()), S,
            fill_color=YELLOW, fill_opacity=0.25, stroke_width=0))
        ray = always_redraw(lambda: ray_group(O.get_center(), ang.get_value()))
        num = DecimalNumber(0, num_decimal_places=2, font_size=60, color=YELLOW)
        lab = VGroup(M(r"\oint_S \mathrm d\Omega=", 60), num, M(r"\pi", 60, YELLOW)).arrange(RIGHT, buff=0.12)
        lab.move_to(UP * 4.3)
        num.add_updater(lambda m: m.set_value(4 * ang.get_value() / TAU))
        self.add(sweep)
        self.play(FadeIn(ray), Write(lab), run_time=0.6)
        cap = T("dentro: cada dirección sale una vez más de las que entra", 26, C_GREY).next_to(lab, DOWN, buff=0.3)
        self.play(FadeIn(cap), ang.animate.set_value(TAU), run_time=5.0, rate_func=linear)
        num.clear_updaters()
        self.play(Flash(lab, color=YELLOW, flash_radius=1.6), run_time=0.6)
        # punto fuera
        self.remove(sweep)
        self.play(FadeOut(cap), FadeOut(ray), run_time=0.3)
        Oout = c + np.array([-3.4, 4.0, 0])
        self.play(O.animate.move_to(Oout), run_time=0.8)
        dirc = c - Oout
        a_mid = np.arctan2(dirc[1], dirc[0])
        ang.set_value(a_mid - 0.42)
        num.set_value(0)
        ray2 = always_redraw(lambda: ray_group(O.get_center(), ang.get_value(), 9))
        cap2 = T("fuera: cada entrada (−dΩ) tiene su salida (+dΩ)", 26, C_GREY).next_to(lab, DOWN, buff=0.3)
        self.play(FadeIn(ray2), FadeIn(cap2), run_time=0.4)
        self.play(ang.animate.set_value(a_mid + 0.42), run_time=3.2, rate_func=there_and_back_with_pause)
        self.play(FadeOut(ray2), FadeOut(cap2), run_time=0.3)
        res = M(r"\oint_S \mathrm d\Omega=\begin{cases}4\pi & O\ \text{dentro}\\ 0 & O\ \text{fuera}\end{cases}", 58)
        res.move_to(lab).shift(DOWN * 0.3)
        box = SurroundingRectangle(res, color=YELLOW, buff=0.2)
        self.play(ReplacementTransform(lab, res), Create(box), run_time=1.0)
        self.outro(2.4)


class C03_Gauss(VClip):
    idx = 3
    title = "La ley de Gauss en 30 segundos"

    def construct(self):
        self.header()
        e1 = M(r"\vec E\cdot\mathrm d\vec S=\frac{q}{4\pi\varepsilon_0}\,\frac{\hat u_R\cdot\mathrm d\vec S}{R^2}", 50)
        e1.move_to(UP * 4.6)
        e2 = M(r"=\frac{q}{4\pi\varepsilon_0}\,\mathrm d\Omega", 50).next_to(e1, DOWN, buff=0.3)
        e2[0][-2:].set_color(YELLOW)
        self.play(Write(e1), run_time=1.0)
        self.play(Write(e2), run_time=0.7)
        c = np.array([0, -1.2, 0])
        q = charge(1, c, 0.24)
        N = 20
        dirs = [np.array([np.cos(TAU * k / N + 0.1), np.sin(TAU * k / N + 0.1), 0]) for k in range(N)]
        lines = VGroup(*[Line(c + 0.3 * d, c + 4.6 * d, color=WHITE, stroke_width=2.2, stroke_opacity=0.85) for d in dirs])
        tips = VGroup(*[Triangle(fill_opacity=1, stroke_width=0, color=WHITE).scale(0.08)
                        .rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(c + 3.9 * d) for d in dirs])
        self.play(FadeIn(q, scale=0.3), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.03), run_time=0.9)
        self.add(tips)
        shapes = [blob_pts(c, 2.0, seed=s, dent=dd) for s, dd in [(1, 0), (6, 0.3), (9, 0.1), (2, 0.25)]]
        shapes[1] = shapes[1] * np.array([1.25, 0.8, 1]) + np.array([0, -1.2 * 0.2, 0])
        S = smooth_closed(shapes[0], color=C_NEG, stroke_width=3).set_fill(C_NEG, 0.1)

        def hits():
            poly = np.array([S.point_from_proportion(k / 300) for k in range(300)])
            g = VGroup()
            for d in dirs:
                for t in ray_hits(c, d, poly):
                    g.add(Dot(c + t * d, radius=0.07, color=YELLOW))
            return g

        dots = always_redraw(hits)
        self.play(DrawBorderThenFill(S), run_time=0.7)
        self.add(dots)
        flux = M(r"\Phi_E=\frac{q}{4\pi\varepsilon_0}\cdot 4\pi=\frac{q}{\varepsilon_0}", 56, YELLOW).move_to(DOWN * 5.6)
        fbg = BackgroundRectangle(flux, fill_color=BG, fill_opacity=0.9, buff=0.15)
        self.play(FadeIn(fbg), Write(flux), run_time=0.9)
        for sh in shapes[1:]:
            new = smooth_closed(sh, color=C_NEG, stroke_width=3).set_fill(C_NEG, 0.1)
            self.play(Transform(S, new), run_time=1.0)
        self.play(Indicate(flux, color=YELLOW), run_time=0.6)
        # carga exterior
        c2 = np.array([3.0, 2.3, 0])
        q2 = charge(1, c2, 0.2)
        dirs2 = [rotate_vector(normalize(c - c2), a) for a in np.linspace(-0.55, 0.55, 7)]
        ext = VGroup(*[Line(c2 + 0.25 * d, c2 + 7.5 * d, color=C_GOLD, stroke_width=2) for d in dirs2])

        def hits2():
            poly = np.array([S.point_from_proportion(k / 300) for k in range(300)])
            g = VGroup()
            for d in dirs2:
                ts = ray_hits(c2, d, poly)
                for i, t in enumerate(ts):
                    g.add(Dot(c2 + t * d, radius=0.09, color=C_NEG if i % 2 == 0 else C_POS))
            return g

        self.play(FadeIn(q2, scale=0.3), LaggedStart(*[Create(l) for l in ext], lag_ratio=0.05), run_time=0.8)
        d2 = always_redraw(hits2)
        self.add(d2)
        cap = T("las de fuera entran y salen: aportan 0", 28, C_GOLD).move_to(DOWN * 4.2)
        cap = VGroup(BackgroundRectangle(cap, fill_color=BG, fill_opacity=0.9, buff=0.12), cap)
        self.play(FadeIn(cap), run_time=0.4)
        self.play(q2.animate.shift(LEFT * 0.8 + DOWN * 0.3), *[l.animate.shift(LEFT * 0.8 + DOWN * 0.3) for l in ext],
                  run_time=1.0)
        self.wait(0.4)
        dots.clear_updaters(); d2.clear_updaters()
        law = M(r"\oint_S\vec E\cdot\mathrm d\vec S=\frac{Q_{\text{enc}}}{\varepsilon_0}", 70)
        law.move_to(DOWN * 5.0)
        box = SurroundingRectangle(law, color=YELLOW, buff=0.25)
        lbg = BackgroundRectangle(box, fill_color=BG, fill_opacity=0.92, buff=0.05)
        self.play(FadeOut(cap), FadeIn(lbg), ReplacementTransform(flux, law), run_time=0.9)
        self.play(Create(box), run_time=0.5)
        self.outro(2.4)


class C04_Delta(VClip):
    idx = 4
    title = "La delta de Dirac"

    def construct(self):
        self.header()
        ax = Axes(x_range=[-1.6, 1.6, 0.5], y_range=[0, 6.5, 1], x_length=8, y_length=6.2,
                  axis_config={"color": C_GREY, "include_tip": False}).move_to(DOWN * 0.6)
        xl = M("x", 34, C_GREY).next_to(ax.x_axis.get_end(), DOWN, buff=0.15)
        self.play(Create(ax), FadeIn(xl), run_time=0.6)
        al = ValueTracker(1.0)

        def pulse():
            a = al.get_value()
            w = 1 / a
            p = Polygon(ax.c2p(-w / 2, 0), ax.c2p(-w / 2, a), ax.c2p(w / 2, a), ax.c2p(w / 2, 0),
                        color=YELLOW, stroke_width=3)
            p.set_fill(YELLOW, 0.3)
            return p

        P = always_redraw(pulse)
        area = M(r"\text{área}=1", 46, YELLOW).move_to(UP * 4.3 + LEFT * 2.0)
        an = DecimalNumber(1, num_decimal_places=1, font_size=46)
        alab = VGroup(M(r"\alpha=", 46), an).arrange(RIGHT, buff=0.1).move_to(UP * 4.3 + RIGHT * 2.2)
        an.add_updater(lambda m: m.set_value(al.get_value()))
        self.play(FadeIn(P), FadeIn(area), FadeIn(alab), run_time=0.5)
        self.play(al.animate.set_value(6.0), run_time=2.4, rate_func=smooth)
        # gaussianas
        sg = ValueTracker(0.6)
        G = always_redraw(lambda: ax.plot(lambda x: np.exp(-x ** 2 / (2 * sg.get_value() ** 2)) / (sg.get_value() * np.sqrt(TAU)),
                                          x_range=[-1.6, 1.6, 0.004], color=C_PINK, stroke_width=4))
        Gf = always_redraw(lambda: ax.get_area(G, x_range=[-1.6, 1.6], color=C_PINK, opacity=0.25))
        self.play(FadeOut(P), FadeIn(G), FadeIn(Gf), al.animate.set_value(0.6), run_time=0.6)
        an.clear_updaters()
        sl = M(r"\sigma\to0", 46, C_PINK).move_to(alab)
        self.play(FadeOut(alab), FadeIn(sl), sg.animate.set_value(0.065), run_time=2.0)
        spike = Arrow(ax.c2p(0, 0), ax.c2p(0, 6.4), buff=0, color=YELLOW, stroke_width=7, max_tip_length_to_length_ratio=0.06)
        self.play(FadeOut(G), FadeOut(Gf), GrowArrow(spike), run_time=0.6)
        d = M(r"\delta(x)=\begin{cases}0 & x\neq0\\ \infty & x=0\end{cases}\qquad\int\!\delta\,\mathrm dx=1", 46)
        d.move_to(UP * 4.3)
        self.play(FadeOut(area), FadeOut(sl), Write(d), run_time=1.0)
        self.wait(0.6)
        # propiedad de muestreo
        f = lambda x: 2.6 + 1.1 * np.sin(2.4 * x) + 0.5 * x
        fc = ax.plot(f, x_range=[-1.6, 1.6], color=C_NEG, stroke_width=4)
        fl = M("f(x)", 36, C_NEG).next_to(ax.c2p(1.6, f(1.6)), UP, buff=0.1).shift(LEFT * 0.4)
        a = ValueTracker(0.0)
        spike2 = always_redraw(lambda: Arrow(ax.c2p(a.get_value(), 0), ax.c2p(a.get_value(), 6.4), buff=0,
                                             color=YELLOW, stroke_width=6, max_tip_length_to_length_ratio=0.06))
        pt = always_redraw(lambda: glow_dot(ax.c2p(a.get_value(), f(a.get_value())), WHITE, 0.08))
        self.remove(spike)
        self.add(spike2)
        self.play(Create(fc), FadeIn(fl), FadeIn(pt), run_time=0.7)
        val = DecimalNumber(f(0), num_decimal_places=2, font_size=52, color=YELLOW)
        samp = VGroup(M(r"\int f(x)\,\delta(x-a)\,\mathrm dx=f(a)=", 52), val).arrange(RIGHT, buff=0.12)
        if samp.width > 8.6:
            samp.scale_to_fit_width(8.6)
        samp.move_to(DOWN * 5.0)
        val.add_updater(lambda m: m.set_value(f(a.get_value())))
        self.play(Write(samp), run_time=0.9)
        self.play(a.animate.set_value(1.1), run_time=1.3)
        self.play(a.animate.set_value(-1.2), run_time=1.6)
        self.play(a.animate.set_value(0.4), run_time=1.0)
        val.clear_updaters()
        box = SurroundingRectangle(samp, color=YELLOW, buff=0.2)
        self.play(Create(box), run_time=0.5)
        self.outro(1.6)


class C05_DivDelta(VClip):
    idx = 5
    title = "¿De dónde sale el flujo? ∇·E"

    def construct(self):
        self.header()
        c = np.array([0, -0.4, 0])
        q = charge(1, c, 0.24)
        N = 40
        dirs = [np.array([np.cos(TAU * k / N), np.sin(TAU * k / N), 0]) for k in range(N)]
        lines = VGroup(*[Line(c + 0.3 * d, c + 6.5 * d, color=WHITE, stroke_width=1.6, stroke_opacity=0.55) for d in dirs])
        self.play(FadeIn(q, scale=0.3), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.01), run_time=0.8)
        box_c = ValueTracker(0)
        path = [c + np.array([2.2, 1.8, 0]), c + np.array([-2.0, 2.4, 0]), c + np.array([-1.8, -2.2, 0]), c]

        sq = Square(1.5, color=YELLOW, stroke_width=4).move_to(path[0]).set_fill(YELLOW, 0.08)

        def marks():
            poly = [sq.get_corner(UL), sq.get_corner(UR), sq.get_corner(DR), sq.get_corner(DL)]
            poly = np.array(poly)
            g = VGroup()
            for d in dirs:
                ts = ray_hits(c, d, poly)
                inside = len(ts) % 2 == 1
                for i, t in enumerate(ts):
                    out = (i % 2 == 0) if inside else (i % 2 == 1)
                    g.add(Dot(c + t * d, radius=0.07, color=C_POS if out else C_NEG))
            return g

        mk = always_redraw(marks)
        info = T("entran = salen", 34, WHITE).move_to(UP * 4.5)
        eq0 = M(r"\vec\nabla\cdot\left(\frac{\hat u_R}{R^2}\right)=0", 56).next_to(info, DOWN, buff=0.35)
        self.play(Create(sq), FadeIn(mk), FadeIn(info), Write(eq0), run_time=0.9)
        self.play(sq.animate.move_to(path[1]), run_time=1.2)
        self.play(sq.animate.move_to(path[2]), run_time=1.2)
        info2 = T("solo salen: ¡flujo 4π!", 34, C_POS).move_to(info)
        self.play(sq.animate.move_to(path[3]), Transform(info, info2), run_time=1.2)
        self.play(Flash(c, color=YELLOW, flash_radius=1.0, line_length=0.4), run_time=0.6)
        eq1 = M(r"\vec\nabla\cdot\left(\frac{\hat u_R}{R^2}\right)=4\pi\,\delta^3(\vec R)", 56).move_to(eq0)
        self.play(TransformMatchingShapes(eq0, eq1), run_time=0.9)
        cap = T("cero en todas partes… salvo donde está la carga", 26, C_GREY).next_to(eq1, DOWN, buff=0.3)
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(0.8)
        lap = M(r"\nabla^2\!\left(\frac1R\right)=-4\pi\,\delta^3(\vec R)", 52, C_GREY).move_to(DOWN * 4.6)
        self.play(Write(lap), run_time=0.8)
        self.wait(0.5)
        mk.clear_updaters()
        law = M(r"\vec\nabla\cdot\vec E=\frac{\rho}{\varepsilon_0}", 80, YELLOW).move_to(DOWN * 4.9)
        box = SurroundingRectangle(law, color=YELLOW, buff=0.25)
        sub = T("1.ª ecuación de Maxwell", 28, C_GREY).next_to(box, UP, buff=0.2)
        self.play(FadeOut(lap), FadeIn(law, scale=1.2), run_time=0.7)
        self.play(Create(box), FadeIn(sub), run_time=0.5)
        self.outro(1.8)


class C06_Circulacion(VClip):
    idx = 6
    title = "Circulación nula: ∇×E = 0"

    def construct(self):
        self.header()
        c = np.array([0, -0.3, 0])
        q = charge(1, c, 0.22)
        field = ArrowVectorField(lambda p: 1.2 * normalize(p - c) / max(np.linalg.norm(p - c), 0.6) ** 0.8,
                                 x_range=[-4.2, 4.2, 0.8], y_range=[-4.6, 3.8, 0.8], colors=[C_GREY, WHITE],
                                 length_func=lambda n: 0.5 * np.tanh(n), opacity=0.45)
        eqs = VGroup(*[Circle(r, color=C_NEG, stroke_width=1.5, stroke_opacity=0.35).move_to(c) for r in (1, 1.8, 2.8, 4)])
        self.play(FadeIn(field), FadeIn(q), Create(eqs), run_time=0.8)
        # camino cerrado
        ts = np.linspace(0, TAU, 400, endpoint=False)
        loop_pts = [c + np.array([0.4 + 2.6 * np.cos(t) + 0.6 * np.cos(2 * t), 0.3 + 2.2 * np.sin(t) - 0.5 * np.sin(3 * t), 0]) for t in ts]
        loop = VMobject(color=YELLOW, stroke_width=3, stroke_opacity=0.5)
        loop.set_points_smoothly([*loop_pts, loop_pts[0]])
        s = ValueTracker(0)
        r0 = np.linalg.norm(loop_pts[0] - c)

        def pos():
            return loop.point_from_proportion(min(s.get_value(), 0.9999))

        dot = always_redraw(lambda: glow_dot(pos(), YELLOW, 0.08))
        trace = always_redraw(lambda: loop.copy().pointwise_become_partial(loop, 0, max(s.get_value(), 1e-3))
                              .set_stroke(YELLOW, 6, 1))
        val = DecimalNumber(0, num_decimal_places=2, font_size=60, color=YELLOW, include_sign=True)
        lab = VGroup(M(r"\int\vec E\cdot\mathrm d\vec\ell=", 60), val).arrange(RIGHT, buff=0.12).move_to(UP * 4.4)
        val.add_updater(lambda m: m.set_value(3 * (1 / r0 - 1 / np.linalg.norm(pos() - c))))
        self.play(Create(loop), FadeIn(dot), Write(lab), run_time=0.8)
        self.add(trace)
        self.play(s.animate.set_value(1), run_time=5.0, rate_func=linear)
        val.clear_updaters()
        val.set_value(0)
        cap = T("¡vuelve a cero! (aunque rodee la carga)", 30, YELLOW).next_to(lab, DOWN, buff=0.3)
        self.play(FadeIn(cap), Flash(dot.get_center(), color=YELLOW), run_time=0.6)
        self.wait(0.4)
        chain = VGroup(M(r"\oint_C\vec E\cdot\mathrm d\vec\ell=\iint_S(\vec\nabla\times\vec E)\cdot\mathrm d\vec S=0", 46),
                       M(r"\Rightarrow\ \vec\nabla\times\vec E=\vec 0\ \Rightarrow\ \vec E=-\vec\nabla\phi", 52, YELLOW)
                       ).arrange(DOWN, buff=0.35).move_to(DOWN * 5.0)
        bg = BackgroundRectangle(chain, fill_color=BG, fill_opacity=0.9, buff=0.2)
        self.play(FadeIn(bg), Write(chain[0]), run_time=1.0)
        self.play(Write(chain[1]), run_time=0.8)
        self.wait(1.2)
        # contraste: un campo con remolino
        self.play(FadeOut(VGroup(field, q, eqs, trace, dot, cap)), run_time=0.5)
        swirl = ArrowVectorField(lambda p: 0.6 * np.array([-(p - c)[1], (p - c)[0], 0]) / max(np.linalg.norm(p - c), 0.8),
                                 x_range=[-4.2, 4.2, 0.8], y_range=[-4.6, 3.8, 0.8], colors=[C_PINK, C_PINK],
                                 length_func=lambda n: 0.5 * np.tanh(n), opacity=0.5)
        s.set_value(0)
        val2 = DecimalNumber(0, num_decimal_places=2, font_size=60, color=C_PINK, include_sign=True)
        lab2 = VGroup(M(r"\oint\vec E\cdot\mathrm d\vec\ell=", 60), val2).arrange(RIGHT, buff=0.12).move_to(lab)
        val2.add_updater(lambda m: m.set_value(4.5 * s.get_value()))
        dot2 = always_redraw(lambda: glow_dot(pos(), C_PINK, 0.08))
        self.play(FadeIn(swirl), ReplacementTransform(lab, lab2), FadeIn(dot2), run_time=0.6)
        self.play(s.animate.set_value(1), run_time=2.2, rate_func=linear)
        val2.clear_updaters()
        no = T("con remolino: ∇×E ≠ 0 → no es electrostático", 26, C_PINK).next_to(lab2, DOWN, buff=0.3)
        self.play(FadeIn(no), run_time=0.4)
        self.outro(1.6)
