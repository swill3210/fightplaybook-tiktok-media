# Audit of the current Fight Playbook production (Grok)

Date: Nov 23, 2026. Reviewer: Claude.

## What I reviewed, and how

| Source | What it is | How I reviewed it |
| --- | --- | --- |
| 7 published TikTok cuts from the `fightplaybook-tiktok-media` releases | punch_with_body, hit_harder, check_a_low_kick, roll_under_the_hook, want_to_drop_someone_fast, tt_front_headlock, howtofight teaser 1 | Contact sheets every 2 s, frame sequences at 4 to 5 fps on key beats, per frame motion analysis, caption frames read one by one, audio loudness envelope |
| `swill3210/mamba` share package | Fight Playbook build skill, Khoj creative director brief, motion design skill, AI Town v7 build script | Read in full |

| `swill3210/the-fight-playbook-claude-handoff` (added later the same day) | Grok's full export: RULES.md R1 to R49, long form skill, character reference sheet, liver v4 silent cut (150 s, 107 shots), three finished long form videos, Studio analytics (Nov 13), competitor research, QA reports | Read the handoff, lessons, rules, character spec and analytics; contact sheet of the liver v4 cut every 5 s |

I watched frames, not chapters. Studio analytics in the handoff are from Nov 13 (two days after launch), so retention conclusions are early.

## Long form findings (liver v4 silent cut and channel data)

* The liver v4 stills are well illustrated and on model. Grok's own QA reports 0 anatomy defects after four versions, but getting there took 257,559 ElevenLabs credits and up to 14 regenerations for a single jab (V94). All 25 hook shots failed the strict audit in v3. The method works only through brute force, and it will fail the same way on every punch heavy video.
* Motion is still stills plus eased push ins, shakes and two frame "start pose to impact" phases. A punch is never shown travelling, retracting, or turning the hips, which is exactly what most lessons are about.
* Channel data (Nov 13): Shorts bring 95.9 percent of views and 91 percent of subscribers. Long form CTR is 2.4 to 4.0 percent and AVD is 1:10 to 1:53 on 3 to 6 minute videos. "Fight Someone Taller" bleeds viewers continuously from 0:20; "Stop Flinching" holds a 42 percent plateau, then drops to 20 percent at the outro. Best Shorts are short, single idea and interactive ("Try This on Your Own Chin", 93 percent viewed).

## Rule conflicts Sean needs to rule on

* **R26 says "Still images with hard cuts. No animation. The cut out puppet rig approach is rejected."** Sean's brief to Claude (Nov 23) asks for 2D and 3D animation with Three.js or Blender. The sample here follows the newer brief. If R26 still stands, the rig can be used to produce perfectly posed stills instead of motion.
* **Ground line vs flat background.** The mamba skill asks for a flat ground line under the feet; R10 forbids floors. The sample uses a flat background with contact shadows only.
* **Shorts caption bar** (mamba skill) vs no bar mentioned in R32. The sample keeps the synced bar.

## How Grok builds a video today

1. Grok Imagine generates one still per beat (faceless charcoal fighter, coloured background).
2. ffmpeg holds each still about 1 to 2 s with a slow zoom or slide, sometimes a short image to video clip.
3. Speed lines, rings, arrows, step badges and two caption layers are burned in with ffmpeg.
4. ElevenLabs narration (Ryan Kurk voice) is laid under it; Shorts loop the last line into the first.

## What Grok does well (keep)

* Fast cutting: a new visual every 1 to 2 s in the Shorts. Retention pacing is not the problem.
* Clear numbered structure (Step 1, 2, 3) and a mantra ending.
* Strong, recognisable brand: faceless charcoal fighter, two white eyes, red accents.
* Loop endings ("so if this is you..." back into the hook) are a smart Shorts tactic.
* Wrong versus right split screens are the right teaching idea.

## The biggest limitations (in order of damage)

### 1. Nothing actually moves, so the technique is never shown

Each beat is a separate still. The viewer never sees the kinetic chain (foot, hips, shoulders, arm) as one motion, which is the whole lesson in most Fight Playbook topics. Image to video clips add drift, not mechanics. This caps how good the channel can look no matter how good the prompts get.

### 2. Visuals contradict the narration

| Video | Time | Narration | What is on screen |
| --- | --- | --- | --- |
| punch_with_body | 14.0 to 15.4 s | "Snap it back to your guard" | Arm stays fully extended for the whole line (`evidence/snap_back_mismatch.jpg`) |
| check_a_low_kick | about 4 s | "Hands stay up" | Hero's hands are at the waist |
| check_a_low_kick | about 6 s | "Step one" (checking) | The opponent lifts the knee, not the hero |
| check_a_low_kick | about 13 s | "Meet their shin" | Knee against knee, no shin contact (`evidence/low_kick_errors.jpg`) |

### 3. Anatomy and physics errors that an image model cannot self check

* Fighters with both feet off the ground and no planted leg (check_a_low_kick, "step three", "plant back").
* Kicking shin passing through the hero's leg (check_a_low_kick opening).
* Opponent throwing both hands straight overhead as a reaction to a jab (want_to_drop_someone_fast).

### 4. Character and screen direction drift between shots

* Hero wears boxing gloves in punch_with_body and MMA gloves in hit_harder. The skill locks black MMA gloves with red straps.
* Opponent switches between red and grey tank tops; in punch_with_body the opponent is the same size as the hero, while the skill says clearly bigger.
* Fighters swap screen sides between consecutive shots (want_to_drop_someone_fast), which breaks the 180 degree rule and confuses who is who.

### 5. Caption problems

* A word is missing: the bar shows "TURN THE HIPS AND" then "THROUGH THE PUNCH"; "shoulders" never appears (`evidence/missing_word_shoulders.jpg`).
* The big headline repeats the caption bar word for word, so the screen says the same thing twice instead of adding information.
* Chunks break mid phrase ("KEEP YOUR SHOULDERS AND", "SO NEXT TIME YOU").

The synced caption bar itself is Sean's rule for Shorts and stays.

### 6. Dead narration space not covered

punch_with_body has a 1.5 s voice pause (16.5 to 18.0 s) over a near static frame.

## What to use instead

| Need | Tool | Why |
| --- | --- | --- |
| Correct body mechanics in motion | Procedural 3D rig in Three.js with analytic IK (built here, `production/engine`) | Feet are pinned to the floor by maths, gloves land exactly on target, limbs cannot stretch past real length, every move is a set of timed channels (foot, hips, shoulders, arm) that can be checked |
| Camera language | Scripted virtual cameras per shot | Real angles, push ins, slow motion and over the shoulder contact shots; impossible to fake consistently with stills |
| Explanations | 2D overlay layer drawn from 3D joint positions | Hip and shoulder bars, pivot arcs and labels stick to the body as it moves |
| QC | `production/engine/qc.py` plus per frame rig metrics | Catches the error classes above automatically before Sean sees a cut |
| Later upgrade | Blender with a rigged, sculpted character and mocap clean up | Best possible look; needs a modelled character asset and is a bigger project. Not available in this container today |

Honest trade off: the procedural rig gets the movement right but it is a clean toon render, not Grok's painted illustration look. Painted texture can be layered on later (Blender toon shader, or using Grok stills only for static title and thumbnail art).
