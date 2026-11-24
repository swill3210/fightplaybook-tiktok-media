---
type: workflow
format: long-form
updated: 2026-11-24
---
# Workflow: long form YouTube

Master recipe (verbatim, authoritative): `Fight Playbook Long Form/03 Skills/Longform Build and AB Test (Grok)/skill-draft.md`. Rules: R1 to R15, R22 to R28, R38 to R45 in `RULES.md`.

1. Intake: Sean sends a per verb shot spec (V1..Vn: times, beat, start pose, end pose, visible change, camera, text) and a VO script. Save verbatim. Wait for "start". A newer script replaces the old one; never merge.
2. Plan: parse the spec into a shot plan; count angles per minute (at least 10, no back to back repeats, no more than two wide eye level side shots in a row).
3. Prompts: fixed blocks STYLE, HERO, OPP, arm mechanics block per punch, KEEP, NEG, HOOK_L / HOOK_BODY / HOOK_NEG; name the arm by image side.
4. Stills on ElevenLabs with the character reference; per still zoom QA (borderline fails); ledger every generation. Candidate improvement under test: rig render as the image to redraw for punches (see Lessons 2026-11-24).
5. Silent build (1920x1080, 30 fps): motion layer (eased camera by angle type, two phase strikes, contact push and shake, speed lines in code, door tracker, section push transitions, word by word summary board). Big top text only, no bottom caption bar.
6. Render QA (R28) frame by frame, slow motion on every punch, hook pass; write qa_report.md.
7. Send Sean the silent cut. Narration only after he approves the visuals (Ryan Kurk, eleven_v4; never speed up the voice; retime visuals instead).
8. Mix: lofi bed, about -14 LUFS, at or under -2 dBTP; SFX only with an approved sound map; subscribe ask at the end (C1).
9. Title, description (disclaimer verbatim, Skool FREE line, chapters, 1/2/3 comment CTA, never "AI" or "animated"); thumbnail from the Thumbnail bot (R38) unless Sean asks otherwise.
10. Draft upload only when Sean asks (Private, no schedule, R44); A/B test only when asked.

## Gates added 2026-11-24 (Sean)
1. Script and visual guidelines ready: consult `visual-creative-director` for the timestamped visual plan.
2. Every combat pose starts from the 3D rig; stills are rig pose plus redraw (never text alone for combat).
3. Every combat still or clip: `validate.py` with the rig reference, then `combat-anatomy-specialist` APPROVE (uncertain = rejected).
4. After the render and 5 pass QC: `visual-creative-director` review, fix, re render until APPROVE; then deliver to Sean.

