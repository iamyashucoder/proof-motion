from manimlib import *


class PythagoreanProofShort(InteractiveScene):
    """Brief visual dissection proof of the Pythagorean theorem."""

    def construct(self):
        blue, gold, pink, white = "#4DDCFF", "#FFD54A", "#FF5EA8", "#F8FBFF"
        title = Text("PYTHAGOREAN THEOREM", font_size=44, color=white).to_edge(UP, buff=.38)
        statement = Text("For every right triangle:  a² + b² = c²", font_size=30, color=gold)
        statement.next_to(title, DOWN, buff=.15)
        self.play(Write(title), FadeIn(statement), run_time=.8)

        a, b = 1.8, 2.8
        side = a + b
        origin = LEFT * side / 2 + DOWN * 1.25
        point = lambda x, y: origin + RIGHT * x + UP * y

        outer = Square(side_length=side, color=white, stroke_width=4).move_to(origin + RIGHT * side / 2 + UP * side / 2)
        P, Q, R, T = point(b, 0), point(side, b), point(a, side), point(0, a)
        central = Polygon(P, Q, R, T, color=pink, stroke_width=4)
        central.set_fill(pink, opacity=.24)
        triangles = VGroup(
            Polygon(point(0, 0), P, T, color=blue, stroke_width=3),
            Polygon(P, point(side, 0), Q, color=blue, stroke_width=3),
            Polygon(Q, point(side, side), R, color=blue, stroke_width=3),
            Polygon(T, R, point(0, side), color=blue, stroke_width=3),
        )
        for triangle in triangles:
            triangle.set_fill(blue, opacity=.20)
        c_label = Text("c²", font_size=42, color=pink).move_to(central.get_center())
        diagram_note = Text("Four copies of the same right triangle", font_size=27, color=white).to_edge(DOWN, buff=.52)

        self.play(ShowCreation(outer), FadeIn(diagram_note), run_time=.6)
        self.play(LaggedStart(*[FadeIn(triangle, scale=.85) for triangle in triangles], lag_ratio=.18), run_time=1.2)
        self.play(FadeIn(central, scale=.85), FadeIn(c_label), run_time=.65)
        self.wait(.7)

        line_1 = Text("Area of large square = (a + b)²", font_size=31, color=white).to_edge(DOWN, buff=.50)
        line_2 = Text("= 4 × (½ab) + c²", font_size=34, color=gold).to_edge(DOWN, buff=.50)
        line_3 = Text("a² + 2ab + b² = 2ab + c²", font_size=29, color=white).to_edge(DOWN, buff=.50)
        result = Text("a² + b² = c²", font_size=52, color=gold).to_edge(DOWN, buff=.45)
        self.play(Transform(diagram_note, line_1), run_time=.7)
        self.play(Transform(diagram_note, line_2), run_time=.7)
        self.play(Transform(diagram_note, line_3), run_time=.8)
        self.play(Transform(diagram_note, result), central.animate.set_fill(pink, opacity=.55), run_time=.9)
        self.wait(1.5)
