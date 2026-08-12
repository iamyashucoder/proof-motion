from manimlib import *
import numpy as np


class GaussianWavePacketAdvanced(InteractiveScene):
    """30-second advanced vertical Gaussian packet story."""

    def construct(self):
        blue, green, violet, gold, red, white = "#38BDF8", "#55F28A", "#A78BFA", "#FFD54A", "#FF425F", "#F8FBFF"
        t = ValueTracker(0)
        title = Text("Gaussian Wave Packet Evolution", font_size=38, color=white).to_edge(UP, buff=.34)
        title.fix_in_frame()
        sub = Text("complex phase • dispersion • nonlinearity", font_size=23, color=GREY_A).next_to(title, DOWN, buff=.10)
        sub.fix_in_frame()
        upper_axis = Line(LEFT * 3.65 + UP * 2.25, RIGHT * 3.65 + UP * 2.25, color="#2C3955", stroke_width=2)
        lower_grid = NumberPlane(x_range=(-4, 4, 1), y_range=(-3, 3, 1), width=7.4, height=4.3,
                                 background_line_style={"stroke_color": "#17243C", "stroke_width": 1},
                                 axis_config={"stroke_color": "#263653", "stroke_width": 1}).shift(DOWN * 3.65)
        lower_label = Text("Position x  →        time history / probability density", font_size=22, color=GREY_A).move_to(DOWN * 1.13)
        lower_label.fix_in_frame()
        eq = Text("iℏ ∂Ψ/∂t = -ℏ²/(2m) ∂²Ψ/∂x² + g|Ψ|²Ψ", font_size=22, color=white).move_to(DOWN * 1.48)
        eq.fix_in_frame()

        def state():
            s = t.get_value()
            center = -3.1 + 6.2 * s
            sigma = .35 + .95 * np.sin(PI * s)
            k = 4 + 9 * np.sin(PI * s)
            return s, center, sigma, k

        def env(x):
            _, c, sig, _ = state()
            return np.exp(-((x - c) ** 2) / (2 * sig ** 2))

        def helix(color, phase):
            _, c, sig, k = state()
            lo, hi = max(-3.65, c - 3 * sig), min(3.65, c + 3 * sig)
            return ParametricCurve(lambda x: np.array([x, 2.25 + .70 * env(x) * np.sin(k * (x-c) + phase),
                                                        .24 * env(x) * np.cos(k * (x-c) + phase)]),
                                   t_range=(lo, hi, .035), color=color, stroke_width=4)

        real = always_redraw(lambda: helix(blue, 0))
        imag = always_redraw(lambda: helix(green, PI / 2))
        envelope = always_redraw(lambda: VGroup(
            ParametricCurve(lambda x: np.array([x, 2.25 + .73 * env(x), 0]), t_range=(-3.65, 3.65, .04), color=violet, stroke_width=2),
            ParametricCurve(lambda x: np.array([x, 2.25 - .73 * env(x), 0]), t_range=(-3.65, 3.65, .04), color=violet, stroke_width=2),
        ))
        center_glow = always_redraw(lambda: Dot(np.array([state()[1], 2.25, 0]), radius=.11, color=white))
        carrier = always_redraw(lambda: Dot(np.array([state()[1]-.46, 2.25, 0]), radius=.065, color=red))
        probability = always_redraw(lambda: ParametricCurve(
            lambda x: np.array([x, -3.75 + .95 * env(x) ** 2, 0]), t_range=(-3.65, 3.65, .04), color=gold, stroke_width=6))

        self.play(FadeIn(center_glow, scale=.3), run_time=.5)
        self.play(FadeIn(title), FadeIn(sub), ShowCreation(upper_axis), ShowCreation(lower_grid), FadeIn(lower_label), FadeIn(eq), run_time=1.5)
        self.play(FadeIn(envelope), FadeIn(real), FadeIn(imag), FadeIn(carrier), FadeIn(probability), run_time=1.0)
        # 0–12 s: broadening and phase rotation.
        self.play(t.animate.set_value(.50), self.frame.animate.scale(.94), run_time=10.0, rate_func=smooth)
        max_note = Text("Maximum dispersion", font_size=27, color=gold).move_to(UP * .75); max_note.fix_in_frame()
        self.play(FadeIn(max_note, scale=.8), t.animate.set_value(.68), run_time=3.0, rate_func=smooth)
        self.play(FadeOut(max_note), t.animate.set_value(.88), self.frame.animate.scale(1/.94), run_time=4.0, rate_func=smooth)

        # Final comparison: linear spreads, nonlinear remains localized.
        linear = Text("Linear evolution\npacket spreads", font_size=25, color=blue).move_to(LEFT * 2.0 + DOWN * .2)
        nonlinear = Text("Nonlinear evolution\nself-focusing", font_size=25, color=green).move_to(RIGHT * 1.9 + DOWN * .2)
        for mob in [linear, nonlinear]: mob.fix_in_frame()
        self.play(FadeIn(linear), FadeIn(nonlinear), t.animate.set_value(1.05), run_time=4.0, rate_func=smooth)
        end = Text("Simple equations. Complex dynamics.", font_size=34, color=gold).move_to(DOWN * .25); end.fix_in_frame()
        self.play(FadeOut(VGroup(real, imag, envelope, probability, carrier, center_glow, upper_axis, lower_grid, lower_label, eq, sub, linear, nonlinear)),
                  Transform(title, end), run_time=1.5)
        self.wait(2.0)
