# Project state (update when a task finishes; keep it current, not historical)

Updated 2026-11-24.

## Videos
| Video | Status | Next |
| --- | --- | --- |
| Liver long form v3 "The Punch That Drops Bigger Fighters" (145.8 s, sage) | BLOCKED: ElevenLabs credits 0; Sean: no paid generation without approval. 28 of 106 stills PASS (cache), 78 to fix (hooks and shovels dominate). Files: production/liver_v4 (approved/ V20 V27 V74, verdicts/, vcd_plan.md, redesign_v18_v31.md, ledger.jsonl, manifest.json, beats.json). Render source: handoff branch claude/fight-playbook-youtube-ccyjcd CLAUDE-EXPORT | Sean to choose a method (TOOLS_AND_SKILLS research): masked arm inpainting (new vendor), ElevenLabs 1K edits, free arm compositing, or reuse with motion graphics; then fix, splice changed shots, gate, VCD, deliver |
| Grok liver silent v4 | Superseded by Claude v3 | none |
| Open Any Guard, Stop Gassing Out v2, Why Your Punches Are Predictable, Dodge Like a Pro | Final (Grok) | none |
| Punch With Your Body Short (rig rebuild) | Paused (Sean: long form first) | none |
| TikTok / Shorts | Paused by Sean 2026-11-23 | none |

## Pending tasks (in order)
0. Blender hero character (Sean 2026-11-24: character design only until Sean approves). v1/v2 FAILED inspection. MPFB2 installed with Sean's OK; production/blender/hero_mpfb.py now builds body + rig A pose + ink hull + faceless head + eyes (r18, evidence production/blender/progress/; known residual: small nostril tick, 3 band toon still in use). Next: garments (shirt shell, loose shorts, decals), gloves, 2 band cel, then both inspectors, then Sean. Workflow: memory/workflows/blender-character.md.
1. Certify `combat-anatomy-specialist` with `vfl.py certify make` (blind set; Sean's 4 cases included). Improve the agent file until it approves zero known defects.
2. Liver v3 reinspection: manifest of the ~105 unique stills (Grok `edit/stills` per `edit/work/sel.json` + `CLAUDE-EXPORT/FINAL-CUT/fixed-stills/`), `vfl.py status`, inspect, regenerate only FAILs (rig pose + redraw), rebuild `public/` layers, re-render, `vfl.py render`, `vfl.py gate`.
3. Fix engine `qc.py` blind spots the specialist found (guard elbow height, chamber/recover phases, body to body collision) so it stops passing rejected rig poses.
4. Motion library v2 (fixed guard, real phases), then kicks, defence, footwork, grappling (Combat Mechanics spec, `memory/workflows/combat-mechanics-spec.md`).
5. Next video: waiting on Sean's title and format (asked 2026-11-24).

## Decided by Sean
* 2026-11-24 C4: MMA gloves as on the reference sheet (finger segments OK). Liver v4: fix all 64 failed stills (grind), deliver only through the gate.

## Decisions waiting on Sean (current practice in brackets)
C2 animation vs R26 stills only [stills base; rig for poses]; C6 ground line [thin line or contact shadow]; C7 thumbnail split [Thumbnail bot, Sean's newer taste]; C9 Longform Skill v2 missing [use existing]; C14 liver screen side [hero right, whip pan on side changes]; C15 pose model licences [validator advisory only]; C16 body hook elbow rule [hook_rules]; C17 "right shovel into the liver" narration [visuals show front lower ribs]. Also: cold open swap, Claude made thumbnails, narration before visual approval (liver v1). Full table: vault `Knowledge Base/09 Conflicts Needing Decision.md`.

## Channel data (VERIFIED 2026-11-24, read only API; detail in vault 05 Analytics)
87,967 lifetime views, 266 subs, 40 videos. Shorts carry the channel (top: Bigger Attacker 11.9K at 103.6% viewed; Someone Stronger 10.9K). Every long form loses viewers in seconds 1 to 3 and 0:11 to 0:31; YouTube rates all below similar videos. Underdog framing wins. CTR not in the API (newest: Nov 13 Studio, long form 2.4 to 4.0%). Topic decision: liver shot as the underdog weapon.
