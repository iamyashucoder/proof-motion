import bpy
import math
from pathlib import Path

ROOT = Path(__file__).parent


def clean_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        pass


def material(name, color, metallic=0.0, roughness=0.45):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def add_cube(name, location, scale, mat, bevel=0.0, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("Soft body edges", "BEVEL")
        mod.width = bevel
        mod.segments = 4
    obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    return obj


def add_cylinder(name, location, radius, depth, mat, rotation=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    if parent:
        obj.parent = parent
    bevel = obj.modifiers.new("Tire edge", "BEVEL")
    bevel.width = .06
    bevel.segments = 3
    return obj


clean_scene()

red = material("Deep metallic red", (0.38, 0.012, 0.018), metallic=.78, roughness=.23)
dark = material("Tire rubber", (0.006, 0.008, 0.012), metallic=.05, roughness=.32)
rim = material("Brushed alloy", (0.32, 0.37, 0.43), metallic=.9, roughness=.2)
glass = material("Smoky glass", (0.015, 0.05, 0.075), metallic=.2, roughness=.08)
road_mat = material("Asphalt", (0.018, 0.022, 0.028), metallic=.0, roughness=.76)
line_mat = material("Warm lane paint", (0.95, 0.74, 0.18), metallic=.0, roughness=.38)
grass_mat = material("Roadside grass", (0.015, 0.07, 0.032), roughness=.9)
lamp_mat = material("Lamp metal", (0.06, 0.08, 0.1), metallic=.8, roughness=.25)
headlight_mat = material("Headlight", (1.0, .73, .34), metallic=.1, roughness=.15)

# World and environment
world = bpy.context.scene.world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.008, 0.016, 0.045, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = .22

add_cube("Road", (0, 20, -.18), (5.6, 65, .16), road_mat, bevel=.12)
add_cube("Left grass", (-16, 20, -.31), (10.4, 65, .12), grass_mat)
add_cube("Right grass", (16, 20, -.31), (10.4, 65, .12), grass_mat)

for y in range(-35, 85, 8):
    add_cube("Center lane", (0, y, .015), (.13, 2.25, .025), line_mat, bevel=.04)
    for side in (-1, 1):
        post = add_cylinder("Roadside post", (side*5.15, y+2.5, .55), .06, 1.1, lamp_mat)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=.18, location=(side*5.15, y+2.5, 1.16))
        bulb = bpy.context.object
        bulb.data.materials.append(headlight_mat)

# Car rig
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, -18, 0))
car = bpy.context.object
car.name = "Driving car rig"

body = add_cube("Car body", (0, 0, 1.08), (1.52, 2.75, .48), red, bevel=.25, parent=car)
hood = add_cube("Hood", (0, 1.42, 1.45), (1.38, .95, .16), red, bevel=.15, parent=car)
cabin = add_cube("Cabin", (0, -.38, 1.72), (1.23, 1.28, .52), glass, bevel=.18, parent=car)
front_bumper = add_cube("Front bumper", (0, 2.72, .82), (1.47, .13, .17), dark, bevel=.08, parent=car)

for x in (-1.58, 1.58):
    for y in (-1.7, 1.7):
        # A wheel rig fixes its local Z axis along the car's axle.  The tire
        # then spins around that local axis instead of pitching/skidding.
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=(x, y, .58), rotation=(0, math.pi/2, 0))
        axle = bpy.context.object
        axle.name = "Wheel axle"
        axle.parent = car
        if x > 0 and y > 0:
            removable_wheel = axle
        wheel = add_cylinder("Wheel", (0, 0, 0), .56, .34, dark, parent=axle)
        wheel.location = (0, 0, 0)
        wheel.rotation_euler = (0, 0, 0)
        wheel.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        wheel.rotation_euler[2] = -42
        wheel.keyframe_insert(data_path="rotation_euler", index=2, frame=240)
        wheel_rim = add_cylinder("Rim", (0, 0, 0), .33, .355, rim, parent=axle)
        wheel_rim.location = (0, 0, 0)
        wheel_rim.rotation_euler = (0, 0, 0)
        wheel_rim.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
        wheel_rim.rotation_euler[2] = -42
        wheel_rim.keyframe_insert(data_path="rotation_euler", index=2, frame=240)
        # Five bright spokes give the rolling motion a visible reference.
        for spoke_index in range(5):
            spoke = add_cube("Wheel spoke", (0, 0, 0), (.055, .30, .035), rim, bevel=.018, parent=wheel)
            spoke.location = (0, .16, .20)
            spoke.rotation_euler = (0, 0, spoke_index * (2*math.pi/5))

for x in (-1.02, 1.02):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=.19, location=(x, 2.7, 1.2))
    light = bpy.context.object
    light.scale = (1.0, .45, .6)
    light.data.materials.append(headlight_mat)
    light.parent = car

# Side-view tyre-removal physics shot: the car remains stationary while the
# near-side front wheel detaches, clears the axle, and rolls forward.
car.location = (0, 0, 0)
car.keyframe_insert(data_path="location", frame=1)
car.keyframe_insert(data_path="location", frame=180)
removable_wheel.location = (1.58, 1.7, .58)
removable_wheel.keyframe_insert(data_path="location", frame=1)
removable_wheel.keyframe_insert(data_path="location", frame=68)
removable_wheel.location = (3.15, 1.7, .58)
removable_wheel.keyframe_insert(data_path="location", frame=94)
removable_wheel.location = (3.15, 8.4, .58)
removable_wheel.keyframe_insert(data_path="location", frame=180)

# Following camera: it moves with the car while the roadside sweeps by.
bpy.ops.object.empty_add(type="PLAIN_AXES", location=(1.0, 3.4, .85))
focus = bpy.context.object
focus.parent = car
focus.location = (0, .35, .9)
focus.keyframe_insert(data_path="location", frame=1)
focus.keyframe_insert(data_path="location", frame=70)
focus.location = (1.0, 4.2, .85)
focus.keyframe_insert(data_path="location", frame=180)

bpy.ops.object.camera_add(location=(17.0, -3.0, 3.4))
camera = bpy.context.object
camera.data.lens = 42
camera.data.dof.use_dof = True
camera.data.dof.focus_object = focus
camera.data.dof.aperture_fstop = 4.5
camera.parent = car
track = camera.constraints.new(type="TRACK_TO")
track.target = focus
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
bpy.context.scene.camera = camera

# Lighting
bpy.ops.object.light_add(type="AREA", location=(3.5, -3.0, 9))
key = bpy.context.object
key.data.energy = 1250
key.data.shape = "DISK"
key.data.size = 7
key.data.color = (0.43, 0.62, 1.0)
key.parent = car

bpy.ops.object.light_add(type="AREA", location=(-5, -1, 3.5))
fill = bpy.context.object
fill.data.energy = 750
fill.data.size = 5
fill.data.color = (1.0, .15, .08)
fill.parent = car

bpy.ops.object.light_add(type="SUN", location=(0, 0, 20))
sun = bpy.context.object
sun.rotation_euler = (math.radians(35), math.radians(-20), math.radians(25))
sun.data.energy = 1.2
sun.data.color = (0.7, .78, 1.0)

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(ROOT.parent / "renders" / "tire_removal_frames" / "tire_")
scene.render.fps = 30
scene.frame_start = 1
scene.frame_end = 180
scene.render.image_settings.color_mode = "RGBA"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.film_transparent = False

for obj in scene.objects:
    if obj.type == "MESH":
        obj.select_set(True)

bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "car_driving_3d.blend"))
bpy.ops.render.render(animation=True)
