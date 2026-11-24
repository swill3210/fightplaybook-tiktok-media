"""Hero character model (reference pose), rendered directly in Blender. No generative model.

Body = metaball muscle volumes (separate families for head, torso, each arm, each leg so the junctions draw ink lines),
converted to meshes, garments by plane slices + attributes, toon emission shader (shadow / base / highlight),
Freestyle ink lines (silhouette, crease, ridges and valleys for muscle definition), orthographic turnaround.
Run: python3 hero_model.py OUTDIR [--save-blend PATH]
"""
import math, sys, os
import bpy, bmesh
from mathutils import Vector, Euler

HEX = lambda h: tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (1, 3, 5)) + (1,)
C = {"skin": ("#2b2c31", "#45464c", "#6a6b72"), "shirt": ("#09090b", "#17171a", "#2c2c31"),
     "shorts": ("#141b36", "#212d58", "#33437a"), "red": ("#9b1220", "#d1202f", "#e8505a"),
     "glove": ("#08080a", "#17171a", "#34343a"), "bg": "#D8EEFE", "eye": "#ffffff"}
LIGHT = Vector((-0.45, -0.7, 0.55)).normalized()

# metaball volumes: family -> list of (centre, size xyz, rotation deg xyz). Character faces -Y, LEFT = +X.
def sym(lst):
    out = []
    for c, sz, r in lst:
        out.append(((c[0], c[1], c[2]), sz, r))
        out.append(((-c[0], c[1], c[2]), sz, (r[0], -r[1], -r[2])))
    return out

BODY = {
 "head": [((0, 0.0, 1.705), (0.098, 0.112, 0.142), (14, 0, 0)),
          ((0, 0.015, 1.565), (0.092, 0.085, 0.085), (0, 0, 0))] + sym([((0.096, 0.015, 1.695), (0.014, 0.026, 0.036), (0, 0, 0))]),
 "torso": [((0, 0.0, 1.37), (0.19, 0.115, 0.13), (0, 0, 0)), ((0, -0.03, 1.16), (0.118, 0.092, 0.15), (0, 0, 0)),
           ((0, 0.0, 1.00), (0.165, 0.115, 0.10), (0, 0, 0))] +
          sym([((0.085, -0.052, 1.385), (0.105, 0.065, 0.078), (0, 0, -8)),      # pecs
               ((0.15, 0.035, 1.30), (0.09, 0.075, 0.14), (0, 0, 14)),           # lats
               ((0.105, -0.005, 1.13), (0.055, 0.075, 0.10), (0, 0, -6)),        # obliques
               ((0.10, 0.02, 1.52), (0.13, 0.075, 0.06), (0, 0, -20)),           # traps
               ((0.08, 0.06, 0.97), (0.085, 0.075, 0.085), (0, 0, 0))]),         # glutes
 "arm": [((0.245, 0.0, 1.45), (0.098, 0.095, 0.10), (0, 0, 0)),                # deltoid
         ((0.27, 0.0, 1.19), (0.05, 0.05, 0.09), (0, 0, 3)),                   # elbow bridge
         ((0.278, -0.005, 0.93), (0.038, 0.036, 0.05), (0, 0, 0)),             # wrist bridge
         ((0.27, -0.03, 1.29), (0.068, 0.066, 0.11), (0, 0, 4)),               # biceps
         ((0.278, 0.032, 1.31), (0.07, 0.068, 0.125), (0, 0, 4)),              # triceps
         ((0.282, -0.008, 1.10), (0.068, 0.062, 0.085), (0, 0, 2)),            # forearm upper
         ((0.278, -0.005, 0.985), (0.043, 0.04, 0.075), (0, 0, 0))],           # forearm lower
 "leg": [((0.105, -0.02, 0.75), (0.105, 0.105, 0.21), (0, 0, 3)),               # quad
         ((0.11, 0.0, 0.62), (0.075, 0.075, 0.12), (0, 0, 0)),                 # knee bridge upper
         ((0.113, 0.0, 0.18), (0.042, 0.042, 0.12), (0, 0, 0)),                # ankle bridge
         ((0.11, 0.04, 0.74), (0.088, 0.08, 0.17), (0, 0, 3)),                 # hamstring
         ((0.112, -0.012, 0.53), (0.064, 0.064, 0.085), (0, 0, 0)),            # knee
         ((0.115, 0.03, 0.39), (0.068, 0.066, 0.13), (0, 0, 0)),               # calf
         ((0.112, -0.005, 0.28), (0.046, 0.046, 0.17), (0, 0, 0)),             # shin
         ((0.112, -0.005, 0.085), (0.04, 0.045, 0.05), (0, 0, 0)),             # ankle
         ((0.112, -0.065, 0.035), (0.048, 0.105, 0.032), (0, 0, 0))],          # foot
}


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def toon(name, tones, attr=None, attr_tones=None):
    sh, base, hi = tones
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links; n.clear()
    out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission")
    geo = n.new("ShaderNodeNewGeometry"); dot = n.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = LIGHT; l.new(geo.outputs["Normal"], dot.inputs[0])
    def ramp(t):
        r = n.new("ShaderNodeValToRGB"); r.color_ramp.interpolation = "CONSTANT"; e = r.color_ramp.elements
        e[0].color = HEX(t[0]); e[1].position = 0.12; e[1].color = HEX(t[1])
        h = e.new(0.86); h.color = HEX(t[2]); l.new(dot.outputs["Value"], r.inputs["Fac"]); return r.outputs["Color"]
    col = ramp(tones)
    if attr:
        at = n.new("ShaderNodeAttribute"); at.attribute_name = attr
        mix = n.new("ShaderNodeMix"); mix.data_type = "RGBA"
        l.new(at.outputs["Fac"], mix.inputs[0]); l.new(col, mix.inputs[6]); l.new(ramp(attr_tones), mix.inputs[7])
        col = mix.outputs[2]
    l.new(col, em.inputs["Color"]); l.new(em.outputs[0], out.inputs[0])
    return m


def flat(name, h):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = HEX(h)
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0]); return m


def metaball_mesh(name, elems, voxel=0.0045, smooth=30):
    """union of muscle ellipsoids via voxel remesh, lightly smoothed so junctions become soft valleys"""
    parts = []
    for c, sz, r in elems:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, segments=32, ring_count=16, location=c)
        o = bpy.context.object; o.scale = sz; o.rotation_euler = Euler([math.radians(v) for v in r]); parts.append(o)
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.join(); ob = bpy.context.object; ob.name = name
    rm = ob.modifiers.new("remesh", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = voxel
    sm = ob.modifiers.new("smooth", "SMOOTH"); sm.factor = 0.85; sm.iterations = smooth
    bpy.ops.object.modifier_apply(modifier="remesh"); bpy.ops.object.modifier_apply(modifier="smooth")
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def slice_assign(ob, planes, mats, rule):
    """bisect along planes, then material index per face by rule(center)"""
    bm = bmesh.new(); bm.from_mesh(ob.data)
    for co, no in planes:
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=Vector(co), plane_no=Vector(no).normalized())
    bm.to_mesh(ob.data); bm.free()
    for m in mats:
        ob.data.materials.append(m)
    for p in ob.data.polygons:
        p.material_index = rule(p.center)


def attr(ob, name, fn):
    a = ob.data.attributes.new(name, "FLOAT", "POINT")
    for v in ob.data.vertices:
        a.data[v.index].value = fn(v.co)


def seg(p, a, b):
    a, b = Vector(a), Vector(b); ab = b - a; t = max(0, min(1, (p - a).dot(ab) / ab.length_squared))
    return (p - (a + ab * t)).length


def build_hero():
    skin = toon("skin", C["skin"])
    # head with ears; eyes added after
    head = metaball_mesh("hero_head", BODY["head"]); head.data.materials.append(skin)
    # torso: shirt (with red yoke and side stripes) above the waistband, shorts below
    torso = metaball_mesh("hero_torso", BODY["torso"])
    shirt = toon("shirt", C["shirt"], "red", C["red"]); shorts = toon("shorts", C["shorts"], "red", C["red"])
    band = toon("band", C["shirt"])
    slice_assign(torso, [((0, 0, 1.035), (0, 0, 1)), ((0, 0, 1.06), (0, 0, 1)), ((0, -0.03, 1.535), (0, 0.35, 1))],
                 [skin, shirt, shorts, band],
                 lambda c: 0 if (c.z - 1.535) + 0.35 * (c.y + 0.03) > 0 else (1 if c.z > 1.06 else (3 if c.z > 1.035 else 0)))
    def red(co):
        if co.z <= 1.06:
            return 0.0
        sx = 1 if co.x > 0 else -1
        yoke_f = co.y < 0 and seg(co, (0.075 * sx, -0.06, 1.515), (0.195 * sx, -0.03, 1.425)) < 0.012
        side_f = co.y < 0.02 and seg(co, (0.175 * sx, -0.02, 1.38), (0.13 * sx, -0.07, 1.09)) < 0.011
        yoke_b = co.y > 0 and seg(co, (0.20 * sx, 0.04, 1.46), (0.065 * sx, 0.11, 1.33)) < 0.012
        side_b = co.y > 0 and seg(co, (0.175 * sx, 0.03, 1.36), (0.135 * sx, 0.07, 1.09)) < 0.011
        return 1.0 if (yoke_f or side_f or yoke_b or side_b) else 0.0
    attr(torso, "red", red)
    objs = [head, torso]
    for sd, x in (("L", 1), ("R", -1)):
        a = metaball_mesh(f"hero_arm.{sd}", [((c[0] * x, c[1], c[2]), sz, (r[0], r[1] * x, r[2] * x)) for c, sz, r in BODY["arm"]])
        a.data.materials.append(skin); objs.append(a)
        lg = metaball_mesh(f"hero_leg.{sd}", [((c[0] * x, c[1], c[2]), sz, (r[0], r[1] * x, r[2] * x)) for c, sz, r in BODY["leg"]])
        lg.data.materials.append(skin); objs.append(lg)
        # toes
        for i in range(5):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.016 - 0.0015 * i, location=(x * (0.088 + 0.012 * i), -0.165 + 0.006 * i, 0.017))
            t = bpy.context.object; t.data.materials.append(skin); bpy.ops.object.shade_smooth()
        glove(x)
    loose_shorts(shorts)
    eyes(head)
    face = bpy.data.collections["face_lines_only"]
    for o in list(bpy.data.objects):
        if o.name.startswith(("hero_head", "hero_eye")):
            for c in list(o.users_collection):
                c.objects.unlink(o)
            face.objects.link(o)
    return objs


def loose_shorts(mat):
    """boxy fight shorts: straight legs from the waistband to just above the knee, red notch at the outer hem"""
    parts = []
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.0, 0.965)); b = bpy.context.object; b.scale = (0.36, 0.25, 0.17); parts.append(b)
    for x in (1, -1):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.125, depth=0.36, location=(0.112 * x, -0.005, 0.80), vertices=40)
        c = bpy.context.object; c.rotation_euler = (0, math.radians(3 * x), 0); parts.append(c)
    bpy.ops.object.select_all(action="DESELECT")
    for o in parts:
        o.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True); bpy.ops.object.join()
    sh = bpy.context.object; sh.name = "hero_shorts"
    rm = sh.modifiers.new("r", "REMESH"); rm.mode = "VOXEL"; rm.voxel_size = 0.006
    sm = sh.modifiers.new("s", "SMOOTH"); sm.factor = 0.7; sm.iterations = 6
    bpy.ops.object.modifier_apply(modifier="r"); bpy.ops.object.modifier_apply(modifier="s")
    bm = bmesh.new(); bm.from_mesh(sh.data)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 1.045), plane_no=(0, 0, 1), clear_outer=True)
    bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0.635), plane_no=(0, 0, -1), clear_outer=True)
    bm.to_mesh(sh.data); bm.free()
    sh.data.materials.append(mat)
    def notch(co):
        if abs(co.x) < 0.165 or co.z > 0.78:
            return 0.0
        h = co.z - 0.635; w = 0.085 * (1 - h / 0.14)
        return 1.0 if w - 0.016 < abs(co.y + 0.0) < w + 0.004 else 0.0
    attr(sh, "red", notch)
    for p in sh.data.polygons:
        p.use_smooth = True


def glove(x):
    gm = toon("glove", C["glove"]); rm = toon("strap", C["red"])
    c = Vector((0.282 * x, -0.012, 0.865))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=c); g = bpy.context.object
    g.scale = (0.052, 0.058, 0.065); g.data.materials.append(gm); bpy.ops.object.shade_smooth()
    for i in range(4):  # finger segments across the front of the fist
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=c + Vector((0.006 * x, -0.045, 0.03 - 0.02 * i)))
        f = bpy.context.object; f.scale = (0.04, 0.022, 0.0115); f.data.materials.append(gm); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=c + Vector((-0.03 * x, -0.035, 0.02)))
    th = bpy.context.object; th.scale = (0.016, 0.03, 0.022); th.data.materials.append(gm); bpy.ops.object.shade_smooth()
    for z, mat, r in ((0.935, rm, 0.05), (0.91, gm, 0.052)):  # red strap and black cuff
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.03, location=(0.28 * x, -0.005, z), vertices=32)
        s = bpy.context.object; s.data.materials.append(mat); bpy.ops.object.shade_smooth()


def eyes(head):
    """slanted leaf shaped white eyes placed ON the face by ray casting (faceless: nothing else on the face)"""
    em = flat("eye", C["eye"]); inv = head.matrix_world.inverted()
    for x in (1, -1):
        org = Vector((0.042 * x, -0.4, 1.718)); ok, loc, nor, _ = head.ray_cast(inv @ org, Vector((0, 1, 0)))
        if not ok:
            continue
        loc = head.matrix_world @ loc; nor = (head.matrix_world.to_3x3() @ nor).normalized()
        bm = bmesh.new(); pts = []
        for i in range(32):
            t = i * 2 * math.pi / 32; px = math.cos(t) * 0.033
            pz = math.sin(t) * (0.012 if math.sin(t) > 0 else 0.006)
            pts.append(bm.verts.new((px, pz, 0)))
        bm.faces.new(pts); me = bpy.data.meshes.new("eye"); bm.to_mesh(me); bm.free()
        e = bpy.data.objects.new(f"hero_eye{x}", me); bpy.context.collection.objects.link(e)
        e.rotation_mode = "QUATERNION"
        q = nor.to_track_quat("Z", "Y"); tilt = Euler((0, 0, math.radians(-17 * x))).to_quaternion()
        e.rotation_quaternion = q @ tilt; e.location = loc + nor * 0.0025
        sw = e.modifiers.new("wrap", "SHRINKWRAP"); sw.target = head; sw.offset = 0.0025
        me.materials.append(em)


def scene(bg):
    s = bpy.context.scene
    s.render.engine = "CYCLES"; s.cycles.samples = 16; s.cycles.device = "CPU"
    s.render.resolution_x, s.render.resolution_y = 700, 1080
    s.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("bg"); s.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = HEX(bg)
    s.render.use_freestyle = True; s.render.line_thickness_mode = "ABSOLUTE"
    fs = s.view_layers[0].freestyle_settings
    fs.use_ridges_and_valleys = False; fs.crease_angle = math.radians(140)
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("ink")
    ls.select_by_visibility = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
    ls.select_ridge_valley = False; ls.select_material_boundary = True; ls.select_external_contour = True
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("ink")
    ls.linestyle.color = (0.01, 0.01, 0.015); ls.linestyle.thickness = 2.2
    ls.select_by_collection = True; ls.collection_negation = "EXCLUSIVE"
    face = bpy.data.collections.new("face_lines_only"); bpy.context.scene.collection.children.link(face)
    ls.collection = face
    l2 = fs.linesets.new("face_ink"); l2.select_by_visibility = True; l2.select_silhouette = True; l2.select_border = True
    l2.select_crease = False; l2.select_ridge_valley = False; l2.select_external_contour = True
    l2.select_by_collection = True; l2.collection = face; l2.linestyle = ls.linestyle
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); bpy.context.collection.objects.link(cam)
    cam.data.type = "ORTHO"; cam.data.ortho_scale = 1.95; s.camera = cam
    return s, cam


VIEWS = {"front": 0, "right": -90, "left": 90, "back": 180, "threequarter": 35}

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    reset(); s, cam = scene(C["bg"]); build_hero()
    for name, az in VIEWS.items():
        a = math.radians(az); d = Vector((math.sin(a), -math.cos(a), 0.0))
        cam.location = Vector((0, 0, 0.93)) + d * 8; cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        s.render.filepath = os.path.join(out, f"hero_{name}.png"); bpy.ops.render.render(write_still=True)
        print("rendered", name)
    if "--save-blend" in sys.argv:
        bpy.ops.wm.save_as_mainfile(filepath=sys.argv[sys.argv.index("--save-blend") + 1])
