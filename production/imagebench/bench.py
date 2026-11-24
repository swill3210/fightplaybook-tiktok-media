#!/usr/bin/env python3
"""Fight Playbook image model bake off.

Sends the SAME 10 scene requests (built from Grok's production prompt blocks) to each model,
with the same character reference images and, where the model accepts it, the same OpenPose
skeleton from the 3D rig. Records wall time, cost and the image; builds per scene comparison sheets.

Nothing here replaces the production workflow. Outputs go to --out (keep them out of public repos).

usage:
  python3 bench.py plan  --out DIR                      # write prompts and inputs, no API calls
  python3 bench.py run   --out DIR --models a,b,c       # call the models that have keys
  python3 bench.py sheet --out DIR                      # comparison sheets for review

keys (environment or proxy injected): GEMINI_API_KEY, OPENAI_API_KEY, FAL_KEY
"""
import argparse, base64, importlib.util, io, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

HANDOFF = Path(os.environ.get("FP_HANDOFF", "/home/user/the-fight-playbook-claude-handoff"))
LIVER = HANDOFF / "VIDEO-PROJECTS/target-the-liver-in-boxing/edit"
REFS = [HANDOFF / "CHARACTERS/main_character_reference.jpg", HANDOFF / "CHARACTERS/pair_ref_hero_vs_opponent.jpg"]
POSE_DIR = Path(os.environ.get("FP_POSES", "/tmp/fp_poses"))  # S01.png ... from the rig (render.mjs posebench --pose)

def blocks():
    spec = importlib.util.spec_from_file_location("lp", LIVER / "prompts.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

# 10 identical scene requests. Camera wording follows the liver spec; actions use Grok's arm blocks.
def scenes(m):
    ho = m.ONCE["ho"]
    S = [
        ("S01", "Wide establishing shot from the side, eye level.", f"Both fighters in stance at distance, {m.GUARD}, main character on the RIGHT facing LEFT, opponent on the LEFT facing RIGHT.", "ho"),
        ("S02", "Medium side shot, eye level.", "The main character throws a LEFT jab: the left arm fully extended STRAIGHT and horizontal, shoulder, elbow and glove in one straight line, glove touching the opponent's high guard; the right glove stays at the chin. " + f"Opponent {m.GHIGH}.", "ho"),
        ("S03", "Rear three quarter view from behind the main character's left shoulder.", f"The main character throws a LEFT hook to the body: {m.HOOK}; knees bent to lower the level, hips and shoulders turned into the punch, right glove at the chin; {m.CONTACT}. Opponent {m.GHIGH}.", "ho"),
        ("S04", "Extreme close up on the opponent's right ribs.", f"The main character's black MMA glove with red wrist strap, attached to a visible forearm, {m.CONTACT}.", "ho"),
        ("S05", "Extreme low worm's eye angle looking up.", "The opponent doubled over at the waist after a body shot, hands dropping toward the right ribs, head bowed; the main character stepping back in guard.", "ho"),
        ("S06", "Over the shoulder of the main character (back of the main character's head and shoulder in the near foreground).", f"Opponent facing camera, {m.GHIGH}, ribs exposed below the elbows.", "ho"),
        ("S07", "High overhead bird's eye view looking straight down.", "Both fighters in orthodox stance facing each other, feet on the ground, gloves up.", "ho"),
        ("S08", "First person point of view through the opponent's eyes.", "The main character in front of camera throwing a LEFT jab straight toward the camera, the black glove large in the foreground, right glove at the chin.", "h"),
        ("S09", "Extreme close up on the main character's face.", "Completely blank smooth face with ONLY two small slanted white eyes, eyes narrowed and focused, gloves at the chin.", "h"),
        ("S10", "Medium side shot, eye level.", "The main character throws a RIGHT straight (cross): rear foot pivoted with the heel turned out, hips and shoulders turned forward, right arm fully extended straight to the opponent's chin, left glove at the chin. " + f"Opponent {m.GUARD}.", "ho"),
    ]
    out = []
    for sid, cam, action, people in S:
        cast = m.HERO + " " + (m.OPP if people == "ho" else "Draw ONLY the main character, exactly once.")
        prompt = " ".join([m.STYLE, "CAMERA: " + cam, "ACTION: " + action, cast, ho if people == "ho" else "", m.NOFX, "Wide 16:9 frame."])
        out.append({"id": sid, "camera": cam, "action": action, "people": people, "prompt": " ".join(prompt.split())})
    return out

def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
def mime(p): return "image/png" if str(p).endswith(".png") else "image/jpeg"

def http(url, data=None, headers=None, method="POST", timeout=300):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()

# ---------------- adapters ----------------
# Each returns (png_bytes, info dict). Prices are list prices at the time of writing; the run log
# records the model's own usage numbers when the API returns them, so the report uses actuals.

def gemini(model, price):
    def run(sc, refs, pose):
        key = os.environ.get("GEMINI_API_KEY", "proxy-injected")
        parts = [{"text": sc["prompt"] + (" Match the body pose of the attached stick figure skeleton exactly (it is a pose guide only, do not draw it)." if pose else "")}]
        for p in refs + ([pose] if pose else []):
            parts.append({"inline_data": {"mime_type": mime(p), "data": b64(p)}})
        body = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
        st, raw = http(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                       json.dumps(body).encode(), {"Content-Type": "application/json", "x-goog-api-key": key})
        j = json.loads(raw)
        for part in j["candidates"][0]["content"]["parts"]:
            d = part.get("inlineData") or part.get("inline_data")
            if d: return base64.b64decode(d["data"]), {"usage": j.get("usageMetadata"), "list_price": price}
        raise RuntimeError("no image in response: " + raw[:300].decode(errors="ignore"))
    return run

def openai_img(model, price):
    def run(sc, refs, pose):
        key = os.environ.get("OPENAI_API_KEY", "proxy-injected")
        bnd = "----fpbench"; body = io.BytesIO()
        def field(n, v): body.write(f"--{bnd}\r\nContent-Disposition: form-data; name=\"{n}\"\r\n\r\n{v}\r\n".encode())
        field("model", model); field("size", "1536x1024"); field("quality", "high")
        field("prompt", sc["prompt"] + (" Match the body pose of the attached stick figure skeleton (pose guide only, do not draw it)." if pose else ""))
        for p in refs + ([pose] if pose else []):
            body.write(f"--{bnd}\r\nContent-Disposition: form-data; name=\"image[]\"; filename=\"{Path(p).name}\"\r\nContent-Type: {mime(p)}\r\n\r\n".encode()); body.write(Path(p).read_bytes()); body.write(b"\r\n")
        body.write(f"--{bnd}--\r\n".encode())
        st, raw = http("https://api.openai.com/v1/images/edits", body.getvalue(), {"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={bnd}"})
        j = json.loads(raw)
        return base64.b64decode(j["data"][0]["b64_json"]), {"usage": j.get("usage"), "list_price": price}
    return run

def fal(endpoint, price, use_pose=False, extra=None):
    """fal.ai synchronous endpoint. Images go as data URIs."""
    def run(sc, refs, pose):
        key = os.environ.get("FAL_KEY", "proxy-injected")
        urls = [f"data:{mime(p)};base64,{b64(p)}" for p in refs]
        body = {"prompt": sc["prompt"], "image_urls": urls, "output_format": "png"}
        if use_pose and pose:
            body["controlnets"] = [{"path": "union", "control_image_url": f"data:image/png;base64,{b64(pose)}", "conditioning_scale": 0.7, "control_mode": "pose"}]
        body.update(extra or {})
        st, raw = http(f"https://fal.run/{endpoint}", json.dumps(body).encode(), {"Authorization": f"Key {key}", "Content-Type": "application/json"}, timeout=600)
        j = json.loads(raw); url = j["images"][0]["url"]
        img = base64.b64decode(url.split(",", 1)[1]) if url.startswith("data:") else urllib.request.urlopen(url, timeout=120).read()
        return img, {"seed": j.get("seed"), "list_price": price}
    return run

MODELS = {
    # Grok's current default (via ElevenLabs) is the Gemini 3.1 Flash Image family; included as the baseline.
    "nano-banana-2":     gemini("gemini-3.1-flash-image-preview", 0.067),
    "nano-banana-pro":   gemini("gemini-3-pro-image-preview", 0.134),
    "gpt-image-2":       openai_img("gpt-image-2", 0.21),
    "flux-2-max":        fal("fal-ai/flux-2-max/edit", 0.10),
    "flux-kontext-max":  fal("fal-ai/flux-pro/kontext/max/multi", 0.08),
    # filled in after LoRA training: fal("fal-ai/flux-general", ..., use_pose=True, extra={"loras": [...]})
}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("--out", required=True); ap.add_argument("--models", default="")
    ap.add_argument("--scenes", default=""); a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    m = blocks(); S = scenes(m)
    if a.scenes: S = [s for s in S if s["id"] in a.scenes.split(",")]
    if a.cmd == "plan":
        json.dump(S, open(out / "scenes.json", "w"), indent=1)
        for s in S: print(s["id"], len(s["prompt"].split()), "words", "pose:" + str((POSE_DIR / f"{s['id']}.png").exists()))
        return
    if a.cmd == "run":
        log = out / "runs.jsonl"
        for name in [x for x in a.models.split(",") if x]:
            fn = MODELS[name]; (out / name).mkdir(exist_ok=True)
            for s in S:
                dst = out / name / f"{s['id']}.png"
                if dst.exists(): continue
                pose = POSE_DIR / f"{s['id']}.png"; pose = pose if pose.exists() else None
                t0 = time.time()
                try:
                    img, info = fn(s, REFS, pose); dst.write_bytes(img); ok, err = True, None
                except urllib.error.HTTPError as e:
                    ok, info, err = False, {}, f"HTTP {e.code}: {e.read()[:300].decode(errors='ignore')}"
                except Exception as e:
                    ok, info, err = False, {}, repr(e)[:300]
                rec = {"model": name, "scene": s["id"], "ok": ok, "seconds": round(time.time() - t0, 1), "pose": bool(pose), **info, "error": err}
                open(log, "a").write(json.dumps(rec) + "\n"); print(json.dumps(rec)[:200])
                if not ok and "HTTP 40" in (err or ""): break  # auth or quota problem: stop this model
        return
    if a.cmd == "sheet":
        from PIL import Image, ImageDraw, ImageFont
        f = ImageFont.truetype(str(HANDOFF / "ASSETS/fonts/BebasNeue-Regular.ttf"), 40)
        names = sorted(d.name for d in out.iterdir() if d.is_dir())
        for s in S:
            tiles = [(n, out / n / f"{s['id']}.png") for n in names if (out / n / f"{s['id']}.png").exists()]
            if not tiles: continue
            W, H = 768, 432; sheet = Image.new("RGB", (W * len(tiles), H + 50), "white"); d = ImageDraw.Draw(sheet)
            for i, (n, p) in enumerate(tiles):
                sheet.paste(Image.open(p).convert("RGB").resize((W, H)), (i * W, 50)); d.text((i * W + 10, 4), n, font=f, fill="black")
            sheet.save(out / f"sheet_{s['id']}.jpg", quality=88); print("sheet", s["id"], [n for n, _ in tiles])

if __name__ == "__main__":
    main()
