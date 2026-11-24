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
REGION = {  # target name -> weight (heroic comic build, reference sheet)
    "measure-shoulder-dist-incr": 0.9, "torso-muscle-pectoral-incr": 0.8, "torso-muscle-dorsi-incr": 1.0,
    "measure-waist-circ-decr": 0.6, "measure-hips-circ-decr": 0.3, "torso-scale-horiz-incr": 0.35,
    "l-upperarm-muscle-incr": 1.0, "r-upperarm-muscle-incr": 1.0, "l-lowerarm-muscle-incr": 1.0, "r-lowerarm-muscle-incr": 1.0,
    "l-upperarm-shoulder-muscle-incr": 1.0, "r-upperarm-shoulder-muscle-incr": 1.0,
    "l-upperleg-muscle-incr": 1.0, "r-upperleg-muscle-incr": 1.0, "l-lowerleg-muscle-incr": 1.0, "r-lowerleg-muscle-incr": 1.0,
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


def a_pose(rig, deg=28):
    """lower both arms toward the reference stance using the professional rig (skin weights, no tearing)"""
    from mathutils import Matrix
    bpy.context.view_layer.objects.active = rig; bpy.ops.object.mode_set(mode="POSE")
    for side, sgn in (("L", 1), ("R", -1)):
        pb = rig.pose.bones[f"upperarm01.{side}"]; h = pb.head.copy()
        R = Matrix.Translation(h) @ Matrix.Rotation(math.radians(deg) * sgn, 4, "Y") @ Matrix.Translation(-h)
        pb.matrix = R @ pb.matrix
        bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode="OBJECT")


def outline(ob, thick=0.006):
    """inverted hull ink outline: solidify with flipped normals and a black back face material"""
    ink = bpy.data.materials.new("ink"); ink.use_nodes = True; nt = ink.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.008, 0.008, 0.01, 1)
    geo = nt.nodes.new("ShaderNodeNewGeometry"); tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader"); o = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(geo.outputs["Backfacing"], mix.inputs[0]); nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2]); nt.links.new(mix.outputs[0], o.inputs[0])
    ob.data.materials.append(ink)
    sol = ob.modifiers.new("ink_hull", "SOLIDIFY"); sol.thickness = thick; sol.offset = 1.0
    sol.use_flip_normals = True; sol.material_offset = len(ob.data.materials) - 1; sol.use_rim = False


if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    HM.reset()
    addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
    s, cam = HM.scene(HM.C["bg"])
    body = build_body()
    body.data.materials.clear(); body.data.materials.append(HM.toon("skin", HM.C["skin"]))
    rig = HumanService.add_builtin_rig(body, "default")
    if "--info" in sys.argv:
        print("BONES", [b.name for b in rig.data.bones][:80])
    a_pose(rig)
    outline(body)
    dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg)
    zs = [(body.matrix_world @ v.co).z for v in ev.to_mesh().vertices]; zmax, zmin = max(zs), min(zs); ev.to_mesh_clear()
    print("height", round(zmax - zmin, 3))
    for name, az in HM.VIEWS.items():
        a = math.radians(az); d = Vector((math.sin(a), -math.cos(a), 0.0))
        cam.data.ortho_scale = (zmax - zmin) * 1.12
        cam.location = Vector((0, 0, (zmax + zmin) / 2)) + d * 8; cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
        s.render.filepath = os.path.join(out, f"body_{name}.png"); bpy.ops.render.render(write_still=True)
    if "--save-blend" in sys.argv:
        bpy.ops.wm.save_as_mainfile(filepath=sys.argv[sys.argv.index("--save-blend") + 1])
    print("done")
