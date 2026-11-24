"""Build the Visual Failure Library from the documented history (reproducible; safe to re-run).

Every instance cites the QA report or feedback it came from. Images are fetched only when the source names the exact
file (or, for liver anatomy round 1, when the file is inferred from ledger timestamps; those are flagged inferred and
excluded from worker certification). Nothing is invented: an instance without evidence says so.

Usage: python3 harvest.py [--no-fetch]
"""
import json, re, sys, urllib.request, collections
from pathlib import Path
import vfl_lib as L
import curated

HO = Path("/home/user/the-fight-playbook-claude-handoff")
EXP = Path("/home/user/claude-export/CLAUDE-EXPORT")
LIVER = HO / "VIDEO-PROJECTS/target-the-liver-in-boxing"
CACHE = Path("/tmp/claude-0/vfl_cache"); CACHE.mkdir(parents=True, exist_ok=True)
FETCH = "--no-fetch" not in sys.argv
MISSING = []

# keyword -> class, in priority order (first hit = primary class)
RULES = [
    (r"wrong arm|right arm on a left|uses the right arm|\bright arm\b(?!.*left arm)|right hand thrown|opponent's right hand", "VFC-C01"),
    (r"ghost|turnaround|reference sheet|drawn twice|three figures|third figure|second figure|extra front.view", "VFC-E04"),
    (r"third glove|three gloves|three hands|extra hand|extra glove|third wrist|\bcuff\b|three arm", "VFC-A01"),
    (r"floating|detached|without a visible forearm", "VFC-D01"),
    (r"knee strike instead|horizontal punch, not upward|idle guard|copy of t01|reads as a jab|body jab shape", "VFC-B06"),
    (r"shovel|uppercut", "VFC-B03"),
    (r"straight|open angle|not an l\b|no l\b|not a clear l|slightly bent|near straight|reads as a straight|long and straight", "VFC-B01"),
    (r"elbow (above|below|not at|dropped|hanging)|forearm (sloping|not level|angled down)|low elbow|vertical upper arm|elbow at the hip below", "VFC-B02"),
    (r"kink|sag|too long|stretched|unequal|uneven|rubbery|snake|wrapped around|bent unnaturally", "VFC-A03"),
    (r"lands? (at|mid) (chest|torso)|chest or chin height|on the neck|hit the neck|near the neck|on the throat|groin|shoulder\b(?!s)", "VFC-F01"),
    (r"did not clear|not touching|not rising|on top of the hero's head", "VFC-F02"),
    (r"tangled|crossing", "VFC-A06"),
    (r"fisheye|giant feet|unnatural size", "VFC-A07"),
    (r"finger|bare fist|open hand", "VFC-A05"),
    (r"guard (glove dropped|arms bent wrong|arm raised)|glove raised (behind|above)|rear glove dropped", "VFC-B05"),
    (r"start pose did not sit|chamber pose had to match", "VFC-B08"),
    (r"mouth|nose|scowl|no eyes|face borderline|colour and face", "VFC-E01"),
    (r"red straps|shoes|red shirt|bare.chested", "VFC-E02"),
    (r"colou?r|skin|discolou|tan\b|peach|brown", "VFC-E03"),
    (r"top edge|cut off|cut by", "VFC-G01"),
]


def classify(text):
    t = text.lower()
    hits = []
    for pat, cid in RULES:
        if re.search(pat, t) and cid not in hits:
            hits.append(cid)
    return hits or ["VFC-B06"]


def fetch_gen(gen):
    f = CACHE / f"{gen}.png"
    if f.exists():
        return f.read_bytes()
    if not FETCH:
        return None
    miss = CACHE / f"{gen}.missing"
    if miss.exists():
        return None
    try:
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/flows/image/{gen}", headers={"xi-api-key": "proxy-injected"})
        j = json.loads(urllib.request.urlopen(req, timeout=60).read())
        if j.get("status") != "completed":
            miss.write_text(j.get("status", "?"))
            return None
        b = urllib.request.urlopen(j["content_url"], timeout=120).read()
    except Exception as e:  # deleted generation or another workspace: record, do not invent
        miss.write_text(str(e))
        MISSING.append(gen)
        return None
    f.write_bytes(b)
    return b


# ---------- ledgers: filename -> generation ----------
def liver_ledger():
    g = json.load(open(LIVER / "ledger_liver.json"))["generated"]
    return {e["file"][:-4]: e for e in g if e.get("file")}, g


LIV, LIV_ALL = liver_ledger()


def liver_img(name):
    """bytes of a liver still by file stem: on disk (approved stills) or via its ledger generation."""
    p = LIVER / "edit/stills" / f"{name}.png"
    if p.exists():
        return p.read_bytes(), f"handoff repo edit/stills/{name}.png"
    e = LIV.get(name)
    if e:
        b = fetch_gen(e["gen"])
        if b:
            return b, f"ElevenLabs generation {e['gen']} (ledger_liver.json, file {name}.png, {e['t']})"
    return None, None


def infer_r1(still):
    """latest generation for a still before the anatomy round 1 fixes (2026-11-23 03:23 ET)."""
    c = [e for e in LIV_ALL if e["still"] == still and e.get("file") and e["t"] < "2026-11-23 03:23 ET"]
    return c[-1]["file"][:-4] if c else None


def parse_table(md, ncols_min=3):
    rows = []
    for line in Path(md).read_text().splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= ncols_min:
                rows.append(cells)
    return rows


# ---------- instance builder ----------
class Builder:
    def __init__(self, reg):
        self.reg = reg
        self.reg["instances"] = {k: v for k, v in reg["instances"].items() if v.get("origin") != "harvest"}
        self.n = 0

    def add(self, *, key, classes, title, project, shot="", time="", version="", source, detected_by, approved_by=(),
            explanation, original=None, original_prov="", corrected=None, corrected_prov="", corrected_status="",
            inferred=False, severity=None, status="fixed", test_eligible=True, date=""):
        iid = f"VFI-{len([k for k in self.reg['instances']]) + 1:04d}"
        d = L.EVID / iid
        inst = {"origin": "harvest", "key": key, "class": classes[0], "also": classes[1:], "title": title,
                "project": project, "shot": shot, "time": time, "version": version, "source": source,
                "detected_by": detected_by, "approved_by": list(approved_by), "explanation": explanation,
                "severity": severity or self.reg["classes"].get(classes[0], {}).get("severity") or L.CLASSES[classes[0]][1],
                "status": status, "date": date, "original": None, "corrected": None}
        if original:
            p = L.normalise(original, d / "original.jpg")
            inst["original"] = {"path": L.rel(p), "provenance": original_prov, "inferred": inferred, "dhash": L.dhash(p)}
        if corrected:
            p = L.normalise(corrected, d / "corrected.jpg")
            inst["corrected"] = {"path": L.rel(p), "provenance": corrected_prov, "status": corrected_status, "dhash": L.dhash(p)}
        elif corrected_status:
            inst["corrected"] = {"path": None, "provenance": corrected_prov, "status": corrected_status}
        inst["test_eligible"] = bool(test_eligible and original and not inferred)
        self.reg["instances"][iid] = inst
        self.n += 1
        return iid


GROK_QA = "Grok still QA"
SEAN = "Sean"


def harvest_liver(b):
    v4sel = json.load(open(LIVER / "edit/work/sel.json"))
    # --- pass 1 (first stills, 2026-11-22) ---
    img, prov = liver_img("V3")
    b.add(key="liver.p1.V3", classes=["VFC-E04", "VFC-B01", "VFC-G01"], title="Reference sheet copied into the still; hook drawn straight",
          project="3 Ways to Target the Liver (Grok)", shot="V3", time="0:03", version="pass 1 still",
          source="handoff VIDEO-PROJECTS/target-the-liver-in-boxing/edit/qa/still_qa_pass1.md", detected_by=GROK_QA,
          explanation="Extra front view hero and back view opponent copied from the reference sheet at the sides (turnaround ghosts); the hero's punch is a straight arm to the gloves, not an L hook to the ribs; the opponent's head nearly touches the top edge.",
          original=img, original_prov=prov, date="2026-11-22")
    # --- anatomy rounds R1..R5 (2026-11-23 ~03:2x ET) ---
    for r in parse_table(LIVER / "edit/qa/anatomy_qa.md", 10):
        if r[0] in ("Shot",) or r[3] != "FAIL":
            continue
        shot, t0, angle, final, reason = r[0], r[1], r[2], r[8], r[9]
        if not reason:
            continue
        failed = infer_r1(shot)
        img, prov = liver_img(failed) if failed else (None, None)
        cimg, cprov = liver_img(final) if final and final != "code" else (None, None)
        sec = int(t0.split()[0])
        b.add(key=f"liver.anat.{shot}", classes=classify(reason), title=reason[:90], project="3 Ways to Target the Liver (Grok)",
              shot=shot, time=f"{sec // 60}:{sec % 60:02d}", version="silent v1 anatomy round 1", detected_by=GROK_QA + " (anatomy round 1, after Sean's QC order)",
              approved_by=["Grok first pass QA"] if re.search(r"\(\d:\d\d\)", reason) else [],
              source="handoff edit/qa/anatomy_qa.md (R1 fail reason)", explanation=f"{reason}. Camera: {angle}.",
              original=img, original_prov=(prov or "") + (f"; file {failed} inferred as the latest generation before the round 1 fixes" if failed else ""),
              inferred=True, corrected=cimg, corrected_prov=cprov or "",
              corrected_status=f"Grok anatomy round 5 final {final}; superseded later if it appears in a later instance", date="2026-11-23")
    # --- Sean's flags on the first silent cut ---
    for shot, t, txt, cls in [("V30", "0:37", "Hero's back of head brown and textured (discoloured head)", ["VFC-E03"]),
                               ("V57", "1:15", "Opponent's jab glove sat on top of the hero's head with no slip; the punching arm unclear; stray floor line fragment", ["VFC-F02", "VFC-H06"])]:
        img, prov = liver_img(shot)
        b.add(key=f"liver.sean1.{shot}", classes=cls, title=txt[:90], project="3 Ways to Target the Liver (Grok)", shot=shot, time=t,
              version="silent v1", source="handoff STATUS.md and edit/qa/still_qa_pass2.md", detected_by=SEAN,
              approved_by=["Grok first pass QA"], explanation=txt + ". Sean caught it after Grok's QA passed the cut.",
              original=img, original_prov=prov or "", date="2026-11-23")
    # --- v3 strict arm audit (all these had PASSED anatomy rounds 1 to 5 and the v2 QA) ---
    fails = json.load(open(LIVER / "edit/work/v3_fail_nodes.json"))
    for r in parse_table(LIVER / "edit/qa/v3/anatomy_qa_v3.md", 4):
        shot = r[0]
        if shot not in fails:
            continue
        failed, fault, final = fails[shot][0], r[2], r[3]
        img, prov = liver_img(failed)
        cimg, cprov = liver_img(final)
        sean = "SEAN" in fault
        b.add(key=f"liver.v3.{shot}", classes=classify(fault), title=fault[:90], project="3 Ways to Target the Liver (Grok)", shot=shot,
              time=r[1], version="silent v2 (still " + failed + ")", source="handoff edit/qa/v3/anatomy_qa_v3.md and edit/work/v3_fail_nodes.json",
              detected_by=SEAN if sean else "Grok strict zoomed arm audit (v3)",
              approved_by=["Grok anatomy QA rounds 1 to 5", "Grok v2 render QA (anatomy: no defects)"],
              explanation=fault + f". Still {failed} had passed every earlier QA round.",
              original=img, original_prov=prov or "", corrected=cimg, corrected_prov=cprov or "",
              corrected_status=f"Grok v3 replacement {final}", date="2026-11-23")
    # --- v4 hook rules audit (all these had PASSED the v3 strict audit) ---
    for r in parse_table(LIVER / "edit/qa/v4/hook_qa_v4.md", 4):
        m = re.match(r"(V\w+?) (FAIL|replaced)[: ]+(.*)", r[2])
        if not m or not r[0].startswith("V"):
            continue
        failed, fault = m.group(1), m.group(3)
        final = r[3].split()[0]
        img, prov = liver_img(failed)
        cimg, cprov = liver_img(final)
        b.add(key=f"liver.v4.{r[0]}", classes=classify(fault), title=fault[:90], project="3 Ways to Target the Liver (Grok)", shot=r[0], time=r[1],
              version="silent v3 (still " + failed + ")", source="handoff QUALITY-CONTROL/target-the-liver-in-boxing/v4/hook_qa_v4.md",
              detected_by="Grok hook rules audit (v4, Sean's hook rules)", approved_by=["Grok strict zoomed arm audit (v3)", "Grok v3 render QA (zero defects)"],
              explanation=fault + f". Still {failed} had passed the v3 strict audit and two render passes.",
              original=img, original_prov=prov or "", corrected=cimg, corrected_prov=cprov or "",
              corrected_status=f"Grok v4 replacement {final}; see the Claude v1 audit instances for v4 stills that failed later", date="2026-11-23")
    # --- render-level fails Grok caught ---
    b.add(key="liver.v3render.V80", classes=["VFC-A05"], title="Glove drawn with separate fingers like a bare fist", project="3 Ways to Target the Liver (Grok)",
          shot="V80", time="1:44", version="silent v3 render 1", source="handoff edit/qa/v3/anatomy_qa_v3.md (round 5)", detected_by="Grok slow motion render pass",
          approved_by=["Grok strict zoomed arm audit (still level)"], explanation="Found only in the render slow motion pass; the still audit had passed it.",
          original=liver_img("V80_r2")[0], original_prov=liver_img("V80_r2")[1] or "", corrected=liver_img("V80_r3")[0], corrected_prov=liver_img("V80_r3")[1] or "",
          corrected_status="V80_r3 padded glove (later flagged again by Sean on 2026-11-24, see the Sean examples)", date="2026-11-23")
    # --- Claude v1 audit of Grok's v4 finals (22 fails); corrected = Claude's replacement in CLAUDE-EXPORT ---
    for r in parse_table(EXP / "FINAL-CUT/qa_report.md", 5):
        shot = r[0]
        if not re.match(r"V\d+$", shot):
            continue
        final = v4sel.get(shot, shot)
        img, prov = liver_img(final)
        fix = EXP / "FINAL-CUT/fixed-stills" / f"{shot}.png"
        defect = r[3]
        b.add(key=f"liver.claude1.{shot}", classes=classify(defect + " " + r[2]) if "shoes" not in defect else ["VFC-E02"],
              title=defect[:90], project="Liver long form (Claude v1 built on Grok v4 stills)", shot=shot, time=r[1], version=f"Claude v1 (Grok v4 still {final})",
              source="CLAUDE-EXPORT/FINAL-CUT/qa_report.md (Claude revision 2 audit)", detected_by="Claude combat accuracy audit after Sean's 2026-11-24 review",
              approved_by=["Grok v4 hook QA (0 defects)", "Claude v1 QC"], explanation=f"Spec: {r[2]}. Defect: {defect}. Fix used: {r[4]}.",
              original=img, original_prov=prov or "", corrected=fix.read_bytes() if fix.exists() else None,
              corrected_prov=f"CLAUDE-EXPORT/FINAL-CUT/fixed-stills/{shot}.png" if fix.exists() else "",
              corrected_status="Claude v2/v3 replacement, approved by Claude QC and the visual-creative-director; NOT re-verified under the Visual Failure Library",
              date="2026-11-24")


def harvest_other(b):
    og = json.load(open(HO / "VIDEO-PROJECTS/open-any-guard-body-punches/ledger_open_guard.json"))
    ogm = {e["file"][:-4]: e for e in og["entries"] + og["rework"]["generated"] if e.get("file")}
    def ogimg(n):
        e = ogm.get(n)
        return (fetch_gen(e["gen"]), f"ElevenLabs generation {e['gen']} (ledger_open_guard.json, {n}.png)") if e else (None, "")
    src = "handoff VIDEO-PROJECTS/open-any-guard-body-punches/edit/qa/qa_report*.md"
    items = [
        ("V17", ["VFC-A01", "VFC-G01", "VFC-F01"], "Three hands on the hero, heads cut by the top edge, punch to the centre of the torso", None),
        ("V17b", ["VFC-A01"], "Extra hand on the hero (first rework version)", "V17b_r2"),
        ("V17b_r1", ["VFC-E01"], "Mouth and scowl drawn on the faceless hero", "V17b_r2"),
        ("V12", ["VFC-G01"], "Opponent's head cut off by the top edge (painted band at the top)", "V12_r1"),
        ("V18a", ["VFC-E01", "VFC-B01"], "Hero drawn with no eyes; hook arm read close to a straight punch", "V18a_r3"),
        ("V6a", ["VFC-E02", "VFC-B01"], "Hero shown bare chested; hook came out straight", None),
        ("V27b", ["VFC-E02"], "Hero shown bare chested", None),
        ("V6b", ["VFC-E04", "VFC-B01"], "Hero drawn twice; hook came out straight", "V6b_r3"),
        ("V30a", ["VFC-A01"], "Extra glove in the fist filling close up", "V30a_r2"),
        ("V30a_r1", ["VFC-E03"], "Peach skin instead of charcoal", "V30a_r2"),
        ("V28b", ["VFC-F01"], "Punch hit the neck instead of the chin", None),
        ("V19a", ["VFC-E04"], "Reference sheet copy (turnaround or ghost figures)", None),
        ("V35c", ["VFC-E04"], "Reference sheet copy (turnaround or ghost figures)", None),
        ("V2b", ["VFC-B01"], "Hook came out as a straight", "V2b_r1"),
        ("V15c", ["VFC-B01"], "Hook came out as a straight", "V15c_r1"),
        ("V3", ["VFC-A01"], "Hero with three gloves (v1 still reused in the rework)", None),
        ("V4", ["VFC-E01"], "Opponent drawn with a mouth (v1 still)", None),
        ("V9", ["VFC-E04", "VFC-E01"], "Two extra reference sheet figures and an open mouth on the opponent (painted out locally)", None),
    ]
    for name, cls, txt, fixed in items:
        img, prov = ogimg(name)
        cimg, cprov = ogimg(fixed) if fixed else (None, "")
        b.add(key=f"openguard.{name}", classes=cls, title=txt[:90], project="Open Any Guard With Body Punches (Grok)", shot=name, version="rework 2026-11-21",
              source=src, detected_by=GROK_QA, explanation=txt + ".", original=img, original_prov=prov, corrected=cimg, corrected_prov=cprov,
              corrected_status=f"replacement {fixed}" if fixed else "regenerated or replaced; exact replacement file not recorded", date="2026-11-21")
    cd = json.load(open(HO / "VIDEO-PROJECTS/build-superhuman-cardio-v2/ledger_cardio_v2.json"))
    cm = {(e["id"], e.get("attempt")): e for e in cd["entries"] if e.get("generation_id")}
    def cimg(i, a):
        e = cm.get((i, a))
        return (fetch_gen(e["generation_id"]), f"ElevenLabs generation {e['generation_id']} (ledger_cardio_v2.json, {i} attempt {a})") if e else (None, "")
    csrc = "handoff VIDEO-PROJECTS/build-superhuman-cardio-v2/edit/qa_report.md and qa/qa_report.md"
    for i, a, cls, txt, fa in [
        ("S104", 1, ["VFC-E02"], "Hero drawn in a red shirt (the opponent's colour) on 'easy pace, breathing through'", 2),
        ("S111", 1, ["VFC-E02"], "Hero drawn in a red shirt on 'Your heart rate stays low'", 2),
        ("T02", 1, ["VFC-I03"], "Take 1 was a copy of T01 (no visible change between beats)", 5),
        ("T03", 1, ["VFC-I01"], "Idle guard where the beat needed a punch", None),
        ("T06", 1, ["VFC-I01", "VFC-I03"], "'Two, hands drop a little': gloves stay at the chin, no visible drop", 4),
        ("T06", 2, ["VFC-I01"], "'Two, hands drop a little': arms fully down (reads as 'gone')", 4),
        ("E02", 1, ["VFC-I01"], "'Type one, two or three': glove held across the chest instead of toward the viewer", 2),
    ]:
        img, prov = cimg(i, a)
        fimg, fprov = cimg(i, fa) if fa else (None, "")
        b.add(key=f"cardio.{i}.a{a}", classes=cls, title=txt[:90], project="Build Superhuman Cardio v2 (Grok)", shot=i, version=f"attempt {a}",
              source=csrc, detected_by=GROK_QA, explanation=txt + ".", original=img, original_prov=prov, corrected=fimg, corrected_prov=fprov,
              corrected_status=f"attempt {fa} used" if fa else "", date="2026-11-21")


def main():
    reg = L.load()
    b = Builder(reg)
    harvest_liver(b)
    harvest_other(b)
    curated.add_all(b)
    print("generations not retrievable:", len(MISSING), MISSING[:10])
    L.save(reg)
    c = collections.Counter(v["class"] for v in reg["instances"].values())
    print("instances", len(reg["instances"]), "with original image", sum(1 for v in reg["instances"].values() if v.get("original")),
          "test eligible", sum(1 for v in reg["instances"].values() if v.get("test_eligible")))
    print(sorted(c.items()))


if __name__ == "__main__":
    main()
