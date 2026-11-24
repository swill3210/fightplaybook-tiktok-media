# Blender character model: failed approaches (2026-11-24)

Goal (Sean): a 3D version of the approved 2D hero (reference sheet `main_character_reference.jpg`), rendered directly in Blender, no generative model. Status: NOT approved. Both inspectors FAILED the model (combat-anatomy-specialist: FAIL; visual-creative-director: REVISE).

## What was tried and why it failed (do not repeat)
1. Skin modifier tubes on a joint skeleton (fp_chars.py): thin mannequin limbs, tube head, no muscle forms.
2. Metaball muscle volumes (hero_model.py v1): elements did not blend; separate shrunken blobs.
3. Voxel union of ellipsoid "muscles" + smoothing (hero_model.py v2 to v5): reads as a segmented action figure; jaw volume drew a mouth like crease (E01); boxy or diaper shorts.
4. Plane sliced or separate skin mesh garments: torn shirts, holes, speckled hems.
5. MakeHuman base.obj with hand made edits (hero_mh.py): arms re posed by soft vertex rotation (no rig weights), "heroic" radial scaling hacks, egg head stuck on a separate neck (donut neck read as a mouth), offset shells built from body fragments (skin poked through the shorts, stray wire loops, holes), deltoid spheres bolted on.
6. Shading: emission based fake light 3 band ramp gave blotchy camouflage patches; Freestyle ridges and valleys produced scribbles; no consistent bold ink outline.
Root cause: patching primitives and hacking a base mesh without its rig, targets and proper garment modelling.

## Inspector consensus for the next attempt
* One continuous professional base body at the reference proportions (MPFB2: CC0 MakeHuman base mesh with per region muscle and measurement targets, standard rig with skin weights, A pose). Head, jaw and neck part of the same mesh; face features removed with targets and smoothing, ears kept.
* Model against the FRONT and RIGHT reference views as orthographic background images.
* Garments as 2 to 4 mm offset shells of the body faces (Shrinkwrap + Solidify, no booleans) so skin cannot poke through; shorts loose and straight to above the knee.
* Red raglan yoke, side stripes, hem V notches and the eyes as crisp UV texture decals (filled white slanted almonds angled toward the centre).
* Gloves sculpted as padded MMA gloves with knuckle rows and a wide red strap.
* Shading: EEVEE Shader to RGB into a Constant ramp, exactly 2 bands (base #4A4A4E, shadow about 30 percent darker), one key light from upper front, clean custom normals (data transfer from a smoothed proxy) so shadow shapes are big and readable; narrow sheen on the shirt only.
* Lines: Grease Pencil Line Art (silhouette, crease about 60 degrees, material borders), near black, about 3 px at 1080p, thinner interior lines; inverted hull as a silhouette fallback.

## Environment facts
* 4 CPU cores, 15 GB RAM, no GPU. Blender 5.3 as pip `bpy`; EEVEE works on software GL after `apt-get install libegl1 libgl1-mesa-dri libegl-mesa0` (slow first shader compile), Cycles CPU and Workbench work, Freestyle works.
* MPFB2 repo clones from GitHub (108 MB: base mesh, targets, rigs with weights, poses; assets CC0). Importing it as a plain module fails (needs extension context); installing it as a Blender extension was blocked by the session's permission policy and needs Sean's OK.
* Blender.org asset bundles and files.makehumancommunity.org are unreachable; raw.githubusercontent.com works.
* Single image to 3D (CharacterGen, StdGEN, TripoSR) needs a GPU and is generative (anatomy risk); not used.
