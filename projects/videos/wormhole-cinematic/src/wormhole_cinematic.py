from manimlib import *
import numpy as np


class WormholeCinematic(InteractiveScene):
    """A text-free, vertical 3D wormhole fly-through."""

    def construct(self):
        cyan, violet, pink, gold, white = "#4DDCFF", "#9B5CFF", "#FF4FA3", "#FFD54A", "#F8FBFF"
        rng = np.random.default_rng(9)
        self.frame.reorient(74, -6, 0).move_to(OUT * 4.5)

        # Deep, layered starfield.
        stars = Group()
        for _ in range(270):
            p = np.array([rng.uniform(-7.5, 7.5), rng.uniform(-8, 8), rng.uniform(-15, 8)])
            dot = Dot(p, radius=rng.uniform(.006, .027)).set_color(white)
            dot.set_opacity(rng.uniform(.18, .92))
            stars.add(dot)
        far_halo = VGroup(
            Circle(radius=6.2, stroke_width=42).set_color(violet).set_opacity(.035).shift(IN*8),
            Circle(radius=4.5, stroke_width=30).set_color(cyan).set_opacity(.045).shift(IN*7),
        )
        self.add(stars, far_halo)

        # 38 rings describe a pinched, twisting spacetime throat.
        rings = Group()
        ring_glow = Group()
        for k in range(38):
            z = 6.0 - .43 * k
            radius = .46 + .081 * abs(k - 19) ** 1.13
            color = cyan if k % 3 else violet
            ring = Circle(radius=radius, stroke_width=3.2).set_color(color)
            ring.shift(OUT * z)
            ring.rotate((k - 19) * 2.0 * DEGREES, axis=OUT)
            glow = ring.copy().set_stroke(color, width=17, opacity=.10)
            rings.add(ring)
            ring_glow.add(glow)

        # A bright, animated throat at the centre.
        throat = Sphere(radius=.42, resolution=(18, 32)).set_color(gold).move_to(IN*2.17)
        throat_glow = Sphere(radius=.70, resolution=(16, 28)).set_color(pink).set_opacity(.12)
        throat_glow.move_to(throat.get_center())
        core_rings = VGroup(*[
            Circle(radius=.48 + i*.14, stroke_width=4).set_color(gold if i % 2 else pink)
            .shift(throat.get_center()).rotate(PI/2, axis=RIGHT)
            for i in range(5)
        ])

        # Hot particles spiral inward; their trails give the tunnel motion.
        particles = Group()
        trails = Group()
        for j in range(12):
            a = TAU * j / 12
            p = Sphere(radius=.055, resolution=(8, 14)).set_color(gold if j % 2 else pink)
            p.move_to(np.array([2.2*np.cos(a), 2.2*np.sin(a), 3.8 - .22*j]))
            particles.add(p)
            trails.add(TracedPath(p.get_center, stroke_color=gold if j % 2 else pink,
                                  stroke_width=2.5))

        self.add(trails)
        self.play(FadeIn(ring_glow), FadeIn(rings), FadeIn(throat_glow), FadeIn(throat),
                  FadeIn(core_rings), FadeIn(particles), run_time=1.2)

        # First approach: tunnel breathes and particles are drawn to its centre.
        particle_targets = []
        for j, p in enumerate(particles):
            angle = TAU * j / 12 + PI * 1.7
            particle_targets.append(np.array([.38*np.cos(angle), .38*np.sin(angle), -2.17]))
        self.play(
            *[p.animate.move_to(target) for p, target in zip(particles, particle_targets)],
            Rotate(rings, PI*.18, axis=OUT), Rotate(core_rings, PI*1.5, axis=UP),
            throat.animate.scale(1.35), throat_glow.animate.scale(1.55),
            self.frame.animate.move_to(OUT*1.0).reorient(75, 11, 0),
            run_time=3.3, rate_func=smooth,
        )

        # Energy burst: circles expand away from the throat while the camera dives in.
        shockwaves = VGroup(*[
            Circle(radius=.28 + .10*i, stroke_width=5).set_color(gold if i % 2 else pink)
            .move_to(throat.get_center()) for i in range(6)
        ])
        self.play(FadeIn(shockwaves), Flash(throat.get_center(), color=white, flash_radius=1.2,
                  line_length=.32), run_time=.35)
        self.play(
            *[wave.animate.scale(10).set_opacity(0) for wave in shockwaves],
            Rotate(rings, PI*.42, axis=OUT), Rotate(core_rings, PI*2, axis=RIGHT),
            self.frame.animate.move_to(IN*1.85).reorient(78, -4, 0),
            run_time=3.0, rate_func=rush_into,
        )

        # Pass through the throat: all rings stream past camera, then a final reverse reveal.
        self.play(
            rings.animate.shift(OUT*10.5), ring_glow.animate.shift(OUT*10.5),
            particles.animate.shift(OUT*8.5),
            self.frame.animate.move_to(IN*5.2).reorient(80, 18, 0),
            run_time=3.0, rate_func=linear,
        )
        self.play(
            self.frame.animate.move_to(OUT*.7).reorient(73, -24, 0),
            throat.animate.scale(.70), throat_glow.animate.scale(.70),
            Rotate(core_rings, PI, axis=OUT),
            run_time=2.1, rate_func=smooth,
        )
        self.wait(1.4)
        self.remove(trails)
        self.play(FadeOut(Group(stars, far_halo, ring_glow, rings, throat_glow, throat, core_rings,
                                particles)), run_time=.8)
