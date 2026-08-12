"""Build a real 3D geometric-series staircase: each new step is half-size."""
import bpy
from math import pi
from mathutils import Vector
from pathlib import Path

ROOT = Path(__file__).parent
FRAME_DIR = Path("/private/tmp/geometric_staircase_frames")


def material(name, color, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    m.metallic = metallic
    m.roughness = .28
    return m


def block(name, loc, scale, mat, bevel=.035):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    bevel_mod = obj.modifiers.new("soft edges", "BEVEL")
    bevel_mod.width, bevel_mod.segments = bevel, 3
    return obj


def look_at(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

dark = material("midnight", (.008, .014, .032, 1))
cyan = material("cyan steps", (.03, .56, .92, 1), .1)
violet = material("violet steps", (.38, .13, .86, 1), .1)
gold = material("gold terminal", (1.0, .48, .05, 1), .28)

# The first tread/rise is 4 units.  Each successive term is half as large:
# 4 + 2 + 1 + 1/2 + ... = 8, so infinitely many steps fit within 8 units.
first = 4.0
terms = 12
x_start, total_height = -4.0, 0.0
for index in range(terms):
    size = first / (2 ** index)
    total_height += size
    x = x_start + size / 2
    step_mat = cyan if index % 2 == 0 else violet
    block(f"step_{index + 1}", (x, 0, total_height / 2), (size / 2, 1.55, total_height / 2), step_mat)
    x_start += size

# Bright cap marks the finite destination the infinite series approaches.
block("limit_cap", (4.03, 0, 4.03), (.055, 1.63, .055), gold, .02)
block("ground", (0, 0, -.16), (7.5, 5.4, .16), dark, .02)

# Camera performs a compact 360-degree orbit around the converging corner.
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0.25, 0, 2.1))
rig = bpy.context.object
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(.25, 0, 2.1))
target = bpy.context.object
bpy.ops.object.camera_add(location=(0, -14.5, 6.6))
camera = bpy.context.object
camera.parent = rig
camera.data.lens = 44
track = camera.constraints.new(type="TRACK_TO")
track.target, track.track_axis, track.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
bpy.context.scene.camera = camera
rig.rotation_euler[2] = 0
rig.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
rig.rotation_euler[2] = 2*pi
rig.keyframe_insert(data_path="rotation_euler", index=2, frame=150)

for loc, energy, color, size in [((-6, -7, 12), 1300, (.2, .55, 1), 6), ((8, -1, 8), 1100, (1, .18, .75), 5), ((0, 6, 10), 900, (1, .56, .12), 5)]:
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.object
    light.data.energy, light.data.color, light.data.shape, light.data.size = energy, color, "DISK", size
    look_at(light, (.25, 0, 2))

scene = bpy.context.scene
FRAME_DIR.mkdir(parents=True, exist_ok=True)
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 720, 1280
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(FRAME_DIR / "frame_")
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 150
scene.world.color = (.003, .006, .016)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "geometric_infinite_staircase.blend"))
bpy.ops.wm.obj_export(filepath=str(ROOT / "assets" / "geometric_infinite_staircase.obj"), export_materials=True)
bpy.ops.render.render(animation=True)
