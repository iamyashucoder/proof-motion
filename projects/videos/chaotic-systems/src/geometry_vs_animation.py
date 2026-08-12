import numpy as np

from manimlib import *


class GeometryVsAnimation(InteractiveScene):
    """An original vertical action short: animation versus procedural geometry."""

    default_camera_config = {
        "background_color": "#05070D",
        "resolution": (1080, 1920),
    }

    def construct(self):
        orange = "#FF8A32"
        white = "#F7F8FF"
        gold = "#FFD35A"

        def stick_figure(center, pose="stand", scale=1.0, carrying_phi=False):
            # Explicit joints give each run pose a real weight-bearing stance.
            # The character faces right: the torso leans forward while arms
            # counter-swing against the legs.
            poses = {
                "stand": [
                    (0, 0), (0, .60), (-.24, .36), (-.30, .06), (.22, .36), (.31, .08),
                    (-.17, -.38), (-.21, -.78), (.18, -.38), (.25, -.78),
                ],
                "lean": [
                    (0, 0), (.14, .56), (-.12, .30), (-.34, .12), (.42, .54), (.64, .28),
                    (-.10, -.38), (-.34, -.70), (.34, -.18), (.59, -.56),
                ],
                "run_a": [
                    # Contact: both feet meet the road with near-straight legs.
                    (0, 0), (.14, .55), (.27, .38), (.35, .22), (-.13, .40), (-.25, .25),
                    (-.10, -.35), (-.18, -.68), (.10, -.34), (.20, -.68),
                ],
                "run_b": [
                    # Lift: right knee rises and bends after its foot leaves the road.
                    (0, 0), (.13, .57), (-.13, .39), (-.25, .23), (.27, .41), (.35, .25),
                    (-.10, -.35), (-.18, -.68), (.20, -.12), (.34, -.48),
                ],
                "run_c": [
                    # Opposite contact, with the step transferred to the other side.
                    (0, 0), (.13, .57), (-.13, .39), (-.25, .23), (.27, .41), (.35, .25),
                    (.10, -.34), (.20, -.68), (-.10, -.35), (-.18, -.68),
                ],
                "run_d": [
                    # The trailing leg stays straight; only the forward swing bends.
                    (0, 0), (.14, .55), (.27, .38), (.35, .22), (-.13, .40), (-.25, .25),
                    (.20, -.12), (.34, -.48), (-.09, -.34), (-.18, -.68),
                ],
                # A complete, right-facing run cycle.  fleeing_figure mirrors
                # these poses so the runner travels left on screen.
                "run_contact_a": [
                    (0, 0), (.13, .55), (.30, .34), (.42, .16), (-.12, .36), (-.27, .20),
                    (.18, -.34), (.32, -.69), (-.17, -.32), (-.31, -.65),
                ],
                "run_compression_a": [
                    (0, 0), (.13, .55), (.19, .36), (.24, .20), (-.03, .38), (-.10, .26),
                    (.10, -.26), (.30, -.68), (-.10, -.22), (-.20, -.53),
                ],
                "run_passing_a": [
                    (0, 0), (.13, .55), (.08, .39), (.03, .25), (.08, .39), (.14, .25),
                    (.02, -.36), (.04, -.69), (.28, -.07), (.19, -.38),
                ],
                "run_takeoff_a": [
                    (0, 0), (.13, .55), (-.10, .40), (-.24, .26), (.27, .35), (.40, .16),
                    (-.12, -.31), (-.24, -.63), (.28, -.10), (.36, -.38),
                ],
                "run_flight_a": [
                    (0, 0), (.13, .55), (-.25, .39), (-.40, .20), (.35, .34), (.49, .14),
                    (-.20, -.23), (-.38, -.46), (.26, -.06), (.40, -.33),
                ],
                "run_contact_b": [
                    (0, 0), (.13, .55), (-.12, .36), (-.27, .20), (.30, .34), (.42, .16),
                    (-.17, -.32), (-.31, -.65), (.18, -.34), (.32, -.69),
                ],
                "run_compression_b": [
                    (0, 0), (.13, .55), (-.03, .38), (-.10, .26), (.19, .36), (.24, .20),
                    (-.10, -.22), (-.20, -.53), (.10, -.26), (.30, -.68),
                ],
                "run_passing_b": [
                    (0, 0), (.13, .55), (.08, .39), (.14, .25), (.08, .39), (.03, .25),
                    (.28, -.07), (.19, -.38), (.02, -.36), (.04, -.69),
                ],
                "brace": [
                    (0, 0), (-.10, .54), (-.38, .62), (-.62, .42), (.24, .58), (.50, .39),
                    (-.34, -.22), (-.49, -.67), (.30, -.25), (.54, -.66),
                ],
                "fall": [
                    (0, 0), (.42, .38), (.20, .72), (-.05, .96), (.70, .10), (.98, -.10),
                    (-.18, -.28), (-.52, -.42), (.32, -.37), (.67, -.54),
                ],
                "crouch": [
                    (0, 0), (.04, .38), (-.22, .28), (-.42, .08), (.28, .30), (.48, .10),
                    (-.34, -.14), (-.24, -.48), (.34, -.12), (.20, -.50),
                ],
            }
            coords = [np.array([x, y, 0.0]) for x, y in poses[pose]]
            hip, shoulder, elbow_l, hand_l, elbow_r, hand_r, knee_l, foot_l, knee_r, foot_r = coords
            head = Circle(radius=0.18, stroke_width=7, color=orange).move_to(shoulder + UP * 0.34 + RIGHT * 0.05)
            torso = Line(hip, shoulder, color=orange, stroke_width=8)
            limbs = [
                Line(shoulder, elbow_l, color=orange, stroke_width=7),
                Line(elbow_l, hand_l, color=orange, stroke_width=7),
                Line(shoulder, elbow_r, color=orange, stroke_width=7),
                Line(elbow_r, hand_r, color=orange, stroke_width=7),
                Line(hip, knee_l, color=orange, stroke_width=8),
                Line(knee_l, foot_l, color=orange, stroke_width=8),
                Line(hip, knee_r, color=orange, stroke_width=8),
                Line(knee_r, foot_r, color=orange, stroke_width=8),
            ]
            joints = VGroup(*[
                Dot(point, radius=0.045, fill_color=orange)
                for point in [hip, shoulder, elbow_l, elbow_r, knee_l, knee_r]
            ])
            figure = VGroup(head, torso, *limbs, joints)
            if carrying_phi:
                # The front hand carries the symbol; after mirroring, it sits
                # naturally in the runner's left-facing forward arm.
                phi = Text("φ", font_size=46, color=gold).move_to(hand_l + RIGHT * 0.12 + UP * 0.01)
                figure.add(phi)
            return figure.scale(scale).move_to(center)

        def fleeing_figure(center, pose="stand", scale=1.0, carrying_phi=True):
            """Face left, away from the giant shape chasing from the right."""
            bounce = {
                "run_contact_a": 0.00,
                "run_compression_a": -0.12,
                "run_passing_a": 0.02,
                "run_takeoff_a": 0.08,
                "run_flight_a": 0.15,
                "run_contact_b": 0.00,
                "run_compression_b": -0.12,
                "run_passing_b": 0.02,
            }.get(pose, 0.0)
            # Preserve the established left-facing screen direction.  The
            # acceleration refinement is handled by the individual run poses,
            # never by reversing the whole character.
            figure = stick_figure(ORIGIN, pose, scale, carrying_phi=carrying_phi).flip(UP).rotate(30 * DEG)
            return figure.move_to(center + UP * bounce)

        def wireframe(radius=0.85):
            angles = np.linspace(0, TAU, 12, endpoint=False)
            vertices = [radius * np.array([np.cos(a), np.sin(a), 0]) for a in angles]
            outer = Polygon(*vertices, color=white, stroke_width=2)
            chords = VGroup(*[
                Line(vertices[i], vertices[(i + offset) % len(vertices)], color=white, stroke_width=1.0)
                for i in range(len(vertices))
                for offset in (3, 5)
            ])
            dots = Group(*[GlowDot(v, color=white, radius=0.055, glow_factor=0.55) for v in vertices])
            return Group(outer, chords, dots)

        def impact(center, count=18, color=white):
            rays = []
            for index in range(count):
                angle = TAU * index / count + 0.12 * np.sin(index)
                start = center + 0.05 * np.array([np.cos(angle), np.sin(angle), 0])
                end = center + (0.20 + 0.20 * (index % 3) / 2) * np.array([np.cos(angle), np.sin(angle), 0])
                rays.append(Line(start, end, color=color, stroke_width=2))
            return VGroup(*rays)

        def road_damage(center):
            """A torn gap and loose asphalt fragments left by the rolling shape."""
            x = center[0]
            clear_gap = Line(
                np.array([x - 0.48, road_y, 0]),
                np.array([x + 0.48, road_y, 0]),
                color="#05070D",
                stroke_width=25,
            )
            cracks = VGroup(
                Line(np.array([x - .42, road_y + .08, 0]), np.array([x - .19, road_y - .16, 0]), color=GREY_B, stroke_width=2),
                Line(np.array([x + .34, road_y + .08, 0]), np.array([x + .13, road_y - .18, 0]), color=GREY_B, stroke_width=2),
                Line(np.array([x - .10, road_y - .02, 0]), np.array([x + .07, road_y - .24, 0]), color=GREY_C, stroke_width=2),
                Polygon(
                    np.array([x - .31, road_y - .03, 0]),
                    np.array([x - .15, road_y - .12, 0]),
                    np.array([x - .07, road_y - .32, 0]),
                    np.array([x - .28, road_y - .25, 0]),
                    color=GREY_D,
                    fill_opacity=0.9,
                    stroke_width=1,
                ),
                Polygon(
                    np.array([x + .18, road_y - .04, 0]),
                    np.array([x + .40, road_y - .14, 0]),
                    np.array([x + .30, road_y - .31, 0]),
                    np.array([x + .09, road_y - .22, 0]),
                    color=GREY_D,
                    fill_opacity=0.9,
                    stroke_width=1,
                ),
            )
            return VGroup(clear_gap, cracks)

        def golden_environment():
            squares = VGroup()
            size = 3.4
            center = ORIGIN
            phi = (1 + np.sqrt(5)) / 2
            for index in range(8):
                square = Square(side_length=size, color=white, stroke_width=1.8)
                square.move_to(center)
                squares.add(square)
                direction = [LEFT, DOWN, RIGHT, UP][index % 4]
                center += direction * size * (1 - 1 / phi) / 2
                size /= phi
            spiral = ParametricCurve(
                lambda t: 0.12 * (phi ** (2 * t / PI)) * np.array([np.cos(t), np.sin(t), 0]),
                t_range=(0, 3.8 * PI, 0.02),
                color=gold,
                stroke_width=3,
            )
            return VGroup(squares, spiral)

        # 0–4 s: a straight road and a giant rolling geometric rock.
        road_y = -2.65
        road_half = self.frame.get_width() / 2
        runner_y = DOWN * 1.90
        start_position = RIGHT * (road_half - 0.42) + runner_y
        road = VGroup(
            Line(LEFT * road_half + road_y * UP, RIGHT * road_half + road_y * UP, color=GREY_D, stroke_width=22),
            Line(LEFT * road_half + road_y * UP, RIGHT * road_half + road_y * UP, color=white, stroke_width=2),
            DashedLine(
                LEFT * (road_half - 0.15) + (road_y + 0.12) * UP,
                RIGHT * (road_half - 0.15) + (road_y + 0.12) * UP,
                dash_length=0.14,
                color=GREY_B,
                stroke_width=1.5,
            ),
        )
        hero = fleeing_figure(start_position, "stand", 0.72)
        # Begin just beyond the right edge so the rock rolls in behind him.
        enemy = wireframe(0.95).move_to(RIGHT * (road_half + 1.75) + DOWN * 1.58)
        title = Text(
            "ANIMATION\nVS. GEOMETRY",
            font_size=34,
            color=white,
            line_spacing_height=0.82,
        ).to_edge(UP, buff=0.35)
        title.fix_in_frame()

        # The character and road are visible from the very first frame.
        self.add(road, hero)
        self.wait(0.01)
        self.play(
            FadeIn(enemy, scale=1.35),
            self.frame.animate.scale(0.88).shift(RIGHT * 0.10),
            run_time=0.45,
            rate_func=rush_from,
        )
        self.play(Write(title), run_time=0.75)
        self.play(
            Transform(hero, fleeing_figure(start_position, "lean", 0.72)),
            enemy.animate.rotate(42 * DEG).scale(1.12),
            run_time=0.65,
            rate_func=there_and_back,
        )
        self.play(FadeOut(title), run_time=0.35)

        # 4–10 s: pose-to-pose run and wireframe pursuit.
        # The runner advances at the start and end; the middle third becomes a
        # treadmill-style run in place for a readable rhythmic beat.
        run_positions = [
            RIGHT * (
                road_half - 0.72
                - 0.14 * min(index, 13)
                - 0.14 * max(index - 27, 0)
                + (0.012 * np.sin(index * PI / 2) if 14 <= index <= 27 else 0)
            ) + runner_y
            for index in range(42)
        ]
        gait_cycle = (
            "run_contact_a", "run_compression_a", "run_passing_a", "run_takeoff_a",
            "run_flight_a", "run_contact_b", "run_compression_b", "run_passing_b",
        )
        for index, position in enumerate(run_positions):
            # The runner moves left twice as quickly as the giant shape, so
            # the distance between them clearly increases during the chase.
            # The giant rolls slightly more slowly, so the escape gap expands
            # by the same small amount on every step.
            enemy_x = road_half + 1.75 - 0.12 * (index + 1)
            enemy_target = RIGHT * enemy_x + DOWN * 1.48
            damage = road_damage(RIGHT * enemy_x)
            self.play(
                Transform(hero, fleeing_figure(position, gait_cycle[index % len(gait_cycle)], 0.72)),
                enemy.animate.move_to(enemy_target).rotate(-35 * DEG).scale(1.02),
                FadeIn(damage, scale=0.75),
                run_time=0.07,
                rate_func=linear,
            )

        # Phi slips out ahead of the runner.  Its scrape on the road leaves a
        # straight, evenly spaced line of small gold projectile fragments.
        escape_end = run_positions[-1]
        slip_x = escape_end[0] - 0.42
        loose_phi = Text("φ", font_size=52, color=gold).move_to(RIGHT * slip_x + DOWN * 2.12)
        self.play(
            Transform(hero, fleeing_figure(escape_end + LEFT * 0.08, "run_contact_a", 0.72, carrying_phi=False)),
            FadeIn(loose_phi, scale=0.35),
            run_time=0.16,
        )

        residue_positions = []
        for index in range(8):
            residue_x = slip_x - 0.16 * index
            residue_point = RIGHT * residue_x + UP * (road_y + 0.18)
            residue = Arrow(
                residue_point + LEFT * 0.075,
                residue_point + RIGHT * 0.075,
                buff=0,
                color=gold,
                stroke_width=3,
            )
            residue_positions.append((residue_point, residue))
            phi_position = RIGHT * (slip_x - 0.16 * (index + 1)) + DOWN * 2.12
            runner_position = RIGHT * (escape_end[0] - 0.08 - 0.11 * (index + 1)) + runner_y
            self.play(
                loose_phi.animate.move_to(phi_position),
                Transform(hero, fleeing_figure(runner_position, gait_cycle[index % len(gait_cycle)], 0.72, carrying_phi=False)),
                FadeIn(residue, scale=0.3),
                run_time=0.10,
                rate_func=linear,
            )

        # Phi keeps sliding until it disappears beyond the left edge.
        self.play(
            loose_phi.animate.move_to(LEFT * (road_half + 1.0) + DOWN * 2.12),
            run_time=0.42,
            rate_func=linear,
        )

        # Still running, he gathers the arrow fragments one by one from the road.
        for index, (residue_point, residue) in enumerate(residue_positions):
            pickup_position = RIGHT * residue_point[0] + runner_y
            self.play(
                Transform(hero, fleeing_figure(pickup_position, gait_cycle[(index + 2) % len(gait_cycle)], 0.72, carrying_phi=False)),
                FadeOut(residue, scale=0.2),
                run_time=0.10,
                rate_func=linear,
            )
        self.play(FadeOut(loose_phi, scale=0.4), run_time=0.12)

        # The collected fragments become arrow shots while he keeps moving.
        target = enemy.get_center() + LEFT * 0.35
        fire_origin_x = residue_positions[-1][0][0]
        for burst in range(8):
            firing_position = RIGHT * (fire_origin_x - 0.12 * burst) + runner_y
            shot_origin = hero.get_center() + RIGHT * 0.28 + UP * 0.12
            shot = Arrow(
                shot_origin + LEFT * 0.13,
                shot_origin + RIGHT * 0.13,
                buff=0,
                color=gold,
                stroke_width=4,
            )
            hit_flash = Circle(radius=0.13, color=gold, stroke_width=3).move_to(target)
            self.add(shot)
            self.play(
                shot.animate.move_to(target),
                Transform(hero, fleeing_figure(firing_position, gait_cycle[(burst + 4) % len(gait_cycle)], 0.72, carrying_phi=False)),
                enemy.animate.scale(1.01),
                run_time=0.16,
                rate_func=linear,
            )
            self.play(FadeOut(shot), FadeIn(hit_flash, scale=0.25), FadeOut(hit_flash, scale=1.6), run_time=0.07)
        escape_end = RIGHT * (fire_origin_x - 0.84) + runner_y
        symbols = VGroup(*[
            Text(symbol, font_size=22, color=white).move_to(point)
            for symbol, point in [("x", LEFT * 1.7 + DOWN * 2.25), ("+", LEFT * 1.1 + DOWN * 2.25), ("1", LEFT * 0.5 + DOWN * 2.25)]
        ])
        self.play(FadeIn(symbols), enemy.animate.scale(1.45), run_time=1.1)

        # 10–18 s: the giant rock closes in while the road stays level.
        self.play(FadeOut(symbols), enemy.animate.scale(1.25).rotate(-90 * DEG), run_time=1.0)
        self.play(
            Transform(hero, fleeing_figure(escape_end + LEFT * 0.08, "brace", 0.72, carrying_phi=False)),
            enemy.animate.move_to(escape_end + RIGHT * 1.85 + UP * 0.52).scale(1.18),
            run_time=1.0,
        )
        impact_point = escape_end + RIGHT * 0.34
        flash = impact(impact_point)
        flash_disc = Circle(
            radius=0.46,
            fill_color=white,
            fill_opacity=0.9,
            stroke_width=0,
        ).move_to(impact_point)
        self.play(
            FadeIn(flash, scale=0.2),
            FadeIn(flash_disc, scale=0.2),
            run_time=0.10,
        )
        self.wait(0.06)
        self.play(
            FadeOut(flash_disc),
            Transform(hero, fleeing_figure(escape_end + LEFT * 0.52 + UP * 0.22, "fall", 0.72, carrying_phi=False)),
            self.frame.animate.scale(0.92).shift(UP * 0.18 + RIGHT * 0.05),
            run_time=0.42,
            rate_func=rush_from,
        )
        # The opponent collapses into a square before the recursive world appears.
        seed_square = Square(side_length=1.10, color=white, stroke_width=2).move_to(enemy.get_center())
        self.play(
            FadeOut(flash),
            FadeOut(enemy),
            FadeIn(seed_square, scale=0.55),
            FadeOut(road),
            FadeOut(hero),
            run_time=0.65,
        )

        # 18–29 s: golden-ratio environment closes around the figure.
        gold_world = golden_environment().scale(0.92).shift(DOWN * 0.15)
        phi_symbol = Text("φ", font_size=92, color=gold).move_to(DOWN * 0.30)
        tiny_hero = stick_figure(UP * 1.12 + RIGHT * 0.22, "fall", 0.28)
        self.play(FadeIn(gold_world), FadeOut(seed_square), run_time=0.9)
        self.wait(0.8)
        self.play(FadeIn(tiny_hero), run_time=0.45)
        self.play(
            gold_world.animate.rotate(-12 * DEG).scale(1.06),
            tiny_hero.animate.move_to(UP * 0.22 + RIGHT * 0.05),
            self.frame.animate.scale(0.78).shift(DOWN * 0.18),
            run_time=4.2,
            rate_func=smooth,
        )
        self.play(
            gold_world.animate.rotate(-20 * DEG).scale(1.16).set_opacity(0.35),
            Transform(tiny_hero, stick_figure(DOWN * 0.18, "crouch", 0.23)),
            FadeIn(phi_symbol, scale=0.7),
            run_time=1.8,
        )
        final_caption = Text("Geometry closes the loop.", font_size=27, color=white).to_edge(DOWN, buff=0.55)
        final_caption.fix_in_frame()
        self.play(FadeIn(final_caption), phi_symbol.animate.scale(1.12), run_time=0.7)
        self.wait(1.4)
        self.play(FadeOut(VGroup(gold_world, tiny_hero, phi_symbol, final_caption)), run_time=1.0)
