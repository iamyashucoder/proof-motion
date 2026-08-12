from manim import *

config.frame_height = 14


class AristotlesWheelParadox(Scene):
    def construct(self):
        self.camera.background_color = "#080B12"
        big_c = "#63E6FF"
        small_c = "#FF5EA8"
        yellow = "#FFD166"
        text_c = "#F4F7FF"

        title = Text("ARISTOTLE'S WHEEL PARADOX", font_size=43, color=text_c, weight="BOLD").to_edge(UP, buff=.5)
        subtitle = Text("How can one turn cover two different distances?", font_size=20, color="#AAB8D0").next_to(title, DOWN, buff=.12)

        ground = Line(LEFT*6.2+DOWN*2.05, RIGHT*6.2+DOWN*2.05, color="#3D506E", stroke_width=3)
        small_line = Line(LEFT*6.2+DOWN*4.55, RIGHT*6.2+DOWN*4.55, color="#573A55", stroke_width=3)
        big_label = Text("large circle rolls", font_size=19, color=big_c).next_to(ground, UP, buff=.18).to_edge(LEFT, buff=.85)
        small_label = Text("small circle touches this line", font_size=18, color=small_c).next_to(small_line, DOWN, buff=.18).to_edge(LEFT, buff=.85)

        r_big, r_small = 1.75, .92
        start = LEFT*4.4+DOWN*.3
        tracker = ValueTracker(0)

        def wheel_group():
            # The large circle rolls without slipping: x = R theta.
            theta = tracker.get_value()
            center = start + RIGHT*(r_big*theta)
            big = Circle(radius=r_big, color=big_c, stroke_width=5).move_to(center)
            small = Circle(radius=r_small, color=small_c, stroke_width=5).move_to(center)
            hub = Dot(center, radius=.09, color=text_c)
            # Spokes make the shared one-turn rotation obvious.
            spokes = VGroup()
            for a in [0, PI/2, PI, 3*PI/2]:
                end = center + r_big*.88*np.array([np.cos(a-theta), np.sin(a-theta), 0])
                spokes.add(Line(center, end, color=yellow, stroke_width=3))
            marker_big = Dot(center + r_big*np.array([np.cos(PI/2-theta), np.sin(PI/2-theta), 0]), radius=.07, color=yellow)
            marker_small = Dot(center + r_small*np.array([np.cos(PI/2-theta), np.sin(PI/2-theta), 0]), radius=.065, color=yellow)
            return VGroup(big, small, spokes, hub, marker_big, marker_small)

        wheel = always_redraw(wheel_group)
        self.play(FadeIn(title), FadeIn(subtitle), Create(ground), Create(small_line), FadeIn(big_label), FadeIn(small_label), FadeIn(wheel), run_time=.7)

        big_measure = MathTex(r"2\pi R", color=big_c, font_size=34).move_to(DOWN*2.7+LEFT*1.8)
        small_measure = MathTex(r"2\pi r", color=small_c, font_size=34).move_to(DOWN*5.15+LEFT*3.45)
        self.play(FadeIn(big_measure), FadeIn(small_measure), run_time=.35)
        self.play(tracker.animate.set_value(TAU), run_time=4, rate_func=linear)

        # The big wheel's track matches its circumference.  The small circle's
        # rotation has the same angle, but it spans the larger track distance.
        big_brace = BraceBetweenPoints(LEFT*4.4+DOWN*2.35, LEFT*4.4+RIGHT*(TAU*r_big)+DOWN*2.35, color=big_c)
        big_result = MathTex(r"\text{distance}=2\pi R", color=big_c, font_size=30).next_to(big_brace, DOWN, buff=.12)
        small_brace = BraceBetweenPoints(LEFT*4.4+DOWN*4.22, LEFT*4.4+RIGHT*(TAU*r_big)+DOWN*4.22, color=small_c)
        paradox = Text("But both circles made exactly one turn!", font_size=25, color=yellow).move_to(UP*.95)
        self.play(Create(big_brace), FadeIn(big_result), Create(small_brace), FadeIn(paradox), run_time=.8)
        self.wait(.45)

        # Resolution: use short tick marks to reveal that the small rim sweeps
        # over the line, rather than depositing matching arc-length segments.
        slips = VGroup()
        x0 = -4.4
        for x in np.linspace(x0, x0 + TAU*r_big, 17):
            slips.add(Line(np.array([x, -4.55, 0]), np.array([x+.20, -4.55, 0]), color=small_c, stroke_width=4))
        resolution = Text("Resolution: the small circle slides on the lower line.", font_size=24, color=text_c).move_to(UP*.15)
        explanation = MathTex(r"\text{same rotation}\ \ne\ \text{same rolling distance}", font_size=31, color=yellow).move_to(UP*-.55)
        self.play(FadeOut(paradox), FadeIn(resolution), FadeIn(explanation), Create(slips), run_time=.8)
        self.wait(2)
        self.play(FadeOut(VGroup(title, subtitle, ground, small_line, big_label, small_label, wheel, big_measure, small_measure, big_brace, big_result, small_brace, slips, resolution, explanation)), run_time=.45)
