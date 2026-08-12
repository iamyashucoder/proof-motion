"""Create an original vertical wireframe-lantern animation."""

from math import cos, pi, sin
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import subprocess

W, H, FPS, FRAMES = 576, 1024, 24, 240
ROOT = Path(__file__).parent
FRAMES_DIR = Path("/private/tmp/lantern_animation_frames")
OUT = ROOT / "renders" / "lantern_vs_darkness.mp4"


def mix(a, b, t):
    return a + (b - a) * max(0, min(1, t))


def line(draw, points, fill, width=2):
    draw.line([(int(x), int(y)) for x, y in points], fill=fill, width=width, joint="curve")


def stick_figure(draw, x, ground, phase):
    orange = (255, 130, 18, 255)
    head_y = ground - 77
    draw.ellipse((x - 10, head_y - 10, x + 10, head_y + 10), outline=orange, width=4)
    line(draw, [(x, head_y + 10), (x + 2, ground - 38)], orange, 5)
    swing = sin(phase * 2 * pi) * 13
    line(draw, [(x + 1, ground - 62), (x - 19, ground - 45 + swing * .22)], orange, 4)
    line(draw, [(x + 1, ground - 62), (x + 20, ground - 47 - swing * .22)], orange, 4)
    line(draw, [(x + 2, ground - 38), (x - 16, ground - 6 + swing * .32)], orange, 5)
    line(draw, [(x + 2, ground - 38), (x + 19, ground - 6 - swing * .32)], orange, 5)


def lamp_nodes(cx, cy, scale):
    # Outline nodes for a hurricane lantern, top to bottom.
    points = []
    for y, r in ((-150, 30), (-120, 78), (-86, 92), (-58, 72), (50, 70), (78, 112), (122, 104), (148, 80)):
        for n in range(8):
            angle = 2 * pi * n / 8
            points.append((cx + r * scale * cos(angle), cy + y * scale + r * .11 * scale * sin(angle)))
    # Side rails and arch points.
    points += [(cx - 112 * scale, cy + y * scale) for y in (-78, -10, 70, 130)]
    points += [(cx + 112 * scale, cy + y * scale) for y in (-78, -10, 70, 130)]
    points += [(cx + 118 * scale * cos(a), cy - 168 * scale + 115 * scale * sin(a)) for a in (pi, 2.45, 1.9, 1.25, .7, 0)]
    return points


def lantern_outline(draw, cx, cy, scale, opacity, glow):
    white = (230, 240, 255, int(255 * opacity))
    warm = (255, 154, 35, int(255 * opacity))
    def e(bounds, color, width=2):
        draw.ellipse(tuple(int(v) for v in bounds), outline=color, width=width)
    # reservoir, glass chamber, vented roof, and handle.
    e((cx - 92*scale, cy + 76*scale, cx + 92*scale, cy + 150*scale), white, 3)
    e((cx - 76*scale, cy + 42*scale, cx + 76*scale, cy + 105*scale), white, 2)
    e((cx - 60*scale, cy - 75*scale, cx + 60*scale, cy + 75*scale), white, 3)
    e((cx - 73*scale, cy - 120*scale, cx + 73*scale, cy - 70*scale), white, 3)
    e((cx - 55*scale, cy - 150*scale, cx + 55*scale, cy - 116*scale), white, 3)
    draw.arc((int(cx - 125*scale), int(cy - 230*scale), int(cx + 125*scale), int(cy + 15*scale)), 180, 360, fill=white, width=3)
    for sx in (-1, 1):
        line(draw, [(cx + sx*95*scale, cy - 85*scale), (cx + sx*110*scale, cy + 78*scale), (cx + sx*76*scale, cy + 140*scale)], white, 3)
    # Glowing flame is the visual payoff.
    if glow:
        flame = [(cx, cy + 44*scale), (cx - 13*scale, cy + 17*scale), (cx - 3*scale, cy - 12*scale), (cx + 12*scale, cy + 20*scale)]
        draw.polygon([(int(x), int(y)) for x, y in flame], fill=warm)


def render(frame):
    t = frame / (FRAMES - 1)
    image = Image.new("RGBA", (W, H), (1, 2, 5, 255))
    drawing = ImageDraw.Draw(image, "RGBA")
    ground = 720
    line(drawing, [(0, ground), (W, ground)], (180, 195, 220, 190), 2)
    # The figure enters, pauses, then powers the lantern outline into existence.
    figure_x = mix(55, 190, min(t / .35, 1))
    if t < .67:
        stick_figure(drawing, figure_x, ground, t * 5)
    cx, cy = 367, 608
    build = max(0, min(1, (t - .23) / .42))
    nodes = lamp_nodes(cx, cy, 1.0)
    edges = []
    for i in range(0, 64, 8):
        for j in range(8):
            edges.append((i+j, i+(j+1) % 8))
            if i < 56: edges.append((i+j, i+8+j))
            if j % 2 == 0 and i < 48: edges.append((i+j, i+16+(j+3) % 8))
    for n, (a, b) in enumerate(edges):
        if n / len(edges) < build:
            line(drawing, [nodes[a], nodes[b]], (225, 235, 255, 185), 1)
    for n, point in enumerate(nodes):
        if n / len(nodes) < build:
            x, y = point
            drawing.ellipse((x-2, y-2, x+2, y+2), fill=(255, 255, 255, 230))
    finished = max(0, min(1, (t - .60) / .22))
    if finished:
        lantern_outline(drawing, cx, cy, 1, finished, True)
        # Soft orange illumination on the ground.
        drawing.ellipse((cx-120, ground-12, cx+120, ground+13), fill=(255, 112, 18, int(90*finished)))
    # bloom overlay for the active construction and flame.
    bloom = image.filter(ImageFilter.GaussianBlur(8))
    return Image.alpha_composite(bloom, image).convert("RGB")


FRAMES_DIR.mkdir(exist_ok=True)
for index in range(FRAMES):
    render(index).save(FRAMES_DIR / f"frame_{index:04d}.png")
OUT.parent.mkdir(exist_ok=True)
subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(FRAMES_DIR / "frame_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT),
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
