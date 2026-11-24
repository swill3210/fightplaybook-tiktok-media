// Pose control board for the image model benchmark: one frozen frame per scene (1 s each).
// Hero on the right facing left (camera on the hero's lead side) so the lead hand and the liver face camera.
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const orbit = (target, az, el, dist, fov) => ({ pos: target.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(dist)), target, fov });
const at = (move, extra = 0) => () => MOVES[move].impact * MOVES[move].dur + extra;
const mid = (st, y) => st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5).setY(y);
const shot = (i, id, angle, def) => Object.assign({ id, angle, start: i, end: i + 1, moveAt: 0, still: true, noSpeedLines: true }, def);

export const board = {
  id: 'posebench', width: 1920, height: 1080, fps: 30, duration: 6,
  style: {
    bg: '#C4D6C4',
    hero: { skin: 0x303137, shirt: '#0c0c0f', stripe: '#d1202f', yoke: true, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x111114, scale: 1.08 },
  },
  script: '', captions: [],
  shots: [
    shot(0, 'S01', 'wide side, both in guard', { move: 'jab_high', clock: () => -1, cam: (u, st) => orbit(mid(st, 0.95), Math.PI - 0.05, 0.04, 4.3, 30) }),
    shot(1, 'S02', 'medium side, jab to the high guard', { move: 'jab_high', clock: at('jab_high'), cam: (u, st) => orbit(mid(st, 1.15), Math.PI - 0.12, 0.05, 3.4, 30) }),
    shot(2, 'S03', 'rear three quarter, lead hook to the liver', { move: 'hook_body', clock: at('hook_body'), cam: (u, st) => orbit(mid(st, 1.0), 3.75, 0.14, 3.2, 30) }),
    shot(3, 'S05', 'worms eye, opponent folds', { move: 'hook_body', oppX: 0.85, clock: at('hook_body', 0.6), cam: (u, st) => orbit(st.OJ.pelvisW.clone().setY(0.9), 2.6, -0.18, 2.9, 34) }),
    shot(4, 'S07', 'high overhead, both in stance', { move: 'jab_high', clock: () => -1, cam: (u, st) => ({ pos: mid(st, 0).add(V(0.0, 4.6, -0.6)), target: mid(st, 0.6), fov: 34 }) }),
    shot(5, 'S10', 'medium side, rear straight (cross)', { move: 'cross_body', clock: at('cross_body'), cam: (u, st) => orbit(mid(st, 1.15), Math.PI - 0.1, 0.05, 3.4, 30) }),
  ],
};
