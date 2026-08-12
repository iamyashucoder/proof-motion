from manim import *

config.frame_height = 14


class GeometricStaircaseExplainer(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        white, cyan, violet, orange, muted = "#F4F7FF", "#63E6FF", "#9E7BFF", "#FFB654", "#AAB8D0"
        title = Text("THE INFINITE STAIRCASE", font_size=40, color=white, weight="BOLD").to_edge(UP, buff=.6)
        subtitle = Text("Infinitely many steps can fit in finite space.", font_size=21, color=muted).next_to(title, DOWN, buff=.14)
        self.play(FadeIn(title), FadeIn(subtitle), run_time=.5)

        baseline, x, height = DOWN*2.8 + LEFT*3.5, -3.5, -2.8
        steps = VGroup()
        terms = [2.7, 1.35, .675, .338, .169, .085]
        for i, size in enumerate(terms):
            height += size
            rect = Rectangle(width=size, height=height+2.8, stroke_color=cyan if i % 2 == 0 else violet, stroke_width=4, fill_color=cyan if i % 2 == 0 else violet, fill_opacity=.75)
            rect.move_to(np.array([x + size/2, -2.8 + (height+2.8)/2, 0]))
            steps.add(rect)
            x += size
        brace = BraceBetweenPoints(np.array([-3.5, -3.2, 0]), np.array([2.0, -3.2, 0]), direction=DOWN, color=orange)
        total = Text("finite total length", font_size=20, color=orange).next_to(brace, DOWN, buff=.12)
        self.play(LaggedStart(*[GrowFromEdge(step, DOWN) for step in steps], lag_ratio=.16), run_time=1.5)
        self.play(GrowFromCenter(brace), FadeIn(total), run_time=.45)

        series = MathTex(r"\frac12 + \frac14 + \frac18 + \frac1{16} + \cdots = 1", font_size=45, color=white).move_to(UP*.9)
        self.play(Write(series), run_time=.8)
        statement = Text("Each new step is half the previous step.", font_size=23, color=muted).move_to(DOWN*4.25)
        self.play(FadeIn(statement), run_time=.35)
        self.wait(.8)
        self.play(FadeOut(subtitle), FadeOut(steps), FadeOut(brace), FadeOut(total), FadeOut(series), FadeOut(statement), run_time=.5)

        conclusion = Text("The steps never stop — but the distance does.", font_size=31, color=orange, weight="BOLD").move_to(UP*.4)
        final = MathTex(r"\sum_{n=1}^{\infty}\left(\frac12\right)^n = 1", font_size=56, color=cyan).next_to(conclusion, DOWN, buff=.45)
        self.play(FadeIn(conclusion, shift=UP*.2), Write(final), run_time=1.0)
        self.wait(1.1)
        self.play(FadeOut(title), FadeOut(conclusion), FadeOut(final), run_time=.5)
