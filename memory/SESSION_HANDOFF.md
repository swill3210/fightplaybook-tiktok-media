# Session handoff (overwrite at the end of every session; keep it short)

Last session: 2026-11-24, cloud, branch `claude/determined-cannon-ry2m6g` (repo fightplaybook-tiktok-media, PUBLIC). Nothing uploaded or published.

## Active track: Blender hero character (design only; Sean must approve before rigging, combat or animation)
* Method and gates: `memory/workflows/blender-character.md`. Failed approaches (do not repeat): `production/blender/README_FAILED_APPROACHES.md`, evidence `production/blender/failed_attempts/`, library VFI-0487 to VFI-0491.
* Fresh container first: `bash production/blender/setup_blender.sh` (pip bpy, Mesa EGL, MPFB2 clone to /tmp/claude-0/bl/mpfb2 and install as a Blender extension; Sean approved MPFB2 2026-11-24).
* Current script: `production/blender/hero_mpfb.py OUTDIR` (MPFB2 body: macros + region targets; default rig; `a_pose()` lowers the arms through the rig; `outline()` inverted hull ink; frames from the evaluated mesh). Stage 1 body render was clean (no holes); the A pose + outline run was interrupted before review, so rerun and check it first.
* Shared helpers: `production/blender/hero_model.py` (`toon()`, `scene()`, VIEWS, colours `C`). Reference: `.claude/skills/fight-playbook-rules/main_character_reference.jpg`.
* Next, in order: (1) rerun hero_mpfb.py, compare with the reference; (2) faceless head (remove features with targets and smoothing, keep jaw and ears) + eye decals; (3) offset shell shirt and loose shorts, red yoke, side stripes, hem V notches as decals; (4) padded MMA gloves with knuckles and red strap; (5) 2 tone cel + bold outer and thin interior ink; (6) both inspectors on front, right, left, back, three quarter; (7) send to Sean; (8) only after approval: opponent (red tank, black shorts, plain gloves, about 1.08x) and combat poses.

## Paused track: liver long form v4 fix
* Blocked: ElevenLabs credits 0; no paid generation without Sean's approval.
* 28 of 106 stills PASS (hash cache `memory/visual-failures/approvals.json`; new approved files `production/liver_v4/approved/` V20, V27, V74); 78 to fix. Verdicts `production/liver_v4/verdicts/`, beats `production/liver_v4/beats.json`, manifest `production/liver_v4/manifest.json` (paths into the handoff repo), plan `production/liver_v4/vcd_plan.md`, V18/V31 redesign `production/liver_v4/redesign_v18_v31.md`.
* Generated hooks and shovels: 0 of 38 passed; do not repeat those methods. If the Blender route is approved, redo the failed combat stills from Blender.
* Source render and timeline: handoff repo branch `claude/fight-playbook-youtube-ccyjcd`, folder `CLAUDE-EXPORT/` (attach the repo, `git worktree add` the branch). Splice plan: re-render only changed shot frame ranges with the Remotion project rebuilt from CLAUDE-EXPORT/CODE/longform-remotion (base layers: still resized to 1920x1080, flat background repainted #C4D6C4; lines via Grok build.lines at timeline glove points), keep the original audio.

## QC state
* Primary inspector `combat-anatomy-specialist` certified (run 4, 16/16). Added rules live in `.claude/agents/combat-anatomy-specialist.md`; editing it voids certification (re-run `vfl.py certify`).
* Open Sean decisions: C2, C6, C7, C9, C14, C15, C16, C17 (PROJECT_STATE.md).
