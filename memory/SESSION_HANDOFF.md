# Session handoff (overwrite at the end of every session; keep under 30 lines)

Session 2026-11-24 (cloud, branch `claude/determined-cannon-ry2m6g`).

State
* Liver v4 fix in progress. Primary inspector `combat-anatomy-specialist` certified on run 4 (runs 1 and 3 failed; rules added: beat required, limb census, measured shovel height).
* 106 unique stills: 25 PASS (hash cache `memory/visual-failures/approvals.json`), 81 being regenerated. Sean ruled C4 (MMA gloves as on the reference sheet) and "grind all 64" (now 81).
* Creative director plan: `production/liver_v4/vcd_plan.md` (hero on screen right facing left, no side switches). Generation ledger: `production/liver_v4/ledger.jsonl`.
* Working files (rebuildable, not in git): /tmp/claude-0/liver (manifest, beats, sheets, candidates regen/ regen2/), /tmp/claude-0/lf (Remotion project rebuilt from CLAUDE-EXPORT timeline; base layers via mk_bases.py, lines via mk_lines.py).

Next
1. Inspect candidates (vfl.py sheet + specialist, terse lines), pick passing take per shot, regenerate only failures.
2. Replace stills in /tmp/claude-0/lf, rebuild their layers, render only changed shot frame ranges, splice into liver_v3_final.mp4 with the original audio.
3. vfl.py render + gate, creative director render review, then send to Sean. Never upload.
