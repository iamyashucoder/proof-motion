from manimlib import *
import numpy as np


class SchrodingerComplex3D(InteractiveScene):
    """Advanced 3D visualization: complex wavefunction, density and tunneling."""

    def construct(self):
        cyan, gold, pink, green = "#4DDCFF", "#FFD54A", "#FF5EA8", "#61E294"

        def caption(text, color=WHITE):
            mob = Text(text, font_size=29, color=color).to_edge(DOWN, buff=.42)
            mob.fix_in_frame()
            return mob

        title = Text("SCHRÖDINGER EQUATION: THE COMPLEX WAVE", font_size=43, color=WHITE).to_edge(UP, buff=.26)
        eq = Text("iℏ ∂ψ/∂t = -(ℏ²/2m) ∂²ψ/∂x² + V(x)ψ", font_size=30, color=gold)
        eq.next_to(title, DOWN, buff=.16)
        line = caption("ψ is complex: it has a real part, an imaginary part, and a phase.")
        for mob in [title, eq, line]: mob.fix_in_frame()

        axes = ThreeDAxes(
            x_range=(-5, 5, 1), y_range=(-1.4, 1.4, 1), z_range=(-1.4, 1.4, 1),
            width=10.3, height=4.8, depth=4.8,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * .35)
        axis_labels = VGroup(
            Text("position x", font_size=22, color=GREY_A).move_to(axes.c2p(5.35, 0, 0)),
            Text("Re(ψ)", font_size=23, color=cyan).move_to(axes.c2p(0, 1.65, 0)),
            Text("Im(ψ)", font_size=23, color=pink).move_to(axes.c2p(0, 0, 1.62)),
        )
        self.frame.reorient(64, -52, 0).move_to(axes.get_center())
        self.play(Write(title), FadeIn(eq), ShowCreation(axes), FadeIn(axis_labels), FadeIn(line), run_time=1.1)

        phase = ValueTracker(0)
        packet = always_redraw(lambda: ParametricCurve(
            lambda x: axes.c2p(x, np.exp(-.11 * (x + .5) ** 2) * np.cos(2.3 * x - phase.get_value()),
                                   np.exp(-.11 * (x + .5) ** 2) * np.sin(2.3 * x - phase.get_value())),
            t_range=(-5, 5, .035), color=cyan, stroke_width=5,
        ))
        complex_caption = caption("As phase changes, the wave rotates through the real–imaginary plane.", cyan)
        self.play(Transform(line, complex_caption), FadeIn(packet), run_time=.8)
        self.play(phase.animate.set_value(2 * PI), run_time=5.0, rate_func=linear)

        # Project magnitude squared onto the base plane.
        density = always_redraw(lambda: ParametricCurve(
            lambda x: axes.c2p(x, -1.22, .75 * np.exp(-.22 * (x + .5) ** 2)),
            t_range=(-5, 5, .035), color=gold, stroke_width=6,
        ))
        density_caption = caption("The measurable quantity is |ψ|²: the probability density.", gold)
        self.play(Transform(line, density_caption), FadeIn(density), run_time=.9)
        self.play(phase.animate.set_value(4 * PI), run_time=4.0, rate_func=linear)

        # Swap to a barrier diagram: finite barrier plus incident/reflected/transmitted amplitudes.
        barrier_axes = Axes(x_range=(-5, 5, 1), y_range=(-1.5, 3, 1), width=11.5, height=5.5,
                            axis_config={"stroke_color": GREY_B, "stroke_width": 2}).shift(DOWN * .55)
        barrier = Rectangle(width=1.0, height=3.2, stroke_width=0, fill_color=GREY_D, fill_opacity=.78)
        barrier.move_to(barrier_axes.c2p(1.1, 1.0))
        barrier_label = Text("potential barrier V(x)", font_size=25, color=GREY_A).next_to(barrier, UP, buff=.12)
        incident = ParametricCurve(lambda x: barrier_axes.c2p(x, .75 * np.sin(3.2 * x)),
                                  t_range=(-4.9, .6, .03), color=cyan, stroke_width=5)
        transmitted = ParametricCurve(lambda x: barrier_axes.c2p(x, .20 * np.exp(-.28 * (x - 1.6)) * np.sin(3.2 * x)),
                                     t_range=(1.6, 4.9, .03), color=pink, stroke_width=5)
        tunnel_caption = caption("A classical particle would stop. A quantum wave leaves a small transmitted amplitude.", pink)
        self.play(FadeOut(VGroup(axes, axis_labels, packet, density, title, eq, line)),
                  FadeIn(barrier_axes), FadeIn(barrier), FadeIn(barrier_label), run_time=1.0)
        self.play(FadeIn(incident), FadeIn(transmitted), FadeIn(tunnel_caption), run_time=1.1)
        self.wait(7.0)

        probability_note = Text("Transmission probability ∝ |transmitted wave|²", font_size=31, color=gold).to_edge(UP, buff=1.0)
        probability_note.fix_in_frame()
        takeaway = caption("This is quantum tunneling—the principle behind tunnel microscopes and nuclear fusion.", green)
        self.play(FadeIn(probability_note), Transform(tunnel_caption, takeaway), run_time=.8)
        self.wait(7.0)

        end_title = Text("QUANTUM WAVES", font_size=58, color=gold).move_to(UP * .40)
        end_text = Text("Complex phase controls interference.\n|ψ|² turns the wave into probabilities.",
                        font_size=34, color=WHITE, line_spacing_height=.86).next_to(end_title, DOWN, buff=.25)
        for mob in [end_title, end_text]: mob.fix_in_frame()
        self.play(FadeOut(VGroup(barrier_axes, barrier, barrier_label, incident, transmitted,
                                 probability_note, tunnel_caption)), FadeIn(end_title), FadeIn(end_text), run_time=1.0)
        self.wait(6.0)
