from common import *


class S04_Desarrollo(VScene):
    def construct(self):
        lab = section_label("3", "El desarrollo multipolar")
        self.add(lab)
        self.say("a")
        e1 = MathTex(r"\phi(\vec r)", "=", r"\frac{1}{4\pi\varepsilon_0}", r"\int_{V'}", r"\rho(\vec r\,')",
                     r"\,\frac{1}{\|\vec r-\vec r\,'\|}", r"\,\mathrm dV'", font_size=48).move_to(UP * 1.8)
        e1[0].set_color(C_R); e1[4].set_color(C_POS); e1[5].set_color(C_RR)
        self.play(Write(e1), run_time=2)
        e2 = MathTex(r"\phi(\vec r)", "=", r"\frac{1}{4\pi\varepsilon_0}", r"\int_{V'}", r"\rho(\vec r\,')",
                     r"\sum_{\ell=0}^{\infty}", r"\frac{r'^{\,\ell}}{r^{\ell+1}}", r"P_\ell(\cos\theta')",
                     r"\,\mathrm dV'", font_size=48).move_to(UP * 0.2)
        e2[0].set_color(C_R); e2[4].set_color(C_POS); e2[6].set_color(YELLOW); e2[7].set_color(L_COLORS[1])
        self.play(TransformFromCopy(e1[:5], e2[:5]), TransformFromCopy(e1[6], e2[8]),
                  TransformFromCopy(e1[5], e2[5:8]), run_time=2)
        e3 = MathTex(r"\phi(\vec r)", "=", r"\sum_{\ell=0}^{\infty}", r"\frac{1}{4\pi\varepsilon_0}",
                     r"\frac{1}{r^{\ell+1}}", r"\int_{V'}", r"r'^{\,\ell}", r"\rho(\vec r\,')",
                     r"P_\ell(\cos\theta')", r"\,\mathrm dV'", font_size=48).move_to(DOWN * 1.6)
        e3[0].set_color(C_R); e3[4].set_color(YELLOW); e3[7].set_color(C_POS); e3[8].set_color(L_COLORS[1])
        self.wait(2.5)
        self.play(TransformMatchingShapes(e2.copy(), e3), run_time=2.5)
        arrow = CurvedArrow(e2[6].get_bottom() + DOWN * 0.1, e3[4].get_top() + UP * 0.1, color=YELLOW, angle=-PI / 3)
        self.play(Create(arrow), Indicate(e3[4]))

        self.say("b")
        self.play(FadeOut(VGroup(e1, e2, arrow)), e3.animate.move_to(UP * 2.2))
        res = MathTex(r"\phi(\vec r)=\sum_{\ell=0}^{\infty}\phi_\ell(\vec r)", font_size=48)
        res[0][0:4].set_color(C_R)
        res.next_to(e3, DOWN, buff=0.6)
        box = SurroundingRectangle(VGroup(e3, res), color=YELLOW, buff=0.25)
        self.play(Write(res), Create(box))
        # dibujo: esfera de radio a y P fuera
        bc = np.array([-3.5, -2.2, 0])
        blob = make_blob(bc, 0.75, seed=9, n_dots=50)
        sph = DashedVMobject(Circle(radius=1.25, color=C_GREY).move_to(bc), num_dashes=40)
        ar = Line(bc, bc + 1.25 * np.array([np.cos(-0.5), np.sin(-0.5), 0]), color=C_GREY)
        al = MathTex("a", font_size=34, color=C_GREY).next_to(ar.get_center(), DOWN, buff=0.08)
        Pd = Dot(bc + np.array([3.2, 0.6, 0]), color=C_R)
        Pl = MathTex("P", color=C_R).next_to(Pd, RIGHT, buff=0.1)
        ex = VGroup(T("exacto si  r > a", 30), T("la aproximación: truncar", 30, YELLOW)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ex.move_to([3.4, -2.2, 0])
        self.play(FadeIn(blob), Create(sph), Create(ar), Write(al))
        self.play(FadeIn(Pd), Write(Pl), Write(ex[0]))
        self.wait(1.5)
        self.play(Write(ex[1]))

        self.say("c")
        self.play(FadeOut(VGroup(blob, sph, ar, al, Pd, Pl, ex, res, box)), e3.animate.scale(0.75).to_edge(UP, buff=0.9))
        ax = Axes(x_range=[0.8, 5, 1], y_range=[0, 1.3, 0.5], x_length=8.5, y_length=4.2,
                  axis_config={"color": C_GREY, "include_tip": False})
        ax.move_to(DOWN * 1.0 + LEFT * 1.2)
        xl = MathTex("r", font_size=36).next_to(ax.x_axis.get_end(), RIGHT)
        self.play(Create(ax), FadeIn(xl))
        labels = VGroup()
        curves = VGroup()
        for l in range(4):
            c = ax.plot(lambda x, l=l: min(x ** -(l + 1), 1.3), x_range=[0.8, 5, 0.01], color=L_COLORS[l], stroke_width=4)
            curves.add(c)
            lb = MathTex(rf"\ell={l}:\ \tfrac{{1}}{{r^{{{l + 1}}}}}", font_size=34, color=L_COLORS[l])
            labels.add(lb)
        labels.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax, RIGHT, buff=0.5)
        for c, lb in zip(curves, labels):
            self.play(Create(c), FadeIn(lb), run_time=1.1)

        self.say("d")
        self.play(FadeOut(VGroup(ax, xl, curves, labels, e3)))
        names = ["monopolo", "dipolo", "cuadrupolo", "octupolo"]
        cols = VGroup()
        for l in range(4):
            if l == 0:
                icon = charge(1, ORIGIN, 0.18)
            elif l == 1:
                icon = VGroup(charge(1, UP * 0.4, 0.15), charge(-1, DOWN * 0.4, 0.15))
            elif l == 2:
                icon = VGroup(*[charge(s, 0.45 * np.array([np.cos(a), np.sin(a), 0]), 0.14)
                                for s, a in [(1, 0), (-1, PI / 2), (1, PI), (-1, 3 * PI / 2)]])
            else:
                pts = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
                back = [charge(((i % 2) * 2 - 1), 0.42 * np.array([x, y, 0]) + np.array([0.22, 0.22, 0]), 0.11) for i, (x, y) in enumerate(pts)]
                front = [charge(-((i % 2) * 2 - 1), 0.42 * np.array([x, y, 0]), 0.13) for i, (x, y) in enumerate(pts)]
                edges = VGroup(*[Line(0.42 * np.array([*a, 0]), 0.42 * np.array([*b, 0]), color=C_GREY, stroke_width=1.5)
                                 for a, b in zip(pts, pts[1:] + pts[:1])])
                edges2 = edges.copy().shift([0.22, 0.22, 0])
                links = VGroup(*[Line(0.42 * np.array([*a, 0]), 0.42 * np.array([*a, 0]) + np.array([0.22, 0.22, 0]),
                                      color=C_GREY, stroke_width=1.5) for a in pts])
                icon = VGroup(edges2, *back, links, edges, *front)
            col = VGroup(MathTex(rf"\ell={l}", font_size=40, color=L_COLORS[l]),
                         icon,
                         T(names[l], 30),
                         MathTex(rf"2^{{{l}}}={2 ** l}\text{{ cargas}}", font_size=32, color=C_GREY))
            col.arrange(DOWN, buff=0.45)
            cols.add(col)
        cols.arrange(RIGHT, buff=1.1).move_to(DOWN * 0.2)
        for c in cols:
            self.play(FadeIn(c, shift=0.3 * UP), run_time=0.9)
        self.end()
        self.clear()


class S05_Monopolo(VScene):
    def construct(self):
        lab = section_label("4", "Término monopolar  (ℓ = 0)")
        self.add(lab)
        self.say("a")
        e = MathTex(r"\phi_0", "=", r"\frac{1}{4\pi\varepsilon_0\,r}", r"\int_{V'}", r"\rho(\vec r\,')", r"\,P_0", r"\,\mathrm dV'",
                    font_size=50).move_to(UP * 2 + LEFT * 2.6)
        e[5].set_color(L_COLORS[0])
        self.play(Write(e), run_time=2)
        p0 = MathTex(r"P_0=1", color=L_COLORS[0], font_size=40).next_to(e[5], DOWN, buff=0.6)
        self.play(FadeIn(p0, shift=0.2 * UP))
        self.play(FadeOut(e[5]), FadeOut(p0))
        brace = Brace(e[3:7], DOWN)
        qt = MathTex("Q", color=C_POS, font_size=44).next_to(brace, DOWN)
        self.play(GrowFromCenter(brace), Write(qt))
        res = MathTex(r"\phi_0(\vec r)=\frac{Q}{4\pi\varepsilon_0\,r}", font_size=54).move_to(DOWN * 1.2 + LEFT * 2.6)
        box = SurroundingRectangle(res, color=YELLOW, buff=0.25)
        self.play(Write(res), Create(box))

        self.say("b")
        c = np.array([3.9, -0.4, 0])
        img = potential_image(lambda X, Y: 0.6 / np.hypot(X, Y), c, 6.0, 6.0, vmax=0.8, alpha=0.55)
        q = charge(1, c, 0.2)
        rings = VGroup(*[Circle(radius=2.5 / k, color=C_POS, stroke_width=2).move_to(c) for k in range(1, 9)])
        self.play(FadeIn(img), FadeIn(q, scale=0.3))
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.15), run_time=2.5)
        t = T("equipotenciales: esferas", 28, C_GREY).next_to(rings, DOWN, buff=0.35)
        self.play(FadeIn(t))
        self.wait(1.5)
        t2 = T("Q no depende del origen", 30, YELLOW).next_to(box, DOWN, buff=0.6)
        self.play(Write(t2))
        self.end()
        self.clear()


class S06_Dipolo(VScene):
    def construct(self):
        lab = section_label("5", "Término dipolar  (ℓ = 1)")
        self.add(lab)
        self.say("a")
        e = MathTex(r"\phi_1", "=", r"\frac{1}{4\pi\varepsilon_0\,r^2}", r"\int_{V'}", r"\rho(\vec r\,')", r"\,r'\cos\theta'",
                    r"\,\mathrm dV'", font_size=50).move_to(UP * 2.0)
        e[5].set_color(L_COLORS[1])
        self.play(Write(e), run_time=2)
        dotp = MathTex(r"r'\cos\theta'", "=", r"\vec r\,'\cdot\hat u_r", font_size=46).next_to(e, DOWN, buff=0.8)
        dotp[0].set_color(L_COLORS[1])
        dotp[2][4:].set_color(C_R)
        self.play(TransformFromCopy(e[5], dotp[0]), Write(dotp[1:]))

        self.say("b")
        e2 = MathTex(r"\phi_1", "=", r"\frac{1}{4\pi\varepsilon_0\,r^2}", r"\Big(\int_{V'}\vec r\,'\rho(\vec r\,')\,\mathrm dV'\Big)",
                     r"\cdot\hat u_r", font_size=50).move_to(DOWN * 0.6)
        e2[4].set_color(C_R)
        self.play(FadeIn(e2, shift=0.3 * DOWN), run_time=1.5)
        br = Brace(e2[3], DOWN)
        pl = MathTex(r"\vec p", color=L_COLORS[1], font_size=50).next_to(br, DOWN)
        self.play(GrowFromCenter(br), Write(pl))
        res = MathTex(r"\phi_1(\vec r)=\frac{\vec p\cdot\hat u_r}{4\pi\varepsilon_0\,r^2},\qquad \vec p=\int_{V'}\vec r\,'\rho(\vec r\,')\,\mathrm dV'",
                      font_size=46).to_edge(DOWN, buff=0.5)
        box = SurroundingRectangle(res, color=YELLOW, buff=0.2)
        self.play(Write(res), Create(box), run_time=2)

        self.say("c")
        self.play(FadeOut(VGroup(e, dotp, e2, br, pl)), VGroup(res, box).animate.scale(0.7).to_edge(UP, buff=0.9))
        c = np.array([0, -0.8, 0])
        d = 0.55
        qp = charge(1, c + UP * d, 0.2, "+q")
        qn = charge(-1, c + DOWN * d, 0.2, "-q")
        lv = Arrow(c + DOWN * d, c + UP * d, buff=0.22, color=WHITE, stroke_width=4)
        ll = MathTex(r"\vec\ell", font_size=34).next_to(lv, LEFT, buff=0.1)
        self.play(FadeIn(qp, scale=0.3), FadeIn(qn, scale=0.3))
        self.play(GrowArrow(lv), Write(ll))
        facts = VGroup(MathTex(r"\vec p=q\vec\ell", font_size=44, color=L_COLORS[1]),
                       MathTex(r"Q=0", font_size=44, color=C_POS),
                       MathTex(r"\phi\approx\phi_1\propto\frac{1}{r^2}", font_size=44)).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        facts.move_to([4.3, -1.0, 0])
        for f_ in facts:
            self.play(Write(f_), run_time=1.0)

        self.say("d")
        dip = VGroup(qp, qn, lv, ll)
        self.play(FadeOut(facts), FadeOut(VGroup(res, box)), dip.animate.scale(0.6, about_point=c).shift(-c))
        c = ORIGIN
        img = potential_image(lambda X, Y: 0.5 * Y / np.hypot(X, Y) ** 3, c, 14.3, 8.1, res=420, vmax=0.35, alpha=0.55, rmin=0.45)
        self.play(FadeIn(img), run_time=1.5)
        self.bring_to_front(dip)
        form = MathTex(r"\phi_1=\frac{p\cos\theta}{4\pi\varepsilon_0\,r^2}", font_size=44).to_corner(UR, buff=0.5)
        bg = BackgroundRectangle(form, fill_color=BG, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(bg), Write(form))
        eq = DashedLine(LEFT * 7.2, RIGHT * 7.2, color=WHITE, stroke_width=2)
        plus = MathTex(r"\phi>0", color=C_POS, font_size=40).move_to([-4.5, 2.4, 0])
        minus = MathTex(r"\phi<0", color=C_NEG, font_size=40).move_to([-4.5, -2.4, 0])
        zero = MathTex(r"\phi=0", font_size=36).next_to(eq, UP, buff=0.12).to_edge(RIGHT, buff=0.6)
        self.play(FadeIn(plus), FadeIn(minus))
        self.play(Create(eq), FadeIn(zero))

        self.say("e")
        self.play(FadeOut(VGroup(plus, minus, zero, eq)), img.animate.set_opacity(0.35))
        eqp = dipole_equipotentials([0.6, 1.2, 2.2, 3.6, 5.5, 8.0, 11.5], c, 1.0, sw=2.5)
        fl = dipole_field_lines([0.9, 1.5, 2.4, 3.6, 5.5, 8.5, 13, 20], c, 1.0, rmin=0.45, sw=2)
        t1 = MathTex(r"r^2\propto\cos\theta", font_size=40, color=C_POS).to_corner(DL, buff=0.5)
        t2 = MathTex(r"r\propto\sin^2\theta", font_size=40).next_to(t1, UP, buff=0.3, aligned_edge=LEFT)
        bg2 = BackgroundRectangle(VGroup(t1, t2), fill_color=BG, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(bg2), Write(t1), LaggedStart(*[Create(x) for x in eqp], lag_ratio=0.08), run_time=3)
        self.bring_to_front(dip)
        self.play(Write(t2), LaggedStart(*[Create(x) for x in fl], lag_ratio=0.06), run_time=3)
        self.bring_to_front(dip, bg2, t1, t2, bg, form, lab)
        flashes = [ShowPassingFlash(x.copy().set_stroke(YELLOW, 4), time_width=0.3) for x in fl]
        self.play(LaggedStart(*flashes, lag_ratio=0.03), run_time=2.5)
        # marcar la ortogonalidad en un punto
        th = 0.9
        Cf = 5.5
        pt = np.array([Cf * np.sin(th) ** 3, Cf * np.sin(th) ** 2 * np.cos(th), 0])
        self.play(Flash(pt, color=YELLOW, flash_radius=0.35))

        self.say("f")
        self.clear()
        self.add(lab)
        O = np.array([-5.0, -2.6, 0])
        Op = np.array([-4.2, 1.2, 0])
        blob = make_blob([-1.5, -0.5, 0], 1.2, seed=11, n_dots=70)
        dO = Dot(O); lO = MathTex("O").next_to(dO, DL, buff=0.1)
        dOp = Dot(Op, color=TEAL); lOp = MathTex("O'", color=TEAL).next_to(dOp, UL, buff=0.1)
        sh = Arrow(O, Op, buff=0, color=TEAL, stroke_width=5)
        shl = MathTex(r"\overrightarrow{OO'}", color=TEAL, font_size=34).next_to(sh, LEFT, buff=0.1)
        self.play(FadeIn(blob), FadeIn(dO), Write(lO))
        self.play(GrowArrow(sh), FadeIn(dOp), Write(lOp), Write(shl))
        form = MathTex(r"\vec p_{O'}", "=", r"\vec p_O", "-", r"Q\,\overrightarrow{OO'}", font_size=54).move_to([3.4, 2.0, 0])
        form[4].set_color(TEAL)
        box = SurroundingRectangle(form, color=YELLOW, buff=0.2)
        self.play(Write(form), Create(box))
        c1 = MathTex(r"Q=0\ \Rightarrow\ \vec p\ \text{intrínseco}", font_size=42).next_to(form, DOWN, buff=0.8)
        c2 = MathTex(r"Q\neq0\ \Rightarrow\ \vec r_c=\frac{\vec p_O}{Q}\ :\ \vec p_{c}=\vec 0", font_size=42).next_to(c1, DOWN, buff=0.6)
        self.wait(2)
        self.play(Write(c1))
        self.wait(1.5)
        self.play(Write(c2))
        cdot = Dot([-1.5, -0.5, 0], color=YELLOW, radius=0.09)
        cl = T("centro de carga", 24, YELLOW).next_to(cdot, DOWN, buff=0.15)
        self.play(FadeIn(cdot, scale=3), FadeIn(cl))
        self.end()
        self.clear()


class S07_Cuadrupolo(VScene):
    def construct(self):
        lab = section_label("6", "Término cuadrupolar  (ℓ = 2)")
        self.add(lab)
        self.say("a")
        e = MathTex(r"\phi_2", "=", r"\frac{1}{4\pi\varepsilon_0\,r^3}", r"\int_{V'}", r"\rho\,r'^2", r"\,\tfrac12(3\cos^2\theta'-1)",
                    r"\,\mathrm dV'", font_size=48).move_to(UP * 2.0)
        e[5].set_color(L_COLORS[2])
        self.play(Write(e), run_time=2)
        self.play(Indicate(e[5], color=L_COLORS[2]))
        arrow_t = VGroup(T("vector", 30, C_GREY), MathTex(r"\longrightarrow"), T("matriz", 30, YELLOW)).arrange(RIGHT)
        arrow_t.next_to(e, DOWN, buff=0.8)
        self.play(FadeIn(arrow_t[0]))
        self.play(GrowFromEdge(arrow_t[1], LEFT), FadeIn(arrow_t[2]))

        self.say("b")
        Qd = MathTex(r"Q_{jk}=\int_{V'}\rho(\vec r\,')\,\big(3x_j'x_k'-\delta_{jk}\,r'^2\big)\,\mathrm dV'", font_size=48)
        Qd.move_to(DOWN * 0.4)
        self.play(FadeOut(arrow_t), Write(Qd), run_time=2.5)
        res = MathTex(r"\phi_2(\vec r)=\frac{1}{8\pi\varepsilon_0\,r^3}\sum_{j,k}Q_{jk}\,\ell_j\ell_k", font_size=48).to_edge(DOWN, buff=0.7)
        box = SurroundingRectangle(res, color=YELLOW, buff=0.2)
        self.play(Write(res), Create(box), run_time=2)
        lj = MathTex(r"\ell_j=x_j/r", font_size=34, color=C_GREY).next_to(box, RIGHT, buff=0.4)
        self.play(FadeIn(lj))

        self.say("c")
        self.play(FadeOut(VGroup(e, Qd, res, box, lj)))
        names = [["Q_{xx}", "Q_{xy}", "Q_{xz}"], ["Q_{yx}", "Q_{yy}", "Q_{yz}"], ["Q_{zx}", "Q_{zy}", "Q_{zz}"]]
        M = Matrix(names, h_buff=1.6, v_buff=1.0).scale(1.1).move_to(LEFT * 2.8)
        ents = M.get_entries()
        self.play(Write(M))
        cnt = MathTex("9", font_size=72).move_to(RIGHT * 3.5)
        self.play(FadeIn(cnt))
        self.wait(0.6)
        low = [ents[3], ents[6], ents[7]]
        up = [ents[1], ents[2], ents[5]]
        self.play(*[Indicate(x, color=YELLOW) for x in low + up])
        self.play(*[x.animate.set_opacity(0.2) for x in low],
                  Transform(cnt, MathTex("6", font_size=72).move_to(cnt)))
        sym = MathTex(r"Q_{jk}=Q_{kj}", font_size=36, color=C_GREY).next_to(cnt, DOWN, buff=0.4)
        self.play(FadeIn(sym))
        self.wait(0.8)
        diag = [ents[0], ents[4], ents[8]]
        tr = MathTex(r"Q_{xx}+Q_{yy}+Q_{zz}=0", font_size=36, color=C_GREY).next_to(sym, DOWN, buff=0.3)
        self.play(*[x.animate.set_color(YELLOW) for x in diag], FadeIn(tr))
        self.play(Transform(cnt, MathTex("5", font_size=72, color=YELLOW).move_to(cnt)))
        self.wait(1.0)
        self.play(FadeOut(VGroup(M, cnt, sym, tr)))
        row = VGroup()
        for l, n, w in [(0, 1, "Q"), (1, 3, r"\vec p"), (2, 5, r"Q_{jk}")]:
            row.add(VGroup(MathTex(rf"\ell={l}", color=L_COLORS[l], font_size=40),
                           MathTex(w, font_size=48, color=L_COLORS[l]),
                           MathTex(rf"2\ell+1={n}", font_size=40)).arrange(DOWN, buff=0.4))
        row.arrange(RIGHT, buff=1.8)
        for r_ in row:
            self.play(FadeIn(r_, shift=0.3 * UP), run_time=0.8)

        self.say("d")
        self.play(FadeOut(row))
        c = np.array([-3.5, -0.5, 0])
        dd = 1.0
        q1 = charge(1, c + UP * dd, 0.2, "+q")
        q2 = charge(-1, c, 0.24, "-2q")
        q3 = charge(1, c + DOWN * dd, 0.2, "+q")
        dl = BraceBetweenPoints(c, c + UP * dd, LEFT)
        dlab = MathTex("d", font_size=34).next_to(dl, LEFT, buff=0.1)
        self.play(LaggedStart(FadeIn(q1, scale=0.3), FadeIn(q2, scale=0.3), FadeIn(q3, scale=0.3), lag_ratio=0.3))
        self.play(GrowFromCenter(dl), Write(dlab))
        facts = VGroup(MathTex(r"Q=q+q-2q=0", font_size=42),
                       MathTex(r"\vec p=qd\,\hat u_z-qd\,\hat u_z=\vec 0", font_size=42),
                       MathTex(r"Q_{zz}=\sum_i q_i(3z_i^2-r_i^2)=4qd^2", font_size=42, color=L_COLORS[2])
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([2.6, -0.3, 0])
        for f_ in facts:
            self.play(Write(f_), run_time=1.3)
            self.wait(0.6)

        self.say("e")
        quad = VGroup(q1, q2, q3)
        self.play(FadeOut(VGroup(facts, dl, dlab)), quad.animate.scale(0.45, about_point=c).shift(-c))
        img = potential_image(lambda X, Y: 0.25 * (3 * Y ** 2 / (X ** 2 + Y ** 2) - 1) / np.hypot(X, Y) ** 3,
                              ORIGIN, 14.3, 8.1, res=420, vmax=0.25, alpha=0.55, rmin=0.5)
        self.play(FadeIn(img), run_time=1.5)
        self.bring_to_front(quad)
        eqs = quad_equipotentials([0.4, 1.0, 2.2, 4.5, 9, 18, 36], ORIGIN, 1.0)
        fl = quad_field_lines([1.5, 3, 6, 12, 25, 50, 100], ORIGIN, 1.0, rmin=0.5, rmax=9)
        self.play(LaggedStart(*[Create(x) for x in eqs], lag_ratio=0.03), run_time=2.5)
        self.play(LaggedStart(*[Create(x) for x in fl], lag_ratio=0.02), img.animate.set_opacity(0.35), run_time=2.5)
        self.bring_to_front(quad, lab)
        th0 = np.arccos(1 / np.sqrt(3))
        cone = VGroup(*[DashedLine(ORIGIN, 9 * np.array([np.sin(a), np.cos(a), 0]), color=YELLOW, stroke_width=3)
                        for a in (th0, -th0, PI - th0, PI + th0)])
        arc = Arc(radius=1.6, start_angle=PI / 2, angle=-th0, color=YELLOW)
        al = MathTex(r"54{,}7^\circ", font_size=34, color=YELLOW).move_to(2.1 * np.array([np.sin(th0 / 2), np.cos(th0 / 2), 0]))
        alb = BackgroundRectangle(al, fill_color=BG, fill_opacity=0.8, buff=0.08)
        form = MathTex(r"3\cos^2\theta=1", font_size=40, color=YELLOW).to_corner(UR, buff=0.5)
        fb = BackgroundRectangle(form, fill_color=BG, fill_opacity=0.85, buff=0.15)
        self.play(Create(cone), run_time=1.5)
        self.play(Create(arc), FadeIn(alb), Write(al), FadeIn(fb), Write(form))
        flashes = [ShowPassingFlash(x.copy().set_stroke(YELLOW, 4), time_width=0.3) for x in fl]
        self.play(LaggedStart(*flashes, lag_ratio=0.01), run_time=2)

        self.say("f")
        self.clear()
        self.add(lab)
        shapes = VGroup()
        specs = [(0.8, 2.2, 0, r"Q_{zz}>0", "alargada"), (2.2, 0.8, 0, r"Q_{zz}<0", "achatada"),
                 (1.6, 1.6, 0, r"Q_{zz}=0", "esférica")]
        for w, h, ang, f_, n in specs:
            el = Ellipse(width=w * 1.2, height=h * 1.2, color=C_POS, stroke_width=3)
            el.set_fill(C_POS, opacity=0.25)
            core = Ellipse(width=w * 0.6, height=h * 0.6, stroke_width=0).set_fill(C_POS, opacity=0.35)
            zax = Arrow(DOWN * 1.8, UP * 1.8, buff=0, color=C_GREY, stroke_width=2, max_tip_length_to_length_ratio=0.06)
            zl = MathTex("z", font_size=28, color=C_GREY).next_to(zax, UP, buff=0.05)
            g = VGroup(zax, zl, el, core, MathTex(f_, font_size=40).shift(DOWN * 2.4), T(n, 28, C_GREY).shift(DOWN * 3.0))
            shapes.add(g)
        shapes.arrange(RIGHT, buff=1.6).move_to(DOWN * 0.1)
        for g in shapes:
            self.play(FadeIn(g, shift=0.3 * UP), run_time=1.0)
            self.wait(max(min(self.remaining() / 3 - 1.0, 2.5), 0))
        self.end()
        self.clear()


class S08_Resumen(VScene):
    def construct(self):
        lab = section_label("7", "Resumen")
        self.add(lab)
        self.say("a")
        f = MathTex(r"\phi(\vec r)", "=", r"\frac{1}{4\pi\varepsilon_0}\Bigg[", r"\frac{Q}{r}", "+", r"\frac{\vec p\cdot\hat u_r}{r^2}",
                    "+", r"\frac{1}{2r^3}\sum_{j,k}Q_{jk}\ell_j\ell_k", r"+\cdots\Bigg]", font_size=50).move_to(UP * 2.2)
        f[0].set_color(C_R)
        for i, k in [(3, 0), (5, 1), (7, 2)]:
            f[i].set_color(L_COLORS[k])
        self.play(Write(f[:3]), run_time=1.5)
        self.play(Write(f[3]), run_time=1.3)
        for i in (5, 7):
            self.wait(0.6)
            self.play(Write(f[i - 1]), Write(f[i]), run_time=1.3)
        self.play(Write(f[8]))
        box = SurroundingRectangle(f, color=YELLOW, buff=0.2)
        self.play(Create(box))

        self.say("b")
        w = 3.6
        cs = [np.array([-4.4, -1.4, 0]), np.array([0, -1.4, 0]), np.array([4.4, -1.4, 0])]
        frames = VGroup(*[Square(w, color=C_GREY, stroke_width=1.5).move_to(c) for c in cs])
        sc = 0.32
        mono = VGroup(*[Circle(radius=sc * 5 / k, color=C_POS, stroke_width=2).move_to(cs[0]) for k in range(1, 9)])
        dip = dipole_equipotentials([0.6, 1.2, 2.2, 3.6, 5.5, 8.0, 11.5, 16], cs[1], sc, sw=2)
        qd = quad_equipotentials([0.4, 1.0, 2.2, 4.5, 9, 18, 36, 60], cs[2], sc, sw=2)
        imgs = Group(
            potential_image(lambda X, Y: 0.3 / np.hypot(X, Y), cs[0], w, w, res=200, vmax=0.8, alpha=0.5),
            potential_image(lambda X, Y: 0.05 * Y / np.hypot(X, Y) ** 3, cs[1], w, w, res=200, vmax=0.35, alpha=0.5, rmin=0.15),
            potential_image(lambda X, Y: 0.01 * (3 * Y ** 2 / (X ** 2 + Y ** 2) - 1) / np.hypot(X, Y) ** 3, cs[2], w, w,
                            res=200, vmax=0.25, alpha=0.5, rmin=0.15))
        lbls = VGroup(*[MathTex(s, font_size=34, color=L_COLORS[k]).next_to(frames[k], DOWN, buff=0.2)
                        for k, s in enumerate([r"\ell=0\ \ \propto 1/r", r"\ell=1\ \ \propto 1/r^2", r"\ell=2\ \ \propto 1/r^3"])])
        self.play(Create(frames))
        for k, cur in enumerate([mono, dip, qd]):
            self.play(FadeIn(imgs[k]), LaggedStart(*[Create(x) for x in cur], lag_ratio=0.05), FadeIn(lbls[k]), run_time=1.6)
        self.end()
        self.clear()


class S09_Error(VScene):
    def construct(self):
        lab = section_label("8", "¿Cuántos términos?")
        self.add(lab)
        self.say("a")
        bc = np.array([-4.2, -0.3, 0])
        blob = make_blob(bc, 1.0, seed=2, n_dots=80)
        sph = DashedVMobject(Circle(radius=1.6, color=C_GREY).move_to(bc), num_dashes=40)
        ar = Line(bc, bc + 1.6 * RIGHT, color=C_GREY)
        al = MathTex("a", font_size=34, color=C_GREY).next_to(ar, DOWN, buff=0.08)
        sign = MathTex(r"\rho\ge0", font_size=40, color=C_POS).next_to(sph, DOWN, buff=0.3)
        self.play(FadeIn(blob), Create(sph))
        self.play(Create(ar), Write(al), Write(sign))

        self.say("b")
        bound = MathTex(r"\left|\frac{\phi_n(\vec r)}{\phi_0(\vec r)}\right|", r"\le", r"\left(\frac{a}{r}\right)^{n}", font_size=60)
        bound.move_to([2.6, 1.3, 0])
        bound[2].set_color(YELLOW)
        box = SurroundingRectangle(bound, color=YELLOW, buff=0.25)
        why = VGroup(MathTex(r"|P_n(\cos\theta')|\le 1", font_size=38), MathTex(r"r'\le a", font_size=38)).arrange(RIGHT, buff=1.0)
        why.next_to(box, DOWN, buff=0.6)
        self.play(Write(why[0]))
        self.play(Write(why[1]))
        self.play(Write(bound), Create(box), run_time=2)

        self.say("c")
        self.play(FadeOut(VGroup(blob, sph, ar, al, sign, why)), VGroup(bound, box).animate.scale(0.65).to_corner(UR, buff=0.5))
        cond = MathTex(r"r=10a", font_size=44).to_corner(UL, buff=0.5).shift(DOWN * 0.7)
        self.play(Write(cond))
        ax = Axes(x_range=[-0.5, 4.5, 1], y_range=[-4.5, 0.5, 1], x_length=8, y_length=4.6,
                  axis_config={"color": C_GREY, "include_tip": False}).move_to(DOWN * 0.8)
        ylabels = VGroup(*[MathTex(s, font_size=28).next_to(ax.c2p(-0.5, v), LEFT, buff=0.15)
                           for s, v in [("1", 0), ("10^{-1}", -1), ("10^{-2}", -2), ("10^{-3}", -3), ("10^{-4}", -4)]])
        xlabels = VGroup(*[MathTex(f"n={n}", font_size=30, color=L_COLORS[n] if n < 3 else C_GREY).next_to(ax.c2p(n, -4.5), DOWN, buff=0.2)
                           for n in range(5)])
        self.play(Create(ax), FadeIn(ylabels), FadeIn(xlabels))
        bars = VGroup()
        for n in range(5):
            top = ax.c2p(n, -n)
            bot = ax.c2p(n, -4.5)
            b = Rectangle(width=0.9, height=top[1] - bot[1], stroke_width=0,
                          fill_color=L_COLORS[n] if n < 3 else C_GREY, fill_opacity=0.8)
            b.move_to((np.array(top) + np.array(bot)) / 2)
            bars.add(b)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25), run_time=2)
        thr = DashedLine(ax.c2p(-0.5, -2), ax.c2p(4.5, -2), color=YELLOW)
        thl = T("1 %", 28, YELLOW).next_to(thr, RIGHT, buff=0.2)
        self.play(Create(thr), FadeIn(thl))
        kept = SurroundingRectangle(VGroup(bars[:3], xlabels[:3]), color=WHITE, buff=0.15)
        names = T("monopolo · dipolo · cuadrupolo", 28).next_to(cond, DOWN, buff=0.4, aligned_edge=LEFT)
        self.wait(1.5)
        self.play(Create(kept), Write(names))

        self.say("d")
        self.play(FadeOut(VGroup(ax, ylabels, xlabels, bars, thr, thl, kept, names, cond, bound, box)))
        layers = VGroup()
        for k, (sym, nm) in enumerate([("Q", "carga"), (r"\vec p", "momento dipolar"), (r"Q_{jk}", "tensor cuadrupolar")]):
            layers.add(VGroup(MathTex(sym, font_size=64, color=L_COLORS[k]), T(nm, 26, C_GREY)).arrange(DOWN, buff=0.3))
        layers.arrange(RIGHT, buff=1.4).move_to(UP * 0.5)
        dots = MathTex(r"\cdots", font_size=64).next_to(layers, RIGHT, buff=0.8).align_to(layers[0][0], UP)
        for L in layers:
            self.play(FadeIn(L, shift=0.3 * UP), run_time=1.0)
        self.play(FadeIn(dots))
        fin = T("Desarrollo multipolar", 48, YELLOW).next_to(layers, DOWN, buff=1.2)
        self.play(Write(fin), run_time=1.5)
        self.end(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.5)
