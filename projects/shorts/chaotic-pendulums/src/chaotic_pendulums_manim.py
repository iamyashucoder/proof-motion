import numpy as np
from manim import *

config.frame_height = 14


def simulate(count=1000, frames=500, dt=.004, substeps=8, near_identical=False):
    """Vectorized equal-mass, equal-length double-pendulum integration."""
    rng = np.random.default_rng(7)
    state = np.empty((count, 4), dtype=float)
    if near_identical:
        # Reference-style start: visually one pendulum, with only microscopic
        # differences that later explode into different trajectories.
        state[:, 0] = 2.10 + rng.normal(0, 7e-4, count)
        state[:, 1] = 2.22 + rng.normal(0, 7e-4, count)
        state[:, 2] = rng.normal(0, 8e-4, count)
        state[:, 3] = rng.normal(0, 8e-4, count)
    else:
        angle_band = np.linspace(-.46, .46, count)
        state[:, 0] = 2.24 + angle_band + rng.normal(0, .035, count)
        state[:, 1] = 2.42 + rng.uniform(-.82, .82, count)
        state[:, 2] = rng.uniform(-.75, .75, count)
        state[:, 3] = rng.uniform(-.85, .85, count)
    result = np.empty((frames, count, 4), dtype=float)

    def derivative(s):
        a, b, va, vb = s.T
        delta = a - b
        den = 3 - np.cos(2*delta)
        aa = (-3*9.8*np.sin(a) - 9.8*np.sin(a-2*b) - 2*np.sin(delta)*(vb*vb + va*va*np.cos(delta))) / den
        ab = (2*np.sin(delta)*(2*va*va + 2*9.8*np.cos(a) + vb*vb*np.cos(delta))) / den
        return np.stack((va, vb, aa, ab), axis=1)

    for frame in range(frames):
        result[frame] = state
        for _ in range(substeps):
            k1 = derivative(state)
            k2 = derivative(state + .5*dt*k1)
            k3 = derivative(state + .5*dt*k2)
            k4 = derivative(state + dt*k3)
            state += dt*(k1 + 2*k2 + 2*k3 + k4)/6
    return result


class ChaoticPendulums(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        data = simulate()
        frames, count, _ = data.shape
        # Each hue receives the same number of pendulums.  Repeating the
        # colours across small batches prevents one final colour layer from
        # visually covering the others.
        palette = ["#123B78", "#145A32", "#7B1E2B", "#5B2C83", "#7D3C98", "#B03A73"]
        display_indices = np.arange(count)
        title = Text("CHAOTIC PENDULUMS", font_size=39, color="#F4F7FF", weight="BOLD").to_edge(UP, buff=.55)
        subtitle = Text("1,000 systems. One pivot. A visible cloud from the first frame.", font_size=18, color="#AAB8D0").next_to(title, DOWN, buff=.12)
        pivot = UP*.5
        length = 2.0
        tracker = ValueTracker(0)

        # Faint reference rings make the diverging cloud easier to read.
        halo = VGroup(*[Circle(radius=r, color="#243A5D", stroke_width=1.2, stroke_opacity=.42).move_to(pivot) for r in [length, 2*length]])
        phase_box = RoundedRectangle(width=5.8, height=2.15, corner_radius=.16, stroke_color="#30496E", stroke_width=2).move_to(DOWN*4.5)
        phase_title = Text("PHASE SPACE  ·  angle vs. angular velocity", font_size=16, color="#AAB8D0").move_to(phase_box.get_top()+DOWN*.25)

        def pendulum_cloud():
            f = min(frames-1, int(tracker.get_value()))
            state = data[f]
            # Batching keeps the full 1,000-pendulum spectrum efficient.
            batches = 6
            trails_old = [VMobject(stroke_color=palette[j], stroke_width=1.25, stroke_opacity=.12) for j in range(batches)]
            trails_mid = [VMobject(stroke_color=palette[j], stroke_width=1.6, stroke_opacity=.26) for j in range(batches)]
            trails_new = [VMobject(stroke_color=palette[j], stroke_width=2.1, stroke_opacity=.52) for j in range(batches)]
            rods = [VMobject(stroke_color=palette[j], stroke_width=4.5, stroke_opacity=.32) for j in range(batches)]
            endpoints = [VMobject(stroke_color=palette[j], stroke_width=4.2, stroke_opacity=.85) for j in range(batches)]
            for i, (a, b, va, vb) in enumerate(state):
                # Every system shares the same physical ceiling point.
                local_pivot = pivot
                p1 = local_pivot + length*np.array([np.sin(a), -np.cos(a), 0])
                p2 = p1 + length*np.array([np.sin(b), -np.cos(b), 0])
                if i not in display_indices:
                    continue
                rod = rods[i % batches]
                colour_group = i % batches
                # The opening establishes that these are double pendulums.
                # In the late chaos phase, arms vanish to avoid a spoke wheel.
                if f < 115:
                    rod.start_new_path(local_pivot)
                    rod.add_line_to(p1)
                    rod.start_new_path(p1)
                    rod.add_line_to(p2)
                endpoints[colour_group].start_new_path(p2 + LEFT*.022)
                endpoints[colour_group].add_line_to(p2 + RIGHT*.022)
                # Only 56 long trails: old portions are dim and newer portions
                # are bright, while all other systems remain moving endpoints.
                if f > 115 and i % 18 == 0:
                    history = data[max(0, f-180):f+1:12, i]
                    path = []
                    for hidx, (ha, hb, _, _) in enumerate(history):
                        hp1 = local_pivot + length*np.array([np.sin(ha), -np.cos(ha), 0])
                        path.append(hp1 + length*np.array([np.sin(hb), -np.cos(hb), 0]))
                    trail_parts = [trails_old[colour_group], trails_mid[colour_group], trails_new[colour_group]]
                    cuts = [0, len(path)//3, 2*len(path)//3, len(path)]
                    for part, begin, end in zip(trail_parts, cuts[:-1], cuts[1:]):
                        if end - begin > 1:
                            part.start_new_path(path[begin])
                            for point in path[begin+1:end]:
                                part.add_line_to(point)
            return VGroup(*trails_old, *trails_mid, *trails_new, *rods, *endpoints, Dot(pivot, radius=.105, color="#F4F7FF"))

        def phase_cloud():
            f = min(frames-1, int(tracker.get_value()))
            state = data[f]
            batches = 6
            cloud_points = [VMobject(stroke_color=palette[j % len(palette)], stroke_width=2.4, stroke_opacity=.68) for j in range(batches)]
            center = phase_box.get_center()+DOWN*.08
            for i, (a, b, va, vb) in enumerate(state):
                if i not in display_indices:
                    continue
                x = np.clip((a-1.82)*120, -2.45, 2.45)
                y = np.clip(va*.75, -0.68, .68)
                point = center+RIGHT*x+UP*y
                dots = cloud_points[min(batches - 1, i*batches//count)]
                dots.start_new_path(point + LEFT*.016)
                dots.add_line_to(point + RIGHT*.016)
            return VGroup(*cloud_points)

        cloud = always_redraw(pendulum_cloud)
        phase = always_redraw(phase_cloud)
        start_caption = Text("1,000 pendulums begin as one shared-pivot bundle", font_size=20, color="#63E6FF").move_to(DOWN*2.95)
        end_caption = Text("Tiny differences amplify into chaos.", font_size=22, color="#FFB654").move_to(DOWN*2.95)

        self.play(FadeIn(title), FadeIn(subtitle), FadeIn(halo), FadeIn(cloud), FadeIn(phase_box), FadeIn(phase_title), FadeIn(phase), FadeIn(start_caption), run_time=.7)
        self.play(tracker.animate.set_value(80), run_time=3.0, rate_func=linear)
        self.play(Transform(start_caption, end_caption), run_time=.35)
        # Stop before the former trails/endpoints section begins.
        self.play(tracker.animate.set_value(110), run_time=1.5, rate_func=linear)
        self.play(FadeOut(VGroup(title, subtitle, halo, cloud, phase_box, phase_title, phase, start_caption)), run_time=.5)


class ReferenceStyleChaos(Scene):
    """Minimal, reference-inspired chaos visual without a pendulum count label."""
    def construct(self):
        self.camera.background_color = "#101010"
        data = simulate(count=1000, frames=650, dt=.006, substeps=8, near_identical=True)
        frames, count, _ = data.shape
        colours = color_gradient(["#FFEA2B", "#FF8B18", "#FF3B73", "#C20CFF", "#FFEA2B"], count)
        pivot = ORIGIN + UP*.15
        length = 2.15
        tracker = ValueTracker(0)

        def bundle():
            f = min(frames - 1, int(tracker.get_value()))
            # Colour batches keep all 1,000 real systems efficient to render.
            batches = 64
            rods = [VMobject(stroke_color=colours[int(j*(count-1)/(batches-1))], stroke_width=1.15, stroke_opacity=.74) for j in range(batches)]
            for i, (a, b, _, _) in enumerate(data[f]):
                p1 = pivot + length*np.array([np.sin(a), -np.cos(a), 0])
                p2 = p1 + length*np.array([np.sin(b), -np.cos(b), 0])
                rod = rods[min(batches - 1, i*batches//count)]
                rod.start_new_path(pivot)
                rod.add_line_to(p1)
                rod.start_new_path(p1)
                rod.add_line_to(p2)
            return VGroup(*rods)

        pendulums = always_redraw(bundle)
        self.add(pendulums)
        self.wait(.35)
        # Stay in the asymmetric divergence window.  Letting this ensemble
        # evolve far longer fills every angle and turns into a spoke circle.
        self.play(tracker.animate.set_value(190), run_time=18, rate_func=linear)
        self.play(FadeOut(pendulums), run_time=.35)


def simulate_multi(count=1000, links=3, frames=500, dt=.005, substeps=7):
    """Vectorised equal-mass, equal-length multi-link pendulum simulation."""
    rng = np.random.default_rng(19)
    n = links
    state = np.empty((count, 2*n), dtype=float)
    base = np.linspace(2.06, 2.34, n)
    state[:, :n] = base + rng.normal(0, 7e-4, (count, n))
    state[:, n:] = rng.normal(0, 8e-4, (count, n))
    result = np.empty((frames, count, 2*n), dtype=float)
    weights = np.arange(n, 0, -1, dtype=float)
    g = 9.8

    def derivative(s):
        theta, velocity = s[:, :n], s[:, n:]
        mass_matrix = np.empty((count, n, n))
        derivatives = np.zeros((count, n, n, n))
        for i in range(n):
            for j in range(n):
                factor = weights[max(i, j)]
                delta = theta[:, i] - theta[:, j]
                mass_matrix[:, i, j] = factor * np.cos(delta)
                if i != j:
                    derivatives[:, i, j, i] = -factor * np.sin(delta)
                    derivatives[:, i, j, j] = factor * np.sin(delta)
        coriolis = np.zeros((count, n))
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    gamma = .5 * (derivatives[:, i, j, k] + derivatives[:, i, k, j] - derivatives[:, j, k, i])
                    coriolis[:, i] += gamma * velocity[:, j] * velocity[:, k]
        gravity = g * weights[None, :] * np.sin(theta)
        acceleration = np.linalg.solve(mass_matrix, -(coriolis + gravity)[..., None])[..., 0]
        return np.concatenate((velocity, acceleration), axis=1)

    for frame in range(frames):
        result[frame] = state
        for _ in range(substeps):
            k1 = derivative(state)
            k2 = derivative(state + .5*dt*k1)
            k3 = derivative(state + .5*dt*k2)
            k4 = derivative(state + dt*k3)
            state += dt*(k1 + 2*k2 + 2*k3 + k4)/6
    return result


class TriplePendulumChaos(Scene):
    def construct(self):
        self.camera.background_color = "#101010"
        data = simulate_multi(links=3)
        frames, count, _ = data.shape
        colours = color_gradient(["#FFEA2B", "#FF8B18", "#FF3B73", "#C20CFF", "#FFEA2B"], count)
        pivot = ORIGIN + UP*.2
        length = 1.45
        tracker = ValueTracker(0)

        def bundle():
            f = min(frames - 1, int(tracker.get_value()))
            batches = 64
            rods = [VMobject(stroke_color=colours[int(j*(count-1)/(batches-1))], stroke_width=1.05, stroke_opacity=.72) for j in range(batches)]
            for i in range(0, count, 3):
                row = data[f, i]
                a, b, c = row[:3]
                p1 = pivot + length*np.array([np.sin(a), -np.cos(a), 0])
                p2 = p1 + length*np.array([np.sin(b), -np.cos(b), 0])
                p3 = p2 + length*np.array([np.sin(c), -np.cos(c), 0])
                rod = rods[min(batches - 1, i*batches//count)]
                rod.start_new_path(pivot)
                rod.add_line_to(p1)
                rod.start_new_path(p1)
                rod.add_line_to(p2)
                rod.start_new_path(p2)
                rod.add_line_to(p3)
            return VGroup(*rods)

        pendulums = always_redraw(bundle)
        self.add(pendulums)
        self.wait(.35)
        # As with the reference, end during asymmetric divergence rather than
        # letting the bundle fill every angle into a radial disc.
        self.play(tracker.animate.set_value(220), run_time=18, rate_func=linear)
        self.play(FadeOut(pendulums), run_time=.35)


class QuadruplePendulumChaos(Scene):
    def construct(self):
        self.camera.background_color = "#101010"
        data = simulate_multi(links=4)
        frames, count, _ = data.shape
        colours = color_gradient(["#FFEA2B", "#FF8B18", "#FF3B73", "#C20CFF", "#FFEA2B"], count)
        pivot = ORIGIN + UP*.25
        length = 1.12
        tracker = ValueTracker(0)

        def bundle():
            f = min(frames - 1, int(tracker.get_value()))
            batches = 64
            rods = [VMobject(stroke_color=colours[int(j*(count-1)/(batches-1))], stroke_width=.96, stroke_opacity=.72) for j in range(batches)]
            for i in range(0, count, 3):
                row = data[f, i]
                point = pivot.copy()
                rod = rods[min(batches - 1, i*batches//count)]
                for angle in row[:4]:
                    next_point = point + length*np.array([np.sin(angle), -np.cos(angle), 0])
                    rod.start_new_path(point)
                    rod.add_line_to(next_point)
                    point = next_point
            return VGroup(*rods)

        pendulums = always_redraw(bundle)
        self.add(pendulums)
        self.wait(.35)
        self.play(tracker.animate.set_value(185), run_time=18, rate_func=linear)
        self.play(FadeOut(pendulums), run_time=.35)


class HeadingDouble(Scene):
    def construct(self):
        title = Text("DOUBLE PENDULUMS", font_size=62, color=WHITE, weight="BOLD").to_edge(UP, buff=.9)
        self.add(title)


class HeadingTriple(Scene):
    def construct(self):
        title = Text("TRIPLE PENDULUMS", font_size=62, color=WHITE, weight="BOLD").to_edge(UP, buff=.9)
        self.add(title)
