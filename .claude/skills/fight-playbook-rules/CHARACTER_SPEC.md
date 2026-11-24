# Character spec (WRITTEN FOR THIS EXPORT; consolidated from RULES.md R1, the long-form skill, Letta brand_rules and the prompt blocks in mk_v3_prompts.py / prompts.py)

Reference sheet: `main_character_reference.jpg` (front, right, left and back views). This exact image is the reference node on the ElevenLabs flow; every still is generated wired to it.

## Hero (main character)
* Dark charcoal gray skin, bald, muscular, athletic proportions; stays the smaller fighter next to the opponent.
* Faceless: completely smooth blank face with ONLY two small slanted white eyes. No mouth, nose, eyebrows or teeth.
* **Long-form YouTube outfit (Sean, Nov 23, 2026):** plain black sleeveless compression shirt with red accents and red side stripes, navy shorts with red trim, black MMA gloves with red wrist straps, barefoot. Never bare chested. Shirt brand text, if shown, is red and white (never yellow); the liver prompts ask for no lettering.
* **Short-form and TikTok outfit:** gray tank top (same body and face).
* Stance: orthodox (left lead). A liver shot is the LEFT hook to the opponent's RIGHT side.

Prompt block used (verbatim from `PROMPTS/liver-image-prompts/generators/prompts.py`): "MAIN CHARACTER (exactly as in the reference image): dark charcoal gray skin, bald, muscular, faceless with a completely smooth blank face and ONLY two small slanted white eyes, no mouth, no nose, no eyebrows, no teeth. Plain black sleeveless compression shirt with red accents and red side stripes, NO lettering or logo, never bare chested. Navy shorts with red trim. Black MMA gloves with red wrist straps. Barefoot, no shoes or socks."

## Opponent
* Always red and always bigger than the hero. Same faceless charcoal style, bald, two small slanted white eyes only.
* Plain RED sleeveless tank top with no lettering, black shorts, plain black gloves, barefoot.

## Style
* Clean 2D comic illustration, crisp thin black outlines, flat colours, subtle cel shading, no photorealism.
* One flat background colour per video (sage `#C4D6C4` for the liver video), no scenery, floor texture, gradient or props unless named.
* Strikes: thin black speed lines only, drawn in code, landing on the chin, jaw or body.
* Exactly one of each character per shot; no turnaround or ghost copies of the reference sheet.

## Movement and anatomy rules
* `anatomy/production_notes_arm_mechanics.md`: arm mechanics per punch type, prompt templates, QA checklist.
* `anatomy/hook_rules.md`: Sean's permanent left and right hook rules (Nov 23, 2026).
* `anatomy/FIGHTING_TECHNIQUE_ANIMATION.md` and `anatomy/technique_library/`: per technique mechanics (jab, cross, uppercut, lead hook to liver, high guard, catch block, chin tuck, step off at an angle, clinch knee, biceps jam, wild punch).

## Other files here
* `pair_ref_hero_vs_opponent.jpg`: hero and opponent together, used by the per-verb shared builds.
* `character_ref_promo_batch.jpg`: reference used for promo batches.
* `punch_speed_lines_reference.jpg`: the approved look of the speed lines.
* `rig_side_puppet/`: experimental 2D cut-out side-view puppet (parts, `rig.json`, pose scripts). Not used in production.

No 3D models, textures or Blender rigs exist for this project.
