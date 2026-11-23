// Technique library. Every move is a set of timed channels so the kinetic chain order is
// explicit and checkable. Each move also declares which hand strikes, its target, the arm
// shape it must show (straight or L), the reach it is staged at, and how the opponent reacts.
import * as THREE from 'three';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);

export const clamp01 = (x) => Math.max(0, Math.min(1, x));
export const ease = {
  inOut: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  out: (x) => 1 - Math.pow(1 - x, 2.4),
  in: (x) => x * x * x,
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
};
export const seg = (u, a, b, f = ease.inOut) => f(clamp01((u - a) / (b - a)));
const lerp = (a, b, t) => a + (b - a) * t;

export const MOVES = {
  // Rear straight (cross) with the whole body: foot, hips, shoulders, then arm.
  cross_body: {
    dur: 0.72, impact: 0.44, power: 1.0, hand: 'R', shape: 'straight', target: 'chin', reaction: 'head', reach: 0.975,
    ch: (u) => ({
      foot: seg(u, 0.0, 0.30) - seg(u, 0.62, 0.95),
      hips: seg(u, 0.04, 0.36) - seg(u, 0.60, 0.95),
      shoulders: seg(u, 0.10, 0.42) - seg(u, 0.58, 0.92),
      arm: seg(u, 0.16, 0.44, ease.out) - seg(u, 0.50, 0.70),
    }),
  },
  // The mistake: arm and a little shoulder only.
  cross_arm: {
    dur: 0.58, impact: 0.46, power: 0.22, hand: 'R', shape: 'straight', target: 'chin', reaction: 'head', reach: 0.975,
    ch: (u) => ({
      foot: 0,
      hips: 0.08 * (seg(u, 0.05, 0.4) - seg(u, 0.6, 0.9)),
      shoulders: 0.55 * (seg(u, 0.05, 0.46) - seg(u, 0.56, 0.86)),
      arm: seg(u, 0.06, 0.46, ease.out) - seg(u, 0.56, 0.80),
      reachLean: seg(u, 0.05, 0.46) - seg(u, 0.56, 0.86),
    }),
  },
  // Lead jab to the high guard: arm straight on a horizontal line, small shoulder turn,
  // rear glove stays on the chin, retracts on the same line.
  jab_high: {
    dur: 0.5, impact: 0.42, power: 0.35, hand: 'L', shape: 'straight', target: 'guard', reaction: 'guardUp', reach: 0.97,
    ch: (u) => ({
      arm: seg(u, 0.04, 0.42, ease.out) - seg(u, 0.52, 0.82),
      shoulders: seg(u, 0.04, 0.42) - seg(u, 0.52, 0.86),
    }),
  },
  // Lead hook to the liver: level change with both knees, chamber, then hips, shoulders and
  // the L shaped arm turn through together, pivot on the ball of the lead foot, rear glove on chin.
  hook_body: {
    dur: 0.85, impact: 0.55, power: 1.0, hand: 'L', shape: 'hook', target: 'liver', reaction: 'fold', reach: 0.73,
    ch: (u) => ({
      dip: seg(u, 0.0, 0.32) - seg(u, 0.78, 1.0),
      chamber: seg(u, 0.05, 0.32) - seg(u, 0.36, 0.55),
      hips: seg(u, 0.28, 0.55) - seg(u, 0.72, 1.0),
      shoulders: seg(u, 0.30, 0.57) - seg(u, 0.72, 1.0),
      arm: seg(u, 0.32, 0.55, ease.out) - seg(u, 0.66, 0.95),
      foot: seg(u, 0.28, 0.55) - seg(u, 0.75, 1.0),
    }),
  },
  // Glove touches the ribs once (pointing at the door). No power.
  tap_ribs: {
    dur: 0.7, impact: 0.5, power: 0.08, hand: 'L', shape: 'hook', target: 'liver', reaction: 'none', reach: 0.73,
    ch: (u) => ({
      dip: 0.6 * (seg(u, 0.0, 0.35) - seg(u, 0.7, 1.0)),
      arm: seg(u, 0.1, 0.5, ease.sine) - seg(u, 0.6, 0.95),
      chamber: 0, hips: 0.2 * (seg(u, 0.1, 0.5) - seg(u, 0.6, 1)), shoulders: 0.25 * (seg(u, 0.1, 0.5) - seg(u, 0.6, 1)), foot: 0,
    }),
  },
};

// Orthodox guard stance, fighter local space (+X toward opponent, +Z fighter's right)
export function stance(kind, guard = 'normal') {
  const hands = kind === 'opponent'
    ? (guard === 'high'
      ? { L: { guard: { f: 0.15, side: -0.075, up: 0.03 } }, R: { guard: { f: 0.14, side: 0.075, up: 0.03 } } }
      : { L: { guard: { f: 0.22, side: -0.03, up: -0.32 } }, R: { guard: { f: 0.12, side: 0.085, up: -0.04 } } })
    : { L: { guard: { f: 0.24, side: -0.065, up: -0.02 } }, R: { guard: { f: 0.13, side: 0.078, up: -0.055 } } };
  return {
    feet: {
      L: { x: 0.27, z: -0.13, yaw: 0.30, lift: 0, h: 0 },
      R: { x: -0.30, z: 0.15, yaw: 0.78, lift: 0, h: 0 },
    },
    pelvis: { x: -0.02, y: 0.835, z: 0.0, yaw: -0.55, lean: 0.08 },
    chest: { yaw: -0.62, lean: 0.14, roll: 0 },
    head: { yaw: 0, pitch: 0.16, roll: 0, drop: 0, tuck: 0, squash: 0, squint: 0 },
    shoulderRaise: { L: 0, R: 0 },
    hands,
  };
}

export function applyCross(P, c) {
  const f = P.feet.R;
  f.yaw = lerp(0.78, 0.12, c.foot);
  f.lift = lerp(0, 0.55, c.foot);
  P.pelvis.yaw = lerp(-0.55, 0.18, c.hips);
  P.pelvis.x = lerp(-0.02, 0.055, c.hips);
  P.pelvis.y = lerp(0.835, 0.825, c.hips);
  P.pelvis.lean = lerp(0.08, 0.13, c.hips);
  P.chest.yaw = lerp(-0.62, 0.48, c.shoulders);
  P.chest.lean = lerp(0.14, 0.22, c.shoulders);
  P.hands.R.guard.f += 0.10 * c.shoulders;
  P.hands.R.guard.side += 0.03 * c.shoulders;
  P.shoulderRaise.R = 0.04 * c.arm;
  P.head.drop = 0.028 * c.arm;
  P.head.pitch = 0.16 + 0.10 * c.arm;
  if (c.reachLean) { P.chest.lean += 0.22 * c.reachLean; P.pelvis.lean += 0.06 * c.reachLean; }
}

export function applyJab(P, c) {
  P.chest.yaw = -0.62 - 0.32 * c.shoulders;
  P.pelvis.yaw = -0.55 - 0.08 * c.shoulders;
  P.pelvis.x = -0.02 + 0.03 * c.shoulders;
  P.shoulderRaise.L = 0.035 * c.arm; // lead shoulder up to cover the chin
  P.head.drop = 0.015 * c.arm;
}

export function applyHook(P, c) {
  // level change from the knees, not the waist
  P.pelvis.y = 0.835 - 0.10 * c.dip;
  P.pelvis.lean = 0.08 + 0.05 * c.dip;
  P.chest.lean = 0.14 + 0.08 * c.dip;
  // load slightly the other way in the chamber, then turn through
  P.pelvis.yaw = -0.55 + 0.10 * c.chamber - 0.55 * c.hips;
  P.chest.yaw = -0.62 + 0.15 * c.chamber - 0.80 * c.shoulders;
  P.pelvis.x = -0.02 + 0.02 * c.hips;
  // pivot on the ball of the lead foot, heel turns out
  P.feet.L.yaw = 0.30 + 0.75 * c.foot;
  P.feet.L.lift = 0.30 * c.foot;
  P.head.drop = 0.02 * c.dip;
  // rear glove glued to the chin as the torso turns
  P.hands.R.guard.f += 0.02 * c.shoulders;
}

// lead foot step forward then rear foot follows (dx metres), with the pelvis travelling between
export function applyStep(P, k, dx) {
  const lead = seg(k, 0.0, 0.55), rear = seg(k, 0.35, 0.95);
  P.feet.L.x += dx * lead; P.feet.L.h = 0.07 * Math.sin(Math.PI * clamp01(k / 0.55));
  P.feet.R.x += dx * rear; P.feet.R.h = 0.06 * Math.sin(Math.PI * clamp01((k - 0.35) / 0.6));
  P.pelvis.x += dx * seg(k, 0.1, 0.85);
}

// Opponent reactions. r is a 0..1 impulse response sampled at time since impact.
export function impulse(dt, power, tau = 0.085) {
  if (dt < 0) return 0;
  const x = dt / tau;
  return power * x * Math.exp(1 - x) * (1 - 0.15 * Math.sin(dt * 18) * Math.exp(-dt * 4));
}
// slower rise and hold for a body shot fold
export function foldCurve(dt, power) {
  if (dt < 0) return 0;
  return power * (1 - Math.exp(-dt / 0.12)) * (0.75 + 0.25 * Math.exp(-dt / 0.6));
}
export function applyReaction(P, kind, r, contact) {
  if (kind === 'head') {
    P.head.pitch = 0.16 - 0.55 * r; P.head.yaw += -0.32 * r; P.head.roll = 0.18 * r;
    P.chest.lean -= 0.16 * r; P.chest.yaw -= 0.12 * r; P.pelvis.x -= 0.05 * r;
    P.head.squash = 0.07 * contact;
  } else if (kind === 'guardUp') {
    // the jab pushes the guard back and the gloves climb; elbows lift and open the ribs
    P.head.pitch -= 0.12 * r; P.chest.lean -= 0.05 * r;
    for (const s of ['L', 'R']) { P.hands[s].guard.up += 0.05 * r; P.hands[s].guard.f -= 0.03 * r; }
  } else if (kind === 'fold') {
    // body shot: torso folds forward at the waist and twists away, hands drop toward the ribs, knees give
    P.pelvis.y -= 0.07 * r; P.pelvis.x -= 0.04 * r; P.pelvis.lean += 0.25 * r;
    P.chest.lean += 0.45 * r; P.chest.yaw -= 0.30 * r;
    P.head.pitch += 0.45 * r; P.head.drop = 0.02 * r;
    for (const s of ['L', 'R']) { P.hands[s].guard.up -= 0.30 * r; P.hands[s].guard.f -= 0.04 * r; }
    P.hands.R.guard.side -= 0.02 * r;
  }
}

export const headYawTo = (fromLocal, toLocal) => Math.atan2(-(toLocal.z - fromLocal.z), toLocal.x - fromLocal.x);
