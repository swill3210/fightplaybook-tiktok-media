# Production notes: arm mechanics (Sean t17u, Nov 23, 2026)

Why this exists: v2 of the liver video was rejected because arms were anatomically wrong. Sean's screenshot was V94 (2:02 to 2:04): a body shot where the elbow kinked and dropped so the forearm looked broken and rubbery. The same fault repeated across the video and the earlier QA passed it. These notes apply to every Fight Playbook still from now on.

## 1. The arm mechanics rule (hero, opponent and guard hands)

* Straight punches (jab, cross, body jab): shoulder, elbow and glove in one straight line. Elbow straight or only slightly soft. No kink, no drop, no forearm sag.
* Hooks: a clean 90 degree L. The elbow sits at the same height as the glove and the forearm is level.
* Uppercuts and shovels: the elbow is tucked at the puncher's own hip, the forearm near vertical, the glove directly above the elbow (forearm at least 70 degrees, never a 45 degree diagonal).
* Retracting arms come back along the same path they went out on.
* Always a fail: twisted or backwards elbows, bent wrists at the glove, upper arm and forearm of clearly different lengths, extra or missing limbs, detached or floating gloves, shoulders that do not rotate into the punch, gloves drawn as bare fists with separate fingers.
* Guard hands: the non punching glove at the chin, elbow tucked to the ribs, never dropped to the hip unless the spec says so.

## 2. Prompt template (ElevenLabs creative_edit_image, gpt-image-2.6-sunburst)

Structure: `Edit this image. <shot description> <ARM MECHANICS block for the punch type> <GUARD> <KEEP> <NEGATIVE LIST>`

Build script: `edit/work/mk_v3_prompts.py` (blocks below), extra rounds in `edit/work/mk_v3_r3.py`. Generated prompts are in `edit/prompts_v3/`.

Character tags
* HERO (long form): the main character (black sleeveless shirt with red side stripes, navy shorts with red trim, black gloves with red wrist straps)
* OPP: the opponent (bigger, red tank top, black shorts, plain black gloves)
* Outfit split: long form uses the black shirt with red stripes and navy shorts with red trim. TikTok and short form use the gray tank top.

STRAIGHT block
> STRAIGHT ARM MECHANICS: the punching arm is fully extended in one straight line from the shoulder through the elbow to the glove, the elbow is straight or only very slightly soft, the forearm and upper arm are in line with no bend, no drop and no sag at the elbow, the shoulder rolls forward to the chin.

HOOK block
> HOOK ARM MECHANICS: the punching upper arm is lifted out to the side at the same height as the glove, the elbow is bent at a clean 90 degree angle, the forearm is level and horizontal, travelling sideways across into the target, and the elbow sits at exactly the same height as the glove, forming a clean flat L shape seen from above or the side. The shoulder of the punching arm is rotated forward and the hips are turned into the punch.

UPPERCUT / SHOVEL block
> SHOVEL UPPERCUT ARM MECHANICS: the punching elbow is tucked in tight against the puncher's own hip and lower ribs, the elbow is bent at about 90 degrees or slightly less, the forearm points almost straight up (near vertical), and the glove drives upward from below into the target, palm side facing up and in. The knees are bent and the hips lift into the punch.

Stricter uppercut wording that fixed the stubborn shots (V70, V75, V79):
> The punching upper arm hangs straight DOWN along the puncher's own side so the elbow sits right beside the own hip and belt line, the elbow is bent at about 90 degrees, the forearm points straight UP, vertical, from the hip to the glove, the glove directly above the elbow, NOT a 45 degree diagonal.

GUARD block
> GUARD: the non punching glove stays up beside the chin with the elbow tucked down against the ribs.

KEEP block
> Keep the camera angle, framing, size and position of both characters, the art style, line weight, colours and the plain flat sage green background exactly the same as the reference. Both characters have smooth dark charcoal skin and blank faces with only two white eyes, no brows, no nose, no mouth. Every person has exactly two arms, two gloves and two legs, normal human arm lengths with upper arm and forearm of equal length, one natural elbow per arm, and every glove is attached to a visible wrist and forearm. No text, no effects, no motion lines, no border.

NEGATIVE LIST
> Do NOT draw: a kinked, bent, broken, sagging or drooping forearm; an elbow that drops below a straight punch; an elbow hanging far below or far above a hook glove; rubbery, noodle, stretched or wavy arms; a twisted or backwards elbow; a bent or broken wrist at the glove; an upper arm and forearm of very different lengths; extra arms, extra gloves, extra hands, missing arms, or floating gloves not attached to a forearm.

Extra negatives when needed
* Skin: both characters have dark charcoal grey skin, NOT tan, peach, brown or light grey (V75, V70 drifted).
* Gloves: a proper padded boxing glove, one rounded mitt with the thumb along the side, NO separate fingers, NOT an MMA glove, NOT a bare fist (V80).

## 3. Prefer reference image edits

* Always edit from the node of a still whose camera, framing and background are already right (`connect_from` = that still's node from `ledger_liver.json`). Only describe what changes (the arm) and lock everything else with the KEEP block.
* Use 2 generations per call and pick the cleaner one in the zoomed review.
* If a round fails, rewrite the arm wording more literally (where the elbow is relative to the hip or glove, which way the forearm points) rather than repeating the same prompt.
* Never fix an arm by cropping, covering with a text badge, speed lines, blur or a camera move. Regenerate.

## 4. Mandatory zoomed crop arm QA checklist (before any render)

For EVERY still, including start pose stills (V2a, V3a), at 2x zoom on each arm:

1. Count: exactly two arms, two gloves, two legs per person. Every glove attached to a forearm.
2. Straight punch: draw an imaginary line shoulder to glove. Does the elbow sit on it? Any kink, drop or sag = FAIL.
3. Hook: is the elbow at glove height and the forearm level? Elbow far above or below the glove = FAIL.
4. Uppercut or shovel: is the elbow at the own hip and the forearm near vertical? Diagonal reaching arm = FAIL.
5. Segments: upper arm and forearm about equal. Wrist straight into the glove. Elbow bends the natural way.
6. Shoulder of the punching side rotated forward.
7. Guard hand at the chin, elbow tucked.
8. Opponent arms get the same checks.
9. Borderline = FAIL. Write the shot, the fault and the round in the QA log.

Tools: `edit/work/arm_sheets.py` (2 up zoomed audit sheets), `edit/work/cand_arm.py "<note>" IDs...` (zoomed candidate crops), `edit/work/grid_sheet.py` (grid sheets to set glove points).

## 5. Render QA

* Decode the delivered mp4, review every shot on contact sheets (`edit/work/v3_review_sheets.py`, sheets `qa/v3/r1_*.png`).
* Slow motion pass: every punch shot, every second frame of the first 16 frames (`qa/v3/r2_*.png`), checking that the camera push, shake and speed lines never make a straight arm look bent and that two phase shots (V2a to V2, V3a to V3) travel a believable path.
* Repeat until a full pass finds nothing.


## 6. Hook rules (PERMANENT, Sean pt18u, Nov 23, 2026)

The full standard is `/workspace/fightplaybook/standards/hook_rules.md`. In short:

* LEFT HOOK is thrown with the LEFT arm, RIGHT HOOK with the RIGHT arm. Never switch arms mid animation, and the arm must match what the spec or script calls the punch.
* The elbow bends about 90 degrees into an L, with the fist and elbow moving together. On head hooks the elbow is roughly level with the fist.
* The fist travels a short, curved, horizontal path AROUND the guard. A hook is not a straight punch, jab, cross, uppercut or exaggerated swinging slap.
* Shoulder, hips and torso rotate. On the right hook the right shoulder and hip go forward together and the rear foot pivots.
* The non punching hand stays at the chin, and the punching hand returns to guard after impact.
* Body hooks (liver shots, left hooks to the body) lower the level by bending the knees and rotating the torso. The arm keeps its L, with no unnatural bend.
* The elbow stays anatomically connected. Never twist, detach, reverse or unnaturally bend an arm. Anatomy stays consistent from every camera angle.
* Orthodox hero: the left is the lead. A liver shot is the LEFT hook to the opponent's RIGHT side.
  * Hero facing the camera: the hook arm is on the image right and the guard on the image left.
  * Opponent facing the camera: their liver side is on the image left.
  * Opponent from behind: their liver side is on the image right.

Prompt blocks: `HOOK_L`, `HOOK_BODY` and `HOOK_NEG` in `edit/work/mk_v3_prompts.py`. Hook prompts are built by `edit/work/mk_v4_hooks.py`. Every hook prompt is:
`Edit this image. <shot> <HOOK_L> [<HOOK_BODY>] <KEEP> <NEG> <HOOK_NEG>`

Hook QC (every hook shot, zoomed, borderline = FAIL):
1. Spec arm vs the arm used.
2. L at about 90 degrees.
3. Elbow height.
4. Curved path (start pose to impact).
5. Guard hand at the chin.
6. Hip and shoulder rotation.
7. Rear foot pivot on right hooks.
8. Knee bend on body hooks.
9. Return to guard if shown.

Then do a slow motion pass of every hook in the render. Log the results in `qa/v4/hook_qa_v4.md`.
