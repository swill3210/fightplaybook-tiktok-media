# Reverse-Engineering: @viet_vet_nam ("Grunt's Field Notes")

**Data date:** 2026-11-25 · **Source:** vidIQ (live YouTube data) · **Credits used:** 110
**What I ran:**
- channel stats (daily history), plus top and recent long-form uploads (52 videos)
- thumbnails for 20 videos plus the avatar (viewed directly)
- full **video watch** of 3 videos:
  - [#1 hit](https://www.youtube.com/watch?v=YWZVQOW1Wqk), 773K views
  - [high-comment hit](https://www.youtube.com/watch?v=nLFbzcEive4), 104K views
  - [recent flop](https://www.youtube.com/watch?v=hAVRrzYwGUc), 135 views
- full transcript of the #1 hit
- daily view history and an earnings estimate for the #1 hit
- the top 40 comment threads on the #1 hit

Labels used throughout:
- **[V] Verified** — straight from vidIQ/YouTube data or from what I saw in the images.
- **[W] Watch-tool report** — vidIQ's AI viewing of the video. Strong evidence, but it can misidentify things.
- **[A] Assumption** — my inference. Treat it as a hypothesis.

---

## 0. The most important finding: the formula worked for about 2 weeks, then stalled

| Date | Channel total views [V] | Notes |
|---|---|---|
| 2026-09-24 | 0 | First upload. The channel was **created 2022-07-18** and sat unused, so it's a repurposed channel [V]. Country: **UA** [V] |
| 2026-10-05 | 786K | One video passed 300K in 4 days |
| 2026-10-13 | 1.89M | ~77% of lifetime views arrived in the first 3 weeks |
| 2026-11-24 | 2.45M | Now gaining **~1–2K views/day** across the whole channel |

- The #1 video peaked at **~7,100 views/hour on Oct 4–5**. It's now under 5 views/hour [V].
- **Every one of the top 9 videos was published between Sep 24 and Oct 12** [V]. Everything after Oct 13 is under 18K views. The last 10 uploads got **135 to 1,587 views** [V].
- **The drop isn't a quality problem.** The watch tool rated the recent flop as well researched, with documented legal sources, no AI artifacts and no templated filler [W].
- **The drop isn't (only) the thumbnail style either.** Uploads from Nov 11–13 still used the old no-text style and got 173–506 views [V].

**Most likely causes [A]:**
1. A burst of browse/suggested traffic in the first weeks that the channel couldn't sustain. **Uploading every day** split its own audience across too many videos (52 videos in 58 days [V]).
2. **The topics drifted** from experiences every veteran shared (first week, last day, rations, firebase life) to narrow, negative individual cases (AWOL, fragging, jail, refusing a patrol).
3. Possibly the same title template reused too many times. "…Habits That Made No Sense (Until You Learn Why)" went from 104K → 11.7K → 9.3K → 3.2K [V].

**What this means for you:** copy what drove the first 3 weeks, not the last 6. The blueprint below has guardrails against all three causes.

---

## 1. Content strategy and target audience

**Positioning [V, from the avatar and transcript]:** "The Unwritten Manual: Vietnam 1965–1973. Not in the manual." Every video describes the gap between the official rule and what grunts actually did.

**Audience [V, from comments]:** Vietnam veterans in their 70s–80s and their families: widows, children, grandchildren. Top comments are personal memories:
- "80 years old now. I have nothing left but memories" (203 likes, 17 replies)
- "I just buried my brother on Sept 5… Agent Orange claimed him"
- "Left via Long Binh in '71… I brought an RPG launcher. It did not end well" (147 likes)
- Many comments name units, years and bases.

**Audience [A]:** mostly US-based, mostly male, 65+. They watch on TV or desktop and accept 20+ minute videos. That combination makes the audience valuable to advertisers.

**Why it works [A]:**
- Nostalgia and validation. "Somebody finally told it right."
- A sense of belonging. The comments section works like a reunion.
- Curiosity about what the rule really was and why people broke it.

---

## 2. Viral topics and recurring patterns

Top 20 by views [V]:

| # | Views | Title | Published | Length |
|---|---|---|---|---|
| 1 | 772,953 | 7 Things the Army Took From Grunts on Their Last Day in Vietnam | Sep 30 | 21:37 |
| 2 | 390,839 | 9 Firebase Rules the Army Never Taught Grunts in Vietnam | Sep 24 | 23:00 |
| 3 | 350,876 | 9 Things Nobody Told the New Guy His First Week in Vietnam | Oct 7 | 20:48 |
| 4 | 152,394 | 9 Things the RTO Did in Vietnam Because the Enemy Was Listening | Oct 6 | 23:13 |
| 5 | 150,487 | 8 Firebase Rules Grunts Lived By the Night Sappers Hit | Oct 3 | 22:12 |
| 6 | 104,013 | 9 C-Ration Habits That Made No Sense (Until You Learn Why) | Oct 11 | 22:13 |
| 7 | 80,751 | 9 Things the Army Refused to Believe About Grunts in Vietnam | Oct 5 | 24:11 |
| 8 | 60,831 | 9 Things Grunts Did Their Last 30 Days in Vietnam | Oct 9 | 21:06 |
| 9 | 58,674 | 9 Things Marines Had to Steal From the Army in Vietnam | Oct 12 | 21:52 |
| 10 | 36,153 | 9 Things the Army Ordered Grunts to Carry That Stayed in Base Camp | Oct 1 | 22:05 |
| 11 | 33,415 | 12 Times Grunts Out-Thought the Army Manual in Vietnam | Oct 2 | 24:28 |
| 12 | 31,322 | 8 Things the Man Walking Point Trusted More Than Any Officer | Sep 25 | 30:49 |
| 13 | 31,094 | 8 Rules That Kept Grunts Alive When Their Firebase Was Cut Off | Oct 8 | 22:36 |
| 14 | 29,918 | The Army Rule That Told Grunts to Skip Underwear in Vietnam | Oct 4 | 18:11 |
| 15 | 20,580 | The Purple Heart a Grunt Mailed to His Brother, Not His Parents | Oct 10 | 22:24 |
| 16 | 17,636 | The Army's Own Study Said Grunts Were Safer Farther Past the Wire | Oct 13 | 21:58 |
| 17 | 16,822 | 9 Weapons the Army Never Issued That Grunts Carried Anyway | Oct 15 | 22:00 |
| 18 | 11,754 | 9 Helmet Habits That Made No Sense (Until You Learn Why) | Nov 2 | 19:36 |
| 19 | 9,548 | 8 Night Rules That Kept Grunts Alive in the Bush in Vietnam | Nov 1 | 19:07 |
| 20 | 9,320 | 9 M16 Habits That Made No Sense (Until You Learn Why) | Oct 25 | 22:00 |

10 most recent [V]:

| Views | Title | Published |
|---|---|---|
| 135 | 9 Things the Army Did to a Vietnam Grunt Who Refused a Patrol in 1969 | Nov 21 |
| 439 | 9 Things the Army Did to a Vietnam Grunt Who Lost His M16 in 1968 | Nov 20 |
| 384 | 9 Things the Army Did to a Vietnam Grunt Charged With Fragging in 1971 | Nov 19 |
| 580 | 5 Things the Army Did to a Vietnam Grunt Who Went AWOL in 1970 | Nov 18 |
| 1,587 | 11 Things the Army Did to a Vietnam Grunt in Long Binh Jail in 1968 | Nov 17 |
| 436 | 12 Things the Army Did to a Vietnam Grunt Who Quit Basic in 1966 | Nov 16 |
| 506 | Why Grunts Rolled Their Sleeves Down in 100-Degree Heat | Nov 13 |
| 410 | Why Grunts Burned Poop Barrels With Diesel in Vietnam | Nov 12 |
| 173 | Why Grunts in Vietnam Kept a Short-Timer's Calendar | Nov 11 |
| 201 | A US Colonel Told Hanoi "You Never Beat Us." The Answer Hinged on One Word | Nov 10 |

**Patterns [V from the tables; interpretation A]:**
1. **Moments every veteran lived through win.** First week (351K), last day (773K) and last 30 days (61K). Every viewer can say "that was me."
2. **Places and daily systems win:** firebase rules (391K, 150K), rations (104K), radio procedure (152K).
3. **Official rule vs. what actually happened** is in nearly every hit ("Army never taught", "refused to believe", "out-thought the manual").
4. **Numbered lists of 7–9 items, 20–24 minutes long.** Every top-10 video is 20:48–24:11.
5. **Weak:** single-question "Why…" videos (173–506 views), individual punishment cases, and battle narratives ("LZ Grant", 2.4K).

---

## 3. Thumbnails (viewed directly) [V]

**What the hits look like (Sep 24 – Oct 13):**
- **No text at all.**
- A single photoreal candid scene that looks like 1960s colour film: warm, faded Kodachrome/Ektachrome tones, slight grain, soft contrast.
- Composition: one young soldier's face or body takes up 40–60% of the frame. His expression is tired, wary or blank. Usually a supporting element too: an MP inspecting gear, a sleeping man on sandbags, a caged bus marked "U.S. ARMY", a helmet with "Just You And Me, Right, Lord?" written on it.
- **Palette:** olive drab, khaki, dusty red earth, washed-out sky. Low saturation.
- **[A] They look AI-generated** in a 1960s film style. The faces are very clean, the lighting is too perfect and the details are too tidy for real archival photos. This is my visual judgment and isn't confirmed.

**What the flops look like (Nov 16–21):**
- 2–3 words of **bold yellow sans-serif text** with black outlines: "FROM HERO TO OUTCAST", "FIND IT OR PAY", "DEATH PENALTY", "SIGN OR JAIL", "WELCOME TO LBJ", "HE SAID NO", "UNBEATEN?".
- A red underline or swoosh, and staged courtroom or tribunal scenes.
- A cleaner, more modern AI render look.

**Recommendation [A]:** Use the no-text, faded colour-film style as your default. If you want to try text, A/B test it with YouTube's thumbnail test feature, limited to 2–3 words in a muted colour (cream or off-white, not neon yellow).

---

## 4. Title formulas and psychological hooks [V titles / A psychology]

| Formula | Example | Best result | Hook |
|---|---|---|---|
| `[N] Things [Authority] [Took/Did/Never Told] [Group] [Universal Moment]` | 7 Things the Army Took From Grunts on Their Last Day | 773K | Grievance + nostalgia + "I was there" |
| `[N] [Place] Rules [the Army Never Taught / Grunts Lived By] [Condition]` | 9 Firebase Rules the Army Never Taught Grunts | 391K | Insider knowledge, unwritten codes |
| `[N] Things Nobody Told [the New Guy] [Moment]` | …His First Week in Vietnam | 351K | Shared vulnerability ("we were all the new guy") |
| `[N] Things the [Role] Did Because [Threat]` | 9 Things the RTO Did Because the Enemy Was Listening | 152K | Role pride + curiosity |
| `[N] [Object] Habits That Made No Sense (Until You Learn Why)` | 9 C-Ration Habits… | 104K, then fading | A puzzle that gets solved. Wears out quickly |
| `The Army Rule That Told Grunts to [Absurd Thing]` | …Skip Underwear in Vietnam | 30K | Absurdity |

Common traits: "grunts" (insider word), "the Army" (the authority), specific places (Long Binh, Con Thien), and odd numbers (7, 9).

---

## 5. Script structure and storytelling (from the full transcript of the #1 hit) [V]

The transcript is about 3,200 words over 21:37, so **~148 words per minute.**

1. **Cold open, 0:00–0:51.** A present-tense scene: "Long Binh, 1970. A building made of plywood and sheet metal…". Close sensory detail (boots worn white at the toes, letters held with a rubber band, khakis with fold lines). It ends on a hidden object: a helmet cover with 365 crossed-out boxes.
2. **Honesty line + open loop, 0:51.** "That scene is put together from many accounts because it happened thousands of times… **We will come back to it before the end.**"
3. **Thesis + promise, 1:05.** "Seven things counted down from the one a man could laugh about years later to the one that still has no answer." The emotional intensity rises as the countdown goes.
4. **Early engagement prompt, 1:25.** "Tell us… where you are watching from, and if you served, where you flew home from and when." Then a like/subscribe request framed as service: "help these stories reach the men they belong to."
5. **Each numbered item (~2–3 minutes) follows the same 5 beats:**
   - a named object or system ("Number six, the money")
   - the official rule, with hard specifics (dates, form numbers like "DD Form 603", series numbers "641, 661, 681, 692", statistics)
   - "In practice…": how rules actually varied by year, port and the man behind the table
   - a human image ("a grandchild finds one and holds it up…")
   - a closing line ("Paper the army printed. And paper the army took back.")
6. **Second-person immersion in the middle (~9:50).** "Now, put yourself in that line… Your hand is on the strap. And you still do not know what you are going to do."
7. **Moral seriousness (~12:50).** "Every one of those rifles was carried by a man on the other side… This channel does not tell that part as a joke." This builds trust with veterans.
8. **Callback, 19:04.** The opening scene comes back, item by item, and the open loop is resolved.
9. **Epilogue.** The "freedom bird" flight: "the whole cabin cheered. And then… it went quiet."
10. **Final call to action.** "What did they take from you at the table?… **The best answers may become a future video.**" Then a share prompt aimed at families, and a dedication: "this one is for you."

**Persona [V/W]:** the narrator speaks in third person with moments of second person. **He never claims to be a veteran.** No AI or sourcing disclaimers [W]. In the C-ration video he names sources out loud: the Library of Congress, the Rutgers oral history archive, Natick Laboratories, and memoirs [W].

---

## 6. Animation, visual effects, shots and transitions [W unless marked]

- **Visuals:** "archival Vietnam photographs and brief 16mm newsreel footage" [W, both hit videos].
  - **Caution:** this conflicts with the AI look of the thumbnails [A]. The watch tool may not tell AI stills apart from real archival photos. Expect a mix: real public-domain archival material plus AI "period" stills to fill gaps.
- **Shot length:** 2–6 seconds per shot. Not animation: stills with motion.
- **Camera:** Ken Burns slow push-ins and pans, slight parallax on documents.
- **Look:** faded retro colour, simulated film grain, vignette, occasional blue or sepia duotone.
- **On-screen text:**
  - word-for-word captions in bold sans-serif (white with a shadow in one video, yellow in another [W]; inconsistent)
  - lower-third tags in all-caps, e.g. `BINH DINH PROVINCE • 1ST FIELD FORCE • JULY 1967`
  - like/subscribe overlay animations
- **Transitions:** mostly straight cuts on narration beats. Each numbered item gets a short pause and a title moment.

## 7. Narration, music and sound [W]

- **Voice:**
  - #1 hit: "male, middle-aged, American, measured… sounds human"
  - C-ration video: "deep, raspy… **likely AI-assisted**"
  - So it's either a professional human voice or a high-quality cloned or AI voice [A].
- **Pace:** ~148 wpm [V], with 0.5–1 second pauses before each number.
- **Music:** low melancholy ambient pads with sparse piano or guitar, kept well under the voice.
- **Sound effects:** none in the #1 hit. The C-ration video and the flop add subtle helicopters, distant artillery and jungle ambience.

## 8. Engagement and retention [V numbers / W techniques]

| Video | Like rate | Comment rate |
|---|---|---|
| #1 (773K) | 0.69% | 0.05% (407 comments) |
| C-Ration (104K) | 1.29% | **0.37%** (386 comments; prompts like "do you still have your P-38?") |
| First Week (351K) | 0.84% | 0.10% |

**Retention techniques:**
- an open loop in the first minute that pays off at the end
- a countdown with rising emotional intensity
- each item ending on an unresolved line ("Where the pile went, nobody can say")
- a second-person scene in the middle
- callbacks to the opening
- **comment prompts that ask for specific memories (unit, base, year)**

**Comment loop [V wording]:** "The best answers may become a future video." Comments become both research and topic ideas for later videos.

## 9. Upload strategy [V]

- 52 long-form videos in 58 days, **roughly one a day.**
- Published at 17:00 UTC (1pm US Eastern) before the clock change and 18:00 UTC after it, so 1pm ET either way. One upload went out at 06:00 UTC.
- No Shorts in the data I pulled.

## 10. Estimated revenue

- **vidIQ estimate for the #1 video [V]:** **$529–$1,410 (mid $881)**. That works out to about $0.68–1.82 RPM.
- **Caveat:** vidIQ bases this on the channel's country (Ukraine), which lowers the estimate. The comments show a clearly **US audience.**
- **My estimate [A]:** with US viewers aged 65+ watching 20-minute history videos, $4–10 RPM is more realistic.
  - Lifetime, if monetized: vidIQ's model gives **$1.7K–4.5K**; my US-audience assumption gives **$9.8K–24.5K.**
  - Current run rate (~45K views/month): **$30–450/month.**
- **Monetization status is unknown.** 5,900 subscribers and well past 4,000 watch hours, so it's almost certainly eligible, but I can't confirm it's approved.

## 11. Likely software and AI tools [A — nothing here is confirmed]

| Job | Likely tool(s) |
|---|---|
| Research and script | An LLM (Claude/GPT) plus real sources: Library of Congress Veterans History Project, Rutgers Oral History Archives, the US Army Center of Military History, NARA |
| Thumbnails | Midjourney or FLUX with a "1960s Kodachrome candid photo" style; text added in Photoshop or Canva |
| Archival visuals | NARA, the Army Signal Corps and other public-domain DoD collections; possibly AI stills for gaps |
| Voice | A professional voice actor, or an ElevenLabs-grade cloned or professional voice |
| Edit | CapCut, Premiere or DaVinci Resolve with a film-grain/vignette template, auto-captions and Ken Burns presets |
| Music | Epidemic Sound, Artlist or the YouTube Audio Library (ambient/somber) |

---

# THE PRODUCTION BLUEPRINT

## Guardrails (built in because of what killed the original's momentum)

1. **Cadence: 3 videos a week, not daily.** Gate each next video on the previous one's 72-hour performance.
2. **Topic mix:** 70% moments every veteran shared or daily systems, 20% roles (RTO, medic, cook), 10% experiments. **No more than 2 videos in a row** with the same title formula.
3. **No fake veteran persona.** Narrate in third or second person like the original. Use its honest line about composite scenes. Never invent quotes and attribute them to real people.
4. **Sources required for every factual claim** (go/no-go gate). List them in the description.
5. **Disclosure:** tick YouTube's "altered or synthetic content" box whenever AI stills depict realistic scenes.
6. **Rights log:** every archival asset needs a source URL and its rights status. US federal works are generally public domain. Oral-history collections (Library of Congress, Rutgers, Texas Tech) have their own terms, so check each one.
7. **Human approval** before anything is published or uploaded. Your current production workflow (the TikTok media repo) stays untouched; this pipeline is separate.

## Agent roles and step-by-step workflow

### Step 1 — Topic Scout agent
- **Input:** the topic bank (section 13 below) plus fresh data.
- **Actions:**
  1. vidIQ `outliers` (keyword: Vietnam/military-life topic, `maxSubscribers` 50K, `publishedWithin` threeMonths).
  2. `keyword_research` for search demand.
  3. Mine your own comments (`video_comments`) for memories and requests.
  4. `comment_insights` with `mode=validate` on each shortlisted idea.
- **Output:** 3 ranked topics, each with evidence (competitor views, comment quotes).
- **Gate:** the topic is a shared moment, a daily system or a role, and it repeats none of the last 2 title formulas.

### Step 2 — Research agent
- **Sources, in priority order:**
  - US Army Center of Military History publications, field manuals of the period, NARA catalog API
  - Library of Congress Veterans History Project (cite; check rights before reusing media)
  - Rutgers Oral History Archives, the Texas Tech Vietnam Center & Archive
  - memoirs (cite, don't copy)
- **Output:** a research dossier.
  - 7–9 items, each with: official rule (with date or document), what happened in practice (2+ independent accounts), one human detail, and citations
  - plus one opening scene built from many accounts (labelled as a composite)

### Step 3 — Fact-check agent
- Checks every date, number, form name and unit against at least 2 sources.
- Flags anything with only one source, and removes or softens those claims.
- **Gate:** zero unsupported specific claims.

### Step 4 — Script agent (template below)
- **Target:** 3,000–3,400 words, about 21–23 minutes at 148 wpm.
- Writes in plain, concrete prose with short sentences. No hype words.
- **Output:** a script marked with item breaks, `[PAUSE]` beats and lower-third tags.

### Step 5 — Voice agent
- ElevenLabs API, which **is already connected in this cloud environment.** The model is a mature, warm American male voice from ElevenLabs' licensed voice library, or a voice actor's clone with written consent. Never clone a real veteran or a well-known narrator.
- Settings:
  - stability ~0.5
  - style low
  - render each item separately so mistakes can be redone cheaply
  - insert 0.6–1.0 second silences at `[PAUSE]`
- **Gate:** a listen-through pass. Check pronunciation of place names (Cam Ranh, Quang Tri, Tan Son Nhut) with the pronunciation dictionary.

### Step 6 — Visual Asset agent
- **Tiers:**
  1. Public-domain archival photos and film (NARA, DoD/DVIDS historical, Army Signal Corps)
  2. AI "period" stills (FLUX/Midjourney) only to fill gaps, always disclosed, never presented as a real photo of a named person or event
  3. Maps and document recreations
- **Output:** a shot list of about 300–450 images and clips for 22 minutes (one every 3–4 seconds), plus a **rights log CSV.**

### Step 7 — Edit agent (programmatic)
- Remotion (React) or FFmpeg + MoviePy.
- Template:
  - Ken Burns push-in or pan on every still (4–8% scale over the shot)
  - film-grain overlay at ~8–12% opacity, vignette, faded LUT (lifted blacks, warm mids)
  - lower-third: all-caps place • unit • month year
  - item title card: "NUMBER SIX — THE MONEY"
  - captions burned in from WhisperX word timestamps (cream or white, 2 lines max)
- **Audio:** music bed at −24 to −28 LUFS under a voice at −16 LUFS integrated. Optional jungle or helicopter ambience at very low level only during scenes.

### Step 8 — Thumbnail agent
- Make 3 variants:
  - **A:** no-text faded colour-film candid (the style that won)
  - **B:** the same image with 2–3 muted words
  - **C:** an alternative image
- Prompt pattern: "1968 Kodachrome candid photograph, [specific scene], young American soldier, [emotion], faded warm colors, film grain, documentary photojournalism".
- Score them with vidIQ `score_thumbnail`. The top 3 go into YouTube's Test & Compare.

### Step 9 — QA agent
- vidIQ `video_watch` on **your own rendered file** (videoUrl mode; 25 credits for files over 3 minutes). Prompt it to check: hook clarity in the first 30 seconds, AI artifacts (hands, gibberish text, anachronisms like modern weapons or uniforms), caption sync, and audio levels.
- vidIQ `score_title` on 5 title options.
- **Gate:** no artifacts, no anachronisms, every claim has a source.

### Step 10 — Publish-prep agent (draft only)
- Writes the description (summary, chapters, a sources list, an AI-disclosure note), tags and the pinned comment (a memory prompt).
- Uploads as **private** through the YouTube Data API, or just prepares the files.
- **Stops and asks for your approval.** Scheduled slot: 1pm ET.

### Step 11 — Analyst agent
- vidIQ `video_stats` at 24 hours, 72 hours and 7 days, plus YouTube Analytics (CTR, average view duration, traffic sources).
- Writes a one-page report: what to repeat, what to cut, and which comment memories to turn into future videos.
- **Kill rule:** if 3 videos in a row get under 30% of the channel's 30-day median, pause and change the topic mix.

## Script template (for the Script agent)
```
COLD OPEN (≈130 words): "[Place], [Year]." Present-tense scene. 5+ physical details.
  End on one hidden/small object. Then: "That scene is put together from many accounts…
  We will come back to it before the end."
THESIS (≈60 words): what the war/army took or taught; promise N items, "counted down from
  the one a man could laugh about to the one that still has no answer."
PROMPT (≈45 words): "Tell us where you're watching from — and if you served, [specific memory question]."
ITEM ×N (≈320 words each): "Number N, [object/system]." Official rule (date/form/number) →
  "In practice…" (variation by year/place/person) → human image → closing line.
MID IMMERSION (inside item ~N/2): "Now put yourself in [place]…" 2nd person, present tense, ends undecided.
RESPECT BEAT (once): acknowledge the other side / the dead, plainly.
CALLBACK (≈120 words): return to cold-open object; list items as images.
EPILOGUE (≈150 words): what came next (flight, homecoming).
CTA (≈90 words): specific memory question + "the best answers may become a future video" +
  share-with-family line + dedication.
```

## Repositories, tools, skills and automation

**Open-source repos (all real, widely used):**

| Purpose | Repo |
|---|---|
| Agent orchestration | `anthropics/claude-agent-sdk-python` (or `langchain-ai/langgraph`) |
| Programmatic video | `remotion-dev/remotion` (templates, captions, Ken Burns) or `Zulko/moviepy` + `FFmpeg/FFmpeg` |
| Word-level caption timing | `m-bain/whisperX` (or `SYSTRAN/faster-whisper`) |
| Voice API | `elevenlabs/elevenlabs-python` |
| Local image generation | `comfyanonymous/ComfyUI` + FLUX models (`black-forest-labs/flux`) |
| Upscaling archival photos | `xinntao/Real-ESRGAN` |
| Thumbnail text and compositing | `python-pillow/Pillow` |
| Shot detection and QA | `Breakthrough/PySceneDetect` |
| YouTube upload (private drafts) | `googleapis/google-api-python-client` (YouTube Data API v3) |
| Reference pipelines to study (don't copy blindly) | `harry0703/MoneyPrinterTurbo`, `FujiwaraChoki/MoneyPrinter` |

**APIs and services:** vidIQ (connected), ElevenLabs (connected), the NARA Catalog API, the Library of Congress API, Midjourney/FLUX, Epidemic Sound or Artlist (licensed music), YouTube Data API + Analytics API.

**Skills to give the agents:**
- a research-citation skill (claims → sources)
- a script-template skill (above)
- a rights-log skill
- the editing template as Remotion code
- a QA checklist skill
- a publish-prep skill that is draft-only

**Estimated cost per video [A]:**
- tools: $15–40 (voice ~$5–10, images ~$5–15, music subscription share, vidIQ credits ~60–80)
- human review: 1–2 hours
- tools per month at 3 videos a week: ~$150–350

---

## 13. 30 original topics (built from the verified patterns, not copies of their titles)

**Moments every veteran shared** (strongest pattern):
1. 9 Things That Happened a Grunt's First Night on a Firebase
2. 8 Things the Replacement Depot Handed the New Guy at Bien Hoa
3. 8 Things That Changed the Week a Grunt Got Short
4. 9 Things a Grunt Learned on His First R&R
5. 7 Things Waiting for a Vietnam Vet at His First Thanksgiving Home
6. 9 Things a Vet's Family Noticed His First Week Back
7. 7 Things the Freedom Bird Flight Was Really Like
8. 8 Things That Happened the Day a Grunt Made Sergeant in the Field

**Places and daily systems:**

9. 9 Unwritten Rules of a Huey Ride Into an LZ
10. 8 Monsoon Rules Grunts Lived By in the Highlands
11. 9 Rules of a Base Camp Hooch Nobody Wrote Down
12. 8 Mail Call Rules That Kept a Platoon Sane
13. 9 Rules for Writing Home Every Grunt Learned
14. 8 Hot-Meal Rules When the Mess Hall Was 30 Miles Away
15. 9 Things That Happened When a Grunt Called Home on a MARS Radio

**Objects ("why they did it" angle; rotate formulas, don't overuse "Made No Sense"):**

16. 9 Things Grunts Wrote on Their Helmet Covers
17. 9 Uses for a Poncho Liner the Army Never Planned
18. 9 Things a Grunt Carried in His Steel Pot
19. 8 Things Grunts Engraved on Their Zippos, and Why
20. 9 Rucksack Lessons Grunts Learned the Hard Way

**Roles** (the RTO video got 152K):

21. 9 Things the Medic Carried That Weren't in His Aid Bag
22. 8 Things the Company Clerk Knew About Everyone
23. 9 Things the Scout Dog Handler Knew About the Trail
24. 8 Things the Firebase Cook Did That Grunts Never Forgot
25. 9 Things the Chopper Crew Chief Saw From the Door

**Official rule vs. reality:**

26. 9 Things the Army Promised Grunts That Never Showed Up
27. 8 Things Grunts Traded the Navy For
28. 9 Things the Army Changed After 1968 That Grunts Noticed First
29. 8 Army Inspections Grunts Learned to Beat
30. 9 Things the Army Manual Said About the Jungle That Grunts Ignored

**Order for the first 9 videos [A]:** 1, 3, 21, 9, 6, 16, 26, 2, 13. Strongest patterns first, with no back-to-back repeats of a formula.

---

## What I didn't verify / next steps
- Thumbnail CTR and audience retention: only the channel owner can see those.
- Whether the channel is monetized, and whether its later videos were limited by YouTube.
- Whether the visuals are AI or archival: the watch tool and my own reading of the thumbnails disagree.
- **Your decisions:**
  - the channel name and positioning (don't reuse "Grunt's Field Notes" or "The Unwritten Manual")
  - human narrator or licensed AI voice
  - approval to build the pipeline (I haven't touched any existing workflow)
