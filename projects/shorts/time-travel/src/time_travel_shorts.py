from manimlib import *


# Vertical YouTube Short: rendered with manim-vertical-black.yml
class TimeTravelShort(InteractiveScene):
    def glow(self, mob, color, width=18, opacity=.14):
        halo = mob.copy().set_stroke(color, width=width, opacity=opacity)
        halo.set_fill(color, opacity=0)
        return halo

    def label(self, words, y, size=32, color="#F8FBFF"):
        text = Text(words, font_size=size).set_color(color)
        text.move_to(UP * y).fix_in_frame()
        return text

    def make_clock(self, color, radius=.72):
        rim = Circle(radius=radius, stroke_width=4).set_color(color)
        center = Dot(radius=.05).set_color(color)
        hour = Line(ORIGIN, UP * radius * .42, stroke_width=4).set_color(color)
        minute = Line(ORIGIN, RIGHT * radius * .62, stroke_width=3).set_color(color)
        ticks = VGroup(*[
            Line(UP * (radius * .83), UP * radius, stroke_width=2).set_color(color).rotate(k * PI / 6)
            for k in range(12)
        ])
        return VGroup(rim, ticks, hour, minute, center), VGroup(hour, minute)

    def construct(self):
        white = "#F8FBFF"
        cyan = "#4DDCFF"
        violet = "#A66CFF"
        pink = "#FF5EA8"
        gold = "#FFD54A"
        red = "#FF4B4B"
        muted = "#7D8A9A"

        # 0–4 s: hook
        hook = self.label("CAN YOU TRAVEL", 4.95, 45, white)
        hook2 = self.label("THROUGH TIME?", 4.25, 52, gold)
        pulse = Circle(radius=.12, stroke_width=5).set_color(gold).move_to(ORIGIN + DOWN * .25)
        self.play(FadeIn(hook, shift=UP*.15), FadeIn(hook2, shift=UP*.15),
                  GrowFromCenter(pulse), run_time=.8)
        self.play(pulse.animate.scale(19), pulse.animate.set_opacity(0), run_time=.85, rate_func=rush_from)
        self.play(FadeOut(hook), FadeOut(hook2), run_time=.45)

        # 4–14 s: real forward time travel via special relativity.
        header = self.label("1. THE FUTURE IS POSSIBLE", 5.35, 31, cyan)
        caption = self.label("Move close to light speed…", -5.50, 30, white)
        earth = Circle(radius=1.05, stroke_width=5).set_color(cyan).move_to(LEFT*2.05 + DOWN*.35)
        earth_glow = self.glow(earth, cyan, 22, .16)
        land = VGroup(
            Arc(PI*.15, PI*.72, radius=.62, stroke_width=4).set_color(cyan),
            Arc(PI*1.1, PI*.55, radius=.48, stroke_width=4).set_color(cyan),
        ).move_to(earth.get_center())
        earth_name = Text("EARTH", font_size=22).set_color(cyan).next_to(earth, DOWN, buff=.20)
        earth_clock, earth_hands = self.make_clock(cyan, .55)
        earth_clock.move_to(earth.get_center())

        ship = VGroup(
            Triangle(fill_opacity=1, stroke_width=2).set_color(pink).scale(.33).rotate(-PI/2),
            Line(LEFT*.52, RIGHT*.18, stroke_width=4).set_color(pink),
        ).move_to(RIGHT*2.2 + UP*.4)
        ship_glow = self.glow(ship, pink, 20, .18)
        ship_clock, ship_hands = self.make_clock(pink, .55)
        ship_clock.move_to(ship.get_center() + DOWN*1.30)
        ship_name = Text("SHIP", font_size=22).set_color(pink).next_to(ship_clock, DOWN, buff=.15)
        speed_line = Arrow(ship.get_left()+LEFT*.2, ship.get_left()+LEFT*1.25, buff=0, thickness=3).set_color(pink)
        speed = Text("0.99c", font_size=28).set_color(gold).next_to(ship, UP, buff=.24)

        self.play(FadeIn(header), FadeIn(caption), FadeIn(earth_glow), FadeIn(earth),
                  FadeIn(land), FadeIn(earth_clock), FadeIn(earth_name),
                  FadeIn(ship_glow), FadeIn(ship), FadeIn(ship_clock), FadeIn(ship_name),
                  FadeIn(speed_line), FadeIn(speed), run_time=1.0)
        self.play(Rotate(earth_hands, -2*PI, about_point=earth_clock.get_center()),
                  Rotate(ship_hands, -PI*.38, about_point=ship_clock.get_center()),
                  ship.animate.shift(RIGHT*.55), ship_glow.animate.shift(RIGHT*.55),
                  speed_line.animate.shift(RIGHT*.55), speed.animate.shift(RIGHT*.55),
                  run_time=2.8, rate_func=linear)
        slow = self.label("…your clock ticks slower.", -5.50, 30, gold)
        self.play(ReplacementTransform(caption, slow), run_time=.45)
        equation = Text("time dilation", font_size=38).set_color(white).move_to(UP*2.3)
        equation2 = Text("Δt = γ Δτ", font_size=44).set_color(gold).next_to(equation, DOWN, buff=.20)
        self.play(FadeIn(equation), FadeIn(equation2), run_time=.6)
        self.wait(.7)
        self.play(FadeOut(VGroup(header, slow, earth_glow, earth, land, earth_clock, earth_name,
                                  ship_glow, ship, ship_clock, ship_name, speed_line, speed,
                                  equation, equation2)), run_time=.65)

        # 14–23 s: wormhole as a hypothetical shortcut.
        header = self.label("2. A WORMHOLE?", 5.35, 36, violet)
        caption = self.label("A shortcut through spacetime — hypothetical.", -5.50, 27, white)
        rings = VGroup(*[
            Circle(radius=.52 + .24*k, stroke_width=4-k*.35).set_color(
                violet if k % 2 == 0 else cyan
            ) for k in range(8)
        ])
        rings.rotate(PI/2, axis=RIGHT).move_to(ORIGIN + DOWN*.10)
        tunnel_glow = self.glow(rings, violet, 22, .16)
        stars = VGroup(*[
            Dot(np.array([np.random.uniform(-3.4, 3.4), np.random.uniform(-3.8, 3.7), 0]), radius=.022)
            .set_color(white) for _ in range(70)
        ])
        particle = Dot(radius=.13).set_color(gold).move_to(LEFT*3.2 + DOWN*.1)
        approach = CurvedArrow(particle.get_center(), RIGHT*1.2 + DOWN*.1, angle=-PI/3, stroke_width=4).set_color(gold)
        self.play(FadeIn(header), FadeIn(caption), FadeIn(stars), FadeIn(tunnel_glow), FadeIn(rings),
                  FadeIn(particle), ShowCreation(approach), run_time=1.0)
        self.play(Rotate(rings, 2*PI, axis=UP), particle.animate.move_to(RIGHT*3.25 + DOWN*.1),
                  FadeOut(approach), run_time=2.4, rate_func=linear)
        warning = self.label("But no stable wormhole has ever been found.", -5.50, 26, red)
        self.play(ReplacementTransform(caption, warning), run_time=.45)
        self.play(FadeOut(VGroup(header, warning, stars, tunnel_glow, rings, particle)), run_time=.65)

        # 23–34 s: why backward travel causes paradoxes.
        header = self.label("3. THE PAST IS A PROBLEM", 5.35, 34, red)
        caption = self.label("Changing the past creates paradoxes.", -5.50, 29, white)
        timeline = Line(LEFT*3.25 + DOWN*.2, RIGHT*3.25 + DOWN*.2, stroke_width=5).set_color(white)
        past = Text("PAST", font_size=24).set_color(muted).next_to(timeline.get_left(), DOWN, buff=.22)
        now = Text("NOW", font_size=24).set_color(gold).next_to(timeline.get_center(), DOWN, buff=.22)
        future = Text("FUTURE", font_size=24).set_color(cyan).next_to(timeline.get_right(), DOWN, buff=.22)
        traveler = Dot(radius=.13).set_color(gold).move_to(timeline.get_right())
        loop = Arc(start_angle=0, angle=TAU*.78, radius=1.42, stroke_width=5).set_color(violet)
        loop.move_to(ORIGIN + UP*1.15)
        paradox = Text("Can you change what made you exist?", font_size=31).set_color(red).move_to(UP*2.8)
        self.play(FadeIn(header), FadeIn(caption), ShowCreation(timeline),
                  FadeIn(past), FadeIn(now), FadeIn(future), FadeIn(traveler), run_time=.8)
        self.play(ShowCreation(loop), traveler.animate.move_to(timeline.get_left()), run_time=1.8, rate_func=smooth)
        self.play(FadeIn(paradox, shift=UP*.12), Flash(timeline.get_left(), color=red, flash_radius=.42), run_time=.6)
        branch_a = Line(timeline.get_center(), RIGHT*2.65 + UP*1.7, stroke_width=4).set_color(cyan)
        branch_b = Line(timeline.get_center(), RIGHT*2.65 + DOWN*1.7, stroke_width=4).set_color(pink)
        branches = Text("OR: branching timelines", font_size=31).set_color(gold).move_to(DOWN*3.25)
        self.play(ShowCreation(branch_a), ShowCreation(branch_b), FadeIn(branches), run_time=.9)
        self.wait(.65)
        self.play(FadeOut(VGroup(header, caption, timeline, past, now, future, traveler, loop, paradox,
                                  branch_a, branch_b, branches)), run_time=.65)

        # 34–40 s: conclusion.
        end1 = self.label("TO THE FUTURE?", 1.05, 50, cyan)
        end2 = self.label("PHYSICS SAYS YES.", .20, 49, gold)
        end3 = self.label("TO THE PAST?", -1.35, 48, pink)
        end4 = self.label("WE DON'T KNOW.", -2.20, 48, white)
        end_line = Line(LEFT*2.75 + DOWN*3.15, RIGHT*2.75 + DOWN*3.15, stroke_width=3).set_color(violet)
        tag = Text("TIME TRAVEL", font_size=28).set_color(violet).next_to(end_line, DOWN, buff=.25)
        self.play(FadeIn(end1, shift=UP*.18), FadeIn(end2, shift=UP*.18), run_time=.65)
        self.play(FadeIn(end3, shift=UP*.18), FadeIn(end4, shift=UP*.18), run_time=.65)
        self.play(ShowCreation(end_line), FadeIn(tag), run_time=.5)
        self.wait(2.0)
        self.play(FadeOut(VGroup(end1, end2, end3, end4, end_line, tag)), run_time=.6)
