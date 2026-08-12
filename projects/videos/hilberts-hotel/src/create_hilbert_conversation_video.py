"""Animate a manager and customer discussing Hilbert's Hotel."""

from pathlib import Path
from math import cos, sin, pi
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

W, H, FPS, FRAMES = 576, 1024, 30, 630
ROOT = Path(__file__).parent
BACKGROUND = ROOT / "assets" / "infinite_hotel_preview.png"
OUT = ROOT / "renders" / "hilberts_hotel_manager_customer.mp4"
FRAME_DIR = Path("/private/tmp/hilbert_conversation_frames")


def clamp(value): return max(0.0, min(1.0, value))
def ease(value):
    value = clamp(value)
    return value * value * (3 - 2 * value)


def pick_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for item in candidates:
        if Path(item).exists(): return ImageFont.truetype(item, size)
    return ImageFont.load_default()


TITLE, DIALOGUE, ROLE, SMALL = pick_font(27, True), pick_font(22, True), pick_font(16, True), pick_font(17)
FRIEND_ONE, FRIEND_TWO, WHITE = (255, 139, 25, 255), (80, 211, 255, 255), (246, 249, 255, 255)


def draw_figure(draw, x, ground, color, walking):
    # Direct key poses from the supplied reference: contact, passing,
    # opposite contact, mirrored passing. No procedural knee oscillation.
    poses = [
        # hip, left knee, left foot, right knee, right foot, left hand, right hand
        ((0,-78), (-12,-45), (-28,-18), (12,-45), (28,-18), (-25,-88), (23,-90)),
        ((0,-78), (-28,-55), (-14,-44), (3,-45), (5,-18), (-22,-86), (13,-84)),
        ((0,-78), (12,-45), (28,-18), (-12,-45), (-28,-18), (25,-88), (-23,-90)),
        ((0,-78), (17,-47), (30,-18), (28,-55), (14,-44), (22,-86), (-13,-84)),
    ]
    phase = (walking * .58 * 4) % 4
    current, following = int(phase), (int(phase) + 1) % 4
    blend = phase - int(phase)
    blend = blend * blend * (3 - 2 * blend)
    def lerp(a, b): return a + (b-a) * blend
    def point(a, b): return (x + lerp(a[0], b[0]), ground + lerp(a[1], b[1]))
    hip, left_knee, left_foot, right_knee, right_foot, left_hand, right_hand = [
        point(poses[current][n], poses[following][n]) for n in range(7)
    ]
    shoulder = (x, hip[1] - 68)
    head_y = shoulder[1] - 29
    draw.ellipse((shoulder[0]-20, head_y-20, shoulder[0]+20, head_y+20), outline=color, width=6)
    draw.line((shoulder, hip), fill=color, width=7)
    left_elbow = ((shoulder[0] + left_hand[0]) / 2 - 4, shoulder[1] + 30)
    right_elbow = ((shoulder[0] + right_hand[0]) / 2 + 4, shoulder[1] + 30)
    draw.line((shoulder, left_elbow, left_hand), fill=color, width=6, joint="curve")
    draw.line((shoulder, right_elbow, right_hand), fill=color, width=6, joint="curve")
    draw.line((hip, left_knee, left_foot), fill=color, width=7, joint="curve")
    draw.line((hip, right_knee, right_foot), fill=color, width=7, joint="curve")
    draw.line((left_foot, (left_foot[0]+10, left_foot[1])), fill=color, width=5)
    draw.line((right_foot, (right_foot[0]+10, right_foot[1])), fill=color, width=5)


def bubble(draw, side, text, opacity):
    if opacity <= 0: return
    if side == "left":
        box = (20, 420, 343, 555); tip = [(145,555),(172,555),(158,584)]
    else:
        box = (233, 420, 556, 555); tip = [(395,555),(422,555),(408,584)]
    color = (11, 20, 39, int(235*opacity))
    border = FRIEND_ONE if side == "left" else FRIEND_TWO
    draw.rounded_rectangle(box, radius=18, fill=color, outline=(*border[:3], int(255*opacity)), width=3)
    draw.polygon(tip, fill=color)
    # Text wraps manually at meaningful line breaks.
    lines = text.split("\n")
    y = 440
    for line in lines:
        width = draw.textbbox((0,0), line, font=DIALOGUE)[2]
        x = (box[0]+box[2]-width)/2
        draw.text((x,y), line, font=DIALOGUE, fill=(*WHITE[:3], int(255*opacity)))
        y += 30


LINES = [
    (0.5, 3.0, "left", "Did you know about\nHilbert's Hotel?"),
    (3.2, 6.1, "right", "Yes. It has infinitely many rooms,\nand every room is occupied."),
    (6.3, 9.0, "left", "What if a new customer comes?\nWill they get a room?"),
    (9.2, 11.8, "right", "Let me think… Oh, yes—\nthere is a way."),
    (12.0, 13.6, "left", "What is it?"),
    (13.8, 17.4, "right", "Move every guest to the\nnext room: n → n + 1.\nRoom 1 becomes free."),
    (17.7, 20.2, "left", "Perfect—you got it, dude!"),
]


def render(index):
    t = index / FPS
    walk = clamp(t / 20.0)
    # Hotel preview fills the vertical frame with a darkened cinematic crop.
    base = Image.open(BACKGROUND).convert("RGB")
    base = base.resize((int(base.width * H / base.height), H))
    # The building scrolls past the friends at the same time as their walk
    # cycle runs, anchoring each step to the pavement instead of a static view.
    crop_left = (base.width - W) // 2 + int(220 * walk)
    base = base.crop((crop_left, 0, crop_left + W, H)).convert("RGBA")
    overlay = Image.new("RGBA", (W,H), (3,8,19,128))
    image = Image.alpha_composite(base, overlay)
    d = ImageDraw.Draw(image, "RGBA")
    # A physical poster is attached high on the hotel facade.
    d.rounded_rectangle((112, 82, 464, 180), radius=10, fill=(12, 23, 43, 240), outline=(220, 181, 82, 255), width=4)
    title = "HILBERT'S HOTEL"
    tw = d.textbbox((0,0), title, font=TITLE)[2]
    d.text(((W-tw)/2, 105), title, font=TITLE, fill=(255, 223, 139, 255))
    poster = "INFINITELY MANY ROOMS"
    pw = d.textbbox((0,0), poster, font=SMALL)[2]
    d.text(((W-pw)/2, 143), poster, font=SMALL, fill=WHITE)
    # The two friends walk together across the hotel forecourt.
    # They remain close enough to converse while travelling clearly across
    # the frame; their translated positions are much larger than the stride.
    friend_one_x = 110
    friend_two_x = 270
    d.ellipse((friend_one_x-63, 835, friend_one_x+63, 866), fill=(0, 0, 0, 72))
    d.ellipse((friend_two_x-63, 835, friend_two_x+63, 866), fill=(0, 0, 0, 72))
    d.line((0, 850, W, 850), fill=(180, 201, 233, 50), width=2)
    draw_figure(d, friend_one_x, 850, FRIEND_ONE, t)
    draw_figure(d, friend_two_x, 850, FRIEND_TWO, t+.4)
    d.text((friend_one_x-46, 870), "FRIEND 1", font=ROLE, fill=FRIEND_ONE)
    d.text((friend_two_x-46, 870), "FRIEND 2", font=ROLE, fill=FRIEND_TWO)
    for start, end, side, text in LINES:
        visible = ease((t-start)/.22) * (1-ease((t-end)/.22))
        bubble(d, side, text, visible)
    # final idea stays on screen
    if t > 18.0:
        alpha = int(255*ease((t-18)/.5))
        message = "In an infinite hotel, there is always room for one more."
        width = d.textbbox((0,0), message, font=SMALL)[2]
        d.text(((W-width)/2, 930), message, font=SMALL, fill=(194,231,255,alpha))
    return Image.alpha_composite(image.filter(ImageFilter.GaussianBlur(5)), image).convert("RGB")


FRAME_DIR.mkdir(exist_ok=True)
for frame in range(FRAMES): render(frame).save(FRAME_DIR / f"frame_{frame:04d}.png")
OUT.parent.mkdir(exist_ok=True)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(FRAME_DIR/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
