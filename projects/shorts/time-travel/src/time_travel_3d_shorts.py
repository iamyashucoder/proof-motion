from manimlib import *
import numpy as np


class TimeTravel3DShort(InteractiveScene):
    """A 9:16, perspective-first time-travel YouTube Short."""

    def hud(self, words, position, size=30, color=WHITE):
        text = Text(words, font_size=size).set_color(color).move_to(position)
        text.fix_in_frame()
        return text

    def construct(self):
        white, cyan, violet, pink, gold, red, grid = (
            "#F8FBFF", "#4DDCFF", "#A66CFF", "#FF5EA8", "#FFD54A", "#FF4B4B", "#506074"
        )
        self.frame.reorient(62, -48, 0).move_to(ORIGIN)

        title = self.hud("CAN YOU TRAVEL THROUGH TIME?", UP*5.55, 40, white)
        sub = self.hud("Physics gives a surprising answer.", UP*4.93, 28, gold)
        self.play(FadeIn(title, shift=UP*.16), FadeIn(sub, shift=UP*.16), run_time=.7)

        # 0–11 s: a 3D spacetime grid and diverging clock/world lines.
        axes = ThreeDAxes(
            x_range=(-4, 4, 1), y_range=(-2.5, 3, 1), z_range=(-2.5, 2.5, 1),
            width=8, height=5.5, depth=5,
            axis_config={"stroke_color": grid, "stroke_width": 2},
        ).shift(DOWN*.35)
        axis_words = VGroup(
            Text("space", font_size=22).set_color(cyan).move_to(axes.c2p(4.45, -2.3, 0)),
            Text("time", font_size=22).set_color(gold).move_to(axes.c2p(-3.8, 3.2, 0)),
        )
        earth = Sphere(radius=.52, resolution=(18, 32)).set_color(cyan).set_opacity(.82)
        earth.move_to(axes.c2p(-2.5, -1.25, 0))
        ship = VGroup(
            Triangle(fill_opacity=1).set_color(pink).scale(.27).rotate(-PI/2),
            Line(LEFT*.42, RIGHT*.2, stroke_width=3).set_color(pink),
        ).move_to(axes.c2p(-2.5, -1.25, .18))
        earth_tag = Text("EARTH", font_size=21).set_color(cyan).move_to(axes.c2p(-2.5, -1.9, 0))
        ship_tag = Text("SHIP", font_size=21).set_color(pink).move_to(axes.c2p(-2.5, -1.9, .45))
        earth_worldline = ParametricCurve(
            lambda t: axes.c2p(-2.5, -1.2 + 3.65*t, 0), t_range=(0, 1, .02),
            stroke_width=6,
        ).set_color(cyan)
        ship_worldline = ParametricCurve(
            lambda t: axes.c2p(-2.5 + 4.5*t, -1.2 + 1.65*t, .7*np.sin(PI*t)), t_range=(0, 1, .02),
            stroke_width=6,
        ).set_color(pink)
        clock_note = self.hud("Near light speed, your clock runs slower.", DOWN*5.55, 28, gold)
        self.play(FadeOut(Group(title, sub)), FadeIn(axes), FadeIn(axis_words), FadeIn(earth), FadeIn(ship),
                  FadeIn(earth_tag), FadeIn(ship_tag), FadeIn(clock_note), run_time=.8)
        self.play(ShowCreation(earth_worldline), ShowCreation(ship_worldline),
                  ship.animate.move_to(axes.c2p(2.0, .45, .0)),
                  self.frame.animate.reorient(67, -60, 0), run_time=3.6, rate_func=smooth)
        dilation = self.hud("FUTURE TRAVEL: REAL", UP*5.55, 34, cyan)
        factor = self.hud("Δt = γ Δτ", UP*4.95, 39, gold)
        self.play(FadeIn(dilation), FadeIn(factor), run_time=.5)
        self.wait(.7)
        self.play(FadeOut(Group(axes, axis_words, earth, ship, earth_tag, ship_tag, earth_worldline,
                                  ship_worldline, clock_note, dilation, factor)), run_time=.65)

        # 11–22 s: a real 3D wormhole tunnel, with camera orbit.
        worm_title = self.hud("A WORMHOLE?", UP*5.55, 43, violet)
        worm_text = self.hud("A hypothetical shortcut through curved spacetime.", DOWN*5.55, 27, white)
        rings = VGroup()
        for k in range(12):
            radius = .45 + .12*k
            ring = Circle(radius=radius, stroke_width=3.5).set_color(violet if k % 2 else cyan)
            ring.rotate(PI/2, axis=RIGHT)
            ring.shift(OUT * (-2.0 + .34*k))
            rings.add(ring)
        core = Sphere(radius=.32, resolution=(14, 28)).set_color(gold).move_to(IN*1.9)
        traveler = Sphere(radius=.14, resolution=(12, 20)).set_color(pink).move_to(OUT*2.3)
        tunnel_axis = Line(IN*2.6, OUT*2.6, stroke_width=2).set_color(white).set_opacity(.45)
        self.frame.reorient(70, -35, 0).move_to(ORIGIN)
        self.play(FadeIn(worm_title), FadeIn(worm_text), FadeIn(tunnel_axis), FadeIn(rings),
                  FadeIn(core), FadeIn(traveler), run_time=1.0)
        self.play(traveler.animate.move_to(IN*2.3), Rotate(rings, PI*.75, axis=OUT),
                  self.frame.animate.reorient(72, 18, 0), run_time=3.2, rate_func=smooth)
        warning = self.hud("We have never found a stable one.", DOWN*5.55, 29, red)
        self.play(Transform(worm_text, warning), core.animate.scale(1.55), run_time=.55)
        self.play(FadeOut(Group(worm_title, worm_text, tunnel_axis, rings, core, traveler)), run_time=.65)

        # 22–33 s: a 3D timeline bends back and splits into alternate histories.
        paradox_title = self.hud("THE PAST CREATES PARADOXES", UP*5.55, 32, red)
        paradox_text = self.hud("What happens if you change your own past?", DOWN*5.55, 28, white)
        self.frame.reorient(62, -48, 0).move_to(ORIGIN)
        time_axis = Arrow(LEFT*3.4 + DOWN*.8, RIGHT*3.4 + DOWN*.8, buff=0, thickness=4).set_color(white)
        loop = ParametricCurve(
            lambda t: np.array([1.2*np.cos(t), .15 + .7*np.sin(t), 1.2*np.sin(t)]),
            t_range=(PI*.05, TAU*1.05, .025), stroke_width=6,
        ).set_color(violet)
        past_dot = Sphere(radius=.16, resolution=(12, 20)).set_color(gold).move_to(RIGHT*2.7 + DOWN*.8)
        branch_one = Line(ORIGIN + DOWN*.8, RIGHT*2.7 + UP*1.45 + OUT*1.0, stroke_width=5).set_color(cyan)
        branch_two = Line(ORIGIN + DOWN*.8, RIGHT*2.7 + DOWN*2.45 + IN*1.0, stroke_width=5).set_color(pink)
        past_label = Text("PAST", font_size=23).set_color(violet).move_to(LEFT*3 + DOWN*1.35)
        future_label = Text("FUTURE", font_size=23).set_color(cyan).move_to(RIGHT*2.7 + DOWN*1.35)
        self.play(FadeIn(paradox_title), FadeIn(paradox_text), ShowCreation(time_axis),
                  FadeIn(past_dot), FadeIn(past_label), FadeIn(future_label), run_time=.8)
        self.play(ShowCreation(loop), past_dot.animate.move_to(LEFT*3.0 + DOWN*.8),
                  self.frame.animate.reorient(64, -12, 0), run_time=2.1, rate_func=smooth)
        split = self.hud("Maybe reality branches instead.", DOWN*5.55, 29, gold)
        self.play(ShowCreation(branch_one), ShowCreation(branch_two), Transform(paradox_text, split), run_time=1.0)
        self.wait(.5)
        self.play(FadeOut(Group(paradox_title, paradox_text, time_axis, loop, past_dot, branch_one,
                                  branch_two, past_label, future_label)), run_time=.65)

        # 33–39 s: final answer.
        self.frame.reorient(0, 0, 0).move_to(ORIGIN)
        end1 = self.hud("TO THE FUTURE?", UP*.90, 48, cyan)
        end2 = self.hud("YES — RELATIVITY ALLOWS IT.", UP*.08, 39, gold)
        end3 = self.hud("TO THE PAST?", DOWN*1.45, 48, pink)
        end4 = self.hud("STILL UNSOLVED.", DOWN*2.28, 42, white)
        self.play(FadeIn(end1, shift=UP*.15), FadeIn(end2, shift=UP*.15), run_time=.6)
        self.play(FadeIn(end3, shift=UP*.15), FadeIn(end4, shift=UP*.15), run_time=.6)
        self.wait(2.2)
        self.play(FadeOut(Group(end1, end2, end3, end4)), run_time=.55)
