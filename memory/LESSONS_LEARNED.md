# Lessons learned (newest first; append, never delete; one line each, cite the source)

Full history: vault `Knowledge Base/08 Mistakes and Lessons Learned.md`, handoff `LESSONS-LEARNED.md`. Defect specifics live in `memory/visual-failures/` (do not repeat them here).

## What works (methods proven on real builds)
* 2026-11-24 Old ElevenLabs generations stay retrievable for free: `GET /v1/flows/image/{generation_id}` returns a fresh signed `content_url`. Every ledger (`ledger_*.json`) maps file names to generation ids, so rejected originals can be recovered (9 of about 160 returned 404).
* 2026-11-24 Rig pose redraw: passing the 3D rig render FIRST with "REDRAW THE FIRST IMAGE, keep every limb angle, change only the rendering" made Nano Banana 2 draw a correct 90 degree body hook (1,224 credits, 22 s). Nano Banana Pro ignored it. 7 of 13 hooks passed first time, 11 of 13 after one retry.
* 2026-11-24 Hard poses (shovel): arm only edits of the closest correct image ("change ONLY the right arm: elbow down at the own hip, forearm straight up like a pillar") beat fresh prompts in every model. Check existing passing stills before generating.
* 2026-11-24 Never redraw extreme close ups from the rig (mannequin look leaks); crop a passing wide still instead. Add an explicit LAYOUT line (who is on which side, exactly two people) or the model swaps sides.
* 2026-11-24 Character consistency was excellent on every model when the reference sheet was attached; arms were the failure, not identity.
* 2026-11-24 An independent visual review after every render pays off (creative director caught empty frames, headlines over heads, a forbidden flash, narration echo).
* 2026-11-23 Narration first, then retime visuals to the real voice (ElevenLabs with-timestamps, previous_text/next_text); Remotion compositor with word timed kinetic type, counters and parallax (`production/longform-remotion`).
* 2026-11-23 Grok era: fixed prompt blocks (STYLE, HERO, OPP, arm mechanics, KEEP, NEG, HOOK_L/HOOK_BODY/HOOK_NEG) with screen side wording; edits from an already correct still; ledger for every generation; checkpoints after every round.
* 2026-11-23 Rig: over the shoulder contact shots (profiles of the faceless head read as the back of the head); amber outline highlight instead of emissive glow; hook range 0.50 m gives 99 degrees; snap back needs the guard point moved forward.

## What failed (root causes)
* 2026-11-24 Blender character model (hero) FAILED both inspectors after 10 render passes: primitives, metaballs, voxel unions and a hacked MakeHuman mesh (no rig, fake heroic scaling, fragment garment shells) gave mannequin proportions, skin through the shorts, a mouth like neck seam and blotchy shading. Full write up: production/blender/README_FAILED_APPROACHES.md (also in the vault). Next attempt must use MPFB2 (professional base mesh, targets, rig with weights), offset shell garments, texture decals, 2 band Shader to RGB and Line Art.
* 2026-11-24 Liver v4 candidate rounds: generated hooks and shovels 0 of 38 passed (rig pose REDRAW, reference image REF mode, plain text with geometry wording, Nano Banana 2). Failure modes: straight arm 150 to 170 degrees, wrong (right) arm, glove at chest height, tangled bodies. Do not repeat these methods for hooks or shovels; next try masked arm inpainting or arm compositing on approved stills.
* 2026-11-24 Eye direction edits on the faceless head (V18, V31): 0 of 4; edits add brow lines (E01). Show gaze with camera tilt and graphics instead.
* 2026-11-24 Whole image edits drift outside the asked change (V12 first try stripped the hero's straps); always state what must stay ("KEEP ... exactly").
* 2026-11-24 The certified inspector (16 of 16 on the blind set) still passed V54 (opponent missing his right arm) and V95 (opponent's arm shrunk, opponent too large); Claude also picked both as good reference bases. Cause: inspection focused on the punching arm and contact, not every limb of every character. Fix: mandatory limb census and scale check per character (agent file), V54/V95 added to the certification set; never use a still as a generation base until it passes the census.
* 2026-11-24 Sean found 4 critical defects (1:26, 1:35, 1:36, 1:48) in liver v3 that had passed Grok QA, Claude's 51 still audit and 5 pass QC, and the creative director's APPROVE. Cause: whole frame review at 640 to 720 px, trusting stills that passed earlier rounds, no check for "glove hidden under clothing", "limb traced to a body", "eye side vs body orientation". Fix: Visual Failure Library + certified primary inspector + cached hash approvals (`memory/workflows/visual-qc.md`).
* 2026-11-24 Metrics only check what they measure: rig metrics passed 96 of 96 motion library stills that the specialist rejected; 86 of 528 in between frames interpenetrated. Check every frame, not key poses.
* 2026-11-24 Pose estimation alone is unreliable on stylised art (a correct hook from behind reads 171 degrees in 2D); only same camera comparison with the rig separates good from bad, with a thin margin.
* 2026-11-24 Image models default to straight arms for body punches and hooks in every model tested.
* 2026-11-24 Raw OpenPose skeletons passed to image models leak in as ghost figures; use mannequin renders.
* 2026-11-24 Renders and working files in `/home/user/fp-longform` were not committed; the container reset would have lost liver v3. Sean recovered it via CLAUDE-EXPORT. Commit or export every deliverable.
* 2026-11-24 A stopped render process kept running and produced a stale file that was nearly delivered.
* 2026-11-24 ElevenLabs balance hit 0 mid batch; harnesses must skip finished images so resuming costs nothing.
* 2026-11-23 Lenient QA (whole frames, borderline passed) missed defects Sean caught at 0:04, 0:21, 0:32, 0:37, 1:15, 1:56, 2:02; a strict zoomed audit then failed 37 "passing" stills; all 25 hooks failed the hook rules audit after that.

## Environment discoveries
* 2026-11-24 ElevenLabs quota (2,781,816) exhausted during liver v4 regeneration; the API answers 401 with code quota_exceeded. Check with a tiny POST before a big batch.
* 2026-11-24 Liver v4 round 1: 0 of 14 hook candidates passed (rig pose redraws and V36 reference generations); models draw the hero's RIGHT (far) arm or a straight arm when the hero is on screen right facing left. Edits of near correct stills remain the best bet.
* rtmlib pose weights: download.openmmlab.com unreachable from cloud sessions (2026-11-24); huggingface.co reachable. Pose model licence question open (C15).
* ElevenLabs key lacks `user_read`: credit balance cannot be read; stop and report only on an actual quota error.
* Cloud containers are ephemeral: anything not pushed to GitHub is lost.
