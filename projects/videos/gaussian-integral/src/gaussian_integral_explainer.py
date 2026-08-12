from manim import *

config.frame_height = 14


class GaussianIntegralExplainer(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#050914"
        white, cyan, violet, orange, muted = "#F4F7FF", "#63E6FF", "#9E7BFF", "#FFB654", "#AAB8D0"
        title = Text("THE GAUSSIAN INTEGRAL", font_size=38, color=white, weight="BOLD").to_edge(UP, buff=.55)
        start = MathTex(r"I=\int_{-\infty}^{\infty}e^{-x^2}\,dx", font_size=48, color=cyan).move_to(UP*1.7)
        statement = Text("A one-dimensional bell curve hides a circle.", font_size=22, color=muted).next_to(start, DOWN, buff=.25)
        self.play(FadeIn(title), Write(start), FadeIn(statement), run_time=.9)
        self.wait(.55)
        self.play(FadeOut(start), FadeOut(statement), run_time=.35)

        squared = MathTex(r"I^2=\iint_{\mathbb{R}^2} e^{-(x^2+y^2)}\,dx\,dy", font_size=42, color=white).move_to(UP*1.75)
        subtitle = Text("Squaring creates a two-dimensional Gaussian.", font_size=21, color=muted).next_to(squared, DOWN, buff=.2)
        self.play(Write(squared), FadeIn(subtitle), run_time=.8)

        axes = ThreeDAxes(x_range=[-2.6, 2.6, 1], y_range=[-2.6, 2.6, 1], z_range=[0, 1.1, .5], x_length=5.3, y_length=5.3, z_length=2.4, axis_config={"color": "#7286A8", "stroke_width": 2})
        surface = Surface(lambda u, v: axes.c2p(u, v, np.exp(-(u*u+v*v))), u_range=[-2.45, 2.45], v_range=[-2.45, 2.45], resolution=(32, 32), fill_color=violet, fill_opacity=.82, checkerboard_colors=[violet, cyan], stroke_color=cyan, stroke_opacity=.16)
        base = Circle(radius=2.15, color=cyan, stroke_opacity=.45, stroke_width=3).move_to(DOWN*.15)
        rings = VGroup(*[Circle(radius=r, color=orange, stroke_width=2, stroke_opacity=.7).move_to(DOWN*.15) for r in [.45, .9, 1.35, 1.8, 2.15]])

        self.set_camera_orientation(phi=62*DEGREES, theta=-48*DEGREES, zoom=.82)
        self.play(Create(axes), FadeIn(surface, scale=.82), run_time=1.3)
        self.begin_ambient_camera_rotation(rate=.10)
        self.wait(1.4)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(surface), FadeOut(axes), FadeOut(subtitle), FadeOut(squared), run_time=.55)
        self.move_camera(phi=0, theta=-90*DEGREES, zoom=1.0, run_time=.7)

        polar_title = Text("POLAR COORDINATES", font_size=32, color=white, weight="BOLD").move_to(UP*1.9)
        polar = MathTex(r"x^2+y^2=r^2,\qquad dx\,dy=r\,dr\,d\theta", font_size=38, color=cyan).move_to(UP*.95)
        self.play(FadeIn(polar_title), Write(polar), Create(base), LaggedStart(*[Create(r) for r in rings], lag_ratio=.13), run_time=1.2)
        arc = Arc(radius=2.15, start_angle=0, angle=TAU, color=orange, stroke_width=9).move_to(DOWN*.15)
        circumference = MathTex(r"\text{around each ring: }2\pi", font_size=30, color=orange).move_to(DOWN*3.0)
        self.play(Create(arc), FadeIn(circumference), run_time=.7)

        self.play(FadeOut(VGroup(base, rings, arc, circumference, polar_title, polar)), run_time=.45)
        derivation = VGroup(
            MathTex(r"I^2=2\pi\int_0^\infty r e^{-r^2}\,dr", font_size=42, color=white),
            MathTex(r"=\pi", font_size=50, color=orange),
            MathTex(r"\boxed{\displaystyle \int_{-\infty}^{\infty}e^{-x^2}\,dx=\sqrt{\pi}}", font_size=43, color=cyan),
        ).arrange(DOWN, buff=.45).move_to(DOWN*.25)
        self.play(Write(derivation[0]), run_time=.75)
        self.play(Write(derivation[1]), run_time=.45)
        self.play(Write(derivation[2]), run_time=.85)
        note = Text("The \u03c0 comes from circular symmetry.", font_size=22, color=muted).next_to(derivation, DOWN, buff=.48)
        self.play(FadeIn(note), run_time=.35)
        self.wait(1.1)
        self.play(FadeOut(VGroup(title, derivation, note)), run_time=.5)
