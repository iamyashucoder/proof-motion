from itertools import product
from math import cos, sin
from manim import *


config.frame_height = 14.0


def clamp(value, lower, upper):
    return max(lower, min(upper, value))


class RotatingTesseract(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        cyan, violet, orange, soft, muted = "#63E6FF", "#9E7BFF", "#FFB654", "#F4F7FF", "#AAB8D0"
        cyan_c, violet_c, orange_c = ManimColor(cyan), ManimColor(violet), ManimColor(orange)
        rng = np.random.default_rng(17)
        stars = VGroup(*[
            Dot(
                point=np.array([rng.uniform(-3.75, 3.75), rng.uniform(-6.5, 6.5), 0]),
                radius=rng.uniform(.006, .018),
                color=interpolate_color(cyan_c, violet_c, rng.uniform(0, 1)),
                fill_opacity=rng.uniform(.16, .48),
            )
            for _ in range(95)
        ])
        self.add(stars)

        title = Text("TESSERACT", font_size=45, color=soft, weight="BOLD").to_edge(UP, buff=.58)
        subtitle = Text("A rotating projection of a 4D hypercube", font_size=22, color=muted).next_to(title, DOWN, buff=.14)
        self.play(FadeIn(title, shift=DOWN*.18), FadeIn(subtitle, shift=DOWN*.18), run_time=.75)

        # The tesseract has 16 vertices: every choice of ±1 along x, y, z, w.
        vertices = list(product((-1, 1), repeat=4))
        edges = [(i, j) for i, a in enumerate(vertices) for j, b in enumerate(vertices) if sum(x != y for x, y in zip(a, b)) == 1 and i < j]
        theta = ValueTracker(0)

        def project(vertex, angle):
            x, y, z, w = vertex
            # Rotate through planes containing w: this is the 4D movement.
            x, w = x*cos(angle) - w*sin(angle), x*sin(angle) + w*cos(angle)
            y, w = y*cos(angle*.73) - w*sin(angle*.73), y*sin(angle*.73) + w*cos(angle*.73)
            # Project w, then use a fixed 3D camera angle to place it on screen.
            four_scale = 3.4 / (4.3 - w)
            x, y, z = x*four_scale, y*four_scale, z*four_scale
            yaw, pitch = -.68, .38
            x, z = x*cos(yaw) - z*sin(yaw), x*sin(yaw) + z*cos(yaw)
            y, z = y*cos(pitch) - z*sin(pitch), y*sin(pitch) + z*cos(pitch)
            scale = 6.2 / (3.7 - z)
            return np.array([x*scale, y*scale - .35, 0]), w

        def tesseract_lines():
            angle = theta.get_value()
            lines = VGroup()
            # Faint trailing projections make the fourth-dimensional movement
            # feel more spatial without obscuring the main object.
            for ghost_angle, opacity in ((angle-.52, .07), (angle-.27, .13)):
                ghost_points = [project(vertex, ghost_angle)[0] for vertex in vertices]
                for start, end in edges:
                    lines.add(Line(ghost_points[start], ghost_points[end], stroke_color=violet_c, stroke_width=5.5, stroke_opacity=opacity))
            projected = [project(vertex, angle) for vertex in vertices]
            for start, end in edges:
                a, wa = projected[start]
                b, wb = projected[end]
                # Edges with a larger w component glow warmer, making the 4D
                # projection visibly change as it rotates.
                color = interpolate_color(violet_c, orange_c, clamp((wa + wb + 2) / 4, 0, 1))
                lines.add(Line(a, b, stroke_color=color, stroke_width=13, stroke_opacity=.10))
                lines.add(Line(a, b, stroke_color=color, stroke_width=3.3, stroke_opacity=.98))
            for point, w in projected:
                color = interpolate_color(cyan_c, orange_c, clamp((w + 1.8) / 3.6, 0, 1))
                lines.add(Dot(point, radius=.06, color=color))
            return lines

        def orbital_arcs():
            angle = theta.get_value()
            arcs = VGroup()
            for radius, start, arc_color in ((2.66, angle*.52, cyan_c), (2.02, -angle*.38+1.4, violet_c)):
                arcs.add(Arc(radius=radius, start_angle=start, angle=1.62, color=arc_color, stroke_width=1.7, stroke_opacity=.28).shift(DOWN*.35))
                arcs.add(Arc(radius=radius, start_angle=start+PI, angle=1.05, color=arc_color, stroke_width=1.7, stroke_opacity=.20).shift(DOWN*.35))
            return arcs

        orbit_group = always_redraw(orbital_arcs)
        object_group = always_redraw(tesseract_lines)
        caption = Text("16 vertices  •  32 edges  •  8 cubic cells", font_size=21, color=muted).move_to(DOWN*4.55)
        self.play(FadeIn(orbit_group), FadeIn(object_group, scale=.86), FadeIn(caption), run_time=1.0)
        self.play(theta.animate.set_value(TAU*.75), run_time=4.0, rate_func=linear)

        label_4d = Text("Rotate through the fourth dimension (w)", font_size=26, color=orange, weight="BOLD").move_to(DOWN*3.75)
        self.play(FadeIn(label_4d, shift=UP*.1), theta.animate.set_value(TAU*1.45), run_time=3.4, rate_func=linear)
        self.play(FadeOut(label_4d), run_time=.3)

        takeaway = RoundedRectangle(corner_radius=.2, width=6.65, height=1.2, stroke_color=cyan, stroke_width=2.5, fill_color="#0D1A30", fill_opacity=.95).move_to(DOWN*4.42)
        takeaway_text = Text("What you see is a 3D shadow of a 4D shape.", font_size=23, color=soft, weight="BOLD").move_to(takeaway)
        self.play(FadeOut(caption), FadeIn(takeaway, scale=.95), Write(takeaway_text), run_time=.75)
        self.play(theta.animate.set_value(TAU*2.15), run_time=3.0, rate_func=linear)
        self.wait(.7)

        # Continue naturally into the next dimension: a 5D hypercube is also
        # called a penteract and contains two tesseracts connected together.
        self.play(
            FadeOut(object_group), FadeOut(orbit_group), FadeOut(takeaway), FadeOut(takeaway_text),
            FadeOut(title), FadeOut(subtitle), run_time=.55,
        )
        title_5d = Text("5D HYPERCUBE", font_size=45, color=soft, weight="BOLD").to_edge(UP, buff=.58)
        subtitle_5d = Text("A penteract: two tesseracts joined through a fifth axis", font_size=19, color=muted).next_to(title_5d, DOWN, buff=.14)
        self.play(FadeIn(title_5d, shift=DOWN*.18), FadeIn(subtitle_5d, shift=DOWN*.18), run_time=.7)

        vertices_5d = list(product((-1, 1), repeat=5))
        edges_5d = [(i, j) for i, a in enumerate(vertices_5d) for j, b in enumerate(vertices_5d) if sum(x != y for x, y in zip(a, b)) == 1 and i < j]
        phi = ValueTracker(0)

        def project_5d(vertex, angle):
            x, y, z, w, v = vertex
            # First compress the fifth axis (v), then the fourth (w), then
            # display the resulting 3D form using the same virtual camera.
            x, v = x*cos(angle*.88) - v*sin(angle*.88), x*sin(angle*.88) + v*cos(angle*.88)
            z, v = z*cos(angle*.46) - v*sin(angle*.46), z*sin(angle*.46) + v*cos(angle*.46)
            fifth_scale = 3.7 / (4.75 - v)
            x, y, z, w = x*fifth_scale, y*fifth_scale, z*fifth_scale, w*fifth_scale
            y, w = y*cos(angle*.63) - w*sin(angle*.63), y*sin(angle*.63) + w*cos(angle*.63)
            fourth_scale = 3.3 / (4.25 - w)
            x, y, z = x*fourth_scale, y*fourth_scale, z*fourth_scale
            yaw, pitch = -.66, .36
            x, z = x*cos(yaw) - z*sin(yaw), x*sin(yaw) + z*cos(yaw)
            y, z = y*cos(pitch) - z*sin(pitch), y*sin(pitch) + z*cos(pitch)
            scale = 4.25 / (3.9 - z)
            return np.array([x*scale, y*scale - .38, 0]), v

        def penteract_lines():
            angle = phi.get_value()
            projected = [project_5d(vertex, angle) for vertex in vertices_5d]
            group = VGroup()
            for start, end in edges_5d:
                a, va = projected[start]
                b, vb = projected[end]
                color = interpolate_color(cyan_c, orange_c, clamp((va + vb + 2) / 4, 0, 1))
                group.add(Line(a, b, stroke_color=color, stroke_width=10, stroke_opacity=.075))
                group.add(Line(a, b, stroke_color=color, stroke_width=2.15, stroke_opacity=.84))
            for point, v in projected:
                group.add(Dot(point, radius=.042, color=interpolate_color(violet_c, orange_c, clamp((v + 1.6) / 3.2, 0, 1))))
            return group

        penteract = always_redraw(penteract_lines)
        caption_5d = Text("32 vertices  •  80 edges  •  10 tesseract cells", font_size=20, color=muted).move_to(DOWN*4.55)
        self.play(FadeIn(penteract, scale=.88), FadeIn(caption_5d), run_time=1.0)
        self.play(phi.animate.set_value(TAU*.74), run_time=4.3, rate_func=linear)
        fifth_caption = Text("Now the shape rotates through a fifth direction (v)", font_size=24, color=orange, weight="BOLD").move_to(DOWN*3.72)
        self.play(FadeIn(fifth_caption, shift=UP*.12), phi.animate.set_value(TAU*1.43), run_time=3.4, rate_func=linear)
        self.play(FadeOut(fifth_caption), run_time=.3)
        takeaway_5d = RoundedRectangle(corner_radius=.2, width=6.75, height=1.25, stroke_color=violet, stroke_width=2.5, fill_color="#171329", fill_opacity=.95).move_to(DOWN*4.4)
        takeaway_5d_text = Text("5D adds another axis beyond x, y, z and w.", font_size=22, color=soft, weight="BOLD").move_to(takeaway_5d)
        self.play(FadeOut(caption_5d), FadeIn(takeaway_5d, scale=.95), Write(takeaway_5d_text), run_time=.75)
        self.play(phi.animate.set_value(TAU*2.05), run_time=3.0, rate_func=linear)
        self.wait(.8)

        # One more extension: the 6-cube is visually denser, so its wireframe
        # uses lighter edges while retaining the same projection idea.
        self.play(
            FadeOut(penteract), FadeOut(takeaway_5d), FadeOut(takeaway_5d_text),
            FadeOut(title_5d), FadeOut(subtitle_5d), run_time=.55,
        )
        title_6d = Text("6D HYPERCUBE", font_size=45, color=soft, weight="BOLD").to_edge(UP, buff=.58)
        subtitle_6d = Text("A 6D shape projected into the space we can see", font_size=21, color=muted).next_to(title_6d, DOWN, buff=.14)
        self.play(FadeIn(title_6d, shift=DOWN*.18), FadeIn(subtitle_6d, shift=DOWN*.18), run_time=.7)

        vertices_6d = list(product((-1, 1), repeat=6))
        edges_6d = [(i, j) for i, a in enumerate(vertices_6d) for j, b in enumerate(vertices_6d) if sum(x != y for x, y in zip(a, b)) == 1 and i < j]
        psi = ValueTracker(0)

        def project_6d(vertex, angle):
            x, y, z, w, v, u = vertex
            # Successive perspective projections: 6D → 5D → 4D → 3D → screen.
            x, u = x*cos(angle*.78) - u*sin(angle*.78), x*sin(angle*.78) + u*cos(angle*.78)
            z, u = z*cos(angle*.37) - u*sin(angle*.37), z*sin(angle*.37) + u*cos(angle*.37)
            sixth_scale = 3.5 / (4.7 - u)
            x, y, z, w, v = x*sixth_scale, y*sixth_scale, z*sixth_scale, w*sixth_scale, v*sixth_scale
            x, v = x*cos(angle*.59) - v*sin(angle*.59), x*sin(angle*.59) + v*cos(angle*.59)
            fifth_scale = 3.35 / (4.55 - v)
            x, y, z, w = x*fifth_scale, y*fifth_scale, z*fifth_scale, w*fifth_scale
            y, w = y*cos(angle*.45) - w*sin(angle*.45), y*sin(angle*.45) + w*cos(angle*.45)
            fourth_scale = 3.15 / (4.15 - w)
            x, y, z = x*fourth_scale, y*fourth_scale, z*fourth_scale
            yaw, pitch = -.62, .34
            x, z = x*cos(yaw) - z*sin(yaw), x*sin(yaw) + z*cos(yaw)
            y, z = y*cos(pitch) - z*sin(pitch), y*sin(pitch) + z*cos(pitch)
            scale = 5.15 / (3.85 - z)
            return np.array([x*scale, y*scale - .38, 0]), u

        def hexeract_lines():
            angle = psi.get_value()
            projected = [project_6d(vertex, angle) for vertex in vertices_6d]
            group = VGroup()
            for start, end in edges_6d:
                a, ua = projected[start]
                b, ub = projected[end]
                color = interpolate_color(violet_c, cyan_c, clamp((ua + ub + 2) / 4, 0, 1))
                group.add(Line(a, b, stroke_color=color, stroke_width=1.45, stroke_opacity=.58))
            for point, u in projected:
                group.add(Dot(point, radius=.027, color=interpolate_color(violet_c, orange_c, clamp((u + 1.8) / 3.6, 0, 1))))
            return group

        hexeract = always_redraw(hexeract_lines)
        caption_6d = Text("64 vertices  •  192 edges  •  12 penteract cells", font_size=20, color=muted).move_to(DOWN*4.55)
        self.play(FadeIn(hexeract, scale=.88), FadeIn(caption_6d), run_time=1.0)
        self.play(psi.animate.set_value(TAU*.68), run_time=4.2, rate_func=linear)
        sixth_caption = Text("A sixth independent direction makes the projection denser", font_size=21, color=orange, weight="BOLD").move_to(DOWN*3.72)
        self.play(FadeIn(sixth_caption, shift=UP*.12), psi.animate.set_value(TAU*1.34), run_time=3.3, rate_func=linear)
        self.play(FadeOut(sixth_caption), run_time=.3)
        takeaway_6d = RoundedRectangle(corner_radius=.2, width=6.75, height=1.25, stroke_color=cyan, stroke_width=2.5, fill_color="#102334", fill_opacity=.95).move_to(DOWN*4.4)
        takeaway_6d_text = Text("More dimensions add structure we can only project.", font_size=22, color=soft, weight="BOLD").move_to(takeaway_6d)
        self.play(FadeOut(caption_6d), FadeIn(takeaway_6d, scale=.95), Write(takeaway_6d_text), run_time=.75)
        self.play(psi.animate.set_value(TAU*1.98), run_time=3.0, rate_func=linear)
        self.wait(.8)

        # From 7D onward the number of edges grows exponentially. We retain
        # the real counts but deliberately sample the displayed wireframe so
        # the projection remains interpretable on a phone screen.
        self.play(
            FadeOut(hexeract), FadeOut(takeaway_6d), FadeOut(takeaway_6d_text),
            FadeOut(title_6d), FadeOut(subtitle_6d), run_time=.5,
        )

        for dimension in range(7, 11):
            title_hd = Text(f"{dimension}D HYPERCUBE", font_size=43, color=soft, weight="BOLD").to_edge(UP, buff=.58)
            subtitle_hd = Text(f"A {dimension}-dimensional shape, projected into view", font_size=20, color=muted).next_to(title_hd, DOWN, buff=.14)
            self.play(FadeIn(title_hd, shift=DOWN*.15), FadeIn(subtitle_hd, shift=DOWN*.15), run_time=.5)

            vertices_hd = list(product((-1, 1), repeat=dimension))
            all_edges_hd = [
                (i, j) for i, a in enumerate(vertices_hd) for j, b in enumerate(vertices_hd)
                if sum(x != y for x, y in zip(a, b)) == 1 and i < j
            ]
            # Use more edges for 7D and fewer relative edges for 10D; the
            # caption always reports the actual, unsampled combinatorics.
            edge_limit = {7: 448, 8: 500, 9: 560, 10: 620}[dimension]
            stride = max(1, len(all_edges_hd) // edge_limit)
            displayed_edges = all_edges_hd[::stride]
            point_stride = max(1, len(vertices_hd) // 180)
            displayed_points = list(range(0, len(vertices_hd), point_stride))
            tracker = ValueTracker(0)

            def project_high_dim(vertex, angle, n=dimension):
                coords = [float(value) for value in vertex]
                # Fold each extra axis into the first three through a sequence
                # of rotations and perspective scalings.
                for axis in range(n - 1, 2, -1):
                    rate = .31 + .07 * axis
                    a = angle * rate
                    coords[0], coords[axis] = (
                        coords[0] * cos(a) - coords[axis] * sin(a),
                        coords[0] * sin(a) + coords[axis] * cos(a),
                    )
                    b = angle * (rate * .67)
                    coords[1], coords[axis] = (
                        coords[1] * cos(b) - coords[axis] * sin(b),
                        coords[1] * sin(b) + coords[axis] * cos(b),
                    )
                    shrink = 3.15 / (4.35 - coords[axis])
                    for index in range(axis):
                        coords[index] *= shrink
                x, y, z = coords[:3]
                yaw, pitch = -.60, .33
                x, z = x*cos(yaw) - z*sin(yaw), x*sin(yaw) + z*cos(yaw)
                y, z = y*cos(pitch) - z*sin(pitch), y*sin(pitch) + z*cos(pitch)
                # Higher-dimensional projections shrink after repeated
                # perspective steps, so compensate progressively for clarity.
                scale = (7.5 + 4.0 * (n - 7)) / (4.0 - z)
                color_value = sum(coords[3:]) if n > 3 else 0
                return np.array([x*scale, y*scale - .38, 0]), color_value

            def high_dim_wireframe(n=dimension):
                angle = tracker.get_value()
                projected = [project_high_dim(vertex, angle, n) for vertex in vertices_hd]
                group = VGroup()
                for start, end in displayed_edges:
                    a, depth_a = projected[start]
                    b, depth_b = projected[end]
                    tone = clamp((depth_a + depth_b + n) / (2 * n), 0, 1)
                    color = interpolate_color(violet_c, cyan_c, tone)
                    group.add(Line(a, b, stroke_color=color, stroke_width=1.15 if n >= 9 else 1.45, stroke_opacity=.42 if n >= 9 else .58))
                for index in displayed_points:
                    point, depth = projected[index]
                    color = interpolate_color(cyan_c, orange_c, clamp((depth + n/2) / n, 0, 1))
                    group.add(Dot(point, radius=.018 if n >= 9 else .025, color=color))
                return group

            hypercube = always_redraw(high_dim_wireframe)
            vertex_count = 2 ** dimension
            edge_count = dimension * 2 ** (dimension - 1)
            facet_name = {7: "hexeract", 8: "7D cell", 9: "8D cell", 10: "9D cell"}[dimension]
            facet_count = 2 * dimension
            sample_suffix = "  •  sampled projection" if dimension >= 8 else ""
            caption_hd = Text(f"{vertex_count} vertices  •  {edge_count} edges  •  {facet_count} {facet_name}s{sample_suffix}", font_size=18, color=muted).move_to(DOWN*4.55)
            self.play(FadeIn(hypercube, scale=.90), FadeIn(caption_hd), run_time=.75)
            self.play(tracker.animate.set_value(TAU*.72), run_time=2.75, rate_func=linear)
            if dimension < 10:
                self.play(FadeOut(hypercube), FadeOut(caption_hd), FadeOut(title_hd), FadeOut(subtitle_hd), run_time=.38)
            else:
                final_box = RoundedRectangle(corner_radius=.2, width=6.85, height=1.25, stroke_color=orange, stroke_width=2.5, fill_color="#241A16", fill_opacity=.96).move_to(DOWN*4.4)
                final_text = Text("10D: structure beyond direct visualization.", font_size=22, color=soft, weight="BOLD").move_to(final_box)
                self.play(FadeOut(caption_hd), FadeIn(final_box, scale=.95), Write(final_text), run_time=.7)
                self.play(tracker.animate.set_value(TAU*1.40), run_time=2.6, rate_func=linear)
                self.wait(.8)
