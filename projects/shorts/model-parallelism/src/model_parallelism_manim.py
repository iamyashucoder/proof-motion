from manim import *

config.frame_height = 14.0


class ModelParallelismExplainer(Scene):
    def construct(self):
        self.camera.background_color = "#050914"
        cyan, purple, orange, soft, muted = "#5DE4FF", "#9B7BFF", "#FFB44D", "#F4F7FF", "#A9B7D0"

        def label(text, size=28, color=soft):
            return Text(text, font_size=size, color=color, weight="BOLD")

        title = label("MODEL PARALLELISM", 42).to_edge(UP, buff=.58)
        subtitle = Text("One neural network  •  multiple GPUs", font_size=21, color=muted).next_to(title, DOWN, buff=.16)
        self.play(FadeIn(title, shift=DOWN*.18), FadeIn(subtitle, shift=DOWN*.18), run_time=.8)

        # Input token stream
        tokens = RoundedRectangle(corner_radius=.16, width=2.65, height=.78, stroke_color=cyan, stroke_width=2, fill_color="#10243B", fill_opacity=.9)
        token_text = label("INPUT TOKENS", 22, cyan).move_to(tokens)
        token_group = VGroup(tokens, token_text).move_to(UP*4.45)
        self.play(FadeIn(token_group, scale=.93), run_time=.55)

        # Device cards, each holding half the model's layers.
        def device_card(title_text, layer_text, color, side):
            card = RoundedRectangle(corner_radius=.22, width=6.25, height=3.25, stroke_color=color, stroke_width=3, fill_color="#0B1528", fill_opacity=.98)
            heading = label(title_text, 29, color).move_to(card.get_top() + DOWN*.42)
            layers = VGroup(*[
                RoundedRectangle(corner_radius=.07, width=4.65, height=.35, stroke_color=color, stroke_width=1.2, fill_color=color, fill_opacity=.18)
                for _ in range(4)
            ]).arrange(DOWN, buff=.16).move_to(card.get_center() + DOWN*.27)
            layer_label = Text(layer_text, font_size=21, color=soft).move_to(card.get_center() + DOWN*1.12)
            return VGroup(card, heading, layers, layer_label).move_to(UP*side)

        gpu0 = device_card("GPU 0", "Transformer layers 1 – 12", cyan, 1.65)
        gpu1 = device_card("GPU 1", "Transformer layers 13 – 24", purple, -2.25)
        self.play(Create(gpu0[0]), FadeIn(gpu0[1:], shift=UP*.15), run_time=.75)
        self.play(Create(gpu1[0]), FadeIn(gpu1[1:], shift=UP*.15), run_time=.75)

        # Local work inside each device.
        local_caption = Text("Each GPU stores only part of the model", font_size=22, color=muted).move_to(DOWN*4.55)
        self.play(FadeIn(local_caption), run_time=.45)
        self.play(
            Indicate(gpu0[2], color=cyan, scale_factor=1.02),
            Indicate(gpu1[2], color=purple, scale_factor=1.02),
            run_time=1.2,
        )

        # Forward activation moves from input through both device partitions.
        first_arrow = Arrow(token_group.get_bottom(), gpu0[0].get_top(), color=cyan, buff=.15, stroke_width=4, max_tip_length_to_length_ratio=.12)
        bridge = Arrow(gpu0[0].get_bottom(), gpu1[0].get_top(), color=orange, buff=.18, stroke_width=5, max_tip_length_to_length_ratio=.1)
        self.play(GrowArrow(first_arrow), run_time=.5)
        activation = Dot(color=orange, radius=.12).move_to(token_group.get_bottom())
        self.add(activation)
        self.play(activation.animate.move_to(gpu0[0].get_center()), run_time=.7)
        forward = label("FORWARD PASS", 25, orange).move_to(DOWN*.12)
        transfer = Text("activations cross devices", font_size=19, color=muted).next_to(forward, DOWN, buff=.1)
        self.play(GrowArrow(bridge), FadeIn(forward), FadeIn(transfer), run_time=.55)
        self.play(activation.animate.move_to(gpu1[0].get_center()), run_time=.9)
        self.play(Flash(gpu1[0].get_center(), color=orange, flash_radius=.55, line_length=.16), run_time=.35)
        self.wait(.35)

        # Backward pass travels in the opposite direction.
        self.play(FadeOut(forward), FadeOut(transfer), run_time=.25)
        grad_arrow = Arrow(gpu1[0].get_top(), gpu0[0].get_bottom(), color="#7EF0B6", buff=.18, stroke_width=5, max_tip_length_to_length_ratio=.1)
        backward = label("BACKWARD PASS", 25, "#7EF0B6").move_to(DOWN*.12)
        grad_text = Text("gradients return across devices", font_size=19, color=muted).next_to(backward, DOWN, buff=.1)
        self.play(Transform(bridge, grad_arrow), FadeIn(backward), FadeIn(grad_text), run_time=.55)
        gradient = Dot(color="#7EF0B6", radius=.12).move_to(gpu1[0].get_center())
        self.add(gradient)
        self.play(gradient.animate.move_to(gpu0[0].get_center()), run_time=.95)
        self.play(Flash(gpu0[0].get_center(), color="#7EF0B6", flash_radius=.55, line_length=.16), run_time=.35)
        self.play(FadeOut(gradient), FadeOut(activation), FadeOut(first_arrow), FadeOut(bridge), FadeOut(backward), FadeOut(grad_text), FadeOut(local_caption), run_time=.45)

        takeaway_box = RoundedRectangle(corner_radius=.2, width=6.7, height=1.3, stroke_color=orange, stroke_width=2.4, fill_color="#1A1720", fill_opacity=.95).move_to(DOWN*4.45)
        takeaway = label("Fit models too large for one GPU", 27, soft).move_to(takeaway_box)
        self.play(FadeIn(takeaway_box, scale=.95), Write(takeaway), run_time=.75)
        self.wait(1.0)
