"""Generate a long modular hotel facade designed to look infinite in perspective."""

from pathlib import Path


vertices: list[tuple[float, float, float]] = []
faces: list[tuple[str, tuple[int, ...]]] = []


def box(name: str, material: str, x0: float, y0: float, z0: float, x1: float, y1: float, z1: float) -> None:
    base = len(vertices) + 1
    vertices.extend([
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1),
    ])
    for face in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
        faces.append((f"{name}|{material}", tuple(base + item for item in face)))


ROOMS = 64
ROOM_WIDTH = 1.25
LENGTH = ROOMS * ROOM_WIDTH

# Foundation, two-storey body, roofline and a deeply receding side wing.
box("foundation", "stone", -2, -0.35, 0, LENGTH + 2, 1.4, 0.35)
box("hotel_body", "wall", -1.5, 0.15, 0.35, LENGTH + 1.5, 1.25, 7.1)
box("roof_cornice", "trim", -2, -0.10, 7.05, LENGTH + 2, 1.50, 7.45)
box("side_wing", "wall_dark", LENGTH - 1.5, 1.0, 0.35, LENGTH + 2.5, 20, 7.1)

for room in range(ROOMS):
    x = room * ROOM_WIDTH
    # repeated stone pilasters make every room module distinct
    box(f"room_{room + 1:03d}_pillar", "trim", x, -0.16, 0.35, x + 0.10, 0.03, 7.05)
    # Ground-floor entrance, balcony, and glowing upper window.
    box(f"room_{room + 1:03d}_door", "door", x + 0.28, -0.18, 0.45, x + 0.97, 0.02, 2.55)
    box(f"room_{room + 1:03d}_door_light", "warm_light", x + 0.36, -0.19, 1.45, x + 0.89, -0.185, 2.36)
    box(f"room_{room + 1:03d}_balcony", "iron", x + 0.14, -0.52, 2.65, x + 1.10, 0.03, 2.82)
    box(f"room_{room + 1:03d}_upper_window", "warm_light", x + 0.27, -0.19, 3.38, x + 0.98, -0.185, 5.65)
    box(f"room_{room + 1:03d}_window_frame_left", "trim", x + 0.22, -0.22, 3.24, x + 0.29, -0.18, 5.80)
    box(f"room_{room + 1:03d}_window_frame_right", "trim", x + 0.97, -0.22, 3.24, x + 1.04, -0.18, 5.80)
    box(f"room_{room + 1:03d}_window_frame_mid", "trim", x + 0.60, -0.22, 3.24, x + 0.66, -0.18, 5.80)
    box(f"room_{room + 1:03d}_number", "gold", x + 0.46, -0.225, 2.72, x + 0.79, -0.20, 3.05)

# At the distant end, narrow repeated annexes continue the rhythm around the corner.
for room in range(18):
    y = 1.3 + room * 1.05
    box(f"distant_wing_{room + 1:03d}", "wall_dark", LENGTH - 1.45, y, 0.40, LENGTH + 1.5, y + 0.10, 6.90)
    box(f"distant_window_{room + 1:03d}", "warm_light", LENGTH - 1.52, y + 0.22, 3.45, LENGTH - 1.48, y + 0.78, 5.50)

asset_dir = Path(__file__).parent / "assets"
asset_dir.mkdir(exist_ok=True)
obj = asset_dir / "infinite_hotel.obj"
mtl = asset_dir / "infinite_hotel.mtl"
mtl.write_text("""newmtl wall
Kd 0.12 0.20 0.32
newmtl wall_dark
Kd 0.06 0.10 0.18
newmtl stone
Kd 0.18 0.22 0.28
newmtl trim
Kd 0.65 0.71 0.77
newmtl door
Kd 0.07 0.04 0.02
newmtl warm_light
Kd 1.00 0.55 0.12
Ke 1.00 0.35 0.04
newmtl iron
Kd 0.03 0.04 0.06
newmtl gold
Kd 0.75 0.48 0.08
""", encoding="utf-8")
with obj.open("w", encoding="utf-8") as handle:
    handle.write("# Infinite Hotel: 64 repeated rooms and a receding side wing\nmtllib infinite_hotel.mtl\n")
    for x, y, z in vertices:
        handle.write(f"v {x:.5f} {y:.5f} {z:.5f}\n")
    active = None
    for descriptor, face in faces:
        name, material = descriptor.split("|")
        if descriptor != active:
            handle.write(f"o {name}\nusemtl {material}\n")
            active = descriptor
        handle.write("f " + " ".join(map(str, face)) + "\n")
print(obj)
