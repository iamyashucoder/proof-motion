from manimlib import *


class PythagoreanRearrangementShort(InteractiveScene):
    """A term-by-term, diagram-led rearrangement proof for a vertical Short."""

    def caption(self, words, color="#F8FBFF", size=31):
        label = Text(words, font_size=size, color=color)
        label.move_to(DOWN * 3.20)
        label.fix_in_frame()
        return label

    def construct(self):
        white, blue, pink, gold, muted = (
            "#F8FBFF", "#4DDCFF", "#FF5EA8", "#FFD54A", "#AAB6C5"
        )
        title = Text("PYTHAGOREAN THEOREM", font_size=38, color=white).to_edge(UP, buff=.34)
        subtitle = Text("FIRST DAY OF PROVING PYTH. THEO.", font_size=24, color=gold)
        subtitle.next_to(title, DOWN, buff=.12)
        title.fix_in_frame(); subtitle.fix_in_frame()
        self.play(FadeIn(title, shift=DOWN * .15), FadeIn(subtitle), run_time=.65)
        self.wait(.60)

        a, b = 1.45, 2.15
        side = a + b
        origin = LEFT * side / 2 + DOWN * 1.50
        p = lambda x, y: origin + RIGHT * x + UP * y

        def make_dimension(start, end, label, color, label_shift=ORIGIN):
            arrow = Line(start, end, color=color, stroke_width=2)
            arrow.add_tip(at_start=True, width=.17, length=.18)
            arrow.add_tip(width=.17, length=.18)
            text = Text(label, font_size=26, color=color).move_to((start + end) / 2 + label_shift)
            text.fix_in_frame()
            return VGroup(arrow, text)

        # The large square and the inner c-square.
        outer = Square(side_length=side, color=white, stroke_width=3).move_to(p(side / 2, side / 2))
        whole_fill = Square(side_length=side, stroke_width=0).move_to(outer.get_center())
        whole_fill.set_fill(gold, opacity=0)

        P, Q, R, T = p(b, 0), p(side, b), p(a, side), p(0, a)
        c_square = Polygon(P, Q, R, T, color=pink, stroke_width=4)
        c_square.set_fill(pink, opacity=.28)
        c_label = Text("c²", font_size=44, color=pink).move_to(c_square.get_center())
        c_label.fix_in_frame()

        def blue_triangle(points):
            tri = Polygon(*points, color=blue, stroke_width=3)
            tri.set_fill(blue, opacity=.23)
            return tri

        # Four identical right-triangle pieces around the c-square.
        triangles = VGroup(
            blue_triangle([p(0, 0), P, T]),
            blue_triangle([P, p(side, 0), Q]),
            blue_triangle([Q, p(side, side), R]),
            blue_triangle([T, R, p(0, side)]),
        )

        first_dimensions = VGroup(
            make_dimension(p(0, -.34), p(b, -.34), "b", gold, DOWN * .22),
            make_dimension(p(-.34, 0), p(-.34, a), "a", gold, LEFT * .22),
            make_dimension(P + LEFT * .22 + DOWN * .12, T + LEFT * .22 + DOWN * .12,
                           "c", gold, LEFT * .24),
            make_dimension(p(0, side + .34), p(side, side + .34), "a + b", muted, UP * .22),
        )

        text = self.caption("WE HAVE A SQUARE.")
        self.add(whole_fill)
        self.play(ShowCreation(outer), FadeIn(text), run_time=.65)
        self.play(whole_fill.animate.set_fill(gold, opacity=.18), outer.animate.set_color(gold), run_time=.45)
        self.play(whole_fill.animate.set_fill(gold, opacity=0), outer.animate.set_color(white), run_time=.25)
        self.wait(.70)

        self.play(Transform(text, self.caption("LET'S DRAW ANOTHER SQUARE INSIDE THIS BIGGER SQUARE.", size=23)), run_time=.55)
        self.play(FadeIn(triangles), ShowCreation(c_square), FadeIn(c_label, scale=.9), run_time=.80)
        self.wait(.85)

        self.play(Transform(text, self.caption("LET'S NAME THESE DIMENSIONS.")), run_time=.50)
        self.play(FadeIn(first_dimensions), run_time=.65)
        self.wait(1.50)

        # Flip/rearrange the four pieces to expose a² and b².
        targets = VGroup(
            blue_triangle([p(0, a), p(a, a), p(0, side)]),
            blue_triangle([p(a, a), p(a, side), p(0, side)]),
            blue_triangle([p(a, 0), p(side, 0), p(a, a)]),
            blue_triangle([p(a, a), p(side, 0), p(side, a)]),
        )
        # Both exposed squares share the same c-square pink visual language.
        a_square = Square(side_length=a, color=pink, stroke_width=3).move_to(p(a / 2, a / 2))
        a_square.set_fill(pink, opacity=.27)
        b_square = Square(side_length=b, color=pink, stroke_width=3).move_to(p(a + b / 2, a + b / 2))
        b_square.set_fill(pink, opacity=.27)
        a_label = Text("a²", font_size=38, color=pink).move_to(a_square.get_center())
        b_label = Text("b²", font_size=42, color=pink).move_to(b_square.get_center())
        a_label.fix_in_frame(); b_label.fix_in_frame()
        second_dimensions = VGroup(
            make_dimension(p(0, -.34), p(a, -.34), "a", gold, DOWN * .22),
            make_dimension(p(a, side + .34), p(side, side + .34), "b", pink, UP * .22),
            make_dimension(p(side + .34, 0), p(side + .34, side), "a + b", muted, RIGHT * .28),
        )

        self.play(Transform(text, self.caption("ON FLIPPING THESE FOUR TRIANGLES…", gold)), run_time=.50)
        self.play(FadeOut(c_square), FadeOut(c_label), FadeOut(first_dimensions),
                  *[Transform(old, new) for old, new in zip(triangles, targets)],
                  run_time=2.40, rate_func=smooth)
        self.play(FadeIn(a_square), FadeIn(b_square), FadeIn(a_label), FadeIn(b_label),
                  FadeIn(second_dimensions), run_time=.60)
        self.wait(1.0)

        # Build c² = a² + b² in the exact order the user requested.
        self.play(Transform(text, self.caption("AS YOU CAN SEE, c² CAN BE WRITTEN AS:", white)), run_time=.55)
        self.wait(.75)
        equation_y = DOWN * 3.95
        lhs = Text("c²  =", font_size=45, color=white).move_to(equation_y + LEFT * 1.95)
        a_term = Text("a²", font_size=45, color=pink).move_to(equation_y + LEFT * .35)
        plus = Text("+", font_size=43, color=white).move_to(equation_y + RIGHT * .72)
        b_term = Text("b²", font_size=45, color=pink).move_to(equation_y + RIGHT * 1.65)
        for item in (lhs, a_term, plus, b_term):
            item.fix_in_frame()

        self.play(FadeIn(lhs, shift=RIGHT * .15), run_time=.45)
        self.wait(.35)
        self.play(FadeIn(a_term, shift=UP * .12),
                  a_square.animate.set_fill(pink, opacity=.74), a_label.animate.set_color(white), run_time=.55)
        self.play(a_square.animate.set_fill(pink, opacity=.27), a_label.animate.set_color(pink), run_time=.20)
        self.wait(.65)
        self.play(FadeIn(plus), run_time=.30)
        self.wait(.35)
        self.play(FadeIn(b_term, shift=UP * .12),
                  b_square.animate.set_fill(pink, opacity=.74), b_label.animate.set_color(white), run_time=.55)
        self.play(b_square.animate.set_fill(pink, opacity=.27), b_label.animate.set_color(pink), run_time=.20)
        self.wait(.65)
        self.play(Transform(text, self.caption("THAT'S IT.", gold, size=36)), run_time=.45)
        self.wait(1.2)

        # The same pieces also build the binomial area identity.
        self.play(FadeOut(VGroup(lhs, a_term, plus, b_term)),
                  Transform(text, self.caption("WE CAN ALSO PROVE AN IDENTITY WITH THIS.", gold, size=32)),
                  run_time=.85)
        self.wait(.50)

        # Use two aligned lines so the identity can be substantially larger in 9:16.
        identity_y = DOWN * 3.95
        triangle_y = DOWN * 4.68
        whole_term = Text("(a + b)²", font_size=46, color=gold).move_to(identity_y + LEFT * 2.25)
        equal_sign = Text("=", font_size=48, color=white).move_to(identity_y + LEFT * .75)
        a_identity = Text("a²", font_size=46, color=pink).move_to(identity_y + RIGHT * .15)
        plus_a_b = Text("+", font_size=44, color=white).move_to(identity_y + RIGHT * .84)
        b_identity = Text("b²", font_size=46, color=pink).move_to(identity_y + RIGHT * 1.55)
        plus_triangles = Text("+", font_size=46, color=white).move_to(triangle_y + LEFT * .90)
        triangle_term = Text("½ab", font_size=46, color=gold).move_to(triangle_y + RIGHT * .15)
        for item in (whole_term, equal_sign, a_identity, plus_a_b, b_identity, plus_triangles, triangle_term):
            item.fix_in_frame()

        # (a + b)² is the complete outer square.
        self.play(FadeIn(whole_term, shift=UP * .10),
                  whole_fill.animate.set_fill(gold, opacity=.18), outer.animate.set_color(gold), run_time=.85)
        self.wait(.35)
        self.play(whole_fill.animate.set_fill(gold, opacity=0), outer.animate.set_color(white), run_time=.28)

        # a² and b² are the two exposed squares.
        self.play(FadeIn(equal_sign), FadeIn(a_identity, shift=UP * .10),
                  a_square.animate.set_fill(pink, opacity=.74), a_label.animate.set_color(white), run_time=.80)
        self.wait(.30)
        self.play(a_square.animate.set_fill(pink, opacity=.27), a_label.animate.set_color(pink), run_time=.25)
        self.play(FadeIn(plus_a_b), FadeIn(b_identity, shift=UP * .10),
                  b_square.animate.set_fill(pink, opacity=.74), b_label.animate.set_color(white), run_time=.80)
        self.wait(.30)
        self.play(b_square.animate.set_fill(pink, opacity=.27), b_label.animate.set_color(pink), run_time=.25)

        # Add the same ½ab triangle term, then count all four pieces visibly.
        self.play(FadeIn(plus_triangles), FadeIn(triangle_term, shift=UP * .10),
                  triangles[0].animate.set_fill(gold, opacity=.75), run_time=.75)
        self.wait(.25)
        self.play(triangles[0].animate.set_fill(blue, opacity=.23), run_time=.22)
        count = Text("(2)", font_size=42, color=gold).next_to(triangle_term, RIGHT, buff=.12)
        count.fix_in_frame()
        self.play(FadeIn(count), triangles[1].animate.set_fill(gold, opacity=.75), run_time=.75)
        self.wait(.25)
        self.play(triangles[1].animate.set_fill(blue, opacity=.23), run_time=.22)
        count_3 = Text("(3)", font_size=42, color=gold).move_to(count.get_center())
        count_3.fix_in_frame()
        self.play(Transform(count, count_3), triangles[2].animate.set_fill(gold, opacity=.75), run_time=.75)
        self.wait(.25)
        self.play(triangles[2].animate.set_fill(blue, opacity=.23), run_time=.22)
        count_4 = Text("(4)", font_size=42, color=gold).move_to(count.get_center())
        count_4.fix_in_frame()
        self.play(Transform(count, count_4), triangles[3].animate.set_fill(gold, opacity=.75), run_time=.75)
        self.wait(.25)
        self.play(triangles[3].animate.set_fill(blue, opacity=.23), run_time=.22)

        simplified = Text("(a + b)² = a² + 2ab + b²", font_size=36, color=white)
        simplified.move_to(DOWN * 5.40).fix_in_frame()
        self.play(FadeIn(simplified, shift=UP * .10), run_time=.90)
        self.wait(3.5)

        self.play(FadeOut(VGroup(title, subtitle, outer, triangles, a_square, b_square,
                                  a_label, b_label, second_dimensions, text, lhs, a_term,
                                  plus, b_term, whole_term, equal_sign, a_identity, plus_a_b,
                                  b_identity, plus_triangles, triangle_term, count, simplified)), run_time=.55)
