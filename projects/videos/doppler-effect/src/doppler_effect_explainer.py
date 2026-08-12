from manim import *

config.frame_height = 14


class DopplerEffectExplainer(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        white, cyan, violet, orange, muted = "#F4F7FF", "#63E6FF", "#9E7BFF", "#FFB654", "#AAB8D0"
        title = Text("THE DOPPLER EFFECT", font_size=42, color=white, weight="BOLD").to_edge(UP, buff=.58)
        subtitle = Text("Why a moving siren changes pitch", font_size=21, color=muted).next_to(title, DOWN, buff=.14)
        road = Line(LEFT*4.0 + DOWN*2.5, RIGHT*4.0 + DOWN*2.5, color="#31435F", stroke_width=8)
        listener = VGroup(Circle(radius=.28, color=orange, fill_opacity=1), Line(DOWN*.28, DOWN*.85, color=orange, stroke_width=7), Line(LEFT*.33+DOWN*.53, RIGHT*.33+DOWN*.53, color=orange, stroke_width=6))
        listener.move_to(RIGHT*2.45 + DOWN*1.95)
        listener_label = Text("listener", font_size=18, color=orange).next_to(listener, DOWN, buff=.15)

        car = VGroup(RoundedRectangle(width=1.2, height=.46, corner_radius=.12, color=cyan, fill_opacity=1), Circle(radius=.13, color="#09101D", fill_opacity=1).shift(LEFT*.36+DOWN*.28), Circle(radius=.13, color="#09101D", fill_opacity=1).shift(RIGHT*.36+DOWN*.28), Triangle(color=white, fill_opacity=1).scale(.13).rotate(-PI/2).shift(RIGHT*.36))
        car.move_to(LEFT*3.75 + DOWN*2.08)
        siren = Dot(car.get_center()+UP*.35, radius=.07, color=violet)
        car_group = VGroup(car, siren)
        source_label = Text("siren", font_size=18, color=cyan).next_to(car_group, UP, buff=.24)

        caption = Text("Approaching: wavefronts bunch up → higher pitch", font_size=23, color=white).move_to(DOWN*4.55)
        pitch = Text("HIGH PITCH", font_size=29, color=violet, weight="BOLD").move_to(UP*2.2)
        self.play(FadeIn(title), FadeIn(subtitle), Create(road), FadeIn(listener), FadeIn(listener_label), FadeIn(car_group), FadeIn(source_label), FadeIn(caption), FadeIn(pitch), run_time=.7)

        # Wave rings launched from successively closer source positions make the
        # compressed spacing at the listener physically visible.
        approaching = VGroup()
        for x in [-3.4, -2.75, -2.1, -1.45, -.8, -.15, .5, 1.15]:
            ring = Circle(radius=.22, color=violet, stroke_width=4, stroke_opacity=.75).move_to(np.array([x, -2.08, 0]))
            approaching.add(ring)
        self.play(LaggedStart(*[GrowFromCenter(r) for r in approaching], lag_ratio=.11), car_group.animate.shift(RIGHT*3.9), source_label.animate.shift(RIGHT*3.9), run_time=2.6, rate_func=linear)
        self.play(approaching.animate.scale(3.4, about_point=LEFT*3.75 + DOWN*2.08).set_opacity(.3), run_time=.65)

        self.play(FadeOut(approaching), FadeOut(caption), FadeOut(pitch), run_time=.3)
        caption2 = Text("Receding: wavefronts spread out → lower pitch", font_size=23, color=white).move_to(DOWN*4.55)
        pitch2 = Text("LOW PITCH", font_size=29, color=cyan, weight="BOLD").move_to(UP*2.2)
        receding = VGroup()
        for x in [1.4, 2.15, 2.9, 3.65]:
            ring = Circle(radius=.22, color=cyan, stroke_width=4, stroke_opacity=.75).move_to(np.array([x, -2.08, 0]))
            receding.add(ring)
        self.play(FadeIn(caption2), FadeIn(pitch2), LaggedStart(*[GrowFromCenter(r) for r in receding], lag_ratio=.25), car_group.animate.shift(RIGHT*2.1), source_label.animate.shift(RIGHT*2.1), run_time=2.6, rate_func=linear)
        self.play(receding.animate.scale(3.1, about_point=RIGHT*1.2 + DOWN*2.08).set_opacity(.3), run_time=.55)
        formula = MathTex(r"f_{\mathrm{heard}} = f_{\mathrm{source}}\,\frac{v}{v \mp v_s}", font_size=38, color=white).move_to(UP*.75)
        summary = Text("Motion changes the spacing of arriving wavefronts.", font_size=22, color=muted).next_to(formula, DOWN, buff=.22)
        self.play(FadeIn(formula), FadeIn(summary), run_time=.55)
        self.wait(.75)
        self.play(FadeOut(VGroup(title, subtitle, road, listener, listener_label, car_group, source_label, caption2, pitch2, receding, formula, summary)), run_time=.45)
