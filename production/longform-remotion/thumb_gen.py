import json, base64, time, urllib.request, sys, importlib.util
from pathlib import Path
H = Path("/home/user/the-fight-playbook-claude-handoff"); L = H / "VIDEO-PROJECTS/target-the-liver-in-boxing/edit"
spec = importlib.util.spec_from_file_location("p", L / "prompts.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
refs = [H / "CHARACTERS/main_character_reference.jpg", H / "CHARACTERS/pair_ref_hero_vs_opponent.jpg"]
sel = json.load(open(L / "work/sel.json"))
base = "YouTube thumbnail, single full frame action shot, very tight framing, big bold shapes readable at phone size, characters fill the frame, leave the TOP THIRD of the frame plain flat sage for big text added later. "
C = {
 "A_pov": (base + "FIRST PERSON point of view of the opponent looking down at their own red tank top: the main character's black MMA glove with red wrist strap is buried in the right side of the ribs (the liver) in the lower half of the frame, red shirt denting around the knuckles, the main character's face close behind the glove looking up at camera with BIG bright slanted white eyes, thin black horizontal speed lines behind the glove.", [L / "stills" / f"{sel['V35']}.png"]),
 "B_fold": (base + "Low angle close up: the much BIGGER opponent in red folding forward at the waist, hands dropping to the right ribs, head bowed; the smaller main character in front, left hook just landed in the liver with the elbow bent 90 degrees in an L, eyes BIG and bright, thin black horizontal speed lines.", [L / "stills" / f"{sel['V4']}.png"]),
 "C_size": (base + "The opponent is HUGE, towering over the much smaller main character; the main character is crouched low driving a LEFT hook into the giant's right ribs (liver), elbow bent 90 degrees in an L, the giant's eyes wide in shock, both faces only two slanted white eyes, thin black horizontal speed lines.", [L / "stills" / f"{sel['V34']}.png"]),
}
def b64(p): return base64.b64encode(Path(p).read_bytes()).decode()
for name, (scene, extra) in C.items():
    if Path(f"{name}.png").exists(): continue
    prompt = " ".join([m.STYLE, scene, m.HERO, m.OPP, m.ONCE["ho"], m.NOFX.replace("speed lines, ", "")])
    imgs = [{"type": "inline_base64", "content_base64": b64(p), "mime_type": "image/jpeg" if str(p).endswith("jpg") else "image/png"} for p in refs + extra]
    body = {"model_id": "gemini-3.1-flash-image", "prompt": prompt, "images": imgs, "aspect_ratio": "16:9", "resolution": "2K"}
    rq = urllib.request.Request("https://api.elevenlabs.io/v1/flows/image", json.dumps(body).encode(), {"xi-api-key": "proxy-injected", "Content-Type": "application/json"})
    gid = json.loads(urllib.request.urlopen(rq, timeout=120).read())["id"]
    while True:
        time.sleep(3); j = json.loads(urllib.request.urlopen(urllib.request.Request(f"https://api.elevenlabs.io/v1/flows/image/{gid}", headers={"xi-api-key": "proxy-injected"}), timeout=60).read())
        if j["status"] == "completed": Path(f"{name}.png").write_bytes(urllib.request.urlopen(j["content_url"], timeout=120).read()); print("ok", name); break
        if j["status"] == "failed": print("failed", name, j.get("failure_reason"), j.get("error_message")); break
