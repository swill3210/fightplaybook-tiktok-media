// Approved motion library v1: every rig technique x 3 phases x 6 cameras, one still per shot (t = index + 0.5).
// Each still is written with its measured metrics and COCO 17 skeleton (render.mjs --still), which the anatomy
// validator uses as the reference. Build list and expectations: production/motionlib/library.json.
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const orbit = (t, az, el, d, fov) => ({ pos: t.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(d)), target: t, fov });
const mid = (st, y) => st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5).setY(y);
export const CAMS = {
  liver34: (st) => orbit(mid(st, 1.0), Math.PI + 0.45, 0.15, 3.2, 30),
  side: (st) => orbit(mid(st, 1.0), Math.PI, 0.05, 3.4, 30),
  rear34: (st) => orbit(mid(st, 1.0), Math.PI + 1.0, 0.12, 3.1, 30),
  low: (st) => orbit(mid(st, 0.9), Math.PI + 0.4, -0.3, 2.6, 36),
  overhead: (st) => ({ pos: mid(st, 0).add(V(0.0, 4.6, -0.6)), target: mid(st, 0.6), fov: 34 }),
  rightside: (st) => orbit(mid(st, 0.95), 0.15, 0.0, 3.1, 32),
};
export const ENTRIES = [
  ['guard', 'jab_high', 'guard'], ['jab', 'jab_high', 'strike'], ['cross', 'cross_body', 'strike'], ['arm_punch_mistake', 'cross_arm', 'strike'],
  ['lead_body_hook', 'hook_body', 'strike'], ['shovel_uppercut', 'shovel_up', 'strike'],
];
// chamber 35 percent of the way to impact (glove still near the guard), recover 0.35 s after impact (on the way back to guard)
const PHASES = { chamber: 'c', impact: 'i', recover: 'r' };
const clock = (move, kind, ph) => () => { if (kind === 'guard') return -1; const imp = MOVES[move].impact * MOVES[move].dur; return ph === 'c' ? 0.35 * imp : ph === 'i' ? imp : imp + 0.35; };
export const LIST = [];
for (const [name, move, kind] of ENTRIES) for (const cam of Object.keys(CAMS)) for (const [ph, dt] of Object.entries(PHASES)) {
  if (kind === 'guard' && ph !== 'impact') continue;
  LIST.push({ name, move, cam, phase: kind === 'guard' ? 'stance' : ph, clock: clock(move, kind, dt) });
}
export const board = {
  id: 'motionlib', width: 1920, height: 1080, fps: 30, duration: LIST.length,
  style: {
    bg: '#C4D6C4',
    hero: { skin: 0x303137, shirt: '#0c0c0f', stripe: '#d1202f', yoke: true, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x111114, scale: 1.08 },
  },
  script: '', captions: [],
  shots: LIST.map((e, i) => ({ id: `${e.name}.${e.cam}.${e.phase}`, angle: e.cam, start: i, end: i + 1, move: e.move, moveAt: 0, clock: e.clock, cam: (u, st) => CAMS[e.cam](st), still: true, noSpeedLines: true, noReact: e.phase !== 'recover' })),
};
