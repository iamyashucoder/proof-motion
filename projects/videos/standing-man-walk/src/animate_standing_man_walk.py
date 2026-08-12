"""Animate the standing-road mannequin in a rightward, planted-foot walk."""
import bpy
from pathlib import Path

ROOT = Path(__file__).parent
FRAMES = Path("/private/tmp/standing_man_walk_frames")

bpy.ops.wm.open_mainfile(filepath=str(ROOT / "standing_man_on_road.blend"))
scene = bpy.context.scene

person_prefixes = ("torso", "neck", "head", "hair_cap", "upper_arm", "forearm", "hand", "thigh", "shin", "shoe")
parts = [obj for obj in scene.objects if obj.name.startswith(person_prefixes)]

# A single root ensures the person genuinely travels to screen-right.
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
root = bpy.context.object
root.name = "walk_root"
for obj in parts:
    obj.parent = root
    obj.matrix_parent_inverse = root.matrix_world.inverted()

def get_pair(base):
    pair = sorted([obj for obj in parts if obj.name == base or obj.name.startswith(base + ".")], key=lambda o: o.name)
    return pair[:2]

left_thigh, right_thigh = get_pair("thigh")
left_shin, right_shin = get_pair("shin")
left_upper, right_upper = get_pair("upper_arm")
left_fore, right_fore = get_pair("forearm")

def key(obj, frame, y_rotation):
    obj.rotation_euler[1] = y_rotation
    obj.keyframe_insert(data_path="rotation_euler", index=1, frame=frame)

# Five compact walk cycles: legs alternate at contact poses, and arms counter-swing.
poses = [(1, .34), (9, .16), (16, 0), (24, -.16), (31, -.34), (39, -.16), (46, 0), (54, .16), (61, .34), (69, .16), (76, 0), (84, -.16), (91, -.34), (99, -.16), (106, 0), (114, .16), (121, .34), (129, .16), (136, 0), (144, -.16), (150, -.28)]
for frame, swing in poses:
    key(left_thigh, frame, swing)
    key(right_thigh, frame, -swing)
    # Lower legs fold forward slightly during the swing phase.
    key(left_shin, frame, -.55 * min(0, swing))
    key(right_shin, frame, -.55 * min(0, -swing))
    key(left_upper, frame, -.72 * swing)
    key(right_upper, frame, .72 * swing)
    key(left_fore, frame, -.28 * swing)
    key(right_fore, frame, .28 * swing)

for frame, x, z in [(1, -3.05, 0), (31, -1.85, .035), (61, -.65, 0), (91, .55, .035), (121, 1.75, 0), (150, 2.9, .02)]:
    root.location = (x, 0, z)
    root.keyframe_insert(data_path="location", frame=frame)

FRAMES.mkdir(parents=True, exist_ok=True)
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 720, 1280
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(FRAMES / "frame_")
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 150
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "standing_man_walk.blend"))
bpy.ops.render.render(animation=True)
