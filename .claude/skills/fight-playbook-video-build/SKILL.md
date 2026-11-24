---
name: fight-playbook-video-build
description: Build a Fight Playbook video silently first while holding the faceless character lock, the background rotation, the script timings, an early payoff and a pose match for every action verb. Old box paths are mapped in PATHS.md.
---
# Fight Playbook Video Build

## Source of truth: Sean's YouTube bot skill

- The permanent source of instructions for every Fight Playbook long-form video is `workspace/user/files/Fight_Playbook_Longform_Skill_2.md`. Follow it. Where it conflicts with this file, the bot skill wins. Never modify that file.
- Key rules from it (Nov 22, 2026): six background colors (pale blue #D8EEFE, warm sand #ECD6B0, sage green #C4D6C4, slate gray #BEC6D0, deep teal #30767C, cream #F5ECD6), never the same back to back; at least 10 distinct camera angles per minute, never the same angle twice in a row; no dashes anywhere including messages to Sean; gender neutral everywhere; hero in navy shorts with red trim and barefoot; opponent always red and clearly bigger; no bottom caption bar on long-form; big text white with dark outline, top centre, max 3 words, Bebas Neue; strikes only on chin, jaw, body; speed lines are the only strike effect and are added in code, never in image prompts; no safety lines ever; end with the subscribe ask; description carries the verbatim narrator disclaimer line and the Skool line and never says AI or animated; no ElevenLabs credit caps ever, stop only on an actually empty balance.

## Lock the character before you generate anything

- Open the reference image at workspace/user/files/EFE2594C-7995-4D65-A95F-14323AB41B61-photo-DB2BD1FE-31DE-4208-B7F4-7A2F2A1EE603.jpg and read the face again before you generate a still.

- Keep the face completely smooth and blank with only two slanted white eyes and no mouth, no nose, no eyebrows and no other facial features.

- Keep the black sleeveless shirt free of lettering and keep the black MMA gloves with red wrist straps.

- Keep the opponent in red and keep hands bare only in the grip tutorial so the equipment stays visible.

- Put the character lock in every image prompt in full words rather than relying on a short phrase such as faceless.

- Choose a background from Pale Blue, Warm Sand Beige, Deep Teal and Warm Cream Yellow and do not repeat the background used in the previous video.

## Match every still to the action it shows

- Give each action verb its own image and never reuse one image for a whole step.

- State the start pose and the end pose and the visible change for each image before you generate it.

- Check that the pose in the image does what the narration says at that moment.

- Reject an image that is identical to the previous image except for text or zoom and regenerate that shot only.

- Fix only the failed shots and do not rebuild the whole video when one pose is wrong.

- Do not use a legs only still for a kick and do not use a side angle for a move described as forward.

- Vary the camera angles and never use more than two wide eye level side shots in a row.

- Show every punch landing on its target in a contact shot, with the glove touching the target and the target compressing at the point of contact.

- Show uppercuts from below with the knuckles buried in the lower half of the target and the target compressing upward.

- Make the money moment a slow motion hard zoom in close up on the contact.

## Anchor every body and crop every shot cleanly

- Draw a flat ground line under the feet in every standing shot and keep the feet on that line.

- Never deliver a floating body, a floating arm, a floating hand or floating fingers.

- Attach every close up hand to a visible wrist and forearm and attach that forearm to a visible torso.

- Never crop through a thigh or a torso or a forearm and never leave fingers without a palm.

- Cut a torso only when the cut blends into a corner or the bottom of the screen.

- Never cut a torso with a vertical slice through the chest at the left or right edge mid-frame.

## Build silent first and match the script timings

- Build the video silent first and add narration only after Sean reviews the visuals and approves it.

- Do not connect ElevenLabs or spend narration credits while the silent build is still in review.

- Count the script words yourself and budget about 0.39 seconds per word at the calm coach pace before you promise a runtime.

- Compare the delivered cut timings with the script timings section by section before you present the cut as finished.

- Ask Sean which timing to keep when the cut and the script disagree instead of silently shipping the mismatch.

- Keep the average hold near 1 second and keep no still on screen for more than 2 seconds except the summary board and the money moment.

- Vary the step structure to fit the topic instead of repeating the same nine beats in the same order for every step and every video.

- Put the self test at 0:17 and put the full chain at speed by 0:32 in a long form rebuild that targets 70 percent viewed.

- Keep each step to about 25 seconds in that rebuild shape and show doses as short overlays of about 3 seconds each instead of full dose cards.

- Put the first drill and the self test early in the video and keep one mantra for the whole video.

- Leave out unsourced overclaims about blindness, knockouts or timing unless Sean supplies a source for the claim.

- End with a concrete spoken call to action that asks viewers to answer with 1, 2 or 3.

- Start SUBSCRIBE only after the last narration word and hold it for at least 3 seconds.

## Check every still before you deliver it

- Inspect each generated still against the reference image for face, shirt lettering, gloves and background before you assemble the cut.

- Inspect each still for pose match as well as character lock and do not deliver a still that fails either check.

- Count the arms and legs on every character in every still and regenerate a still with an extra limb or a missing limb.

- Reject any still that carries a PLACEHOLDER label or watermark and regenerate that shot only.

- Hash check stills for reuse and reject a still that is pixel identical to a still used in another section.

- Regenerate a still that adds a mouth, a nose, eyebrows, shirt lettering or a different character and do not deliver it for review.

- Keep the bottom caption bar on Shorts and sync it to the narration so the words match the spoken word at the same moment.

- Transcribe the finished audio twice before you call any file ready and confirm every script word is present in order at natural pace.

- Call a file silent when it has no spoken narration and never call a silent file ready to publish.

- Retime the visuals to the voiceover real durations when the voiceover overruns a section and never speed up the voice.

- Report the overrun per section and stop before mixing when the timing does not fit.

- Confirm whether a Short loops before you judge its ending as cut off.

- State whether you watched the video file frame by frame or read its chapters only when you report a review.

- Deliver a short review cut first when Sean asks for one and name the exact time range it covers.

- Report what you checked, what passed and what still needs a decision rather than claiming the character is fixed without inspecting it.

## Available connectors

- Use `muse.connector_search` to find other connectors and `muse.skill_search` to find related skills.

- If nothing here fits, look on the web for a maintained API or MCP server and set it up with [Custom Connectors and MCPs](/opt/muse/skills/custom-connector-setup/SKILL.md), or build a custom connector.

## Alternatives for better results

- Check the channel analytics with the social content performance skill before you choose a new structure so the change answers the actual retention drop.

- Start from the competitor patterns in workspace/your_files/fight-playbook-competitor-analysis-2026-11-21.md and frame each topic as an outcome with a counterintuitive twist.

- Name the strategy for each video and keep it with the script so Sean can compare what worked across videos.

- Offer the next small review step and wait for Sean at his decision points instead of pushing narration or automation ahead of his review.
