# Workflow: visual QC (token lean, mandatory for every still, clip and render)

Approved by Sean 2026-11-24 (Visual Failure Library + token efficiency orders). Tool: `production/vfl/vfl.py`. Library: `memory/visual-failures/`.

## Rules
* Load only `memory/visual-failures/CHECKLIST.md` (all mandatory visual rules, about 1,700 tokens). Open `classes/<CODE>.md` or `vfl.py show CODE` only for the codes in play. Never load `registry.json`.
* One primary inspector: `combat-anatomy-specialist`. A second inspector only for UNSURE items (second opinion UNSURE = FAIL).
* Cheap first: programmatic screeners (known defect hash match, edge contact, skin colour, render flash/empty/freeze) run before any AI call. A clean screen is never an approval: anatomy and technique always need the inspector.
* Each unique still is inspected once. Its verdict is cached by sha256 in `memory/visual-failures/approvals.json`. Reinspect only when the file changes (regenerated, edited, recropped) or is marked questionable (`--recheck`).
* Regenerate only the failed still. Never rebuild a scene or video to fix one image. A replacement is a new file hash, so it is inspected automatically.
* Inspector replies one line per asset, nothing else: `V71 PASS` | `V71 FAIL F03,G01 glove under shirt` | `V71 UNSURE B03 elbow hidden`. Unknown pattern: `V71 FAIL NEW short description` (creates a pending class).
* Every FAIL is written to the library automatically and deduplicated (same image or same project+shot+class adds an occurrence instead of a new entry).
* Generation, animation and render tools refuse to run until `vfl.py checklist --role <role>` has been run in the session (`require_ack`).

## Steps
1. `python3 production/vfl/vfl.py checklist --role qc`
2. Write a manifest JSON `{asset_id: path}` for the video's unique stills.
3. `vfl.py status manifest.json`: cached PASS skipped; hard FAILs recorded; prints what needs eyes.
4. `vfl.py sheet manifest.json --out DIR`: 2x2 labelled sheets of only those assets (`--full` for single full size, used for escalations and close ups).
5. Inspector (one Agent call per batch of sheets, prompt = checklist + sheet paths) returns terse lines. Save to a file.
6. `vfl.py verdict manifest.json lines.txt --project "<video>"`: caches, records failures, prints ESCALATE list. Escalate those at `--full` to the second inspector, then `verdict ... --inspector visual-inspector-second-opinion`.
7. Regenerate failed stills only (rig pose + redraw for combat), repeat 3 to 6 for the new files.
8. Render, then `vfl.py render out.mp4 --timeline timeline.json --exempt V102,V107` (flash, empty, freeze, edge crops added by camera moves). Inspect only the flagged frames plus one 2x2 sheet per transition cluster.
9. `vfl.py gate manifest.json --video out.mp4 --inspector-file .claude/agents/combat-anatomy-specialist.md`. GATE: PASS is required before anything goes to Sean. The visual-creative-director render review (CLAUDE.md standard) still runs after the gate, with the same terse format.

## Certification (inspector must not approve a known defect)
`vfl.py certify make --n 16` builds a blind set from documented defects (Sean's cases first, one per class). Inspector answers with the terse format; `vfl.py certify score answers.txt --worker combat-anatomy-specialist --worker-file .claude/agents/combat-anatomy-specialist.md`. Any PASS on a defect = FAIL: improve the inspector's instructions, re certify. Editing the agent file voids the certification (hash check in `gate`).
