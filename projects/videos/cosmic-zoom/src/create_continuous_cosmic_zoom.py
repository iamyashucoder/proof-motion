"""One uninterrupted 3D camera lift: farmland to a speculative multiverse."""
import bpy
from math import cos, sin, pi
from mathutils import Vector
from pathlib import Path
import random

ROOT = Path(__file__).parent
FRAMES = Path("/private/tmp/continuous_cosmic_zoom_frames")

def material(name, color, emission=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = color
    p.inputs["Roughness"].default_value = .5
    if emission:
        p.inputs["Emission Color"].default_value = color
        p.inputs["Emission Strength"].default_value = 2
    return m

def sphere(name, loc, radius, mat, segments=20):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=12, location=loc, radius=radius)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return o

def key(obj, frame, value):
    obj.location = value
    obj.keyframe_insert(data_path="location", frame=frame)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
random.seed(11)
blue = material("earth ocean", (.015, .12, .42, 1))
green = material("continents", (.05, .34, .11, 1))
gold = material("sun", (1, .26, .01, 1), True)
cyan = material("cosmic cyan", (.02, .55, 1, 1), True)
violet = material("cosmic violet", (.25, .04, .8, 1), True)
white = material("stars", (.7, .85, 1, 1), True)

# A field sits on a curved planet so rising the camera reveals Earth naturally.
earth = sphere("Earth", (0, 0, -30), 30, blue, 40)
for _ in range(24):
    a, b = random.uniform(0, 2*pi), random.uniform(.15, 1.1)
    r = 30.15
    p = (r*sin(b)*cos(a), r*sin(b)*sin(a), -30+r*cos(b))
    land = sphere("continent", p, random.uniform(1, 3), green, 12)
    land.scale.z = .22
bpy.ops.mesh.primitive_plane_add(size=13.5, location=(0, 0, .15))
field = bpy.context.object
field.name = "agricultural land"
fm = bpy.data.materials.new("farmland texture")
fm.use_nodes = True
nodes, links = fm.node_tree.nodes, fm.node_tree.links
tex = nodes.new("ShaderNodeTexImage")
tex.image = bpy.data.images.load(str(ROOT / "assets/cosmic_zoom/01_farmland.png"))
links.new(tex.outputs["Color"], nodes.get("Principled BSDF").inputs["Base Color"])
field.data.materials.append(fm)

# Wider scales coexist in the same world; only a travelling camera reveals them.
sun_center = Vector((250, 0, -100))
sphere("Sun", sun_center, 30, gold, 30)
for orbit, size, mat in [(95, 4, green), (145, 6, blue), (205, 8, violet), (290, 13, gold)]:
    sphere("planet", sun_center + Vector((orbit, 0, 0)), size, mat, 16)
    bpy.ops.mesh.primitive_torus_add(major_radius=orbit, minor_radius=.4, major_segments=48, minor_segments=8, location=sun_center)
    bpy.context.object.data.materials.append(cyan)

galaxy_center = Vector((900, 0, -500))
for arm in range(3):
    for i in range(42):
        r, a = 10+i*6, arm*2*pi/3+i*.38
        sphere("galaxy star", galaxy_center+Vector((r*cos(a), r*sin(a), random.uniform(-10,10))), random.uniform(1,3), cyan if i%3 else violet, 8)
sphere("galactic core", galaxy_center, 20, gold, 20)

multi_center = Vector((2700, 0, -1500))
for i in range(22):
    a, r = i*2.4, 160+(i%6)*90
    pos = multi_center+Vector((r*cos(a), r*sin(a), (i%5-2)*90))
    bubble = sphere("universe bubble", pos, 35+(i%4)*15, violet if i%2 else cyan, 16)
    w = bubble.modifiers.new("bubble shell", "WIREFRAME")
    w.thickness = 2
    sphere("bubble galaxy", pos, 7, gold if i%3 == 0 else cyan, 12)

for _ in range(220):
    sphere("distant star", (random.uniform(-1200,4200), random.uniform(-1600,1600), random.uniform(-1800,300)), random.uniform(.5,1.8), white, 8)

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0,0,0))
target = bpy.context.object
bpy.ops.object.camera_add(location=(0,0,8))
camera = bpy.context.object
camera.data.lens, camera.data.clip_end = 52, 20000
track = camera.constraints.new(type="TRACK_TO")
track.target, track.track_axis, track.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
bpy.context.scene.camera = camera
for frame, cam, aim in [(1,(0,0,8),(0,0,0)), (70,(0,-20,65),(0,0,-10)), (140,(120,-150,420),sun_center), (210,(520,-520,1250),galaxy_center), (300,(1850,-1350,3600),multi_center)]:
    key(camera, frame, cam)
    key(target, frame, aim)

bpy.ops.object.light_add(type="POINT", location=(0,0,40))
bpy.context.object.data.energy = 1500
bpy.ops.object.light_add(type="POINT", location=sun_center+Vector((0,0,60)))
bpy.context.object.data.energy = 3000

FRAMES.mkdir(parents=True, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 720, 1280
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(FRAMES / "frame_")
scene.render.fps, scene.frame_start, scene.frame_end = 30, 1, 300
scene.world.color = (.001,.002,.009)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "continuous_agriculture_to_multiverse.blend"))
bpy.ops.render.render(animation=True)
