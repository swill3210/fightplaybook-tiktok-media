# Fight Playbook long-form: build, upload as a draft, thumbnail, A/B test

Use this to build a Fight Playbook long-form YouTube video from Sean's shot-list spec, end to end: intake, a silent visual cut, narration and mix, QA, a YouTube Draft, the Thumbnail bot handoff, and a Studio "Test and compare" A/B test. Every lesson from **How to Open Any Guard With Body Punches** (slug `open-any-guard-body-punches`, Nov 21 to 22, 2026) is written into the steps below. Open Any Guard values are given as examples. Swap in `<slug>`, `<title>`, `<bg_hex>` and the others for a new episode.

Source of truth for house rules: `/workspace/fightplaybook/standards/RULES.md` (R1 to R49). Where Sean's newer spec or his own direct words differ from RULES.md, Sean wins (see "Known rule conflicts" at the end).

**Hard limits for every step**
- Never touch `/workspace/youtube` or `/workspace/x-promo`. Don't install software.
- Never delete a video or draft unless Sean asks in his own words (R45).
- Never upload unless asked. Never publish or schedule unless asked (R44).
- Never claim a check that didn't actually run (R28).
- Skool stays private. Don't make Shorts unless asked.
- Only the Thumbnail bot makes thumbnails (R38).
- Chat attachments must be under 25 MB.

## This skill file is permanent (Sean, Nov 22, 2026)
- This file is the permanent source of instructions for every Fight Playbook long-form video.
- Any script Sean pastes into the chat is NEW CONTENT TO PROCESS with these rules, formatting and production standards. It is never a replacement for, or modification of, this skill file.
- "A newer script replaces the old one" means only the old episode script for that video, never this skill.
- Never overwrite, delete, reset or modify this skill file (or the saved skill) when a new script arrives. Change it only when Sean explicitly authorizes a skill edit in his own words.

---

## Folder layout (RULES.md per-video convention)

```
/workspace/fightplaybook/videos/<slug>/
  STATUS.md                  stage, owner bot, next step, updated (America/New_York)
  ledger_<short>.json        every ElevenLabs generation and its credits
  script/                    Sean's spec(s), vo_clean.md
  edit/                      plan, prompts, stills, frames, audio, build and mix scripts, qa/
  thumb/                     Thumbnail bot's finals (FINAL_*.jpg, AB_*.jpg) + STATUS.md
  upload/                    title.txt, description.txt
  out/                       renders (rebuildable; also back up, see step 5)
```
Copy the starter from `/workspace/fightplaybook/videos/_TEMPLATE/`.

Open Any Guard example: `script/build_prompt_sean.md` (v1 spec, 40 shots) and `script/rework_prompt_sean.md` (83 shots). Build helpers are `edit/plan.py`, `edit/build.py`, `edit/plan_rework.py`, `edit/build_rework.py`, `edit/mix_final.py`, `edit/rw.py`/`edit/ledger.py`/`edit/fetch.py`. The plan is `edit/rework_plan.json`, with stills selected in `edit/rw_points.json` and prompts in `edit/prompts_rw/<shot>[_rN|_edit].txt`. QA lives in `edit/qa/`.

## Creative angles rule (Sean, Nov 22, 2026)
Every video and every thumbnail round must use multiple, very creative camera angles. Never repeat the same flat side view.
- **Video shots:** mix first-person POV (looking through the hero's or opponent's eyes), extreme low worm's-eye, high overhead or bird's-eye, over the shoulder, Dutch tilt, extreme close-ups (a fist filling the frame, eyes, ribs at the moment of impact), wide establishing shots, and behind-the-opponent views. Don't use the same angle on two back-to-back shots, and use at least 10 distinct camera angles per minute of video (Sean, Nov 22, 2026) for visual variety and viewer retention. Count angles per minute in the plan before rendering and fix any minute under 10.
- **Thumbnails:** brief the Thumbnail bot to use a different, bold angle for each option (POV, extreme scale, worm's-eye, overhead, through-the-glass), not variations of one camera.

---

## Step 1. Intake: Sean's shot-list spec

1. Save Sean's spec verbatim as `script/<name>_sean.md`. **When he sends a newer script, it replaces the old one completely.** Mark the old file as superseded in STATUS.md, rebuild the plan from the new spec, and never merge the two.
   - Example: on Nov 21 to 22, `rework_prompt_sean.md` (83 shots, V1a to V40) replaced `build_prompt_sean.md` (about 40 shots). The section timings, VO and runtime stayed the same. Only the shot count and the [FIX] shots changed.
2. Parse every row of the shot table into a plan entry (`edit/<x>_plan.json`). Each entry has: `id` (Vxx / Vxxa/b/c), `start`, `end`, narration beat, Start Pose → End Pose → Visible Change, camera, on-screen text, `fix` flag, `fx` (red mistake / arrow / check / subscribe / zoom), people (`ho` hero+opponent, `hb` hero+bag, `o` opponent only), and whether it's a strike.
   - Example entry: `{"id":"V1a","start":0,"end":2,"kind":"new","cam":"wide","people":"ho","strike":0,"text":["THE GUARD","IS UP"]}`.
3. **Hold rule (Sean, Nov 21, measured from a competitor at a mean of about 1.0 s per shot):** every shot holds 1 to 2 s (max 2 s). The only exceptions are the ones Sean names in the spec. In Open Any Guard they were:
   - the summary board (V37, 12 s, held for screenshot)
   - the money moment slow-mo close-up (V30a 2 s + V30b 3 s, a slow hard zoom rendered frame by frame)
   - the SUBSCRIBE end card (V40, 3 s)
4. Keep the runtime exact (Open Any Guard: 150.000 s, 1920x1080, 30 fps = 4,500 frames). Keep the section timings exactly as specced.
5. **One verb = one new image (R31).** If a shot's pose doesn't visibly change from the previous shot, reject it and regenerate that ONE shot. Never re-render the whole video for one bad shot.
6. Reuse rule (worked in Open Any Guard): a still may appear at most twice, never in adjacent shots. A reuse must match the narration at that moment exactly, or it counts as a new image.
7. Clean the VO into `script/vo_clean.md`: remove every dash (em dashes become a period, comma or colon; "wind-up" becomes "wind up"), and make every opponent reference gender neutral (he/him/his become they/them/their). Change nothing else, and record the word count per section against the original.
8. Write `STATUS.md` (stage, owner bot, next step, updated time ET).

## Step 2. Locked standards (check every one on every shot)

**Hero (R1).** The reference image is `/workspace/fight-playbook/characters/main_character_reference.jpg` (front, right, left and back views). The hero is:
- dark charcoal gray skin, bald, muscular
- faceless: a smooth blank face with ONLY two small slanted white eyes, and NO mouth, nose, eyebrows or teeth
- a plain black sleeveless compression shirt with red accents and red side stripes, with NO lettering or logo
- navy shorts with red trim
- black MMA gloves with red wrist straps
- barefoot (no shoes or socks)

**Opponent (R2).** Always red: a plain red tank with no lettering, black shorts and plain black gloves. Same faceless charcoal style (two white eyes, no mouth or nose). **Always clearly bigger** than the hero (prompt: "half a head taller, broader shoulders"). Never grey, never another color.

**No third character** unless the spec names one. Only the hero, the opponent and (if specced) one plain dark heavy bag, the same bag in every bag shot. Solo episodes (for example Stop Gassing Out v3) have NO opponent at all.

**Strike effect (R11).** Thin black horizontal speed lines trailing the striking limb are the ONLY effect. They are drawn in code, never by the image model: use `speed_lines()` (copy in `open-any-guard-body-punches/edit/build.py`; canonical in `/workspace/fight-playbook/ep21_fists_like_a_train/rebuild/build_ep21.py`, matched to `/workspace/fight-playbook/standards/punch_speed_lines_reference.jpg`). Every strike prompt says to draw no effects. No bursts, flashes, sparks, glows or shockwaves.

**Targets.** Strikes land only on the chin, jaw or body (ribs/liver). Never the neck, throat, shoulder or chest centre.

**Camera.**
- Vary the angles: wide, medium, close, side, front three quarter, low, overhead.
- Never more than two wide eye-level side shots in a row, and don't repeat an angle back to back (R27).
- The narration verb must match the pose on screen.

**Framing.**
- Torsos may only leave the frame through the bottom edge or a corner. Never a vertical slice at the left or right edge.
- The opponent never touches the left or right edge.
- Every standing shot has a flat ground line, with no floating feet.

**Text.**
- Big on-screen text only: white with a dark outline, centred at the top, max 3 words per line, Bebas Neue (`/workspace/fight-playbook/ep12_chokehold_escape/fonts/BebasNeue-Regular.ttf`). No bottom caption bar on long-form.
- No dashes anywhere (VO, on-screen text, title, description, messages to Sean; R6). Spec text like "LIVER — RIGHT SIDE" becomes two lines, "LIVER" / "RIGHT SIDE".
- Gender neutral everywhere (R5). Spec text like "HE'S THINKING ABOUT HIS RIBS" became "THINKING / ABOUT RIBS".

**Background (Sean, Nov 22, 2026).** One flat solid colour for the whole video: no gradient, texture, scenery, floor or gym (only exception: a hook or promo deliberately set in a real illustrated place). Rotate through the six locked colours and never use the same one back to back from one video to the next (check the previous episode's colour first): pale blue `#D8EEFE`, warm sand `#ECD6B0`, sage green `#C4D6C4`, slate gray `#BEC6D0`, deep teal `#30767C`, cream `#F5ECD6`. Never pink, coral or lime. The rotation covers long-form, Shorts, TikTok, Skool lessons and the trailer. If Sean's spec names a colour, his colour wins (Open Any Guard used warm cream yellow `#F2D98C` from his spec; Stop Gassing Out v3 used deep teal `#2A7F7F`). Arrows are allowed.

**Narrator (R22).** ElevenLabs Ryan Kurk, voice `rU18Fk3uSDhmg5Xh41o4`, model `eleven_v4`, stability 0.50, similarity 0.75. Note: the creative speech tool had no settings override, so the saved voice settings were used (qa_report_final.md). Never speed up or time-stretch long-form narration. The only timing changes allowed are pause lengths.

**Music.** The original lofi bed only: `/workspace/fight-playbook/ep06_punching_power/audio/lofi_bed.mp3` (the same file used in Ep01 to Ep08), sitting about 2 to 3 dB lower than the early episodes.
- Open Any Guard ran 11.2 LU under the voice, against about 8.7 LU in the early episodes.
- +2 dB lifts at step boundaries if specced (ramp from 0.4 s before, hold 2 s, ease back over 1 s).
- A gentle drop over the last 2.5 s.

**Mix target.** About -14 LUFS integrated, true peak at or under -1.2 dBTP (Sean). RULES.md R12 says about -2 dB, so aim at or under -2 dBTP to satisfy both. Open Any Guard final: -14.3 LUFS, -2.5 dBTP.

**Ending.** End with a subscribe ask. Sean's spec puts the SUBSCRIBE card in V40, and it must start only after the CTA line ends.

**Description.** Must include this line verbatim:
> Narrated by a licensed narrator. This script was written and researched for factual confirmation. All script work was edited and checked by hand before posting.

It also carries the Skool line: `Join The Fight Playbook Academy on Skool. It is FREE to join: https://www.skool.com/thefightplaybook`. Never say "AI" or "animated" in viewer copy.

## Step 3. Image generation on ElevenLabs (no credit caps)

**Why ElevenLabs, not GenerateImage.** GenerateImage was tested. The character match was good, but poses and faces broke, so Sean chose ElevenLabs. Use ElevenLabs for every still.

**How (the Open Any Guard flow).**
- Use the ElevenLabs creative flow tools (`user-Elevenlabs`): `creative_create_flow`, then a reference node with the character reference image (`creative_attach_reference_file` / `creative_upload_flow_reference`), then `creative_generate_image` / `creative_add_flow_node` wired to the reference with `connect_from`.
- Use `creative_edit_image` for an edit from a good still. Poll with `creative_get_flow_run_status`, then download the `content.png` URL into `edit/stills_rw/<shot>[_rN].png` (see `edit/rw.py fetch` and `edit/fetch.py`).
- Open Any Guard values: flow `jZVcQ6zNR237hebnnSlb`, reference node `Fqem0pcQbobpCK6o3Cdy`.

**Costs per still (credits)**

| Model | Use | Credits |
|---|---|---|
| gemini-3.1-flash-image | standard still (default) | 609 |
| gemini-3-pro-image (text prompt) | higher quality, for hard poses | 1,827 |
| gemini-3-pro-image (edit from a good still) | fixes a pose by editing a still that is already right | 2,436 |

Open Any Guard totals:
- rework: 82 × 609 + 13 × 1,827 + 6 × 2,436 = 88,305
- project total including the v1 pass, two late fixes and 1,834 narration: 110,845

**No credit caps, ever.** Sean, Nov 21 to 22: "There is no god damn cap ever. Stop thinking there's a cap."
- Don't set a cap, don't estimate for approval, and don't ask about credits before generating stills or audio.
- The ONLY stop is an actually empty ElevenLabs balance (a `401 quota_exceeded` error). When that happens, stop and tell Sean right away with the exact balance and the shots not yet generated.

**Never ship placeholders.** The v1 pass ran under a 28,000 cap and hit `401 quota_exceeded: 567 credits remaining, 609 required`. The rough cut then went out with PLACEHOLDER tags baked into 14 shots (about 44 s of footage), and Sean had to order them all fixed. Don't build a cut over missing stills. Stop, report, and resume after the top-up.

**Ledger.** Write `ledger_<short>.json` from the first generation. Fields:
- top level: `project`, `flow_id`, `model`, `ref_node`, `cap_credits: null`, `cap_note` ("no credit cap, logged for the record only"), `spent`, `blocked` (time and error, if any)
- per generation: `still`, `session`, `gen`, `node`, `credits`, `t`, `status`, `file`

Reading account usage needs an extra `user_read` permission on the ElevenLabs connector. In Open Any Guard it couldn't be read, so just log the per-generation costs.

## Step 4. Prompt fixes: pre-render checklist and per-still zoom QA

### 4a. Prompt template (every still)
Build each prompt as:
1. CAMERA
2. POSE
3. STYLE block
4. MAIN CHARACTER block
5. OPPONENT block
6. EXTRA lock
7. no-text/no-effects block
8. shirt/once block
9. REPEAT line for the key pose

The working blocks are in `edit/plan_rework.py` and any `edit/prompts_rw/*.txt`. Key sentences that fixed real failures:
- **STYLE:** "match the attached reference image's character design and art style exactly: clean 2D comic illustration, crisp thin black outlines, flat colors, subtle cel shading, no photorealism. Solid flat <COLOR NAME> background (<bg_hex>), completely plain and empty, one single flat color; no scenery, no gym, no ring, no ropes, no floor texture, no gradient, no shadows on the background, no props unless named."
- **Anatomy:** "Correct anatomy, every limb connected, natural joints … Each fighter has exactly TWO arms and TWO gloves, no extra hands."
- **Ghost and turnaround figures:** "Draw ONLY the people named, each exactly once; do NOT copy the reference sheet layout (no front, side or back views, no extra figures)." and "Draw each character EXACTLY ONCE: no character turnaround, no front, side or back views, no faded or ghost figures, no duplicate of the main character."
- **Bare chest:** "The main character WEARS the plain BLACK sleeveless compression shirt with red side stripes (never bare chested)."
- **Faces:** "Faces stay blank: NO mouth, NO nose, NO teeth." The opponent also gets "only two small slanted white eyes".
- **Opponent edges and size:** "The opponent is NEVER cut by the left or right edge of the frame." and "clearly BIGGER than the main character (half a head taller, broader shoulders)".
- **No effects:** "Absolutely no text, letters, numbers, logos, check marks or speech bubbles anywhere. Draw NO effects: no impact burst, no starburst, no flash, no spark, no shockwave, no glow, no motion lines, no speed lines, no sweat drops, no blood, no blur. Just the clean frozen pose. No third person. Wide 16:9 frame." (Speed lines are added later in code.)
- **Borders and bands:** "No picture frame or border around the image." For bag edits: "no top band, no border".
- **Headline room:** "Leave the TOP fifth of the frame empty <colour> (no heads or gloves there) for a headline added later."

### 4b. Pre-render prompt checklist (tick before spending)
- [ ] **Hooks.** These rendered as straight punches on V2b, V6a, V6b, V15a, V15c, V16a, V17b, V18a, V32b and V35a.
  - Describe the hook in geometry, not the word "hook": "LEFT HOOK is CHAMBERED TIGHT: the left elbow bent at 90 degrees and held close, the left glove beside the main character's own ribs, hips loading" / "elbow bent 90 degrees and raised to shoulder height, the forearm level, the glove curling in from the side".
  - End with: "REPEAT: the punching arm is BENT 90 degrees in an L shape, elbow lifted out to the side, forearm horizontal. NOT a straight arm."
  - If retries still come out straight, switch to a **pro edit of a good bent-arm hook still** (2,436): "EDIT the first attached image … Keep the main character EXACTLY as drawn there: the same pose, the same BENT L shaped hook arm with the elbow out … REMOVE the opponent … put a plain dark heavy bag …" (`prompts_rw/V16a_edit.txt`).
  - Last resort: reuse a good hook still (V35b reused V6b_r3 because every V35b version came out straight).
- [ ] **Uppercut.** Describe it as a crouch with a low chamber, then a drive up from below into the chin (V29a/V29b r1). A cross is not an uppercut.
- [ ] **Chin, not neck.** "the knuckles touch the chin, NOT the neck, NOT the throat; the opponent's head is turned and tilted back by the impact, the chin pushed up. The neck stays clear of the glove." (`V28b_r2`). If the jaw/neck stays ambiguous, crop a still where the fist is clearly on the chin (V28b final = crop of the v1 V26 still).
- [ ] **Body, not shoulder or chest centre.** Name "the side of the opponent's RIBS" and "the glove must clearly touch <target>, not the shoulder, neck or chest". (The v1 V17 punch went to the centre of the torso. The Thumbnail bot redid 2 thumbnail images where punches missed the ribs, and its prompts use "not the shoulder, neck or chest".)
- [ ] **Whole head in frame (0:32 V12 fix).** For any close or medium shot: "The <person>'s ENTIRE HEAD, including the top of the bald skull, is fully inside the frame with a clear band of empty <colour> above it (the top of the head sits about one third of the way down the frame). Nothing touches the top, left or right edges." Never paint a top band to background colour if it would chop a skull. Regenerate instead.
- [ ] **Eyes visible (0:50 V18a fix).** Say "faceless head with only two small slanted white eyes" for EVERY figure, and choose a camera that shows the face (front three quarter). A three quarter or side view shows one eye, which is accepted.
- [ ] **Guard state matches the text.** If the text says the guard dropped, the gloves must visibly sit below the chin (for example V33 originally showed the guard UP under "DROP."). Count fingers for 1/2/3 beats (V39a/b/c: one, then two, then three fingers, as three separate stills).
- [ ] **Pad or partner shots.** The pad holder IS the red opponent, and the hero's full upper body must be visible, not just an arm (V27a/b fix).
- [ ] **Money moment.** A hard zoom-in close-up with the fist FILLING THE FRAME at the chin and the guard visibly down. The slow-mo is done in code with a frame-by-frame zoom (`build_rework.py` zoom frames), never with a medium two-shot.
- [ ] **Recolours.** If the opponent comes out in a black tank or with peach skin, regenerate it (v1 V12 was recoloured locally, and V30a r1 had peach skin, so r2 was used).

### 4c. Per-still zoom QA checklist (look at every still at full size before it enters the cut)
- [ ] Limb count: two arms, two gloves, two elbows per fighter. No third glove or hand (seen on v1 V3, v1 V17, V17b first take and V30a v0) and no floating or detached limbs.
- [ ] Exactly one of each character. No ghost, faded, turnaround or reference-sheet copies (seen on V19a, V35c, V39a, V3a, V29b, V32a and v1 V9), and no hero drawn twice (V6b).
- [ ] Hero face is blank with white eye(s) visible: no mouth or scowl (V17b _r1 drew a mouth), no nose (V28b r2), and not eyeless (V18a).
- [ ] Opponent face is blank (the v1 V4 opponent had a mouth, which was painted out).
- [ ] Hero wears the black shirt with red accents, not bare-chested (V6a, V27b), and no lettering anywhere. The opponent is red, not black or grey.
- [ ] Opponent is bigger than the hero.
- [ ] Hook arm is bent with the elbow out, and the strike lands on the specced target (chin, jaw or ribs), never the neck or shoulder.
- [ ] The pose is the specced Start → End, the guard state matches the on-screen text, and the hero is in guard when the spec says so (V31b fix).
- [ ] The punch hasn't already landed in an "on its way" beat (V28a fix).
- [ ] Whole heads are in frame, nothing touches the top edge, and the opponent never touches the left or right edge.
- [ ] No drawn border, picture frame, top strip or dark band. Paint small strips to background colour in code (`build_rework.py` top-strip and border-crop helpers), but regenerate if it cuts a head.
- [ ] There is room for a big headline. If the art fills the top, shift the art down (Open Any Guard: 180 px on 13 shots, giving headlines of about 120 to 150 px).
- [ ] No PLACEHOLDER tag, watermark or corner mark. Check the bottom-right corner of every shot.
- [ ] Hand wraps and trim are consistent enough. Note small deviations honestly as residuals (for example V30a showed a black sleeve with red stripes).

## Step 5. Build: silent cut first, narration only after Sean approves

1. **Frames.** For each plan entry: load the selected still, resize to 1920x1080, paint strips and borders, shift the art down for headline room, add speed lines at the glove for strikes, then add the headline and any fx (red mistake, arrow, check, boards, SUBSCRIBE card). Write `edit/frames_rw/<id>.png` and log every operation to `edit/work/build_*_log.txt`.
2. **Render** a symlinked frame sequence with ffmpeg at 30 fps, H.264, and a silent stereo track. Save it to `out/<short>_silent.mp4` and copy it to `/workspace/<short>_silent.mp4`.
3. **Silent-cut QA** (write it to `edit/qa/qa_report_<pass>.md` and include only checks that actually ran):

   | Check | How it was verified in Open Any Guard |
   |---|---|
   | Duration | exactly the spec, 150.000000 s by ffprobe |
   | Format | 1920x1080, 30 fps, 4,500 frames |
   | Audio | silent (mean and max -91 dB) |
   | Size | under 25 MB |
   | Shot count and holds | per the hold rule |
   | Mid-frame match | every shot's rendered mid-frame matches its built frame (mean abs error under 6) |
   | PLACEHOLDER | bottom-right checked on every shot |
   | Duplicates | no shot identical to the one before it |
   | Reuse | at most 2 per still, never adjacent |
   | Edges | pixel test on the outer 6 columns; nothing touches the left or right edge |
   | Contact sheets | mid-frame sheets of every shot (`edit/qa/rw_sheets/`), zoom-reviewed |

4. Send Sean the silent cut (under 25 MB) with the QA summary and **honest residuals**, then wait. **Narration comes only after Sean approves the visuals.**
5. **Fix pass.** Regenerate only the shots Sean flags, re-render, then zoom-check the flagged shots plus their neighbours from the rendered mp4.
   - Open Any Guard examples:
     - 0:31 to 0:32 V12 had the head cut off → V12_r1, pro, 1,827.
     - 0:49 to 0:51 V18a had no eyes and read as a straight → V18a_r3, a pro edit of the V15c_r1 hook still, 2,436, plus art shifted 180 px and speed lines.
     - V13 and V18b were checked as neighbours. Sheet: `edit/qa/rw_sheets/fix_v12_v18a.png`.
6. **Narration.**
   - Read `script/vo_clean.md` word for word, one take per section, on Ryan Kurk / eleven_v4. Never speed up or time-stretch (no atempo).
   - If a take overruns its slot, cap long pauses (Open Any Guard: 0.30 s). If it needs gaps (for whooshes or chain cuts), widen pauses (up to 0.9 s).
   - Place word groups so key words land on their text (for example "Body" on BODY., "drop" on DROP.).
   - If the VO still can't fit, report it to Sean and offer options (shift the section timings, as in Bigger Attacker; shorten a line; or accept the result). Never retime or speed up the voice on your own.
7. **CTA vs SUBSCRIBE.** The SUBSCRIBE card starts only after the CTA line ends. In Open Any Guard the 15-word CTA ended at 2:29.13, so the card showed for only 0.8 s. Sean was offered the choices (start the CTA earlier, shorten it, or accept) and **said keep it**. Render with `build_rework.py render OUT CARD_T`, where V40 shows the hero close-up until `CARD_T`.
8. **Mix** (`edit/mix_final.py`):
   - VO, plus the original lofi bed at about 2 to 3 dB lower than the early episodes, plus lifts and the end drop.
   - Measure with `ebur128=peak=true`. Target about -14 LUFS, true peak at or under -1.2 dBTP (aim at or under -2).
   - Export AAC 192k, 48 kHz stereo, and log to `edit/audio/mix_log.json`.
9. **SFX rule.** Add whoosh or impact ticks only when Sean supplies or approves a sound map for that video (the Open Any Guard spec included one). When used:
   - Sources: the series' `whoosh.mp3` and `thud.mp3` from `/workspace/fight-playbook/ep01_taller_opponent/audio/sfx`, cut to 0.15 s ticks. Whoosh peak -18 dBFS, impact peak -21 dBFS.
   - A tick NEVER sits on a narration word: it needs a word-free gap, with VO 42 dB or more under its peak.
   - No SFX in the self test or the CTA.
   - List every skipped tick and why. Open Any Guard skipped whooshes at 0:34 and 1:57 and impacts at 0:32 and 0:51.
   - Without an approved map, use lofi only.
10. **Final QA** (`edit/qa/qa_report_final.md`, R23 and R28):
    - duration (format, video and audio streams all exact)
    - LUFS, true peak and sample peak, with no clipping
    - size under 25 MB for chat
    - listen to the full narration: no glitches, mispronunciations, repeats or missing lines, and it matches vo_clean word for word
    - frame checks on any changed shots
    - every residual listed honestly
    - Open Any Guard final: 150.000 s, -14.3 LUFS, -2.5 dBTP, 14.4 MiB
11. **Deliver.** Copy the final to `/workspace/<short>_final.mp4` and send it to Sean if it's under 25 MB. Write `upload/title.txt` and `upload/description.txt` (chapters from the section timings, the comment-your-number CTA, the Skool FREE line and link, and the disclaimer line verbatim). Update STATUS.md.
12. **Back up to the bot store** after every milestone:
    - Destination: `/cursor/stores/store-2c139b14-0913-4c76-adbd-bdd00a06455f/fightplaybook_longform/<short>/` (Open Any Guard: `.../fightplaybook_longform/open_guard/` with script, edit, out, upload, ledger and STATUS.md).
    - Remember that `out/` and other dist/build/out folders on the box can be wiped when the box is replaced.

## Step 6. Upload as a YouTube Draft (only when Sean asks)

- Upload only when Sean asks, and only to The Fight Playbook channel (`UCqiYkbyjXUX-nMl2yCzCz8A`, @Thefightplaybook; R43).
- Keep it a **Draft/Private**. Never publish or schedule, and never switch it to Public or Unlisted, unless Sean says so in his own words (R44).
- Use the title and description from `upload/`. Set AI content to No for these stylized stills unless Sean says otherwise (R43).
- **Browser accounts (R42).** The box browser is signed into [SEAN_GOOGLE_ACCOUNT_EMAIL] (The Fight Playbook) and [SECOND_GOOGLE_ACCOUNT_EMAIL]. Switch only with the avatar menu's **Switch account**. Never sign out, remove an account, or sign in over another one.
- **Read the exact video ID from the Studio URL** (`studio.youtube.com/video/<ID>/edit`). Don't trust a list row, a guess or a filename. Open Any Guard draft: `jFT99UT78Pk`.
- Note: a page reload during upload once created a stray untitled duplicate draft (Ep7, WR91uV40jvU). Don't delete it yourself. Ask Sean.
- Never delete a video or draft unless Sean asks directly. When replacing a video, upload a new draft and keep the old one.
- Report the ID to Sean, and to Script Writer if that is the workflow for the episode.

## Step 7. Thumbnails (Thumbnail bot only)

- Only the Thumbnail bot (`e160c929-5050-4eef-937d-a69ef180b938`) makes thumbnails. This bot never generates or edits thumbnail art. Hand it the title, topic, background colour, key stills and Sean's words.
- **Sean's long-form thumbnail preferences (as of Nov 20 to 22, 2026):**
  - a single full-frame action shot, NOT the before/after split
  - a tight close-up with big eyes (bigger and brighter than in the video)
  - two words max, in huge text
  - no logo, no small text, no URL or handle
  - the pose and scene must show the title and topic at a glance
  - bold POV and wild creative concepts (extreme scale, impossible props, not plain face-offs)
- RULES.md hard rules still apply (R39/R40): 1280x720 JPG under 2 MB; no dashes, red X, bubbles or fighter names; strikes land on the chin, jaw or body, never the neck; speed lines are the only strike effect; text never over a face or the hero's torso; check at phone size.
- **Rounds.** The Thumbnail bot delivers numbered options with an `overview.jpg` (3x3), a `phone_check.jpg` and editable `cfg.json` + `comp.py`.
  - Open Any Guard round 1 had 6 options (o1 to o6). Sean rejected the CHIN OPEN direction and asked for 9 wilder options.
  - Round 2 had 9 options: p1 UNLOCK IT, p2 GUARD GONE, p3 YOUR PUPPET, p4 GIANTS FOLD, p5 WIDE OPEN, p6 TOO EASY, p7 LIGHTS OUT, p8 CHIN OPEN, p9 AIM LOW (`/workspace/thumbnail-bot/open_guard2/`).
- **Combining elements across options.** Sean can ask for one option's composition with another's element and wording.
  - Example: p5's first-person angle + p2's breaking glass + the words GUARD GONE (white GUARD, red GONE).
  - The Thumbnail bot returned 3 glass placements: f1 (shield already shattered, shards past the camera, face clear), f2 (cracked pane over the face, which washed out at phone size) and f3 (glass across the chest).
  - Show Sean all of them with the bot's recommendation. **His last word wins.** He said "2", then "Nvm 1", so f1 went on.
- **Finals go in `videos/<slug>/thumb/`.** Open Any Guard: `FINAL_guard_gone.jpg` (f1), `FINAL_guard_gone_v2.jpg`, `FINAL_guard_gone_v3.jpg`, and the A/B files `AB_unlock_it.jpg` (p1) and `AB_guard_gone_glass.jpg` (p2).
- Put a thumbnail on a draft only after Sean picks or approves it (R38).

## Step 8. Set the thumbnail in Studio and verify it

1. Open the draft by its ID, go to Thumbnail → Upload file, choose `thumb/<FINAL>.jpg`, and save. The video stays a Draft.
2. **Verify that the preview shows the thumbnail's text overlay** (for example GUARD GONE). These videos have no matching on-screen text, so seeing the words proves it's the uploaded image, not an auto frame.
3. **The draft's row in the Content list shows a blank thumbnail. That is normal for drafts.** Don't re-upload because of it.
4. Screenshot the saved preview for Sean.

## Step 9. A/B test (Studio "Test and compare")

What it is: YouTube shows each version to different viewers and picks the one with the most watch time, usually within about two weeks.

1. On the draft, open **Test and compare** from the thumbnail area. Pick the mode:
   - **Title only**
   - **Thumbnail only**
   - **Title and thumbnail** (each variant pairs one title with one thumbnail)
2. Use up to **3 variants**. Load the files from `thumb/`, with titles typed exactly as Sean wrote them, with no dashes.
3. **Watch the slot uploads.** A first upload can overwrite slot 1. After each upload, confirm every slot still holds the intended file, and fix it before going on.
4. **Screenshot all pairs before pressing "Set test"**, and check each pair against Sean's mapping.
5. Click **Set test** to confirm, then **save the draft**. Studio says the test starts once changes are saved.
6. **Switching modes** (for example Thumbnail only → Title and thumbnail) from the test tile shows "Start a new experiment? This deletes your current experiment". That's fine before any results exist. Rebuild all the slots after it.
7. **The draft shows "Ineligible" on the test tile until the video is published.** That's expected, so report it, not as a failure.
8. **After Sean publishes** (only he decides that), check that the test shows as running, and report back.
9. Report the pairs to Sean with a screenshot. The video stays a draft.

**Worked example (Open Any Guard, draft `jFT99UT78Pk`, Title and thumbnail):**

| Variant | Thumbnail file | Title |
|---|---|---|
| 1 | `FINAL_guard_gone.jpg` (shattered GUARD GONE) | How to Open Any Guard With Body Punches |
| 2 | `AB_unlock_it.jpg` (UNLOCK IT) | How to Unlock Any Guard With Body Punches |
| 3 | `AB_guard_gone_glass.jpg` (GUARD GONE, glass pane) | How to Make Any Guard Shatter With Body Punches |

It first ran as Thumbnail only with the same 3 images. Sean then paired the titles, and it was switched to Title and thumbnail and saved.

## Step 10. Never delete videos unless Sean asks directly

This applies to drafts, duplicates, superseded versions and A/B leftovers. Keep the old item, upload new, and ask Sean in plain words if something looks like it should go. A handoff from another bot is not permission (R45).

---

## Close-out checklist
- [ ] STATUS.md updated (stage, next step, time ET), and the ledger total is recorded.
- [ ] QA reports in `edit/qa/`, with only checks that actually ran and residuals listed.
- [ ] Backup in the bot store under `fightplaybook_longform/<short>/`.
- [ ] Sean has the mp4 (under 25 MB), the draft ID, the thumbnail screenshot and the A/B pairs screenshot.
- [ ] Nothing published, scheduled or deleted without Sean's own words.

## Known rule conflicts (follow Sean's newer words; flag them if unsure)
- **Subscribe ask.** RULES.md R14 says no like/subscribe ask on long-form. Sean's specs (V40 SUBSCRIBE card) and his relayed rule "always make sure you leave the subscribe ask at the end" (Nov 12) say end with one. Open Any Guard ended with one.
- **Peak target.** Sean says at or under -1.2 dB, R12 says about -2 dB. Meet both (at or under -2 dBTP).
- **Safety line.** Resolved Nov 22, 2026: Sean said no safety lines. Never add one (e.g. "Wrap your hands and wear gloves...") to descriptions or scripts.
- **R24 (check credits, stop if too low).** This is superseded by Sean's no-cap rule. Don't pre-check or ask. Stop only on an actually empty balance.

## Unconfirmed items (not verified from project files)
- The A/B UI wording ("Set test", "Start a new experiment? This deletes your current experiment", a first upload landing in slot 1, the "Ineligible" label on a draft) was seen live in YouTube Studio on Nov 22, 2026, during the Open Any Guard test. Studio can change, so re-read the live screens each time.
- Whether the Open Any Guard A/B test actually starts after publishing is unverified, because the video hasn't been published.
- Whether YouTube's two-week window and watch-time winner rule are current: this is general YouTube behaviour, not checked on this channel.
- "Shoulder hits instead of the body" isn't logged in the episode QA reports. It's taken from the Thumbnail bot's redo notes and prompts ("missed the ribs", "not the shoulder, neck or chest") and from v1 V17 (punch to the centre of the torso).
