# Workflow: 3D characters rendered directly in Blender (approved direction, Sean 2026-11-24)

Goal: a three dimensional version of the approved 2D hero and opponent (reference: skill fight-playbook-rules `main_character_reference.jpg`, `pair_ref_hero_vs_opponent.jpg`) rendered straight from Blender, so anatomy is controlled exactly. Final images never pass through a generative image model.

## Gates (Sean)
1. Character design only until Sean personally approves the model. No rigging for animation, combat poses, animation or video work before that approval.
2. Every turnaround (front, right, left, back, three quarter, orthographic) is inspected against the reference by BOTH the combat-anatomy-specialist and the visual-creative-director before Sean sees it.
3. No paid generation or purchases; free and open source tools only.

## Method (required)
* Setup per fresh container: `bash production/blender/setup_blender.sh` (pip bpy, Mesa EGL for EEVEE, MPFB2 clone and install as a Blender extension).
* Base: MPFB2 professional base (CC0 MakeHuman mesh, macro and region targets, default rig with skin weights). Script: `production/blender/hero_mpfb.py`. Shape with targets (macros: male, muscle 1.0, proportions 1.0; region: shoulders, pectorals, lats, waist, arm and leg muscle), never with hand made vertex hacks.
* Pose only through the MPFB rig (skin weights), never by rotating vertices.
* Head: keep the MPFB skull, jaw and ears; NO MOUTH, no nose: remove features with targets, delete every face-zone face not visible from the front (faces only), Shrinkwrap the weighted face (mouth at full weight) onto a hidden, rig parented convex hull proxy of the head and transfer its normals (remesh is used ONLY on that proxy, never on the rendered body); eyes = filled white slanted almonds angled toward the centre (2026-11-24 r18).
* Garments: offset shells of the body faces (Shrinkwrap + Solidify, 2 to 4 mm, no booleans), shorts loose and straight to above the knee; red yoke, side stripes and hem V notches as crisp texture decals; gloves sculpted as padded MMA gloves with knuckle rows and a wide red strap.
* Look: 2 tone cel (Shader to RGB into a Constant ramp in EEVEE, or the emission toon in Cycles), one key light from the upper front, clean big shadow shapes; bold outer ink (inverted hull or Line Art) plus thinner interior lines.
* Do not use: primitive or metaball bodies, voxel unions, skin modifier tubes, garment shells from body fragments, image to 3D generators (see production/blender/README_FAILED_APPROACHES.md).

## SUCCESSFUL METHOD (Sean 2026-11-24: "significant improvement"; permanent checkpoints production/hero_checkpoints/t2_permanent and f3_refined)
1. Mesh: Hunyuan3D-2mv (free HF Space) from the 4 sheet views (production/meshgen/run_hy2mv.py, token on the env proxy). Do not swap base models.
2. Build: `cd production/meshgen && python3 hero_tex.py out/hy2mv_shape_generation_0.glb OUTDIR` (about 2 min, hi res 1400x2160 + 1600 close ups).
3. Geometry fixes in hero_tex.py: remove_plate (floor plate generated from the sheet shadow), head_neck (head +14 percent above the chin, neck core slimmed 12 percent, smooth falloff).
4. Texture = the sheet art itself: per view planar UVs (figure matched by height and centre), BVH visibility per vertex, weights sharpened RELATIVE to the best view (^24); sheet prepared with background + outer outline + eyes inpainted (cv2), bilateral smoothing, red snapped to #E0262B.
5. Eyes: decal almonds from sheet head ratios (hero_hy.EYE), inner ends down, offset 3 mm. Ink: displaced hull copy.
6. Pitfalls: absolute ^24 weights underflow (ghosting); sheet outer outline paints dark caps; zone rule colouring (hero_hy) is the fallback only.
7. Head pass (g10, production/hero_checkpoints/g10_head_pass; f3_refined is the fallback): head_fit.py warps head and neck GEOMETRY to the sheet: chin found by the profile jump (model 1.712 -> sheet 1.748) and z remapped above 1.66; face pushed to the head's convex envelope (no nose, mouth, cheek dents); row by row x and y fit to the sheet front and right silhouettes above z 1.68 (lower rows include the shoulders and warp the traps); jaw ring smoothed; head and neck core get a uniform 2 tone cel (no mask seams); eyes TRACED from the sheet eye contours (sheet_eyes); ink hull smoothed before displacement.
   Open: temple width vs ears (front view slightly light bulb), small crease under the jaw.
