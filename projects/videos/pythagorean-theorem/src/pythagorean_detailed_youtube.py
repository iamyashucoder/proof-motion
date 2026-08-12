from manimlib import *


class PythagoreanDetailedYouTube(InteractiveScene):
    """Detailed area-dissection proof for a horizontal YouTube video."""

    def construct(self):
        blue, gold, pink, white = "#4DDCFF", "#FFD54A", "#FF5EA8", "#F8FBFF"

        def caption(text, color=WHITE):
            mob = Text(text, font_size=31, color=color).to_edge(DOWN, buff=.38)
            mob.fix_in_frame()
            return mob

        title = Text("A Complete Visual Proof of the Pythagorean Theorem", font_size=40, color=white).to_edge(UP, buff=.30)
        subtitle = Text("For a right triangle: a² + b² = c²", font_size=29, color=gold).next_to(title, DOWN, buff=.14)
        intro = caption("We will compare two ways of measuring the same large square.")
        for mob in [title, subtitle, intro]: mob.fix_in_frame()
        self.play(Write(title), FadeIn(subtitle), FadeIn(intro), run_time=1.2)
        self.wait(3)

        a, b = 2.0, 3.0
        side = a + b
        # Keep the diagram below the title/subtitle band.
        origin = LEFT * 2.5 + DOWN * 2.55
        p = lambda x, y: origin + RIGHT * x + UP * y
        outer = Square(side_length=side, color=white, stroke_width=4).move_to(origin + RIGHT * side / 2 + UP * side / 2)
        P, Q, R, T = p(b, 0), p(side, b), p(a, side), p(0, a)
        triangles = VGroup(
            Polygon(p(0, 0), P, T, color=blue, stroke_width=3),
            Polygon(P, p(side, 0), Q, color=blue, stroke_width=3),
            Polygon(Q, p(side, side), R, color=blue, stroke_width=3),
            Polygon(T, R, p(0, side), color=blue, stroke_width=3),
        )
        for tri in triangles: tri.set_fill(blue, opacity=.22)
        central = Polygon(P, Q, R, T, color=pink, stroke_width=4).set_fill(pink, opacity=.25)

        # First show one labelled right triangle.
        sample = Polygon(LEFT * 4.8 + DOWN * .25, LEFT * 2.8 + DOWN * .25, LEFT * 4.8 + UP * 2.75,
                         color=blue, stroke_width=4).set_fill(blue, opacity=.18)
        leg_a = Text("a", font_size=34, color=gold).move_to(LEFT * 5.05 + UP * 1.2)
        leg_b = Text("b", font_size=34, color=gold).move_to(LEFT * 3.8 + DOWN * .55)
        hyp = Text("c", font_size=34, color=pink).move_to(LEFT * 3.6 + UP * 1.55)
        right_angle = Square(side_length=.25, color=white, stroke_width=2).move_to(LEFT * 4.67 + DOWN * .12)
        tri_caption = caption("Start with a right triangle. Its legs are a and b; its hypotenuse is c.", blue)
        self.play(Transform(intro, tri_caption), FadeIn(sample), FadeIn(VGroup(leg_a, leg_b, hyp, right_angle)), run_time=1.0)
        self.wait(4)
        self.play(FadeOut(VGroup(sample, leg_a, leg_b, hyp, right_angle)), run_time=.7)

        outer_caption = caption("Place four congruent copies inside a square whose side length is a + b.")
        self.play(Transform(intro, outer_caption), ShowCreation(outer), run_time=.8)
        self.play(LaggedStart(*[FadeIn(tri, scale=.88) for tri in triangles], lag_ratio=.20), run_time=1.5)
        self.wait(3)

        congruent_caption = caption("All four blue triangles are identical, so each has area ½ab.", blue)
        self.play(Transform(intro, congruent_caption), run_time=.6)
        self.wait(4)

        center_caption = caption("The uncovered middle is a square: each of its sides is the hypotenuse c.", pink)
        c_square = Text("central area = c²", font_size=35, color=pink).move_to(central.get_center())
        self.play(Transform(intro, center_caption), FadeIn(central, scale=.9), FadeIn(c_square), run_time=.9)
        self.wait(4)

        outer_area = Text("Area of the outer square = (a + b)²", font_size=35, color=gold).to_edge(DOWN, buff=.38)
        outer_area.fix_in_frame()
        self.play(Transform(intro, outer_area), run_time=.7)
        self.wait(3)

        pieces_area = Text("Same area = 4(½ab) + c²", font_size=38, color=white).to_edge(DOWN, buff=.38)
        pieces_area.fix_in_frame()
        self.play(Transform(intro, pieces_area), run_time=.7)
        self.wait(4)

        expand = Text("(a + b)² = 4(½ab) + c²", font_size=38, color=gold).to_edge(DOWN, buff=.38)
        expand.fix_in_frame()
        simplify = Text("a² + 2ab + b² = 2ab + c²", font_size=36, color=white).to_edge(DOWN, buff=.38)
        simplify.fix_in_frame()
        result = Text("a² + b² = c²", font_size=58, color=gold).to_edge(DOWN, buff=.34)
        result.fix_in_frame()
        self.play(Transform(intro, expand), run_time=.7); self.wait(3)
        self.play(Transform(intro, simplify), run_time=.8); self.wait(3)
        final_caption = Text("Subtract 2ab from both sides. The Pythagorean theorem follows.",
                             font_size=27, color=gold).move_to(DOWN * 2.72)
        final_caption.fix_in_frame()
        self.play(Transform(intro, result), central.animate.set_fill(pink, opacity=.62), FadeIn(final_caption), run_time=1.0)
        self.wait(5)

        end = Text("One area. Two descriptions. One theorem.", font_size=42, color=white).move_to(ORIGIN)
        end.fix_in_frame()
        self.play(FadeOut(VGroup(outer, triangles, central, c_square, title, subtitle, intro, final_caption)),
                  FadeIn(end, scale=.9), run_time=1.0)
        self.wait(4)
