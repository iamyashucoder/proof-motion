"""Generate a low-poly old-fashioned kerosene hurricane lantern as an OBJ."""

from math import cos, pi, sin
from pathlib import Path

verts: list[tuple[float, float, float]] = []
parts: list[tuple[str, tuple[int, ...]]] = []


def circle(radius: float, z: float, count: int = 20) -> list[int]:
    result = []
    for n in range(count):
        angle = 2 * pi * n / count
        verts.append((radius * cos(angle), radius * sin(angle), z))
        result.append(len(verts))
    return result


def frustum(name: str, lower: float, upper: float, z0: float, z1: float, caps: bool = True) -> None:
    bottom, top = circle(lower, z0), circle(upper, z1)
    if caps:
        parts.append((name, tuple(reversed(bottom))))
        parts.append((name, tuple(top)))
    for n in range(len(bottom)):
        nxt = (n + 1) % len(bottom)
        parts.append((name, (bottom[n], bottom[nxt], top[nxt], top[n])))


def tube(name: str, a: tuple[float, float, float], b: tuple[float, float, float], radius: float) -> None:
    dx, dy, dz = (b[i] - a[i] for i in range(3))
    size = (dx * dx + dy * dy + dz * dz) ** 0.5
    axis = (dx / size, dy / size, dz / size)
    ref = (0.0, 0.0, 1.0) if abs(axis[2]) < 0.8 else (0.0, 1.0, 0.0)
    u = (axis[1] * ref[2] - axis[2] * ref[1], axis[2] * ref[0] - axis[0] * ref[2], axis[0] * ref[1] - axis[1] * ref[0])
    size_u = sum(v * v for v in u) ** 0.5
    u = tuple(v / size_u for v in u)
    v = (axis[1] * u[2] - axis[2] * u[1], axis[2] * u[0] - axis[0] * u[2], axis[0] * u[1] - axis[1] * u[0])
    first, second = [], []
    for n in range(8):
        angle = 2 * pi * n / 8
        shift = tuple(radius * (cos(angle) * u[i] + sin(angle) * v[i]) for i in range(3))
        verts.append(tuple(a[i] + shift[i] for i in range(3))); first.append(len(verts))
        verts.append(tuple(b[i] + shift[i] for i in range(3))); second.append(len(verts))
    parts.append((name, tuple(reversed(first))))
    parts.append((name, tuple(second)))
    for n in range(8):
        nxt = (n + 1) % 8
        parts.append((name, (first[n], first[nxt], second[nxt], second[n])))


# Rounded oil reservoir and wick assembly.
frustum("brass_base", 0.62, 0.70, 0.00, 0.12)
frustum("brass_base", 0.70, 0.54, 0.12, 0.34)
frustum("burner", 0.29, 0.25, 0.34, 0.52)
frustum("wick_knob", 0.10, 0.10, 0.52, 0.60)

# Glass chimney, made open-ended so a transparent material can reveal the flame.
frustum("glass_chimney", 0.36, 0.25, 0.49, 1.32, caps=False)

# Ventilator dome and top ring.
frustum("top_vent", 0.42, 0.28, 1.31, 1.48)
frustum("top_cap", 0.28, 0.18, 1.48, 1.55)

# Four vertical guard rails around the chimney.
for n in range(4):
    angle = pi / 4 + n * pi / 2
    x, y = 0.46 * cos(angle), 0.46 * sin(angle)
    tube("wire_frame", (x, y, 0.28), (x, y, 1.42), 0.027)

# Curved carrying handle as segmented wire over the lantern.
handle_points = []
for n in range(13):
    angle = pi - pi * n / 12
    handle_points.append((0.0, 0.57 * cos(angle), 1.38 + 0.65 * sin(angle)))
for a, b in zip(handle_points, handle_points[1:]):
    tube("carrying_handle", a, b, 0.032)

# Small side adjustment knob.
tube("wick_adjuster", (0.52, 0.0, 0.43), (0.68, 0.0, 0.43), 0.06)

output = Path(__file__).parent / "assets" / "vintage_hurricane_lantern.obj"
with output.open("w", encoding="utf-8") as file:
    file.write("# Old-fashioned kerosene hurricane lantern\n")
    for x, y, z in verts:
        file.write(f"v {x:.6f} {y:.6f} {z:.6f}\n")
    current = ""
    for name, face in parts:
        if current != name:
            file.write(f"o {name}\n")
            current = name
        file.write("f " + " ".join(str(index) for index in face) + "\n")
print(output)
