from manimlib import *


class VectorSpaceExplainer(InteractiveScene):
    """A compact visual introduction to the idea of a vector space."""

    default_camera_config = {"background_color": "#05070D"}

    def construct(self):
        orange = "#FF6A00"
        cyan = "#4DDCFF"
        green = "#61E294"

        title = Text("VECTOR SPACE", font_size=58, color=WHITE).to_edge(UP, buff=.45)
        subtitle = Text("A world closed under addition and scaling", font_size=28, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=.16)
        self.play(Write(title), FadeIn(subtitle, shift=UP * .15), run_time=.8)

        plane = NumberPlane(
            x_range=(-5, 5, 1), y_range=(-3, 3, 1),
            width=10.5, height=6.0,
            background_line_style={"stroke_color": GREY_E, "stroke_width": 1},
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * .55)
        self.play(ShowCreation(plane), run_time=.7)

        origin = plane.c2p(0, 0)
        u_end = plane.c2p(2, 1)
        v_end = plane.c2p(-1, 2)
        u = Arrow(origin, u_end, buff=0, color=cyan, stroke_width=6)
        v = Arrow(origin, v_end, buff=0, color=orange, stroke_width=6)
        u_label = Text("u", color=cyan, font_size=42).next_to(u.get_end(), RIGHT, buff=.1)
        v_label = Text("v", color=orange, font_size=42).next_to(v.get_end(), LEFT, buff=.1)
        intro = Text("Vectors are arrows with direction and size.", font_size=30).to_edge(DOWN, buff=.4)
        self.play(GrowArrow(u), GrowArrow(v), FadeIn(u_label), FadeIn(v_label), FadeIn(intro), run_time=.8)
        self.wait(.5)

        add_caption = Text("1. Add any two vectors", font_size=36, color=WHITE).to_edge(DOWN, buff=.4)
        result_end = plane.c2p(1, 3)
        translated_v = Arrow(u_end, result_end, buff=0, color=orange, stroke_width=5)
        result = Arrow(origin, result_end, buff=0, color=green, stroke_width=7)
        result_label = Text("u + v", color=green, font_size=38).next_to(result.get_end(), UP, buff=.08)
        self.play(Transform(intro, add_caption), TransformFromCopy(v, translated_v), run_time=.7)
        self.play(GrowArrow(result), FadeIn(result_label), run_time=.55)
        self.wait(.5)

        scale_caption = Text("2. Multiply by a number", font_size=36, color=WHITE).to_edge(DOWN, buff=.4)
        two_u = Arrow(origin, plane.c2p(4, 2), buff=0, color=cyan, stroke_width=7)
        two_u_label = Text("2u", color=cyan, font_size=38).next_to(two_u.get_end(), RIGHT, buff=.1)
        self.play(
            FadeOut(VGroup(translated_v, result, result_label)),
            Transform(intro, scale_caption),
            Transform(u, two_u), Transform(u_label, two_u_label),
            run_time=.8,
        )
        self.wait(.5)

        zero_caption = Text("3. The zero vector is included", font_size=36, color=WHITE).to_edge(DOWN, buff=.4)
        zero = Dot(origin, radius=.09, color=WHITE)
        zero_label = Text("0", color=WHITE, font_size=38).next_to(zero, DOWN + LEFT, buff=.1)
        self.play(Transform(intro, zero_caption), FadeIn(zero), FadeIn(zero_label), run_time=.6)

        opposite_caption = Text("4. Every vector has an opposite", font_size=36, color=WHITE).to_edge(DOWN, buff=.4)
        opposite = Arrow(origin, plane.c2p(-2, -1), buff=0, color=YELLOW, stroke_width=6)
        opposite_label = Text("-u", color=YELLOW, font_size=38).next_to(opposite.get_end(), LEFT, buff=.1)
        cancellation = Text("u + (-u) = 0", color=WHITE, font_size=42).move_to(UP * .15)
        self.play(Transform(intro, opposite_caption), GrowArrow(opposite), FadeIn(opposite_label), run_time=.6)
        self.play(Write(cancellation), run_time=.55)
        self.wait(.6)

        conclusion = Text("Add and scale — stay in the same space.", font_size=38, color=green)
        conclusion.move_to(DOWN * .55)
        self.play(
            FadeOut(VGroup(subtitle, intro, u, v, u_label, v_label, opposite, opposite_label, zero, zero_label, cancellation)),
            FadeIn(conclusion, scale=.85), run_time=.7,
        )
        self.wait(1.2)
