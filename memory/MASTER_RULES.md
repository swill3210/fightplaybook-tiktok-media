# Master rules (permanent; condensed from Sean's instructions and the vault Knowledge Base 01 to 12)

Verbatim sources outrank this summary: skill `fight-playbook-rules` (R1 to R49, hook_rules, character lock, background rotation), then `fight-playbook-long-form-build-and-a-b-test`, `fight-playbook-video-build`, `fight-playbook-fighting-technique-animation`, `fight-playbook-wild-punch-haymaker-animation`, then `fight-playbook-production`. Order of authority: Sean's newest words > verbatim skills > this file. Never edit, delete or simplify a skill, rule or approved standard without Sean's approval; mark superseded rules, never delete them.

## 1. Non negotiables (every format)
* Never upload, publish, schedule, post or delete without Sean's own words for that file. A bot handoff is not permission.
* Honest and direct; do not agree by default; push back with a better option. Flag anything that would not work in a real fight (Sean: Army Infantry veteran, law enforcement and boxing experience).
* Never claim a check ran unless it ran. Never invent numbers, sources, footage or analytics; label VERIFIED / STUDIO EXPORT / PUBLIC / ESTIMATE.
* Language: no dashes anywhere (on screen, captions, titles, descriptions, messages to Sean); gender neutral (never guy, guys, man, he, him, his, bro); no famous fighter names; never "AI" or "animated" in viewer copy; no safety or legal disclaimer lines.
* Secrets never in files, notes, commits or chat; keys only via secure forms (environment network secrets).
* Quality over speed: "Do not sacrifice animation quality to speed up production."
* Do not start a new spec or script until Sean says start. A newer script replaces the old one completely; never merge.

## 2. Formats stay separate (a rule for one format never applies to another)
| Format | Workflow | Key differences |
| --- | --- | --- |
| Long form YouTube | `memory/workflows/long-form.md` | Black shirt with red side stripes, 16:9 1920x1080 30 fps, no bottom caption bar, silent first, subscribe ask at the end |
| Shorts and TikTok | `memory/workflows/shorts-tiktok.md` (PAUSED by Sean 2026-11-23) | Gray tank top, 9:16, synced caption bar on Shorts, seamless loop, no CTA |
| Promos / TikTok Shop | `memory/workflows/promos.md` | Illustrated room allowed, CTA "Tap the orange cart below to grab it", no loop |
| Skool Academy | R21, R48 | Walled off from YouTube and TikTok |

## 3. Characters (R1, R2, CHARACTER_SPEC; reference sheet in skill fight-playbook-rules)
* Hero: dark charcoal skin, bald, muscular; faceless: smooth blank face with ONLY two small slanted white eyes (no mouth, nose, eyebrows, ever); clean 2D comic style, thin black outlines; barefoot always. Long form outfit: plain black sleeveless compression shirt with red side stripes, no lettering; navy shorts with red trim; black MMA gloves with red wrist straps exactly as drawn on the reference sheet, visible finger segments allowed (Sean ruled C4 on 2026-11-24; supersedes "padded with no separate fingers"); bare fists, loose open fingers or boxing gloves fail. Shorts/TikTok: gray tank top.
* Opponent: same faceless charcoal design; ALWAYS red sleeveless tank, no lettering, black shorts, plain black gloves, barefoot; ALWAYS clearly bigger (about half a head taller, broader). Drill partner: plain grey shirt.
* Exactly the scripted cast; count arms, legs, gloves per character on every still; watch skin, shorts and shirt colour drift.
* Claude's 3D rig is a pose and camera stand in, NOT an approved design for final videos unless Sean approves.

## 4. Look, framing, text
* One flat solid background per video, never the same colour two videos in a row: pale blue #D8EEFE, warm sand #ECD6B0, sage #C4D6C4, slate gray #BEC6D0, deep teal #30767C, cream #F5ECD6 (Sean's named colour wins; never pink, coral, lime). Thin ground line or contact shadow only (C6).
* Strike effect: ONLY thin black speed lines drawn in code (R11). No bursts, flashes, sparks, glows, swirls. Image prompts say "draw no effects".
* Strikes land only on chin, jaw or body (ribs, liver, stomach); never neck, throat, shoulder, chest centre. Contact Law: every landed punch has a contact shot with the glove ON the target ~~and the target compressing~~ (superseded 2026-11-25 by Sean's ruling: the prompts turned "compressing" into "buried" and "dent", which produced every F03 glove under the shirt; now the whole glove stays visible on top of the clothing and the clothing keeps its natural structure); uppercuts from below.
* Framing: top fifth clear for the headline; nothing touches the top, left or right edges; bodies leave only through the bottom or a corner; close up hands attach to a visible wrist, forearm and torso. Orthodox liver work: hero on screen RIGHT facing left (C14).
* Text: Bebas Neue, white with dark outline, top centre, max 3 words per line, must add information (never echo the narration or caption), each treatment max about 3 uses per video, never over a head or face. Long form has no bottom caption bar; Shorts keep a caption bar synced to the spoken word.

## 5. Combat accuracy (Mandatory Rules Update 2026-11-24 + hook rules)
* Before illustrating any technique, check it against the technique library (skill fight-playbook-fighting-technique-animation) and the rules below. Never trust a generated image because it looks good. Combat poses start from the 3D rig (measured joints), then redraw in the house style; never text alone.
* Straights: shoulder, elbow, glove in one line, elbow at least 160 degrees. Hooks: LEFT hook = left arm, about 90 degree L (fail outside 70 to 110), elbow level with the glove, curved path, rotation, non punching glove at the chin, return to guard; body hooks bend the knees. Uppercuts and shovels: elbow at the own hip, forearm 70 to 85 degrees. A retracting arm returns along its path. Guard elbows on the ribs.
* Orthodox liver shot = LEFT hook to the opponent's RIGHT side; name the arm by owner and image side.
* Every claim needs two or more sources; cut unsourced overclaims (blindness, knockout guarantees, timing).

## 5b. Mandatory visual corrections (Sean 2026-11-25, after the liver v3 review)
* Every character: exactly two arms, two hands, two legs, two feet, each attached at the right place; natural shoulder, elbow, wrist, hip and knee alignment.
* Gloves and limbs never penetrate another character's body. Clothing keeps its natural structure: no spiraling, melting, excessive stretching or vortex deformation.
* Clear separation between overlapping characters and their limbs. Intentional framing: close ups must not hide the body mechanics.
* Text, diagrams and graphics never cover an important demonstration (overlays pick an empty slot per shot from the character occupancy grid; see long-form workflow).
* Keep the approved character designs, 2D style, palette and animated graphics. No exaggerated claims (for example, a single punch guaranteed to incapacitate).
* QC covers the whole video, including stills approved earlier; find whether a defect comes from generation, crop, animation, compositing or render and fix that cause instead of regenerating with the same method.

## 6. Pacing and engagement (long form, Sean 2026-11-23/24)
* New still or meaningful composition about every 1.5 s; animated text or graphic every 3 to 5 s; at least 10 distinct angles per minute; never the same angle twice in a row; never more than two wide eye level side shots in a row; no static holds (eased camera move on every shot).
* Engagement mix synced to narration: keywords, numbers, countdowns, arrows, diagrams, side by side, correct vs incorrect, highlighted body parts and paths, zooms, annotated freeze frames, transitions, progress indicators. No decoration without meaning.
* Hook: action landing in frame one, first word at 0:00, self test early (~0:17), full technique at speed by ~0:32; end with the 1, 2 or 3 comment CTA and SUBSCRIBE starting after the last word, held at least 3 s.

## 7. Quality control (mandatory)
* Visual QC follows `memory/workflows/visual-qc.md` and the Visual Failure Library (`memory/visual-failures/CHECKLIST.md`). Borderline = FAIL; uncertain = escalate; any known defect = the video cannot pass.
* 5 pass QC on every video: anatomy, combat accuracy, synchronisation, retention, full playback (frame by frame on questionable sequences). Log every defect with a timestamp, fix, repeat.
* Two subagent gates: `combat-anatomy-specialist` must APPROVE every combat asset (uncertain = rejected); `visual-creative-director` reviews every render after QC until APPROVE.
* Audio: about -14 LUFS, true peak at or under -2 dBTP; never speed up long form voice (retime visuals); SFX on exact frames (the "no tick on narration" rule was removed by Sean 2026-11-24).
* Render hygiene: confirm no other render is running; render to a new filename; commit or export finished renders (the v3 render was nearly lost in an ephemeral container).

## 8. Packaging
* Description: verbatim disclaimer "Narrated by a licensed narrator. This script was written and researched for factual confirmation. All script work was edited and checked by hand before posting."; Skool line says FREE to join; chapters; comment your number CTA; never AI or animated.
* Thumbnails: Thumbnail bot only unless Sean asks; Sean's taste: one full frame action shot, tight close up, max 2 huge words, no before/after split (C7).
* Voice: Ryan Kurk `rU18Fk3uSDhmg5Xh41o4`, eleven_v4, stability 0.50, similarity 0.75; narration only after Sean approves the silent visuals.

## 9. 3D character track (Sean 2026-11-24)
* Combat illustrations may be rendered directly in Blender; final images must never pass through a generative image model. Method and gates: `memory/workflows/blender-character.md`.
* Character design must be approved by Sean before any rigging for animation, combat poses or animation.
* No paid image generation or purchases without Sean's approval (ElevenLabs credits are at 0).

## 10. Repository decision (Sean 2026-11-24)
Project memory, skills, agents and the Visual Failure Library live in this PUBLIC repo `fightplaybook-tiktok-media` by Sean's choice (supersedes KB 06 "never put rules or analytics here"). Still never commit credentials, tokens, emails or private OAuth files.
