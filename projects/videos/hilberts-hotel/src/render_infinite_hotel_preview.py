"""Headless Blender preview render for the infinite hotel OBJ."""

import bpy
from mathutils import Vector
from pathlib import Path


ROOT = Path(__file__).parent
ASSET = ROOT / "assets" / "infinite_hotel.obj"
OUTPUT = ROOT / "assets" / "infinite_hotel_preview.png"


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
bpy.ops.wm.obj_import(filepath=str(ASSET))

# Gentle bevels help the repeated modules read clearly in a product-style preview.
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        bevel = obj.modifiers.new("soft_edges", "BEVEL")
        bevel.width = 0.018
        bevel.segments = 2

# Ground plane and a perspective camera looking along the endless facade.
bpy.ops.mesh.primitive_plane_add(size=240, location=(35, -3, 0))
ground = bpy.context.object
ground.data.materials.append(bpy.data.materials.new("ground"))
ground.data.materials[0].diffuse_color = (0.015, 0.022, 0.04, 1)

bpy.ops.object.camera_add(location=(-13, -23, 9.5))
camera = bpy.context.object
look_at(camera, (28, 0.15, 3.4))
camera.data.lens = 46
bpy.context.scene.camera = camera

bpy.ops.object.light_add(type="AREA", location=(-4, -10, 15))
key = bpy.context.object
key.data.energy = 1400
key.data.shape = "RECTANGLE"
key.data.size = 10
look_at(key, (15, 0, 3))

bpy.ops.object.light_add(type="AREA", location=(42, -2, 10))
fill = bpy.context.object
fill.data.energy = 950
fill.data.color = (0.25, 0.48, 1.0)
fill.data.size = 14
look_at(fill, (38, 0, 3))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(OUTPUT)
scene.world.color = (0.004, 0.008, 0.018)
scene.render.film_transparent = False
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "assets" / "infinite_hotel_preview.blend"))
bpy.ops.render.render(write_still=True)
print(OUTPUT)
