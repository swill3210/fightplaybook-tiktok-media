"""Hero on the MPFB2 professional base (CC0 MakeHuman mesh, targets, default rig with skin weights).
Stage 1: body only (macros + region targets), A pose like the reference, turnaround renders for inspection.
Run: python3 hero_mpfb.py OUTDIR [--info] [--save-blend PATH]
"""
import math, os, sys
import bpy, addon_utils
from mathutils import Vector
sys.path.insert(0, os.path.dirname(__file__))
import hero_model as HM

addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.targetservice import TargetService

MACRO = {"gender": 1.0, "age": 0.5, "muscle": 1.0, "weight": 0.62, "proportions": 1.0, "height": 0.8, "cupsize": 0.5,
         "firmness": 0.5, "race": {"african": 0.34, "asian": 0.33, "caucasian": 0.33}}
REGION = {  # target name -> weight (heroic comic build, reference sheet); tuned 2026-11-24 r4 against the side views
    "measure-shoulder-dist-incr": 0.45, "torso-muscle-pectoral-incr": 1.0, "torso-muscle-dorsi-incr": 1.0,
    "torso-vshape-incr": 0.8, "torso-scale-depth-incr": 0.45, "measure-bust-circ-incr": 0.5,
    "measure-waist-circ-decr": 0.6, "measure-hips-circ-decr": 0.3, "torso-scale-horiz-incr": 0.2,
    "measure-neck-circ-incr": 1.0, "neck-scale-horiz-incr": 0.6, "measure-neck-height-decr": 0.6,
    "head-scale-horiz-decr": 0.3, "head-scale-vert-decr": 0.12, "head-scale-depth-decr": 0.12,
    "measure-upperarm-circ-incr": 1.0, "measure-thigh-circ-incr": 0.6, "measure-calf-circ-incr": 0.6,
    **{f"{s}-{part}": 1.0 for s in "lr" for part in (
        "upperarm-muscle-incr", "lowerarm-muscle-incr", "upperarm-shoulder-muscle-incr",
        "upperleg-muscle-incr", "lowerleg-muscle-incr")},
    **{f"{s}-{part}": 0.5 for s in "lr" for part in (
        "upperarm-scale-horiz-incr", "upperarm-scale-depth-incr", "lowerarm-scale-horiz-incr", "lowerarm-scale-depth-incr")},
}


def build_body():
    h = HumanService.create_human(scale=0.1, feet_on_ground=True, macro_detail_dict=MACRO)
    missing = []
    for name, w in REGION.items():
        p = TargetService.target_full_path(name)
        if p:
            TargetService.load_target(h, p, weight=w, name=name)
        else:
            missing.append(name)
    if missing:
        print("missing targets", missing)
    return h


FACE = {  # flatten the features first with targets (keeps the MPFB skull, jaw and ears), then smooth what is left
    "nose-volume-decr": 1.0, "nose-scale-depth-decr": 1.0, "nose-scale-horiz-decr": 0.6, "nose-flaring-decr": 1.0,
    "mouth-upperlip-volume-decr": 1.0, "mouth-lowerlip-volume-decr": 1.0, "mouth-scale-depth-decr": 1.0,
    "mouth-scale-horiz-decr": 0.5, "eyebrows-trans-backward": 1.0, "l-eye-bag-decr": 1.0, "r-eye-bag-decr": 1.0,
    # reference head: egg shaped mask, jaw tapering to a narrow chin (front view), one smooth slope brow to chin (profile)
    "head-invertedtriangular": 0.7, "head-oval": 0.6, "chin-width-decr": 1.0, "chin-height-incr": 0.5, "chin-prominent-incr": 0.4,
}


def _centroid(ob, coords, group):
    gi = ob.vertex_groups[group].index
    pts = [coords[v.index] for v in ob.data.vertices if any(g.group == gi for g in v.groups)]
    return sum(pts, Vector()) / len(pts)


def remove_hidden_face_walls(h, co, f, r, ymax, zmin, body):
    """inside the face zone keep only faces SEEN from the front (5 frontal rays); delete the rest (inner lip roll,
    mouth bag, nostrils, socket walls; faces only so vertex indices, shape keys and weights stay valid) and cap the holes.
    The depth test (close_cavities) kept the shallow inner lip roll, which z-fought with the outer lip after
    projection and drew a mouth (r19 to r22). The hero has NO MOUTH."""
    import bmesh
    from mathutils.bvhtree import BVHTree
    bm = bmesh.new(); bm.from_mesh(h.data); bm.faces.ensure_lookup_table(); dl = bm.verts.layers.deform.active
    faces = [fc for fc in bm.faces if all(body in v[dl] for v in fc.verts)]
    polys = [[v.index for v in fc.verts] for fc in faces]
    tree = BVHTree.FromPolygons(co, polys)
    dirs = [Vector(d).normalized() for d in ((0, 1, 0), (0.5, 1, 0), (-0.5, 1, 0), (0, 1, 0.45), (0, 1, -0.45))]
    kill = []
    for k, fc in enumerate(faces):
        c = sum((co[v.index] for v in fc.verts), Vector()) / len(fc.verts)
        if (c - f).length > r or c.y > ymax or c.z < zmin:
            continue
        seen = False
        for d in dirs:
            hit = tree.ray_cast(c - d * 1.0, d)
            if hit[2] is not None and (hit[2] == k or (hit[0] - c).length < 1e-4):
                seen = True; break
        if not seen:
            kill.append(fc)
    bmesh.ops.delete(bm, geom=kill, context="FACES_ONLY")
    edges = [e for e in bm.edges if e.is_boundary and all(body in v[dl] for v in e.verts)]
    caps = bmesh.ops.holes_fill(bm, edges=edges, sides=0)["faces"]
    bmesh.ops.triangulate(bm, faces=caps, quad_method="BEAUTY", ngon_method="BEAUTY")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(h.data); bm.free(); h.data.update()
    print("hidden face walls removed", len(kill), "caps", len(caps))


def close_cavities(h, co, feats, depth, body):
    """delete the mouth bag and eye socket walls (faces only; vertex indices, shape keys and weights stay valid)
    and cap the openings with ngons, so smoothing cannot open the lips into a dark ring (r6, E01)"""
    import bmesh
    inner = set()
    for c, rx, rz in feats:  # elliptical zones; a round mouth zone reached the nostrils and tore them (r7)
        near = [i for i, p in enumerate(co) if ((p.x - c.x) / rx) ** 2 + ((p.z - c.z) / rz) ** 2 < 1]
        front = min(co[i].y for i in near)
        inner |= {i for i in near if co[i].y > front + depth}
    bm = bmesh.new(); bm.from_mesh(h.data); bm.verts.ensure_lookup_table()
    dl = bm.verts.layers.deform.active
    kill = [f for f in bm.faces if all(v.index in inner and body in v[dl] for v in f.verts)]
    bmesh.ops.delete(bm, geom=kill, context="FACES_ONLY")
    edges = [e for e in bm.edges if e.is_boundary and all(body in v[dl] for v in e.verts)]
    caps = bmesh.ops.holes_fill(bm, edges=edges, sides=0)["faces"]
    bmesh.ops.triangulate(bm, faces=caps, quad_method="BEAUTY", ngon_method="BEAUTY")
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)  # inside out caps made the voxel proxy scoop the face (r11)
    bm.to_mesh(h.data); bm.free(); h.data.update()
    print("cavity faces removed", len(kill))


def faceless(h, iters=120):
    """remove face features: FACE targets, then a Laplacian smooth weighted to the face front (ears and jaw kept).
    Works because the MPFB body mesh is closed at the eyes and mouth (no boundary loops; checked 2026-11-24)."""
    for name, w in FACE.items():
        p = TargetService.target_full_path(name)
        if p:
            TargetService.load_target(h, p, weight=w, name=name)
    dg = bpy.context.evaluated_depsgraph_get(); ev = h.evaluated_get(dg); me = ev.to_mesh()
    co = [v.co.copy() for v in me.vertices]; ev.to_mesh_clear()  # Mask modifier keeps indices? use shape key mix instead
    kb = h.data.shape_keys.key_blocks if h.data.shape_keys else None
    if kb:  # mixed shape (all targets) at their current weights
        base = [v.co.copy() for v in kb[0].data]
        co = [c.copy() for c in base]
        for k in kb[1:]:
            if k.value:
                for i, (a, b) in enumerate(zip(k.data, kb[0].data)):
                    co[i] += (a.co - b.co) * k.value
    le, re, mo = (_centroid(h, co, g) for g in ("joint-l-eye", "joint-r-eye", "joint-mouth"))
    iod = (le - re).length
    f = Vector((0, min(le.y, re.y) - 0.2 * iod, (le.z + mo.z) / 2 - 0.15 * iod))  # mouth must be at FULL weight (r21: partial weight left lips)
    ears = h.vertex_groups["ears"].index; body = h.vertex_groups["body"].index
    remove_hidden_face_walls(h, co, f, 2.0 * iod, le.y + 0.6 * iod, mo.z - 1.3 * iod, body)
    vg = h.vertex_groups.new(name="face_smooth")
    r0, r1 = 1.3 * iod, 2.0 * iod
    for v in h.data.vertices:
        gs = {g.group for g in v.groups}
        if body not in gs or ears in gs:
            continue
        c = co[v.index]
        if c.y > le.y + 0.6 * iod or c.z < mo.z - 1.3 * iod:
            continue
        d = (Vector((c.x, c.y, c.z)) - f).length
        w = 1.0 if d < r0 else max(0.0, 1 - (d - r0) / (r1 - r0))
        if w > 0:
            vg.add([v.index], w * w * (3 - 2 * w), "REPLACE")
    # Smooth alone left a nose and an open O mouth (r5, r6); capping the cavities left a recessed ring (r8, r9).
    # So project the weighted face onto a smooth mask proxy: the head voxel remeshed (seals the lip slit and sockets)
    # and smoothed. The proxy is only a projection target and is never rendered.
    # Mask proxy = CONVEX HULL of the head (ears excluded): no concavity can survive, so no mouth, sockets or nostrils,
    # and the profile becomes one slope from brow to chin like the reference. Earlier proxies (voxel remesh of the head,
    # r10 to r19; plus a weighted smooth, r20) kept a lip mound or shrank into a dark recess.
    import bmesh
    dg = bpy.context.evaluated_depsgraph_get(); src = bpy.data.meshes.new_from_object(h.evaluated_get(dg))
    bm = bmesh.new(); bm.from_mesh(src); dl = bm.verts.layers.deform.active
    keep = [v for v in bm.verts if body in v[dl] and ears not in v[dl] and v.co.z > mo.z - 1.6 * iod and v.link_faces]
    hull = bmesh.ops.convex_hull(bm, input=keep)
    hv = {v for g in hull["geom"] if isinstance(g, bmesh.types.BMFace) for v in g.verts}
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v not in hv], context="VERTS")
    pm = bpy.data.meshes.new("face_proxy"); bm.to_mesh(pm); bm.free(); bpy.data.meshes.remove(src)
    proxy = bpy.data.objects.new("face_proxy", pm); bpy.context.collection.objects.link(proxy)
    rm = proxy.modifiers.new("even", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = 0.06 * iod
    ps = proxy.modifiers.new("round", "SMOOTH"); ps.factor = 1.0; ps.iterations = 12
    proxy.hide_render = True; proxy.hide_viewport = True
    sw = h.modifiers.new("faceless", "SHRINKWRAP"); sw.target = proxy; sw.vertex_group = vg.name
    sw.wrap_method = "NEAREST_SURFACEPOINT"
    h.modifiers.move(h.modifiers.find(sw.name), 0)
    sm = h.modifiers.new("blend", "SMOOTH"); sm.vertex_group = vg.name; sm.factor = 0.5; sm.iterations = 6
    h.modifiers.move(h.modifiers.find(sm.name), 1)
    # shading normals of the face come from the smooth proxy: the lips and nostrils collapse into slivers on the
    # proxy and their own normals drew a mouth line and a nostril mark even without ink (2026-11-24 d1). NO MOUTH.
    dt = h.modifiers.new("mask_normals", "DATA_TRANSFER"); dt.object = proxy; dt.use_loop_data = True
    dt.data_types_loops = {"CUSTOM_NORMAL"}; dt.loop_mapping = "POLYINTERP_NEAREST"; dt.vertex_group = vg.name
    h.modifiers.move(h.modifiers.find(dt.name), 2)
    return le, re, iod


def eyes(h, rig, le, re, iod, slant=27):
    """filled white slanted almonds, inner corners lower (angled toward the centre), hugging the face (Shrinkwrap)"""
    import bmesh
    white = HM.flat("eye_white", HM.C["eye"]); obs = []
    for c, sgn in ((le, 1), (re, -1)):
        me = bpy.data.meshes.new("eye"); bm = bmesh.new()
        w, hh, n = 0.5 * iod, 0.15 * iod, 40  # reference eyes: small, thin, steep (r18 eyes were too big and round)
        rim = []
        for i in range(n):
            t = 2 * math.pi * i / n; x = w / 2 * math.cos(t)
            z = hh * math.sin(t) * (1 - (2 * x / w) ** 2) ** 0.35 * (1.0 if t < math.pi else 0.55)  # flatter lower lid
            rim.append((x, z))
        ctr = bm.verts.new((0, 0, 0)); rings = 4; prev = None; vs_all = []
        for r in range(1, rings + 1):
            ring = [bm.verts.new((x * r / rings, 0, z * r / rings)) for x, z in rim]; vs_all.append(ring)
        for i in range(n):
            j = (i + 1) % n; bm.faces.new((ctr, vs_all[0][i], vs_all[0][j]))
            for r in range(rings - 1):
                bm.faces.new((vs_all[r][i], vs_all[r + 1][i], vs_all[r + 1][j], vs_all[r][j]))
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new("eye", me); bpy.context.collection.objects.link(ob); me.materials.append(white)
        ob.location = Vector((c.x * 1.04, c.y - 0.6 * iod, c.z)); ob.rotation_euler = (0, math.radians(-slant) * sgn, 0)
        sw = ob.modifiers.new("hug", "SHRINKWRAP"); sw.target = h; sw.wrap_method = "PROJECT"
        sw.use_project_y = True; sw.use_negative_direction = True; sw.use_positive_direction = True; sw.offset = 0.0012
        obs.append(ob)
    for ob in obs:  # object parent for the design stage; bone parenting sent one eye to the floor (r5), redo at rigging
        ob.parent = rig; ob.matrix_parent_inverse = rig.matrix_world.inverted()
    return obs


def _rot(rig, bone, deg, axis, sgn):
    from mathutils import Matrix
    pb = rig.pose.bones[bone]; h = pb.head.copy()
    pb.matrix = Matrix.Translation(h) @ Matrix.Rotation(math.radians(deg) * sgn, 4, axis) @ Matrix.Translation(-h) @ pb.matrix
    bpy.context.view_layer.update()


def a_pose(rig, body, deg=30, clav=7, elbow=30):
    """lower both arms toward the reference stance through the professional rig (skin weights, no tearing).
    The drop is shared between shoulder01 and upperarm01 and the armature uses dual quaternion skinning,
    so the deltoid keeps its volume instead of collapsing into a box (2026-11-24 render r2)."""
    for m in body.modifiers:
        if m.type == "ARMATURE":
            m.use_deform_preserve_volume = True
    bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode="POSE")
    for side, sgn in (("L", 1), ("R", -1)):
        _rot(rig, f"shoulder01.{side}", clav, "Y", sgn)
        _rot(rig, f"upperarm01.{side}", deg - clav, "Y", sgn)
        if elbow:
            _rot(rig, f"lowerarm01.{side}", elbow, "X", 1)  # +X swings the hand back; the MPFB base forearm points forward (0 and -25 left the hands reaching forward, r4, r17)
    bpy.ops.object.mode_set(mode="OBJECT")


def outline(body, thick=0.007):
    """inverted hull ink as a SEPARATE linked object (same mesh, same armature), pushed out along normals.
    Solidify on the body put the ink material on the body surface itself and rendered a black silhouette (r1, r2)."""
    ink = bpy.data.materials.new("ink"); ink.use_nodes = True; nt = ink.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.008, 0.008, 0.01, 1)
    geo = nt.nodes.new("ShaderNodeNewGeometry"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Backfacing"], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1])  # hull front = see through
    nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], o.inputs[0])  # hull inside = ink rim
    hull = body.copy(); hull.name = body.name + "_ink"; bpy.context.collection.objects.link(hull)
    for sl in hull.material_slots:
        sl.link = "OBJECT"; sl.material = ink
    d = hull.modifiers.new("push", "DISPLACE"); d.direction = "NORMAL"; d.mid_level = 0.0; d.strength = thick
    if "faceless" in hull.modifiers:  # face: offset from the smooth proxy; normals of the folded features poked ink through (r15)
        hull.modifiers["faceless"].offset = thick
        d.vertex_group = "face_smooth"; d.invert_vertex_group = True
    hull.visible_shadow = False
    return hull


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    HM.reset()
    addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
    s, cam = HM.scene(HM.C["bg"]); s.render.use_freestyle = False  # Freestyle draws nothing on shape keyed meshes
    body = build_body()
    body.data.materials.clear(); body.data.materials.append(HM.toon("skin", HM.C["skin"]))
    le, re, iod = faceless(body)
    rig = HumanService.add_builtin_rig(body, "default")
    eyes(body, rig, le, re, iod)
    bpy.data.objects["face_proxy"].parent = rig  # Shrinkwrap is world space: the proxy must turn with the figure (r13)
    if "--info" in sys.argv:
        print("BONES", [b.name for b in rig.data.bones][:80])
    a_pose(rig, body)
    if "--no-ink" not in sys.argv:
        outline(body)
    dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg)
    zs = [(body.matrix_world @ v.co).z for v in ev.to_mesh().vertices]; zmax, zmin = max(zs), min(zs); ev.to_mesh_clear()
    print("height", round(zmax - zmin, 3))
    cam.data.ortho_scale = (zmax - zmin) * 1.12; cam.location = Vector((0, -8, (zmax + zmin) / 2)); cam.rotation_euler = (math.pi / 2, 0, 0)
    for name, az in ([] if "--face-only" in sys.argv else HM.VIEWS.items()):  # turn the figure, not the camera, so the key light is the same in every view
        rig.rotation_euler.z = -math.radians(az); bpy.context.view_layer.update()
        s.render.filepath = os.path.join(out, f"body_{name}.png"); bpy.ops.render.render(write_still=True)
    rig.rotation_euler.z = 0
    hz = max(le.z, re.z); cam.data.ortho_scale = 10 * iod; cam.location = Vector((0, -8, hz - 0.4 * iod))
    for name, az in (("face_front", 0), ("face_threequarter", 35), ("face_right", -90)):
        rig.rotation_euler.z = -math.radians(az); bpy.context.view_layer.update()
        hc = rig.matrix_world @ Vector((0, 0.5 * le.y, hz))  # head centre, framed after the turn
        cam.location.x = hc.x
        s.render.filepath = os.path.join(out, f"{name}.png"); bpy.ops.render.render(write_still=True)
    rig.rotation_euler.z = 0
    if "--save-blend" in sys.argv:
        bpy.ops.wm.save_as_mainfile(filepath=sys.argv[sys.argv.index("--save-blend") + 1])
    print("done")
