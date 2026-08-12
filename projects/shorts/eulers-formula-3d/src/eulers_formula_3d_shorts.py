from manimlib import *
import numpy as np


class EulersFormula3DShort(InteractiveScene):
    """Vertical YouTube Short: Euler's formula as circle + time helix."""

    def construct(self):
        cyan = "#4DDCFF"
        gold = "#FFD54A"
        pink = "#FF5EA8"

        # Fixed captions stay readable while the 3D camera moves.
        title = Text("EULER'S FORMULA IN 3D", font_size=48, color=WHITE).to_edge(UP, buff=.45)
        formula = Text("e^(iθ) = cos(θ) + i sin(θ)", font_size=36, color=gold)
        formula.next_to(title, DOWN, buff=.22)
        formula.fix_in_frame()
        title.fix_in_frame()

        theory = Text("A rotating point on the unit circle", font_size=30, color=GREY_A)
        theory.to_edge(DOWN, buff=.52).fix_in_frame()

        axes = ThreeDAxes(
            x_range=(-1.6, 1.6, 1),
            y_range=(-1.6, 1.6, 1),
            z_range=(0, 7, 1),
            width=5.8,
            height=5.8,
            depth=6.8,
            axis_config={"stroke_color": GREY_B, "stroke_width": 2},
        ).shift(DOWN * .45)
        x_label = Text("real", font_size=24, color=GREY_A).move_to(axes.c2p(1.65, 0, 0))
        y_label = Text("imaginary", font_size=24, color=GREY_A).move_to(axes.c2p(0, 1.72, 0))
        theta_label = Text("θ", font_size=30, color=GREY_A).move_to(axes.c2p(0, 0, 7.35))

        unit_circle = ParametricCurve(
            lambda t: axes.c2p(np.cos(t), np.sin(t), 0),
            t_range=(0, TAU, 0.04), color=GREY_B, stroke_width=3,
        )
        self.frame.reorient(58, -42, 0).move_to(axes.get_center() + UP * .10)
        self.play(Write(title), FadeIn(formula), ShowCreation(axes), ShowCreation(unit_circle),
                  FadeIn(x_label), FadeIn(y_label), FadeIn(theta_label), FadeIn(theory), run_time=1.2)

        angle = ValueTracker(0)

        def circle_point():
            t = angle.get_value()
            return axes.c2p(np.cos(t), np.sin(t), 0)

        radial = always_redraw(lambda: Arrow(axes.c2p(0, 0, 0), circle_point(), buff=0, color=cyan, stroke_width=6))
        point = always_redraw(lambda: Dot(circle_point(), radius=.10, color=gold))
        real_component = always_redraw(lambda: Line(
            axes.c2p(0, 0, 0), axes.c2p(np.cos(angle.get_value()), 0, 0),
            color=cyan, stroke_width=6,
        ))
        imaginary_component = always_redraw(lambda: Line(
            axes.c2p(np.cos(angle.get_value()), 0, 0), circle_point(),
            color=pink, stroke_width=6,
        ))
        projection = always_redraw(lambda: DashedLine(
            circle_point(), axes.c2p(np.cos(angle.get_value()), np.sin(angle.get_value()), angle.get_value() / TAU * 6.2),
            color=GREY_B, stroke_width=2,
        ))
        components_note = Text("cos(θ) = real     i sin(θ) = imaginary", font_size=29, color=WHITE)
        components_note.to_edge(DOWN, buff=.52).fix_in_frame()
        self.play(FadeIn(radial), FadeIn(point), FadeIn(real_component), FadeIn(imaginary_component), run_time=.5)
        self.play(Transform(theory, components_note), angle.animate.set_value(TAU), run_time=2.8, rate_func=linear)

        helix = ParametricCurve(
            lambda t: axes.c2p(np.cos(t), np.sin(t), t / TAU * 6.2),
            t_range=(0, 2 * TAU, 0.04), color=pink, stroke_width=5,
        )
        helix_note = Text("Add time: the circle becomes a helix", font_size=30, color=pink)
        helix_note.to_edge(DOWN, buff=.52).fix_in_frame()
        self.play(Transform(theory, helix_note), ShowCreation(helix), FadeIn(projection), run_time=1.4)
        self.play(angle.animate.set_value(2 * TAU), run_time=3.4, rate_func=linear)

        takeaway = Text("One rotation traces every complex number of length 1", font_size=29, color=gold)
        takeaway.to_edge(DOWN, buff=.52).fix_in_frame()
        self.play(Transform(theory, takeaway), self.frame.animate.reorient(70, -65, 0), run_time=1.2)
        self.wait(.7)

        # The famous special case makes the formula feel resolved, not merely
        # visual: half a turn lands exactly at -1.
        identity_heading = Text("HALF A TURN: θ = π", font_size=35, color=GREY_A).to_edge(UP, buff=1.35)
        identity = Text("e^(iπ) + 1 = 0", font_size=60, color=gold).move_to(ORIGIN)
        identity_note = Text("Euler's identity", font_size=32, color=pink).next_to(identity, DOWN, buff=.28)
        for mob in [identity_heading, identity, identity_note]:
            mob.fix_in_frame()
        self.play(
            FadeOut(VGroup(axes, unit_circle, helix, radial, point, real_component, imaginary_component, projection,
                           x_label, y_label, theta_label, title, formula, theory)),
            FadeIn(identity_heading, shift=UP * .15), FadeIn(identity, scale=.85), FadeIn(identity_note),
            run_time=1.0,
        )
        self.wait(1.5)
