"""Create a silent visual explanation of 1/2 + 1/4 + ... = 1."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

W, H, FPS, FRAMES = 576, 1024, 30, 360  # 12 seconds, vertical
ROOT = Path(__file__).parent
OUT = ROOT / "renders" / "infinite_geometric_series.mp4"
FRAME_DIR = Path("/private/tmp/infinite_series_frames")


def clamp(value):
    return max(0.0, min(1.0, value))


def mix(start, end, amount):
    return start + (end - start) * amount


def ease(value):
    value = clamp(value)
    return value * value * (3 - 2 * value)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def math_font(size):
    unicode_font = Path("/Library/Fonts/Arial Unicode.ttf")
    return ImageFont.truetype(unicode_font, size) if unicode_font.exists() else font(size)


TITLE = font(32, True)
LABEL = font(23, True)
EQUATION = font(29, True)
SMALL = font(18)
TINY = font(12, True)
MATH_LABEL = math_font(23)
MATH_SMALL = math_font(18)
MATH_TINY = math_font(12)
MATH_EQUATION = math_font(29)
COLORS = [(61, 176, 255), (112, 91, 255), (255, 104, 138), (255, 178, 54), (50, 211, 153), (123, 210, 255), (198, 133, 255)]


def fraction_label(denominator):
    common = {2: "½", 4: "¼", 8: "⅛"}
    if denominator in common:
        return common[denominator]
    subscripts = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return "¹⁄" + str(denominator).translate(subscripts)


def text_center(draw, y, value, selected_font, color):
    box = draw.textbbox((0, 0), value, font=selected_font)
    draw.text(((W - (box[2] - box[0])) / 2, y), value, font=selected_font, fill=color)


def frame(index):
    t = index / FPS
    bg = Image.new("RGBA", (W, H), (8, 11, 22, 255))
    d = ImageDraw.Draw(bg, "RGBA")
    # restrained star-like texture
    for x, y in ((48, 130), (510, 214), (81, 760), (505, 860), (140, 884), (455, 118)):
        d.ellipse((x, y, x+2, y+2), fill=(130, 159, 211, 75))

    # The camera follows the active remaining corner. Each alternating split
    # leaves the next unfilled rectangle nested toward the lower-right, so we
    # both pan and zoom into exactly the region being partitioned.
    camera_progress = ease((t - 1.1) / 6.6)
    zoom = mix(0.84, 3.35, camera_progress)
    size = 420 * zoom
    world_left, world_top, world_size = 78, 278, 420
    focus_x = mix(world_left + world_size / 2, world_left + world_size, camera_progress)
    focus_y = mix(world_top + world_size / 2, world_top + world_size, camera_progress)
    left = W / 2 - (focus_x - world_left) * zoom
    top = 500 - (focus_y - world_top) * zoom
    bottom = top + size
    # faint outer glow / unit-square field
    d.rounded_rectangle((left-8, top-8, left+size+8, bottom+8), radius=14, fill=(54, 94, 172, 16))
    d.rectangle((left, top, left+size, bottom), fill=(18, 25, 46, 255))

    # Each term gets a 0.72s reveal after a brief intro. The cut direction
    # alternates: vertical, horizontal, vertical, horizontal ...
    start = 1.0
    duration = .57
    terms = 12
    remaining = [float(left), float(top), float(left + size), float(bottom)]
    for n in range(terms):
        progress = ease((t - (start + n * duration)) / .38)
        x0, y0, x1, y1 = remaining
        vertical = n % 2 == 0
        if vertical:
            midpoint = (x0 + x1) / 2
            filled = (x0, y0, midpoint, y1)
            next_remaining = [midpoint, y0, x1, y1]
            animated = (x0, y0, mix(x0, midpoint, progress), y1)
        else:
            midpoint = (y0 + y1) / 2
            filled = (x0, y0, x1, midpoint)
            next_remaining = [x0, midpoint, x1, y1]
            animated = (x0, y0, x1, mix(y0, midpoint, progress))
        if progress > 0:
            color = COLORS[n % len(COLORS)]
            d.rectangle(animated, fill=(*color, 235))
            # Moving division line, perpendicular to the preceding cut.
            if vertical:
                d.line((animated[2], y0, animated[2], y1), fill=(235, 244, 255, 225), width=2)
            else:
                d.line((x0, animated[3], x1, animated[3]), fill=(235, 244, 255, 225), width=2)
            width, height = animated[2] - animated[0], animated[3] - animated[1]
            if progress > .63 and width > 20 and height > 18:
                label = fraction_label(2 ** (n + 1))
                label_font = MATH_LABEL if min(width, height) > 65 else (MATH_SMALL if min(width, height) > 38 else MATH_TINY)
                label_box = d.textbbox((0, 0), label, font=label_font)
                label_width = label_box[2] - label_box[0]
                if label_width < width - 5:
                    label_height = label_box[3] - label_box[1]
                    d.text((animated[0] + (width - label_width) / 2, animated[1] + (height - label_height) / 2), label, font=label_font, fill=(255, 255, 255, 245))
        remaining = next_remaining

    # Persistent square border makes the invariant explicit.
    d.rectangle((left, top, left+size, bottom), outline=(245, 248, 255, 255), width=4)
    text_center(d, 720, "The remaining space is always cut in half.", SMALL, (184, 201, 229, 255))

    # A term appears in the equation only once its corresponding coloured
    # partition is visibly established in the square (same 63% threshold as
    # the in-square label above).
    shown = sum(
        1 for n in range(terms)
        if ease((t - (start + n * duration)) / .38) > .63
    )
    pieces = [fraction_label(2 ** (i + 1)) for i in range(shown)]
    if shown <= 4:
        text_center(d, 786, " + ".join(pieces), MATH_EQUATION, (255, 255, 255, 255))
    else:
        # Continue the series in compact rows so every newly revealed
        # partition, including 1/32 onward, has a matching written term.
        text_center(d, 765, " + ".join(pieces[:4]), MATH_EQUATION, (255, 255, 255, 255))
        tail = pieces[4:]
        for row, begin in enumerate(range(0, len(tail), 3)):
            text = "+ " + " + ".join(tail[begin:begin + 3])
            if begin + 3 >= len(tail) and shown == terms:
                text += " + ... = 1"
            text_center(d, 802 + row * 27, text, MATH_SMALL, (215, 227, 251, 255))
    if t > 8.2:
        alpha = int(255 * ease((t - 8.2) / .7))
        text_center(d, 930, "Infinitely many smaller pieces — never beyond the whole.", SMALL, (120, 212, 255, alpha))
    # Keep the explanatory header readable as the camera follows the corner.
    d.rectangle((0, 64, W, 166), fill=(8, 11, 22, 225))
    text_center(d, 86, "THE INFINITE GEOMETRIC SERIES", TITLE, (238, 244, 255, 255))
    text_center(d, 127, "How infinitely many pieces add to one whole", SMALL, (151, 172, 205, 255))
    # subtle glow around colored regions
    glow = bg.filter(ImageFilter.GaussianBlur(11))
    return Image.alpha_composite(glow, bg).convert("RGB")


FRAME_DIR.mkdir(exist_ok=True)
for i in range(FRAMES):
    frame(i).save(FRAME_DIR / f"frame_{i:04d}.png")
OUT.parent.mkdir(exist_ok=True)
subprocess.run([
    "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(FRAME_DIR / "frame_%04d.png"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT),
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
