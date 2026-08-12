import numpy as np

from manimlib import *


class HelloWorld(InteractiveScene):
    default_camera_config = {"background_color": "#05070D"}

    def construct(self):
        # A balanced three-quarter view keeps all three spatial axes legible
        # while giving the Lorenz curve clear depth.
        self.frame.reorient(-42, 68, 0)

        self.title = Text("Lorenz Attractor", font_size=56).to_edge(UP)
        self.title.fix_in_frame()
        self.hook = Text(
            "Can a difference of 0.0001\nchange the future?",
            font_size=52,
            line_spacing_height=0.85,
        )
        self.hook.fix_in_frame()

        # The governing Lorenz system remains readable in the foreground while
        # its solution is drawn in 3D behind it.
        self.equation_heading = Text("Lorenz system", font_size=30, color=YELLOW)
        self.equations = VGroup(
            Text("dx/dt = σ(y − x)", font_size=31, color=WHITE),
            Text("dy/dt = x(ρ − z) − y", font_size=31, color=WHITE),
            Text("dz/dt = xy − βz", font_size=31, color=WHITE),
            Text("σ = 10, ρ = 28, β = 8/3", font_size=23, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        self.equation_heading.next_to(self.equations, UP, aligned_edge=LEFT, buff=0.18)
        self.equations.to_corner(UL, buff=0.35).shift(DOWN * 0.62)
        self.equation_heading.next_to(self.equations, UP, aligned_edge=LEFT, buff=0.18)
        self.equation_heading.fix_in_frame()
        self.equations.fix_in_frame()
        self.initial_conditions_label = Text(
            "Initial gap: 0.0001",
            font_size=22,
            color=YELLOW,
        )
        self.initial_conditions_label.next_to(self.equations, DOWN, buff=0.20)
        self.initial_conditions_label.fix_in_frame()
        self.trajectory_key = VGroup(
            Text("Cyan: trajectory A", font_size=18, color=BLUE_C),
            Text("Yellow: trajectory B", font_size=18, color=YELLOW),
        ).arrange(RIGHT, buff=0.22)
        self.trajectory_key.next_to(self.initial_conditions_label, DOWN, aligned_edge=LEFT, buff=0.10)
        self.trajectory_key.fix_in_frame()
        self.equation_panel = SurroundingRectangle(
            VGroup(
                self.equation_heading,
                self.equations,
                self.initial_conditions_label,
                self.trajectory_key,
            ),
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0.72,
            buff=0.22,
        )
        self.equation_panel.fix_in_frame()

        # Pi enters at more than ten times its final size, then makes room for
        # the mathematical scene at the lower-right of the frame.
        self.pi_body = Text("π", font_size=220, color=YELLOW)
        left_eye = Dot(radius=0.06, fill_color=WHITE)
        right_eye = Dot(radius=0.06, fill_color=WHITE)
        left_eye.move_to(self.pi_body.get_center() + LEFT * 0.34 + UP * 0.25)
        right_eye.move_to(self.pi_body.get_center() + RIGHT * 0.34 + UP * 0.25)
        self.pi_mouth = Arc(radius=0.20, start_angle=0, angle=PI, color=WHITE)
        self.pi_mouth.move_to(self.pi_body.get_center() + DOWN * 0.30)
        # This is π's single right arm. It is part of the character, but is
        # kept as its own mobject so only the arm—not the π glyph—can stretch.
        shoulder = self.pi_body.get_right() + LEFT * 0.12 + UP * 0.05
        elbow = shoulder + RIGHT * 0.40 + UP * 0.12
        hand = elbow + UP * 0.26
        self.pi_arm = VGroup(
            Line(shoulder, elbow, color=YELLOW, stroke_width=9),
            Line(elbow, hand, color=YELLOW, stroke_width=9),
            Dot(hand, radius=0.09, fill_color=YELLOW),
        )
        self.pi_symbol = VGroup(self.pi_body, self.pi_arm)
        self.pi_character = VGroup(
            self.pi_symbol, left_eye, right_eye, self.pi_mouth,
        )
        # This is intentionally huge for the introduction; it finishes at the
        # previous compact corner size after the entrance animation.
        self.pi_character.scale(10)
        self.pi_character.fix_in_frame()

        # Axes are scaled to the standard Lorenz-system solution range.
        self.axes = ThreeDAxes(
            x_range=(-24, 24, 8),
            y_range=(-32, 32, 8),
            z_range=(0, 50, 10),
            width=12,
            height=7,
            depth=6,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
            },
            x_axis_config={"line_to_number_direction": DOWN},
            y_axis_config={"line_to_number_direction": LEFT},
            z_axis_config={"line_to_number_direction": RIGHT},
        )
        # Orbit around the middle of the attractor rather than the world origin,
        # keeping the full shape in view for the forthcoming 360° camera move.
        self.frame.move_to(self.axes.c2p(0, 0, 25))
        # Numerically solve the Lorenz equations using their classic values.
        # A small Runge-Kutta step keeps neighbouring curve segments so close
        # together that the drawn attractor reads as one continuous smooth line.
        sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
        x, y, z = 0.1, 0.0, 0.0
        nearby_x, nearby_y, nearby_z = 0.1001, 0.0, 0.0
        dt = 0.0025
        points = []
        nearby_points = []
        def derivatives(px, py, pz):
            return (
                sigma * (py - px),
                px * (rho - pz) - py,
                px * py - beta * pz,
            )

        def runge_kutta_step(px, py, pz):
            k1 = derivatives(px, py, pz)
            k2 = derivatives(
                px + dt * k1[0] / 2,
                py + dt * k1[1] / 2,
                pz + dt * k1[2] / 2,
            )
            k3 = derivatives(
                px + dt * k2[0] / 2,
                py + dt * k2[1] / 2,
                pz + dt * k2[2] / 2,
            )
            k4 = derivatives(
                px + dt * k3[0],
                py + dt * k3[1],
                pz + dt * k3[2],
            )
            return (
                px + dt * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6,
                py + dt * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6,
                pz + dt * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]) / 6,
            )

        for step in range(26000):
            x, y, z = runge_kutta_step(x, y, z)
            nearby_x, nearby_y, nearby_z = runge_kutta_step(
                nearby_x, nearby_y, nearby_z,
            )
            # Discard the initial transient, then retain every integration step.
            if step > 3000:
                points.append(self.axes.c2p(x, y, z))
                nearby_points.append(self.axes.c2p(nearby_x, nearby_y, nearby_z))

        # Each sketching light has a large halo and an opaque yellow core.
        # The core is deliberately a regular Dot so it remains clearly visible.
        def make_light(point, color):
            halo = GlowDot(
                point,
                color=color,
                radius=0.55,
                glow_factor=0.8,
                opacity=0.9,
            )
            core = Dot(point, radius=0.22, fill_color=color)
            return Group(halo, core)

        # Two almost identical starting points create two trajectories whose
        # eventual separation makes the butterfly effect visible.
        self.primary_curve = VMobject(stroke_width=4, color=BLUE_C)
        self.primary_curve.set_points_as_corners(points)
        self.primary_curve.apply_depth_test()
        self.nearby_curve = VMobject(stroke_width=3, color=YELLOW)
        self.nearby_curve.set_points_as_corners(nearby_points)
        self.nearby_curve.apply_depth_test()
        self.primary_tracer = make_light(self.primary_curve.get_start(), BLUE_C)
        self.nearby_tracer = make_light(self.nearby_curve.get_start(), YELLOW)
        self.tracers = Group(self.primary_tracer, self.nearby_tracer)
        self.tip_markers = Group(
            make_light(self.primary_curve.get_end(), BLUE_C),
            make_light(self.nearby_curve.get_end(), YELLOW),
        )

        self.play(Write(self.hook), run_time=0.7)
        self.play(FadeOut(self.hook), run_time=0.4)
        self.play(Write(self.title), run_time=0.7)
        self.play(FadeIn(self.pi_character, scale=0.8), run_time=0.45)
        # A small wobble makes pi look puzzled about the Lorenz attractor.
        self.play(
            self.pi_character.animate.rotate(8 * DEG),
            run_time=0.15,
            rate_func=there_and_back,
        )
        self.play(
            self.pi_character.animate.scale(0.055).to_corner(DR, buff=0.4),
            run_time=0.5,
        )

        # Pi wonders what is being drawn. This caption is fixed in the frame,
        # so it always remains visibly in front of the 3D scene and above pi.
        self.pi_question = Text("Lorenz attractor?", font_size=30, color=WHITE)
        self.pi_question.next_to(self.pi_character, UP, buff=0.12)
        self.pi_question.fix_in_frame()
        self.play(FadeIn(self.pi_question), run_time=0.25)

        # Stretch only π's arm to the top of its head. The letter itself never
        # transforms during this action.
        def stretched_arm_pose(hand_offset):
            shoulder = self.pi_body.get_right() + LEFT * 0.07 + UP * 0.03
            hand = self.pi_body.get_top() + hand_offset
            elbow = shoulder + RIGHT * 0.34 + UP * 0.48
            return VGroup(
                Line(shoulder, elbow, color=YELLOW, stroke_width=5),
                Line(elbow, hand, color=YELLOW, stroke_width=5),
                Dot(hand, radius=0.05, fill_color=YELLOW),
            )

        hand_left = LEFT * 0.12 + DOWN * 0.04
        hand_right = RIGHT * 0.16 + DOWN * 0.03
        self.play(Transform(self.pi_arm, stretched_arm_pose(hand_left)), run_time=0.25)
        self.play(
            Transform(self.pi_arm, stretched_arm_pose(hand_right)),
            run_time=0.10,
        )
        self.play(
            Transform(self.pi_arm, stretched_arm_pose(hand_left)),
            run_time=0.10,
        )
        self.play(
            Transform(self.pi_arm, stretched_arm_pose(hand_right)),
            run_time=0.10,
        )
        self.play(
            Transform(self.pi_arm, stretched_arm_pose(hand_left)),
            run_time=0.10,
        )

        # Draw the 3D axes only after pi has moved aside and scratched its head.
        self.play(
            FadeIn(self.axes),
            FadeIn(self.equation_panel),
            Write(self.equation_heading),
            Write(self.equations),
            FadeIn(self.initial_conditions_label),
            FadeIn(self.trajectory_key),
            FadeOut(self.title),
            run_time=0.8,
        )

        self.add(self.tracers)
        sketch_animations = [
            ShowCreation(self.primary_curve, rate_func=linear),
            MoveAlongPath(self.primary_tracer, self.primary_curve, rate_func=linear),
            ShowCreation(self.nearby_curve, rate_func=linear),
            MoveAlongPath(self.nearby_tracer, self.nearby_curve, rate_func=linear),
        ]
        # Complete one smooth, continuous orbit while the trajectories draw.
        orbit_progress = ValueTracker(0)
        initial_theta = self.frame.get_theta()

        self.frame.add_updater(
            lambda frame: frame.set_theta(
                initial_theta + 360 * DEG * orbit_progress.get_value()
            )
        )
        self.play(
            *sketch_animations,
            orbit_progress.animate.set_value(1),
            run_time=50,
            rate_func=linear,
        )
        self.frame.clear_updaters()
        self.play(FadeOut(self.tracers), FadeIn(self.tip_markers), run_time=0.5)

        # Once the curve is complete, pi changes from a frown to a smile.
        happy_mouth = Arc(radius=0.20, start_angle=PI, angle=PI, color=WHITE)
        happy_mouth.move_to(self.pi_mouth.get_center())
        conclusion = Text(
            "Small changes.\nCompletely different futures.",
            font_size=30,
            line_spacing_height=0.85,
        ).to_corner(DL, buff=0.35)
        conclusion.fix_in_frame()
        self.play(
            Transform(self.pi_mouth, happy_mouth),
            self.pi_character.animate.rotate(8 * DEG),
            FadeOut(self.pi_question),
            FadeIn(conclusion),
            run_time=0.6,
            rate_func=there_and_back,
        )

        # After the mathematical explanation, remove every interface element
        # and leave only one bare Lorenz curve in space.
        self.play(
            FadeOut(self.axes),
            FadeOut(self.equation_panel),
            FadeOut(self.equation_heading),
            FadeOut(self.equations),
            FadeOut(self.initial_conditions_label),
            FadeOut(self.trajectory_key),
            FadeOut(self.pi_character),
            FadeOut(conclusion),
            FadeOut(self.nearby_curve),
            FadeOut(self.tip_markers),
            run_time=0.8,
        )

        # The completed visualization disappears completely before the next
        # small story begins on a clean stage.
        self.play(
            FadeOut(self.primary_curve),
            self.frame.animate.reorient(0, 0, 0).move_to(ORIGIN),
            run_time=0.8,
        )

        # New closing scene: the orange character rides a large pendulum bob.
        pivot = UP * 2.85
        bob_center = DOWN * 1.65
        string = Line(pivot, bob_center, color=GREY_B, stroke_width=5)
        bob = Circle(radius=.64, color=GREY_B, stroke_width=5)
        bob.set_fill(color=GREY_D, opacity=.85).move_to(bob_center)
        bob_glow = bob.copy().set_stroke(color=WHITE, width=15, opacity=.10)
        pivot_dot = Dot(pivot, radius=.09, fill_color=WHITE)

        # A compact seated pose: both arms reach down to grip the bob.
        # Clear seated position directly on top of the bob.
        sit_base = bob_center + UP * .62
        head = Circle(radius=.14, color="#FF6A00", stroke_width=5).move_to(sit_base + UP * .43)
        torso = Line(sit_base + UP * .27, sit_base, color="#FF6A00", stroke_width=6)
        arm_l = Line(sit_base + UP * .24, sit_base + LEFT * .31 + DOWN * .05, color="#FF6A00", stroke_width=5)
        arm_r = Line(sit_base + UP * .24, sit_base + RIGHT * .31 + DOWN * .05, color="#FF6A00", stroke_width=5)
        thigh_l = Line(sit_base, sit_base + LEFT * .24 + DOWN * .23, color="#FF6A00", stroke_width=6)
        shin_l = Line(sit_base + LEFT * .24 + DOWN * .23, sit_base + LEFT * .05 + DOWN * .46, color="#FF6A00", stroke_width=6)
        thigh_r = Line(sit_base, sit_base + RIGHT * .25 + DOWN * .22, color="#FF6A00", stroke_width=6)
        shin_r = Line(sit_base + RIGHT * .25 + DOWN * .22, sit_base + RIGHT * .08 + DOWN * .46, color="#FF6A00", stroke_width=6)
        rider = VGroup(head, torso, arm_l, arm_r, thigh_l, shin_l, thigh_r, shin_r)
        rider_glow = rider.copy().set_stroke(color="#FF8A00", width=14, opacity=.13)

        pendulum = VGroup(string, bob_glow, bob, rider_glow, rider)
        self.play(FadeIn(pivot_dot), ShowCreation(string), FadeIn(bob_glow), FadeIn(bob), FadeIn(rider_glow), FadeIn(rider), run_time=.8)
        self.play(pendulum.animate.rotate(24 * DEG, about_point=pivot), run_time=1.0, rate_func=smooth)
        self.play(pendulum.animate.rotate(-48 * DEG, about_point=pivot), run_time=1.55, rate_func=smooth)
        self.play(pendulum.animate.rotate(42 * DEG, about_point=pivot), run_time=1.35, rate_func=smooth)
        self.play(pendulum.animate.rotate(-30 * DEG, about_point=pivot), run_time=1.15, rate_func=smooth)
        self.play(pendulum.animate.rotate(12 * DEG, about_point=pivot), run_time=.8, rate_func=smooth)
        self.wait(.7)
        self.play(FadeOut(VGroup(pivot_dot, pendulum)), run_time=.7)

        return

        def rope_man(center, pose="hang", scale=0.50):
            orange = "#FF6A00"
            pose_points = {
                "hang": [
                    (0, 0), (0, .55), (-.18, .82), (-.10, 1.16), (.18, .82), (.10, 1.16),
                    (-.16, -.36), (-.20, -.75), (.16, -.36), (.20, -.75),
                ],
                "land": [
                    (0, 0), (.03, .54), (-.16, .76), (-.08, 1.00), (.16, .76), (.08, 1.00),
                    (-.18, -.34), (-.24, -.73), (.18, -.34), (.24, -.73),
                ],
                # Hunched forward as he slips down the rope, rather than
                # staying perfectly upright like a rigid stick figure.
                "slip": [
                    (.05, 0), (-.14, .47), (-.35, .58), (-.44, .88), (.04, .66), (.00, 1.04),
                    (-.17, -.32), (-.34, -.62), (.20, -.25), (.30, -.55),
                ],
                "slip_low": [
                    (-.02, 0), (-.25, .40), (-.43, .48), (-.52, .72), (-.08, .67), (-.02, 1.02),
                    (-.24, -.27), (-.44, -.48), (.19, -.24), (.36, -.60),
                ],
                "pull": [
                    (.10, -.03), (-.23, .43), (-.34, .72), (-.27, 1.13), (-.12, .74), (-.06, 1.16),
                    (-.25, -.30), (-.50, -.66), (.27, -.23), (.46, -.63),
                ],
                "fall": [
                    (0, 0), (-.34, .20), (-.55, .26), (-.78, .10), (-.38, .43), (-.52, .64),
                    (-.19, -.25), (-.45, -.42), (.18, -.13), (.48, -.22),
                ],
                "pickup": [
                    (.02, 0), (-.23, .32), (-.43, .15), (-.58, -.03), (-.09, .18), (.05, .02),
                    (-.18, -.24), (-.35, -.48), (.20, -.19), (.42, -.34),
                ],
                "throw": [
                    (0, 0), (-.05, .53), (-.26, .80), (-.42, 1.12), (.15, .82), (.34, 1.10),
                    (-.18, -.31), (-.34, -.67), (.18, -.28), (.34, -.64),
                ],
                "swing": [
                    (0, 0), (-.05, .52), (-.25, .70), (-.42, .53), (.18, .66), (.52, .56),
                    (-.18, -.31), (-.34, -.67), (.18, -.28), (.34, -.64),
                ],
            }
            points = [np.array([x, y, 0.0]) for x, y in pose_points[pose]]
            hip, shoulder, elbow_l, hand_l, elbow_r, hand_r, knee_l, foot_l, knee_r, foot_r = points
            head = Circle(radius=.15, color=orange, stroke_width=5).move_to(shoulder + UP * .29)
            torso = Line(hip, shoulder, color=orange, stroke_width=6)
            limbs = VGroup(
                Line(shoulder, elbow_l, color=orange, stroke_width=5),
                Line(elbow_l, hand_l, color=orange, stroke_width=5),
                Line(shoulder, elbow_r, color=orange, stroke_width=5),
                Line(elbow_r, hand_r, color=orange, stroke_width=5),
                Line(hip, knee_l, color=orange, stroke_width=6),
                Line(knee_l, foot_l, color=orange, stroke_width=6),
                Line(hip, knee_r, color=orange, stroke_width=6),
                Line(knee_r, foot_r, color=orange, stroke_width=6),
            )
            body = VGroup(head, torso, limbs).scale(scale).move_to(center)
            glow = body.copy().set_stroke(color="#FF8A00", width=14, opacity=.12)
            return VGroup(glow, body)

        roof = Line(LEFT * 5.6 + UP * 3.15, RIGHT * 5.6 + UP * 3.15, color=WHITE, stroke_width=4)
        ground = Line(LEFT * 5.6 + DOWN * 2.75, RIGHT * 5.6 + DOWN * 2.75, color=WHITE, stroke_width=3)
        # Solid white ground continuing below the horizon line.
        solid_ground = Rectangle(
            width=12.0,
            height=1.55,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=1,
        ).move_to(DOWN * 3.52)
        # A gently swaying rope, with its spare length coiled on the floor.
        rope = VMobject(color=GREY_B, stroke_width=4)
        rope.set_points_smoothly([
            UP * 3.15,
            np.array([-.04, 1.90, 0]),
            np.array([.08, .45, 0]),
            np.array([-.07, -1.05, 0]),
            np.array([.03, -2.48, 0]),
        ])
        slack_rope = rope.copy()
        taut_rope = VMobject(color=GREY_B, stroke_width=4)
        taut_rope.set_points_smoothly([
            UP * 3.15,
            np.array([-.015, 1.85, 0]),
            np.array([.015, .40, 0]),
            np.array([-.025, -1.08, 0]),
            np.array([-.12, -2.37, 0]),
        ])
        sway_rope = VMobject(color=GREY_B, stroke_width=4)
        sway_rope.set_points_smoothly([
            UP * 3.15,
            np.array([.08, 1.90, 0]),
            np.array([-.10, .45, 0]),
            np.array([.10, -1.05, 0]),
            np.array([-.05, -2.48, 0]),
        ])
        # One continuous, irregular length of rope scattered on the floor.
        # It begins at the hanging rope's end, so both parts read as one rope.
        coil_points = [np.array([.03, -2.48, 0]), np.array([.03, -2.64, 0])]
        for index in range(9):
            angle_offset = .30 * index
            center_x = .14 + .10 * np.sin(1.7 * index)
            center_y = -2.67 + .025 * np.cos(1.3 * index)
            radius_x = 1.02 - .070 * index
            radius_y = .15 - .007 * index
            for angle in np.linspace(0, TAU, 15):
                wobble = 1 + .10 * np.sin(3 * angle + index)
                coil_points.append(np.array([
                    center_x + radius_x * wobble * np.cos(angle + angle_offset),
                    center_y + radius_y * wobble * np.sin(angle + angle_offset),
                    0,
                ]))
        floor_coils = VMobject(color=GREY_B, stroke_width=4)
        floor_coils.set_points_smoothly(coil_points)
        floor_coils.set_fill(opacity=0).set_stroke(color=GREY_B, width=4, opacity=1)
        knot = Dot(UP * 3.15, radius=.07, fill_color=WHITE)
        man = rope_man(UP * 1.75, "hang")
        self.play(
            FadeIn(solid_ground), ShowCreation(roof), ShowCreation(ground), ShowCreation(rope),
            ShowCreation(floor_coils), FadeIn(knot), FadeIn(man, shift=UP * .25),
            run_time=.7,
        )
        self.play(man.animate.rotate(5 * DEG), run_time=.25, rate_func=there_and_back)
        # Descend in separate gripping poses so he visibly slides down the
        # rope instead of simply translating as a fixed figure.
        self.play(
            Transform(man, rope_man(LEFT * .05 + DOWN * .20, "slip")),
            Transform(rope, sway_rope), run_time=.55, rate_func=smooth,
        )
        self.play(
            Transform(man, rope_man(RIGHT * .06 + DOWN * 1.05, "slip_low")),
            Transform(rope, slack_rope), run_time=.55, rate_func=linear,
        )
        self.play(
            Transform(man, rope_man(LEFT * .04 + DOWN * 1.95, "slip")),
            Transform(rope, sway_rope), run_time=.55, rate_func=linear,
        )
        self.play(
            Transform(man, rope_man(DOWN * 2.22, "land")),
            Transform(rope, slack_rope), run_time=.30, rate_func=rush_from,
        )

        # Five increasingly forceful tugs.  Each pull makes the rope taut,
        # then it visibly relaxes before the next attempt.
        for _ in range(4):
            self.play(
                Transform(man, rope_man(LEFT * .10 + DOWN * 2.18, "pull")),
                Transform(rope, taut_rope),
                run_time=.42,
                rate_func=rush_into,
            )
            self.play(
                Transform(man, rope_man(DOWN * 2.22, "land")),
                Transform(rope, slack_rope),
                run_time=.30,
                rate_func=rush_from,
            )

        impact_bits = VGroup(*[
            Dot(UP * 3.15 + 0.12 * np.array([
                np.cos(angle), np.sin(angle), 0,
            ]), radius=.035, fill_color=WHITE)
            for angle in np.linspace(0, TAU, 10, endpoint=False)
        ])
        fallen_rope = VMobject(color=GREY_B, stroke_width=4)
        fallen_rope.set_points_smoothly([
            np.array([-.12, -2.56, 0]), np.array([.22, -2.47, 0]),
            np.array([-.34, -2.58, 0]), np.array([.45, -2.64, 0]),
            np.array([-.08, -2.70, 0]),
        ])
        self.play(
            Transform(man, rope_man(LEFT * .10 + DOWN * 2.18, "pull")),
            Transform(rope, taut_rope),
            run_time=.46,
            rate_func=rush_into,
        )
        self.play(
            FadeOut(knot), FadeIn(impact_bits), Transform(rope, fallen_rope),
            Transform(man, rope_man(LEFT * .32 + DOWN * 2.32, "fall")),
            run_time=.30,
            rate_func=rush_from,
        )
        self.play(FadeOut(impact_bits), run_time=.25)

        # He collects the broken rope and swings its weighted end in a circle
        # from his hand before releasing it upward.
        self.play(
            Transform(man, rope_man(RIGHT * .12 + DOWN * 2.31, "pickup")),
            rope.animate.shift(RIGHT * .12),
            run_time=.45,
            rate_func=smooth,
        )
        # This point matches the raised right hand in the "swing" pose, so
        # the rope visibly turns from his grip instead of above his head.
        pivot = np.array([.26, -1.87, 0])

        def swing_rope(angle):
            end = pivot + .58 * np.array([np.cos(angle), np.sin(angle), 0])
            curve = VMobject(color=GREY_B, stroke_width=4)
            curve.set_points_smoothly([
                pivot,
                .55 * pivot + .45 * end + np.array([.06, -.03, 0]),
                end,
            ])
            return curve, end

        first_swing, stone_position = swing_rope(-PI / 2)
        stone = Dot(stone_position, radius=.105, fill_color=GREY_B)
        self.play(
            Transform(man, rope_man(DOWN * 2.08, "swing")),
            Transform(rope, first_swing), FadeOut(floor_coils), FadeIn(stone),
            run_time=.42,
            rate_func=smooth,
        )
        # Build speed through several circular swings, like a rope with a
        # stone tied to its end.
        for angle, duration in zip(
            [0, PI / 2, PI, 3 * PI / 2, 2 * PI, 5 * PI / 2],
            [.22, .19, .17, .15, .14, .13],
        ):
            swung_rope, stone_position = swing_rope(angle)
            self.play(
                Transform(rope, swung_rope), stone.animate.move_to(stone_position),
                run_time=duration, rate_func=linear,
            )

        # After release, the rope remains visible as it flies up from the
        # floor along a deliberately uneven path through the frame.
        def flying_rope(center, tilt):
            direction = np.array([np.cos(tilt), np.sin(tilt), 0])
            normal = np.array([-np.sin(tilt), np.cos(tilt), 0])
            start = center - .42 * direction
            end = center + .42 * direction
            airborne = VMobject(color=GREY_B, stroke_width=4)
            airborne.set_points_smoothly([
                start,
                center - .12 * direction + .11 * normal,
                center + .10 * direction - .09 * normal,
                end,
            ])
            return airborne, end

        flight_steps = [
            (np.array([.28, -1.15, 0]), .65),
            (np.array([.86, -.36, 0]), 1.65),
            (np.array([-.48, .42, 0]), .42),
            (np.array([.45, 1.22, 0]), 2.10),
            (np.array([.02, 1.78, 0]), .95),
        ]
        first_flight, stone_position = flying_rope(*flight_steps[0])
        self.play(
            Transform(man, rope_man(LEFT * .18 + DOWN * 1.98, "throw")),
            Transform(rope, first_flight), stone.animate.move_to(stone_position),
            run_time=.30, rate_func=rush_from,
        )
        for center, tilt in flight_steps[1:]:
            airborne_rope, stone_position = flying_rope(center, tilt)
            self.play(
                Transform(rope, airborne_rope), stone.animate.move_to(stone_position),
                run_time=.24, rate_func=linear,
            )

        spiral_rope = VMobject(color=GREY_B, stroke_width=5)
        spiral_points = []
        for angle in np.linspace(0, 4 * PI, 50):
            radius = .10 + .055 * angle
            spiral_points.append(np.array([
                radius * np.cos(angle),
                .15 + radius * np.sin(angle),
                0,
            ]))
        spiral_rope.set_points_smoothly(spiral_points)
        self.play(
            Transform(rope, spiral_rope), FadeOut(stone),
            run_time=.55, rate_func=smooth,
        )
        self.play(rope.animate.rotate(2 * PI).scale(.90), run_time=.60, rate_func=linear)

        thomas_heading = Text(
            "LET'S MOVE TO\nTHOMAS ATTRACTOR NOW",
            font_size=46,
            line_spacing_height=.82,
            color=WHITE,
        ).move_to(UP * .35)
        heading_glow = thomas_heading.copy().set_stroke(color="#FF8A00", width=14, opacity=.13)
        self.play(
            FadeOut(VGroup(roof, ground, solid_ground, man)),
            Transform(rope, thomas_heading), FadeIn(heading_glow),
            run_time=.75,
            rate_func=smooth,
        )
        self.wait(1.2)
        self.play(FadeOut(VGroup(rope, heading_glow)), run_time=.6)

        # Uncomment for interactive editing; keep disabled when exporting video.
        # self.embed()


class PolarRosette(InteractiveScene):
    """A closed spirograph-style rosette from radial sinusoidal modulation."""

    default_camera_config = {"background_color": "#05070D"}

    def construct(self):
        title = Text("Closed Polar Rosette", font_size=52, color=WHITE).to_edge(UP)
        equation = Text("r = 10 + 4 sin(24θ / 25)", font_size=30, color=YELLOW)
        equation.next_to(title, DOWN, buff=0.20)
        details = Text(
            "6 ≤ r ≤ 14   •   closes after 25 turns",
            font_size=22,
            color=GREY_B,
        ).next_to(equation, DOWN, buff=0.16)

        # θ must travel through 25 full revolutions before the 24/25 frequency
        # ratio returns to its starting phase and closes the rosette.
        theta_values = np.linspace(0, 50 * PI, 30000)
        display_scale = 0.22
        points = [
            display_scale * (10 + 4 * np.sin(24 * theta / 25)) * np.array([
                np.cos(theta), np.sin(theta), 0,
            ])
            for theta in theta_values
        ]
        rosette = VMobject(stroke_width=3)
        rosette.set_points_as_corners(points)
        rosette.set_color_by_gradient(BLUE_C, TEAL, YELLOW, TEAL, BLUE_C)
        rosette.shift(DOWN * 0.45)

        center_dot = GlowDot(DOWN * 0.45, color=YELLOW, radius=0.15, glow_factor=1.3)

        self.play(Write(title), FadeIn(equation), FadeIn(details), run_time=1.2)
        self.play(ShowCreation(rosette, rate_func=linear), run_time=18)
        self.play(FadeIn(center_dot, scale=0.5), run_time=0.5)


class ThomasAttractor(InteractiveScene):
    """The cyclic-sine Thomas attractor at its standard chaotic parameter."""

    default_camera_config = {"background_color": WHITE}

    def construct(self):
        self.frame.reorient(-42, 68, 0)

        title = Text("Thomas' Attractor", font_size=54, color=BLACK).to_edge(UP)
        title.fix_in_frame()
        system = VGroup(
            Text("dx/dt = sin(y) − bx", font_size=30, color=BLACK),
            Text("dy/dt = sin(z) − by", font_size=30, color=BLACK),
            Text("dz/dt = sin(x) − bz", font_size=30, color=BLACK),
            Text("b = 0.208186", font_size=23, color="#7A1F5C"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        system.to_corner(UL, buff=0.35).shift(DOWN * 0.62)
        system.fix_in_frame()

        axes = ThreeDAxes(
            x_range=(-6, 6, 2),
            y_range=(-6, 6, 2),
            z_range=(-6, 6, 2),
            width=9,
            height=7,
            depth=7,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GREY_B,
                "stroke_width": 1.5,
            },
        )
        self.frame.move_to(axes.c2p(0, 0, 0))

        b = 0.208186
        state = np.array([0.1, 0.0, 0.0])
        dt = 0.005

        def derivatives(vector):
            x, y, z = vector
            return np.array([
                np.sin(y) - b * x,
                np.sin(z) - b * y,
                np.sin(x) - b * z,
            ])

        points = []
        for step in range(70000):
            k1 = derivatives(state)
            k2 = derivatives(state + dt * k1 / 2)
            k3 = derivatives(state + dt * k2 / 2)
            k4 = derivatives(state + dt * k3)
            state += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            if step > 6000 and step % 3 == 0:
                points.append(axes.c2p(*state))

        curve = VMobject(stroke_width=1.8)
        curve.set_points_as_corners(points)
        # A time-ordered plasma gradient: dark purple to burgundy, orange,
        # and pale yellow, with no cyan component.
        curve.set_color_by_gradient(
            "#2B0A3D", "#7A1F5C", "#C24642", "#F08A3C", "#FFF1A6",
        )
        curve.apply_depth_test()
        tracer = Group(
            GlowDot(
                curve.get_start(),
                color="#FFF1A6",
                radius=0.18,
                glow_factor=0.55,
                opacity=0.65,
            ),
            Dot(curve.get_start(), radius=0.06, fill_color="#FFF1A6"),
        )

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(axes), FadeOut(title), run_time=1.0)
        self.add(tracer)

        orbit_progress = ValueTracker(0)
        initial_theta = self.frame.get_theta()
        self.frame.add_updater(
            lambda frame: frame.set_theta(
                initial_theta + 360 * DEG * orbit_progress.get_value()
            )
        )
        self.play(
            ShowCreation(curve, rate_func=linear),
            MoveAlongPath(tracer, curve, rate_func=linear),
            orbit_progress.animate.set_value(1),
            run_time=38,
            rate_func=linear,
        )
        self.frame.clear_updaters()
        self.play(FadeOut(tracer), run_time=0.4)


class ChenAttractor(InteractiveScene):
    """A plasma-styled visualization of the classic chaotic Chen system."""

    default_camera_config = {"background_color": WHITE}

    def construct(self):
        self.frame.reorient(-42, 68, 0)

        title = Text("Chen Attractor", font_size=56, color=BLACK).to_edge(UP)
        subtitle = Text(
            "a = 35   •   b = 3   •   c = 28",
            font_size=24,
            color="#7A1F5C",
        ).next_to(title, DOWN, buff=0.18)
        title.fix_in_frame()
        subtitle.fix_in_frame()

        axes = ThreeDAxes(
            x_range=(-30, 30, 10),
            y_range=(-35, 35, 10),
            z_range=(0, 55, 10),
            width=10,
            height=7,
            depth=7,
            axis_config={
                "include_tip": True,
                "include_numbers": False,
                "color": GREY_B,
                "stroke_width": 1.5,
            },
        )
        self.frame.move_to(axes.c2p(0, 0, 28))

        a, b, c = 35.0, 3.0, 28.0
        state = np.array([0.1, 0.0, -0.1])
        dt = 0.0025

        def derivatives(vector):
            x, y, z = vector
            return np.array([
                a * (y - x),
                (c - a) * x - x * z + c * y,
                x * y - b * z,
            ])

        points = []
        for step in range(80000):
            k1 = derivatives(state)
            k2 = derivatives(state + dt * k1 / 2)
            k3 = derivatives(state + dt * k2 / 2)
            k4 = derivatives(state + dt * k3)
            state += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            if step > 5000 and step % 3 == 0:
                points.append(axes.c2p(*state))

        curve = VMobject(stroke_width=1.8)
        curve.set_points_as_corners(points)
        curve.set_color_by_gradient(
            "#2B0A3D", "#7A1F5C", "#C24642", "#F08A3C", "#FFF1A6",
        )
        curve.apply_depth_test()
        tracer = Group(
            GlowDot(
                curve.get_start(),
                color="#FFF1A6",
                radius=0.18,
                glow_factor=0.55,
                opacity=0.65,
            ),
            Dot(curve.get_start(), radius=0.06, fill_color="#FFF1A6"),
        )

        self.play(Write(title), FadeIn(subtitle), run_time=1.0)
        self.play(FadeIn(axes), FadeOut(title), FadeOut(subtitle), run_time=1.0)
        self.add(tracer)

        orbit_progress = ValueTracker(0)
        initial_theta = self.frame.get_theta()
        self.frame.add_updater(
            lambda frame: frame.set_theta(
                initial_theta + 360 * DEG * orbit_progress.get_value()
            )
        )
        self.play(
            ShowCreation(curve, rate_func=linear),
            MoveAlongPath(tracer, curve, rate_func=linear),
            orbit_progress.animate.set_value(1),
            run_time=40,
            rate_func=linear,
        )
        self.frame.clear_updaters()
        self.play(FadeOut(tracer), run_time=0.4)
