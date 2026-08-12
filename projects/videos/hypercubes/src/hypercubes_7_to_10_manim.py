from itertools import product
from math import cos, sin
from manim import *


config.frame_height = 14.0


def clamp(value, lower, upper):
    return max(lower, min(upper, value))


class HypercubesSevenToTen(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        cyan, violet, orange, soft, muted = "#63E6FF", "#9E7BFF", "#FFB654", "#F4F7FF", "#AAB8D0"
        cyan_c, violet_c, orange_c = ManimColor(cyan), ManimColor(violet), ManimColor(orange)
        rng = np.random.default_rng(29)
        stars = VGroup(*[
            Dot(np.array([rng.uniform(-3.75, 3.75), rng.uniform(-6.5, 6.5), 0]), radius=rng.uniform(.006, .016), color=interpolate_color(cyan_c, violet_c, rng.uniform(0, 1)), fill_opacity=.3)
            for _ in range(80)
        ])
        self.add(stars)

        for dimension in range(7, 11):
            title = Text(f"{dimension}D HYPERCUBE", font_size=43, color=soft, weight="BOLD").to_edge(UP, buff=.58)
            subtitle = Text(f"A {dimension}-dimensional shape, projected into view", font_size=20, color=muted).next_to(title, DOWN, buff=.14)
            self.play(FadeIn(title, shift=DOWN*.12), FadeIn(subtitle, shift=DOWN*.12), run_time=.4)

            vertices = list(product((-1, 1), repeat=dimension))
            # Bit flips create exactly the edges of an n-dimensional hypercube.
            edges = [(index, index ^ (1 << bit)) for index in range(1 << dimension) for bit in range(dimension) if index < (index ^ (1 << bit))]
            edge_limit = {7: 180, 8: 160, 9: 140, 10: 120}[dimension]
            step = max(1, len(edges) // edge_limit)
            display_edges = edges[::step]
            point_step = max(1, len(vertices) // 96)
            tracker = ValueTracker(0)

            def project(vertex, angle, n=dimension):
                values = [float(value) for value in vertex]
                for axis in range(n - 1, 2, -1):
                    rate = .30 + .07 * axis
                    angle_a, angle_b = angle * rate, angle * rate * .61
                    values[0], values[axis] = values[0]*cos(angle_a) - values[axis]*sin(angle_a), values[0]*sin(angle_a) + values[axis]*cos(angle_a)
                    values[1], values[axis] = values[1]*cos(angle_b) - values[axis]*sin(angle_b), values[1]*sin(angle_b) + values[axis]*cos(angle_b)
                    factor = 3.10 / (4.30 - values[axis])
                    for index in range(axis):
                        values[index] *= factor
                x, y, z = values[:3]
                x, z = x*cos(-.60) - z*sin(-.60), x*sin(-.60) + z*cos(-.60)
                y, z = y*cos(.33) - z*sin(.33), y*sin(.33) + z*cos(.33)
                scale = (9.0 + 5.0*(n-7)) / (4.0-z)
                return np.array([x*scale, y*scale-.35, 0]), sum(values[3:])

            def wireframe(n=dimension):
                angle = tracker.get_value()
                points = [project(vertex, angle, n) for vertex in vertices]
                group = VGroup()
                for start, end in display_edges:
                    a, da = points[start]
                    b, db = points[end]
                    color = interpolate_color(violet_c, cyan_c, clamp((da+db+n)/(2*n), 0, 1))
                    group.add(Line(a, b, stroke_color=color, stroke_width=1.45, stroke_opacity=.62))
                for index in range(0, len(vertices), point_step):
                    point, depth = points[index]
                    group.add(Dot(point, radius=.026, color=interpolate_color(cyan_c, orange_c, clamp((depth+n/2)/n, 0, 1))))
                return group

            shape = always_redraw(wireframe)
            vertices_count, edges_count = 2**dimension, dimension*2**(dimension-1)
            suffix = "  •  sampled projection" if dimension >= 8 else ""
            caption = Text(f"{vertices_count} vertices  •  {edges_count} edges{suffix}", font_size=20, color=muted).move_to(DOWN*4.55)
            self.play(FadeIn(shape, scale=.9), FadeIn(caption), run_time=.55)
            self.play(tracker.animate.set_value(TAU*.9), run_time=2.15, rate_func=linear)
            if dimension < 10:
                self.play(FadeOut(shape), FadeOut(caption), FadeOut(title), FadeOut(subtitle), run_time=.3)
            else:
                end_box = RoundedRectangle(corner_radius=.2, width=6.85, height=1.2, stroke_color=orange, stroke_width=2.4, fill_color="#241A16", fill_opacity=.96).move_to(DOWN*4.38)
                end_text = Text("10D: structure beyond direct visualization.", font_size=22, color=soft, weight="BOLD").move_to(end_box)
                self.play(FadeOut(caption), FadeIn(end_box), Write(end_text), run_time=.6)
                self.play(tracker.animate.set_value(TAU*1.42), run_time=1.6, rate_func=linear)
                self.wait(.7)
