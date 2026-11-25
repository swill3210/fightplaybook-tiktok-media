# Visual QC master checklist (condensed; detail: `vfl.py show CODE`)
Borderline = FAIL. Uncertain = UNSURE (escalated). Reply one line per asset: `ID PASS` | `ID FAIL CODES note` | `ID UNSURE CODES note`.

**A Anatomy (missing heads, extra or disfigured limbs)**
- A01 !Extra limb, hand, glove or wrist: Count arms, hands, gloves and wrists per character on every still and every animation frame; exactly two of each.
- A02 !Missing head or missing body part: Every visible arm must trace to a shoulder, a torso and a head inside the frame or leave through the bottom or a corner. A limb attached to a shapeless blob fails.
- A03 !Distorted, kinked or rubbery limb: Zoomed crop of every arm: one bend at the elbow only, segments of similar length, no stretch or snake shapes.
- A04 !Impossible joint or reversed limb: Check which shoulder each arm leaves from and the thumb side; wrists straight behind the glove.
- A05 Bare fist or wrong glove type: Hero gloves are black MMA gloves with red wrist straps exactly as drawn on the reference sheet (visible finger segments are correct, Sean C4 ruling 2026-11-24); fail bare fists, loose open fingers, peach hands or boxing gloves (bare hands only in a grip tutorial).
- A06 !Bodies merged or limbs tangled: For every limb, name its owner. Any limb whose owner is unclear fails. Keep a visible gap between torsos.
- A07 Disproportion or lens distortion: Compare proportions with the reference sheet; no body part more than about 1.3x its reference size relative to the head.
**B Strike and movement mechanics**
- B01 !Hook drawn as a straight or open arm: Hooks: elbow about 90 degrees (fail outside 70 to 110), forearm level, elbow at glove height (hook_rules.md).
- B02 !Hook elbow height or forearm angle wrong: Elbow level with the glove, forearm level; check in a zoomed crop.
- B03 !Uppercut or shovel with the elbow off the hip: Uppercuts and shovels: elbow at the own hip, forearm 70 to 85 degrees from horizontal, glove rising under the ribs or chin.
- B04 !Straight punch kinked, sagging or overlong: Straight punches: shoulder, elbow and glove in one line, elbow at least 160 degrees, arm length matches the other arm.
- B05 Guard hand dropped or elbows flared: Non punching glove at the chin or cheek; guard elbows on the ribs (at least 0.45 x torso below the shoulder in the rig).
- B06 !Wrong technique drawn: Name the technique in the picture before reading the spec; it must match the spec and narration.
- B07 !Kick or leg mechanics wrong: Kicks and checks: shin meets shin, one planted foot, no leg passes through another, knees land on the stomach or ribs.
- B08 Motion phases wrong or kinetic chain missing: Chamber shows the glove at the guard, impact at full technique, recover back at the guard; check every in between frame, not only key poses.
- B09 Implausible reaction or impossible pose: Ask: would this happen in a real exchange? If not, regenerate.
**C Positioning and orientation**
- C01 !Wrong arm for the named punch: Name the punching arm by owner and image side before checking anything else (hook_rules.md screen side table).
- C02 Screen side swap without a motivated transition: Plan screen sides for the whole video; a side change needs a whip pan or a hard cut inside a montage (C14).
- C03 !Target on the wrong side of the body: Orthodox liver = opponent's RIGHT side; check image side for every liver contact and target graphic.
- C04 !Wrong character performs the action: Confirm who acts in the narration and who acts in the picture.
- C05 !Head or face orientation impossible: Check that the eyes sit on the side of the head that faces the camera for that body orientation.
- C06 !Stance switched (southpaw instead of orthodox): Orthodox: LEFT hand and LEFT foot lead in every shot; the same jab hand throughout a sequence.
**D Floating or disconnected parts**
- D01 !Floating or detached glove, hand or limb: Every glove and hand must trace through a wrist, forearm and upper arm to a shoulder.
- D02 Feet floating or detached from the ground: Planted feet touch the ground line; one foot at least is planted in every standing technique.
**E Character design consistency**
- E01 !Face features on a faceless character: Faces are blank with exactly two small slanted white eyes; nothing else.
- E02 Outfit drift: Compare every character with the reference sheet for the format (long form black shirt, Shorts gray tank; opponent red tank, black shorts, plain black gloves; barefoot).
- E03 Skin or colour drift and speckles: Skin is charcoal everywhere; run the colour screener and inspect flagged patches at full size.
- E04 !Ghost, duplicate or extra character: Count characters; exactly the scripted cast, no faded or turnaround copies.
- E05 Opponent size or role wrong: Opponent about half a head taller with broader shoulders in every two shot.
- E06 Style break: Compare with approved 2D stills; reject any 3D shading or glow on the characters.
**F Impact physics and contact**
- F01 !Strike lands on a forbidden target: Strikes land only on chin, jaw or body (ribs, liver, stomach), with the neck visible and clear.
- F02 !Strike does not connect or a miss reads as a hit: Contact Law (amended Sean 2026-11-25): every landed punch touches the target surface with the whole glove visible ON TOP of the clothing; the body reacts through posture, never through cloth deformation; every miss shows a clear gap. Never prompt buried, sinks, dents or compressing.
- F03 !Glove or limb buried inside the opponent or their clothing: At contact the whole glove stays visible on top of the shirt and the shirt keeps its natural structure (Sean 2026-11-25). Any glove partly under fabric, any shirt hem lifted by the glove, any cloth swirl or vortex fails. Zoom to the contact on every strike still.
- F04 !Forbidden impact effect: Speed lines drawn in code are the only strike effect (R11); image prompts say draw no effects.
**G Camera framing and cropping**
- G01 Head or body cut by the frame edge: Nothing important touches the left, right or top edge; bodies leave only through the bottom or a corner.
- G02 Text or graphic covering a head, face or the action: Every overlay box must sit on background pixels only; check every shot an overlay spans.
- G03 Camera hides the key action: Pick the angle that shows the lesson; the technique in the narration must be visible.
**H Animation, transition and compositing**
- H01 Overlay or layer compositing error: Overlays on their own transparent layer; inspect the first and last frame of every overlay.
- H02 Empty, frozen or dead frames: No frame is mostly empty background outside intended cards; every second has motion.
- H03 Transition or render error: Render to a new filename with no other render running; frame check every transition.
- H04 !Interpenetration in animation: Check every animation frame, not key poses only; the rig collision metrics must be zero.
- H05 Placeholder, watermark or reused crop shipped: No placeholder or watermark ever reaches a cut; reused stills at most twice and never adjacent.
- H06 Stray lines, streaks or artifacts: Inspect edges and backgrounds at full size.
**I Narration, caption and text accuracy**
- I01 !Visual contradicts the narration: At each narration line ask: does the picture do exactly what the words say, right now?
- I02 Caption or on screen text error: Every label must be true of the picture under it; captions match the spoken words exactly.
- I03 No visible change between beats: One verb, one image: every beat has a start pose, an end pose and a visible change.
