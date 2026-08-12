from manimlib import *
import numpy as np


class SchrodingerWaveEquation(InteractiveScene):
    """Horizontal visual explanation of the 1D time-dependent Schrödinger equation."""

    def construct(self):
        cyan, gold, pink, green = "#4DDCFF", "#FFD54A", "#FF5EA8", "#61E294"

        def caption(text, color=WHITE):
            mob = Text(text, font_size=30, color=color).to_edge(DOWN, buff=.40)
            mob.fix_in_frame()
            return mob

        title = Text("SCHRÖDINGER'S WAVE EQUATION", font_size=48, color=WHITE).to_edge(UP, buff=.30)
        equation = Text("iℏ ∂ψ/∂t = -(ℏ²/2m) ∂²ψ/∂x² + V(x)ψ", font_size=34, color=gold)
        equation.next_to(title, DOWN, buff=.18)
        explanation = caption("This equation predicts how a quantum wavefunction changes over time.")
        for mob in [title, equation, explanation]: mob.fix_in_frame()
        self.play(Write(title), FadeIn(equation), FadeIn(explanation), run_time=1.1)
        self.wait(3.2)

        axes = Axes(x_range=(-5, 5, 1), y_range=(-2.2, 2.7, 1), width=11.5, height=5.7,
                    axis_config={"stroke_color": GREY_B, "stroke_width": 2}).shift(DOWN * .55)
        x_label = Text("position x", font_size=24, color=GREY_A).move_to(axes.c2p(5.25, 0))
        y_label = Text("energy / amplitude", font_size=23, color=GREY_A).move_to(axes.c2p(-5.5, 2.45))
        self.play(ShowCreation(axes), FadeIn(x_label), FadeIn(y_label), run_time=.9)

        # A finite potential well: outside energy is high, inside is low.
        potential = VMobject(color=GREY_A, stroke_width=5)
        potential.set_points_as_corners([
            axes.c2p(-5, 1.85), axes.c2p(-2.8, 1.85), axes.c2p(-2.8, -.55),
            axes.c2p(2.8, -.55), axes.c2p(2.8, 1.85), axes.c2p(5, 1.85),
        ])
        potential_label = Text("V(x): potential energy", font_size=26, color=GREY_A).move_to(axes.c2p(0, 2.15))
        potential_caption = caption("V(x) describes the environment: here, a particle is confined in a potential well.", cyan)
        self.play(Transform(explanation, potential_caption), ShowCreation(potential), FadeIn(potential_label), run_time=1.1)
        self.wait(4.0)

        # ψ is a wave, not directly a probability curve.
        phase = ValueTracker(0)
        wave = always_redraw(lambda: ParametricCurve(
            lambda x: axes.c2p(x, .72 * np.cos(1.55 * x - phase.get_value()) * np.exp(-.075 * x * x)),
            t_range=(-2.75, 2.75, .035), color=cyan, stroke_width=5,
        ))
        wave_label = Text("ψ(x,t): wavefunction", font_size=27, color=cyan).move_to(axes.c2p(-3.7, .95))
        wave_caption = caption("ψ is a complex probability amplitude. Its sign and phase can interfere.", cyan)
        self.play(Transform(explanation, wave_caption), FadeIn(wave), FadeIn(wave_label), run_time=.9)
        self.play(phase.animate.set_value(2 * PI), run_time=4.0, rate_func=linear)

        # |ψ|² is the measurable probability density.
        density = always_redraw(lambda: ParametricCurve(
            lambda x: axes.c2p(x, -1.55 + .75 * (np.cos(1.55 * x - phase.get_value()) ** 2) * np.exp(-.15 * x * x)),
            t_range=(-2.75, 2.75, .035), color=pink, stroke_width=6,
        ))
        density_label = Text("|ψ|²: probability density", font_size=27, color=pink).move_to(axes.c2p(-3.25, -1.25))
        density_caption = caption("Square the magnitude: |ψ|² tells where the particle is most likely to be found.", pink)
        self.play(Transform(explanation, density_caption), FadeIn(density), FadeIn(density_label), run_time=1.0)
        self.play(phase.animate.set_value(4 * PI), run_time=4.0, rate_func=linear)

        terms = VGroup(
            Text("iℏ ∂ψ/∂t", font_size=34, color=gold),
            Text("time evolution", font_size=24, color=GREY_A),
            Text("-(ℏ²/2m) ∂²ψ/∂x²", font_size=34, color=cyan),
            Text("spreading and curvature", font_size=24, color=GREY_A),
            Text("V(x)ψ", font_size=34, color=pink),
            Text("effect of the environment", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=.10).to_corner(UR, buff=.32)
        terms.fix_in_frame()
        term_caption = caption("The equation balances time evolution, wave curvature, and potential energy.", green)
        self.play(Transform(explanation, term_caption), FadeIn(terms, shift=LEFT * .12), run_time=1.0)
        self.wait(6.0)

        final_title = Text("QUANTUM PREDICTION", font_size=55, color=gold).move_to(UP * .45)
        final_text = Text("The wavefunction evolves smoothly.\nMeasurements reveal probabilities, not certainties.",
                          font_size=34, color=WHITE, line_spacing_height=.85).next_to(final_title, DOWN, buff=.28)
        for mob in [final_title, final_text]: mob.fix_in_frame()
        self.play(FadeOut(VGroup(axes, x_label, y_label, potential, potential_label, wave, wave_label,
                                 density, density_label, title, equation, explanation, terms)),
                  FadeIn(final_title, scale=.85), FadeIn(final_text, shift=UP * .15), run_time=1.0)
        self.wait(6.0)
