# Session handoff (overwrite at the end of every session; keep under 30 lines)

Session 2026-11-24 (cloud, branch `claude/determined-cannon-ry2m6g`).

Done
* Merged Claude's production code into this branch; built `production/vfl/` (Visual Failure Library: harvest, screeners, cache, verdicts, certification, gate).
* Audited all QA reports, ledgers, lessons and Sean feedback: 249 documented failures, 147 with original images, 98 blind test eligible, in `memory/visual-failures/` (45 classes, CHECKLIST.md, INDEX.md).
* Added Sean's 4 liver v3 examples (VFI-0150 to VFI-0153) with render frames, his screenshots and source stills.
* Built this memory system; copied the vault's 5 skills and 2 subagents into `.claude/` so they load natively.

In progress / next
* Certify `combat-anatomy-specialist` (`vfl.py certify make`), then reinspect liver v3 per `memory/workflows/visual-qc.md`. Nothing has been delivered or uploaded.
* The liver v3 render lives on the handoff repo branch `claude/fight-playbook-youtube-ccyjcd` in `CLAUDE-EXPORT/` (attach that repo, clone, `git worktree add` the branch).

Watch out
* This repo is PUBLIC (Sean's choice 2026-11-24): no credentials, tokens or emails.
* Engine `qc.py` still passes rig poses the specialist rejects (pending task 3).
