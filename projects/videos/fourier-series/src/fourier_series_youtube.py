from manimlib import *
import numpy as np


class FourierSeriesYouTube(InteractiveScene):
    """~2-minute horizontal Fourier-series lesson with 3D harmonic diagrams."""

    def construct(self):
        cyan, gold, pink, green = "#4DDCFF", "#FFD54A", "#FF5EA8", "#61E294"
        colors = [cyan, gold, pink, green]

        def fixed_text(text, size=30, color=WHITE, location=DOWN * 3.35):
            mob = Text(text, font_size=size, color=color).move_to(location)
            mob.fix_in_frame()
            return mob

        title = Text("Fourier Series: Building Any Periodic Wave", font_size=46, color=WHITE).to_edge(UP, buff=.28)
        title.fix_in_frame()
        hook = fixed_text("How can smooth sine waves build a sharp square wave?", 34, gold)
        self.play(Write(title), FadeIn(hook, shift=UP * .15), run_time=1.2)
        self.wait(3.0)

        axes = ThreeDAxes(
            x_range=(-PI, PI, PI), y_range=(-2.2, 2.4, 1), z_range=(-1.8, 1.8, 1),
            width=10.0, height=5.5, depth=5.5,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * .25)
        self.frame.reorient(61, -47, 0).move_to(axes.get_center())
        labels = VGroup(
            Text("position x", font_size=22, color=GREY_A).move_to(axes.c2p(PI + .35, 0, 0)),
            Text("harmonic layer", font_size=22, color=GREY_A).move_to(axes.c2p(0, 2.7, 0)),
            Text("amplitude", font_size=22, color=GREY_A).move_to(axes.c2p(0, 0, 2.05)),
        )
        intro = fixed_text("A Fourier series represents a repeating signal as a sum of simple sine and cosine waves.", 28)
        self.play(FadeOut(hook), ShowCreation(axes), FadeIn(labels), FadeIn(intro), run_time=1.3)
        self.wait(4.0)

        formula = Text("f(x) = a₀ + Σ [ aₙ cos(nx) + bₙ sin(nx) ]", font_size=32, color=gold)
        formula.to_edge(UP, buff=1.00).fix_in_frame()
        self.play(FadeIn(formula, shift=DOWN * .12), run_time=.8)
        self.wait(4.0)

        # 3D stack of the first four odd sine harmonics of a square wave.
        odd = [1, 3, 5, 7]
        layers = [1.75, .82, -.10, -1.02]
        waves, wave_labels = VGroup(), VGroup()
        component_caption = fixed_text("For a square wave, only odd sine harmonics are needed.", 29, cyan)
        self.play(Transform(intro, component_caption), run_time=.6)
        for n, layer, color in zip(odd, layers, colors):
            wave = ParametricCurve(
                lambda x, n=n, layer=layer: axes.c2p(x, layer, np.sin(n * x) / n),
                t_range=(-PI, PI, .03), color=color, stroke_width=4,
            )
            label = Text(f"sin({n}x) / {n}", font_size=24, color=color).move_to(axes.c2p(-PI - .38, layer, 0))
            waves.add(wave); wave_labels.add(label)
            self.play(ShowCreation(wave), FadeIn(label), run_time=1.1)
            self.wait(1.6)

        coefficient_caption = fixed_text("The coefficient 1/n makes higher-frequency waves weaker.", 29, gold)
        self.play(Transform(intro, coefficient_caption), run_time=.6)
        self.wait(5.0)

        # Accumulate the square-wave approximation in a front layer.
        def partial(x, count):
            return 4 / PI * sum(np.sin(n * x) / n for n in odd[:count])

        sum_layer = -1.88
        partial_curve = ParametricCurve(
            lambda x: axes.c2p(x, sum_layer, partial(x, 1)),
            t_range=(-PI, PI, .03), color=WHITE, stroke_width=6,
        )
        sum_label = Text("partial sum", font_size=24, color=WHITE).move_to(axes.c2p(-PI - .38, sum_layer, 0))
        build_caption = fixed_text("Now add the harmonics. The first wave gives only a rough outline.", 29, WHITE)
        self.play(Transform(intro, build_caption), ShowCreation(partial_curve), FadeIn(sum_label), run_time=1.3)
        self.wait(4.0)

        for count in [2, 3, 4]:
            next_curve = ParametricCurve(
                lambda x, count=count: axes.c2p(x, sum_layer, partial(x, count)),
                t_range=(-PI, PI, .03), color=WHITE, stroke_width=6,
            )
            term = Text(f"+ sin({odd[count - 1]}x)/{odd[count - 1]}", font_size=27, color=colors[count - 1])
            term.to_edge(DOWN, buff=.55).fix_in_frame()
            glow = waves[count - 1].copy().set_stroke(width=14, opacity=.20)
            self.play(Transform(intro, term), FadeIn(glow), Transform(partial_curve, next_curve), FadeOut(glow), run_time=1.7)
            self.wait(3.5)

        gibbs_caption = fixed_text("The small ripples near corners are called the Gibbs phenomenon.", 29, pink)
        self.play(Transform(intro, gibbs_caption), self.frame.animate.reorient(72, -66, 0), run_time=1.3)
        self.wait(5.0)

        coefficient_panel = VGroup(
            Text("For this square wave:", font_size=31, color=WHITE),
            Text("amplitude of sin(nx) = 4 / (πn)", font_size=30, color=gold),
            Text("n = 1, 3, 5, 7, ...", font_size=29, color=cyan),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.18).to_corner(UR, buff=.38)
        coefficient_panel.fix_in_frame()
        derivation_caption = fixed_text("Fourier coefficients measure how much of each frequency is present.", 29, green)
        self.play(FadeIn(coefficient_panel, shift=LEFT * .16), Transform(intro, derivation_caption), run_time=1.0)
        self.wait(7.0)

        orthogonality_caption = fixed_text(
            "Sine and cosine waves are orthogonal: each frequency can be measured independently.", 28, cyan)
        self.play(Transform(intro, orthogonality_caption), run_time=.7)
        self.wait(8.0)

        measurement_caption = fixed_text(
            "The Fourier coefficient is the strength of that frequency inside the original signal.", 28, gold)
        self.play(Transform(intro, measurement_caption), run_time=.7)
        self.wait(8.0)

        resolution_caption = fixed_text(
            "Adding more harmonics improves detail, but sharp jumps always retain a tiny overshoot.", 28, pink)
        self.play(Transform(intro, resolution_caption), run_time=.7)
        self.wait(8.0)

        application_caption = fixed_text("This idea powers audio compression, image processing, heat flow, and signal analysis.", 28, gold)
        self.play(Transform(intro, application_caption), run_time=.7)
        self.wait(6.0)

        final_formula = Text("square wave = 4/π [sin(x) + sin(3x)/3 + sin(5x)/5 + …]", font_size=31, color=green)
        final_formula.to_edge(UP, buff=1.0).fix_in_frame()
        conclusion = fixed_text("Complex periodic shapes are built from simple rotating waves.", 32, WHITE)
        self.play(FadeOut(formula), Transform(coefficient_panel, final_formula), Transform(intro, conclusion), run_time=1.0)
        self.wait(7.0)

        end_title = Text("FOURIER SERIES", font_size=58, color=gold).move_to(UP * .35)
        end_text = Text("Break a periodic signal into frequencies.\nAdd the frequencies to rebuild the signal.",
                        font_size=34, color=WHITE, line_spacing_height=.86).next_to(end_title, DOWN, buff=.28)
        for mob in [end_title, end_text]: mob.fix_in_frame()
        self.play(
            FadeOut(VGroup(axes, labels, waves, wave_labels, partial_curve, sum_label, formula, coefficient_panel, intro)),
            FadeIn(end_title, scale=.85), FadeIn(end_text, shift=UP * .15), run_time=1.0,
        )
        self.wait(10.0)
