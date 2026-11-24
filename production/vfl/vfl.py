#!/usr/bin/env python3
"""Visual Failure Library CLI: token lean visual QC for The Fight Playbook.

Flow (cheapest first):
  1. checklist        print the condensed master checklist (the only rules text a worker loads)
  2. status MANIFEST  hash every asset; skip cached PASS; run free programmatic screeners; list what needs eyes
  3. sheet IDS        2x2 labelled contact sheets of only the assets that need the inspector
  4. verdict FILE     ingest terse inspector lines "ID PASS" / "ID FAIL A01,F03 note" / "ID UNSURE B01 note";
                      caches by file hash, records new failures in the library (deduplicated), lists escalations
  5. render VIDEO     screen the final render for defects added by animation or cropping
  6. gate             block delivery unless every asset PASSes, the render is clean and the inspector is certified
Detail on demand: show CODE prints one class with up to N example paths. Never load the whole registry.
"""
import argparse, hashlib, json, random, re, sys, time
from pathlib import Path
import vfl_lib as L

CACHE = L.LIB / "approvals.json"          # sha256 -> verdict (shared across sessions via the vault)
CHECKLIST = L.LIB / "CHECKLIST.md"
INSPECTOR = "combat-anatomy-specialist"    # the one primary visual inspector
SECOND = "visual-inspector-second-opinion" # used only for UNSURE items
CERT_DIR = Path("/tmp/claude-0/vfl_cert")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jload(p, d):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else d


def jsave(p, d):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(d, indent=1, ensure_ascii=False))


def code(cid):
    return cid.split("-", 1)[1]


# ---------------- checklist ----------------
def checklist_text(role=None):
    cats = L.ROLES.get(role, "ABCDEFGHI").split() if role else list("ABCDEFGHI")
    lines = ["# Visual QC master checklist (condensed; detail: `vfl.py show CODE`)",
             "Borderline = FAIL. Uncertain = UNSURE (escalated). Reply one line per asset: `ID PASS` | `ID FAIL CODES note` | `ID UNSURE CODES note`.", ""]
    for c in cats:
        lines.append(f"**{c} {L.CATEGORIES[c]}**")
        for cid, (cat, sev, name, desc, rule, auto) in L.CLASSES.items():
            if cat == c:
                lines.append(f"- {code(cid)} {'!' if sev == 'critical' else ''}{name}: {rule}")
    return "\n".join(lines)


def cmd_checklist(a):
    txt = checklist_text(a.role)
    full = checklist_text(None)
    CHECKLIST.parent.mkdir(parents=True, exist_ok=True)
    if not CHECKLIST.exists() or CHECKLIST.read_text() != full + "\n":
        CHECKLIST.write_text(full + "\n")
    L.STATE.mkdir(parents=True, exist_ok=True)
    (L.STATE / f"ack_{a.role or 'all'}.json").write_text(json.dumps({"hash": hashlib.sha256(full.encode()).hexdigest()[:16], "t": L.now()}))
    print(txt)


def require_ack(role):
    """Called by generation, animation and render tools before they run."""
    full = checklist_text(None)
    h = hashlib.sha256(full.encode()).hexdigest()[:16]
    for r in (role, "all"):
        f = L.STATE / f"ack_{r}.json"
        if f.exists() and json.loads(f.read_text()).get("hash") == h:
            return True
    sys.exit(f"VFL gate: run `python3 production/vfl/vfl.py checklist --role {role}` before {role} work (checklist changed or not read).")


# ---------------- detail on demand ----------------
def cmd_show(a):
    reg = L.load()
    cid = a.code if a.code.startswith("VFC-") else "VFC-" + a.code
    c = reg["classes"].get(cid) or {}
    print(f"{code(cid)} [{c.get('severity')}] {c.get('name')}\n  what: {c.get('description')}\n  rule: {c.get('prevention_rule')}")
    hits = [(k, v) for k, v in reg["instances"].items() if v["class"] == cid or cid in v.get("also", [])]
    hits.sort(key=lambda kv: (kv[1].get("detected_by") != "Sean", not kv[1].get("original")))
    print(f"  {len(hits)} documented instances; showing {min(a.n, len(hits))}:")
    for k, v in hits[: a.n]:
        o = (v.get("original") or {}).get("path")
        print(f"  {k} {v['project'][:28]} {v.get('shot','')} {v.get('time','')}: {v['title'][:70]}" + (f"\n     img: {L.LIB / o}" if o else ""))


# ---------------- status / screening ----------------
def manifest(p):
    m = json.loads(Path(p).read_text())
    return {k: str(v) for k, v in m.items()}


def cmd_status(a):
    from checks import screen_still
    reg, cache = L.load(), jload(CACHE, {})
    need, out = [], {"PASS": [], "FAIL": [], "NEED": []}
    for aid, p in manifest(a.manifest).items():
        h = sha(p)
        c = cache.get(h)
        if c and not a.recheck:
            out[c["verdict"] if c["verdict"] in ("PASS", "FAIL") else "NEED"].append(f"{aid} {c['verdict']} {','.join(c.get('codes', []))}")
            continue
        hits = screen_still(p, reg)
        hard = [x for x in hits if x[1] == "FAIL"]
        if hard:
            cache[h] = {"asset": aid, "path": p, "verdict": "FAIL", "codes": sorted({x[0] for x in hard}), "by": "programmatic", "t": L.now(), "note": hard[0][2]}
            out["FAIL"].append(f"{aid} FAIL {','.join(cache[h]['codes'])} ({hard[0][2]})")
        else:
            out["NEED"].append(f"{aid} NEED " + ";".join(f"{c} {n}" for c, _, n in hits))
            need.append(aid)
    jsave(CACHE, cache)
    for k in ("FAIL", "NEED"):
        for line in out[k]:
            print(line)
    print(f"summary: {len(out['PASS'])} cached PASS, {len(out['FAIL'])} FAIL, {len(out['NEED'])} need the inspector")
    Path(a.manifest).with_suffix(".need.json").write_text(json.dumps(need))


def cmd_sheet(a):
    from PIL import Image, ImageDraw, ImageFont
    m = manifest(a.manifest)
    ids = a.ids or json.loads(Path(a.manifest).with_suffix(".need.json").read_text())
    per = 1 if a.full else 4
    W, H = 1920, 1080
    font = ImageFont.load_default(size=44)
    outdir = Path(a.out); outdir.mkdir(parents=True, exist_ok=True)
    sheets = []
    for i in range(0, len(ids), per):
        sheet = Image.new("RGB", (W, H), (20, 20, 20))
        for j, aid in enumerate(ids[i:i + per]):
            im = Image.open(m[aid]).convert("RGB")
            cw, ch = (W, H) if per == 1 else (W // 2, H // 2)
            im.thumbnail((cw - 8, ch - 8))
            x, y = (0, 0) if per == 1 else ((j % 2) * cw, (j // 2) * ch)
            sheet.paste(im, (x + 4, y + 4))
            d = ImageDraw.Draw(sheet)
            d.rectangle([x + 4, y + 4, x + 20 + 30 * len(aid), y + 60], fill=(255, 230, 0))
            d.text((x + 12, y + 8), aid, fill=(0, 0, 0), font=font)
        f = outdir / f"sheet_{i // per + 1:02d}.jpg"
        sheet.save(f, quality=88)
        sheets.append(str(f))
    print("\n".join(sheets))


# ---------------- verdicts, recording, escalation ----------------
LINE = re.compile(r"^\s*(\S+)\s+(PASS|FAIL|UNSURE)\b\s*([A-I]\d\d(?:\s*,\s*[A-I]\d\d)*|NEW)?\s*(.*)$", re.I)


def _proj(a, b):
    a, b = a.lower(), b.lower()
    return bool(a and b) and (a.startswith(b) or b.startswith(a))


def record(reg, aid, path, codes, note, by, project):
    """Add a failure to the library without duplicating: same image (dhash) or same project+asset+class appends an occurrence."""
    h = L.dhash(path)
    added = []
    for c in codes:
        cid = "VFC-" + c
        dup = None
        for k, v in reg["instances"].items():
            same_img = (v.get("original") or {}).get("dhash") and L.hamming((v["original"]["dhash"]), h) <= 10
            if (v["class"] == cid or cid in v.get("also", [])) and (same_img or (_proj(v.get("project", ""), project) and v.get("shot") == aid)):
                dup = k
                break
        if dup:
            reg["instances"][dup].setdefault("occurrences", []).append({"t": L.now(), "by": by, "note": note[:120]})
            continue
        iid = L.next_id(reg)
        p = L.normalise(Path(path), L.EVID / iid / "original.jpg")
        reg["instances"][iid] = {"origin": "auto", "class": cid, "also": [], "title": note[:90] or L.CLASSES.get(cid, ("", "", "new"))[2],
                                 "project": project, "shot": aid, "time": "", "version": "", "source": f"vfl verdict {L.now()}",
                                 "detected_by": by, "approved_by": [], "explanation": note, "severity": L.CLASSES.get(cid, ("", "major"))[1],
                                 "status": "open", "date": L.now()[:10], "original": {"path": L.rel(p), "provenance": str(path), "inferred": False, "dhash": h},
                                 "corrected": None, "test_eligible": True}
        added.append(iid)
    return added


def cmd_verdict(a):
    m, reg, cache = manifest(a.manifest), L.load(), jload(CACHE, {})
    unsure, new, n = [], [], 0
    for line in Path(a.file).read_text().splitlines():
        mt = LINE.match(line)
        if not mt or mt.group(1) not in m:
            continue
        aid, v, codes, note = mt.group(1), mt.group(2).upper(), mt.group(3), mt.group(4).strip()
        codes = [c.strip().upper() for c in (codes or "").split(",") if c.strip() and c.upper() != "NEW"]
        if mt.group(3) and mt.group(3).upper() == "NEW":
            nid = f"VFC-X{len([c for c in reg['classes'] if c.startswith('VFC-X')]) + 1:02d}"
            reg["classes"][nid] = {"category": "X", "severity": "major", "name": note[:60], "description": note, "prevention_rule": "PENDING review",
                                   "auto_checks": [], "origin": "auto"}
            codes = [nid[4:]]
        p = m[aid]
        if a.inspector == SECOND and v == "UNSURE":
            v = "FAIL"  # second opinion uncertain counts as rejected
        cache[sha(p)] = {"asset": aid, "path": p, "verdict": v, "codes": codes, "by": a.inspector, "t": L.now(), "note": note[:160],
                         "lib": reg["version"]}
        if v == "FAIL":
            new += record(reg, aid, p, codes or ["B06"], note, a.inspector, a.project)
        if v == "UNSURE":
            unsure.append(aid)
        n += 1
    jsave(CACHE, cache)
    L.save(reg)
    print(f"{n} verdicts cached; new library instances: {', '.join(new) or 'none'}")
    if unsure:
        print("ESCALATE to second inspector (full size):", " ".join(unsure))


# ---------------- render ----------------
def cmd_render(a):
    from checks import screen_render, edge_frames
    t = json.loads(Path(a.timeline).read_text()) if a.timeline else {"shots": []}
    exempt = [(s["start"], s["end"]) for s in t["shots"] if s["id"] in (a.exempt or "").split(",")]
    hits = screen_render(a.video, exempt)
    times = []
    for s in t["shots"]:
        d = s["end"] - s["start"]
        times += [round(s["start"] + 0.15 * d, 2), round(s["start"] + 0.85 * d, 2)]
    hits += edge_frames(a.video, times)
    for h in hits:
        print(f"{h[0]:7.2f}s {h[1]} {h[2]} {h[3]}")
    fails = [h for h in hits if h[2] == "FAIL"]
    print(f"render screen: {len(fails)} FAIL, {len(hits) - len(fails)} FLAG (flags go to the inspector as frames)")
    jsave(Path(a.video).with_suffix(".vfl_render.json"), {"t": L.now(), "hits": hits})


# ---------------- certification ----------------
def cmd_certify(a):
    reg = L.load()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    if a.action == "make":
        pool = [(k, v) for k, v in reg["instances"].items() if v.get("test_eligible") and v.get("original") and v["severity"] == "critical"]
        pool.sort(key=lambda kv: (kv[1].get("detected_by") != "Sean", not kv[1].get("approved_by"), kv[0]))
        seen, pick = set(), []
        for k, v in pool:                      # Sean's cases first, then one per class, then fill
            if v.get("detected_by") == "Sean" or v["class"] not in seen:
                pick.append(k); seen.add(v["class"])
        for k, v in pool:
            if len(pick) >= a.n: break
            if k not in pick: pick.append(k)
        pick = pick[: a.n]
        random.Random(a.seed).shuffle(pick)
        man = {f"T{i + 1:02d}": str(L.LIB / reg["instances"][k]["original"]["path"]) for i, k in enumerate(pick)}
        key = {f"T{i + 1:02d}": k for i, k in enumerate(pick)}
        jsave(CERT_DIR / "manifest.json", man)
        jsave(CERT_DIR / "key.json", key)   # kept out of the vault and out of the inspector's prompt
        print(f"{len(man)} blind test images; manifest {CERT_DIR / 'manifest.json'}; build sheets with: vfl.py sheet {CERT_DIR / 'manifest.json'} --ids ... --out {CERT_DIR}")
    else:
        key = jload(CERT_DIR / "key.json", {})
        res = {}
        for line in Path(a.file).read_text().splitlines():
            mt = LINE.match(line)
            if mt and mt.group(1) in key:
                res[mt.group(1)] = (mt.group(2).upper(), mt.group(3) or "")
        approved = [t for t, (v, _) in res.items() if v == "PASS"]
        missing = [t for t in key if t not in res]
        unsure = [t for t, (v, _) in res.items() if v == "UNSURE"]
        ok = not approved and not missing
        rec = {"worker": a.worker, "worker_hash": hashlib.sha256(Path(a.worker_file).read_bytes()).hexdigest()[:16] if a.worker_file else "",
               "date": L.now(), "library_version": reg["version"], "n": len(key), "result": "PASS" if ok else "FAIL",
               "approved_known_defects": [key[t] for t in approved], "unanswered": [key[t] for t in missing], "unsure": [key[t] for t in unsure],
               "class_hits": sum(1 for t, (v, c) in res.items() if v == "FAIL" and code(reg["instances"][key[t]]["class"]) in (c or "").upper())}
        reg["certifications"].append(rec)
        for t in approved:
            reg["instances"][key[t]]["approved_by"] = sorted(set(reg["instances"][key[t]]["approved_by"] + [f"{a.worker} (certification {rec['date'][:10]})"]))
        L.save(reg)
        print(json.dumps(rec, indent=1))


def certified(reg, worker, worker_file=None):
    cs = [c for c in reg["certifications"] if c["worker"] == worker]
    if not cs or cs[-1]["result"] != "PASS":
        return False
    if worker_file and cs[-1]["worker_hash"] != hashlib.sha256(Path(worker_file).read_bytes()).hexdigest()[:16]:
        return False  # inspector instructions changed since it was certified
    return True


def cmd_gate(a):
    reg, cache = L.load(), jload(CACHE, {})
    problems = []
    if not certified(reg, INSPECTOR, a.inspector_file):
        problems.append(f"primary inspector {INSPECTOR} not certified against the library (run vfl.py certify)")
    for aid, p in manifest(a.manifest).items():
        c = cache.get(sha(p))
        if not c or c["verdict"] != "PASS":
            problems.append(f"{aid}: {c['verdict'] + ' ' + ','.join(c.get('codes', [])) if c else 'never inspected'}")
    if a.video:
        r = jload(Path(a.video).with_suffix(".vfl_render.json"), None)
        if not r:
            problems.append("render not screened (vfl.py render)")
        else:
            problems += [f"render {h[0]}s {h[1]} {h[3]}" for h in r["hits"] if h[2] == "FAIL" and f"{h[0]}" not in (a.waive or "")]
    if problems:
        print("GATE: BLOCKED\n" + "\n".join(problems[:60]) + (f"\n... {len(problems) - 60} more" if len(problems) > 60 else ""))
        sys.exit(1)
    print("GATE: PASS")


def cmd_notes(a):
    """Regenerate INDEX.md (one line per code) and classes/<CODE>.md (one line per instance). Never edit these by hand."""
    reg = L.load()
    d = L.LIB / "classes"; d.mkdir(parents=True, exist_ok=True)
    idx = ["# Visual Failure Library index (generated by `vfl.py notes`; do not edit)",
           f"Registry v{reg['version']}, {len(reg['instances'])} documented failures. Rules: CHECKLIST.md. Open one class file only when relevant.", "",
           "| Code | Sev | Name | Cases | Imgs | File |", "| --- | --- | --- | --- | --- | --- |"]
    for cid in sorted(reg["classes"]):
        c = reg["classes"][cid]
        hits = sorted([(k, v) for k, v in reg["instances"].items() if v["class"] == cid or cid in v.get("also", [])],
                      key=lambda kv: (kv[1].get("detected_by") != "Sean", kv[0]))
        imgs = sum(1 for _, v in hits if v.get("original"))
        idx.append(f"| {code(cid)} | {c['severity'][:4]} | {c['name']} | {len(hits)} | {imgs} | classes/{code(cid)}.md |")
        lines = [f"# {code(cid)} {c['name']} ({c['severity']})", f"What: {c['description']}", f"Rule: {c['prevention_rule']}",
                 f"Auto screeners: {', '.join(c.get('auto_checks') or []) or 'none (inspector only)'}", "",
                 "ID | project | shot time | defect | detected by | missed by | original | corrected"]
        for k, v in hits:
            o = (v.get("original") or {}).get("path") or "-"
            cr = v.get("corrected") or {}
            lines.append(f"{k} | {v['project'][:30]} | {v.get('shot','')} {v.get('time','')} | {v['title'][:80]} | {v['detected_by'][:30]} | "
                         f"{'; '.join(v.get('approved_by', []))[:80] or '-'} | {o} | {cr.get('path') or (cr.get('status') or '-')[:50]}")
        (d / f"{code(cid)}.md").write_text("\n".join(lines) + "\n")
    (L.LIB / "INDEX.md").write_text("\n".join(idx) + "\n")
    print(f"INDEX.md and {len(reg['classes'])} class files written")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = ap.add_subparsers(dest="cmd", required=True)
    p = s.add_parser("notes"); p.set_defaults(f=cmd_notes)
    p = s.add_parser("checklist"); p.add_argument("--role"); p.set_defaults(f=cmd_checklist)
    p = s.add_parser("show"); p.add_argument("code"); p.add_argument("--n", type=int, default=3); p.set_defaults(f=cmd_show)
    p = s.add_parser("status"); p.add_argument("manifest"); p.add_argument("--recheck", action="store_true"); p.set_defaults(f=cmd_status)
    p = s.add_parser("sheet"); p.add_argument("manifest"); p.add_argument("--ids", nargs="*"); p.add_argument("--out", required=True)
    p.add_argument("--full", action="store_true"); p.set_defaults(f=cmd_sheet)
    p = s.add_parser("verdict"); p.add_argument("manifest"); p.add_argument("file"); p.add_argument("--inspector", default=INSPECTOR)
    p.add_argument("--project", default=""); p.set_defaults(f=cmd_verdict)
    p = s.add_parser("render"); p.add_argument("video"); p.add_argument("--timeline"); p.add_argument("--exempt"); p.set_defaults(f=cmd_render)
    p = s.add_parser("certify"); p.add_argument("action", choices=["make", "score"]); p.add_argument("file", nargs="?")
    p.add_argument("--worker", default=INSPECTOR); p.add_argument("--worker-file"); p.add_argument("--n", type=int, default=16)
    p.add_argument("--seed", type=int, default=7); p.set_defaults(f=cmd_certify)
    p = s.add_parser("gate"); p.add_argument("manifest"); p.add_argument("--video"); p.add_argument("--inspector-file"); p.add_argument("--waive")
    p.set_defaults(f=cmd_gate)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
