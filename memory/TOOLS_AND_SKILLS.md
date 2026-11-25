# Tools and skills (what exists, how to run it; read the section you need)

## Skills (native, `.claude/skills/`; load the one the task needs)
| Skill | Use |
| --- | --- |
| `fight-playbook-rules` | Verbatim R1 to R49, hook_rules.md, CHARACTER_SPEC, background rotation, one verb one image law, reference images (`main_character_reference.jpg`, `pair_ref_hero_vs_opponent.jpg`, `punch_speed_lines_reference.jpg`). Load before any Fight Playbook task |
| `fight-playbook-long-form-build-and-a-b-test` | Grok's long form recipe (spec intake to Draft and A/B test) |
| `fight-playbook-video-build` | Silent first build, character lock, pose match per verb |
| `fight-playbook-fighting-technique-animation` | Technique library (jab, cross, uppercut, lead hook to liver, guard, catch, chin tuck, step off, clinch knee, biceps jam, combo) and arm mechanics |
| `fight-playbook-wild-punch-haymaker-animation` | Wild punches that must read as wild |
| `fight-playbook-production` | Claude's rig pipeline (engine commands, storyboard rules, QC gate) |
PATHS.md in each Grok skill maps old box paths; verbatim originals also live in the private vault and the handoff repo.

## Production code (`production/`)
| Tool | Run | Notes |
| --- | --- | --- |
| Visual Failure Library | `python3 production/vfl/vfl.py checklist|status|sheet|verdict|render|gate|certify|show|notes` | See `memory/workflows/visual-qc.md`. `harvest.py` rebuilds history (re-run only if sources change). Python: numpy, Pillow |
| 3D rig engine | `cd production/engine && npm install && node render.mjs <board> <out> [--still t1,t2]`; `python3 qc.py <out> <final.mp4> --audio <voice>` | Three.js rig with IK, moves: jab, cross, lead body hook, shovel (rejected v1), arm punch; motion library v1 all REJECTED (guard elbows flared) |
| Long form compositor | `production/longform-remotion` (Remotion 4): `build_timeline.py`, `render.mjs` | Liver v3 timeline and VO sections: handoff repo branch `claude/fight-playbook-youtube-ccyjcd`, folder `CLAUDE-EXPORT/CODE/longform-remotion/` (`timeline.json`, `vo_sections.json`). Needs `public/` layers rebuilt from stills |
| Image bake-off / redraw | `production/imagebench/bench.py`, `fix_redraw.py` | ElevenLabs Image API `POST /v1/flows/image`, poll `GET /v1/flows/image/{id}`; set `FP_RESTYLE=1` for rig redraw |
| Pose validator | `production/anatomy/validate.py` | rtmlib + onnxruntime CPU; needs weights (openmmlab host blocked; HF reachable); licence C15 open; advisory only |
| Vault bridge | `production/kb/kb.py pull|brief|capture|log|sync` | Optional: private Obsidian vault `the-fight-playbook-brain` (not required; project memory is in `memory/`) |
| YouTube analytics | `production/analytics/yt_analytics.py` | Read only OAuth; token does not survive a new container; follow `memory/workflows/analytics.md` |
| Grok audit | `production/audit/GROK_AUDIT.md` + `evidence/` | 2026-11-23 audit of Grok's TikToks and pipeline |

| Blender character (experimental, FAILED v1) | `production/blender/` (fp_chars.py, hero_model.py, hero_mh.py) | Blender 5.3 pip bpy; Cycles CPU + Freestyle; MakeHuman CC0 base + targets in assets/; see README_FAILED_APPROACHES.md before touching |

## Services and IDs (no secrets here)
* vidIQ (YouTube, TikTok, Instagram research: keyword research, outliers, similar thumbnails, channel stats, trending, earnings; 40+ tools). It is a claude.ai CONNECTOR, not a file: the login happens through vidIQ's own sign-in on claude.ai and belongs to Sean's account, so every chat and session gets it once connected. NEVER store the vidIQ login, password or tokens in this repo (PUBLIC). Status 2026-11-25: NOT connected (registry entry exists, directory id dc5bb20f-6ebd-4dbe-a47e-c2d20fa25acc). Check each session: ListConnectors (keyword vidiq) shows connected and enabledInChat; if it's missing, Sean connects it at claude.ai Settings, Connectors. Read only research; never publish or change anything through it without Sean's words.
* ElevenLabs (images AND voice, Sean 2026-11-24). Key is a proxy injected network secret on the cloud environment; send any dummy value. Models: `gemini-3.1-flash-image` (Nano Banana 2, 2K 1,224 credits), `gemini-3-pro-image` (Pro, 2,436), `gpt-image-2` (1,182). No FLUX, LoRA or ControlNet on ElevenLabs. Voice Ryan Kurk `rU18Fk3uSDhmg5Xh41o4`, eleven_v4, stability 0.50, similarity 0.75.
* Grok's ElevenLabs flow `jZVcQ6zNR237hebnnSlb`, reference node `Fqem0pcQbobpCK6o3Cdy`.
* Installed in the container: node 22, ffmpeg 6.1, Python 3.13, Chromium + Playwright. Blender not installed.

## Repositories
| Repo | Visibility | Holds |
| --- | --- | --- |
| `swill3210/fightplaybook-tiktok-media` | PUBLIC | This project: memory, skills, agents, code, Visual Failure Library, TikTok releases for Buffer |
| `swill3210/the-fight-playbook-claude-handoff` | private | Grok's export (read only): stills, ledgers, QA reports, videos. Branch `claude/fight-playbook-youtube-ccyjcd` has `CLAUDE-EXPORT/` (liver v3 final cut, fixed stills, timeline, tests) |
| `swill3210/the-fight-playbook-brain` | private | Sean's Obsidian vault (Knowledge Base originals, verbatim sources) |
| `swill3210/mamba` | private | Share package (fight_playbook_video_build skill, Khoj brief); not attached by default |
To read a private repo in a cloud session, attach it with the add_repo tool, then clone with `--depth 1`.

## Research already done (do not repeat)
* 2026-11-24 Cheaper illustration methods (web research, prices as listed by vendors on that date, unverified):
  * ElevenLabs Nano Banana 2 at 1K costs 406 credits vs 1,224 at 2K (from a quota error message); 3x cheaper, needs upscaling for 1080p.
  * Masked inpainting (edit ONLY the arm, rest pixel identical): FLUX.1 Fill [pro] about $0.05 per image or per MP (fal.ai, BFL); Kontext [pro] about $0.055/MP for instruction edits. Best fit for near correct stills (V36, V54, V95). Needs a new vendor key and Sean's approval.
  * Pose conditioned generation (OpenPose/ControlNet from our rig skeleton): SDXL or Z Image Turbo ControlNet about $0.003 to $0.012 per image, FLUX ControlNet Union Pro 2.0 about $0.03 (ModelsLab, WaveSpeed, fal.ai, Cut.Pro). Character and style consistency would need our LoRA (`imagebench/lora_dataset.py`, 22 approved images, trigger `tfphero`); untested.
  * Free: composite a verified L hook arm cut from an approved still onto other approved stills (deterministic, seam risk); reuse approved stills with Remotion camera moves, crops and motion graphics (limited by the one image at most twice law).
Image model bake-off (all models draw body hooks straight); pose tool verdicts (keep rig + redraw; rtmlib as validator runtime; ControlNet, MediaToPose, Blender Rigify rejected for now); motion tool audit (Remotion and GSAP installable; Manim available; Blender not needed yet); channel analytics 2026-11-23/24 (summary in PROJECT_STATE.md).
