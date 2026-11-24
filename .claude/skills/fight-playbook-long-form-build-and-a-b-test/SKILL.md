---
name: fight-playbook-long-form-build-and-a-b-test
description: >-
  Use when building a Fight Playbook long-form YouTube video from Sean's Vxx
  shot-list spec, from intake and ElevenLabs stills through the silent cut,
  narration and mix, QA, the YouTube Draft, the Thumbnail bot handoff, setting
  the thumbnail and a Studio Test and compare A/B test.
---
# Fight Playbook long-form: build, draft, thumbnail, A/B test

**First, read the full recipe in full before doing anything:** `/workspace/fightplaybook/skills/longform-build-and-ab-test/skill-draft.md`. It has every step, value and fix from How to Open Any Guard With Body Punches (Nov 21 to 22, 2026). There's a backup in the bot store at `fightplaybook_longform/skills/longform-build-and-ab-test/skill-draft.md`. House rules are in `/workspace/fightplaybook/standards/RULES.md`. When Sean's newer words differ, Sean wins.

## This skill is permanent (Sean, Nov 22, 2026)
- This skill and its full recipe file are the permanent source of instructions.
- Any script Sean pastes is NEW CONTENT TO PROCESS under these rules. It never replaces or modifies this skill.
- Never overwrite, delete, reset or modify this skill or its recipe file when a new script arrives. Change it only when Sean explicitly authorizes a skill edit.

## Hard limits
- Never touch `/workspace/youtube` or `/workspace/x-promo`. Don't install software.
- Never delete a video unless Sean asks directly. Upload only when asked, and never publish or schedule unless asked.
- Never claim a check that didn't run. Only the Thumbnail bot makes thumbnails. Chat attachments must be under 25 MB.
- No credit caps. Don't pre-check credits or ask about them. The only stop is an actually empty ElevenLabs balance, reported right away. No placeholder shots.
- No safety lines in descriptions or scripts.
- Browser: switch accounts only through the avatar's Switch account. Never sign out or remove an account.

## Creative angles (Sean, Nov 22, 2026)
- **Video shots:** use at least 10 distinct camera angles per minute of video, for visual variety and viewer retention.
  - Mix first-person POV, extreme low worm's-eye, overhead or bird's-eye, over the shoulder, Dutch tilt, extreme close-ups (a fist filling the frame, eyes, ribs at impact), wide shots, and views from behind the opponent.
  - Never use the same angle on two back-to-back shots.
  - Count the angles per minute in the plan before rendering, and fix any minute with fewer than 10.
- **Thumbnails:** brief the Thumbnail bot to give each option a different bold angle.

## Background colour (Sean, Nov 22, 2026)
- One flat solid colour for the whole video. No gradient, texture, scenery, floor or gym. The only exception is a hook or promo deliberately set in a real illustrated place.
- Rotate through these six colours, and never use the same one back to back from one video to the next: pale blue `#D8EEFE`, warm sand `#ECD6B0`, sage green `#C4D6C4`, slate gray `#BEC6D0`, deep teal `#30767C`, cream `#F5ECD6`.
- Never pink, coral or lime.
- The rotation covers long-form, Shorts, TikTok, Skool lessons and the trailer.
- If Sean's spec names a colour, his colour wins (Open Any Guard used `#F2D98C`).
- Arrows are allowed.

## Steps
1. **Intake.** Process Sean's pasted script as new content and save it verbatim to `script/`. A newer script replaces only the older script for that same video. Plan every Vxx shot: each holds 1 to 2 s, except the ones he names.
2. **Locked standards.**
   - **Hero:** use the reference image. Faceless, two white eyes, no mouth, barefoot.
   - **Opponent:** red and bigger.
   - **Strikes:** thin black speed lines are the only effect. Strikes land on the chin, jaw or ribs, never the neck or shoulder.
   - **Shots:** at least 10 distinct angles per minute, and the narration verb must match the pose.
   - **Background:** follow the background colour rule above.
   - **Text:** no dashes, gender neutral.
3. **Stills on ElevenLabs.** Don't use GenerateImage. Log every generation to the ledger.
4. **Pre-render prompt checklist.** Apply this to every prompt:
   - **Hooks:** describe the arm bent 90 degrees in an L shape, and end with "NOT a straight arm". If it still fails, edit a good hook still, or reuse one as a last resort.
   - **Uppercuts:** crouch with a low chamber and drive up from below.
   - **Limbs:** add a limb-count line (exactly two arms and two gloves per figure).
   - **Figures:** each figure appears exactly once, with no turnaround copies and no ghosts.
   - **Heads:** the whole head in frame, with empty space above the skull. Never paint over a band that would chop a head.
   - **Eyes:** say "two white eyes" for every figure and prefer a front three-quarter camera.
   - **Faces and clothing:** no mouth, nose or scowl. The hero always wears the shirt. The opponent is never in black or drawn with skin tones.
   - **Framing:** no borders, top strips or bands. Leave headline room, and don't let anyone touch a side edge.
   - **Pose matches the beat:** an "on its way" punch hasn't landed, the hero is in guard, finger counts are correct, and a pad holder shows as a whole person.
5. **Per-still zoom QA.** Check every still at full size against the checklist and redo any failure before the cut.
6. **Build.**
   - Send Sean the silent visual cut first. Narration comes only after he approves the visuals.
   - **Voice:** Ryan Kurk `rU18Fk3uSDhmg5Xh41o4` on eleven_v4, stability 0.50, similarity 0.75. Never speed up the voice; fix timing with pauses only.
   - **Music:** the original lofi bed, about 2 to 3 dB lower than early episodes.
   - **Mix:** about -14 LUFS, with peaks at or under -2 dBTP.
   - **SFX:** only with an approved sound map.
   - **Ending:** end with a subscribe ask.
   - QA everything, then back up to the bot store.
7. **Description.** Include the disclaimer exactly: "Narrated by a licensed narrator. This script was written and researched for factual confirmation. All script work was edited and checked by hand before posting." Add the Skool line saying it's FREE to join, with https://www.skool.com/thefightplaybook. No safety lines.
8. **Upload as a Draft** only when asked. Read the exact video ID from the Studio edit URL.
9. **Thumbnails.** Hand off to the Thumbnail bot. Sean's preferences:
   - A single full-frame action shot with a tight close-up and big eyes.
   - Two words max, in huge text.
   - Wild creative concepts and angles, no logo.
   - He usually wants 9 options, and often combines elements across options.
   - Finals go in `thumb/`.
10. **Set the thumbnail.** Verify by checking that the Studio preview shows the text overlay. A blank draft row in the Content list is normal.
11. **A/B test (Test and compare).**
    - Up to 3 variants, in one of three modes: Title only, Thumbnail only, or Title and thumbnail.
    - Confirm with "Set test", then save the draft.
    - Switching modes deletes the current experiment, which is fine before results exist.
    - Check every slot, and screenshot the pairs before Set test.
    - A draft shows "Ineligible" until it's published. Check the test is running after publish.
12. **Hand Sean** the mp4, the draft ID, the thumbnail screenshot and the A/B pairs screenshot.
