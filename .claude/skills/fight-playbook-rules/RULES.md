# The Fight Playbook — RULES.md

Single source of truth for every Fight Playbook bot. Read this before you write, build, upload, pin, or post.

**How to change a rule:** edit this file. Do not relay rules by message.

**Canonical project folder:** `/workspace/fightplaybook/`. Older files in `/workspace/fight-playbook/` stay in place; do not move, rename, or delete them.

Each rule names its source. Where sources once conflicted, the current wording is in the rule itself, and the resolution is listed at the end.

Last compiled: 2026-11-20 10:42 PM ET (America/New_York). Open conflicts were resolved the same evening.

---

## Roles

- **Script Writer** writes and reviews scripts (drafts plus the review pass). It does not build or upload videos.
- **Thumbnail** is the only bot that makes thumbnails. Other bots do not generate or invent thumbnail art.
- **Shorts bot** (The Fights Playbook Shorts) is the only short-form builder. It builds YouTube Shorts and the short-form video file that can also go to TikTok.
- **Tik Tok Clips** publishes to TikTok through Buffer and runs ads. It does not build a second short-form pipeline. It may still apply the TikTok cover frame and Buffer/ad steps.
- **The Fight Playbook Youtube** builds and uploads long-form YouTube videos (and Academy lesson videos when handed that work).
- **YT Community** handles pins and replies on The Fight Playbook channel.
- **Skool** handles The Fight Playbook Academy on Skool.

Source: Sean-approved role split, 2026-11-20, compiled into this rulebook.

---

## Per-video folder convention

For every new video, use:

`/workspace/fightplaybook/videos/<slug>/{script,edit,thumb,upload}/`

plus a `STATUS.md` in the video folder with: stage, owner bot, next step, and updated date (America/New_York).

Copy the starter from `/workspace/fightplaybook/videos/_TEMPLATE/`. Do not migrate old episodes. Existing work stays in its current folders (`/workspace/fight-playbook/ep*`, `/workspace/fightplaybook/tiktok/`, `/workspace/skool/`, and so on).

Suggested contents:

- `script/` — script, sources, caption or description drafts
- `edit/` — stills, scene plan, audio, renders, `qa_report.md`
- `thumb/` — thumbnail or cover options and the approved file
- `upload/` — final file, title, description, tags, upload notes

---

## Brand / voice

**R1. Official character is locked.** The only character reference is `/workspace/fight-playbook/characters/main_character_reference.jpg` (front, right, left, back). All earlier designs are retired. Dark charcoal gray body and face. Bald, faceless head with small white eyes (completely smooth and blank: no mouth, no nose, no eyebrows, no other facial features). Muscular athletic build. Black sleeveless compression shirt with red accents and no lettering or logo. Navy shorts with red trim. Black MMA gloves with red detailing / wrist straps. Bare feet, never shoes or socks. Clean 2D comic style with defined muscle shading and thin uniform outlines. Never change appearance, colors, outfit, or style. Only pose, movement, camera angle, and height may change, and only when the video requires it.
Source: `/workspace/fight-playbook/standards/MASTER_PRODUCTION_STANDARD.md` (Sean, 2026-11-11, lettering removed the same day); reinforced in `/workspace/fightplaybook/standards/master_visual_rule_2026-11-19.md` and `promo_video_rules.md`.

**R2. Opponent and partner stay distinct.** The opponent uses the same faceless design, usually taller or bigger, in a red sleeveless shirt with no lettering. A drill partner (if any) wears a plain grey shirt with no lettering. Opponent is always red, partner is always grey — never swap them in a split frame. For promo or long-form, the opponent may be shown without gloves when that is the locked style for the scene; do not mix glove rules inside one video.
Source: MASTER_PRODUCTION_STANDARD.md (opponent same design, taller or bigger); master_visual_rule_2026-11-19.md (red opponent, grey partner).

**R3. Anatomy must be correct in every frame.** No floating fists, detached hands, disconnected arms, extra limbs, or missing parts. Wrists, elbows, shoulders, knees, and ankles stay connected. Punches, kicks, blocks, defense, and footwork follow real boxing and MMA mechanics. No impossible sudden pose changes. Both fighters stay consistent. Natural joints. Fix any defect before publishing. Fighters face each other unless the script says otherwise.
Source: MASTER_PRODUCTION_STANDARD.md §2; one_verb_one_image_law_2026-11-19.md (natural joints).

**R4. Every visual must explain the narration.** No random shapes, confusing symbols, or meaningless illustrations. Favor accurate fighting demonstrations over generic diagrams. Use arrows, labels, and highlights only when they help. No unrelated or unnecessary static images. If a visual is confusing, replace it. Stills must match what the voiceover says at that moment: the right move, position, direction, character, and gloves.
Source: MASTER_PRODUCTION_STANDARD.md §3; Skool / YouTube standing rule "the photos must match" (Skool and The Fight Playbook Youtube transcripts, mid-November 2026).

**R5. Language is gender-neutral everywhere.** Sean's words: "this is a gender neutral group. Avoid saying guys, he, etc. this goes for videos, scripts or whatever. We want to be open to all clientele." Do not use guy, guys, man, he, him, his, or bro for the viewer or the characters. Use someone, they, them, their, you, your partner, the attacker, or everyone. This applies to scripts, voiceovers, titles, descriptions, on-screen text, thumbnails, captions, ads, community pins, and replies.
Source: Sean, via Skool, applied across bots (The Fight Playbook Youtube, Shorts, Tik Tok Clips, Script Writer, Thumbnail, YT Community).

**R6. No dashes anywhere in viewer-facing copy or in explanations to Sean.** No hyphens, en dashes, or em dashes in voiceover, on-screen text, titles, descriptions, captions, cover text, or messages to Sean. Use plain beginner words.
Source: MASTER_PRODUCTION_STANDARD.md (standing rules carried over); shorts_two_structure_rotation.md; shorts_retention_rules_2026-11-18.md; promo_video_rules.md; `/workspace/fightplaybook/PIPELINE.md`; TikTok originals PIPELINE.md.

**R7. Voice is punchy and practical.** Straight, practical fighting tips. Open with a real scenario and de-escalation first; go to the fight only when there is no other choice. Use punchy, plain wording. Chat or thought bubbles and "Situation A or B" beats are flavor to mix in, not a rigid template. Varied action: not only standing exchanges; include ground work, takedowns, the clinch, and varied scenes and angles when the topic calls for it.
Source: MASTER_PRODUCTION_STANDARD.md, MASTER PLAN and VISUAL METHOD OVERRIDE (Sean, 2026-11-11).

**R8. No famous fighter or historical fight name drops.** Tips stay research-backed; the names stay off the screen and out of the narration. Never invent stats or claims. Fact-check claims (two or more sources) and log them in the script.
Source: MASTER_PRODUCTION_STANDARD.md (scripts and story); TikTok originals PIPELINE.md; promo_video_rules.md (no invented stats).

**R9. Never say "animated," and never include safety or legal disclaimers.** No "EDUCATION ONLY. TRAIN SLOW..." lower thirds or similar disclaimer cards. No price lines in Academy or promo copy unless Sean asks. Do not present the narrator or character as a real expert, and stay away from medical or legal advice.
Source: promo_video_rules.md; Skool standing rule (Sean banned disclaimer cards, mid-November 2026); The Fight Playbook Youtube guidance on AI-use honesty in Studio.

**R10. Background colors rotate across every format.** Flat solid background only, no gradients or textures, no floor or environment unless a promo or hook is specifically set in a real illustrated room or location. Rotate: pale blue `#D8EEFE`, warm sand `#ECD6B0`, sage green `#C4D6C4`, slate gray `#BEC6D0`, deep teal `#30767C`, cream `#F5ECD6`. Never pink, coral, or lime. Never use the same color back to back from one video to the next. Do not repeat a camera angle back to back either (except a deliberate repeat such as a self-test, summary board, or loop reset). The six-color set applies to long-form, Shorts, TikTok, Skool Academy lessons, and the trailer.
Source: `/workspace/fightplaybook/standards/background_color_rotation.md` (mandatory as of 2026-11-18, from Sean); `/workspace/fightplaybook/standards/background_color_hex.md` (locked 2026-11-18 / hex confirmed 2026-11-19 from Tik Tok Clips palette); Sean on 2026-11-19, to the Shorts bot, when asked if sage and slate should be dropped from the four-color list in master_visual_rule_2026-11-19.md: "Nah add those." Older mismatched hex values (`#D8EFFE`, `#EAD9B8`) stay retired. Default kept: use this locked palette.

**R11. Black horizontal speed lines are the only strike effect.** Every strike (punch, kick, knee, elbow, palm) gets thin black horizontal speed lines trailing the striking limb, like a comic panel. Use `speed_lines()` from `/workspace/fight-playbook/ep21_fists_like_a_train/rebuild/build_ep21.py`, matched to `/workspace/fight-playbook/standards/punch_speed_lines_reference.jpg`. Do not use the old navy `speedlines()` in `shorts/_shared/motion.py`. No impact bursts, flashes, sparks, shockwaves, glows, or other strike effects. Draw lines in code; strike image prompts must say to draw no effects. Head shots land on the chin or jaw, never the neck. Every strike shown in a thumbnail or teaching still lands on its intended target (no missed or ghosted strikes in thumbs).
Source: MASTER_PRODUCTION_STANDARD.md, Hook and strike rules (2026-11-13); Script Writer standing rule, then update that lines go on all strikes not just punches; TikTok originals PIPELINE.md; promo_video_rules.md.

**R12. Music is a quiet lofi bed under the narration.** Keep volume consistent. Music and SFX never overpower the voice. Target roughly -14 LUFS, true peak at or below about -2 dB. Music may fade on a long-form outro. For Shorts, music stays at one steady level across a loop cut, with no fade at the end.
Source: MASTER_PRODUCTION_STANDARD.md §5 and MASTER PLAN; TikTok originals PIPELINE.md (finish pass); shorts loop notes.

---

## Scripts

**R13. Every script is built from extensive, sourced research.** Log sources in the script. Soften or cut unsourced claims.
Source: MASTER_PRODUCTION_STANDARD.md, standing rules carried over; Script Writer / Skool research corrections.

**R14. Long-form story structure.** For every long video:

1. Hook, about 12 to 17 seconds. No intro and no title card. The first word of narration plays at 0:00. Open with the problem in one line, then "Let's see how [you/fighters] should actually [do the topic], so you can…" (adapt to the topic). Frame one is action already landing or mid motion, never static, with a matching 2 to 4 word text pop.
2. Fundamentals. The de-escalation scenario belongs here, right after the hook, not inside the hook.
3. Numbered SECTIONS (the Zero2Kombat layout), which map onto Level 1 / Level 2 / Level 3 escalating stages when the topic needs them, plus a short science section with sources, plus how to fit it into a training week.
4. Close on one line: "And that's everything you need to know about [topic]" (or "That's how fighters actually..."). Then silent summary boards, one per section, hard cut between them, held so the ending is readable (the original structure used an 11 second hold). No narration on that hold. Music may fade. No SFX. No like/subscribe ask, no end screen pitch.

Follow the construction in `/workspace/fight-playbook/standards/LAYOUT_TEMPLATE_z2k_build_muscle.md` exactly, minus the sponsor read and the free plan / lead magnet pitch (never include either). Each section opens with a silent title card ("SECTION 1: ...") that blurs in, holds about 4 seconds with music only, and blurs out. Inside sections: numbered PRINCIPLE / LEVEL cards, beige rectangular text cards and pop ins, arrows, side by side comparisons, split screens, charts and tables, red glow for target or tension, yellow glow for force transfer, green + for recovery, calendar or weekly plan grids. Hard cuts every 2 to 5 seconds, a new visual for each sentence, a concrete example for every principle.
Source: MASTER_PRODUCTION_STANDARD.md, SCRIPT STRUCTURE (2026-11-11), LAYOUT TEMPLATE (Sean, 2026-11-11 11:27 ET, "this is exactly how I want it"), Hook and strike rules (2026-11-13).

**R15. There is no minute limit on long-form runtime.** Do not pad or trim a script just to hit a clock. Write the teaching clearly and build the video.
Source: Sean to Script Writer, direct: "There is no more minute limit just get the video made." This supersedes the earlier "no Fight Playbook video can be under 3:00" rule. A later 2:30 remake of How To Actually Fight was also kept at 2:30 on purpose.

**R16. Shorts use the two-structure rotation, not Micro Adjustment only.** Sean: "Just stick to 1 and 2." Alternate Structure 1 and Structure 2 (odd numbered Shorts are Structure 1, even numbered are Structure 2), and match the structure to the topic where it fits better. This supersedes the "Micro Adjustment only" rule and stays until Sean says otherwise.

- Length: Structure 1 runs 20 to 25 seconds and 55 to 70 words, never over 70. Structure 2 keeps 18 to 22 seconds and 50 to 58 words. No fluff, no greetings. Start on the action at second zero.
- **Structure 1, The 3 Step Sequence:** direct promise hook (0 to 3s, about 10 words): "Three steps to [high value goal] instantly." Core problem (keep this short; see R18). Then Step 1 / 2 / 3 badges (base/feet, hips/torso, impact/finish). End on a rhythmic 3 word rule that flows into the loop, with no "follow" line.
- **Structure 2, Myth vs Fix:** exactly `/workspace/fightplaybook/standards/shorts_micro_adjustment_blueprint.md`: counter-intuitive hook, fatal mistake, exactly 2 physical cues, and a golden rule ("[3 word rule], not [common mistake]") that loops to frame one.
Source: `/workspace/fightplaybook/standards/shorts_two_structure_rotation.md` (Sean, 2026-11-16); `/workspace/fightplaybook/standards/shorts_micro_adjustment_blueprint.md` (standing rule from 2026-11-16, now Structure 2 only).

**R17. YouTube Shorts may be standalone.** They do not need their own long-form video. Link the most related published long-form as the Related Video in Studio when one exists.
Source: Sean, relayed to the Shorts bot by Script Writer (Shorts bot transcript): "Shorts are standalone now and don't need their own long form video. Just link the most related published video as the Related Video." This supersedes the earlier "every Short comes from a published long form" rule.

**R18. Shorts retention rules sit on top of the two structures.** (Mandatory as of 2026-11-18, from Sean.)

1. Setup under 3 seconds. Go from the hook straight into Step 1, with at most one short problem line. Never spend 6 or 7 seconds on what most people do wrong.
2. A rewatchable moment in Step 2 or Step 3: the move at full speed, then a 2 second slow motion breakdown or an on-screen directional arrow. Slow motion is only for that breakdown, never the ending.
3. A seamless loop. The final line must flow grammatically straight into the hook, but it never repeats the hook line itself (no hook said twice). No recap, no trailing audio, no unconnected tease like "and here is the catch." Hard cut with no pause.

Keep gender-neutral language, no dashes, beginner words, quick frames, and no CTA on regular Shorts.
Source: `/workspace/fightplaybook/standards/shorts_retention_rules_2026-11-18.md`. Hook-line wording confirmed Sean, 2026-11-20 (see R29). The older Structure 1 "core problem 3 to 6s" window is retired in favor of this setup-under-3-seconds rule. Default kept.

**R19. TikTok original scripts use only the TikTok script template.** `/workspace/fightplaybook/tiktok/originals/TIKTOK_SCRIPT_TEMPLATE.md` is the only TikTok script format (Sean, 2026-11-16). It applies to TikTok only, not Shorts. Target 20 to 25 seconds, 55 to 65 words max. Four segments: visceral hook and myth (0:00 to 0:05), core rule / anchor (0:05 to 0:12), counter / escape (0:12 to 0:19), loop / rule of thumb (0:19 to 0:24). One problem, one solution, exactly one specific movement per video. Every sentence matches a physical motion on screen. No filler ("Hey guys", "Did you know", "Today I'm going to show you"). Loop technique in `/workspace/fightplaybook/tiktok/originals/LOOP_AND_SCRIPT_NOTES.md` still applies.
Source: TIKTOK_SCRIPT_TEMPLATE.md; LOOP_AND_SCRIPT_NOTES.md. Length and word cap confirmed Sean, 2026-11-20: 20 to 25 seconds, 55 to 65 words max. Older 20 to 35 second / 70 to 80 word lines in originals/PIPELINE.md are retired.

**R20. Promo / TikTok Shop scripts have their own rules.** About 20 to 30 seconds, roughly 65 to 85 words (about 0.33 s per word). Hook up to about 4 seconds (promos are the only exception to the under 3 s hook rule). Name a problem or mistake, then go straight into value. No fluff, no intro, no "hey guys". Straight to useful tips that teach something real while using the product. It does not have to be "3 ways." Include one rewatchable moment (full speed, then about 2 s slow motion or an arrow). CTA last line points to the TikTok Shop product on the video itself: "Tap the orange cart below to grab it." Never "link in bio", "showcase", or "pinned comment". Sean reviews the script first unless he says otherwise. Finished video is sent to Sean as a file; do not upload it anywhere unless Sean says to. Approved structure template: `/workspace/fightplaybook/ads/punch_faster/build_uppercut/uppercut_promo_v2.mp4` and `uppercut_promo_v3.md`. Outdated, do not copy: `/workspace/fightplaybook/ads/funpunch/short_ad_v*.md`.
Source: `/workspace/fightplaybook/standards/promo_video_rules.md` (current as of 2026-11-19); Shorts bot, Sean on uppercut v2 structure (real illustrated room with walls and a couch, rotation color on the main wall, full-body demonstration, creative angles, subtle synced SFX under the VO, CTA, hard cut on the last word, no loop).

**R21. Skool Academy scripts stay walled off from YouTube and TikTok.** Sean: "Don't let this affect our YouTube, TikTok scripts. This script is strictly for skool, don't apply this anywhere else." Academy content teaches simple, practical self defense, not complex martial arts. No Skool or YouTube plugs inside lesson videos. No price lines. Never call it animated.
Source: Sean to Script Writer, direct; promo and Skool house rules.

---

## Narration / ElevenLabs

**R22. The narrator is always ElevenLabs Ryan Kurk.** Voice id `rU18Fk3uSDhmg5Xh41o4`, model `eleven_v4`, stability 0.50, similarity 0.75. Same voice for long-form, Shorts, TikTok, Academy lessons, and the trailer (including "I'm Sean" lines unless Sean records them himself).
Source: MASTER_PRODUCTION_STANDARD.md, standing rules carried over; TikTok originals PIPELINE.md; Skool trailer approvals.

**R23. Inspect the full audio before upload.** Narration must be natural and clear, with no glitches, mispronunciations, repeated words, awkward pauses, missing sentences, or cuts. Keep volume consistent. Narration must be technically accurate and must match the script word for word. Fix any issue automatically. For timed reads, about 0.33 seconds per word is the usual pace when a section has to fit a slot.
Source: MASTER_PRODUCTION_STANDARD.md §5; Sean's 2:30 remake VO brief (The Fight Playbook Youtube transcript).

**R24. Check ElevenLabs credits before any paid build or transcription check.** Do not start a render that will fail mid-way for lack of credits. If credits are too low, stop and tell Sean. Short-form voiceover is typically sped with `atempo=1.10` (Shorts have used 1.10 to 1.13x) and word-timed with Whisper `medium.en`, not `small.en`.
Source: TikTok originals PIPELINE.md; The Fight Playbook Youtube transcripts (builds blocked or checks skipped when the balance was too low, including a 144-credit balance).

**R25. Re-voice leftover gendered lines.** If a finished voiceover still uses he/him/his about the attacker or viewer, re-record those lines to they/them/the attacker rather than leaving them.
Source: Sean, via Skool, on gender-neutral re-voices.

---

## Long-form edit

**R26. Still images with hard cuts. No animation.** The cut-out puppet rig approach is rejected; do not use `/workspace/fight-playbook/rig` for episodes. Build videos like Episode 1: still images of the official character, hard cuts, a new image for each beat or concept. Add text pops (bold all caps, Bebas Neue style), arrows, target icons, and red glows on targets as overlays on top of the stills. Never leave one image on screen while the narrator explains several different concepts. Avoid unnecessary pauses or overly long transitions. Before generating the video, write a scene-by-scene animation plan that matches each narration segment to its exact visual demonstration.
Source: MASTER_PRODUCTION_STANDARD.md, VISUAL METHOD OVERRIDE (Sean, 2026-11-11 10:26 ET) and §4 pacing (revised 08:36 ET). The later 2:30 remake SFX and push-in map is not a standing rule for every long video. Default kept: stills plus hard cuts stay the base.

**R27. Vary the camera, and get creative, without breaking the stills rule.** Change angle shot to shot (low, overhead, over the shoulder, behind the character, side on, tight on hands or feet, split frames). Use side-by-side framing rarely. Do not repeat an angle back to back. Include appropriate close-ups, slow-motion demonstrations (as still-sequence breakdowns or holds), and movement arrows. Show techniques from different angles when it improves understanding.
Source: Sean, "practice different angles and get creative, without deviating from his rules or the script," relayed by Script Writer; MASTER_PRODUCTION_STANDARD.md §4; Shorts bot confirmation that different angles also apply to TikTok.

**R28. Mandatory final inspection. Never upload without it.**

1. Review the full export start to finish.
2. Inspect frames for disconnected limbs, glitches, and distortion.
3. Compare the character against the reference.
4. Confirm every visual matches the narration.
5. Find unnecessary static scenes, confusing graphics, and pacing problems.
6. Check narration, sync, subtitles, and sound.
7. Verify that the techniques are technically accurate.
8. Fix every problem.
9. Regenerate defective scenes.
10. Re-render and repeat the full inspection until everything passes.

If something can't be fixed or a check can't be completed, do not publish. Flag it to Sean. Never claim a check passed unless it was actually performed and verified. Write the inspection log to the episode folder as `qa_report.md`. Always use the latest approved character image. Never upload incomplete, defective, or unverified videos just to meet a schedule.
Source: MASTER_PRODUCTION_STANDARD.md §6 and §7.

---

## Shorts / TikTok short-form

**R29. Absolute seamless loop on every Short and TikTok, except promos.** Sean, 2026-11-19 5:16 PM ET, direct to the Shorts bot: "It needs to be an absolute seamless loop! Tell this to script too for all shorts and TikTok videos there needs to be a seamless loop." Goal: 100% retention; the viewer should not sense the video is ending. No recap, no "Follow for more", no CTA, no end card, no fade, no subscribe line. The ending flows into the opening hook but never repeats the hook line itself (seamless loop, no hook said twice). The last line is a separate lead-in that runs with zero pause into a hard cut back to frame one, where the hook finishes the thought. Music carries across the wrap at one steady level, no fade. The final visual leads into frame 0 (last frame mid motion or matching the opening pose). Cut bridge audio at the end of its last word (about 0.08 s gap). Do not let the hook's first word leak into the bridge tail. Listen across the seam, and test by playing the video twice back to back. Promos with a CTA are the exception: no loop, hard cut on the last word.
Source: Sean, Shorts bot transcript, 2026-11-19 5:16 PM ET (reinforcing the loop rule restored on 2026-11-16 after a 2026-11-14 "no loop" instruction). Also shorts_two_structure_rotation.md, shorts_retention_rules_2026-11-18.md, LOOP_AND_SCRIPT_NOTES.md. Hook-line wording confirmed Sean, 2026-11-20.

**R30. The hook is everything.** The 0 to 2 second moment must grab attention instantly. Frame one is action already landing or mid motion, never static, never a blank wall or slow intro. The first spoken line lands at 0.0 s with a matching 2 to 4 word text pop. No intro. For TikTok originals, frame 0 is the cover, then hook text plus a strike already landing with speed lines; cut every 1 to 1.5 s in the first 5 s.
Source: Sean, standing rule 2026-11-13, Shorts and Script Writer transcripts; MASTER_PRODUCTION_STANDARD.md hook rules (2026-11-13); TikTok originals PIPELINE.md (fast opening, 2026-11-13).

**R31. One verb equals one new image.** Parse the script into action verbs first, not steps. "Wide feet, sink hips, head up" is 3 verbs, so it is 3 images. Every image must have a Start Pose, an End Pose, and a Visible Change (a body part has moved to a different position; zoom, crop, or an arrow is not movement). If a new image is identical to the previous one except for text, zoom, or crop, reject it and regenerate that one shot only. Never re-render the whole video for one bad shot.

Pose-change check, before assembly, for each consecutive pair:

1. Did a body part move?
2. Is the body part named in the text the body part that moved?
3. Is the direction in the text the direction in the image? (Up = up, forward = forward, down = down.)

If any answer is No, that shot fails. Regenerate that shot only, with a new Start Pose and End Pose written out in full. Do not "fix it in the edit" with an arrow.

Credit-saving work order: (1) generate stills only, one per verb; (2) pose-change check; (3) fix failed shots only; (4) assemble silent, with big text only, and check text sync; (5) only then add narration, lofi bed, and any SFX. Never spend narration or render credits on a video whose stills have not passed the pose check.

For already-built Shorts: list only the failed shots, regenerate only those, patch them in, and keep the good shots, the audio, and the loop.
Source: Sean, direct, 2026-11-19 9:04 PM ET, `/workspace/fightplaybook/standards/one_verb_one_image_law_2026-11-19.md`; expanded in `/workspace/fightplaybook/standards/master_visual_rule_2026-11-19.md`.

**R32. Camera and text rules for short-form stills.**

- Feet, hips, weight, stepping, dropping: full body, feet and head in frame. If feet are cut off, the shot fails.
- Head, chin, eyes: close-up on the head only.
- Hands, grip, elbows: close-up on hands / arms. Use a front angle for "forward"; forward does not read from a side angle.
- A punch, kick, or tackle landing: show the landing. Front for impact, side for form, overhead for ground work.
- Never use a legs-only still for a kick. Every kick still shows hands up and the full body.
- Never use the same camera angle for two consecutive teaching stills unless the action is a deliberate repeat (self-test, summary board, loop reset).
- Chin tucked when the script says so. No ghosting.
- For hard-to-read moves (grip break, slip, roll, drop): two frames back to back (before then after), or a before/after split in one frame, left = before, right = after, arrow left to right. Do not jump from locked to free, or from standing to down, in a single cut with no middle frame.
- Big on-screen text only, max 3 words per still. Text must name the action in the image, not the next action and not the last action. No text over the hero's eyes. No label cropped at the frame edge. In close-ups, arms enter from the frame edge.
- The bottom caption bar is allowed again. Keep it in sync with the VO. (Sean removed the "no bottom caption bar / no double text" rule on 2026-11-19 at 10:30 PM ET and said to redo the affected Shorts with the bar back on.)
Source: master_visual_rule_2026-11-19.md; one_verb_one_image_law_2026-11-19.md; Sean, Shorts bot transcript, 2026-11-19 10:30 PM ET.

**R33. Short-form music is lofi only, with no sound effects on regular Shorts.** Black speed lines remain the only strike effect. Regular Shorts stay lofi only, no SFX except promos. Promos may use subtle synced SFX under the VO. TikTok originals keep whoosh and thud SFX on strike contact.
Source: shorts_two_structure_rotation.md; Script Writer handoffs to the Shorts bot ("Sean confirmed today: music only, NO sound effects"); promo_video_rules.md; TikTok originals PIPELINE.md finish pass. SFX split confirmed Sean, 2026-11-20.

**R34. Format for finished short-form files.** 1080x1920 (9:16), 30 fps, H.264, yuv420p, AAC. Keep subjects big. On TikTok, nothing important goes below y 1450 or in the right 140 px (TikTok UI). Upload regular Shorts as private drafts with no schedule unless Sean says otherwise.
Source: TikTok originals PIPELINE.md; Script Writer / Shorts bot upload handoffs.

**R35. Illustrative covers are the default for every TikTok.** Sean, 2026-11-17 about 1:35 PM ET: "thumbnails on each tiktok that clearly illustrate what the video is about while also looking appealing." Use the video's own key-move still (the threat and the fix), zoomed about 1.5x so heads sit just below the title and the action fills the 3:4 grid crop. Title is uniform: Poppins Black, line 1 = the PROBLEM ending in ? (white, navy outline, 200 px, y 440), line 2 = the FIX (red, white outline, 232 px, y 670). Text block y 345 to 757, 110 px or more side margins. If a line is too wide, shorten the words, never the size. No dashes. No watermark. Art is faded out under the title band (y 0 to 790) so limbs never cross the words. New originals need a `cover_spec.json`. Always view the full 1080x1920 cover and the 3:4 center crop (`crop=1080:1440:0:240`) yourself; rebuild if the move is unclear, tiny, hidden behind text, warped, or off style.

Cover QA is required before every post or schedule. Sean, 2026-11-17: "Make sure the thumbnail fits so no wording is cut and it looks uniform." Extract frame 0 (the 0.167 s cover, thumbnailOffset 0) from the exact MP4 you will host and post. Pass only if every word is fully visible in both the full frame and the 3:4 crop. The old engine.thumbnail layout (line 1 at y 220) fails because the grid crop cuts line 1. Prepend 5 frames (0.167 s) of the cover with silence, then the official video unchanged. Do not recrop, rescale, or reedit the official Short `final.mp4`, and do not burn new captions onto it. If a Shorts thumbnail is missing, report it and skip that Short; do not invent a cover.
Source: `/workspace/fightplaybook/PIPELINE.md` (illustrative covers and cover QA); TikTok originals PIPELINE.md.

**R36. TikTok publishing rules.**

- Cadence: 3 posts a day at 1:00, 5:00, and 9:00 PM ET, every day. Alternate originals and official Shorts. The older 6-a-day (1, 3, 5, 7, 9, and 11 PM ET) and 2 PM / 9 PM cadences are retired. A one-off "every 4 hours" batch is not the standing cadence.
- Post only to the Fight Playbook TikTok channel in Buffer (`thefightplaybook`, shown in Buffer as `grimmclipss`). Channel id `6af3af1562b70b94b0ebdac4`, org `6ad2fe954126c206e7aa045c`.
- The same official Shorts that go out on YouTube should go out on TikTok. Do not cut new clips from long videos. Do not modify files under `/workspace/fight-playbook/shorts/`.
- Use a Short only when it is s09 or higher, marked READY, and has a finished `final.mp4`. Never use s01 through s08. Never post the same Short twice. Prefer TikTok going out the same day as, or after, the YouTube version when a YouTube time is known.
- Read `/workspace/fightplaybook/posted_log.md` first. Never schedule a Short or original that has a POSTED entry, or the same lesson as one, and never schedule anything marked HELD. Sean also posts from his phone, so a video can be live without a Buffer record. Check Buffer `list_posts` for duplicates before every create, including before a retry. Never retry a successful create.
- Buffer's free plan caps scheduled posts at 10. Leave headroom and refill open slots as posts send, never above 10.
- Captions: TikTok-friendly title and hook, no YouTube link line, no dashes, 3 to 5 relevant hashtags (for example `#selfdefense #fighting #boxing #fightplaybook`).
- Host MP4s on GitHub releases (`swill3210/fightplaybook-tiktok-media`), stable github.com URL only, verify HTTP 200 and a byte match. Set `thumbnailOffset` to 0. Set `isAiGenerated: false`. Sean changed this on 2026-11-13: the AI label stays off on every TikTok post.
- To swap a video on an already scheduled post, never delete the post. Use `edit_post` with the same `dueAt`, full caption, and new asset URL, then confirm it is still scheduled. Do not change the slot unless Sean asked to reschedule.
- Append every attempt and outcome to `/workspace/fightplaybook/posted_log.md`.
Source: `/workspace/fightplaybook/PIPELINE.md` (2026-11-16 footer and LOOP_AND_SCRIPT_NOTES.md for the 3-a-day slots). Cadence confirmed Sean, 2026-11-20: 3 posts a day at 1:00, 5:00 and 9:00 PM ET.

**R37. Promo visual extras.** Product photos from Sean are reference only. Never put the real photo or screenshots in the video. Redraw the product in the house style, copying the real item exactly (shape, colors, logo), with people, prices, and shop text left out. Show a product feature only if Sean confirms it or the listing shows it.
Source: promo_video_rules.md.

---

## Thumbnails

**R38. Only the Thumbnail bot makes thumbnails.** Other bots hand off the brief, stills, and title; they do not generate a competing thumbnail or invent cover art. Drop the approved file where the upload bot expects it (for long-form, historically `thumbnail_tb.jpg` in the episode folder, 1280x720 JPG under 2 MB) and let the upload bot attach it. Sean picks or approves a thumbnail before it is swapped onto a draft, unless he has already said "use it" / "ship it."
Source: Sean-approved role split, 2026-11-20; Thumbnail / The Fight Playbook Youtube handoff method; Sean approvals such as "Use it", "ship it" on the dodge-pro thumbnail.

**R39. Hard rules for every thumbnail.** No famous fighter names, no dashes, no red X, no ghosted or "mistake" visuals, no bubbles. Every strike lands on its intended target. Head punches land on the chin or jaw, never the neck. Speed lines are the only strike effect. Gender-neutral text. No logo, no URL, no handle, no channel name, no small fourth element, no "BOXING • MMA • FIGHT TACTICS" noise. 2 or 3 words max, all caps, outcome or negation, not a sentence and not the exact video title (the title already sits under the thumbnail). Text never goes over a face or the hero's torso. Check the image at phone / Home-feed size.
Source: The Fight Playbook Youtube thumbnail method handed to Thumbnail (hard rules from Sean); Sean's later Zero2Kombat thumbnail brief to Thumbnail (2 to 3 words, no logo, no small text).

**R40. Long-form thumbnails are 1280x720.** Shorts and TikTok covers are 1080x1920. Skool covers follow the size requested for that surface (for example 1084x576 for a group cover, 1920x1080 for the Academy trailer). TikTok covers follow R35, not the YouTube long-form layout.
Source: Thumbnail / YouTube bot method (ep18 canonical, with the correction that text sits at the top); PIPELINE.md cover specs.

**R41. The default long-form thumbnail layout is a before / after split that reads as a transformation.** Left: the problem, red tint, using the video's background color. Right: the solution, green or yellow tint, on warm cream or white, not pale blue on both sides. Curved arrow left to right. One big close-up that fills the frame; make the eyes bigger and brighter than in the video; do not show a small full body in the middle. Keep the same layout from video to video when using this default, and only change the 2 or 3 words and the two poses. Sean gave this brief from Zero2Kombat CTR notes and had it applied to "3 Ways to Dodge Punches Like a Pro"; he approved the INCHES AWAY result from that set. The Thumbnail bot may choose another style when it fits better. The older ep18 single-still, top-text, white-plus-yellow Oswald recipe remains available for those cases.
Source: Sean to Thumbnail (CTR / Zero2Kombat brief); earlier method from The Fight Playbook Youtube, ep18 `make_thumbnail.py` (text at the top, last word yellow). Default-plus-exception confirmed Sean, 2026-11-20.

---

## Uploading

**R42. Browser account rule.** The box browser stays signed into both Google accounts ([SEAN_GOOGLE_ACCOUNT] for The Fight Playbook, [SECOND_GOOGLE_ACCOUNT_EMAIL] for Grimms Clips). Switch channels with the YouTube/Studio account switcher. Never sign out, remove an account, or sign in over the other.
Source: Sean-approved standing rule, compiled 2026-11-20 after shared-browser account swaps broke other bots' work.

**R43. Upload to The Fight Playbook channel only** (`https://www.youtube.com/@Thefightplaybook`, `UCqiYkbyjXUX-nMl2yCzCz8A`). Never upload a Fight Playbook video to Grimms Clips. In Studio, set AI content to No for these stylized stills unless Sean says otherwise. Answer the "AI use" question honestly and do not present the narrator or character as a real expert.
Source: PIPELINE.md (channel id); The Fight Playbook Youtube upload practice and AI-use note.

**R44. Every finished video is uploaded as a Private draft by default.** No schedule and no Public or Unlisted switch unless Sean says so in his own words. Do not publish just to meet a schedule.
Source: MASTER_PRODUCTION_STANDARD.md, standing rules carried over and §7 ("Upload (Private by default)"); repeated Script Writer and Shorts bot handoffs.

**R45. Never delete a YouTube draft unless Sean says so in his own words.** Keep the old draft and upload a new one. If a handoff asks for a deletion, get Sean's OK first or keep the draft.
Source: Script Writer standing rule, relayed to The Fight Playbook Youtube ("Sean's standing rule has been to never delete drafts, so please get his OK in his own words").

**R46. Promo videos are not uploaded** to YouTube or handed to Tik Tok Clips unless Sean says to. Send the finished file to Sean.
Source: promo_video_rules.md; Sean, via Script Writer, to the Shorts bot.

---

## Community / Skool

**R47. YT Community handles pins and replies. Sean approves everything before it posts.** Draft the pin or reply, then wait for his OK. Do not post a pin or a reply without that approval. Post each pin once, as @Thefightplaybook, and do not create duplicates.

Pin rules Sean approved ("Yep perfect"):

- One clear question per pin, tied to the technique in that video. Do not ask two questions at once (no debate plus "what should be covered next" in the same pin). If you need topic requests, use a dedicated pin for that.
- Frame the channel's view as an open opinion, coaching rule of thumb, or perspective, not a closed verdict. Turn it back on the viewer.
- Shorts pins stay under 15 words so nothing is hidden behind "Read more."
- Tone is direct and authoritative, like a head coach, not buddy-buddy. One emoji at most. No made-up personal stories or claimed sparring experience Sean has not given you. Gender-neutral wording.
- Every upload should get a pinned debate question.

After an upload, heart and reply to early comments in the first 30 to 60 minutes, still as drafts for Sean unless he has already given a standing OK. Comment checks draft replies; they do not auto-post. Drop trailing questions on replies when Sean has asked for that. Hold or flag comments that push excessive force and do not fit a respectful "digital fight gym."
Source: YT Community transcript, Sean-approved pin rewrite and checklist; community rundown (coach tone, approval, first 60 minutes); later practice of waiting on OK for drafts and dropping trailing questions.

**R48. Skool handles The Fight Playbook Academy.** Keep Academy images exclusive to Skool when that is requested, in the same brand style. Training demos and members' own training clips only, per the Academy rules post. Full feet and legs stay in frame; do not ship cut-off toes or shins. Recolor and still-swap existing lessons rather than rebuilding whole videos when only some beats fail. Use the six-color rotation, gender-neutral language, no dashes, no disclaimer cards, no price, and never say "animated."
Source: Sean to Script Writer and Skool; Skool standing rule that photos must match; Sean's words on regenerating cut-off frames and removing disclaimer / soft-surface cards.

**R49. Ads and trailer changes need Sean's own go-ahead.** TikTok Spark ads to the Academy were paused after visits with no joins, until the Skool page was fixed. Do not unpause or retarget an ad unless Sean says so. Captions that already say the Academy is free to join stay that way when he has said to keep that line. Send finished trailers to Sean in his chat when he asks; do not spend past a credit cap he set.
Source: Tik Tok Clips and Skool transcripts (ad pause; "TikTok captions: keep saying free to join"; trailer credit caps).

---

## Resolved conflicts

These items were open in the first compile. The current wording is in the named rules. Sean's answers are from 2026-11-20, 10:42 PM ET. "Default kept" means the rulebook's existing choice stands.

1. **TikTok posting cadence.** Resolved, Sean, 2026-11-20: 3 posts a day at 1:00, 5:00 and 9:00 PM ET. See R36. The older 6-a-day clock, the 2 PM / 9 PM clock, and the 2026-11-20 "every 4 hours" batch are not the standing cadence.

2. **Hook line at the end.** Resolved, Sean, 2026-11-20: the ending flows into the opening hook but never repeats the hook line itself (seamless loop, no hook said twice). See R29 and R18.

3. **TikTok original length and word count.** Resolved, Sean, 2026-11-20: 20 to 25 seconds, 55 to 65 words max. See R19. Older 20 to 35 second / 70 to 80 word lines in originals/PIPELINE.md are retired.

4. **Sound effects on TikTok originals vs regular Shorts.** Resolved, Sean, 2026-11-20: TikTok originals keep whoosh and thud SFX on strike contact. Regular Shorts stay lofi only, no SFX except promos. See R33.

5. **Long-form push-ins and SFX.** Default kept: stills plus hard cuts remain the base (R26). The 2:30 remake SFX and push-in map is not a standing rule for every long video.

6. **Long-form thumbnail recipe.** Resolved, Sean, 2026-11-20: the before/after split is the default, but the Thumbnail bot may choose another style when it fits better. See R41.

7. **Minor hex mismatch.** Default kept: use the locked hex file (R10), pale blue `#D8EEFE` and warm sand `#ECD6B0`. Older values `#D8EFFE` and `#EAD9B8` are not used on new work.

8. **Structure 1 "core problem" timing vs the Nov 18 retention rule.** Default kept: setup under 3 seconds, at most one short problem line, and never 6 or 7 seconds on what most people do wrong (R18). The "And here is the catch:" tease stays banned.
