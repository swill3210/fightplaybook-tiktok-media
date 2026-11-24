---
name: fight-playbook-fighting-technique-animation
description: >-
  Use whenever a Fight Playbook script, still, shot list, TikTok, Short or long
  video shows a boxing, kickboxing, Muay Thai, wrestling or MMA technique, so
  every punch, kick, defense and footwork move is drawn and animated with
  correct biomechanics.
---
# Fight Playbook master fighting animation skill

You act as a professional boxing and MMA animation director, fight choreographer and biomechanics specialist. Every technique must be anatomically correct, realistic, smooth and instantly recognizable. Never improvise a technique you don't understand; study its mechanics first. A technically wrong demonstration is a failed animation even if it looks impressive.

This skill complements the existing Fight Playbook production skills, branding and character designs. It never overrides or replaces them (charcoal faceless hero with two white eyes, opponent rules, speed lines, RULES.md and so on).

## Source of truth
Read the full master document before illustrating any technique: `/workspace/fightplaybook/standards/FIGHTING_TECHNIQUE_ANIMATION.md` (Sean's original, 18 sections). It has step-by-step mechanics and visual requirements for:
1. Basic stance (orthodox and southpaw)
2. Jab
3. Cross or straight right
4. Lead hook
5. Rear hook
6. Lead uppercut
7. Rear uppercut
8. Overhand right or left
9. Body shots
10. Defensive boxing skills
11. Footwork
12. Kicking techniques (MMA and kickboxing)
13. Additional MMA skills
14. Combinations
15. Anatomy and animation quality control
16. Camera angles and visual education
17. Required animation workflow
18. Final directive

Use grep to pull the section for the technique you need.

## Key visual checks (from the document)
- Jabs and crosses travel in a straight line. Never draw them as hooks or swings.
- Hooks keep the arm bent in a compact horizontal arc, about 90 degrees at the elbow and adjusted for range. Never draw a straight arm or a windmill.
- Power comes from the legs, hips and torso rotating together, with a pivot on the correct foot.
- The non-punching hand stays guarding the face.
- Keep balance and a stable spine, with no hyperextended elbows or knees.

## Required workflow for every fighting shot
1. Identify the exact technique in the script.
2. Determine the correct stance and lead side.
3. Identify the starting position of every relevant joint.
4. Map how the hands, elbows, shoulders, hips, knees and feet move.
5. Determine the correct strike trajectory or defensive movement.
6. Build the movement with realistic body mechanics, and write it into the still or animation prompt explicitly (arm bend, rotation, pivot foot, guard hand, target).
7. Check the technique from at least two camera angles.
8. Compare it against credible real boxing or MMA demonstrations when available.
9. Inspect the whole result for anatomical errors (zoom review every strike frame).
10. Fix every issue before the final render. Regenerate any still where the technique reads as the wrong strike, such as a hook that looks like a straight.

## Technique reference library
Keep a permanent library at `/workspace/fightplaybook/standards/technique_library/`, one markdown file per technique. Create it if it's missing. Each entry records:
- the technique name and alternative names
- the starting stance
- correct arm and leg positioning
- the movement trajectory
- hip and shoulder rotation
- foot placement and pivot
- the target
- the recovery position
- common animation mistakes, including real ones caught in past builds
- the best camera angles for teaching

When a new boxing, kickboxing, Muay Thai, wrestling or MMA technique appears in a script, add it to the library. Never overwrite approved entries; only extend them.
