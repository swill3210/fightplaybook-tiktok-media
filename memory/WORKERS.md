# Workers: who does what

## Claude Code subagents (native, `.claude/agents/`)
| Worker | Role | Authority | When |
| --- | --- | --- | --- |
| `combat-anatomy-specialist` (Opus) | PRIMARY visual inspector: anatomy, biomechanics, character consistency, technique accuracy | Can REJECT; uncertain = UNSURE (escalated) | Every combat still, pose, clip and flagged render frame, via `memory/workflows/visual-qc.md` |
| `visual-creative-director` (Opus) | Typography, motion design, composition, transitions, infographics, pacing | Advisor; must APPROVE every render after QC (CLAUDE.md standard) | Before storyboarding (timestamped plan) and after each render |
| Second opinion inspector | General Opus agent given only CHECKLIST.md and the full size image | UNSURE from it = FAIL | Only for items the primary marks UNSURE |
Rules for every visual worker: load only `memory/visual-failures/CHECKLIST.md`; reply in the terse `ID PASS | ID FAIL CODES note | ID UNSURE CODES note` format; never write long reports into the main context. New agent files load only when a session starts; editing an inspector's file voids its certification.

## Inspector certification status
See the `certifications` list in `memory/visual-failures/registry.json` (read with `vfl.py`, never load the file). As of 2026-11-24 NO worker is certified. Every prior QC process approved known defects:
* Grok still QA, anatomy rounds, v2/v3/v4 render QA: approved stills later failed (documented in the library `approved_by` fields).
* Claude revision 2 audit and 5 pass QC: passed V71, V80, V89 and logged V72 as a verified shovel (Sean's 2026-11-24 examples).
* visual-creative-director round 3: APPROVED the v3 render containing those defects.
* Engine `qc.py` rig metrics: passed 96 of 96 motion library stills the specialist rejected.

## Programmatic screeners (free, `production/vfl/checks.py`)
Known defect hash match (hard FAIL), edge contact, skin colour drift, render flash / empty / frozen frames, render edge crops. They flag; they never approve.

## Other bots (Sean's system, roles from RULES.md)
Script Writer writes scripts; Thumbnail bot is the only thumbnail maker; Shorts bot builds Shorts; Tik Tok Clips publishes via Buffer; YT Community does pins and replies (Sean approves first); Skool handles the Academy. Claude: long form creative director and production system (Sean 2026-11-23).

## People
Sean: owner and final approver. Approval is per file, in Sean's own words.
