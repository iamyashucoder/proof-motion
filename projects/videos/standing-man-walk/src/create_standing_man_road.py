"""Create a clean stylized 3D man standing naturally on a road."""
import bpy
from mathutils import Vector
from pathlib import Path

ROOT = Path(__file__).parent
PREVIEW = ROOT / "assets" / "standing_man_road_preview.png"


def mat(name, color, rough=.45):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    m.use_nodes = True
    principled = m.node_tree.nodes.get("Principled BSDF")
    principled.inputs["Base Color"].default_value = color
    principled.inputs["Roughness"].default_value = rough
    m.roughness = rough
    return m


def uv(name, location, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return obj


def cylinder_between(name, a, b, radius, material):
    a, b = Vector(a), Vector(b)
    middle = (a+b)/2
    direction = b-a
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=radius, depth=direction.length, location=middle)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    obj.data.materials.append(material)
    bevel = obj.modifiers.new("soft edges", "BEVEL")
    bevel.width, bevel.segments = .06, 3
    return obj


def cube(name, location, scale, material, bevel=.05):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    modifier = obj.modifiers.new("soft edges", "BEVEL")
    modifier.width, modifier.segments = bevel, 3
    return obj


def look_at(obj, target):
    obj.rotation_euler = (Vector(target)-obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

asphalt = mat("asphalt", (.025, .032, .045, 1), .72)
marking = mat("road paint", (.92, .80, .27, 1), .35)
skin = mat("skin", (.43, .20, .12, 1), .52)
hair = mat("hair", (.018, .012, .01, 1), .45)
shirt = mat("shirt", (.045, .34, .75, 1), .42)
trousers = mat("trousers", (.025, .04, .09, 1), .5)
shoes = mat("shoes", (.008, .01, .016, 1), .35)

# Road and center markings.
cube("road", (0, 0, -.12), (6.4, 16, .12), asphalt, .02)
for y in range(-13, 15, 5):
    cube("lane_mark", (0, y, .012), (.13, 1.25, .018), marking, .01)

# Natural, upright mannequin with slightly relaxed arms.
uv("torso", (0, 0, 4.35), (.73, .42, 1.05), shirt)
uv("neck", (0, 0, 5.45), (.19, .18, .28), skin)
uv("head", (0, 0, 5.95), (.49, .44, .58), skin)
uv("hair_cap", (0, -.015, 6.30), (.50, .45, .25), hair)

# Arms: shoulders, elbows, hands rest naturally beside the hips.
for side in (-1, 1):
    shoulder = (side*.68, 0, 4.96)
    elbow = (side*.86, .04, 4.06)
    wrist = (side*.72, .10, 3.40)
    cylinder_between("upper_arm", shoulder, elbow, .17, shirt)
    cylinder_between("forearm", elbow, wrist, .135, skin)
    uv("hand", (side*.70, .11, 3.25), (.16, .13, .24), skin)

# Legs: feet are planted flat, with a subtle asymmetrical stance.
hips = [(-.31, .03, 3.48), (.31, -.02, 3.48)]
knees = [(-.37, .08, 2.05), (.41, -.10, 2.06)]
ankles = [(-.43, .12, .67), (.50, -.14, .67)]
for hip, knee, ankle in zip(hips, knees, ankles):
    cylinder_between("thigh", hip, knee, .24, trousers)
    cylinder_between("shin", knee, ankle, .19, trousers)
for x, y in [(-.43, .25), (.50, -.02)]:
    cube("shoe", (x, y, .33), (.28, .48, .16), shoes, .12)

bpy.ops.object.camera_add(location=(9.4, -16.0, 7.0))
camera = bpy.context.object
camera.data.lens = 54
look_at(camera, (0, 0, 3.25))
bpy.context.scene.camera = camera

for loc, energy, color, size in [((-5, -8, 11), 1500, (.58, .76, 1), 6), ((7, -3, 7), 1000, (1, .45, .18), 5), ((0, 5, 10), 800, (.25, .45, 1), 4)]:
    bpy.ops.object.light_add(type="AREA", location=loc)
    light = bpy.context.object
    light.data.energy, light.data.color, light.data.shape, light.data.size = energy, color, "DISK", size
    look_at(light, (0, 0, 3))

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 1080, 1920
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(PREVIEW)
scene.world.color = (.006, .011, .025)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "standing_man_on_road.blend"))
bpy.ops.wm.obj_export(filepath=str(ROOT / "assets" / "standing_man_on_road.obj"))
bpy.ops.render.render(write_still=True)
