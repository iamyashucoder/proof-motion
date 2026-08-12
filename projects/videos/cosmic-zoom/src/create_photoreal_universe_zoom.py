"""Photoreal 2.5D, single-camera zoom using layered aerial and space imagery."""
import bpy
from pathlib import Path

ROOT = Path(__file__).parent
FRAMES = Path("/private/tmp/photoreal_universe_zoom_frames")
ASSETS = ROOT / "assets" / "cosmic_zoom"


def image_plane(name, path, z, height, transparent_space=False):
    image = bpy.data.images.load(str(path))
    aspect = image.size[0] / image.size[1]
    bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, z))
    plane = bpy.context.object
    plane.name = name
    plane.dimensions = (height * aspect, height, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    material = bpy.data.materials.new(name + " material")
    material.use_nodes = True
    nodes, links = material.node_tree.nodes, material.node_tree.links
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Linear"
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Strength"].default_value = 1.0
    output = nodes.get("Material Output")
    links.new(tex.outputs["Color"], emission.inputs["Color"])
    if transparent_space:
        luminance = nodes.new("ShaderNodeRGBToBW")
        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = .025
        ramp.color_ramp.elements[1].position = .12
        transparent = nodes.new("ShaderNodeBsdfTransparent")
        mix = nodes.new("ShaderNodeMixShader")
        links.new(tex.outputs["Color"], luminance.inputs["Color"])
        links.new(luminance.outputs["Val"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], mix.inputs[0])
        links.new(transparent.outputs[0], mix.inputs[1])
        links.new(emission.outputs[0], mix.inputs[2])
        links.new(mix.outputs[0], output.inputs["Surface"])
        material.surface_render_method = "DITHERED"
    else:
        links.new(emission.outputs["Emission"], output.inputs["Surface"])
    plane.data.materials.append(material)
    return plane


def key(obj, frame, z):
    obj.location = (0, 0, z)
    obj.keyframe_insert(data_path="location", frame=frame)


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

# Each layer is ten times farther and ten times larger.  As the camera rises,
# the current foreground naturally shrinks to reveal the next cosmic scale.
layers = [
    ("farmland", "01_farmland.png", 0, 42),
    ("Earth", "02_earth.png", -220, 420),
    ("Solar System", "03_solar_system_matched.png", -2200, 4200),
    ("Galaxy", "04_galaxy_matched.png", -22000, 42000),
    ("Multiverse", "05_multiverse_matched.png", -220000, 420000),
]
layer_planes = []
for index, (name, filename, z, h) in enumerate(layers):
    layer_planes.append(image_plane(name, ASSETS / filename, z, h, transparent_space=index > 0))

# The physical field is present only at the beginning, then dissolves naturally
# as the camera leaves the surface instead of remaining as a visible square.
field_plane = layer_planes[0]
field_plane.hide_render = False
field_plane.keyframe_insert(data_path="hide_render", frame=1)
field_plane.hide_render = False
field_plane.keyframe_insert(data_path="hide_render", frame=90)
field_plane.hide_render = True
field_plane.keyframe_insert(data_path="hide_render", frame=110)

bpy.ops.object.camera_add(location=(0, 0, 8))
camera = bpy.context.object
camera.data.lens = 50
camera.data.clip_end = 1000000
camera.rotation_euler = (0, 0, 0)
# Point straight down along -Z; no panning means every scale stays centred.
camera.rotation_euler = (0, 0, 0)
bpy.context.scene.camera = camera

# Smooth logarithmic lift; no cuts and no target drift.
for frame, height in [(1, 8), (105, 75), (205, 750), (305, 7500), (405, 75000), (500, 150000)]:
    key(camera, frame, height)

FRAMES.mkdir(parents=True, exist_ok=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 360, 640
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(FRAMES / "frame_")
scene.render.fps = 25
scene.frame_start, scene.frame_end = 1, 500
scene.world.color = (0, 0, 0)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "photoreal_universe_zoom.blend"))
bpy.ops.render.render(animation=True)
