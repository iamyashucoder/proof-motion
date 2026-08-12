"""Centered, continuous farmland-to-cosmos zoom inspired by the supplied reference."""
import bpy
from math import cos, sin, pi
from mathutils import Vector
from pathlib import Path
import random

ROOT = Path(__file__).parent
FRAMES = Path("/private/tmp/reference_universe_zoom_frames")
random.seed(29)

def mat(name, color, glow=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = color
    p.inputs["Roughness"].default_value = .45
    if glow:
        p.inputs["Emission Color"].default_value = color
        p.inputs["Emission Strength"].default_value = glow
    return m

def sphere(name, pos, r, material, seg=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=12, location=pos, radius=r)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(material)
    return o

def key(obj, frame, loc):
    obj.location = loc
    obj.keyframe_insert(data_path="location", frame=frame)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
ocean = mat("Earth ocean", (.01, .08, .30, 1))
land = mat("land", (.03, .28, .08, 1))
cloud = mat("cloud", (.7, .84, 1, 1), .1)
star = mat("star", (.7, .88, 1, 1), 3)
cyan = mat("cyan glow", (.02, .42, 1, 1), 3)
violet = mat("violet glow", (.42, .05, 1, 1), 3)
gold = mat("gold glow", (1, .16, .01, 1), 4)

# FIELD -> EARTH.  The field is a texture on a tangent plane above the curved planet.
earth = sphere("Earth", (0, 0, -80), 80, ocean, 48)
for _ in range(48):
    a, b = random.uniform(0, 2*pi), random.uniform(0.05, 1.35)
    p = Vector((80.3*sin(b)*cos(a), 80.3*sin(b)*sin(a), -80+80.3*cos(b)))
    continent = sphere("continent", p, random.uniform(2, 8), land, 12)
    continent.scale.z = .15
for _ in range(35):
    a, b = random.uniform(0, 2*pi), random.uniform(0.05, 1.3)
    p = Vector((80.5*sin(b)*cos(a), 80.5*sin(b)*sin(a), -80+80.5*cos(b)))
    c = sphere("cloud", p, random.uniform(1, 5), cloud, 12)
    c.scale.z = .06
bpy.ops.mesh.primitive_plane_add(size=22, location=(0,0,.35))
field = bpy.context.object
field.name = "aerial agricultural land"
fm = bpy.data.materials.new("field texture")
fm.use_nodes = True
t = fm.node_tree.nodes.new("ShaderNodeTexImage")
t.image = bpy.data.images.load(str(ROOT / "assets/cosmic_zoom/01_farmland.png"))
fm.node_tree.links.new(t.outputs["Color"], fm.node_tree.nodes.get("Principled BSDF").inputs["Base Color"])
field.data.materials.append(fm)

# Deep starfield behind every later scale.
for _ in range(420):
    angle = random.uniform(0, 2*pi)
    radius = random.uniform(180, 3400)
    sphere("star", (radius*cos(angle), radius*sin(angle), random.uniform(-4200,-550)), random.uniform(.8, 4), star, 8)

# Centered spiral galaxy, visible as the camera reaches intergalactic scale.
galaxy = bpy.data.objects.new("galaxy_group", None)
bpy.context.collection.objects.link(galaxy)
for arm in range(4):
    for i in range(72):
        r, a = 30+i*11, arm*pi/2+i*.33
        s = sphere("galaxy", (r*cos(a), r*sin(a), -1800+random.uniform(-20,20)), random.uniform(2,7), cyan if i%3 else violet, 8)
        s.parent = galaxy
core = sphere("galaxy core", (0,0,-1800), 45, gold, 20)
core.parent = galaxy

# Final multiverse cluster stays exactly on the camera axis.
multi = bpy.data.objects.new("multiverse_group", None)
bpy.context.collection.objects.link(multi)
for i in range(35):
    a, r = i*2.4, 170+(i%7)*105
    pos = (r*cos(a), r*sin(a), -4700+(i%5-2)*80)
    bubble = sphere("universe bubble", pos, 35+(i%4)*18, violet if i%2 else cyan, 14)
    bubble.parent = multi
    wire = bubble.modifiers.new("bubble outline", "WIREFRAME")
    wire.thickness = 2.1
    inner = sphere("bubble core", pos, 7, gold if i%3 == 0 else cyan, 10)
    inner.parent = multi

# Radial star streaks expand from the centre as speed increases.
streaks = bpy.data.objects.new("warp_speed_streaks", None)
bpy.context.collection.objects.link(streaks)
for _ in range(110):
    a = random.uniform(0,2*pi)
    length, dist = random.uniform(70,300), random.uniform(60,700)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=random.uniform(.6,1.8), depth=length, location=(dist*cos(a), dist*sin(a), -900))
    line = bpy.context.object
    line.name = "star streak"
    line.rotation_euler = (0, pi/2, a)
    line.data.materials.append(star if random.random()>.25 else cyan)
    line.parent = streaks
streaks.scale = (.15,.15,.15)
streaks.keyframe_insert(data_path="scale", frame=205)
streaks.scale = (2.2,2.2,2.2)
streaks.keyframe_insert(data_path="scale", frame=310)
streaks.scale = (.35,.35,.35)
streaks.keyframe_insert(data_path="scale", frame=365)

bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0,0,-80))
target = bpy.context.object
bpy.ops.object.camera_add(location=(0,0,9))
camera = bpy.context.object
camera.data.lens, camera.data.clip_end = 50, 20000
constraint = camera.constraints.new(type="TRACK_TO")
constraint.target, constraint.track_axis, constraint.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
bpy.context.scene.camera = camera

# Entirely axial movement: every scale remains centred, never dies in a corner.
for frame, height, aim_z in [(1,9,0), (85,70,-45), (165,380,-150), (245,1100,-900), (340,2600,-1800), (450,5700,-4700), (500,7200,-4700)]:
    key(camera, frame, (0,0,height))
    key(target, frame, (0,0,aim_z))

bpy.ops.object.light_add(type="POINT", location=(0,0,100))
bpy.context.object.data.energy = 1700
bpy.ops.object.light_add(type="POINT", location=(0,0,-1700))
bpy.context.object.data.energy = 2500

FRAMES.mkdir(parents=True, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 360, 640
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(FRAMES / "frame_")
scene.render.fps, scene.frame_start, scene.frame_end = 25, 1, 500
scene.world.color = (.0005,.001,.006)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "reference_style_universe_zoom.blend"))
bpy.ops.render.render(animation=True)
