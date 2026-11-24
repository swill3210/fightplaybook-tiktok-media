# Fight Playbook hook animation rules (PERMANENT, Sean pt18u, Nov 23, 2026)

These rules apply to every Fight Playbook video with a hook, long form and short form. They sit on top of the general arm mechanics rules in each video's `edit/production_notes_arm_mechanics.md`.

## Left hook
* Thrown with the fighter's LEFT arm, never the right.
* The left elbow bends about 90 degrees into an L. The fist and elbow move together.
* The fist travels a short, curved, horizontal path toward the opponent.
* The left shoulder, hips and torso rotate to make the power.
* On a head hook the elbow stays roughly level with the fist.
* The right hand stays at the chin.
* After impact the left hand returns to guard.

## Right hook
* Thrown with the fighter's RIGHT arm, never the left.
* The right elbow bends about 90 degrees.
* The fist travels a curved, horizontal path toward the opponent.
* The right shoulder and hip rotate forward together, and the rear foot pivots naturally.
* The left hand stays at the chin.
* After impact the right hand returns to guard.

## Critical visual rules
* A hook is NOT a straight punch, jab, cross, uppercut or exaggerated swinging slap.
* The fist goes AROUND the opponent's guard, not straight forward.
* The elbow stays anatomically connected to the shoulder and forearm. Never twist, detach, reverse or unnaturally bend an arm.
* Never switch left and right arms during the animation. The arm must match what the spec or script calls the punch.
* Show realistic shoulder rotation, hip movement and foot position. Keep anatomy consistent from every camera angle.
* Body hooks, including liver shots and left hooks to the body, lower the level by bending the knees and rotating the torso. The arm keeps its L, with no unnatural bend.

## Which arm on screen (orthodox hero: left foot and left hand lead)
* A liver shot is normally the LEFT hook to the opponent's RIGHT side.
* LEAD hand means the hand on the side nearer the opponent. That is the hero's left, and it is the hook hand.
* REAR hand means the right. It stays at the chin.
* Hero facing the camera, including shots from behind the opponent and the opponent's POV: the hook arm is on the IMAGE RIGHT and the guard hand on the IMAGE LEFT.
* Hero in three quarter view facing right with the chest open to the camera: the hook arm is the front arm on the image right.
* Opponent facing the camera: their right side (the liver) is on the IMAGE LEFT.
* Opponent seen from behind: their right side is on the IMAGE RIGHT.

## Prompt wording (ElevenLabs edits)
Template blocks are `HOOK_L`, `HOOK_BODY` and `HOOK_NEG` in `videos/<video>/edit/work/mk_v3_prompts.py`, copied into each new video's prompt builder.

Positive wording:
> LEFT HOOK: the main character throws the hook with the LEFT arm, the LEAD arm on the side nearer the opponent. The left elbow is bent at a sharp 90 degree right angle so the upper arm and forearm make a clear letter L. The upper arm is lifted out to the side, almost horizontal, and the forearm is horizontal, wrapping AROUND from the side into the target, with the elbow at the same height as the glove. The left shoulder and the hips are rotated into the punch and the torso is turned. The RIGHT glove (the rear hand) stays tight against the chin with the right elbow tucked to the ribs.

Body hook addition:
> BODY HOOK: the main character lowers the level by bending BOTH knees deeply and turning the torso, so the shoulder drops toward the height of the opponent's ribs. The arm keeps the same 90 degree L, with the elbow at glove height. The arm itself does not bend down to reach low.

Negatives:
> Do NOT draw: a hook thrown with the wrong arm (no right arm hook when a left hook is called for); a straight arm hook or an arm that is almost straight like a jab or cross; an upward uppercut path; a wide looping swinging slap with an open arm; the guard hand dropped away from the chin; a twisted, reversed, detached or backwards bent elbow; arms switching sides; an upright stiff body with no knee bend on a body hook.

## QC checklist (every hook shot, zoomed, borderline = FAIL)
1. Arm called for by the spec or script, and the arm used on screen. Work it out from the hero's facing (see above).
2. L at about 90 degrees. Not straight, not more open than about 110 degrees.
3. Elbow height: level with the glove on head hooks, at glove height on body hooks.
4. Curved path: the glove comes from the side around the guard (start pose to impact where both exist). No straight forward path.
5. Guard hand at the chin.
6. Shoulder and hip rotation visible.
7. Rear foot pivot on right hooks.
8. Knee bend on body hooks.
9. Return to guard, where the shot shows it.
10. Opponent arms and any guard hands pass the general arm mechanics rules.

Regenerate any failing hook on ElevenLabs before delivery and re-check it. Never hide a wrong hook with a crop, text badge, blur or camera move.
