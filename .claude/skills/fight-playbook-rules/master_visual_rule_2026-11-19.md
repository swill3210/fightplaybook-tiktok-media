# Fight Playbook Shorts — Master Visual Rule
Paste this ONCE into your YouTube bot, at the top of its system prompt. It applies to EVERY short. Do not paste it per-video. Do not skip it for a "quick" short.

This rule exists to stop one bug, which has already cost credits on multiple shorts: the narration/text moves to a new action, but the image stays on the same pose. Zoom, crop, or an arrow is not movement.

## THE LAW — 1 verb = 1 new image
- Parse the script into ACTION VERBS first, not steps. "Wide feet, sink hips, head up" is 3 verbs, so it is 3 images. Never 1 image per step.
- Every image must have: Start Pose, End Pose, Visible Change.
- Visible Change means a body part has moved to a different position in the frame. Feet wider, hips lower, chin up, elbows forward, arms up, grip open — it must be measurable in the image.
- If the new image is identical to the previous image except for text, zoom, or crop, REJECT it and regenerate that ONE shot only. Never re-render the whole video for one bad shot.

## Pose-change check — run this before any video is assembled
For each consecutive pair of images, ask:
1. Did a body part move? Yes / No
2. Is the body part named in the text the body part that moved? Yes / No
3. Is the direction in the text the direction in the image? (Up = up, forward = forward, down = down) Yes / No

If any answer is No, that shot FAILS. Regenerate that shot only, with a new Start Pose and End Pose written out in full. Do not move on, do not "fix it in the edit" with an arrow.

## Camera rules — pick by action type, not by habit
- Feet, hips, weight, stepping, dropping: FULL BODY, feet and head in frame. If feet are cut off, the shot fails.
- Head, chin, eyes: CLOSE-UP on head only. Chin up must read as chin up, eyes forward.
- Hands, grip, elbows: CLOSE-UP on hands / arms. Use a FRONT angle for "forward" — forward does not read from a side angle.
- A punch, kick, or tackle landing: show the landing. No landing = no shot. Use front for impact, side for form, overhead for ground work.
- Never use a legs-only still for a kick. Every kick still shows hands up and the full body.
- Never use the same camera angle for two consecutive teaching stills unless the action is a deliberate repeat (self-test, summary board, loop reset).

## Text rules
- Big on-screen text only, max 3 words per still.
- (REMOVED by Sean 2026-11-19 10:30 PM ET: the bottom caption bar is allowed again. Keep it in sync with the VO.)
- No text over the hero's eyes. No label cropped at the frame edge.
- Text must name the action in the image, not the next action, not the last action.

## Character and look — locked for every short
- Hero: black/charcoal bald faceless muscular boxer — face completely smooth and blank with ONLY two slanted white eyes, NO mouth, NO nose, NO eyebrows, NO other facial features ever. Black sleeveless shirt with red accents and red side stripes, black MMA gloves with red wrist straps, NO lettering on the shirt.
- Opponent: same faceless style, red sleeveless shirt, no lettering.
- Drill partner (if any): plain grey shirt, no lettering. Opponent is always red, partner is always grey — never swap them in a split frame.
- Background: one solid colour per short, from the rotation — Pale Blue, Warm Sand Beige, Deep Teal, Warm Cream Yellow. Never the same colour twice in a row.
- Looped shorts: last frame must match the opening pose, so the loop cuts cleanly back to 0:00.

## Before / after — use it for hard moves
If a move is hard to read in one still — grip break, slip, roll, drop — use one of these, in order:
1. Two frames back to back: before → after, with a visible pose change between them.
2. A before/after split in one frame, left = before, right = after, arrow left to right.
Do NOT jump from locked to free, or from standing to down, in a single cut with no middle frame.

## Credit-saving workflow — do this in order, do not render video first
1. Generate STILLS only, one per verb.
2. Run the pose-change check above on the stills. Fix failed shots only.
3. Assemble the video silent, with big text only. Check text sync — big text must match the action on screen at that second.
4. Only then add narration, lofi bed, and SFX. Never spend narration / render credits on a video whose stills have not passed the pose check.

## How to fix the shorts that already have this bug — do NOT re-render whole videos
For each existing short, list only the failed shots:
- Shot time, verb, what the text says, what the image actually shows.
- Regenerate ONLY those shots, with a new Start Pose / End Pose.
- Patch the new shots in. Keep the good shots, the audio, and the loop.
- Re-run the pose-change check on the patched shots only.

## QA checklist — bot must pass ALL of these before export
- [ ] Image count = verb count. If verbs > images, FAIL.
- [ ] No two consecutive images are the same pose with different text.
- [ ] Every "up / down / forward / wider / lower" word matches the direction in the image.
- [ ] Feet/hips/weight shots are full body, feet in frame.
- [ ] No text over eyes, no cropped labels.
- [ ] Character lock holds in every frame — no mouth, no nose, no shirt lettering.
- [ ] Loop short: last frame matches first frame pose.
- [ ] Only failed shots were regenerated. The rest of the video was not re-rendered.
