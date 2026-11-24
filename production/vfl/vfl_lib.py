"""Visual Failure Library (VFL): shared core.

The registry lives in Sean's private vault (Claude Production/Visual Failure Library/registry.json) and is the
single source of truth for every documented visual defect. Evidence images sit next to it. This module holds the
taxonomy, registry I/O, image normalisation and the perceptual hash used to recognise known defective images.

No credentials live here. Writes only inside the vault's Claude Production folder.
"""
import hashlib, io, json, os, time
from pathlib import Path

VAULT = Path(os.environ.get("FP_VAULT", "/home/user/the-fight-playbook-brain"))
LIB = Path(os.environ.get("FP_VFL", str(Path(__file__).resolve().parents[2] / "memory" / "visual-failures")))
REG = LIB / "registry.json"
EVID = LIB / "evidence"
STATE = Path(os.environ.get("FP_VFL_STATE", str(Path.home() / ".fp_vfl")))  # session local acks

CATEGORIES = {
    "A": "Anatomy (missing heads, extra or disfigured limbs)",
    "B": "Strike and movement mechanics",
    "C": "Positioning and orientation",
    "D": "Floating or disconnected parts",
    "E": "Character design consistency",
    "F": "Impact physics and contact",
    "G": "Camera framing and cropping",
    "H": "Animation, transition and compositing",
    "I": "Narration, caption and text accuracy",
}

# Defect classes. severity: critical = never ships; major = never ships unless Sean waives; minor = fix before delivery.
# auto: ids of automated screeners in checks.py that can flag the class (never sufficient to approve).
CLASSES = {
 # A anatomy
 "VFC-A01": ("A", "critical", "Extra limb, hand, glove or wrist",
   "A character has more than two arms, hands, gloves or wrists (third glove, three hands, a cuff with no arm).",
   "Count arms, hands, gloves and wrists per character on every still and every animation frame; exactly two of each.",
   ["pose_person_count"]),
 "VFC-A02": ("A", "critical", "Missing head or missing body part",
   "A body part that must be visible is absent: no head on a body, a limb that ends in nothing, a torso replaced by a shapeless mass.",
   "Every visible arm must trace to a shoulder, a torso and a head inside the frame or leave through the bottom or a corner. A limb attached to a shapeless blob fails.",
   ["pose_person_count"]),
 "VFC-A03": ("A", "critical", "Distorted, kinked or rubbery limb",
   "Limbs bend in more than one place, sag, stretch, snake, or have unequal upper arm and forearm lengths.",
   "Zoomed crop of every arm: one bend at the elbow only, segments of similar length, no stretch or snake shapes.",
   []),
 "VFC-A04": ("A", "critical", "Impossible joint or reversed limb",
   "A joint bends the wrong way or a limb is mirrored (a right arm drawn as a left arm, thumb on the wrong side, twisted elbow, bent wrist at the glove).",
   "Check which shoulder each arm leaves from and the thumb side; wrists straight behind the glove.",
   []),
 "VFC-A05": ("A", "major", "Fingered glove or bare fist instead of a padded glove",
   "A glove drawn with separate fingers like a bare fist, or bare hands where gloves are locked.",
   "Every glove is padded with no separate fingers (bare hands only in a grip tutorial).",
   []),
 "VFC-A06": ("A", "critical", "Bodies merged or limbs tangled",
   "Two characters' limbs, heads or torsos merge or tangle so ownership of a limb is unclear; guards intersect at pocket range.",
   "For every limb, name its owner. Any limb whose owner is unclear fails. Keep a visible gap between torsos.",
   ["pose_person_count"]),
 "VFC-A07": ("A", "major", "Disproportion or lens distortion",
   "Oversized deltoid or feet, fisheye giant feet, limbs or body parts out of scale with the character sheet.",
   "Compare proportions with the reference sheet; no body part more than about 1.3x its reference size relative to the head.",
   []),
 # B mechanics
 "VFC-B01": ("B", "critical", "Hook drawn as a straight or open arm",
   "A hook with an elbow of 120 to 180 degrees that reads as a jab or body jab instead of a 90 degree L.",
   "Hooks: elbow about 90 degrees (fail outside 70 to 110), forearm level, elbow at glove height (hook_rules.md).",
   ["pose_elbow_angle"]),
 "VFC-B02": ("B", "critical", "Hook elbow height or forearm angle wrong",
   "Hook elbow above or below the glove, forearm sloping, upper arm vertical with a low elbow.",
   "Elbow level with the glove, forearm level; check in a zoomed crop.",
   ["pose_elbow_angle"]),
 "VFC-B03": ("B", "critical", "Uppercut or shovel with the elbow off the hip",
   "Shovel or uppercut drawn as a long reaching arm, horizontal punch or diagonal forearm with the elbow away from the hip.",
   "Uppercuts and shovels: elbow at the own hip, forearm 70 to 85 degrees from horizontal, glove rising under the ribs or chin.",
   ["pose_elbow_angle"]),
 "VFC-B04": ("B", "critical", "Straight punch kinked, sagging or overlong",
   "A jab or cross with a kinked elbow, a sagging forearm, or an arm longer than the body allows.",
   "Straight punches: shoulder, elbow and glove in one line, elbow at least 160 degrees, arm length matches the other arm.",
   ["pose_elbow_angle"]),
 "VFC-B05": ("B", "major", "Guard hand dropped or elbows flared",
   "The non punching hand is off the chin, a guard glove sits at the hip, or guard elbows flare to shoulder height.",
   "Non punching glove at the chin or cheek; guard elbows on the ribs (at least 0.45 x torso below the shoulder in the rig).",
   ["rig_guard_elbow"]),
 "VFC-B06": ("B", "critical", "Wrong technique drawn",
   "The picture shows a different technique from the one named: knee strike instead of a punch, cross instead of a jab, straight instead of a hook, idle guard.",
   "Name the technique in the picture before reading the spec; it must match the spec and narration.",
   []),
 "VFC-B07": ("B", "critical", "Kick or leg mechanics wrong",
   "Knee against knee instead of shin, both feet off the ground with no planted leg, a shin passing through a leg, knee landing in the groin.",
   "Kicks and checks: shin meets shin, one planted foot, no leg passes through another, knees land on the stomach or ribs.",
   []),
 "VFC-B08": ("B", "major", "Motion phases wrong or kinetic chain missing",
   "Chamber, impact and recover frames are taken at the wrong moments, the glove starts at the target, the arm retracts on a different path or never returns to guard.",
   "Chamber shows the glove at the guard, impact at full technique, recover back at the guard; check every in between frame, not only key poses.",
   ["rig_phases"]),
 "VFC-B09": ("B", "major", "Implausible reaction or impossible pose",
   "Reactions no fighter would make (both hands thrown overhead from a jab), impossible crouches or poses.",
   "Ask: would this happen in a real exchange? If not, regenerate.",
   []),
 # C orientation
 "VFC-C01": ("C", "critical", "Wrong arm for the named punch",
   "Right arm on a left hook, rear hand on a jab, opponent's wrong hand.",
   "Name the punching arm by owner and image side before checking anything else (hook_rules.md screen side table).",
   []),
 "VFC-C02": ("C", "major", "Screen side swap without a motivated transition",
   "Fighters swap screen sides between consecutive shots, breaking the 180 degree rule.",
   "Plan screen sides for the whole video; a side change needs a whip pan or a hard cut inside a montage (C14).",
   []),
 "VFC-C03": ("C", "critical", "Target on the wrong side of the body",
   "A liver shot landing on the spleen side, a target glow or label on the wrong side.",
   "Orthodox liver = opponent's RIGHT side; check image side for every liver contact and target graphic.",
   []),
 "VFC-C04": ("C", "critical", "Wrong character performs the action",
   "The opponent checks the kick when the narration says the hero does, the partner swaps roles.",
   "Confirm who acts in the narration and who acts in the picture.",
   []),
 "VFC-C05": ("C", "critical", "Head or face orientation impossible",
   "Eyes drawn on the back of a head seen from behind, a face turned the wrong way for the body.",
   "Check that the eyes sit on the side of the head that faces the camera for that body orientation.",
   []),
 "VFC-C06": ("C", "critical", "Stance switched (southpaw instead of orthodox)",
   "The orthodox hero drawn with the right hand and right foot leading, or the jab hand flipping between shots of one sequence.",
   "Orthodox: LEFT hand and LEFT foot lead in every shot; the same jab hand throughout a sequence.",
   []),
 # D floating
 "VFC-D01": ("D", "critical", "Floating or detached glove, hand or limb",
   "A glove without a forearm, an arm detached from the shoulder, a hand with no visible owner.",
   "Every glove and hand must trace through a wrist, forearm and upper arm to a shoulder.",
   []),
 "VFC-D02": ("D", "major", "Feet floating or detached from the ground",
   "Feet hovering, both feet off the ground in a standing technique, heels below the floor.",
   "Planted feet touch the ground line; one foot at least is planted in every standing technique.",
   ["rig_feet"]),
 # E identity
 "VFC-E01": ("E", "critical", "Face features on a faceless character",
   "A mouth, nose, eyebrows or scowl on the hero or opponent, or missing eyes.",
   "Faces are blank with exactly two small slanted white eyes; nothing else.",
   []),
 "VFC-E02": ("E", "major", "Outfit drift",
   "Wrong shirt colour, bare chest, shoes or socks, wrong glove type, red straps on opponent gloves, lettering on shirts, wrong format outfit.",
   "Compare every character with the reference sheet for the format (long form black shirt, Shorts gray tank; opponent red tank, black shorts, plain black gloves; barefoot).",
   ["colour_outfit"]),
 "VFC-E03": ("E", "major", "Skin or colour drift and speckles",
   "Skin drifting tan or peach, discoloured heads, shorts drifting navy, speckles from colour cleanup.",
   "Skin is charcoal everywhere; run the colour screener and inspect flagged patches at full size.",
   ["colour_skin"]),
 "VFC-E04": ("E", "critical", "Ghost, duplicate or extra character",
   "Reference sheet turnaround copies, the hero drawn twice, a faded figure, a third person in a two person scene, a partner in a solo video.",
   "Count characters; exactly the scripted cast, no faded or turnaround copies.",
   ["pose_person_count"]),
 "VFC-E05": ("E", "major", "Opponent size or role wrong",
   "The opponent is not clearly bigger, proportions of the opponent change between shots.",
   "Opponent about half a head taller with broader shoulders in every two shot.",
   []),
 "VFC-E06": ("E", "major", "Style break",
   "3D mannequin look leaking into the 2D style, emissive glow recolouring the costume, generic AI look.",
   "Compare with approved 2D stills; reject any 3D shading or glow on the characters.",
   []),
 # F impact
 "VFC-F01": ("F", "critical", "Strike lands on a forbidden target",
   "Punches on the neck, throat, shoulder, ear, top of the head or chest centre; knee in the groin.",
   "Strikes land only on chin, jaw or body (ribs, liver, stomach), with the neck visible and clear.",
   []),
 "VFC-F02": ("F", "critical", "Strike does not connect or a miss reads as a hit",
   "The glove stops short, passes behind, or a slip reads as a hit; the jab does not clear a dipped head.",
   "Contact Law: every landed punch touches the target and compresses it; every miss shows a clear gap.",
   []),
 "VFC-F03": ("F", "critical", "Glove or limb buried inside the opponent or their clothing",
   "The glove disappears under the opponent's shirt or into the body instead of compressing the surface; fabric drawn wrapping over the glove.",
   "At contact the whole glove stays visible on top of the shirt; the shirt and body dent inward around it. A glove hidden under fabric fails.",
   []),
 "VFC-F04": ("F", "critical", "Forbidden impact effect",
   "Bursts, flashes, white frames, sparks, shockwaves, glows or spiral swirls on a strike.",
   "Speed lines drawn in code are the only strike effect (R11); image prompts say draw no effects.",
   ["flash_frames"]),
 # G framing
 "VFC-G01": ("G", "major", "Head or body cut by the frame edge",
   "A head clipped by the top edge, an opponent sliced by a side edge, an arm entering mid edge, a sliver of an eye.",
   "Nothing important touches the left, right or top edge; bodies leave only through the bottom or a corner.",
   ["edge_contact"]),
 "VFC-G02": ("G", "major", "Text or graphic covering a head, face or the action",
   "Headlines, chips, CTA buttons or labels over a head or the strike.",
   "Every overlay box must sit on background pixels only; check every shot an overlay spans.",
   []),
 "VFC-G03": ("G", "major", "Camera hides the key action",
   "The punching arm hidden by the body, a profile head reading as the back of the head, contact behind the opponent.",
   "Pick the angle that shows the lesson; the technique in the narration must be visible.",
   []),
 # H compositing / animation
 "VFC-H01": ("H", "major", "Overlay or layer compositing error",
   "Alpha drawn at full strength, colour cleanup speckling cloth, background detection recolouring figures, overlay on the wrong body part.",
   "Overlays on their own transparent layer; inspect the first and last frame of every overlay.",
   []),
 "VFC-H02": ("H", "major", "Empty, frozen or dead frames",
   "Frames with only background, freezes, static holds over voice pauses.",
   "No frame is mostly empty background outside intended cards; every second has motion.",
   ["empty_frames", "freeze_frames"]),
 "VFC-H03": ("H", "major", "Transition or render error",
   "Flash during a whip pan, stale render from a stopped process, a shot one frame early, dropped tail.",
   "Render to a new filename with no other render running; frame check every transition.",
   ["flash_frames"]),
 "VFC-H04": ("H", "critical", "Interpenetration in animation",
   "Gloves passing through heads, elbows into torsos, glove clashes in in between frames.",
   "Check every animation frame, not key poses only; the rig collision metrics must be zero.",
   ["rig_collision"]),
 "VFC-H05": ("H", "major", "Placeholder, watermark or reused crop shipped",
   "Placeholder labels, watermarks, crops of other shots standing in for a missing still.",
   "No placeholder or watermark ever reaches a cut; reused stills at most twice and never adjacent.",
   ["known_defect_match"]),
 "VFC-H06": ("H", "minor", "Stray lines, streaks or artifacts",
   "Stray floor line fragments, sky streaks, speed lines drawn in the wrong place.",
   "Inspect edges and backgrounds at full size.",
   []),
 # I narration
 "VFC-I01": ("I", "critical", "Visual contradicts the narration",
   "The picture shows something other than what is said at that second (snap back with the arm still out, hands stay up with hands down, a sprint in a scene about gassing).",
   "At each narration line ask: does the picture do exactly what the words say, right now?",
   []),
 "VFC-I02": ("I", "major", "Caption or on screen text error",
   "Missing caption word, headline repeating the narration, chunks broken mid phrase, wrong counts, labels that do not match the picture (ELBOW ON HIP with no elbow on the hip).",
   "Every label must be true of the picture under it; captions match the spoken words exactly.",
   []),
 "VFC-I03": ("I", "major", "No visible change between beats",
   "One image reused for different concepts, two consecutive beats with no visible change.",
   "One verb, one image: every beat has a start pose, an end pose and a visible change.",
   ["known_defect_match"]),
}

ROLES = {
    "image-generation": "A B C D E F G",
    "animation": "A B C D E F G H",
    "compositing": "G H I",
    "qc": "A B C D E F G H I",
    "combat-anatomy-specialist": "A B C D E F",
    "visual-creative-director": "E F G H I",
}


def now():
    return time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())


def load():
    if REG.exists():
        return json.loads(REG.read_text())
    return {"version": 0, "updated": now(), "classes": {}, "instances": {}, "workers": {}, "certifications": []}


def save(reg):
    reg["version"] = int(reg.get("version", 0)) + 1
    reg["updated"] = now()
    for cid, (cat, sev, name, desc, rule, auto) in CLASSES.items():
        reg["classes"].setdefault(cid, {}).update(
            {"category": cat, "severity": sev, "name": name, "description": desc, "prevention_rule": rule, "auto_checks": auto})
    LIB.mkdir(parents=True, exist_ok=True)
    tmp = REG.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, indent=1, ensure_ascii=False))
    tmp.replace(REG)
    return reg


def lib_hash(reg=None):
    """Hash of everything a worker must know: classes plus instance ids and their explanations."""
    reg = reg or load()
    core = {"c": reg["classes"], "i": {k: (v["class"], v.get("explanation", "")) for k, v in sorted(reg["instances"].items())}}
    return hashlib.sha256(json.dumps(core, sort_keys=True).encode()).hexdigest()[:16]


def next_id(reg, prefix="VFI"):
    n = [int(k.split("-")[1]) for k in reg["instances"] if k.startswith(prefix + "-")]
    return f"{prefix}-{(max(n) + 1 if n else 1):04d}"


# ---------- images ----------
def _img():
    from PIL import Image
    return Image


def normalise(src_bytes_or_path, dest: Path, max_w=1280):
    Image = _img()
    im = Image.open(io.BytesIO(src_bytes_or_path) if isinstance(src_bytes_or_path, (bytes, bytearray)) else src_bytes_or_path)
    im = im.convert("RGB")
    if im.width > max_w:
        im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, "JPEG", quality=84, optimize=True)
    return dest


def dhash(path_or_im, size=16):
    """256 bit difference hash (robust to re-encoding and mild scaling, not to crops)."""
    Image = _img()
    im = path_or_im if hasattr(path_or_im, "convert") else Image.open(path_or_im)
    g = im.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for r in range(size):
        for c in range(size):
            bits = (bits << 1) | (px[r * (size + 1) + c] > px[r * (size + 1) + c + 1])
    return f"{bits:0{size * size // 4}x}"


def hamming(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def rel(p: Path):
    return str(Path(p).relative_to(LIB))
