from manim import *

config.frame_height = 14


class AristotleReferenceStyle(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        cyan, green, wood, silver, yellow = "#12DAF4", "#39F06D", "#B9794B", "#D4D8DE", "#FFD166"

        # Faint technical grid, matching the supplied reference language.
        grid = VGroup()
        for x in np.arange(-7, 7.1, 1.25):
            grid.add(Line([x, -7, 0], [x, 7, 0], stroke_color="#20242B", stroke_width=1))
        for y in np.arange(-7, 7.1, 1.25):
            grid.add(Line([-7, y, 0], [7, y, 0], stroke_color="#20242B", stroke_width=1))
        heading = Text("Paradox Explained", font_size=42, slant=ITALIC, weight="BOLD", t2c={"Paradox": green, "Explained": cyan}).to_edge(UP, buff=.65)

        def wheel(radius, spokes, label=None):
            outer = Circle(radius=radius, stroke_color=wood, stroke_width=9)
            inner = Circle(radius=radius*.20, stroke_color=wood, stroke_width=6)
            hub = Dot(radius=.12, color="#121419", stroke_color=silver, stroke_width=2)
            bars = VGroup()
            for i in range(spokes):
                a = TAU*i/spokes
                bars.add(Line(radius*.20*np.array([np.cos(a), np.sin(a), 0]), radius*.88*np.array([np.cos(a), np.sin(a), 0]), stroke_color=silver, stroke_width=6))
            group = VGroup(outer, bars, inner, hub)
            if label:
                label_obj = Text(label, font_size=25, slant=ITALIC, color=WHITE)
                return group, label_obj
            return group

        big, big_text = wheel(1.12, 9, "A big wheel")
        small, small_text = wheel(.55, 8, "the small wheel")
        big.move_to(LEFT*2.4+UP*.2)
        small.move_to(LEFT*2.4+DOWN*2.1)
        big_text.next_to(big, DOWN, buff=.55)
        small_text.next_to(small, DOWN, buff=.55)

        self.add(grid)
        self.play(FadeIn(heading), FadeIn(big), FadeIn(big_text), run_time=.65)
        self.wait(.7)
        self.play(FadeIn(small), FadeIn(small_text), run_time=.55)
        self.wait(.65)

        # Bring the small wheel into the big one: the two circles share one axle.
        nested_big = wheel(1.43, 9)
        nested_small = wheel(.70, 8)
        nested_big.move_to(ORIGIN+UP*.05)
        nested_small.move_to(ORIGIN+UP*.05)
        together = VGroup(nested_big, nested_small)
        closer = Text("Let's look closer", font_size=26, slant=ITALIC, color=WHITE).move_to(DOWN*3.3)
        self.play(FadeOut(big_text), FadeOut(small_text), Transform(big, nested_big), Transform(small, nested_small), FadeIn(closer), run_time=.8)
        self.wait(.8)

        # Set the wheel on paired coloured tracks. The identical rotation later
        # appears to create two different path lengths.
        track_y1, track_y2 = -1.55, -2.45
        line1 = Line(LEFT*6.2+UP*track_y1, RIGHT*6.2+UP*track_y1, color=cyan, stroke_width=4)
        line2 = Line(LEFT*6.2+UP*track_y2, RIGHT*6.2+UP*track_y2, color=green, stroke_width=4)
        self.play(FadeOut(closer), together.animate.move_to(LEFT*3.8+UP*.1), Create(line1), Create(line2), run_time=.8)

        tracker = ValueTracker(0)
        start = LEFT*3.8+UP*.1
        def rolling_pair():
            theta = tracker.get_value()
            pos = start + RIGHT*(1.43*theta)
            g = together.copy().move_to(pos).rotate(-theta, about_point=pos)
            return g
        rolling = always_redraw(rolling_pair)
        self.remove(together)
        self.add(rolling)
        phrase1 = Text("Both make one full rotation...", font_size=26, slant=ITALIC, color=WHITE).move_to(DOWN*3.6)
        self.play(FadeIn(phrase1), tracker.animate.set_value(TAU), run_time=4.0, rate_func=linear)

        big_path = BraceBetweenPoints(LEFT*3.8+UP*(track_y1+.35), LEFT*3.8+RIGHT*(TAU*1.43)+UP*(track_y1+.35), color=cyan)
        small_path = BraceBetweenPoints(LEFT*3.8+UP*(track_y2-.35), LEFT*3.8+RIGHT*(TAU*.70)+UP*(track_y2-.35), color=green)
        unequal = Text("...but their circumferences are not equal.", font_size=25, slant=ITALIC, color=WHITE).move_to(DOWN*3.6)
        self.play(FadeOut(phrase1), Create(big_path), Create(small_path), FadeIn(unequal), run_time=.8)
        self.wait(.75)

        final = Text("Only the big wheel rolls without slipping.", font_size=27, slant=ITALIC, color=yellow).move_to(DOWN*4.35)
        self.play(FadeIn(final), run_time=.5)
        self.wait(1.2)
        self.play(FadeOut(VGroup(grid, heading, rolling, line1, line2, big_path, small_path, unequal, final)), run_time=.45)
