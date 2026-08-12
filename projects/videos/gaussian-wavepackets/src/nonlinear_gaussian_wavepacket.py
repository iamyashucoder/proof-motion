from manimlib import *
import numpy as np


class NonlinearGaussianWavePacket(InteractiveScene):
    """22-second 9:16 visualization of a nonlinear Gaussian wave packet."""

    def construct(self):
        blue, green, violet, red, gold, white = "#38BDF8", "#55F28A", "#9B7BFF", "#FF425F", "#FFD54A", "#F8FBFF"
        phase_time = ValueTracker(0)

        # Fixed scientific labels.
        title = Text("Gaussian Wave Packet Evolution", font="Helvetica Neue", font_size=37, color=white).to_edge(UP, buff=.35)
        upper_eq = Text("Ψ(x,t) = A exp[-(x-vt)²/(2σ²)] exp[i(kx-ωt)]", font="Times New Roman", font_size=22, color=white)
        upper_eq.next_to(title, DOWN, buff=.13)
        lower_title = Text("Nonlinear Schrödinger Equation", font="Helvetica Neue", font_size=29, color=white).move_to(DOWN * .65)
        lower_eq = Text("iℏ ∂Ψ/∂t = -ℏ²/(2m) ∂²Ψ/∂x² + g|Ψ|²Ψ", font="Times New Roman", font_size=23, color=white)
        lower_eq.next_to(lower_title, DOWN, buff=.12)
        for mob in [title, upper_eq, lower_title, lower_eq]:
            mob.fix_in_frame()

        # Upper 3D complex-wave axes.
        upper_axes = ThreeDAxes(
            x_range=(-3.7, 3.7, 1), y_range=(-1.15, 1.15, 1), z_range=(-1.15, 1.15, 1),
            width=7.1, height=2.5, depth=2.4,
            axis_config={"stroke_color": "#34415C", "stroke_width": 1.4},
        ).shift(UP * 2.3)

        # Lower region: receding grid in a low perspective-like trapezoid.
        grid = VGroup()
        for y in np.linspace(-5.9, -2.05, 8):
            factor = (y + 6.1) / 4.1
            grid.add(Line(LEFT * (3.85 - .9 * factor) + UP * y, RIGHT * (3.85 - .9 * factor) + UP * y,
                          color="#18233A", stroke_width=1))
        for x in np.linspace(-3.8, 3.8, 13):
            grid.add(Line(np.array([x * .72, -5.95, 0]), np.array([x, -2.05, 0]), color="#18233A", stroke_width=1))

        def state():
            # A single normalized timeline avoids resetting the packet at the
            # edge of the frame, so propagation remains visually continuous.
            s = phase_time.get_value()
            center = -2.85 + 5.75 * s
            sigma = .40 + 1.02 * np.sin(PI * s) ** 1.15
            freq = 3.2 + 10.0 * np.sin(PI * s)
            phase = 2 * PI * (1.25 * s)
            return s, center, sigma, freq, phase

        # Restore the original single, continuous packet.
        packet_offsets = [0.0]

        def packet_envelope(x, offset=0):
            _, center, sigma, _, _ = state()
            return np.exp(-((x - (center + offset)) ** 2) / (2 * sigma ** 2))

        def envelope(x):
            return min(1.0, sum(packet_envelope(x, offset) for offset in packet_offsets))

        def upper_helix(packet_offset=0, phase_offset=0, color=blue):
            _, center, sigma, freq, phase = state()
            center += packet_offset
            lo, hi = max(-3.55, center - 3 * sigma), min(3.55, center + 3 * sigma)
            return ParametricCurve(
                lambda x: upper_axes.c2p(x, .83 * packet_envelope(x, packet_offset) * np.cos(freq * (x - center) - phase + phase_offset),
                                      .83 * packet_envelope(x, packet_offset) * np.sin(freq * (x - center) - phase + phase_offset)),
                t_range=(lo, hi, .045), color=color, stroke_width=4,
            )

        real_helix = always_redraw(lambda: VGroup(*[upper_helix(offset, 0, blue) for offset in packet_offsets]))
        imag_helix = always_redraw(lambda: VGroup(*[upper_helix(offset, PI / 2, green) for offset in packet_offsets]))
        envelope_top = always_redraw(lambda: VGroup(*[
            ParametricCurve(lambda x, offset=offset: upper_axes.c2p(x, .85 * packet_envelope(x, offset), 0),
                            t_range=(-3.55, 3.55, .045), color=violet, stroke_width=2)
            for offset in packet_offsets
        ]))
        envelope_bottom = always_redraw(lambda: VGroup(*[
            ParametricCurve(lambda x, offset=offset: upper_axes.c2p(x, -.85 * packet_envelope(x, offset), 0),
                            t_range=(-3.55, 3.55, .045), color=violet, stroke_width=2)
            for offset in packet_offsets
        ]))
        packet_center = always_redraw(lambda: VGroup(*[
            Dot(upper_axes.c2p(state()[1] + offset, 0, 0), radius=.075, color=white)
            for offset in packet_offsets if -3.6 < state()[1] + offset < 3.6
        ]))
        trailing_point = always_redraw(lambda: Dot(upper_axes.c2p(state()[1] - .68, 0, -.12), radius=.065, color=red))
        phase_ring = always_redraw(lambda: Circle(
            radius=.10 + .045 * np.sin(2 * PI * phase_time.get_value()) ** 2,
            color=gold, stroke_width=3,
        ).move_to(upper_axes.c2p(state()[1], 0, 0)))

        # A layered lower amplitude surface: synchronized with the upper packet.
        def surface():
            _, center, sigma, freq, phase = state()
            ridges = VGroup()
            for depth in np.linspace(-.56, .56, 11):
                curve = ParametricCurve(
                    lambda x, depth=depth: np.array([
                        .95 * x,
                        -4.22 + 1.25 * depth + .52 * np.exp(-((x - center) ** 2) / (2 * sigma ** 2))
                        * (1 + .58 * np.cos(freq * (x - center) - phase + 3 * depth)),
                        0,
                    ]),
                    t_range=(-3.55, 3.55, .06),
                    color=blue if depth < 0 else green,
                    stroke_width=2.3,
                )
                ridges.add(curve)
            return ridges

        lower_surface = always_redraw(surface)
        lower_hotspot = always_redraw(lambda: VGroup(*[
            Dot(np.array([.95 * (state()[1] + offset), -4.22, 0]), radius=.08, color=white)
            for offset in packet_offsets if -3.6 < state()[1] + offset < 3.6
        ]))
        lower_glow = always_redraw(lambda: Circle(radius=.16, color=gold, stroke_width=3, stroke_opacity=.65)
                                   .move_to(np.array([.95 * state()[1], -4.22, 0])))

        # A very shallow perspective reveals the upper helix out of its plane
        # while preserving the lower grid's centred, readable layout.
        self.frame.reorient(12, -10, 0).move_to(ORIGIN)
        self.play(FadeIn(title), FadeIn(upper_eq), FadeIn(lower_title), FadeIn(lower_eq),
                  ShowCreation(upper_axes), ShowCreation(grid), FadeIn(real_helix), FadeIn(imag_helix),
                  FadeIn(envelope_top), FadeIn(envelope_bottom), FadeIn(packet_center), FadeIn(trailing_point),
                  FadeIn(phase_ring), FadeIn(lower_surface), FadeIn(lower_hotspot), FadeIn(lower_glow), run_time=2.0)

        # One continuous, unbroken propagation cycle.
        self.play(phase_time.animate.set_value(.50), self.frame.animate.scale(.96), run_time=9.0, rate_func=smooth)
        self.play(phase_time.animate.set_value(.73), run_time=5.0, rate_func=smooth)
        self.play(phase_time.animate.set_value(.92), self.frame.animate.scale(1 / .96), run_time=4.0, rate_func=smooth)
        # The packet exits and every panel fades to black.
        self.play(phase_time.animate.set_value(1.08),
                  FadeOut(VGroup(real_helix, imag_helix, envelope_top, envelope_bottom, packet_center,
                                 trailing_point, phase_ring, lower_surface, lower_hotspot, lower_glow, upper_axes, grid,
                                 title, upper_eq, lower_title, lower_eq)),
                  run_time=2.0, rate_func=smooth)
