// Fight Playbook render engine: deterministic frame renderer driven by a storyboard.
// window.FP.render(t) draws frame at video time t and returns QC metrics for that frame.
import * as THREE from 'three';
import { Fighter } from './rig.js';
import { MOVES, stance, applyCross, applyJab, applyHook, applyShovel, impulse, foldCurve, applyReaction, headYawTo } from './motion.js';
const APPLY = { cross_body: applyCross, cross_arm: applyCross, jab_high: applyJab, hook_body: applyHook, tap_ribs: applyHook, shovel_up: applyShovel };

const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
let W = 1080, H = 1920;

export class Engine {
  constructor(board) {
    this.board = board;
    W = board.width || 1080; H = board.height || 1920;
    const bg = new THREE.Color(board.style.bg);
    this.gl = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    this.gl.setPixelRatio(1); this.gl.setSize(W, H);
    this.gl.shadowMap.enabled = true; this.gl.shadowMap.type = THREE.PCFSoftShadowMap;
    this.gl.outputColorSpace = THREE.SRGBColorSpace;
    this.scene = new THREE.Scene();
    this.scene.background = bg;
    // floor: a shade darker than the backdrop so a clean ground line reads in every standing shot
    // R10: flat solid background. The floor is invisible except for the contact shadows that ground the feet.
    const floorCol = bg.clone().multiplyScalar(0.9);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ color: 0x1c2640, opacity: 0.28 }));
    floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; this.scene.add(floor);
    this.scene.add(new THREE.HemisphereLight(0xffffff, floorCol, 1.6));
    const key = new THREE.DirectionalLight(0xffffff, 2.2);
    key.position.set(1.5, 6, 4); key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -2.5, right: 3.5, top: 3, bottom: -2, near: 1, far: 15 });
    key.shadow.radius = 4; key.shadow.bias = -0.0008;
    this.scene.add(key);
    const rim = new THREE.DirectionalLight(0xffffff, 1.0); rim.position.set(-3, 3, -4); this.scene.add(rim);

    this.hero = new Fighter(board.style.hero); this.scene.add(this.hero.root);
    this.opp = new Fighter(board.style.opponent); this.scene.add(this.opp.root);
    this.cam = new THREE.PerspectiveCamera(35, W / H, 0.05, 60);

    // flat floor graphics (pivot arrow, arcs) live here and are rebuilt per frame
    this.fx = new THREE.Group(); this.scene.add(this.fx);

    // output canvases
    this.out = document.createElement('canvas'); this.out.width = W; this.out.height = H;
    this.ctx = this.out.getContext('2d');
    document.body.appendChild(this.out);
    this.prev = {};
    this.stage = {};
    for (const k of Object.keys(MOVES)) this.stage[k] = MOVES[k].range ?? this.fitRange(k);
    // each move is staged at its own true range; range only changes on a cut between angles
  }

  // ---------- staging: place the opponent so the punch lands with a slightly bent arm ----------
  fitRange(moveName) {
    let lo = 0.4, hi = 1.6;
    for (let i = 0; i < 22; i++) {
      const x = (lo + hi) / 2;
      const r = this.solveAt(MOVES[moveName].impact * MOVES[moveName].dur, { move: moveName, moveAt: 0, oppX: x, noReact: true });
      // reach is target distance over arm length; aim for 0.975
      const mv = MOVES[moveName];
      if (r.heroMetrics.reach['arm' + mv.hand] > mv.reach) hi = x; else lo = x;
    }
    return (lo + hi) / 2;
  }

  // ---------- solve both fighters at action time tau ----------
  solveAt(tau, s) {
    const move = s.move ? MOVES[s.move] : null;
    const oppX = s.oppX ?? ((s.move === 'shovel_up' && typeof window !== 'undefined' && window.FP_SHOV && window.FP_SHOV.oppX) || this.stage[s.move || 'cross_body']);
    const bob = (ph) => (s.still ? 0 : 0.007 * Math.sin(2 * Math.PI * 1.35 * tau + ph));
    const guardStyle = s.oppGuard || (move && move.target === 'liver' ? 'high' : 'normal');
    const oRoot = { pos: V(oppX, 0, 0.02), yaw: Math.PI };
    const oppPose = () => { const o = stance('opponent', guardStyle); o.elbowOut = 0.2; o.pelvis.y += bob(1.3); o.rootPos = oRoot.pos; o.rootYaw = oRoot.yaw; o.head.yaw = 0; return o; };

    let impactTau = null, c = { foot: 0, hips: 0, shoulders: 0, arm: 0, chamber: 0, dip: 0 };
    if (move) {
      const u = (tau - s.moveAt) / move.dur;
      c = Object.assign({ foot: 0, hips: 0, shoulders: 0, arm: 0, chamber: 0, dip: 0 }, move.ch(Math.max(-1, Math.min(2, u))));
      impactTau = s.moveAt + move.impact * move.dur;
    }
    // aim points come from the opponent before any reaction
    let OJ = this.opp.solve(oppPose());
    const fwdO = OJ.forwardW.clone();
    const aim = { chin: OJ.chinW.clone(), guard: OJ.gloveW.R.clone(), liver: OJ.liverW.clone(),
      body: OJ.pelvisW.clone().add(V(0, 0.27 * (this.opp.o.scale || 1), 0)).add(fwdO.multiplyScalar(0.13)).add(V(0, 0, -0.05)) };
    let r = 0, contact = 0;
    if (move && !s.noReact && move.reaction !== 'none') {
      const dt = tau - impactTau;
      r = move.reaction === 'fold' ? foldCurve(dt, move.power) : impulse(dt, move.power);
      contact = Math.exp(-Math.pow(dt / 0.035, 2)) * move.power;
      if (r > 0 || contact > 0) { const o = oppPose(); applyReaction(o, move.reaction, r, contact); OJ = this.opp.solve(o); }
    }

    // hero
    const P = stance('hero');
    P.pelvis.y += bob(0);
    P.rootPos = V(0, 0, 0); P.rootYaw = 0;
    if (move) (APPLY[s.move] || applyCross)(P, c);
    P.head.yaw = headYawTo(V(0, 0, 0), OJ.headW) * 0.9;
    let J = this.hero.solve(P);
    if (move) {
      const h = move.hand;
      if (move.shape === 'straight' && c.arm > 0.001) {
        const tgt = aim[move.target];
        const dir = tgt.clone().sub(J.shoulderW[h]).normalize();
        const stand = move.target === 'guard' ? 0.14 + 0.07 : 0.14 - 0.012;  // stop on the glove, sink slightly into the chin
        P.hands[h].target = tgt.clone().sub(dir.multiplyScalar(stand));
        P.hands[h].w = c.arm;
        J = this.hero.solve(P);
      } else if (move.shape === 'hook' && (c.chamber > 0.001 || c.arm > 0.001)) {
        // L shaped arm on a short curved horizontal path around the guard into the side of the ribs
        const guardW = J.wristW[h].clone();
        const chamberW = J.hipW.L.clone().add(V(0.16, 0.26, -0.12));
        const fdir = V(0.35, 0, 1).normalize();
        const hitW = aim.liver.clone().sub(fdir.clone().multiplyScalar(0.12));
        const ctrl = chamberW.clone().lerp(hitW, 0.5).add(V(-0.02, 0.03, -0.20));
        const bez = (a, b, cc, t) => a.clone().multiplyScalar((1 - t) * (1 - t)).add(cc.clone().multiplyScalar(2 * t * (1 - t))).add(b.clone().multiplyScalar(t * t));
        const p = c.arm > 0.001 ? bez(chamberW, hitW, ctrl, Math.min(1, c.arm)) : guardW.clone().lerp(chamberW, c.chamber);
        const k = Math.max(c.chamber, c.arm);
        P.hands[h].target = guardW.clone().lerp(p, Math.min(1, k * 1.5));
        P.hands[h].w = 1;
        P.elbowPole = { L: V(0, 0.8, -2.4).multiplyScalar(h === 'L' ? k : 0), R: V(0.1, 0, 0.6) };
        J = this.hero.solve(P);
      } else if (move.shape === 'uppercut' && (c.chamber > 0.001 || c.arm > 0.001)) {
        // glove chambered at the own hip, then drives UP and in, forearm near vertical, elbow tucked on the hip
        const guardW = J.wristW[h].clone();
        const chamberW = J.hipW.R.clone().add(V(0.16, 0.10, -0.06));
        const SV = (typeof window !== 'undefined' && window.FP_SHOV) || {};
        const hitW = aim.body.clone().add(V(SV.dx ?? -0.08, SV.dy ?? 0.10, SV.dz ?? 0));
        const p = c.arm > 0.001 ? chamberW.clone().lerp(hitW, Math.min(1, c.arm)) : guardW.clone().lerp(chamberW, c.chamber);
        const k = Math.max(c.chamber, c.arm);
        P.hands[h].target = p; P.hands[h].w = 1;
        P.elbowPole = { L: V(0, 0, 0), R: V(SV.px ?? 1.0, SV.py ?? -2.5, SV.pz ?? 0.4).multiplyScalar(k) };
        J = this.hero.solve(P);
      }
    }
    return { J, OJ, c, r, contact, impactTau, heroMetrics: this.hero.metrics, oppMetrics: this.opp.metrics };
  }

  shotAt(t) {
    const shots = this.board.shots;
    for (let i = 0; i < shots.length; i++) if (t >= shots[i].start && t < shots[i].end) return [shots[i], i];
    return [shots[shots.length - 1], shots.length - 1];
  }

  // ---------- render one frame ----------
  render(t) {
    const [s, idx] = this.shotAt(t);
    const tl = t - s.start, dur = s.end - s.start;
    const tau = s.clock(tl, dur);
    const st = this.solveAt(tau, s);
    let cam = s.cam(tl / dur, st, tl);
    if (window.FP_CAM) { const [az, el, dist, fov, tx, ty, tz] = window.FP_CAM; const tg = V(tx, ty, tz);
      cam = { pos: tg.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(dist)), target: tg, fov }; }
    this.cam.fov = cam.fov; this.cam.position.copy(cam.pos); this.cam.up.set(0, 1, 0);
    if (cam.up) this.cam.up.copy(cam.up);
    this.cam.lookAt(cam.target); this.cam.updateProjectionMatrix();
    this.cam.updateMatrixWorld();

    // highlights (kinetic chain) and floor fx
    this.hero.head.visible = !(s.hide || []).includes('heroHead'); this.opp.head.visible = !(s.hide || []).includes('oppHead'); this.opp.root.visible = !(s.hide || []).includes('opp');
    this.applyHighlights(s.highlight ? s.highlight(tl / dur, st, tau) : {});
    this.fx.clear();
    if (s.fx3d) s.fx3d(this.fx, st, tl / dur, tau);

    const g = this.ctx;
    const proj = (v) => { const p = v.clone().project(this.cam); return { x: (p.x + 1) / 2 * W, y: (1 - p.y) / 2 * H, z: p.z }; };
    if (window.FP_POSE) { this.drawPose(g, [st.J, st.OJ], proj); return this.qc(t, s, idx, st, proj); }
    this.gl.render(this.scene, this.cam);
    g.globalAlpha = 1; g.drawImage(this.gl.domElement, 0, 0);

    // 2D layer
    this.drawSpeedLines(g, st, proj, tau, s);
    if (s.draw2d) s.draw2d(g, st, proj, tl / dur, tau, this);
    this.drawText(g, t, s);

    return this.qc(t, s, idx, st, proj);
  }

  // COCO 17 keypoints (x, y in pixels) for both fighters, the reference the anatomy validator compares against
  coco(J, proj) {
    const up = V(0, 1, 0), fwd = J.forwardW.clone(), right = fwd.clone().cross(up).normalize();
    const nose = J.headW.clone().add(fwd.clone().multiplyScalar(0.10)).add(V(0, -0.01, 0));
    const eye = (sd) => nose.clone().add(V(0, 0.035, 0)).add(right.clone().multiplyScalar(sd * 0.035));
    const ear = (sd) => J.headW.clone().add(right.clone().multiplyScalar(sd * 0.09));
    return [nose, eye(-1), eye(1), ear(-1), ear(1), J.shoulderW.L, J.shoulderW.R, J.elbowW.L, J.elbowW.R, J.wristW.L, J.wristW.R,
      J.hipW.L, J.hipW.R, J.kneeW.L, J.kneeW.R, J.ankleW.L, J.ankleW.R].map(proj).map((p) => [+p.x.toFixed(1), +p.y.toFixed(1)]);
  }

  // OpenPose COCO 18 skeleton (black background, standard limb colours) for ControlNet / pose conditioning
  drawPose(g, fighters, proj) {
    g.fillStyle = '#000'; g.fillRect(0, 0, W, H);
    const COL = [[255,0,0],[255,85,0],[255,170,0],[255,255,0],[170,255,0],[85,255,0],[0,255,0],[0,255,85],[0,255,170],[0,255,255],[0,170,255],[0,85,255],[0,0,255],[85,0,255],[170,0,255],[255,0,255],[255,0,170],[255,0,85]];
    const PAIRS = [[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[1,0],[0,14],[14,16],[0,15],[15,17]];
    const sc = H / 1080;
    for (const J of fighters) {
      const up = V(0, 1, 0), fwd = J.forwardW.clone(), right = fwd.clone().cross(up).normalize();
      const nose = J.headW.clone().add(fwd.clone().multiplyScalar(0.10)).add(V(0, -0.01, 0));
      const k = [nose, J.shoulderW.L.clone().lerp(J.shoulderW.R, 0.5).add(V(0, 0.02, 0)),
        J.shoulderW.R, J.elbowW.R, J.wristW.R, J.shoulderW.L, J.elbowW.L, J.wristW.L,
        J.hipW.R, J.kneeW.R, J.ankleW.R, J.hipW.L, J.kneeW.L, J.ankleW.L,
        nose.clone().add(V(0, 0.035, 0)).add(right.clone().multiplyScalar(0.035)), nose.clone().add(V(0, 0.035, 0)).add(right.clone().multiplyScalar(-0.035)),
        J.headW.clone().add(right.clone().multiplyScalar(0.09)), J.headW.clone().add(right.clone().multiplyScalar(-0.09))].map(proj);
      PAIRS.forEach(([a, b], i) => {
        const A = k[a], B = k[b]; const mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2;
        const len = Math.hypot(A.x - B.x, A.y - B.y) / 2, ang = Math.atan2(B.y - A.y, B.x - A.x);
        g.save(); g.globalAlpha = 0.6; g.fillStyle = `rgb(${COL[i].join(',')})`;
        g.beginPath(); g.ellipse(mx, my, len, 4 * sc, ang, 0, Math.PI * 2); g.fill(); g.restore();
      });
      k.forEach((p, i) => { g.fillStyle = `rgb(${COL[i].join(',')})`; g.beginPath(); g.arc(p.x, p.y, 4 * sc, 0, Math.PI * 2); g.fill(); });
    }
  }

  applyHighlights(h) {
    const groups = {
      foot: ['footR', 'shinR', 'kneeR'],
      hips: ['pelvis', 'thighR', 'thighL', 'shortR', 'shortL'],
      shoulders: ['torso', 'chest', 'deltR', 'deltL'],
      arm: ['upperR', 'foreR', 'elbowR', 'gloveR'],
    };
    const hero = this.hero;
    if (!hero._hl) {
      hero._hl = {};
      for (const [k, names] of Object.entries(groups)) {
        hero._hl[k] = [];
        for (const n of names) {
          const part = hero.parts[n]; if (!part) continue;
          part.traverse((m) => {
            if (m.isMesh && m.material && m.material.isShaderMaterial && m.material.uniforms.col) {
              m.material.userData.w0 = m.material.userData.w0 ?? m.material.uniforms.w.value;
              hero._hl[k].push(m.material);
            }
          });
        }
      }
    }
    const dark = new THREE.Color(0x0b0c12), amber = new THREE.Color(0xffb000);
    for (const k of Object.keys(groups)) {
      const a = h[k] || 0;
      // highlight = thick amber outline, so the costume colours never change
      for (const mat of hero._hl[k]) {
        mat.uniforms.col.value.copy(dark).lerp(amber, Math.min(1, a * 1.4));
        mat.uniforms.w.value = mat.userData.w0 * (1 + 1.6 * a);
      }
    }
  }

  // speed lines: the only strike effect, drawn behind a fast moving punching glove
  drawSpeedLines(g, st, proj, tau, s) {
    if (s.noSpeedLines) return;
    const key = 'gR';
    const now = st.J.gloveW.R.clone();
    const prevTau = this._prevTau;
    let vel = 0;
    // estimate glove speed with a second solve slightly earlier in action time
    const dt = 1 / 120;
    const back = this.solveAt(tau - dt, s);
    const pv = back.J.gloveW.R;
    vel = now.distanceTo(pv) / dt; // m/s in action time
    // re-solve current state so the scene graph matches this frame again
    this.solveAt(tau, s);
    if (vel < 2.2 || st.c.arm <= 0.3) return;
    const a = proj(now), b = proj(pv);
    let dx = a.x - b.x, dy = a.y - b.y; const L = Math.hypot(dx, dy); if (L < 0.5) return;
    dx /= L; dy /= L;
    const nx = -dy, ny = dx;
    const strength = Math.min(1, (vel - 2.2) / 4);
    const scale = Math.abs(proj(now.clone().add(V(0, 0.1, 0))).y - a.y) * 10; // pixels per meter
    g.save(); g.lineCap = 'round';
    const lines = [[-0.9, 1.0], [-0.45, 1.6], [0, 1.25], [0.45, 1.8], [0.9, 1.1]];
    for (const [o, len] of lines) {
      const r = scale * 0.075;
      const sx = a.x - dx * scale * 0.11 + nx * o * r, sy = a.y - dy * scale * 0.11 + ny * o * r;
      const l = scale * 0.22 * len * strength;
      g.strokeStyle = `rgba(0,0,0,${0.85 * strength})`; g.lineWidth = Math.max(3, scale * 0.006);
      g.beginPath(); g.moveTo(sx, sy); g.lineTo(sx - dx * l, sy - dy * l); g.stroke();
    }
    g.restore();
    this._speed = vel;
  }

  // ---------- typography ----------
  drawText(g, t, s) {
    const B = this.board;
    // top centre big text, max 3 words, white with dark outline
    if (s.top) {
      const words = s.top.text;
      const tl = t - s.start;
      const pop = Math.min(1, tl / 0.12);
      const sc = 0.86 + 0.14 * (1 - Math.pow(1 - pop, 3));
      g.save(); g.translate(W / 2, 330); g.scale(sc, sc);
      g.font = '150px "Bebas Neue"'; g.textAlign = 'center'; g.textBaseline = 'middle';
      g.lineJoin = 'round';
      const lines = Array.isArray(words) ? words : [words];
      lines.forEach((ln, i) => {
        const y = i * 140;
        g.lineWidth = 22; g.strokeStyle = '#141a2e'; g.strokeText(ln, 0, y + 4);
        g.fillStyle = (s.top.red && i === lines.length - 1) ? '#e3242f' : '#ffffff';
        g.fillText(ln, 0, y);
      });
      g.restore();
    }
    if (s.step) {
      g.save(); g.font = '64px "Bebas Neue"'; g.textBaseline = 'middle';
      const label = 'STEP'; const tw = g.measureText(label).width;
      const x0 = W / 2 - (tw + 76) / 2, y0 = 170;
      g.lineWidth = 12; g.strokeStyle = '#141a2e'; g.lineJoin = 'round';
      g.strokeText(label, x0, y0); g.fillStyle = '#fff'; g.fillText(label, x0, y0);
      g.beginPath(); g.arc(x0 + tw + 46, y0 - 2, 34, 0, Math.PI * 2); g.fillStyle = '#e3242f'; g.fill();
      g.lineWidth = 5; g.strokeStyle = '#fff'; g.stroke();
      g.fillStyle = '#fff'; g.textAlign = 'center'; g.fillText(String(s.step), x0 + tw + 46, y0 + 1);
      g.restore();
    }
    // bottom caption bar synced to narration (Shorts)
    const cap = B.captions.find((c) => t >= c.start && t < c.end);
    if (cap) {
      g.save(); g.font = '76px "Bebas Neue"'; g.textAlign = 'center'; g.textBaseline = 'middle';
      const tw = g.measureText(cap.text).width;
      const y = 1395, padX = 30, h = 100;
      g.fillStyle = 'rgba(16,14,22,0.88)';
      const x = W / 2 - tw / 2 - padX;
      g.beginPath(); g.roundRect(x, y - h / 2, tw + padX * 2, h, 14); g.fill();
      g.fillStyle = '#fff'; g.fillText(cap.text, W / 2, y + 3);
      g.restore();
    }
  }

  // ---------- per frame QC metrics ----------
  qc(t, s, idx, st, proj) {
    const { J, OJ } = st;
    const issues = [];
    const hm = this.hero.metrics, om = this.opp.metrics;
    for (const [k, v] of Object.entries(hm.reach)) if (v > 0.999) issues.push(`hero ${k} overextended ${v.toFixed(3)}`);
    for (const [k, v] of Object.entries(om.reach)) if (v > 0.999) issues.push(`opponent ${k} overextended ${v.toFixed(3)}`);
    for (const s2 of ['L', 'R']) {
      if (hm['ankleGap' + s2] > 0.004) issues.push(`hero foot ${s2} detached ${hm['ankleGap' + s2].toFixed(3)}`);
      if (om['ankleGap' + s2] > 0.004) issues.push(`opponent foot ${s2} detached ${om['ankleGap' + s2].toFixed(3)}`);
    }
    const pen = (a, ra, b, rb) => (ra + rb) - a.distanceTo(b);
    for (const s2 of ['L', 'R']) {
      const p1 = pen(J.gloveW[s2], J.gloveR, J.headW, J.headR);
      if (p1 > 0.03) issues.push(`hero glove ${s2} inside own head ${p1.toFixed(3)}`);
      for (const s3 of ['L', 'R']) {
        const p2 = pen(J.gloveW[s2], J.gloveR, OJ.gloveW[s3], OJ.gloveR);
        if (p2 > 0.01) issues.push(`glove clash hero ${s2} vs opp ${s3} ${p2.toFixed(3)}`);
      }
      const p3 = pen(J.gloveW[s2], J.gloveR, OJ.headW, OJ.headR);
      if (p3 > 0.045) issues.push(`hero glove ${s2} too deep in opponent head ${p3.toFixed(3)}`);
      // elbow inside torso
      const ax = J.torsoAxisW; const seg = new THREE.Line3(ax.a, ax.b); const cp = new THREE.Vector3();
      seg.closestPointToPoint(J.elbowW[s2], true, cp);
      if (cp.distanceTo(J.elbowW[s2]) < ax.r * 0.75) issues.push(`hero elbow ${s2} inside torso`);
    }
    const toOpp = OJ.headW.clone().sub(J.headW).setY(0).normalize();
    if (J.forwardW.dot(toOpp) < 0.6) issues.push('hero not facing opponent');
    const toHero = J.headW.clone().sub(OJ.headW).setY(0).normalize();
    if (OJ.forwardW.dot(toHero) < 0.3 && st.r < 0.2) issues.push('opponent not facing hero');
    for (const F of [J, OJ]) for (const s2 of ['L', 'R']) if (F.heelW[s2].y < -0.01) issues.push('heel below floor');
    if (J.hipW.R.distanceTo(OJ.hipW.L) < 0.3) issues.push('bodies overlapping');
    // feet planted: ball positions must not slide between frames inside one shot
    const balls = [J.ballW.L, J.ballW.R, OJ.ballW.L, OJ.ballW.R];
    if (this.prev.idx === idx && this.prev.balls) {
      balls.forEach((b, i) => { const d = b.distanceTo(this.prev.balls[i]); if (d > 0.002) issues.push(`foot slide ${d.toFixed(3)}`); });
    }
    this.prev = { idx, balls: balls.map((b) => b.clone()) };
    // framing: both heads must be inside the frame when the shot claims to show the exchange
    const onScreen = (v) => { const p = proj(v); return p.x > 0 && p.x < W && p.y > 0 && p.y < H && p.z < 1; };
    if (s.mustSee) for (const k of s.mustSee) {
      const v = k === 'heroHead' ? J.headW : k === 'oppHead' ? OJ.headW : k === 'rearFoot' ? J.ballW.R : k === 'gloveR' ? J.gloveW.R : null;
      if (v && !onScreen(v)) issues.push(`${k} out of frame`);
    }
    return { t: +t.toFixed(3), shot: s.id, angle: s.angle, issues, arm: +st.c.arm.toFixed(3), reach: +(hm.reach.armR || 0).toFixed(3), elbowL: +(hm.elbowDegL || 0).toFixed(0), elbowR: +(hm.elbowDegR || 0).toFixed(0), forearmUpR: +(hm.forearmUpDegR || 0).toFixed(0), kp: { hero: this.coco(J, proj), opp: (s.hide || []).includes('opp') ? null : this.coco(OJ, proj) } };
  }
}
