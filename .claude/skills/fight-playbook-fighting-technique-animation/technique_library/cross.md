# Cross (straight right, rear straight)
Created Nov 23 2026 for tt_liver_vs_head (Why a Liver Shot Can Hurt More Than a Head Shot). Source: FIGHTING_TECHNIQUE_ANIMATION.md sections 3, 15 and 16.

**Alternative names:** cross, straight right (orthodox), rear straight, the two, right hand. Southpaw: straight left.

**Starting stance (orthodox):** left foot forward, right foot back, gloves at the cheeks, elbows on the ribs, chin tucked. Mid to long range (about one arm length).

**Arm and leg positioning:**
- REAR (right) arm punches, travelling in a STRAIGHT line from the chin to the target, palm turning down, elbow nearly straight at contact but never locked or hyperextended.
- LEAD (left) glove stays on the left cheek and chin the whole time, elbow tucked.
- Knees soft, spine upright and balanced over the feet; no leaning past the lead knee.

**Trajectory:** straight out and straight back along the same line. Never a loop, swing or hook.

**Hip and shoulder rotation:** the rear hip and rear shoulder rotate forward together; the rear shoulder ends up forward, near the chin line.

**Foot placement and pivot:** pivot on the ball of the REAR (right) foot, heel lifting and turning out; lead foot stays planted.

**Target:** the chin or face (never the neck). Against a tight high guard it lands on the gloves and forearms (the mistake in tt_liver_vs_head).

**Recovery:** the rear hand comes straight back to the right cheek, hips and shoulders return to guard.

**Opponent reaction:** on a clean landing the head moves back along the line of the punch; when blocked, the gloves are pushed back toward the face and the opponent stays upright (15.11).

**Common animation mistakes:**
- Drawing the LEAD arm extended (that is a jab) while calling it a cross. In any non side view the image model drew the lead arm every time (see the catches below).
- The punch drawn as a swing or arc (that is a hook or overhand).
- The lead hand dropping from the chin.
- Locked or hyperextended elbow; leaning over the lead knee.

**Real catches in builds (tt_liver_vs_head, Nov 23 2026):**
- Side view, main character on the RIGHT facing LEFT (ws_head): both variations drew a correct cross: the near (lead) glove stays at the chin and the extended arm comes from the far (rear) shoulder behind the head. Variation a kept (the glove lands flat on the partner's raised gloves).
- Second camera angle FAILED 5 times: a rear three quarter try, 2 rear three quarter retries that named the right arm as "the one on the right of the back, nearest the viewer", a front three quarter try and 2 front three quarter retries that described the arm by image side. Every one drew the LEAD arm extended with the rear glove at the chin, which is a jab. Not used. Next time: keep the cross in side view with the puncher's lead side toward the camera (the far arm punching reads correctly), or try a top down view, or check it with a pose reference instead of text.

**Best camera angles:** side view with the lead side toward the camera (extension, straight line, rear arm passing behind the head line); front view for the straight path down the centre line (hard for the image model); rear three quarter for the rear hip turn and heel pivot (hard for the image model).

**Extension Nov 23 2026 (tt_protect_chin):** the cross thrown BY the attacker, seen over the attacker's own shoulder (camera behind the attacker's left shoulder, attacker's back to the camera, defender facing the camera). This camera draws the cross well: the right arm extends in one straight line from the right shoulder, rear heel lifted, lead glove at the own face (pc_hook4_a lands on the lifted chin; pc_block3_b lands on the raised glove). The image model also turns any "hook" request in this camera into this straight arm, so use this camera for crosses, not for hooks. Speed lines: clear background above and below the extended arm, so streaks draw (render log calls under 3 = 0).
