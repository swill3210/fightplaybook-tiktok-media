---
name: fight-playbook-production
description: Produce Fight Playbook boxing, MMA and self defense videos (Shorts and long form) with the 3D rig engine in production/engine. Use for any Fight Playbook script, storyboard, animation, render, QC or delivery task. Sean's own fight_playbook_video_build skill and the YouTube bot skill (Fight_Playbook_Longform_Skill_2.md) outrank this file where they conflict.
---

# Fight Playbook production (Claude pipeline)

Pipeline: Research, Script, Storyboard, Animate (3D rig), Voice, Edit, QC, Deliver for review.
Nothing is uploaded, posted or published without Sean's explicit approval for that specific file.

## 0. Source of truth and order of authority

1. Sean's direct instructions in the current conversation.
2. Grok's export, repo `swill3210/the-fight-playbook-claude-handoff`: `SKILLS/standards/RULES.md` (R1 to R49), `SKILLS/fightplaybook-skills/longform-build-and-ab-test/skill-draft.md`, `SKILLS/standards/hook_rules.md`, the Shorts standards, `CHARACTERS/main_character_reference.jpg`. Read `CLAUDE-HANDOFF.md` and `LESSONS-LEARNED.md` first. Never modify these files; propose changes to Sean.
3. `fight_playbook_video_build` skill (mamba repo, `skills/fight_playbook_video_build/SKILL.md`).
4. This file.

Open conflicts waiting on Sean (see `production/audit/GROK_AUDIT.md`): R26 (no animation) vs the Nov 23 brief asking for animation; ground line vs flat background.

Outfit split (Sean, Nov 23): long form hero wears the black shirt with red side stripes; Shorts and TikTok hero wears a gray tank top.

Read `production/audit/GROK_AUDIT.md` once to know which mistakes the old pipeline made.

## 1. Brand lock (from Sean's skills, Nov 22 to 23, 2026)

* Hero: black or charcoal bald muscular boxer, completely smooth blank face, only two slanted white eyes. No mouth, nose, eyebrows or other features, ever. Black sleeveless shirt with red side stripes, no lettering. Navy shorts with red trim. Barefoot. Black MMA gloves with red wrist straps (bare hands only in a grip tutorial).
* Opponent: always red and clearly bigger (rig scale 1.1).
* Background: one of pale blue #D8EEFE, warm sand #ECD6B0, sage green #C4D6C4, slate gray #BEC6D0, deep teal #30767C, cream #F5ECD6. Never the same as the previous video. Sean's named colour wins.
* Text: Bebas Neue. Big text top centre, white with dark outline, max 3 words, and it must add information, not repeat the caption bar.
* Shorts keep a bottom caption bar synced to the spoken word. Long form has no bottom caption bar.
* No dashes anywhere in on screen text, captions, titles, descriptions or messages to Sean. Gender neutral wording.
* Strikes land only on chin, jaw or body. Speed lines are the only strike effect, added in code.
* No safety lines. Long form ends with the subscribe ask (SUBSCRIBE starts after the last word, holds 3 s or more) and a 1, 2 or 3 reply question.
* Description carries the verbatim narrator disclaimer and Skool line and never says AI or animated.

The rig colours live in the storyboard `style` block. Change them there only.

## 2. Engine (production/engine)

* `src/rig.js` Fighter: joints solved with two bone IK. Feet are pinned at the ball of the foot, gloves aim at world targets, the reach ratio of every limb is recorded.
* `src/motion.js` Technique library. Each move is a set of timed channels (foot, hips, shoulders, arm, plus extras) over a normalised duration with an impact point and a power value. Add new techniques here (jab, hook, uppercut, slip, roll, kicks, checks, escapes) as channel sets, never as one off poses.
* `src/engine.js` Scene, toon shading with ink outlines, shadows, auto staging (opponent placed so the punch lands at 97.5 percent arm reach), opponent reaction, outline highlights, speed lines, captions, per frame QC metrics.
* `src/fx.js` Overlay helpers: bars through joints, rings, leader labels, floor arcs, ghost footprints.
* `boards/<video>.js` One storyboard per video: script, caption timings, shots.
* `render.mjs` Headless Chromium render to H.264, plus `qc_frames.json`. `--still t1,t2` renders single frames; `--cam az,el,dist,fov,x,y,z` overrides the camera for framing tests.
* `qc.py` Video level QC, writes `QC_REPORT.md`.

Commands:
```
cd production/engine && npm install
node render.mjs <board> <outdir> --still 0.8,5.6,19.7     # look before you render
node render.mjs <board> <outdir>                           # full render, silent
ffmpeg -i <outdir>/video_silent.mp4 -i <voice> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest <outdir>/final.mp4
python3 qc.py <outdir> <outdir>/final.mp4 --audio <voice>
```

## 3. Storyboard rules

* Write the board from the narration timings. Every shot states: id, angle name, start, end, move and clock, camera, top text, and what must be visible (`mustSee`).
* Shot length 0.6 to 3 s. Never the same angle twice in a row. At least 10 distinct angles per minute.
* Pick the angle that shows the lesson, not the one that looks cool:
  * Footwork and pivots: low ground camera on the foot, or high angle with a floor arc and a ghost footprint.
  * Hip and shoulder rotation: high rear three quarter with hip bar (amber) and shoulder bar (white).
  * Kinetic chain: side view, 0.24x to 0.3x slow motion, outline highlight travelling foot to fist, labels 1 to 4 lighting in order.
  * Contact: over the hero's punching shoulder toward the opponent's face. Side views of a faceless head read as the back of the head; avoid them for contact.
  * Money moment: slow motion hard zoom on contact (ease out quart, 0.25x to 0.3x).
* Stay on the hero's right side of the action line (camera azimuth between about -1.3 and +1.3) so fighters never swap screen sides.
* Slow motion is a clock function (action time = video time times k). Loops must have a period longer than the move.
* Cover every voice pause with motion: a camera move, a reset, or a replay. Never a frozen frame.
* Open on the technique in motion in frame 1. End by looping into the hook on Shorts.

## 4. Technique accuracy

Before animating a technique, write its channel order and check it against coaching sources:
* Cross: rear foot pivots on the ball, heel turns out and lifts; hips turn; shoulders turn further; arm extends last and snaps straight back to guard; lead hand stays at the face; chin tucks behind the punching shoulder.
* Arm punch (the mistake): no pivot, hips nearly still, reaching lean.
Add each new technique's checklist here once it is built.

## 5. QC gate (run every time, before Sean sees anything)

`qc.py` blocks delivery on: overextended limbs, detached or sliding feet, gloves inside heads or torsos, glove clashes, fighters not facing each other, heels below the floor, overlapping bodies, repeated angles, under 10 angles per minute, top text over 3 words, any dash, captions not matching the script word for word, frozen seconds, audio and video length mismatch.

It warns on: subjects out of frame, holds outside 0.6 to 3 s, captions more than 0.25 s from a voice onset.

Then do a human style pass on a contact sheet of every shot plus frame sequences on each contact: does the picture do what the narration says at that second? Fix only the failed shots and re-render.

Report what was checked, what passed and what still needs Sean's decision. State that the review was frame by frame.

## 6. Voice

* Build silent first. Narration only after Sean approves the visuals (his rule).
* Exception used for A/B tests: reusing an existing approved voice track costs nothing and keeps the comparison fair.
* Caption bar text comes from the actual spoken words. Measure timings from the audio (faster whisper with word timestamps where available).

## 7. Learning log (update after every video)

| Date | Video | Strategy | What worked | What failed | Analytics |
| --- | --- | --- | --- | --- | --- |
| 2026-11-23 | punch_with_body rebuild (A/B vs Grok) | Same script and voice, 3D rig, 17 shots | Rig mechanics, over the shoulder contact, outline highlights | First pass: emissive glow recoloured the costume (fixed with outline glow); profile contact shots unreadable (fixed with over the shoulder) | Not posted |

When YouTube Studio data arrives, record per video: CTR, average view duration, percent viewed, the retention dips with timestamps, and which shot sat at each dip.
