"""Create a silent animated explanation of Hilbert's Hotel."""

from math import sin, pi
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

W, H, FPS, FRAMES = 576, 1024, 30, 480
ROOT = Path(__file__).parent
OUT = ROOT / "renders" / "hilberts_hotel_shift_to_infinity.mp4"
FRAME_DIR = Path("/private/tmp/hilberts_hotel_frames")


def clamp(x): return max(0.0, min(1.0, x))
def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)
def mix(a, b, x): return a + (b - a) * x


def pick_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for item in candidates:
        if Path(item).exists(): return ImageFont.truetype(item, size)
    return ImageFont.load_default()


TITLE, CAPTION, SMALL, NUMBER = pick_font(31, True), pick_font(24, True), pick_font(17), pick_font(18, True)
WHITE, MUTED, ORANGE, CYAN, GREEN = (242, 247, 255, 255), (164, 183, 214, 255), (255, 132, 26, 255), (93, 201, 255, 255), (85, 223, 167, 255)


def centered(draw, y, txt, active_font, fill):
    box = draw.textbbox((0, 0), txt, font=active_font)
    draw.text(((W - (box[2]-box[0]))/2, y), txt, font=active_font, fill=fill)


def stick(draw, x, y, scale=1, pose=0, color=ORANGE):
    def L(points, width=4):
        draw.line([(int(a), int(b)) for a,b in points], fill=color, width=max(1, int(width*scale)), joint="curve")
    r = 10*scale
    draw.ellipse((x-r, y-70*scale-r, x+r, y-70*scale+r), outline=color, width=max(1,int(4*scale)))
    shoulder = (x, y-58*scale); hip = (x, y-30*scale)
    L([shoulder, hip], 5)
    wave = sin(pose*2*pi)*12*scale
    L([shoulder, (x+28*scale, y-54*scale+wave)], 4)
    L([shoulder, (x-25*scale, y-44*scale)], 4)
    L([hip, (x-18*scale, y)], 5); L([hip, (x+18*scale, y)], 5)


def hotel(draw, y, phase, mapping="normal"):
    """Draw six rooms plus a vanishing continuation, including occupants."""
    x0, room_w, room_h = 48, 70, 112
    draw.rounded_rectangle((26, y-38, 550, y+room_h+28), radius=16, fill=(19, 31, 55, 255), outline=(120, 158, 212, 180), width=2)
    for i in range(7):
        x = x0 + i*room_w
        draw.rounded_rectangle((x, y, x+room_w-8, y+room_h), radius=5, fill=(35, 56, 91, 255), outline=(177, 203, 244, 180), width=2)
        label = i+1
        occupant = True
        if mapping == "one_shift":
            # Original guest i ends up in i+1; room 1 becomes empty.
            occupant = label != 1
        elif mapping == "infinite_shift":
            # Current guests take even rooms; odds are available.
            occupant = label % 2 == 0
        if occupant:
            cx, cy = x + (room_w-8)/2, y+56
            draw.ellipse((cx-7, cy-20, cx+7, cy-6), outline=CYAN, width=2)
            draw.line((cx,cy-6,cx,cy+15), fill=CYAN, width=2)
            draw.line((cx-8,cy+2,cx+8,cy+2), fill=CYAN, width=2)
        else:
            draw.text((x+23, y+43), "OPEN", font=SMALL, fill=GREEN)
        draw.text((x+23, y+89), str(label), font=NUMBER, fill=WHITE)
    draw.text((534, y+42), "…", font=TITLE, fill=WHITE)
    # During a shift, glowing arrows show how occupants move.
    if phase > 0:
        alpha = int(255*phase)
        if mapping == "one_shift":
            for i in range(5):
                sx, ex = x0+i*room_w+31, x0+(i+1)*room_w+31
                draw.line((sx,y-12,ex,y-12), fill=(255,185,84,alpha), width=3)
                draw.polygon([(ex,y-12),(ex-8,y-17),(ex-8,y-7)], fill=(255,185,84,alpha))
        elif mapping == "infinite_shift":
            for i in range(3):
                sx, ex = x0+i*room_w+31, x0+(2*i+1)*room_w+31
                draw.line((sx,y-12,ex,y-12), fill=(255,185,84,alpha), width=3)
                draw.polygon([(ex,y-12),(ex-8,y-17),(ex-8,y-7)], fill=(255,185,84,alpha))


def render(i):
    t = i/FPS
    image = Image.new("RGBA", (W,H), (5,8,17,255))
    d = ImageDraw.Draw(image, "RGBA")
    # title bar remains readable above hotel movement
    d.rectangle((0, 55, W, 155), fill=(5,8,17,240))
    centered(d, 76, "HILBERT'S HOTEL", TITLE, WHITE)
    centered(d, 116, "A hotel with infinitely many rooms", SMALL, MUTED)
    hotel_y = 275

    if t < 3:
        hotel(d, hotel_y, 0, "normal")
        caption = "Every room is occupied. The hotel is full."
        stick(d, 100, 682, 1.15, t, ORANGE)
    elif t < 8:
        shift = ease((t-3)/1.6)
        hotel(d, hotel_y, shift, "one_shift" if shift > .65 else "normal")
        if t < 4.6:
            caption = "One new guest arrives. Where can they stay?"
            stick(d, 105, 682, 1.15, t, ORANGE)
            stick(d, 450, 682, .85, t, GREEN)
        else:
            caption = "Move every guest: room n  →  room n + 1"
            stick(d, 105, 682, 1.15, t, ORANGE)
            d.rounded_rectangle((190, 628, 445, 676), radius=10, fill=(255,132,26,25), outline=(255,132,26,150), width=2)
            centered(d, 639, "n → n + 1", CAPTION, WHITE)
        if t > 6.1:
            d.rounded_rectangle((56, 480, 191, 526), radius=9, fill=(85,223,167,35), outline=GREEN, width=2)
            d.text((72,491), "Room 1 is free!", font=SMALL, fill=GREEN)
    else:
        shift = ease((t-8)/1.4)
        hotel(d, hotel_y, shift, "infinite_shift" if shift > .65 else "normal")
        caption = "Even infinitely many new guests can fit."
        stick(d, 100, 682, 1.15, t, ORANGE)
        if t > 9.5:
            d.rounded_rectangle((176, 628, 459, 676), radius=10, fill=(255,132,26,25), outline=(255,132,26,150), width=2)
            centered(d, 639, "n → 2n", CAPTION, WHITE)
            centered(d, 704, "All odd-numbered rooms are now open.", SMALL, GREEN)
    centered(d, 770, caption, CAPTION, WHITE)
    centered(d, 824, "Infinity is not a very large number — it behaves differently.", SMALL, MUTED)
    return Image.alpha_composite(image.filter(ImageFilter.GaussianBlur(7)), image).convert("RGB")


FRAME_DIR.mkdir(exist_ok=True)
for i in range(FRAMES): render(i).save(FRAME_DIR / f"frame_{i:04d}.png")
OUT.parent.mkdir(exist_ok=True)
subprocess.run(["ffmpeg","-y","-framerate",str(FPS),"-i",str(FRAME_DIR/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(OUT)
