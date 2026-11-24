// Fight Playbook fighter rig.
// Joint positions are solved from pose parameters with analytic two bone IK,
// so feet stay planted, gloves reach exactly where they are aimed, and no limb
// is ever stretched past its real length. Meshes are then fitted between joints.
// Fighter local space: +X forward (toward opponent), +Y up, +Z fighter's right.
import * as THREE from 'three';

const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const UP = V(0, 1, 0);

export const DIMS = {
  ankleH: 0.075, thigh: 0.44, shin: 0.44,
  hipHalf: 0.10, shoulderY: 0.46, shoulderHalf: 0.20, neckY: 0.50, headY: 0.645,
  headR: 0.105, upperArm: 0.29, foreArm: 0.27, gloveOff: 0.055, gloveR: 0.058,
};

// ---------- small math helpers ----------
export function twoBoneIK(root, target, a, b, pole, out) {
  const d0 = target.clone().sub(root);
  let d = d0.length();
  const max = (a + b) * 0.999;
  out.reach = d / (a + b);
  out.clamped = d > max;
  if (d > max) d = max;
  if (d < Math.abs(a - b) + 1e-4) d = Math.abs(a - b) + 1e-4;
  const dir = d0.normalize();
  const x = (a * a - b * b + d * d) / (2 * d);
  const h = Math.sqrt(Math.max(0, a * a - x * x));
  const n = pole.clone().sub(dir.clone().multiplyScalar(pole.dot(dir)));
  if (n.lengthSq() < 1e-8) n.set(0, -1, 0);
  n.normalize();
  out.mid = root.clone().add(dir.clone().multiplyScalar(x)).add(n.multiplyScalar(h));
  out.end = root.clone().add(dir.clone().multiplyScalar(d));
  return out;
}

const yawQ = (a) => new THREE.Quaternion().setFromAxisAngle(UP, a);

// ---------- materials ----------
function toonGradient() {
  const c = new Uint8Array([70, 70, 70, 255, 150, 150, 150, 255, 235, 235, 235, 255]);
  const t = new THREE.DataTexture(c, 3, 1, THREE.RGBAFormat);
  t.minFilter = t.magFilter = THREE.NearestFilter; t.needsUpdate = true; return t;
}
const GRAD = toonGradient();
export function toon(color, extra = {}) {
  return new THREE.MeshToonMaterial({ color, gradientMap: GRAD, ...extra });
}
const outlineMat = (w) => new THREE.ShaderMaterial({
  uniforms: { w: { value: w }, col: { value: new THREE.Color(0x0b0c12) } },
  vertexShader: `uniform float w; void main(){ vec3 p = position + normal * w; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }`,
  fragmentShader: `uniform vec3 col; void main(){ gl_FragColor = vec4(col,1.0); }`,
  side: THREE.BackSide,
});

function withOutline(mesh, w = 0.008) {
  const o = new THREE.Mesh(mesh.geometry, outlineMat(w));
  o.castShadow = false; o.renderOrder = -1;
  mesh.add(o);
  mesh.castShadow = true;
  return mesh;
}

// tapered limb segment: unit length along +Y, base radius r0 at y=0, r1 at y=1
function limbGeo(r0, r1) {
  const pts = [];
  const N = 14;
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    // swell in the middle for muscle
    const r = THREE.MathUtils.lerp(r0, r1, t) * (1 + 0.16 * Math.sin(Math.PI * Math.min(1, t * 1.15)));
    pts.push(new THREE.Vector2(r, t));
  }
  const g = new THREE.LatheGeometry(pts, 20);
  return g;
}

function sphere(r, mat, sx = 1, sy = 1, sz = 1) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 28, 20), mat);
  m.scale.set(sx, sy, sz);
  return withOutline(m, 0.008 / Math.max(sx, sy, sz));
}

// stripe texture for the shirt: black with red side stripes (u wraps around torso)
function shirtTexture(base, stripe, opts = {}) {
  const c = document.createElement('canvas'); c.width = 512; c.height = 256;
  const g = c.getContext('2d');
  g.fillStyle = base; g.fillRect(0, 0, 512, 256);
  if (stripe) {
    g.fillStyle = stripe;
    // lathe u=0 is +Z side? stripes at the two sides (u = .25 and .75)
    for (const u of [0.25, 0.75]) { g.fillRect(u * 512 - 9, 0, 18, 256); }
    // thin accent at the neckline and armholes
    g.fillRect(0, 0, 512, 6);
  }
  if (stripe && opts.yoke) {
    // red shoulder accents running over the top of the chest, as on the reference sheet
    g.fillStyle = stripe;
    for (const u of [0.25, 0.75]) { g.beginPath(); g.moveTo(u * 512 - 60, 18); g.lineTo(u * 512 + 60, 18); g.lineTo(u * 512 + 60, 30); g.lineTo(u * 512 - 60, 30); g.fill(); }
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// ---------- fighter ----------
export class Fighter {
  constructor(opts) {
    this.o = Object.assign({
      skin: 0x34353b, shirt: '#0d0d10', stripe: '#d1202f', shorts: 0x1c2747, trim: 0xd1202f,
      glove: 0x111114, strap: 0xd1202f, scale: 1, eyes: true,
    }, opts);
    this.root = new THREE.Group();
    this.root.scale.setScalar(this.o.scale);
    this.parts = {};
    this.build();
    this.metrics = {};
  }

  build() {
    const o = this.o, R = this.root;
    const skin = toon(o.skin), shorts = toon(o.shorts), trim = toon(o.trim), glove = toon(o.glove), strap = toon(o.strap);
    this.mats = { skin, shorts, glove };
    const shirtMat = toon(0xffffff, { map: shirtTexture(o.shirt, o.stripe, { yoke: o.yoke }) });
    const add = (k, m) => { this.parts[k] = m; R.add(m); return m; };

    // torso: lathe profile from pelvis (y=0) to neck (y=.5); elliptic cross section
    const prof = [
      [0.0, 0.150], [0.06, 0.158], [0.12, 0.150], [0.20, 0.152], [0.28, 0.172], [0.35, 0.198], [0.42, 0.208], [0.47, 0.175], [0.51, 0.07],
    ].map(([y, r]) => new THREE.Vector2(r, y));
    const torsoG = new THREE.LatheGeometry(prof, 32);
    const abdomen = new THREE.Mesh(torsoG, shirtMat);
    withOutline(abdomen, 0.009);
    this.torso = add('torso', new THREE.Group());
    this.torso.add(abdomen);
    abdomen.scale.set(0.74, 1, 1.0); // depth (x) thinner than width (z)
    abdomen.position.y = 0.04;
    // shorts / pelvis
    const pelvG = new THREE.LatheGeometry([[0.0, 0.11], [0.04, 0.165], [0.10, 0.172], [0.16, 0.160], [0.18, 0.13]].map(([y, r]) => new THREE.Vector2(r, y - 0.11)), 32);
    const pelvis = withOutline(new THREE.Mesh(pelvG, shorts), 0.009);
    pelvis.scale.set(0.8, 1, 1);
    this.pelvis = add('pelvis', new THREE.Group()); this.pelvis.add(pelvis);
    const band = new THREE.Mesh(new THREE.TorusGeometry(0.155, 0.012, 8, 40), trim);
    band.rotation.x = Math.PI / 2; band.scale.set(0.8, 1, 1); band.position.y = 0.065; this.pelvis.add(band);

    // deltoids and pecs are part of chest group
    this.chest = add('chest', new THREE.Group());
    for (const s of [-1, 1]) {
      const d = sphere(0.085, skin, 1.05, 0.95, 1); d.position.set(0, 0, s * DIMS.shoulderHalf); this.chest.add(d);
      this.parts[s < 0 ? 'deltL' : 'deltR'] = d;
    }
    const traps = sphere(0.1, skin, 0.85, 0.55, 1.6); traps.position.set(-0.01, 0.035, 0); this.chest.add(traps);

    // neck + head
    this.neck = add('neck', new THREE.Mesh(limbGeo(0.058, 0.05), skin)); withOutline(this.neck, 0.007);
    this.head = add('head', new THREE.Group());
    const skull = sphere(DIMS.headR, skin, 1.0, 1.12, 0.92); this.head.add(skull); this.skull = skull;
    const jaw = sphere(0.07, skin, 1.0, 0.8, 1.05); jaw.position.set(0.035, -0.07, 0); this.head.add(jaw);
    if (o.eyes) {
      const eyeM = new THREE.MeshBasicMaterial({ color: 0xffffff });
      this.eyes = [];
      for (const s of [-1, 1]) {
        const e = new THREE.Mesh(new THREE.SphereGeometry(0.02, 16, 10), eyeM);
        e.scale.set(0.35, 0.42, 1.25);
        e.position.set(0.094, 0.012, s * 0.036);
        e.rotation.x = s * 0.42; // slanted: inner end lower
        e.rotation.y = s * 0.25;
        this.head.add(e); this.eyes.push(e);
      }
    }

    // limbs (unit length along +Y, scaled to bone length)
    const mk = (k, r0, r1, mat) => { const m = new THREE.Mesh(limbGeo(r0, r1), mat); withOutline(m, 0.0075); return add(k, m); };
    for (const s of ['L', 'R']) {
      mk('thigh' + s, 0.1, 0.07, skin);
      mk('shin' + s, 0.07, 0.045, skin);
      mk('upper' + s, 0.068, 0.056, skin);
      mk('fore' + s, 0.058, 0.046, skin);
      // shorts leg sleeve over upper thigh
      const sl = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.118, 1, 24, 1, true), shorts);
      sl.material.side = THREE.DoubleSide; withOutline(sl, 0.006);
      add('short' + s, sl);
      const hem = new THREE.Mesh(new THREE.TorusGeometry(0.119, 0.012, 8, 32), trim); add('hem' + s, hem);
      // knee, elbow, ankle joint balls
      add('knee' + s, sphere(0.068, skin));
      add('elbow' + s, sphere(0.056, skin));
      // foot: heel to toe, built in foot local space with ball of foot at origin
      const foot = new THREE.Group();
      const fm = sphere(0.05, skin, 2.4, 0.62, 1.0); fm.position.set(-0.045, 0.03, 0); foot.add(fm);
      const heel = sphere(0.045, skin, 1, 0.85, 1); heel.position.set(-0.15, 0.04, 0); foot.add(heel);
      add('foot' + s, foot);
      // glove: MMA glove, compact fist plus red wrist strap
      const g = new THREE.Group();
      const fist = sphere(DIMS.gloveR, glove, 1.25, 0.95, 1.05); fist.position.set(0, 0.02, 0); g.add(fist);
      const knuckle = sphere(0.04, glove, 0.9, 1.0, 1.25); knuckle.position.set(0, 0.07, 0); g.add(knuckle);
      const st = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.04, 20), strap); withOutline(st, 0.006);
      st.position.set(0, -0.045, 0); g.add(st);
      add('glove' + s, g);
    }
    this.root.traverse((m) => { if (m.isMesh && !(m.material instanceof THREE.ShaderMaterial)) { m.castShadow = true; } });
  }

  // place a unit +Y limb mesh between a and b (local coords)
  fit(mesh, a, b, roll = null) {
    const d = b.clone().sub(a); const L = d.length();
    mesh.position.copy(a);
    mesh.quaternion.setFromUnitVectors(UP, d.clone().normalize());
    mesh.scale.set(1, L, 1);
  }

  // ---------- solve ----------
  // p: pose parameters (see poseDefaults); world targets are converted into local space.
  solve(p) {
    const D = DIMS, R = this.root;
    R.position.copy(p.rootPos); R.rotation.set(0, p.rootYaw, 0); R.updateMatrixWorld(true);
    const inv = R.matrixWorld.clone().invert();
    const toLocal = (w) => w.clone().applyMatrix4(inv);
    const m = { reach: {}, clamp: [] };

    // feet: ball of foot on ground; yaw = toe angle toward fighter's right (+Z); heel lift pitch
    const feet = {};
    for (const s of ['L', 'R']) {
      const f = p.feet[s];
      const g = this.parts['foot' + s];
      g.position.set(f.x, f.h || 0, f.z);
      g.rotation.set(0, -f.yaw, -f.lift, 'YZX');
      g.updateMatrix();
      const ankle = V(-0.115, D.ankleH, 0).applyMatrix4(g.matrix);
      const toeDir = V(Math.cos(f.yaw), 0, Math.sin(f.yaw));
      feet[s] = { ankle, toeDir, ball: V(f.x, f.h || 0, f.z), planted: !(f.h > 0.001) };
    }

    // pelvis
    const pelvisPos = V(p.pelvis.x, p.pelvis.y, p.pelvis.z);
    const pq = yawQ(p.pelvis.yaw).multiply(new THREE.Quaternion().setFromAxisAngle(V(0, 0, 1), -p.pelvis.lean));
    this.pelvis.position.copy(pelvisPos); this.pelvis.quaternion.copy(pq);

    // chest frame
    const cq = yawQ(p.chest.yaw).multiply(new THREE.Quaternion().setFromAxisAngle(V(0, 0, 1), -p.chest.lean))
      .multiply(new THREE.Quaternion().setFromAxisAngle(V(1, 0, 0), p.chest.roll || 0));
    const spineBase = pelvisPos.clone().add(V(0, 0.06, 0).applyQuaternion(pq));
    const chestOrigin = spineBase.clone();
    const shoulderC = chestOrigin.clone().add(V(0, D.shoulderY - 0.06, 0).applyQuaternion(cq));
    this.torso.position.copy(chestOrigin); this.torso.quaternion.copy(cq);
    this.chest.position.copy(shoulderC); this.chest.quaternion.copy(cq);
    const sh = {
      L: shoulderC.clone().add(V(0, p.shoulderRaise.L, -D.shoulderHalf).applyQuaternion(cq)),
      R: shoulderC.clone().add(V(0, p.shoulderRaise.R, D.shoulderHalf).applyQuaternion(cq)),
    };
    this.parts.deltL.position.set(0, p.shoulderRaise.L, -D.shoulderHalf);
    this.parts.deltR.position.set(0, p.shoulderRaise.R, D.shoulderHalf);

    // neck and head
    const neckBase = chestOrigin.clone().add(V(0, D.neckY - 0.06, 0).applyQuaternion(cq));
    const hq = yawQ(p.head.yaw).multiply(new THREE.Quaternion().setFromAxisAngle(V(0, 0, 1), -p.head.pitch))
      .multiply(new THREE.Quaternion().setFromAxisAngle(V(1, 0, 0), p.head.roll || 0));
    const headPos = neckBase.clone().add(V(0.0, 0.03, 0).applyQuaternion(cq)).add(V(0, D.headY - D.neckY - 0.03, 0).applyQuaternion(hq))
      .add(V(p.head.tuck || 0, -(p.head.drop || 0), 0).applyQuaternion(cq));
    this.head.position.copy(headPos); this.head.quaternion.copy(hq);
    this.skull.scale.set(1.0 * (1 - (p.head.squash || 0)), 1.12, 0.92);
    if (this.eyes) for (const e of this.eyes) e.scale.y = 0.42 * (1 - 0.55 * (p.head.squint || 0));
    this.fit(this.neck, neckBase.clone().add(V(0, -0.04, 0)), headPos.clone().add(V(0, -0.05, 0)));

    // legs
    const hips = {
      L: pelvisPos.clone().add(V(0, -0.03, -D.hipHalf).applyQuaternion(pq)),
      R: pelvisPos.clone().add(V(0, -0.03, D.hipHalf).applyQuaternion(pq)),
    };
    for (const s of ['L', 'R']) {
      const ft = feet[s];
      const side = s === 'L' ? -1 : 1;
      const pole = ft.toeDir.clone().add(V(0, 0, side * 0.35).applyQuaternion(pq)).normalize();
      const ik = twoBoneIK(hips[s], ft.ankle, D.thigh, D.shin, pole, {});
      m.reach['leg' + s] = ik.reach; if (ik.clamped) m.clamp.push('leg' + s);
      this.fit(this.parts['thigh' + s], hips[s], ik.mid);
      this.fit(this.parts['shin' + s], ik.mid, ik.end);
      this.parts['knee' + s].position.copy(ik.mid);
      // shorts sleeve: from hip to 55% down the thigh
      const kneeDir = ik.mid.clone().sub(hips[s]);
      const sleeveEnd = hips[s].clone().add(kneeDir.clone().multiplyScalar(0.55));
      this.fit(this.parts['short' + s], hips[s].clone().add(kneeDir.clone().multiplyScalar(-0.12)), sleeveEnd);
      this.parts['short' + s].position.lerp(sleeveEnd, 0); // keep base
      // cylinder geometry is centered: shift to midpoint
      const sMid = hips[s].clone().add(kneeDir.clone().multiplyScalar(0.215));
      this.parts['short' + s].position.copy(sMid);
      const hem = this.parts['hem' + s];
      hem.position.copy(sleeveEnd); hem.quaternion.setFromUnitVectors(V(0, 0, 1), kneeDir.clone().normalize());
      // if leg target was out of reach the ankle we drew is end, not the foot ankle: record slide
      m['ankleGap' + s] = ik.end.distanceTo(ft.ankle);
    }

    // arms
    const gl = {};
    for (const s of ['L', 'R']) {
      const side = s === 'L' ? -1 : 1;
      const hs = p.hands[s];
      const hy = yawQ(p.head.yaw);
      const gpt = headPos.clone().add(V(hs.guard.f, hs.guard.up, hs.guard.side).applyQuaternion(hy));
      let wrist = gpt;
      if (hs.target && hs.w > 0) wrist = gpt.clone().lerp(toLocal(hs.target), hs.w);
      const pole = V(-0.35, -1, side * (p.elbowOut ?? 0.55)).applyQuaternion(cq).add(p.elbowPole ? p.elbowPole[s] : V()).normalize();
      const ik = twoBoneIK(sh[s], wrist, D.upperArm, D.foreArm, pole, {});
      m.reach['arm' + s] = ik.reach; if (ik.clamped) m.clamp.push('arm' + s);
      const ua = sh[s].clone().sub(ik.mid).normalize(), fa = ik.end.clone().sub(ik.mid).normalize();
      m['elbowDeg' + s] = THREE.MathUtils.radToDeg(Math.acos(Math.max(-1, Math.min(1, ua.dot(fa)))));
      this.fit(this.parts['upper' + s], sh[s], ik.mid);
      this.fit(this.parts['fore' + s], ik.mid, ik.end);
      this.parts['elbow' + s].position.copy(ik.mid);
      const fdir = ik.end.clone().sub(ik.mid).normalize();
      const g = this.parts['glove' + s];
      g.position.copy(ik.end.clone().add(fdir.clone().multiplyScalar(D.gloveOff - 0.02)));
      g.quaternion.setFromUnitVectors(UP, fdir);
      gl[s] = { center: ik.end.clone().add(fdir.clone().multiplyScalar(D.gloveOff)), dir: fdir, elbow: ik.mid, wrist: ik.end, shoulder: sh[s] };
    }

    R.updateMatrixWorld(true);
    const W = (v) => v.clone().applyMatrix4(R.matrixWorld);
    const sc = this.o.scale;
    this.joints = {
      headW: W(headPos), headR: D.headR * sc * 1.05,
      chinW: W(headPos.clone().add(V(0.10, -0.075, 0).applyQuaternion(hq))),
      gloveW: { L: W(gl.L.center), R: W(gl.R.center) }, gloveR: D.gloveR * 1.15 * sc,
      gloveFrontW: { L: W(gl.L.wrist.clone().add(gl.L.dir.clone().multiplyScalar(0.14))), R: W(gl.R.wrist.clone().add(gl.R.dir.clone().multiplyScalar(0.14))) },
      elbowW: { L: W(gl.L.elbow), R: W(gl.R.elbow) }, wristW: { L: W(gl.L.wrist), R: W(gl.R.wrist) },
      kneeW: { L: W(this.parts.kneeL.position), R: W(this.parts.kneeR.position) },
      shoulderW: { L: W(sh.L), R: W(sh.R) },
      hipW: { L: W(hips.L), R: W(hips.R) },
      pelvisW: W(pelvisPos), chestW: W(shoulderC),
      // the liver door: the fighter's right side just under the ribs
      liverW: W(pelvisPos.clone().add(V(0.05, 0.22, 0.165).applyQuaternion(pq))),
      ankleW: { L: W(feet.L.ankle), R: W(feet.R.ankle) },
      ballW: { L: W(feet.L.ball), R: W(feet.R.ball) }, planted: { L: feet.L.planted, R: feet.R.planted },
      heelW: {
        L: W(V(-0.19, 0, 0).applyMatrix4(this.parts.footL.matrix)),
        R: W(V(-0.19, 0, 0).applyMatrix4(this.parts.footR.matrix)),
      },
      forwardW: V(1, 0, 0).applyQuaternion(hq).applyQuaternion(R.quaternion).setY(0).normalize(),
      torsoAxisW: { a: W(spineBase), b: W(shoulderC), r: 0.15 * sc },
    };
    this.metrics = m;
    return this.joints;
  }
}
