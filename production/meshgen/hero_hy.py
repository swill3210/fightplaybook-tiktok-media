"""Hero from the Hunyuan3D-2mv mesh (Sean 2026-11-24: use existing tools, stop hand sculpting).
Colours come from the turnaround sheet itself: every face takes the class (skin, black, navy, red, white) voted
in the sheet view that really sees it (BVH occlusion test), then gets a 2 tone cel material from the sheet palette.
Run: python3 hero_hy.py IN.glb OUTDIR [--save-blend PATH]
"""
import sys, os, math
import numpy as np
import bpy, bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from PIL import Image
sys.path.insert(0, "/home/user/fightplaybook-tiktok-media/production/blender")
import hero_model as HM
import compare_ref as CR

SKIN, BLACK, NAVY, RED, WHITE, GLOVE = range(6)
NAMES = ["skin", "black", "navy", "red", "white", "glove"]
# (shadow, base) sampled from main_character_reference.jpg
PAL = {SKIN: ("#36363C", "#48484E"), BLACK: ("#0C0C0F", "#1C1C21"), NAVY: ("#121833", "#1E2647"),
       RED: ("#9A1418", "#E0262B"), WHITE: ("#FFFFFF", "#FFFFFF"), GLOVE: ("#09090B", "#202024")}
KEY = Vector((-0.25, -0.85, 0.55)).normalized()
VIEWS = {"front": Vector((0, -1, 0)), "right": Vector((-1, 0, 0)), "left": Vector((1, 0, 0)), "back": Vector((0, 1, 0))}


def classify(px):
    """px: (...,3) uint8 -> class per pixel, -1 for background"""
    r, g, b = (px[..., i].astype(int) for i in range(3))
    lum = (r + g + b) / 3
    cls = np.full(r.shape, SKIN)
    cls[lum < 42] = BLACK
    cls[(b - r > 18) & (lum < 120)] = NAVY
    cls[(r > 110) & (r - g > 60)] = RED
    cls[(r > 200) & (g > 200) & (b > 200) & (b - r < 12)] = WHITE
    cls[(r > 180) & (b - r >= 12)] = -1  # sheet background
    return cls


def sheet_views():
    ref = Image.open(CR.REF).convert("RGB"); out = {}
    for n, (x0, y0, x1, y1) in CR.BOXES.items():
        crop = ref.crop((x0, y0, x1, y1)); g = crop.convert("L"); bg = g.getpixel((2, 2))
        bb = g.point(lambda p: 255 if abs(p - bg) > 60 else 0).getbbox()
        out[n] = (classify(np.asarray(crop)), bb)
    return out


def load(src):
    bpy.ops.import_scene.gltf(filepath=src)
    ob = [o for o in bpy.context.scene.objects if o.type == "MESH"][0]
    mw = ob.matrix_world.copy(); ob.parent = None; ob.matrix_world = mw
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for o in list(bpy.context.scene.objects):
        if o.type == "EMPTY": bpy.data.objects.remove(o)
    vs = np.array([v.co[:] for v in ob.data.vertices])
    lo, hi = vs.min(0), vs.max(0); s = 2.0 / (hi[2] - lo[2])
    vs = (vs - [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]]) * s
    ob.data.vertices.foreach_set("co", vs.ravel()); ob.data.update()
    for p in ob.data.polygons: p.use_smooth = True
    return ob


def paint(ob, win=4):
    me = ob.data; views = sheet_views()
    bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
    tree = BVHTree.FromBMesh(bm)
    vs = np.array([v.co[:] for v in me.vertices])
    cls = np.full(len(bm.faces), -1)
    frame = {}
    for n, d in VIEWS.items():  # mesh silhouette frame per view, matched to the sheet figure by height and centre
        r = (-d).cross(Vector((0, 0, 1)))
        u = vs @ np.array(r[:]); frame[n] = (r, (u.min() + u.max()) / 2)
    for f in bm.faces:
        c = f.calc_center_median(); nrm = f.normal; best = None
        for n, d in VIEWS.items():
            k = nrm.dot(d)
            if k < 0.2 or (best and k <= best[0]):
                continue
            hit = tree.ray_cast(c + d * 1e-3, d)
            if hit[0] is None:  # nothing between the face and that camera
                best = (k, n)
        if not best:
            continue
        n = best[1]; grid, (bx0, by0, bx1, by1) = views[n]; r, uc = frame[n]
        sc = (by1 - by0) / 2.0
        X = int((bx0 + bx1) / 2 + (c.dot(r) - uc) * sc); Y = int(by1 - c.z * sc)
        w = grid[max(0, Y - win):Y + win + 1, max(0, X - win):X + win + 1].ravel(); w = w[w >= 0]
        if len(w):
            cls[f.index] = np.bincount(w, minlength=5).argmax()
    for _ in range(6):  # unseen faces take the majority of their neighbours; isolated specks are removed
        new = cls.copy()
        for f in bm.faces:
            nb = [cls[g.index] for e in f.edges for g in e.link_faces if g is not f]
            nb = [x for x in nb if x >= 0]
            if nb and (cls[f.index] < 0 or nb.count(cls[f.index]) == 0):
                new[f.index] = max(set(nb), key=nb.count)
        cls = new
    cls[cls < 0] = SKIN
    cls = zone_fix(bm, cls)
    bm.free()
    me.materials.clear()
    for k in range(6):
        me.materials.append(cel(NAMES[k], PAL[k]))
    me.polygons.foreach_set("material_index", cls.astype(np.int32))
    me.update()
    print("class counts", {NAMES[k]: int((cls == k).sum()) for k in range(6)})


TORSO = [(0.9, 0.265), (1.0, 0.245), (1.1, 0.215), (1.2, 0.185), (1.3, 0.165), (1.4, 0.2)]  # measured half widths


def zone_fix(bm, cls):
    """body zone rules (h1: sheet ink and muscle lines turned skin black, highlights turned white):
    arms and legs skin, hands gloves (+ red strap), torso shirt black (+ red), shorts navy (+ red), head skin.
    Eyes are decals, never projected."""
    zt = np.array([z for z, _ in TORSO]); wt = np.array([w for _, w in TORSO])
    for f in bm.faces:
        c = f.calc_center_median(); x, z = abs(c.x), c.z; k = cls[f.index]
        arm = 0.82 < z < 1.4 and x > np.interp(z, zt, wt)  # h2: below the fists the outer legs counted as arms
        if z > 1.74:  # h10: z>1.64 also swallowed the traps
            k = SKIN                                        # head and neck
        elif arm and z < 1.03:
            k = RED if k == RED and z > 0.97 else GLOVE     # fists, red strap at the wrist
        elif arm:
            k = SKIN
        elif z < 0.74:
            k = SKIN                                        # legs (mesh and sheet shorts hem at z 0.74, h2)
        elif z < 0.97:
            k = k if k in (NAVY, RED) else NAVY             # shorts
        elif z < 1.4:
            k = k if k in (BLACK, RED, NAVY) else BLACK     # shirt (waistband may be navy)
        else:  # tank top above the chest (reference): covers the traps to a round neckline, armhole curves round the deltoid
            hole = 0.25 - max(0.0, z - 1.5) * 0.4          # h9: straight x and z cuts left boxy corners
            neck = 0.088 + max(0.0, 1.62 - z) * 0.6         # round neckline flaring into the collar
            yoke = 1.665 - (x - 0.10) * 0.55                # top of the shoulder from the collar out to the armhole
            front = c.y < 0
            collar = (1.6 if front else 1.66) + 0.07 * (x / 0.12) ** 2   # round crew neck, higher at the back (h11 was square)
            if z > 1.74 or (x < 0.12 and z > collar):
                k = SKIN                                    # head and neck
            elif x > hole:
                k = SKIN                                    # bare deltoid
            elif abs(z - yoke) < 0.016 and x > neck:
                k = RED                                     # red raglan yoke over the shoulder
            else:
                k = BLACK
        cls[f.index] = k
    return cls


# eye layout measured on the sheet's front view, relative to the head box (h4: projecting sheet blobs was fragile)
EYE = {"x": 0.19, "down": 0.54, "w": 0.2, "h": 0.058, "slant": -20}  # h5: +20 tilted the inner ends up (sad); reference dips them


def head_box(ob):
    vs = np.array([v.co[:] for v in ob.data.vertices]); top = vs[:, 2].max()
    zs = np.arange(top - 0.4, top - 0.1, 0.005)
    widths = [np.ptp(vs[np.abs(vs[:, 2] - z) < 0.004, 0]) for z in zs]
    chin = zs[int(np.argmin(widths))]  # narrowest neck slice under the head
    band = vs[(vs[:, 2] > chin + 0.4 * (top - chin)) & (vs[:, 2] < top - 0.05)]
    return top, chin, np.ptp(band[:, 0])


def eyes(ob, white="#FFFFFF"):
    top, chin, W = head_box(ob); H = top - chin
    tree = BVHTree.FromObject(ob, bpy.context.evaluated_depsgraph_get())
    mat = cel("eye_white", (white, white)); obs = []
    w, h = EYE["w"] * W, EYE["h"] * H; cz = top - EYE["down"] * H
    for sgn in (-1, 1):
        cx = sgn * EYE["x"] * W
        hit = tree.ray_cast(Vector((cx, -2, cz)), Vector((0, 1, 0)))
        if hit[0] is None:
            print("eye miss", cx, cz); continue
        me = bpy.data.meshes.new("eye"); bm = bmesh.new(); n = 40; ctr = bm.verts.new((0, 0, 0)); rings = []
        for rr in (0.25, 0.5, 0.75, 1.0):
            ring = []
            for i in range(n):
                t = 2 * math.pi * i / n; x = w / 2 * math.cos(t)
                z = h * math.sin(t) * (1 - (2 * x / w) ** 2) ** 0.8 * (1.0 if t < math.pi else 0.6)
                ring.append(bm.verts.new((x * rr, 0, z * rr)))
            rings.append(ring)
        for i in range(n):
            j = (i + 1) % n; bm.faces.new((ctr, rings[0][i], rings[0][j]))
            for r in range(3):
                bm.faces.new((rings[r][i], rings[r + 1][i], rings[r + 1][j], rings[r][j]))
        bm.to_mesh(me); bm.free()
        e = bpy.data.objects.new("eye", me); bpy.context.collection.objects.link(e); me.materials.append(mat)
        e.location = hit[0] + Vector((0, -0.02, 0))
        e.rotation_euler = (0, math.radians(EYE["slant"]) * sgn, 0)  # inner ends lower (toward the centre)
        sw = e.modifiers.new("hug", "SHRINKWRAP"); sw.target = ob; sw.wrap_method = "PROJECT"
        sw.use_project_y = True; sw.use_negative_direction = True; sw.use_positive_direction = True; sw.offset = 0.003  # crisp edge, no z-fight
        obs.append(e)
    print("head top", round(top, 3), "chin", round(chin, 3), "width", round(W, 3), "eye z", round(cz, 3))
    return obs


def cel(name, tones, th=0.32):
    sh, base = (HM.HEX(t) for t in tones)
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links; n.clear()
    out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission")
    geo = n.new("ShaderNodeNewGeometry"); dot = n.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = KEY; l.new(geo.outputs["Normal"], dot.inputs[0])
    band = n.new("ShaderNodeValToRGB"); band.color_ramp.interpolation = "CONSTANT"; e = band.color_ramp.elements
    e[0].color = sh; e[1].position = th; e[1].color = base; l.new(dot.outputs["Value"], band.inputs["Fac"])
    l.new(band.outputs["Color"], em.inputs["Color"]); l.new(em.outputs[0], out.inputs[0])
    return m


def outline(ob, thick=0.007):
    ink = bpy.data.materials.new("ink"); ink.use_nodes = True; nt = ink.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.004, 0.004, 0.005, 1)
    geo = nt.nodes.new("ShaderNodeNewGeometry"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Backfacing"], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], o.inputs[0])
    hull = ob.copy(); hull.data = ob.data.copy(); hull.name = "ink"; bpy.context.collection.objects.link(hull)
    hull.data.materials.clear(); hull.data.materials.append(ink)
    d = hull.modifiers.new("push", "DISPLACE"); d.direction = "NORMAL"; d.mid_level = 0.0; d.strength = thick
    return hull


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
    HM.reset(); s, cam = HM.scene(HM.C["bg"]); s.render.use_freestyle = False; s.cycles.samples = 8
    ob = load(src); paint(ob)
    root = bpy.data.objects.new("root", None); bpy.context.collection.objects.link(root)
    ob.parent = root
    for e in eyes(ob): e.parent = root
    if "--no-ink" not in sys.argv:
        outline(ob).parent = root
    cam.data.ortho_scale = 2.2; cam.location = (0, -8, 1.0); cam.rotation_euler = (math.pi / 2, 0, 0)
    for name, az in HM.VIEWS.items():
        root.rotation_euler.z = -math.radians(az); bpy.context.view_layer.update()
        s.render.filepath = os.path.join(out, f"body_{name}.png"); bpy.ops.render.render(write_still=True)
    root.rotation_euler.z = 0
    if "--save-blend" in sys.argv:
        bpy.ops.wm.save_as_mainfile(filepath=sys.argv[sys.argv.index("--save-blend") + 1])
    print("done")
