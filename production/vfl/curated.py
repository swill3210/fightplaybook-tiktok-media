"""Curated library entries: Sean's examples, the Claude era, Grok's TikTok audit and the legacy episode QA reports.

Each entry cites its source. Images are attached only when the exact evidence exists on disk; otherwise the entry says
"no image preserved". Classifications marked PRELIMINARY are confirmed or corrected by the combat-anatomy-specialist
run recorded in the certification log.
"""
from pathlib import Path
import vfl_lib as L

EXP = Path("/home/user/claude-export/CLAUDE-EXPORT")
SRC = Path("/tmp/claude-0/vfl_src")
STILLS = Path("/home/user/the-fight-playbook-claude-handoff/VIDEO-PROJECTS/target-the-liver-in-boxing/edit/stills")
AUD = Path("/home/user/fightplaybook-tiktok-media/production/audit/evidence")
VAULT_CP = L.VAULT / "Claude Production"
ML = VAULT_CP / "Combat Anatomy/Motion Library"
BAKE = VAULT_CP / "02 Research/Image Model Bakeoff"

LIVER3 = "Liver long form v3 (Claude, final cut awaiting Sean)"
ALL_V3_APPROVERS = ["Grok v4 QA (0 defects)", "Claude revision 2 audit (51 strike stills)", "Claude 5 pass QC v2 and v3",
                    "visual-creative-director round 3 APPROVE"]


def rb(p):
    p = Path(p)
    return p.read_bytes() if p.exists() else None


def extra(b, iid, files):
    """attach additional evidence images (screenshot, source still) to an instance"""
    out = []
    for label, p in files:
        if p and Path(p).exists():
            dest = L.normalise(Path(p), L.EVID / iid / f"{label}.jpg")
            out.append({"label": label, "path": L.rel(dest), "provenance": str(p).replace("/home/user/", "")})
    b.reg["instances"][iid]["extra_evidence"] = out


def add_all(b):
    # ---------------- Sean's four examples (2026-11-24, liver v3 final cut) ----------------
    sean = [
        ("1:26", "V71", "V71_r3", "v3_86.0.jpg", "sean_1m26.png", ["VFC-F03", "VFC-G01", "VFC-B05"],
         "Glove buried under the opponent's tank top",
         "The hero's rising glove and wrist disappear under the opponent's red tank top: the fabric is drawn pulled down over the glove instead of the glove compressing the body on top of the shirt. The opponent's left arm is stretched straight out and leaves the frame at mid height on the right edge, so there is no guard and a limb is cut by the side edge."),
        ("1:35", "V79", "V72_r3 cropped 1.4x (Claude)", "v3_95.3.jpg", "sean_1m35.png", ["VFC-F03", "VFC-I02", "VFC-A06", "VFC-G03"],
         "Glove buried under the shirt; ELBOW ON HIP label with no elbow visible",
         "Claude's 1.4x crop of Grok's V72 (logged as a 'verified shovel'). The glove again disappears under the opponent's tank top. The amber label ELBOW ON HIP and its arrow point at the forearm while the hero's elbow is cropped out of frame, so the label is not true of the picture. The opponent's raised right arm passes behind the hero's head so the fist reads as sprouting from the hero's head (limb ownership unclear). The spec for this beat is a shovel into the BAG; the picture shows the opponent."),
        ("1:36", "V80", "V80_r3", "v3_97.1.jpg", "sean_1m36.png", ["VFC-A02", "VFC-A07", "VFC-D01"],
         "Arm attached to a headless, shapeless body mass",
         "Bag close up: the punching arm grows out of an oversized rounded mass (a giant deltoid with a shirt fragment); no head, neck or readable torso. Upper arm and forearm merge into one curved shape, so the arm does not trace to a believable body. This still had already been regenerated once for a fingered glove (V80_r2) and was then passed by every QC worker."),
        ("1:48", "V89", "V89_r5", "v3_108.4.jpg", "sean_1m48.png", ["VFC-C05", "VFC-F04", "VFC-F03", "VFC-G01"],
         "Eye on the back of the head; spiral impact swirl; gloves cut by the top edge",
         "The hero is seen from behind (back of the shirt and shorts toward camera) but an eye is drawn on the camera side of his head, which is anatomically impossible for that body orientation. The punch is drawn with a spiral swirl in the shirt, an effect R11 forbids (speed lines only), and the glove sinks into the swirl instead of compressing the ribs. Both of the opponent's gloves are cut by the top edge and his head touches it."),
    ]
    for t, shot, still, frame, shot_img, cls, title, expl in sean:
        stem = still.split()[0]
        iid = b.add(key=f"sean.v3.{shot}", classes=cls, title=title, project=LIVER3, shot=shot, time=t, version="liver_v3_final.mp4",
                    source="Sean's screenshots 2026-11-24 (IMG_0960 to IMG_0963); CLAUDE-EXPORT/FINAL-CUT/liver_v3_final.mp4",
                    detected_by="Sean", approved_by=ALL_V3_APPROVERS,
                    explanation=expl + " Classification: Claude PRELIMINARY, confirmed by the combat-anatomy-specialist run in the certification log.",
                    original=rb(SRC / frame), original_prov=f"liver_v3_final.mp4 frame at {frame[3:-4]} s (1920x1080)",
                    corrected=None, corrected_status="OPEN: not yet corrected; replacement must pass the library gate",
                    severity="critical", status="open", date="2026-11-24")
        extra(b, iid, [("sean_screenshot", SRC / shot_img), ("source_still", STILLS / f"{stem}.png")])

    # ---------------- Claude era (vault notes, CLAUDE-EXPORT reports) ----------------
    v3f = "CLAUDE-EXPORT/FINAL-CUT/qa_report_v2.md and vault 07 Videos liver v2/v3 notes"
    claude = [
        ("liv2.V21", ["VFC-B06"], "Redraw drew a knee strike instead of a punch", "V21", "0:24.5", "Claude 5 pass QC (pass 1)", []),
        ("liv2.V33", ["VFC-E01"], "Redraw gave the opponent a mouth", "V33", "0:38.2", "Claude 5 pass QC (pass 1)", []),
        ("liv2.V34", ["VFC-E06"], "Both redraws leaked the 3D mannequin look into the 2D style", "V34", "0:39.1", "Claude 5 pass QC (pass 1)", []),
        ("liv2.V24a", ["VFC-B05"], "First shovel edit dropped the rear glove to the waist (no guard)", "V24", "0:27.5", "Claude 5 pass QC (pass 1)", []),
        ("liv2.V24b", ["VFC-F01"], "One V24 shovel generation landed at the neck", "V24", "0:27.5", "Claude combat accuracy pass", []),
        ("liv2.V84", ["VFC-B01"], "Redrawn hook with an open elbow of about 115 to 120 degrees", "V84", "1:40", "Claude combat accuracy pass", []),
        ("liv2.V94", ["VFC-B01"], "Redrawn hook with an open elbow of about 115 to 120 degrees", "V94", "1:53", "Claude combat accuracy pass", []),
        ("liv2.V2", ["VFC-B01"], "Redrawn close up hook came out straight", "V2", "0:00", "Claude combat accuracy pass", []),
        ("liv2.V79bag", ["VFC-B03"], "Two bag shovel versions rejected: one straight, one forearm at about 50 degrees", "V79", "1:34.9", "Claude combat accuracy pass", []),
        ("liv2.V71edge", ["VFC-G01"], "Opponent's extended arm leaves through the right frame edge (noted, not fixed: 'pre-existing Grok framing')", "V71", "1:25.6", "Claude 5 pass QC (noted only)", ["Claude 5 pass QC (logged as NOTE, shipped)"]),
        ("liv2.stale", ["VFC-H03"], "Stale render from a stopped process showed the old V79 bag still and label", "V79", "1:34.9", "Claude final playback pass", []),
        ("liv2.flash", ["VFC-H03", "VFC-F04"], "Freeze flash fired during the whip pan blur and washed out a frame", "", "1:23.5 and 1:03.3", "Claude final playback pass", []),
        ("liv2.reps", ["VFC-I02"], "Dose counter showed '1 REPS' for 2 frames while counting up", "", "1:35.0", "Claude final playback pass", []),
        ("liv2.empty", ["VFC-H02"], "About 10 empty sage frames at 2:03 (push transition before the summary board draws)", "", "2:03", "visual-creative-director (round 1)", ["Claude 5 pass QC (frame was on its review sheet)"]),
        ("liv2.heads", ["VFC-G02"], "Headlines covering heads", "", "0:29.5 and 1:49", "visual-creative-director (round 1)", ["Claude 5 pass QC"]),
        ("liv2.whiteflash", ["VFC-F04"], "White flash on contact (conflicts with R11)", "", "", "visual-creative-director (round 1)", ["Claude 5 pass QC"]),
        ("liv2.echo", ["VFC-I02"], "About 36 chips repeating the narration word for word, one treatment", "", "", "visual-creative-director (round 1)", ["Claude 5 pass QC"]),
        ("liv3.cta", ["VFC-G02"], "CTA buttons over the hero's face on the subscribe shot", "V107", "", "visual-creative-director (round 2)", ["Claude 5 pass QC"]),
        ("liv3.chips", ["VFC-G02", "VFC-H01"], "Bottom left chips sitting on the progress bar labels", "", "", "visual-creative-director (round 2)", ["Claude 5 pass QC"]),
        ("liv1.dose", ["VFC-I02"], "Door 1 dose badge leaking into Door 2 and the board; mantra on the wrong word; '1 ROUNDS'; a 5 word dose line", "", "", "Claude v1 QC", []),
        ("liv1.static", ["VFC-H02"], "Static board and CTA (push ins added)", "", "", "Claude v1 QC", []),
    ]
    for key, cls, txt, shot, t, det, appr in claude:
        b.add(key=f"claude.{key}", classes=cls, title=txt[:90], project="Liver long form (Claude v1 to v3)", shot=shot, time=t, version="Claude v1 to v3",
              source=v3f, detected_by=det, approved_by=appr, explanation=txt + ". No image preserved (intermediate files were not exported).",
              corrected_status="fixed in a later build (see the build notes)", date="2026-11-24", test_eligible=False)
    for key, t, frame, txt in [("could.combo", "1:49.0", "v3_109.0.jpg", "Combo chips overlap the opponent's chest for about 0.25 s (left as a 'could' item)"),
                               ("could.onetarget", "1:49.5", "v3_109.5.jpg", "ONE TARGET headline about 20 px over the raised glove (left as a 'could' item)")]:
        b.add(key=f"claude.{key}", classes=["VFC-G02"], title=txt[:90], project=LIVER3, shot="V90", time=t, version="liver_v3_final.mp4",
              source="vault 07 Videos/2026-11-24 Liver long form v3 build.md", detected_by="visual-creative-director (round 3, could)",
              approved_by=["visual-creative-director round 3 APPROVE (shipped it)"], explanation=txt + ". Under the library every known overlay collision blocks delivery.",
              original=rb(SRC / frame), original_prov=f"liver_v3_final.mp4 frame at {t}", status="open", corrected_status="OPEN", date="2026-11-24", test_eligible=False)

    # rig and method failures (images: motion library sheets, bake-off sheets)
    rig = [
        ("guard", ["VFC-B05"], "Rig guard: hero elbows flared to shoulder height (lead elbow 0.01 x torso below the shoulder)", ML / "guard.jpg"),
        ("jab", ["VFC-B05", "VFC-B08"], "Rig jab: rear elbow flared, chamber and recover on the flared guard (punching arm itself correct)", ML / "jab.jpg"),
        ("cross", ["VFC-B08", "VFC-B05"], "Rig cross: 'chamber' sampled at 96 percent extension, lead elbow flared", ML / "cross.jpg"),
        ("lead_body_hook", ["VFC-B08", "VFC-G03"], "Rig body hook: chamber already at the target, recover stays at the target, rightside camera hides the arm", ML / "lead_body_hook.jpg"),
        ("shovel_uppercut", ["VFC-B03", "VFC-A06"], "Rig shovel: glove at the hero's own face at impact, elbow off the hip, heads and torsos interpenetrate", ML / "shovel_uppercut.jpg"),
        ("arm_punch_mistake", ["VFC-B08"], "Rig 'arm punch mistake' demo: phases inverted (chamber extended, impact bent)", ML / "arm_punch_mistake.jpg"),
    ]
    for key, cls, txt, img in rig:
        b.add(key=f"rig.motionlib.{key}", classes=cls, title=txt[:90], project="Claude 3D rig motion library v1", version="motionlib v1",
              source="vault Combat Anatomy/02 Rejections Log.md and Motion Library/manifest.json", detected_by="combat-anatomy-specialist",
              approved_by=["engine qc.py rig metrics (passed all 96 stills)", "validate.py reference match"],
              explanation=txt + ".", original=rb(img), original_prov=str(img).replace(str(L.VAULT) + "/", "vault "),
              corrected_status="OPEN: motion library v2 not built", status="open", date="2026-11-24")
    b.add(key="rig.inbetween", classes=["VFC-H04"], title="86 of 528 in between frames: gloves in heads, elbows in torsos, glove clashes",
          project="Claude 3D rig motion library v1", source="Knowledge Base/08 Mistakes and Lessons Learned.md (2026-11-24)", detected_by="Claude per frame animation QC",
          approved_by=["rig key pose metrics (96 of 96 passed)"], explanation="Key poses passed while the frames between them interpenetrated. No image preserved.",
          corrected_status="OPEN", status="open", date="2026-11-24", test_eligible=False)
    for key, cls, txt in [("glow", ["VFC-E06"], "Emissive highlight glow recoloured the rig costume"),
                          ("profile", ["VFC-G03"], "Profile views of the faceless head read as the back of the head"),
                          ("snapback", ["VFC-H04"], "Rear glove passed through the face on the snap back"),
                          ("shorts_outfit", ["VFC-E02"], "Shorts sample built in the long form black shirt instead of the gray tank")]:
        b.add(key=f"rig.{key}", classes=cls, title=txt, project="Claude 3D rig (punch_with_body)", source="Knowledge Base/08 Mistakes and Lessons Learned.md (2026-11-23)",
              detected_by="Claude rig QC", explanation=txt + ". Fixed in the rig. No image preserved.", corrected_status="fixed in code", date="2026-11-23", test_eligible=False)
    for i in range(1, 5):
        b.add(key=f"bakeoff.S0{i}", classes=["VFC-B01"], title=f"Image model bake-off sheet S0{i}: lead body hook drawn as a near straight arm",
              project="Image model bake-off (Claude)", source="vault 02 Research/Image Model Bakeoff", detected_by="Claude bake-off review",
              explanation="Every model (Nano Banana 2 and Pro, GPT Image 2, with or without a mannequin pose guide) drew the lead BODY HOOK as a near straight arm when prompted by text.",
              original=rb(BAKE / f"2026-11-24 sheet S0{i}.jpg"), original_prov=f"vault Image Model Bakeoff/2026-11-24 sheet S0{i}.jpg (contact sheet, several models)",
              corrected_status="method fix: rig pose passed first with REDRAW THE FIRST IMAGE", date="2026-11-24", test_eligible=False)
    b.add(key="bakeoff.openpose", classes=["VFC-E04"], title="Raw OpenPose skeleton passed to the image model leaked in as ghost figures",
          project="Image model bake-off (Claude)", source="Knowledge Base/07 Quality Control.md", detected_by="Claude bake-off review",
          explanation="Never pass stick skeletons to image models. No image preserved.", corrected_status="rule added", date="2026-11-24", test_eligible=False)

    # ---------------- Grok TikTok and Shorts audit (Claude, 2026-11-23) ----------------
    ga = "fightplaybook-tiktok-media production/audit/GROK_AUDIT.md"
    tik = [
        ("snapback", ["VFC-I01"], "punch_with_body 14.0 to 15.4 s: 'Snap it back to your guard' while the arm stays fully extended", AUD / "snap_back_mismatch.jpg"),
        ("handsup", ["VFC-I01"], "check_a_low_kick ~4 s: 'Hands stay up' while the hero's hands are at the waist", AUD / "check_a_low_kick_illus_tiktok.jpg"),
        ("whochecks", ["VFC-C04"], "check_a_low_kick ~6 s: 'Step one' (checking) but the opponent lifts the knee, not the hero", AUD / "check_a_low_kick_illus_tiktok.jpg"),
        ("kneeknee", ["VFC-B07"], "check_a_low_kick ~13 s: 'Meet their shin' shows knee against knee, no shin contact", AUD / "low_kick_errors.jpg"),
        ("nofeet", ["VFC-D02", "VFC-B07"], "check_a_low_kick 'step three' and 'plant back': both feet off the ground, no planted leg; kicking shin passes through the hero's leg", AUD / "low_kick_errors.jpg"),
        ("overhead", ["VFC-B09", "VFC-C02"], "want_to_drop_someone_fast: opponent throws both hands straight overhead as a reaction to a jab; fighters swap screen sides between shots", AUD / "want_to_drop_someone_fast_illus_tiktok.jpg"),
        ("gloves", ["VFC-E02", "VFC-E05"], "punch_with_body: boxing gloves (hit_harder uses MMA gloves); opponent same size as the hero and switching red and grey tanks", AUD / "punch_with_body_illus_tiktok.jpg"),
        ("glovetype2", ["VFC-E02"], "hit_harder: MMA gloves while punch_with_body uses boxing gloves (glove type drift across videos)", AUD / "hit_harder_cover_tiktok.jpg"),
        ("shoulders", ["VFC-I02"], "Caption bar drops the word 'shoulders' ('TURN THE HIPS AND' then 'THROUGH THE PUNCH')", AUD / "missing_word_shoulders.jpg"),
    ]
    for key, cls, txt, img in tik:
        b.add(key=f"tiktok.{key}", classes=cls, title=txt[:90], project="Grok TikTok cuts (published)", source=ga, detected_by="Claude audit of Grok's TikToks",
              approved_by=["Grok TikTok QA (published)"], explanation=txt + ". Evidence image is the audit contact sheet for that video.",
              original=rb(img), original_prov="production/audit/evidence/" + img.name, corrected_status="not corrected (already published)", status="open",
              date="2026-11-23", test_eligible=False)
    for key, cls, txt in [("echo", ["VFC-I02"], "Big headline repeats the caption bar word for word"),
                          ("chunks", ["VFC-I02"], "Caption chunks break mid phrase ('KEEP YOUR SHOULDERS AND')"),
                          ("deadair", ["VFC-H02"], "punch_with_body 16.5 to 18.0 s: 1.5 s voice pause over a near static frame"),
                          ("nomotion", ["VFC-B08"], "Punches are never shown travelling, retracting or turning the hips (stills only)")]:
        b.add(key=f"tiktok.{key}", classes=cls, title=txt, project="Grok TikTok cuts (published)", source=ga, detected_by="Claude audit of Grok's TikToks",
              approved_by=["Grok TikTok QA (published)"], explanation=txt + ".", corrected_status="not corrected", status="open", date="2026-11-23", test_eligible=False)

    # ---------------- Grok legacy episodes and other long forms (text only) ----------------
    H = "handoff VIDEO-PROJECTS/"
    legacy = [
        ("ep01.uppercut", ["VFC-B03"], "Uppercut mostly extended, reads as a rising straight under the chin (waived by Sean 2026-11-11)", "ep01_taller_opponent/qa_report.md", "Grok QA"),
        ("ep01.thirdfig", ["VFC-E04"], "A dedicated pinned generation grew a third figure", "ep01_taller_opponent/qa_report.md", "Grok QA"),
        ("ep01v3.l3card", ["VFC-G01"], "Level 3 card crop clips the head at the top of the panel", "ep01_v3/qa_report.md", "Grok QA"),
        ("ep02.titlecard", ["VFC-G01"], "Section 1 title card: incoming punch and opponent sliver cropped at the right edge", "ep02_stop_flinching/qa_report.md", "Grok QA"),
        ("ep03.overlays", ["VFC-G02"], "A09 arrow crossed the heads; B12/B13 cue cards and B39 card covered a head", "ep03_stronger_opponent/qa_report_v2.md", "Grok QA"),
        ("ep06.overlays", ["VFC-H01"], "Misplaced overlays: heel arrow on the planted foot, X in empty space, X on a thigh, heel glow between the feet", "ep06_punching_power/qa_report_v2.md", "Grok QA"),
        ("ep07.tail", ["VFC-H03"], "Concat render dropped the last 1.6 s (cut 'for the next one')", "ep07_beat_trained_fighter/qa_report_v2.md", "Grok QA"),
        ("ep08.overlays", ["VFC-G02", "VFC-H01"], "Thought cloud over the shorts, loading ring on the chest, cards on the stranger's head, arrow crossing a label", "ep08_why_you_freeze/qa_report.md", "Grok QA"),
        ("ep09.liverside", ["VFC-C03"], "Liver target drawn on the wrong side; chin and solar targets misplaced; garbled skull title", "ep09_knock_out_anyone/qa_report.md", "Grok QA"),
        ("ep12.threefig", ["VFC-E04"], "Two attempts at 'pull him close' came out with three figures", "ep12_chokehold_escape/qa_report.md", "Grok QA"),
        ("ep13.slip", ["VFC-F02"], "Slip still: fist and burst in front of the face read as a hit, not a miss", "ep13_never_get_hit/qa_report.md", "Grok QA"),
        ("ep14.burst", ["VFC-F04"], "White burst at the contact point on kicks (4 burst removals in v2)", "ep14_kick_higher/qa_report.md", "Grok QA"),
        ("ep15.neck", ["VFC-F01"], "Sean: the punches looked like they hit the neck; contact near the ear; glove partly on the neck", "ep15_knockout_any_size/qa_report_v2.md", "Sean"),
        ("ep15.straight", ["VFC-B01"], "Hook stills came out as straights (side hook v1, v2, drill hook v1, v2)", "ep15_knockout_any_size/qa_report.md", "Grok QA"),
        ("ep15.profile", ["VFC-E01", "VFC-F04"], "Gemini hook drawn with a facial profile and extra effects", "ep15_knockout_any_size/qa_report.md", "Grok QA"),
        ("ep15.glow", ["VFC-H01"], "Red chin glow sat on the top of the head", "ep15_knockout_any_size/qa_report.md", "Grok QA"),
        ("ep15.disconnected", ["VFC-D01"], "Edit from the wrong base: arm looked disconnected", "ep15_knockout_any_size/qa_report_v2.md", "Grok QA"),
        ("ep17.neck", ["VFC-F01"], "Jab and rear straight landed at or near the neck; lead hook behind the jaw on the neck; chest jab on the shoulder", "ep17_beat_each_stance/qa_report.md", "Grok QA"),
        ("ep18.neck", ["VFC-F01", "VFC-B07"], "Hook on the upper neck; knee into the groin then the waistband; frame glove at the base of the neck", "ep18_beat_each_range/qa_report.md", "Grok QA"),
        ("ep18.lines", ["VFC-H06"], "Zoom mapping bug drew stray speed lines above the heads", "ep18_beat_each_range/qa_report.md", "Grok QA"),
        ("ep19.narr", ["VFC-I01"], "Fists on top of the head instead of palms on the forehead; deep squat contradicts 'sit down a little'; OTS hook aimed high at the head", "ep19_take_a_punch/qa_report_v2.md", "Grok QA"),
        ("ep19.fig", ["VFC-E04"], "Front chin still had a confusing second figure facing away", "ep19_take_a_punch/qa_report_v2.md", "Grok QA"),
        ("ep19.streak", ["VFC-H06"], "Faint vertical sky streaks above zoomed out and split shots, edge streak on the thumbnail", "ep19_take_a_punch/qa_report_v2.md", "Grok QA"),
        ("ep20.slip", ["VFC-F02"], "Outside slip: fist sat in front of the forehead instead of passing the head", "ep20_dodge_any_punch/qa_report.md", "Grok QA"),
        ("ep21.throat", ["VFC-F01"], "Straight landed under the chin near the throat; OTS straight on the throat; overhead hooks on the cheek or ear", "ep21_fists_like_a_train/qa_report.md", "Grok QA"),
        ("ep23.feet", ["VFC-I01", "VFC-E05"], "Feet trap stills unclear (foot beside the leg, not hooked); opponent proportions wrong in a get up still", "ep23_fight_on_the_ground/qa_report.md", "Grok QA"),
        ("grip.eye", ["VFC-G01"], "V6 crops a sliver of the hero's eye at the top left", "grip_strength/edit/qa/qa_report.md", "Grok QA"),
        ("grip.arm", ["VFC-A04"], "R4 and R5: right arm drawn backwards (thumb and chest on the wrong side)", "grip_strength/edit/qa_v3/qa_report.md", "Grok QA"),
        ("grip.torso", ["VFC-G01"], "Torso cropped at the left edge, floating mid frame", "grip_strength/edit/qa_v2/qa_report.md", "Grok QA"),
        ("guard.teal", ["VFC-H01"], "Renderer background detection turned close up figures teal", "guard-that-actually-works/edit/qa/qa_report.md", "Grok QA"),
        ("guard.detached", ["VFC-D01"], "V5 redraw left the opponent's arm detached from his shoulder", "guard-that-actually-works/edit/qa/qa_report.md", "Grok QA"),
        ("clinch.bar", ["VFC-B06"], "Forearm bar drawn as a straight arm or collar tie in five tries; shipped reading like a forearm across the neck", "clinch-escape/edit/qa/qa_report.md", "Grok QA"),
        ("punchharder.edge", ["VFC-G01", "VFC-F02"], "V8 punching arm enters from the left edge at mid height; gloves only lightly squashed", "punch-harder-without-swinging-harder/edit/qa/qa_report.md", "Grok QA"),
        ("openguard.placeholders", ["VFC-H05"], "13 shots filled with crops of other stills; V29 'uppercut' placeholder shows a cross; V30 money moment a placeholder zoom", "open-any-guard-body-punches/edit/qa/qa_report.md", "Grok QA"),
        ("openguard.123", ["VFC-I01"], "V39 should show 1, then 2, then 3 fingers; only V39c shows three", "open-any-guard-body-punches/edit/qa/qa_report.md", "Grok QA"),
        ("guardv1.watermark", ["VFC-H05"], "Placeholder watermark on 29 percent of Guard v1", "LESSONS-LEARNED.md / SKILL-VB rationale", "Sean"),
        ("cardio.solo", ["VFC-E04"], "Second character (and a red tank opponent) in a solo cardio video", "SCRIPTS/build-superhuman-cardio-v2/v3_fix_list_sean.md", "Sean"),
        ("cardio.sprint", ["VFC-I01"], "A sprint at 0:02 inside the 'gassed' hook; guard up stance at 0:05 contradicts the beat", "SCRIPTS/build-superhuman-cardio-v2/v3_fix_list_sean.md", "Sean"),
        ("liver.V56", ["VFC-H01"], "Mistake border at full strength on frame 0 (alpha drawn into an RGBA frame)", "target-the-liver-in-boxing/edit/qa/v2/anatomy_qa_v2.md", "Grok QA"),
        ("liver.V64", ["VFC-G02"], "SHOVEL UPPERCUT headline under the door tracker", "target-the-liver-in-boxing/edit/qa/v2/anatomy_qa_v2.md", "Grok QA"),
        ("liver.V53speckle", ["VFC-E03", "VFC-H01"], "Colour cleanup speckled V53's red shirt with charcoal", "QUALITY-CONTROL/target-the-liver-in-boxing/v4/hook_qa_v4.md", "Grok QA"),
        ("liver.shorts", ["VFC-E02"], "Opponent shorts drifting navy (V1_r1); skin drifting tan", "edit/qa/still_qa_pass2.md, LESSONS-LEARNED.md", "Grok QA"),
        ("legacy.threearm", ["VFC-A01"], "Three arm opponent", "LESSONS-LEARNED.md / SKILL-VB rationale", "Sean"),
        ("legacy.funpunch", ["VFC-F02"], "FunPunch punches not connecting", "LESSONS-LEARNED.md / SKILL-VB rationale", "Sean"),
    ]
    for key, cls, txt, src, det in legacy:
        b.add(key=f"grok.{key}", classes=cls, title=txt[:90], project=src.split("/")[0], source=H + src if "/" in src and not src.startswith(("LESSONS", "SCRIPTS", "QUALITY")) else "handoff " + src,
              detected_by=det, explanation=txt + ". No image preserved in the export.", corrected_status="fixed or noted in that report",
              date="2026-11-11 to 2026-11-23", test_eligible=False)
