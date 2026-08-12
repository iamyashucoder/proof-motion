from manimlib import *
import numpy as np


class CinematicTimeTravel(InteractiveScene):
    """Stylized deep-space time-travel Short, designed for vertical 9:16."""

    def fixed_text(self, words, point, size, color):
        mob = Text(words, font_size=size).set_color(color).move_to(point)
        mob.fix_in_frame()
        return mob

    def construct(self):
        white, blue, cyan, violet, pink, gold, red = (
            "#F8FBFF", "#265BFF", "#4DDCFF", "#975CFF", "#FF4FA3", "#FFD54A", "#FF5858"
        )
        rng = np.random.default_rng(18)
        self.frame.reorient(70, -35, 0).move_to(ORIGIN)

        # A layered starfield makes the black space feel deep rather than flat.
        stars = Group()
        for _ in range(190):
            point = np.array([rng.uniform(-6.3, 6.3), rng.uniform(-6.8, 6.8), rng.uniform(-4, 4)])
            dot = Dot(point, radius=rng.uniform(.007, .025)).set_color(white)
            dot.set_opacity(rng.uniform(.25, .95))
            stars.add(dot)
        nebula = VGroup(
            Circle(radius=4.6, stroke_width=36).set_color(violet).set_opacity(.035).shift(LEFT*2.6 + UP*.6 + IN*2),
            Circle(radius=3.0, stroke_width=26).set_color(cyan).set_opacity(.035).shift(RIGHT*2.5 + DOWN*.8 + OUT*1),
        )
        self.add(stars, nebula)

        # 0–8 s: Earth clock versus a departing ship.
        opening = self.fixed_text("TIME TRAVEL", UP*5.55, 50, white)
        opening_sub = self.fixed_text("IS THE FUTURE ALREADY REACHABLE?", UP*4.92, 24, gold)
        earth = Sphere(radius=1.28, resolution=(26, 48)).set_color(blue).set_opacity(.92)
        earth.shift(LEFT*2.25 + DOWN*.70 + IN*.55)
        atmosphere = Sphere(radius=1.40, resolution=(22, 42)).set_color(cyan).set_opacity(.12)
        atmosphere.move_to(earth.get_center())
        orbit = Circle(radius=1.95, stroke_width=3).set_color(cyan).set_opacity(.62)
        orbit.rotate(65*DEGREES, axis=RIGHT).move_to(earth.get_center())
        # A visible clock floats above the planet.
        clock = Circle(radius=.70, stroke_width=5).set_color(gold).move_to(earth.get_center() + UP*1.95 + OUT*.35)
        clock_ticks = VGroup(*[
            Line(UP*.55, UP*.68, stroke_width=2).set_color(gold).rotate(k*PI/6)
            for k in range(12)
        ]).move_to(clock.get_center())
        hand1 = Line(clock.get_center(), clock.get_center()+UP*.34, stroke_width=5).set_color(gold)
        hand2 = Line(clock.get_center(), clock.get_center()+RIGHT*.47, stroke_width=3).set_color(gold)
        ship = VGroup(
            Triangle(fill_opacity=1, stroke_width=1).set_color(pink).scale(.34).rotate(-PI/2),
            Line(LEFT*.52, RIGHT*.18, stroke_width=5).set_color(pink),
            Line(LEFT*.72+UP*.10, LEFT*.18+UP*.10, stroke_width=2).set_color(cyan),
            Line(LEFT*.72+DOWN*.10, LEFT*.18+DOWN*.10, stroke_width=2).set_color(cyan),
        ).move_to(RIGHT*1.15 + DOWN*.2 + OUT*.9)
        ship_glow = ship.copy().set_stroke(pink, width=20, opacity=.18).set_fill(pink, opacity=.12)
        engine = Line(ship.get_left()+LEFT*.1, ship.get_left()+LEFT*1.35, stroke_width=8).set_color(violet)
        earth_label = self.fixed_text("EARTH TIME", LEFT*2.25 + DOWN*3.15, 25, cyan)
        ship_label = self.fixed_text("SHIP TIME", RIGHT*1.45 + DOWN*2.0, 25, pink)
        bottom = self.fixed_text("Move near light speed — and time slows for you.", DOWN*5.55, 27, white)
        self.play(FadeIn(opening, shift=UP*.14), FadeIn(opening_sub, shift=UP*.14),
                  FadeIn(earth), FadeIn(atmosphere), FadeIn(orbit), FadeIn(clock), FadeIn(clock_ticks),
                  FadeIn(hand1), FadeIn(hand2), FadeIn(ship_glow), FadeIn(ship), FadeIn(engine),
                  FadeIn(earth_label), FadeIn(ship_label), FadeIn(bottom), run_time=1.0)
        self.play(Rotate(VGroup(hand1, hand2), -2*PI, about_point=clock.get_center()),
                  ship.animate.shift(RIGHT*3.0 + OUT*1.4), ship_glow.animate.shift(RIGHT*3.0 + OUT*1.4),
                  engine.animate.shift(RIGHT*3.0 + OUT*1.4),
                  self.frame.animate.reorient(72, -55, 0), run_time=2.8, rate_func=smooth)
        future = self.fixed_text("FORWARD TIME TRAVEL IS REAL.", UP*5.55, 31, cyan)
        self.play(Transform(opening, future), run_time=.55)
        self.play(FadeOut(Group(opening, opening_sub, earth, atmosphere, orbit, clock, clock_ticks, hand1, hand2,
                                ship_glow, ship, engine, earth_label, ship_label, bottom)), run_time=.75)

        # 8–19 s: dense glowing tunnel and a camera fly through its centre.
        worm_title = self.fixed_text("BUT CAN WE GO BACK?", UP*5.55, 38, white)
        worm_sub = self.fixed_text("A WORMHOLE IS A THEORETICAL SHORTCUT.", UP*4.94, 24, violet)
        tunnel = Group()
        for k in range(27):
            z = -8 + .58*k
            radius = .52 + .095*abs(13-k)
            ring = Circle(radius=radius, stroke_width=3.5).set_color(violet if k % 3 else cyan)
            ring.shift(OUT*z)
            tunnel.add(ring)
        core = Sphere(radius=.28, resolution=(16, 28)).set_color(gold).move_to(IN*8.1)
        traveler = Sphere(radius=.16, resolution=(12, 20)).set_color(pink).move_to(OUT*7.6)
        trail = Line(OUT*7.6, OUT*4.5, stroke_width=10).set_color(pink).set_opacity(.45)
        bottom2 = self.fixed_text("The equations allow it. Nature may not.", DOWN*5.55, 28, gold)
        self.frame.reorient(72, -5, 0).move_to(OUT*2.0)
        self.play(FadeIn(worm_title), FadeIn(worm_sub), FadeIn(tunnel), FadeIn(core), FadeIn(traveler),
                  FadeIn(trail), FadeIn(bottom2), run_time=1.0)
        self.play(traveler.animate.move_to(IN*5.7), trail.animate.shift(IN*10.6),
                  Rotate(tunnel, PI*.34, axis=OUT),
                  self.frame.animate.move_to(IN*3.2).reorient(74, 11, 0), run_time=4.2, rate_func=smooth)
        unstable = self.fixed_text("NO STABLE WORMHOLE HAS BEEN OBSERVED.", DOWN*5.55, 25, red)
        self.play(Transform(bottom2, unstable), core.animate.scale(2.0), run_time=.65)
        self.play(FadeOut(Group(worm_title, worm_sub, tunnel, core, traveler, trail, bottom2)), run_time=.75)

        # 19–29 s: physical-looking time loop and branching histories in depth.
        paradox = self.fixed_text("THE PAST CREATES A PARADOX", UP*5.55, 35, red)
        paradox_sub = self.fixed_text("Change one moment… and which future survives?", DOWN*5.55, 27, white)
        loop = ParametricCurve(
            lambda t: np.array([2.35*np.cos(t), .75*np.sin(2*t), 1.55*np.sin(t)]),
            t_range=(0, TAU, .02), stroke_width=7,
        ).set_color(violet)
        loop_glow = loop.copy().set_stroke(violet, width=22, opacity=.16)
        event = Sphere(radius=.20, resolution=(12, 20)).set_color(gold).move_to(LEFT*2.35)
        branch1 = ParametricCurve(lambda t: np.array([-1.2+3.8*t, -.25+.9*t, .15+1.8*t]),
                                  t_range=(0, 1, .02), stroke_width=6).set_color(cyan)
        branch2 = ParametricCurve(lambda t: np.array([-1.2+3.8*t, -.25-1.25*t, .15-1.7*t]),
                                  t_range=(0, 1, .02), stroke_width=6).set_color(pink)
        self.frame.reorient(66, -48, 0).move_to(ORIGIN)
        self.play(FadeIn(paradox), FadeIn(paradox_sub), FadeIn(loop_glow), ShowCreation(loop), FadeIn(event), run_time=1.0)
        self.play(event.animate.move_to(RIGHT*2.35), self.frame.animate.reorient(66, -5, 0), run_time=1.8, rate_func=smooth)
        branches = self.fixed_text("ONE PAST → MANY POSSIBLE FUTURES", DOWN*5.55, 27, gold)
        self.play(ShowCreation(branch1), ShowCreation(branch2), Transform(paradox_sub, branches), run_time=1.0)
        self.wait(.6)
        self.play(FadeOut(Group(paradox, paradox_sub, loop_glow, loop, event, branch1, branch2)), run_time=.7)

        # 29–35 s: clean closing statement.
        self.frame.reorient(0, 0, 0).move_to(ORIGIN)
        end_a = self.fixed_text("TO THE FUTURE?", UP*.95, 50, cyan)
        end_b = self.fixed_text("YES.", UP*.12, 62, gold)
        end_c = self.fixed_text("TO THE PAST?", DOWN*1.35, 50, pink)
        end_d = self.fixed_text("STILL A MYSTERY.", DOWN*2.25, 42, white)
        self.play(FadeIn(end_a, shift=UP*.15), FadeIn(end_b, shift=UP*.15), run_time=.6)
        self.play(FadeIn(end_c, shift=UP*.15), FadeIn(end_d, shift=UP*.15), run_time=.6)
        self.wait(2.0)
        self.play(FadeOut(Group(stars, nebula, end_a, end_b, end_c, end_d)), run_time=.65)
