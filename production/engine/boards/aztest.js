// Rig poses for the 17 liver shots that failed the combat accuracy audit (redraw references).
// Hero on the right facing left where the liver contact must be visible (camera on the hero's lead side).
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const orbit = (t, az, el, d, fov, up) => ({ pos: t.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(d)), target: t, fov, up });
const imp = (m, dt = 0) => () => MOVES[m].impact * MOVES[m].dur + dt;
const mid = (st, y) => st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5).setY(y);
const S = [
  ['A0', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 2.4, 0.12, 3.2, 30)],
  ['A1', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 2.8, 0.12, 3.2, 30)],
  ['A2', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 3.2, 0.12, 3.2, 30)],
  ['A3', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 3.6, 0.12, 3.2, 30)],
  ['A4', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 4.0, 0.12, 3.2, 30)],
  ['A5', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 4.4, 0.12, 3.2, 30)],
  ['A6', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 4.8, 0.12, 3.2, 30)],
  ['A7', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), 5.2, 0.12, 3.2, 30)],
];
export const board = {
  id: 'aztest', width: 1920, height: 1080, fps: 30, duration: S.length,
  style: {
    bg: '#C4D6C4',
    hero: { skin: 0x303137, shirt: '#0c0c0f', stripe: '#d1202f', yoke: true, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x111114, scale: 1.08 },
  },
  script: '', captions: [],
  shots: S.map(([id, move, clock, cam, hide], i) => ({ id, angle: id, start: i, end: i + 1, move, moveAt: 0, clock, cam: (u, st) => cam(st), hide: hide || [], still: true, noSpeedLines: true, noReact: true })),
};
