#!/usr/bin/env python3
"""Claude Code hooks for the project memory (memory/).

start: SessionStart. Prints the short session handoff so a new session knows where it stands (about 400 tokens).
stop:  Stop. Once per new set of changes, asks Claude to update memory/ when work changed outside memory/ but the
       memory files were not touched. Stays quiet otherwise (no loops).
"""
import hashlib, os, subprocess, sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[1]))
MEM = ROOT / "memory"


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout


def start():
    h = MEM / "SESSION_HANDOFF.md"
    print("PROJECT MEMORY: follow CLAUDE.md. Latest handoff below; open other memory/ files only when the task needs them.")
    if h.exists():
        print(h.read_text()[:3500])
    else:
        print("memory/SESSION_HANDOFF.md missing: create it at the end of this session.")


def stop():
    st = git("status", "--porcelain")
    changed = [l[3:] for l in st.splitlines() if l.strip()]
    work = [f for f in changed if not f.startswith("memory/")]
    mem = [f for f in changed if f.startswith("memory/")]
    sig = hashlib.sha1((st + git("log", "-1", "--format=%H")).encode()).hexdigest()
    state = Path.home() / ".cache" / "fp_memory_stop"
    last = state.read_text().strip() if state.exists() else ""
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(sig)
    if sig == last:
        return
    if work and not mem:
        print("Project memory: work changed outside memory/ but no memory file was updated. If a task finished or something was "
              "learned, update memory/PROJECT_STATE.md, memory/SESSION_HANDOFF.md and (only for new knowledge, no duplicates) "
              "memory/LESSONS_LEARNED.md, then commit and push. If nothing worth keeping happened, just stop.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    {"start": start, "stop": stop}[sys.argv[1] if len(sys.argv) > 1 else "start"]()
