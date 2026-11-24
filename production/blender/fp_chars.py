"""The Fight Playbook characters rendered directly in Blender (no generative model anywhere).

Rig: a parametric skeleton (fp_rig.Pose) solved with exact two bone IK (glove, elbow hint, foot, knee hint),
skinned with a Skin modifier using muscle shaped radii, toon materials (fixed light, two tones, emission so the
palette is exact), Freestyle ink outlines, orthographic cameras, flat background.
Run: python3 fp_chars.py <shot> [--out DIR] [--save-blend PATH]
"""
import math, sys, os
import bpy
from mathutils import Vector, Matrix

HEX = lambda h: tuple((int(h[i:i + 2], 16) / 255) ** 2.2 for i in (1, 3, 5)) + (1,)
BG = "#C4D6C4"
PAL = {
    "hero": {"skin": "#45464c", "skin_sh": "#2a2b30", "shirt": "#17171a", "shirt_sh": "#0b0b0d", "stripe": "#d1202f",
             "shorts": "#22305a", "shorts_sh": "#162040", "trim": "#d1202f", "glove": "#18181b", "glove_sh": "#09090a",
             "strap": "#d1202f", "scale": 1.0},
    "opp": {"skin": "#47484e", "skin_sh": "#2c2d32", "shirt": "#d3212c", "shirt_sh": "#9c1620", "stripe": None,
            "shorts": "#18181b", "shorts_sh": "#0d0d0f", "trim": None, "glove": "#18181b", "glove_sh": "#09090a",
            "strap": "#18181b", "scale": 1.08},
}
LIGHT = Vector((-0.5, -0.6, 0.62)).normalized()
UP = Vector((0, 0, 1))

# segment lengths (metres, scale 1)
L_UP, L_FORE, L_GLOVE = 0.30, 0.25, 0.07
L_THIGH, L_SHIN = 0.38, 0.38

# skin radii (x across, y depth) per joint kind, muscular comic build
R = {"pelvis": (0.18, 0.135), "waist": (0.17, 0.125), "chest": (0.27, 0.16), "neck": (0.088, 0.085),
     "head": (0.07, 0.075), "skull": (0.108, 0.118), "crown": (0.07, 0.075), "clav": (0.13, 0.11), "sh": (0.13, 0.12),
     "bic": (0.09, 0.088), "el": (0.06, 0.06), "farm": (0.074, 0.066), "wr": (0.043, 0.04), "hip": (0.115, 0.115),
     "quad": (0.125, 0.125), "kn": (0.072, 0.072), "calf": (0.088, 0.088), "an": (0.045, 0.045), "toe": (0.038, 0.03)}


def two_bone(a, b, la, lb, hint):
    """exact two bone IK: joint position between a and target b, bent toward hint"""
    d = b - a; dist = min(d.length, (la + lb) * 0.999); dn = d.normalized()
    x = (la * la - lb * lb + dist * dist) / (2 * dist); h = math.sqrt(max(la * la - x * x, 0))
    side = (hint - a) - dn * (hint - a).dot(dn)
    side = side.normalized() if side.length > 1e-6 else dn.orthogonal().normalized()
    return a + dn * x + side * h, a + dn * dist


class Pose:
    """posed skeleton of one character. All inputs in world space except body params."""

    def __init__(self, kind, root, face_deg, drop=0.0, twist=0.0, lean=0.0, head_turn=0.0):
        self.kind = kind; s = self.s = PAL[kind]["scale"]
        f = Vector((math.cos(math.radians(face_deg)), math.sin(math.radians(face_deg)), 0))
        self.f, self.l = f, UP.cross(f)  # facing, character's left
        self.root = Vector(root)
        tw = Matrix.Rotation(math.radians(twist), 3, UP)           # + twist turns the shoulders to the character's left
        ft, lt = tw @ f, tw @ self.l
        lean_v = ft * math.sin(math.radians(lean))
        self.J = J = {}
        J["pelvis"] = self.root + UP * (0.92 - drop) * s
        J["waist"] = J["pelvis"] + (UP * 0.17 + lean_v * 0.10) * s
        J["chest"] = J["waist"] + (UP * 0.21 + lean_v * 0.16) * s
        J["neck"] = J["chest"] + (UP * 0.18 + lean_v * 0.12 + ft * 0.02) * s
        J["head"] = J["neck"] + (UP * 0.06 + ft * 0.01) * s
        J["skull"] = J["head"] + (UP * 0.10 + ft * 0.012) * s
        J["crown"] = J["skull"] + UP * 0.07 * s
        self.ft, self.lt = ft, lt
        hf = Matrix.Rotation(math.radians(head_turn), 3, UP) @ ft
        self.head_f = hf
        for side, x in (("L", 1), ("R", -1)):
            J[f"clav.{side}"] = J["chest"] + (lt * 0.10 * x + UP * 0.10) * s
            J[f"sh.{side}"] = J["chest"] + (lt * 0.21 * x + UP * 0.09) * s
            J[f"hip.{side}"] = J["pelvis"] + (self.l * 0.10 * x - UP * 0.03) * s

    def arm(self, side, glove, elbow_hint):
        s = self.s; sh = self.J[f"sh.{side}"]
        el, g = two_bone(sh, Vector(glove), L_UP * s, (L_FORE + L_GLOVE) * s, Vector(elbow_hint))
        wr = el + (g - el).normalized() * L_FORE * s
        self.J[f"el.{side}"], self.J[f"wr.{side}"], self.J[f"glove.{side}"] = el, wr, g
        self.J[f"bic.{side}"] = sh.lerp(el, 0.5); self.J[f"farm.{side}"] = el.lerp(wr, 0.4)
        return self

    def leg(self, side, foot, knee_hint):
        s = self.s; hip = self.J[f"hip.{side}"]
        an_target = Vector(foot) + UP * 0.085 * s
        kn, an = two_bone(hip, an_target, L_THIGH * s, L_SHIN * s, Vector(knee_hint))
        self.J[f"kn.{side}"], self.J[f"an.{side}"] = kn, an
        self.J[f"toe.{side}"] = Vector(foot) + self.f * 0.15 * s + UP * 0.03 * s
        self.J[f"quad.{side}"] = hip.lerp(kn, 0.45); self.J[f"calf.{side}"] = kn.lerp(an, 0.35)
        return self

    # convenience: body local point -> world
    def W(self, fwd, left, up):
        return self.root + (self.f * fwd + self.l * left + UP * up) * self.s

    def stance(self, lead=0.30, width=0.17, knee=0.25):
        """orthodox: LEFT foot leads"""
        self.leg("L", self.W(lead, width * 0.6, 0), self.W(lead + knee + 0.6, width * 0.8, 0.5))
        self.leg("R", self.W(-lead * 0.8, -width, 0), self.W(-lead * 0.8 + knee + 0.6, -width * 1.2, 0.5))
        return self

    def guard(self, sides="LR"):
        for side, x in (("L", 1), ("R", -1)):
            if side in sides:
                g = self.J["skull"] + (self.ft * 0.17 + self.lt * 0.075 * x - UP * 0.02) * self.s
                self.arm(side, g, self.J[f"sh.{side}"] + (self.lt * 0.12 * x - UP * 0.35 - self.ft * 0.05) * self.s)
        return self

    # skeleton graph for the skin modifier
    def graph(self):
        e = [("pelvis", "waist"), ("waist", "chest"), ("chest", "neck"), ("neck", "head"), ("head", "skull"), ("skull", "crown")]
        for s in "LR":
            e += [("chest", f"clav.{s}"), (f"clav.{s}", f"sh.{s}"), (f"sh.{s}", f"bic.{s}"), (f"bic.{s}", f"el.{s}"),
                  (f"el.{s}", f"farm.{s}"), (f"farm.{s}", f"wr.{s}"), ("pelvis", f"hip.{s}"), (f"hip.{s}", f"quad.{s}"),
                  (f"quad.{s}", f"kn.{s}"), (f"kn.{s}", f"calf.{s}"), (f"calf.{s}", f"an.{s}"), (f"an.{s}", f"toe.{s}")]
        return e


def kind_of(name):
    return name.split(".")[0]


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def toon(name, base, shade, extra=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links; n.clear()
    out = n.new("ShaderNodeOutputMaterial"); em = n.new("ShaderNodeEmission")
    geo = n.new("ShaderNodeNewGeometry"); dot = n.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = LIGHT
    ramp = n.new("ShaderNodeValToRGB"); ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].color = HEX(shade); ramp.color_ramp.elements[1].position = 0.05
    ramp.color_ramp.elements[1].color = HEX(base)
    l.new(geo.outputs["Normal"], dot.inputs[0]); l.new(dot.outputs["Value"], ramp.inputs["Fac"])
    col = ramp.outputs["Color"]
    if extra:
        at = n.new("ShaderNodeAttribute"); at.attribute_name = "stripe"
        mix = n.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.inputs[7].default_value = HEX(extra)
        l.new(at.outputs["Fac"], mix.inputs[0]); l.new(col, mix.inputs[6]); col = mix.outputs[2]
    l.new(col, em.inputs["Color"]); l.new(em.outputs[0], out.inputs[0])
    return m


def flat(name, hexcol):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = HEX(hexcol)
    o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], o.inputs[0])
    return m


def seg_dist(p, a, b):
    ab = b - a; t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9)))
    return (p - (a + ab * t)).length, t


def build(pose):
    """mesh + clothing regions + gloves + eyes + armature for one posed character"""
    P = PAL[pose.kind]; s = pose.s; J = pose.J; kind = pose.kind
    names = [k for k in J if not k.startswith("glove")]
    edges = pose.graph()
    me = bpy.data.meshes.new(kind + "_body")
    me.from_pydata([J[k] for k in names], [(names.index(a), names.index(b)) for a, b in edges], [])
    ob = bpy.data.objects.new(kind + "_body", me); bpy.context.collection.objects.link(ob)
    ob.modifiers.new("skin", "SKIN").use_smooth_shade = True
    for i, k in enumerate(names):
        rx, ry = R[k.split(".")[0]]
        ob.data.skin_vertices[0].data[i].radius = (rx * s, ry * s)
    ob.data.skin_vertices[0].data[names.index("pelvis")].use_root = True
    ob.modifiers.new("sub", "SUBSURF").levels = 2
    bpy.context.view_layer.objects.active = ob
    for md in list(ob.modifiers):
        bpy.ops.object.modifier_apply(modifier=md.name)
    apply_clothing(ob, pose, [toon(kind + "_skin", P["skin"], P["skin_sh"]),
                              toon(kind + "_shirt", P["shirt"], P["shirt_sh"], P["stripe"]),
                              toon(kind + "_shorts", P["shorts"], P["shorts_sh"], P["trim"])])
    # gloves and straps
    gm = toon(kind + "_glove", P["glove"], P["glove_sh"]); sm = toon(kind + "_strap", P["strap"], P["strap"])
    for sd in "LR":
        g, wr, el = J[f"glove.{sd}"], J[f"wr.{sd}"], J[f"el.{sd}"]
        axis = (g - el).normalized(); q = axis.to_track_quat("X", "Z")
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.066 * s, segments=24, ring_count=16, location=g)
        gl = bpy.context.object; gl.name = f"{kind}_glove.{sd}"; gl.rotation_mode = "QUATERNION"; gl.rotation_quaternion = q
        gl.scale = (1.2, 0.95, 1.0); gl.data.materials.append(gm); bpy.ops.object.shade_smooth()
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05 * s, depth=0.05 * s, vertices=24, location=wr + axis * 0.015 * s)
        st = bpy.context.object; st.name = f"{kind}_strap.{sd}"; st.rotation_mode = "QUATERNION"
        st.rotation_quaternion = axis.to_track_quat("Z", "Y"); st.data.materials.append(sm)
    # faceless head: two slanted white eyes on the face side
    em = flat(kind + "_eye", "#ffffff"); hf = pose.head_f; hl = UP.cross(hf)
    for x in (1, -1):
        bpy.ops.mesh.primitive_circle_add(vertices=24, radius=0.036 * s, fill_type="NGON")
        e = bpy.context.object; e.name = f"{kind}_eye{x}"
        e.scale = (1.0, 0.40, 1.0)
        pos = J["skull"] + (hf * 0.112 + hl * 0.042 * x - UP * 0.005) * s
        e.location = pos
        e.rotation_mode = "QUATERNION"
        e.rotation_quaternion = hf.to_track_quat("Z", "Y") @ Matrix.Rotation(math.radians(18 * x), 4, "Z").to_quaternion()
        e.data.materials.append(em)
    # armature matching the posed skeleton (reusable rig for animation export)
    ad = bpy.data.armatures.new(kind + "_rig"); arm = bpy.data.objects.new(kind + "_rig", ad)
    bpy.context.collection.objects.link(arm); bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for a, b in edges:
        eb = ad.edit_bones.new(f"{a}>{b}"); eb.head, eb.tail = J[a], J[b]
    bpy.ops.object.mode_set(mode="OBJECT")
    arm.hide_render = True
    return ob


def apply_clothing(ob, pose, mats):
    """slice the body along exact garment planes (no deletion), then assign skin / shirt / shorts per face"""
    import bmesh
    J, s = pose.J, pose.s
    tax = (J["chest"] - J["pelvis"]).normalized()
    hem = (J["pelvis"].lerp(J["waist"], 0.55), tax)                 # shirt hem, shorts waistband just below
    band = (J["pelvis"].lerp(J["waist"], 0.50), tax)
    neck = (J["chest"].lerp(J["neck"], 0.45), tax)
    arm = {sd: (J["chest"].lerp(J[f"sh.{sd}"], 0.70), (J[f"sh.{sd}"] - J["chest"]).normalized()) for sd in "LR"}
    leg = {sd: (J[f"hip.{sd}"].lerp(J[f"kn.{sd}"], 0.52), (J[f"kn.{sd}"] - J[f"hip.{sd}"]).normalized()) for sd in "LR"}
    bm = bmesh.new(); bm.from_mesh(ob.data)
    for co, no in [hem, band, neck, arm["L"], arm["R"], leg["L"], leg["R"]]:
        bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no)
    bm.to_mesh(ob.data); bm.free()
    for m in mats:
        ob.data.materials.append(m)
    edges = pose.graph()
    armsegs = {e for e in edges if any(k.split(".")[0] in ("bic", "el", "farm", "wr") for k in e)}
    side = lambda c, pl: (c - pl[0]).dot(pl[1])
    for p in ob.data.polygons:
        c = p.center
        seg = min(edges, key=lambda e: seg_dist(c, J[e[0]], J[e[1]])[0])
        if seg in armsegs:
            continue
        if side(c, hem) > 0 and side(c, neck) < 0 and side(c, arm["L"]) < 0 and side(c, arm["R"]) < 0:
            p.material_index = 1
        elif side(c, band) < 0 and side(c, leg["L"]) < 0 and side(c, leg["R"]) < 0 and not seg[0].startswith(("kn", "calf", "an")):
            p.material_index = 2
    at = ob.data.attributes.new("stripe", "FLOAT", "POINT"); P = PAL[pose.kind]
    for v in ob.data.vertices:
        val = 0.0
        if P["stripe"]:
            lat = abs((v.co - J["chest"]).dot(pose.lt)) / s; fr = (v.co - J["chest"]).dot(pose.ft) / s
            if 0.17 < lat < 0.26 and abs(fr) < 0.05 and side(v.co, hem) > 0 and side(v.co, neck) < 0:
                val = 1.0
        if P["trim"]:
            for sd in "LR":
                h = side(v.co, leg[sd])
                if -0.03 * s < h <= 0.002 and seg_dist(v.co, J[f"hip.{sd}"], J[f"kn.{sd}"])[0] < 0.2 * s:
                    val = 1.0
        at.data[v.index].value = val


def scene(width=1920, height=1080):
    s = bpy.context.scene
    s.render.engine = "CYCLES"; s.cycles.samples = 24; s.cycles.device = "CPU"
    s.render.resolution_x, s.render.resolution_y = width, height
    s.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("bg"); s.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = HEX(BG)
    s.render.use_freestyle = True; s.render.line_thickness_mode = "ABSOLUTE"
    fs = s.view_layers[0].freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new("ink")
    ls.select_by_visibility = True; ls.select_silhouette = True; ls.select_border = True; ls.select_crease = False
    ls.select_material_boundary = True; ls.select_external_contour = True
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("ink")
    ls.linestyle.color = (0.02, 0.02, 0.03); ls.linestyle.thickness = 3.0
    gm = flat("ground", "#aabfaa")
    bpy.ops.mesh.primitive_circle_add(vertices=48, radius=1, fill_type="NGON", location=(0, 0, 0.001))
    sh = bpy.context.object; sh.name = "shadow"; sh.scale = (0.85, 0.26, 1); sh.data.materials.append(gm)
    return s


def camera(target, az_deg, el_deg, ortho, dist=12):
    a, e = math.radians(az_deg), math.radians(el_deg)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); bpy.context.collection.objects.link(cam)
    cam.data.type = "ORTHO"; cam.data.ortho_scale = ortho
    cam.location = Vector(target) + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


# ---------------- shots (previously failed liver combat beats) ----------------
def fighters(gap):
    """opponent on screen LEFT facing +X (his right side, the liver, toward the camera at -Y);
    hero on screen RIGHT facing -X (his left side toward the camera)"""
    opp = Pose("opp", (-gap / 2, 0, 0), 0, twist=-8)
    return opp


def place_for_angle(make, side, target, angle_deg=90, iters=12):
    """move the hero along his facing direction until the punch at target has the wanted elbow angle"""
    s = PAL["hero"]["scale"]; a, b = L_UP * s, (L_FORE + L_GLOVE) * s
    want = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(angle_deg)))
    x = 0.0
    for _ in range(iters):
        h = make(x); d = (h.J[f"sh.{side}"] - target).length
        x += (d - want)
    return make(x)


def liver(opp, out=0.0):
    # opponent's RIGHT lower ribs: right = -l
    return opp.J["waist"] + (-opp.lt * 0.15 + opp.ft * 0.05 - UP * 0.03) * opp.s - opp.lt * out


def shot_hook(close=False):
    """V3 / V94 class: LEFT hook to the opponent's RIGHT side: 90 degree L, elbow at glove height, glove on top."""
    opp = Pose("opp", (-0.42, 0, 0), 0, twist=-10).stance(0.26).guard()
    tgt = liver(opp, 0.075)                                               # glove centre just outside the shirt
    hero = place_for_angle(lambda x: Pose("hero", (0.40 - x, 0, 0), 180, drop=0.14, twist=-28, lean=12, head_turn=40), "L", tgt, 92)
    hero.stance(0.30, 0.18)
    sh = hero.J["sh.L"]
    hero.arm("L", tgt, Vector((sh.x + 0.05, sh.y - 0.6, tgt.z + 0.03)))   # elbow out toward the camera side, level
    hero.guard("R")
    build(opp); build(hero)
    if close:
        camera(tgt + Vector((0.05, 0, 0.1)), -28, 22, 1.45)
    else:
        camera(Vector((0, 0, 1.02)), -32, 24, 3.6)
    return hero, opp


def shot_shovel(close=False):
    """V24 / V71 class: RIGHT shovel: elbow at the own hip, forearm near vertical, glove under the lower right ribs."""
    opp = Pose("opp", (-0.36, 0, 0), 0, twist=-6).stance(0.26).guard()
    tgt = opp.J["waist"] + (-opp.lt * 0.06 + opp.ft * 0.17 - UP * 0.02) * opp.s
    hero = place_for_angle(lambda x: Pose("hero", (0.34 - x, 0, 0), 180, drop=0.15, twist=18, lean=12), "R", tgt, 80)
    hero.stance(0.28, 0.18)
    hip = hero.J["hip.R"]
    hero.arm("R", tgt, hip + Vector((0.12, 0.10, -0.05)))
    hero.guard("L")
    build(opp); build(hero)
    if close:
        camera(tgt + Vector((0.08, 0, 0.05)), 25, -6, 1.2)
    else:
        camera(Vector((0, 0, 1.0)), 28, 4, 3.5)
    return hero, opp


SHOTS = {"hook_wide": lambda: shot_hook(), "hook_close": lambda: shot_hook(True),
         "shovel_med": lambda: shot_shovel(), "shovel_close": lambda: shot_shovel(True)}

if __name__ == "__main__":
    shot = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "/tmp"
    reset(); s = scene()
    hero, opp = SHOTS[shot]()
    s.render.filepath = os.path.join(out, f"{shot}.png")
    bpy.ops.render.render(write_still=True)
    if "--save-blend" in sys.argv:
        bpy.ops.wm.save_as_mainfile(filepath=sys.argv[sys.argv.index("--save-blend") + 1])
    el = hero.J.get("el.L") if "hook" in shot else hero.J.get("el.R")
    side = "L" if "hook" in shot else "R"
    a = (hero.J[f"sh.{side}"] - el).angle(hero.J[f"glove.{side}"] - el)
    print("rendered", s.render.filepath, "elbow angle", round(math.degrees(a)), "elbow z", round(el.z, 3), "glove z", round(hero.J[f'glove.{side}'].z, 3))
