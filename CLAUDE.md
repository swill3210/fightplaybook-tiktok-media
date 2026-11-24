# The Fight Playbook: Claude startup instructions

This repo is the permanent home of project knowledge (no Obsidian needed). It is PUBLIC: never commit credentials, tokens or emails.

## Where knowledge lives (open only what the task needs)
| Need | File |
| --- | --- |
| Where we left off (shown at session start by a hook) | `memory/SESSION_HANDOFF.md` |
| Status, pending tasks, Sean's open decisions, active video files (`production/<video>/`) | `memory/PROJECT_STATE.md` |
| Permanent production rules | `memory/MASTER_RULES.md` (verbatim originals: skill `fight-playbook-rules`) |
| What worked and failed | `memory/LESSONS_LEARNED.md` |
| Workers, inspectors, bots | `memory/WORKERS.md` |
| Tools, skills, repos, finished research | `memory/TOOLS_AND_SKILLS.md` |
| Format workflows | `memory/workflows/` (long-form, shorts-tiktok, promos, visual-qc, analytics, combat-mechanics-spec) |
| Visual rules and failures | `memory/visual-failures/CHECKLIST.md`, then `INDEX.md` and `classes/<CODE>.md` for one code; never load `registry.json` (use `production/vfl/vfl.py show CODE`) |

## Mandatory
1. Before any video task: read MASTER_RULES.md and the one workflow for the format; load the matching skill.
2. All visual QC goes through `memory/workflows/visual-qc.md` (one certified inspector, hash cached approvals, terse PASS/FAIL codes, regenerate only failures, gate before delivery).
3. Never upload, publish, schedule or delete without Sean's own words. Honest answers; no dashes; gender neutral.
4. Before research, check TOOLS_AND_SKILLS.md "Research already done" and LESSONS_LEARNED.md.

## Keeping memory current
* Save an important discovery immediately in the right memory file. One line, dated, cited; search first and update the existing line instead of duplicating.
* When a task finishes: update PROJECT_STATE.md; at session end overwrite SESSION_HANDOFF.md (under 30 lines). Commit and push (containers are ephemeral; unpushed work is lost).
* Rules: never delete or weaken an approved rule or skill; mark superseded lines with the date and Sean's ruling.
* Native auto memory may be used for personal notes, but project knowledge belongs here. The Stop hook asks for a memory update when work changed but memory did not.
