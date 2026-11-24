"""Render any generated .glb with the hero turnaround cameras (flat clay + ink) for compare_ref.py.
Run: python3 render_glb.py IN.glb OUTDIR"""
import sys, os, math
import bpy
from mathutils import Vector
sys.path.insert(0, "/home/user/fightplaybook-tiktok-media/production/blender")
import hero_model as HM
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
HM.reset(); s, cam = HM.scene(HM.C["bg"]); s.render.use_freestyle = False
bpy.ops.import_scene.gltf(filepath=src)
obs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
root = bpy.data.objects.new("root", None); bpy.context.collection.objects.link(root)
for o in list(bpy.context.scene.objects):
    if o.parent is None and o is not root and o.type != "CAMERA": o.parent = root
keep_tex = "--tex" in sys.argv
if not keep_tex:
    m = HM.toon("clay", HM.C["skin"])
    for o in obs: o.data.materials.clear(); o.data.materials.append(m)
bpy.context.view_layer.update()
pts = [o.matrix_world @ v.co for o in obs for v in o.data.vertices]
lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
print("bbox", [round(x, 3) for x in lo], [round(x, 3) for x in hi])
up = max(range(3), key=lambda i: hi[i] - lo[i]); print("tallest axis", "xyz"[up])
c = (lo + hi) / 2; root.location = -c; bpy.context.view_layer.update()
H = hi[up] - lo[up]
cam.data.ortho_scale = H * 1.1; cam.location = (0, -8 * H, 0); cam.rotation_euler = (math.pi / 2, 0, 0)
s.cycles.samples = 8
for name, az in HM.VIEWS.items():
    root.rotation_euler.z = -math.radians(az); bpy.context.view_layer.update()
    s.render.filepath = os.path.join(out, f"body_{name}.png"); bpy.ops.render.render(write_still=True)
