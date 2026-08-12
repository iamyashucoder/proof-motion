from itertools import product
from math import cos, sin
from manim import *


config.frame_height = 14.0


def clamp(value, lower, upper):
    return max(lower, min(upper, value))


class EqualScaleHypercube(Scene):
    dimension = 4

    def construct(self):
        self.camera.background_color = "#050914"
        cyan, violet, orange, soft, muted = "#63E6FF", "#9E7BFF", "#FFB654", "#F4F7FF", "#AAB8D0"
        cyan_c, violet_c, orange_c = ManimColor(cyan), ManimColor(violet), ManimColor(orange)
        rng = np.random.default_rng(41)
        stars = VGroup(*[
            Dot(np.array([rng.uniform(-3.75, 3.75), rng.uniform(-6.5, 6.5), 0]), radius=rng.uniform(.006, .015), color=interpolate_color(cyan_c, violet_c, rng.uniform(0, 1)), fill_opacity=.26)
            for _ in range(70)
        ])
        self.add(stars)

        n = self.dimension
        name = "TESSERACT" if n == 4 else ("5D HYPERCUBE" if n == 5 else f"{n}D HYPERCUBE")
        subtitle_text = "A 4D hypercube, projected into view" if n == 4 else f"A {n}-dimensional hypercube, projected into view"
        title = Text(name, font_size=45 if n <= 5 else 42, color=soft, weight="BOLD").to_edge(UP, buff=.58)
        subtitle = Text(subtitle_text, font_size=20, color=muted).next_to(title, DOWN, buff=.14)

        vertices = list(product((-1, 1), repeat=n))
        # The bit-flip construction gives every edge of the n-cube exactly once.
        all_edges = [(index, index ^ (1 << bit)) for index in range(1 << n) for bit in range(n) if index < (index ^ (1 << bit))]
        edge_limit = {4: 32, 5: 80, 6: 160, 7: 180, 8: 170, 9: 155, 10: 140}[n]
        edge_step = max(1, len(all_edges) // edge_limit)
        edges = all_edges[::edge_step]
        point_step = max(1, len(vertices) // 110)
        theta = ValueTracker(0)

        def raw_projection(vertex, angle):
            values = [float(value) for value in vertex]
            # Fold every axis beyond z into x/y using rotations. This keeps
            # dimensions comparable; the final size is normalized below.
            for axis in range(n - 1, 2, -1):
                a, b = angle * (.34 + .055*axis), angle * (.22 + .035*axis)
                values[0], values[axis] = values[0]*cos(a) - values[axis]*sin(a), values[0]*sin(a) + values[axis]*cos(a)
                values[1], values[axis] = values[1]*cos(b) - values[axis]*sin(b), values[1]*sin(b) + values[axis]*cos(b)
            x, y, z = values[:3]
            x, z = x*cos(-.62) - z*sin(-.62), x*sin(-.62) + z*cos(-.62)
            y, z = y*cos(.36) - z*sin(.36), y*sin(.36) + z*cos(.36)
            return np.array([x, y, 0]), sum(values[3:])

        def wireframe():
            angle = theta.get_value()
            raw = [raw_projection(vertex, angle) for vertex in vertices]
            max_horizontal_extent = max(abs(point[0]) for point, _ in raw)
            # Fill the horizontal frame consistently, leaving a slim edge margin.
            points = [(point * (3.65 / max_horizontal_extent) + DOWN*.22, depth) for point, depth in raw]
            group = VGroup()
            for start, end in edges:
                a, da = points[start]
                b, db = points[end]
                tone = clamp((da + db + n) / (2*n), 0, 1)
                color = interpolate_color(violet_c, cyan_c, tone)
                high_dimension = n >= 7
                group.add(Line(a, b, stroke_color=color, stroke_width=9 if high_dimension else 7, stroke_opacity=.16 if high_dimension else .08))
                group.add(Line(a, b, stroke_color=color, stroke_width=21.5 if high_dimension else 19.0, stroke_opacity=.94 if high_dimension else .86))
            for index in range(0, len(vertices), point_step):
                point, depth = points[index]
                group.add(Dot(point, radius=.038 if n >= 7 else .035, color=interpolate_color(cyan_c, orange_c, clamp((depth+n/2)/n, 0, 1))))
            return group

        shape = always_redraw(wireframe)
        vertices_count, edges_count = 2**n, n*2**(n-1)
        suffix = "  •  sampled projection" if n >= 7 else ""
        caption = Text(f"{vertices_count} vertices  •  {edges_count} edges{suffix}", font_size=20, color=muted).move_to(DOWN*4.55)
        # Exactly 5 seconds: 0.4s in + 4.2s rotation + 0.4s out.
        self.play(FadeIn(title, shift=DOWN*.12), FadeIn(subtitle, shift=DOWN*.12), FadeIn(shape, scale=.92), FadeIn(caption), run_time=.4)
        self.play(theta.animate.set_value(TAU*1.65), run_time=4.2, rate_func=linear)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(shape), FadeOut(caption), run_time=.4)


class Hypercube4(EqualScaleHypercube): dimension = 4
class Hypercube5(EqualScaleHypercube): dimension = 5
class Hypercube6(EqualScaleHypercube): dimension = 6
class Hypercube7(EqualScaleHypercube): dimension = 7
class Hypercube8(EqualScaleHypercube): dimension = 8
class Hypercube9(EqualScaleHypercube): dimension = 9
class Hypercube10(EqualScaleHypercube): dimension = 10
