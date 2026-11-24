# Session handoff (overwrite at the end of every session; keep under 30 lines)

Session 2026-11-24 (cloud, branch `claude/determined-cannon-ry2m6g`).

State
* Liver v4 fix PAUSED: ElevenLabs credits 0 and Sean said no paid generation without approval.
* Inspector `combat-anatomy-specialist` certified (run 4). Rules added this session: beat required, limb census, measured shovel height.
* 106 stills: 28 PASS (hash cache memory/visual-failures/approvals.json; new approved files in production/liver_v4/approved/), 78 to fix. All 55 candidates inspected; generated hooks and shovels 0 of 38 (do not repeat those methods; see LESSONS_LEARNED).
* V18 and V31 redesigned without generation: production/liver_v4/redesign_v18_v31.md.
* Cheaper method research: memory/TOOLS_AND_SKILLS.md "Research already done".

Blender character track (newest)
* Hero model attempts FAILED (specialist FAIL, creative director REVISE). Do not reuse hero_model.py / hero_mh.py approaches. Next: MPFB2 professional base (needs permission to install it as a Blender extension), then inspections, then Sean's approval before any rigging or combat.

Next (needs Sean)
1. Sean picks a method and approves spend (masked arm inpainting, 1K edits, free arm compositing, reuse with motion graphics).
2. Rebuild working dirs if the container reset: Remotion project from CLAUDE-EXPORT (attach the handoff repo, worktree the branch; base layers mk_bases logic: resize to 1920x1080, repaint flat background to #C4D6C4; lines with Grok build.lines at timeline glove points).
3. Fix, inspect (vfl.py), splice changed shot frame ranges into liver_v3_final.mp4 with original audio, vfl.py render + gate, VCD review, deliver to Sean. Never upload.
