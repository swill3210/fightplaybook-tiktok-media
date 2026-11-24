"""Hero textured from the turnaround sheet ITSELF (Sean 2026-11-24: match the original art, not a simplified cartoon).
Each sheet view (front, right, left, back) gets a planar projection UV map onto the sheet image; every vertex blends
the views that really see it (BVH visibility, weight = facing^4), so the original muscle contours, layered shading,
red accents, wrist straps and finger lines are carried over. Sheet background is inpainted outward from the figure so
edges never pick up blue; the sheet eyes are painted out (decal eyes from hero_hy stay).
Run: python3 hero_tex.py IN.glb OUTDIR
"""
import sys, os, math
import numpy as np
import cv2
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hero_hy as HY
import hero_model as HM
import compare_ref as CR

SCRATCH = os.environ.get("HERO_TEX_DIR", "/tmp/claude-0/hero_tex"); os.makedirs(SCRATCH, exist_ok=True)


def prepared_sheet():
    """sheet with each panel's background inpainted from the figure, eyes painted with the face colour"""
    img = cv2.imread(CR.REF)  # BGR
    out = img.copy(); boxes = {}
    for n, (x0, y0, x1, y1) in CR.BOXES.items():
        crop = img[y0:y1, x0:x1]; g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY).astype(int)
        bg = np.abs(g - g[2, 2]) <= 60
        ys, xs = np.nonzero(~bg); bb = (xs.min(), ys.min(), xs.max(), ys.max()); boxes[n] = bb
        b, gch, r = (crop[..., i].astype(int) for i in range(3))
        eye = (np.minimum(np.minimum(r, gch), b) > 200) & (np.abs(b - r) < 14)
        eye[bb[1] + int(0.15 * (bb[3] - bb[1])):] = False; eye[:bb[1] + 3] = False
        bgmask = (bg | eye).astype(np.uint8) * 255
        bgmask = cv2.dilate(bgmask, np.ones((3, 3), np.uint8))  # also drop the light halo next to the outline
        fill = cv2.inpaint(crop, bgmask, 9, cv2.INPAINT_TELEA)
        out[y0:y1, x0:x1] = fill
    path = os.path.join(SCRATCH, "sheet_filled.png"); cv2.imwrite(path, out)
    return path, boxes, img.shape[1], img.shape[0]


def project(ob, boxes, W, H):
    me = ob.data
    vs = np.array([v.co[:] for v in me.vertices]); ns = np.array([v.normal[:] for v in me.vertices])
    tree = BVHTree.FromObject(ob, bpy.context.evaluated_depsgraph_get())
    wts = np.zeros((len(vs), 4))
    for k, (n, d) in enumerate(HY.VIEWS.items()):
        x0, y0, _, _ = CR.BOXES[n]; bx0, by0, bx1, by1 = boxes[n]
        r = (-d).cross(Vector((0, 0, 1))); u = vs @ np.array(r[:]); uc = (u.min() + u.max()) / 2
        sc = (by1 - by0) / 2.0
        X = x0 + (bx0 + bx1) / 2 + (u - uc) * sc; Y = y0 + by1 - vs[:, 2] * sc
        uv = me.uv_layers.new(name=n)
        loops_v = np.zeros(len(me.loops), int); me.loops.foreach_get("vertex_index", loops_v)
        co = np.stack([X / W, 1 - Y / H], 1)[loops_v]
        uv.data.foreach_set("uv", co.ravel())
        facing = np.clip(ns @ np.array(d[:]), 0, 1) ** 12  # t1: ^4 ghosted red stripes where views overlap
        dv = Vector(d[:])
        vis = np.array([0.0 if f < 1e-3 else (1.0 if tree.ray_cast(Vector(p) + dv * 2e-3, dv)[0] is None else 0.0)
                        for p, f in zip(vs, facing)])
        wts[:, k] = facing * vis
    s = wts.sum(1, keepdims=True); none = s[:, 0] < 1e-6
    wts[none] = np.clip(ns[none] @ np.array([d[:] for d in HY.VIEWS.values()]).T, 0, 1) ** 4  # occluded everywhere
    wts /= np.maximum(wts.sum(1, keepdims=True), 1e-6)
    att = me.color_attributes.new("vw", "FLOAT_COLOR", "POINT")
    att.data.foreach_set("color", wts.astype(np.float32).ravel())
    print("verts", len(vs), "unseen", int(none.sum()))


def material(img_path):
    m = bpy.data.materials.new("sheet"); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links; n.clear()
    out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission")
    img = bpy.data.images.load(img_path); img.colorspace_settings.name = "sRGB"
    at = n.new("ShaderNodeAttribute"); at.attribute_name = "vw"; at.attribute_type = "GEOMETRY"
    sep = n.new("ShaderNodeSeparateColor"); l.new(at.outputs["Color"], sep.inputs[0])
    wnode = [sep.outputs[0], sep.outputs[1], sep.outputs[2], at.outputs["Alpha"]]
    acc = None
    for k, name in enumerate(HY.VIEWS):
        uvn = n.new("ShaderNodeUVMap"); uvn.uv_map = name
        tx = n.new("ShaderNodeTexImage"); tx.image = img; tx.interpolation = "Cubic"; tx.extension = "EXTEND"
        l.new(uvn.outputs[0], tx.inputs[0])
        mul = n.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs[0].default_value = 1
        l.new(tx.outputs["Color"], mul.inputs[6]); l.new(wnode[k], mul.inputs[7])
        if acc is None:
            acc = mul.outputs[2]
        else:
            add = n.new("ShaderNodeMix"); add.data_type = "RGBA"; add.blend_type = "ADD"; add.inputs[0].default_value = 1
            l.new(acc, add.inputs[6]); l.new(mul.outputs[2], add.inputs[7]); acc = add.outputs[2]
    l.new(acc, em.inputs["Color"]); l.new(em.outputs[0], out.inputs[0])
    return m


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    HM.reset(); s, cam = HM.scene(HM.C["bg"]); s.render.use_freestyle = False; s.cycles.samples = 8
    s.view_settings.view_transform = "Standard"
    ob = HY.load(src)
    path, boxes, W, H = prepared_sheet(); project(ob, boxes, W, H)
    ob.data.materials.clear(); ob.data.materials.append(material(path))
    root = bpy.data.objects.new("root", None); bpy.context.collection.objects.link(root); ob.parent = root
    for e in HY.eyes(ob): e.parent = root
    if "--no-ink" not in sys.argv:
        HY.outline(ob).parent = root
    cam.data.ortho_scale = 2.2; cam.location = (0, -8, 1.0); cam.rotation_euler = (math.pi / 2, 0, 0)
    for name, az in HM.VIEWS.items():
        root.rotation_euler.z = -math.radians(az); bpy.context.view_layer.update()
        s.render.filepath = os.path.join(out, f"body_{name}.png"); bpy.ops.render.render(write_still=True)
    print("done")
