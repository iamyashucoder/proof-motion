"""A 360-degree forced-perspective Penrose staircase visual."""
import bpy
from math import pi, sin, cos
from mathutils import Vector
from pathlib import Path

ROOT = Path(__file__).parent
FRAMES = Path("/private/tmp/infinite_staircase_frames")
BLEND = ROOT / "infinite_staircase_3d.blend"


def mat(name, rgba, metallic=0.0):
    material = bpy.data.materials.new(name)
    material.diffuse_color = rgba
    material.metallic = metallic
    material.roughness = .32
    return material


def cube(name, location, scale, material, bevel=.05):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    modifier = obj.modifiers.new("soft edges", "BEVEL")
    modifier.width = bevel
    modifier.segments = 3
    return obj


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def label(text, location, size, material):
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.object
    obj.data.body = text
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.data.size = size
    obj.data.extrude = .012
    obj.data.bevel_depth = .006
    obj.data.materials.append(material)
    return obj


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

navy = mat("midnight", (0.008, .014, .035, 1))
cyan = mat("cyan steps", (.045, .52, .82, 1), .14)
violet = mat("violet steps", (.36, .16, .82, 1), .12)
gold = mat("gold rails", (1.0, .46, .06, 1), .38)
white = mat("white", (.9, .95, 1, 1))

# Four flights each rise by six steps.  Their final and initial landings only
# appear to meet from the opening camera angle; the orbit exposes the gap.
rise, count, length, width = .16, 6, 1.12, 1.42
directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]
starts = [(-3.35, 3.35), (3.35, 3.35), (3.35, -3.35), (-3.35, -3.35)]
for flight, ((dx, dy), (sx, sy)) in enumerate(zip(directions, starts)):
    color = cyan if flight % 2 == 0 else violet
    for step in range(count):
        h = .18 + rise * (flight * count + step)
        x = sx + dx * (step * length + length / 2)
        y = sy + dy * (step * length + length / 2)
        block = cube(f"flight_{flight}_step_{step}", (x, y, h / 2),
                     (length / 2 + .025, width / 2, h / 2), color)
        if dx == 0:
            block.rotation_euler[2] = pi / 2

    # Gold handrail tracks the direction of each ascending flight.
    rail_z = .68 + rise * (flight * count + count / 2)
    rail_x = sx + dx * (count * length / 2)
    rail_y = sy + dy * (count * length / 2)
    rail = cube(f"rail_{flight}", (rail_x, rail_y, rail_z),
                (count * length / 2, .045, .045), gold, .03)
    if dx == 0:
        rail.rotation_euler[2] = pi / 2

# Small floating landing markers make the non-closing loop legible during orbit.
# Floor and soft studio lighting.
cube("floor", (0, 0, -.12), (10, 10, .12), navy, .02)

bpy.ops.object.light_add(type="AREA", location=(2, -7, 13))
key = bpy.context.object
key.data.energy, key.data.shape, key.data.size = 1500, "DISK", 7
look_at(key, (0, 0, 5))
bpy.ops.object.light_add(type="AREA", location=(-8, 4, 7))
fill = bpy.context.object
fill.data.energy, fill.data.color, fill.data.size = 1100, (.15, .45, 1), 6
look_at(fill, (0, 0, 5))
bpy.ops.object.light_add(type="AREA", location=(7, 7, 8))
rim = bpy.context.object
rim.data.energy, rim.data.color, rim.data.size = 1000, (1, .18, .75), 5
look_at(rim, (0, 0, 6))

# The first half is the magic view; the remaining orbit exposes the impossible gap.
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 2.2))
rig = bpy.context.object
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 2.2))
target = bpy.context.object
bpy.ops.object.camera_add(location=(0, -18.5, 5.4))
camera = bpy.context.object
camera.parent = rig
camera.data.lens = 30
track = camera.constraints.new(type="TRACK_TO")
track.target = target
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
bpy.context.scene.camera = camera
rig.rotation_euler[2] = 0
rig.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
rig.rotation_euler[2] = 2*pi
rig.keyframe_insert(data_path="rotation_euler", index=2, frame=360)

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
scene.render.resolution_percentage = 100
FRAMES.mkdir(parents=True, exist_ok=True)
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(FRAMES / "frame_")
scene.render.fps = 30
scene.frame_start, scene.frame_end = 1, 150
scene.world.color = (.003, .007, .018)
bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
bpy.ops.render.render(animation=True)
