from manimlib import *
import numpy as np


class FourierSeries3DExplainer(InteractiveScene):
    """A vertical 3D visual explanation of Fourier series using a square wave."""

    def construct(self):
        cyan = "#4DDCFF"
        gold = "#FFD54A"
        pink = "#FF5EA8"
        green = "#61E294"
        colors = [cyan, gold, pink, green]

        title = Text("FOURIER SERIES IN 3D", font_size=46, color=WHITE).to_edge(UP, buff=.42)
        formula = Text("f(x) = a₀ + Σ[aₙ cos(nx) + bₙ sin(nx)]", font_size=27, color=gold)
        formula.next_to(title, DOWN, buff=.18)
        theory = Text("Any repeating shape can be built from simple waves.", font_size=28, color=GREY_A)
        theory.to_edge(DOWN, buff=.48)
        for mob in [title, formula, theory]:
            mob.fix_in_frame()

        axes = ThreeDAxes(
            x_range=(-PI, PI, PI), y_range=(-2.2, 2.5, 1), z_range=(-1.7, 1.7, 1),
            width=6.7, height=5.2, depth=6.0,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * .45)
        x_label = Text("x", font_size=25, color=GREY_A).move_to(axes.c2p(PI + .22, 0, 0))
        layer_label = Text("harmonic", font_size=23, color=GREY_A).move_to(axes.c2p(0, 2.65, 0))
        amplitude_label = Text("amplitude", font_size=23, color=GREY_A).move_to(axes.c2p(0, 0, 1.9))

        self.frame.reorient(62, -48, 0).move_to(axes.get_center() + UP * .15)
        self.play(Write(title), FadeIn(formula), ShowCreation(axes), FadeIn(x_label), FadeIn(layer_label),
                  FadeIn(amplitude_label), FadeIn(theory), run_time=.7)

        odd_harmonics = [1, 3, 5, 7]
        layers = [1.8, .85, -.05, -.95]
        waves = VGroup()
        labels = VGroup()
        for n, layer, color in zip(odd_harmonics, layers, colors):
            wave = ParametricCurve(
                lambda x, n=n, layer=layer: axes.c2p(x, layer, (1 / n) * np.sin(n * x)),
                t_range=(-PI, PI, .035), color=color, stroke_width=4,
            )
            label = Text(f"sin({n}x) / {n}", font_size=23, color=color).move_to(axes.c2p(-PI - .3, layer, 0))
            waves.add(wave)
            labels.add(label)

        components_caption = Text("Each layer is one harmonic. Higher frequencies have smaller strength.",
                                  font_size=26, color=WHITE).to_edge(DOWN, buff=.48)
        components_caption.fix_in_frame()
        for wave, label in zip(waves, labels):
            self.play(ShowCreation(wave), FadeIn(label, shift=RIGHT * .08), run_time=.28)
        self.play(Transform(theory, components_caption), run_time=.25)

        def square_partial_sum(x, count):
            return 4 / PI * sum(np.sin(n * x) / n for n in odd_harmonics[:count])

        sum_layer = -1.85
        base_curve = ParametricCurve(
            lambda x: axes.c2p(x, sum_layer, square_partial_sum(x, 1)),
            t_range=(-PI, PI, .035), color=WHITE, stroke_width=6,
        )
        sum_label = Text("partial sum", font_size=25, color=WHITE).move_to(axes.c2p(-PI - .35, sum_layer, 0))
        build_caption = Text("Add the waves: each extra harmonic sharpens the corners.",
                             font_size=27, color=gold).to_edge(DOWN, buff=.48)
        build_caption.fix_in_frame()
        self.play(Transform(theory, build_caption), ShowCreation(base_curve), FadeIn(sum_label), run_time=.45)

        current_sum = base_curve
        for count, color in zip([2, 3, 4], colors[1:]):
            next_sum = ParametricCurve(
                lambda x, count=count: axes.c2p(x, sum_layer, square_partial_sum(x, count)),
                t_range=(-PI, PI, .035), color=WHITE, stroke_width=6,
            )
            pulse = waves[count - 1].copy().set_stroke(width=11, opacity=.22)
            self.play(FadeIn(pulse), Transform(current_sum, next_sum), FadeOut(pulse), run_time=.42)

        square_caption = Text("More terms → a better approximation of the square wave.",
                              font_size=27, color=green).to_edge(DOWN, buff=.48)
        square_caption.fix_in_frame()
        square_formula = Text("square wave ≈ 4/π[sin(x) + sin(3x)/3 + sin(5x)/5 + …]",
                              font_size=25, color=green).next_to(formula, DOWN, buff=.16)
        square_formula.fix_in_frame()
        self.play(Transform(theory, square_caption), FadeIn(square_formula),
                  self.frame.animate.reorient(70, -68, 0), run_time=.65)
        self.wait(.55)

        final_title = Text("FOURIER SERIES", font_size=55, color=gold).move_to(UP * .55)
        final_text = Text("Complex periodic signals\nare sums of simple rotations.", font_size=34, color=WHITE,
                          line_spacing_height=.88).next_to(final_title, DOWN, buff=.28)
        for mob in [final_title, final_text]:
            mob.fix_in_frame()
        self.play(
            FadeOut(VGroup(axes, waves, labels, current_sum, sum_label, x_label, layer_label,
                           amplitude_label, title, formula, square_formula, theory)),
            FadeIn(final_title, scale=.85), FadeIn(final_text, shift=UP * .12), run_time=.55,
        )
        self.wait(.9)
