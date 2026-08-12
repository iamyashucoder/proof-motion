from manim import *

config.frame_height = 14


class BaselProblemExplainer(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        white, cyan, violet, orange, muted = "#F4F7FF", "#63E6FF", "#9E7BFF", "#FFB654", "#AAB8D0"
        title = Text("THE BASEL PROBLEM", font_size=42, color=white, weight="BOLD").to_edge(UP, buff=.55)
        series = MathTex(r"1+\frac14+\frac19+\frac1{16}+\cdots\;=?", font_size=48, color=cyan).move_to(UP*1.5)
        subtitle = Text("Can a sum of squares hide a circle?", font_size=22, color=muted).next_to(series, DOWN, buff=.2)
        self.play(FadeIn(title), Write(series), FadeIn(subtitle), run_time=.85)
        self.wait(.45)
        self.play(FadeOut(series), FadeOut(subtitle), run_time=.35)

        heading = Text("SIMILAR TRIANGLES", font_size=30, color=white, weight="BOLD").move_to(UP*1.8)
        base = Polygon(LEFT*2.75+DOWN*2.5, RIGHT*2.75+DOWN*2.5, LEFT*2.75+UP*2.5, color=cyan, fill_color=cyan, fill_opacity=.12, stroke_width=4)
        triangles = VGroup()
        labels = VGroup()
        colors = [violet, cyan, orange, violet, cyan]
        for i, n in enumerate(range(1, 6)):
            s = 4.7 / n
            tri = Polygon(LEFT*2.35+DOWN*2.2, LEFT*2.35+s*RIGHT+DOWN*2.2, LEFT*2.35+UP*s+DOWN*2.2, color=colors[i], fill_color=colors[i], fill_opacity=.14, stroke_width=3)
            triangles.add(tri)
            lab = MathTex(fr"\frac1{{{n}^2}}", font_size=25, color=colors[i]).move_to(tri.get_center()+RIGHT*.35+DOWN*.15)
            labels.add(lab)
        self.play(FadeIn(heading), Create(base), run_time=.55)
        self.play(LaggedStart(*[Create(t) for t in triangles], lag_ratio=.16), LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=.16), run_time=1.4)
        area_note = Text("Scaling every side by 1/n scales area by 1/n².", font_size=21, color=muted).move_to(DOWN*4.25)
        self.play(FadeIn(area_note), run_time=.4)
        self.wait(.6)
        self.play(FadeOut(VGroup(heading, base, triangles, labels, area_note)), run_time=.45)

        unfold_title = Text("UNFOLDING THE POLYGON", font_size=30, color=white, weight="BOLD").move_to(UP*1.85)
        center = DOWN*.25
        polys = VGroup()
        for sides, color in [(6, violet), (12, cyan), (24, orange)]:
            poly = RegularPolygon(n=sides, radius=2.35, color=color, stroke_width=3, fill_opacity=0).move_to(center)
            polys.add(poly)
        circle = Circle(radius=2.35, color=white, stroke_width=4).move_to(center)
        radius_line = Line(center, center+RIGHT*2.35, color=orange, stroke_width=4)
        self.play(FadeIn(unfold_title), Create(polys[0]), run_time=.5)
        self.play(Transform(polys[0], polys[1]), run_time=.5)
        self.play(Transform(polys[0], polys[2]), run_time=.5)
        self.play(Transform(polys[0], circle), Create(radius_line), run_time=.6)
        pi_note = Text("More sides → the circle and its π-based geometry.", font_size=21, color=muted).move_to(DOWN*4.1)
        self.play(FadeIn(pi_note), run_time=.35)
        self.wait(.45)
        self.play(FadeOut(VGroup(unfold_title, polys, radius_line, pi_note)), run_time=.45)

        proof_title = Text("THE EXACT IDENTITY", font_size=30, color=white, weight="BOLD").move_to(UP*1.9)
        product = MathTex(r"\frac{\sin x}{x}=\prod_{n=1}^{\infty}\left(1-\frac{x^2}{n^2\pi^2}\right)", font_size=37, color=white).move_to(UP*.75)
        expansion = MathTex(r"\frac{\sin x}{x}=1-\frac{x^2}{6}+\cdots", font_size=42, color=cyan).move_to(DOWN*.25)
        compare = Text("Compare the coefficient of x².", font_size=22, color=muted).move_to(DOWN*1.25)
        result = MathTex(r"\boxed{\displaystyle \sum_{n=1}^{\infty}\frac1{n^2}=\frac{\pi^2}{6}}", font_size=49, color=orange).move_to(DOWN*2.65)
        self.play(FadeIn(proof_title), Write(product), run_time=.8)
        self.play(Write(expansion), FadeIn(compare), run_time=.7)
        self.play(Write(result), run_time=.85)
        self.wait(1.1)
        self.play(FadeOut(VGroup(title, proof_title, product, expansion, compare, result)), run_time=.5)
