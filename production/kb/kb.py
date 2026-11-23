#!/usr/bin/env python3
"""Fight Playbook knowledge base bridge (Obsidian vault in a private GitHub repo).

Safety rules enforced in code:
  * Claude writes ONLY inside <vault>/Claude Production. Everything else in the vault is read only.
  * Existing files are never overwritten. New notes get a unique dated name; Claude owned
    log notes are only appended to.
  * Before any push, the staged diff is scanned for credentials; a hit aborts the push.
  * Pull uses --ff-only, so it never rewrites Sean's history; a conflict stops and asks.

Commands:
  kb.py pull                       fetch Sean's latest notes from the vault repo
  kb.py brief [keywords...]        list the notes to read before planning (always read + keyword hits)
  kb.py capture KIND "Title" FILE  save FILE (markdown body) as a new dated note, then commit and push
                                   KIND: lesson error correction technique script research competitor analytics video
  kb.py log "text"                 append one line to the Claude change log, commit and push
  kb.py remind                     Stop hook: ask Claude once per change set to capture lessons
  kb.py check                      show vault status and run the secret scan

Vault location: $FP_VAULT (default /home/user/the-fight-playbook-brain)
"""
import datetime as dt, hashlib, os, re, subprocess, sys

VAULT = os.environ.get("FP_VAULT", "/home/user/the-fight-playbook-brain")
OWN = "Claude Production"
ROOT = os.path.join(VAULT, OWN)
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FOLDERS = {
    "lesson": "06 Learnings/Log", "error": "06 Learnings/Errors and Corrections", "correction": "06 Learnings/Errors and Corrections",
    "technique": "08 Techniques", "script": "03 Scripts", "research": "02 Research/Topics", "competitor": "02 Research/Competitors",
    "analytics": "05 Analytics/Reports", "video": "07 Videos",
}
ALWAYS = ["06 Learnings/Retention Findings.md", "06 Learnings/Hooks That Work.md", "06 Learnings/Animation Quality Lessons.md", "Production Dashboard.md"]
SECRET = re.compile(r"GOCSPX-|ya29\.|1//0[A-Za-z0-9_-]{20,}|\"refresh_token\"\s*:|\"client_secret\"\s*:|-----BEGIN [A-Z ]*PRIVATE KEY|AIza[0-9A-Za-z_-]{30,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|xox[bpa]-|(?i:password\s*[:=]\s*\S{6,})")

def git(*a, check=True):
    return subprocess.run(["git", "-C", VAULT, *a], capture_output=True, text=True, check=check)

def need_vault():
    if not os.path.isdir(os.path.join(VAULT, ".git")):
        sys.exit(f"vault repo not found at {VAULT}; clone it first or set FP_VAULT")

def today(): return dt.date.today().isoformat()

def safe_path(rel):
    p = os.path.realpath(os.path.join(ROOT, rel))
    if not p.startswith(os.path.realpath(ROOT) + os.sep):
        sys.exit(f"refusing to write outside {OWN}: {rel}")
    return p

CREATED, APPENDED = [], {}

def new_file(rel, text):
    p = safe_path(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    base, ext = os.path.splitext(p); n = 2
    while os.path.exists(p):
        p = f"{base} ({n}){ext}"; n += 1
    with open(p, "x") as f: f.write(text)
    CREATED.append(p)
    return os.path.relpath(p, VAULT)

def append(rel, line):
    p = safe_path(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    APPENDED.setdefault(p, os.path.getsize(p) if os.path.exists(p) else None)
    with open(p, "a") as f: f.write(line.rstrip() + "\n")
    return os.path.relpath(p, VAULT)

def undo_local():
    # remove only what this run created, and cut appended logs back to their old length
    for p in CREATED:
        if os.path.exists(p): os.remove(p)
    for p, size in APPENDED.items():
        if size is None:
            if os.path.exists(p): os.remove(p)
        else:
            with open(p, "r+") as f: f.truncate(size)

def commit_push(msg, paths):
    git("add", "--", *paths)
    diff = git("diff", "--cached").stdout
    if SECRET.search(diff):
        git("reset", "-q", "--", *paths); undo_local()
        sys.exit("ABORTED: something that looks like a credential is in the change. Nothing was committed.")
    outside = [f for f in git("diff", "--cached", "--name-only").stdout.split("\n") if f and not f.startswith(OWN + "/")]
    if outside:
        git("reset", "-q"); undo_local()
        sys.exit(f"ABORTED: staged files outside {OWN}: {outside}")
    if not diff.strip():
        print("nothing to commit"); return
    git("-c", "user.name=Claude", "-c", "user.email=noreply@anthropic.com", "commit", "-q", "-m", msg)
    r = git("push", "-q", check=False)
    if r.returncode:
        r2 = git("pull", "--rebase", "-q", check=False)
        r = git("push", "-q", check=False) if r2.returncode == 0 else r2
    print("pushed" if r.returncode == 0 else f"PUSH FAILED (committed locally): {r.stderr.strip()}")

cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
if cmd == "pull":
    need_vault()
    r = git("pull", "--ff-only", check=False)
    print(r.stdout.strip() or "up to date" if r.returncode == 0 else f"PULL STOPPED, needs Sean: {r.stderr.strip()}")
elif cmd == "brief":
    need_vault()
    print("ALWAYS READ before planning:")
    for rel in ALWAYS:
        p = os.path.join(ROOT, rel); print(f"  {'OK ' if os.path.exists(p) else 'MISSING '}{os.path.join(OWN, rel)}")
    reports = sorted(os.listdir(os.path.join(ROOT, "05 Analytics/Reports"))) if os.path.isdir(os.path.join(ROOT, "05 Analytics/Reports")) else []
    if reports: print(f"  OK {OWN}/05 Analytics/Reports/{reports[-1]}")
    kws = [k.lower() for k in sys.argv[2:]]
    if kws:
        hits = []
        for d, _, fs in os.walk(VAULT):
            if "/.git" in d or "/.obsidian" in d or "/.trash" in d: continue
            for f in fs:
                if not f.endswith(".md"): continue
                p = os.path.join(d, f)
                try: t = open(p, errors="ignore").read().lower()
                except OSError: continue
                score = sum(t.count(k) + 5 * f.lower().count(k) for k in kws)
                if score: hits.append((score, os.path.relpath(p, VAULT)))
        print(f"\nRELEVANT to {' '.join(kws)} (Sean's notes included, read only):")
        for s, rel in sorted(hits, reverse=True)[:15]: print(f"  {s:>4}  {rel}")
elif cmd == "capture":
    need_vault()
    kind, title, body_file = sys.argv[2], sys.argv[3], sys.argv[4]
    if kind not in FOLDERS: sys.exit(f"KIND must be one of {list(FOLDERS)}")
    body = open(body_file).read()
    head = f"---\ntype: {kind}\ndate: {today()}\nsource: Claude\n---\n# {title}\n\n"
    rel = new_file(f"{FOLDERS[kind]}/{today()} {re.sub(r'[\\\\/:*?\"<>|]', ' ', title)}.md", head + body)
    log = append("_Claude/Changelog.md", f"* {today()} {kind}: [[{os.path.splitext(os.path.basename(rel))[0]}]]")
    print("wrote", rel); commit_push(f"{kind}: {title}", [rel, log])
elif cmd == "log":
    need_vault()
    log = append("_Claude/Changelog.md", f"* {today()} {sys.argv[2]}")
    commit_push(f"log: {sys.argv[2][:60]}", [log])
elif cmd == "remind":
    # Stop hook. Ask once per new set of production changes, then stay quiet (no loops).
    r = subprocess.run(["git", "-C", PROJECT, "status", "--porcelain", "--", "production", ".claude"], capture_output=True, text=True)
    sig = hashlib.sha1((r.stdout + subprocess.run(["git", "-C", PROJECT, "log", "-1", "--format=%H"], capture_output=True, text=True).stdout).encode()).hexdigest()
    state = os.path.expanduser("~/.cache/fp_kb_remind")
    last = open(state).read().strip() if os.path.exists(state) else ""
    os.makedirs(os.path.dirname(state), exist_ok=True); open(state, "w").write(sig)
    if sig != last and os.path.isdir(os.path.join(VAULT, ".git")) and (r.stdout.strip() or last):
        print("Knowledge capture: if this task produced a verified finding, error, correction or lesson, save it with "
              "`python3 production/kb/kb.py capture <kind> \"<title>\" <file>` (writes only to Claude Production). "
              "If nothing worth keeping happened, just stop.", file=sys.stderr)
        sys.exit(2)
elif cmd == "check":
    need_vault()
    print(git("status", "-sb").stdout)
    tracked = git("ls-files").stdout.split("\n")
    bad = [f for f in tracked if re.search(r"(client_secret|token|credential|\.env|\.pem|\.key)", f, re.I)]
    print("sensitive looking tracked files:", bad or "none")
else:
    sys.exit(__doc__)
