# Combat anatomy gate (automated half)

`validate.py` runs whole body pose estimation on CPU (rtmlib + onnxruntime) and checks person count, hero and opponent identity colours, limb visibility and proportions, torso left/right consistency, the technique signature and, most importantly, the match against the 3D rig skeleton from the same camera (`render.mjs --still` writes `still_<t>.json` with COCO 17 keypoints). The combat-anatomy-specialist subagent must still inspect every asset; a pass here is never proof.

Calibration (2026-11-24): approved rig based redraws 0.13 to 0.22 x torso mean error, Grok's defective stills 0.26 to 0.47; bands PASS < 0.20, UNCERTAIN 0.20 to 0.26, FAIL >= 0.26. Without a rig reference, technique accuracy is always UNCERTAIN (a known straight arm hook passed every 2D check). Unreliable views: overhead, low (false leg FAILs), rear three quarter when legs are hidden.

Licence: the default rtmlib weights (RTMW / DWPose, YOLOX Human-Art) are trained on non-commercial datasets. See vault conflict C15 before production use.

Setup: `pip install onnxruntime==1.20.1 rtmlib==0.0.16 opencv-python-headless`; weights download from download.openmmlab.com (allowed in the Fight Playbook environment).
`method_test.py` runs the A (text to image) vs B (rig pose redraw) comparison through ElevenLabs.
