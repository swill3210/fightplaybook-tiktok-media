#!/usr/bin/env python3
"""Regenerate ONLY failed stills (ElevenLabs Image API, Nano Banana 2 by default).

jobs JSON: [{"id": "V12", "mode": "edit"|"redraw"|"text", "src": "<image to edit>", "pose": "<rig render>", "prompt": "..."}]
edit   = the source still goes FIRST; only the named change is made (cheapest way to keep framing and identity)
redraw = rig pose render first, then the character references (REDRAW THE FIRST IMAGE)
text   = character references only
Each job writes OUT/<id>_<n>.png and appends to the ledger (generation id, credits) so nothing is ever lost or paid twice.
usage: regen.py jobs.json OUT [--n 1] [--model gemini-3.1-flash-image]
"""
import argparse, json, os, sys, time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, str(Path(__file__).parent))
import bench

LEDGER = Path(__file__).resolve().parents[1] / "liver_v4" / "ledger.jsonl"
m = bench.blocks()
KEEP = ("Keep everything else EXACTLY as in the first image: same camera, framing, characters, faces (blank, two white eyes only), "
        "clothing, colours, background and line style. Exactly the same number of people. Draw no effects.")


def run_job(j, out, model, k):
    dst = out / f"{j['id']}_{k}.png"
    if dst.exists():
        return {"id": j["id"], "file": str(dst), "skipped": True}
    os.environ["FP_RESTYLE"] = "1" if j["mode"] == "redraw" else "0"
    run = bench.eleven(model, {"resolution": "2K"})
    if j["mode"] == "edit":
        sc = {"prompt": "EDIT THE FIRST IMAGE. " + j["prompt"] + " " + KEEP}
        refs, pose = [Path(j["src"])] + bench.REFS[:1], None
    elif j["mode"] == "redraw":
        sc = {"prompt": " ".join([m.STYLE, j["prompt"], m.HERO, m.OPP, m.NOFX, "Plain flat sage green background #C4D6C4, thin ground line. Barefoot. Wide 16:9."])}
        refs, pose = bench.REFS, Path(j["pose"])
    else:
        sc = {"prompt": " ".join([m.STYLE, j["prompt"], m.HERO, m.OPP, m.NOFX, "Plain flat sage green background #C4D6C4, thin ground line. Barefoot. Wide 16:9."])}
        refs, pose = bench.REFS, None
    t0 = time.time()
    try:
        img, info = run(sc, refs, pose)
        dst.write_bytes(img)
        rec = {"id": j["id"], "file": str(dst), "mode": j["mode"], "gen": info.get("generation_id"),
               "credits": (info.get("response") or {}).get("credits_used"), "s": round(time.time() - t0, 1), "t": time.strftime("%Y-%m-%d %H:%M")}
    except Exception as e:
        rec = {"id": j["id"], "err": repr(e)[:300], "mode": j["mode"]}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with open(LEDGER, "a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs"); ap.add_argument("out"); ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--model", default="gemini-3.1-flash-image"); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    jobs = json.load(open(a.jobs))
    tasks = [(j, k) for j in jobs for k in range(1, a.n + 1)]
    with ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(lambda t: run_job(t[0], out, a.model, t[1]), tasks):
            print(json.dumps(r)[:200])
            if "err" in r and ("quota" in r["err"] or "401" in r["err"]):
                print("STOP: quota or auth error"); break


if __name__ == "__main__":
    main()
