import bpy
import math
from mathutils import Matrix
from pathlib import Path

TAU = math.tau
ROOT = Path(__file__).parent

def reset():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

def make_mat(name, color, metal=0.0, rough=.4, emit=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1)
        b.inputs["Emission Strength"].default_value = 2.2
    return m

def cyl(name, r, d, material, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=r, depth=d, rotation=(math.pi/2, 0, 0))
    o = bpy.context.object; o.name = name; o.data.materials.append(material)
    if parent:
        o.parent = parent
        o.matrix_parent_inverse = Matrix.Identity(4)
    bevel = o.modifiers.new("Bevel", "BEVEL"); bevel.width=.035; bevel.segments=3
    return o

def wheel(name, r, n, pos, wood, metal, dark):
    rig = bpy.data.objects.new(name, None); bpy.context.collection.objects.link(rig); rig.location=pos
    cyl("Wooden rim", r, .18, wood, rig)
    cyl("Dark hollow", r*.82, .20, dark, rig)
    cyl("Inner wood ring", r*.30, .22, wood, rig)
    cyl("Metal hub", r*.12, .27, metal, rig)
    for i in range(n):
        a = TAU*i/n
        bpy.ops.mesh.primitive_cube_add(location=(math.cos(a)*r*.53, 0, math.sin(a)*r*.53))
        s = bpy.context.object; s.name="Metal spoke"; s.data.materials.append(metal)
        s.dimensions=(r*.60,.10,.08); s.rotation_euler=(0,-a,0); bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); s.parent=rig; s.matrix_parent_inverse=Matrix.Identity(4)
    return rig

reset()
wood = make_mat("Walnut wood", (.34,.11,.035), .05, .23)
metal = make_mat("Brushed metal", (.42,.46,.52), .88, .19)
dark = make_mat("Hub black", (.006,.008,.012), .7, .23)
grid = make_mat("Dim grid", (.025,.03,.04), .1, .65)
cyan = make_mat("Cyan track", (.02,.72,.94), emit=True)
green = make_mat("Green track", (.04,.9,.32), emit=True)
black = make_mat("Black", (.002,.003,.006), 0, 1)

bpy.ops.mesh.primitive_plane_add(size=30, location=(0,1,0), rotation=(math.pi/2,0,0))
bpy.context.object.data.materials.append(black)
for x in range(-8,9):
    bpy.ops.mesh.primitive_cube_add(location=(x*.85,.94,0)); o=bpy.context.object; o.dimensions=(.012,.02,12); o.data.materials.append(grid)
for z in range(-7,8):
    bpy.ops.mesh.primitive_cube_add(location=(0,.94,z*.85)); o=bpy.context.object; o.dimensions=(14,.02,.012); o.data.materials.append(grid)

big = wheel("Big wheel", 1.05, 9, (0,0,.55), wood, metal, dark)
small = wheel("Small wheel", .52, 8, (0,0,-2.05), wood, metal, dark)
nested_big = wheel("Nested big", 1.24, 9, (-1.65,0,.25), wood, metal, dark)
nested_small = wheel("Nested small", .59, 8, (-1.65,0,.25), wood, metal, dark)

tracks=[]
for z, material in ((-1.55,cyan),(-2.38,green)):
    bpy.ops.mesh.primitive_cube_add(location=(0,0,z)); o=bpy.context.object; o.name="Distance track"; o.dimensions=(4.8,.07,.055); o.data.materials.append(material); tracks.append(o)

for o in (big,small):
    o.hide_render=False; o.keyframe_insert("hide_render", frame=1); o.hide_render=True; o.keyframe_insert("hide_render", frame=75)
for o in (nested_big,nested_small,*tracks):
    o.hide_render=True; o.keyframe_insert("hide_render", frame=1); o.hide_render=False; o.keyframe_insert("hide_render", frame=75)
for o in (nested_big,nested_small):
    o.location=(-1.65,0,.25); o.keyframe_insert("location", frame=75); o.rotation_euler=(0,0,0); o.keyframe_insert("rotation_euler", frame=75)
    o.location=(1.65,0,.25); o.keyframe_insert("location", frame=180); o.rotation_euler=(0,-TAU,0); o.keyframe_insert("rotation_euler", frame=180)

bpy.ops.object.camera_add(location=(0,-15,.15), rotation=(math.pi/2,0,0))
cam=bpy.context.object; cam.data.type="ORTHO"; cam.data.ortho_scale=8.4; bpy.context.scene.camera=cam
bpy.ops.object.light_add(type="AREA", location=(-3,-4,6)); bpy.context.object.data.energy=900; bpy.context.object.data.size=6
bpy.ops.object.light_add(type="AREA", location=(4,-3,2)); bpy.context.object.data.energy=500; bpy.context.object.data.color=(.3,.55,1); bpy.context.object.data.size=5

scene=bpy.context.scene; scene.render.engine="BLENDER_EEVEE"; scene.render.resolution_x=720; scene.render.resolution_y=1280; scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"; scene.render.filepath=str(ROOT.parent / "renders" / "aristotle_blender_frames" / "frame_"); scene.render.fps=30; scene.frame_start=40; scene.frame_end=40
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "aristotles_wheel_blender.blend"))
bpy.ops.render.render(animation=True)
