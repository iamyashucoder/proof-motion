from manim import *

config.frame_height = 14


class InfiniteStaircaseExplainer(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        white, cyan, violet, orange, muted = "#F4F7FF", "#63E6FF", "#9E7BFF", "#FFB654", "#AAB8D0"
        title = Text("THE INFINITE STAIRCASE", font_size=40, color=white, weight="BOLD").to_edge(UP, buff=.6)
        sub = Text("Every side seems to go up.", font_size=21, color=muted).next_to(title, DOWN, buff=.16)
        self.play(FadeIn(title), FadeIn(sub), run_time=.5)

        # A clean top-view loop: its arrows create the illusion of a continuous ascent.
        square = RoundedRectangle(width=5.5, height=5.5, corner_radius=.2, stroke_color=cyan, stroke_width=7)
        square.move_to(DOWN*.25)
        arrows = VGroup()
        labels = VGroup()
        sides = [
            (LEFT*2.1 + DOWN*2.75, RIGHT*2.1 + DOWN*2.75),
            (RIGHT*2.75 + DOWN*2.1, RIGHT*2.75 + UP*2.1),
            (RIGHT*2.1 + UP*2.75, LEFT*2.1 + UP*2.75),
            (LEFT*2.75 + UP*2.1, LEFT*2.75 + DOWN*2.1),
        ]
        for index, (start, end) in enumerate(sides):
            arrow = Arrow(start + DOWN*.25, end + DOWN*.25, buff=.12, color=violet if index % 2 else cyan, stroke_width=6, max_tip_length_to_length_ratio=.12)
            arrows.add(arrow)
            label = Text("UP", font_size=20, color=orange).move_to((start+end)/2 + DOWN*.25)
            labels.add(label)
        self.play(Create(square), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.14), FadeIn(labels), run_time=1.8)

        question = Text("But a closed loop must return to its starting height.", font_size=22, color=white).move_to(DOWN*4.05)
        self.play(FadeIn(question), run_time=.45)
        self.wait(.7)
        self.play(FadeOut(square), FadeOut(arrows), FadeOut(labels), FadeOut(question), FadeOut(sub), run_time=.5)

        # Height bookkeeping makes the contradiction explicit.
        heading = Text("FOLLOW THE HEIGHT", font_size=34, color=white, weight="BOLD").next_to(title, DOWN, buff=.35)
        steps = VGroup()
        data = [("Start", "0"), ("after side 1", "+1"), ("after side 2", "+2"), ("after side 3", "+3"), ("after side 4", "+4")]
        for i, (left, right) in enumerate(data):
            row = VGroup(Text(left, font_size=23, color=muted), Text(right, font_size=27, color=cyan if i < 4 else orange, weight="BOLD"))
            row.arrange(RIGHT, buff=1.1)
            row.move_to(UP*(1.75-i*.82))
            steps.add(row)
        self.play(FadeIn(heading), LaggedStart(*[FadeIn(row, shift=RIGHT*.25) for row in steps], lag_ratio=.18), run_time=1.7)
        verdict = Text("You cannot come back to 0 while always going up.", font_size=25, color=orange, weight="BOLD").move_to(DOWN*3.0)
        self.play(FadeIn(verdict, shift=UP*.15), run_time=.55)
        self.wait(.85)
        self.play(FadeOut(title), FadeOut(heading), FadeOut(steps), FadeOut(verdict), run_time=.5)
