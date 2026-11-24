"""Hero built on the CC0 MakeHuman base mesh (muscular male target), faceless egg head, MMA gloves,
offset-shell compression shirt and loose shorts, toon shading + Freestyle ink. Rendered directly in Blender.
Assets: production/blender/assets/makehuman (base.obj + targets, CC0 2020). Run: python3 hero_mh.py OUTDIR [--save-blend PATH]
"""
import math, os, sys
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
sys.path.insert(0, os.path.dirname(__file__))
import hero_model as HM

A = os.path.join(os.path.dirname(__file__), "assets", "makehuman")
HEIGHT = 1.85


def load_mh(targets):
    V, F, groups, cur = [], [], {}, None
    for line in open(os.path.join(A, "base.obj")):
        if line.startswith("v "):
            V.append(Vector([float(x) for x in line.split()[1:4]]))
        elif line.startswith("g "):
            cur = line.split()[1]; groups.setdefault(cur, [])
        elif line.startswith("f ") and cur:
            groups[cur].append([int(t.split("/")[0]) - 1 for t in line.split()[1:]])
    for name, w in targets:
        for line in open(os.path.join(A, name + ".target")):
            if line[0].isdigit():
                i, dx, dy, dz = line.split()[:4]; V[int(i)] += Vector((float(dx), float(dy), float(dz))) * w
    # MakeHuman: Y up, facing +Z, decimetres -> Blender: Z up, facing -Y, metres
    V = [Vector((v.x, -v.z, v.y)) for v in V]
    body_idx = sorted({i for f in groups["body"] for i in f})
    zmin = min(V[i].z for i in body_idx); zmax = max(V[i].z for i in body_idx); k = HEIGHT / (zmax - zmin)
    V = [Vector((v.x * k, v.y * k, (v.z - zmin) * k)) for v in V]
    J = {g[6:]: sum((V[i] for f in fs for i in f), Vector()) / sum(len(f) for f in fs) for g, fs in groups.items() if g.startswith("joint-")}
    return V, groups["body"], J


def soft_rotate(V, J, side, angle_deg):
    """lower the arm about the shoulder joint with a smooth falloff (static reference pose, no rig needed)"""
    x = 1 if side == "l" else -1
    sh = J[f"{side}-shoulder"]; R = Matrix.Rotation(math.radians(angle_deg) * x, 3, "Y")
    for i, v in enumerate(V):
        d = (v.x - sh.x) * x
        if v.z < J[f"{side}-shoulder"].z - 0.55 or d < -0.05:
            continue
        w = max(0.0, min(1.0, (d + 0.05) / 0.12)); w = w * w * (3 - 2 * w)
        if w > 0:
            V[i] = v.lerp(sh + R @ (v - sh), w)
    for k in (f"{side}-elbow", f"{side}-hand"):
        J[k] = sh + R @ (J[k] - sh)
    return V


def heroic(V, J):
    """comic exaggeration: broader shoulders and lats, thicker arms and legs (pose independent radial scaling)"""
    waist, sh_z = J["spine-3"].z, J["l-shoulder"].z
    out = []
    for v in V:
        v = v.copy()
        arm = None
        for s, x in (("l", 1), ("r", -1)):
            if (v.x - J[f"{s}-shoulder"].x) * x > -0.02 and v.z > waist - 0.15:
                arm = s
        if arm:
            a, b = J[f"{arm}-shoulder"], J[f"{arm}-hand"]; ab = b - a; t = max(0, min(1, (v - a).dot(ab) / ab.length_squared))
            c = a + ab * t; k = 1.38 if t < 0.55 else 1.22
            v = c + (v - c) * k
        elif v.z > waist:
            f = 1.0 + 0.24 * max(0.0, min(1.0, (v.z - waist) / (sh_z - waist)))
            v.x *= f; v.y *= 1.0 + 0.06 * max(0.0, min(1.0, (v.z - waist) / (sh_z - waist)))
        elif v.z > J["l-ankle"].z:
            for s, x in (("l", 1), ("r", -1)):
                if v.x * x > 0:
                    a, b = J[f"{s}-upper-leg"], J[f"{s}-ankle"]; ab = b - a; t = max(0, min(1, (v - a).dot(ab) / ab.length_squared))
                    c = a + ab * t; v = c + (v - c) * 1.12
        out.append(v)
    return out


def build_body(V, F, J):
    me = bpy.data.meshes.new("hero_body"); me.from_pydata(V, [], F); me.validate()
    ob = bpy.data.objects.new("hero_body", me); bpy.context.collection.objects.link(ob)
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    neck_cut = J["neck"].z + 0.035
    dele = [v for v in bm.verts if v.co.z > neck_cut]                         # replaced by the faceless egg head
    for s, x in (("l", 1), ("r", -1)):                                        # hands replaced by gloves
        el, wr = J[f"{s}-elbow"], J[f"{s}-hand"]; ax = (wr - el).normalized()
        dele += [v for v in bm.verts if (v.co - wr).dot(ax) > -0.01 and (v.co - wr).length < 0.3]
    bmesh.ops.delete(bm, geom=list(set(dele)), context="VERTS")
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = True
    sub = ob.modifiers.new("sub", "SUBSURF"); sub.levels = 1
    sm = ob.modifiers.new("sm", "SMOOTH"); sm.factor = 0.6; sm.iterations = 12
    bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier="sub"); bpy.ops.object.modifier_apply(modifier="sm")
    return ob


def shell(body, name, keep, offset, mat, red_fn=None, loosen=None):
    """garment = offset copy of the body region (planes give clean hems)"""
    ob = body.copy(); ob.data = body.data.copy(); ob.name = name; bpy.context.collection.objects.link(ob)
    ob.data.materials.clear()
    bm = bmesh.new(); bm.from_mesh(ob.data)
    for co, no in keep["planes"]:
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no)
    dele = [v for v in bm.verts if not keep["test"](v.co)]
    bmesh.ops.delete(bm, geom=dele, context="VERTS")
    bm.normal_update()
    for v in bm.verts:
        extra = loosen(v.co) if loosen else 0.0
        ax = keep["axis"](v.co); radial = v.co - ax
        n = v.normal if v.normal.dot(radial) >= 0 else -v.normal
        v.co += n * (offset + extra)
    bm.to_mesh(ob.data); bm.free()
    ob.data.materials.append(mat)
    if red_fn:
        HM.attr(ob, "red", red_fn)
    return ob


def build(J, body):
    skin = HM.toon("skin", HM.C["skin"]); body.data.materials.append(skin)
    shirt = HM.toon("shirt", HM.C["shirt"], "red", HM.C["red"]); shorts = HM.toon("shorts", HM.C["shorts"], "red", HM.C["red"])
    waist_z = J["spine-3"].z - 0.02; hem_z = J["l-knee"].z + 0.10; neck_z = J["neck"].z - 0.03
    arm_planes = []
    for s, x in (("l", 1), ("r", -1)):
        ax = (J[f"{s}-shoulder"] - J["spine-1"]).normalized(); arm_planes.append((J[f"{s}-shoulder"] - ax * 0.02, ax))
    def torso_keep(co):
        return waist_z - 0.005 < co.z < neck_z + 0.08 - 0.25 * max(0.0, -co.y - 0.02) and all((co - p).dot(n) < 0 for p, n in arm_planes)
    def red(co):
        sx = 1 if co.x > 0 else -1; s = HM.seg
        f = co.y < 0 and (s(co, (0.07 * sx, -0.08, neck_z + 0.01), (0.20 * sx, -0.04, neck_z - 0.08)) < 0.011 or
                          s(co, (0.18 * sx, -0.03, neck_z - 0.14), (0.13 * sx, -0.08, waist_z + 0.04)) < 0.010)
        b = co.y > 0 and (s(co, (0.21 * sx, 0.05, neck_z - 0.05), (0.07 * sx, 0.12, neck_z - 0.24)) < 0.011 or
                          s(co, (0.18 * sx, 0.04, neck_z - 0.15), (0.14 * sx, 0.08, waist_z + 0.04)) < 0.010)
        return 1.0 if (f or b) else 0.0
    shell(body, "hero_shirt", {"planes": [((0, 0, waist_z), (0, 0, 1)), ((0, 0, neck_z), (0, 0.25, 1))] + arm_planes,
                               "test": torso_keep, "axis": lambda co: Vector((0, 0.0, co.z))}, 0.004, shirt, red)
    def near_arm(co):
        return any(HM.seg(co, J[f"{s}-shoulder"], J[f"{s}-hand"]) < 0.075 for s in "lr")
    def shorts_keep(co):
        return hem_z < co.z < waist_z + 0.01 and abs(co.x) < 0.30 and not near_arm(co)
    def leg_axis(co):
        if co.z > J["l-upper-leg"].z + 0.03:
            return Vector((0, 0, co.z))
        s = "l" if co.x > 0 else "r"; a, b = J[f"{s}-upper-leg"], J[f"{s}-knee"]; ab = b - a
        t = (co - a).dot(ab) / ab.length_squared; return a + ab * t
    def loose(co):
        return 0.012 * max(0.0, min(1.0, (waist_z - 0.06 - co.z) / 0.15))
    def notch(co):
        if abs(co.x) < 0.12 or co.z > hem_z + 0.13:
            return 0.0
        h = co.z - hem_z; w = 0.07 * (1 - h / 0.13)
        return 1.0 if w - 0.014 < abs(co.y) < w + 0.004 else 0.0
    shell(body, "hero_shorts", {"planes": [((0, 0, hem_z), (0, 0, 1)), ((0, 0, waist_z + 0.01), (0, 0, 1))], "test": shorts_keep, "axis": leg_axis},
          0.010, shorts, notch, loose)
    # faceless egg head + ears + eyes
    hc = J["head"] + Vector((0, -0.005, 0.06))
    head = HM.metaball_mesh("hero_head", [((hc.x, hc.y, hc.z), (0.093, 0.108, 0.128), (12, 0, 0)),
                                          ((hc.x, hc.y + 0.02, J["neck"].z + 0.01), (0.10, 0.092, 0.10), (0, 0, 0)),
                                          ((hc.x + 0.093, hc.y + 0.012, hc.z - 0.01), (0.013, 0.024, 0.035), (0, 0, 0)),
                                          ((hc.x - 0.093, hc.y + 0.012, hc.z - 0.01), (0.013, 0.024, 0.035), (0, 0, 0))], smooth=12)
    head.data.materials.append(skin)
    eyes_at(head, hc)
    # comic deltoid caps and trapezius slope (separate volumes so the ink line marks the muscle edge)
    caps = []
    for s, x in (("l", 1), ("r", -1)):
        sh = J[f"{s}-shoulder"]; el = J[f"{s}-elbow"]; d = (el - sh).normalized()
        c = sh + d * 0.05 + Vector((0.025 * x, 0, 0.0))
        caps.append(((c.x - 0.01 * x, c.y, c.z - 0.02), (0.078, 0.088, 0.10), (0, 0, 0)))
    delt = HM.metaball_mesh("hero_delts", caps, smooth=10); delt.data.materials.append(skin)
    tz = J["neck"].z - 0.04
    trap = HM.metaball_mesh("hero_traps", [((0.075, 0.03, tz), (0.11, 0.07, 0.055), (0, 0, -22)), ((-0.075, 0.03, tz), (0.11, 0.07, 0.055), (0, 0, 22))], smooth=10)
    trap.data.materials.append(shirt)
    for s, x in (("l", 1), ("r", -1)):
        glove_at(J[f"{s}-elbow"], J[f"{s}-hand"], x)
    face = bpy.data.collections["face_lines_only"]
    for o in list(bpy.data.objects):
        if o.name.startswith(("hero_head", "hero_eye")):
            for c in list(o.users_collection):
                c.objects.unlink(o)
            face.objects.link(o)


def eyes_at(head, hc):
    em = HM.flat("eye", HM.C["eye"]); inv = head.matrix_world.inverted()
    for x in (1, -1):
        ok, loc, nor, _ = head.ray_cast(inv @ Vector((hc.x + 0.042 * x, -0.5, hc.z + 0.005)), Vector((0, 1, 0)))
        if not ok:
            continue
        bm = bmesh.new(); pts = []
        for i in range(32):
            t = i * 2 * math.pi / 32
            pts.append(bm.verts.new((math.cos(t) * 0.033, math.sin(t) * (0.012 if math.sin(t) > 0 else 0.006), 0)))
        bm.faces.new(pts); me = bpy.data.meshes.new("eye"); bm.to_mesh(me); bm.free()
        e = bpy.data.objects.new(f"hero_eye{x}", me); bpy.context.collection.objects.link(e)
        e.rotation_mode = "QUATERNION"
        e.rotation_quaternion = nor.to_track_quat("Z", "Y") @ Euler((0, 0, math.radians(-17 * x))).to_quaternion()
        e.location = loc + nor * 0.0025
        sw = e.modifiers.new("wrap", "SHRINKWRAP"); sw.target = head; sw.offset = 0.0025
        me.materials.append(em)


def glove_at(el, wr, x):
    gm = HM.toon("glove", HM.C["glove"]); rm = HM.toon("strap", HM.C["red"])
    ax = (wr - el).normalized(); q = ax.to_track_quat("Z", "Y")
    c = wr + ax * 0.075
    def add(mesh_fn, loc, scale, mat, rot=None):
        mesh_fn(); o = bpy.context.object; o.location = loc; o.rotation_mode = "QUATERNION"
        o.rotation_quaternion = q if rot is None else rot; o.scale = scale; o.data.materials.append(mat)
        bpy.ops.object.shade_smooth(); return o
    add(lambda: bpy.ops.mesh.primitive_uv_sphere_add(radius=1), c, (0.05, 0.056, 0.066), gm)
    fwd = q @ Vector((0, -1, 0))
    for i in range(4):
        add(lambda: bpy.ops.mesh.primitive_uv_sphere_add(radius=1), c + fwd * 0.045 + ax * (0.03 - 0.02 * i), (0.04, 0.022, 0.0115), gm)
    add(lambda: bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=32), wr + ax * 0.005, (0.048, 0.048, 0.03), rm)
    add(lambda: bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, vertices=32), wr + ax * 0.028, (0.05, 0.05, 0.016), gm)


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    HM.reset(); s, cam = HM.scene(HM.C["bg"])
    V, F, J = load_mh([("universal-male-young-maxmuscle-averageweight", 1.0)])
    for side in ("l", "r"):
        cur = math.degrees(math.atan2(J[f"{side}-shoulder"].z - J[f"{side}-elbow"].z, abs(J[f"{side}-elbow"].x - J[f"{side}-shoulder"].x)))
        V = soft_rotate(V, J, side, 68 - cur)
    # refresh joints after posing arms
    Vj = V
    _, _, J2 = (None, None, None)
    V = heroic(V, J)
    for k in list(J):
        if any(k.startswith(p) for p in ("l-", "r-")) and ("shoulder" in k or "elbow" in k or "hand" in k):
            pass
    body = build_body(V, F, J)
    build(J, body)
    for name, az in HM.VIEWS.items():
        a = math.radians(az); d = Vector((math.sin(a), -math.cos(a), 0.0))
        cam.location = Vector((0, 0, 0.93)) + d * 8; cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        s.render.filepath = os.path.join(out, f"hero_{name}.png"); bpy.ops.render.render(write_still=True)
        print("rendered", name)
    if "--save-blend" in sys.argv:
        bpy.ops.wm.save_as_mainfile(filepath=sys.argv[sys.argv.index("--save-blend") + 1])
