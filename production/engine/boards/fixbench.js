// Rig poses for the 17 liver shots that failed the combat accuracy audit (redraw references).
// Hero on the right facing left where the liver contact must be visible (camera on the hero's lead side).
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const orbit = (t, az, el, d, fov, up) => ({ pos: t.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(d)), target: t, fov, up });
const imp = (m, dt = 0) => () => MOVES[m].impact * MOVES[m].dur + dt;
const mid = (st, y) => st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5).setY(y);
const S = [
  ['V2', 'hook_body', imp('hook_body'), (st) => orbit(st.OJ.liverW.clone().add(V(0, 0.15, 0)), Math.PI + 0.5, 0.1, 1.9, 32)],
  ['V3', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 0.45, 0.18, 3.1, 30)],
  ['V9', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 0.9, 0.12, 3.0, 30)],
  ['V15', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 0.3, 0.3, 3.3, 30)],
  ['V20', 'jab_high', imp('jab_high'), (st) => ({ pos: st.J.headW.clone().add(V(-0.45, 0.14, 0.32)), target: st.OJ.headW.clone().add(V(0, -0.15, 0)), fov: 42 })],
  ['V21', 'hook_body', imp('hook_body'), (st) => orbit(st.OJ.liverW.clone(), Math.PI + 0.35, -0.35, 2.3, 38)],
  ['V23', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 1.05, 0.05, 2.9, 30)],
  ['V24', 'shovel_up', imp('shovel_up'), (st) => orbit(mid(st, 0.95), Math.PI + 0.55, -0.15, 2.6, 32)],
  ['V33', 'hook_body', imp('hook_body', -0.05), (st) => orbit(mid(st, 1.0), Math.PI + 0.25, 0.08, 3.0, 30, V(-0.25, 0.97, 0))],
  ['V34', 'hook_body', imp('hook_body'), (st) => orbit(st.OJ.liverW.clone(), Math.PI + 0.6, -0.3, 2.4, 38)],
  ['V53', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 0.75, 0.25, 3.1, 30)],
  ['V70', 'shovel_up', imp('shovel_up'), (st) => orbit(mid(st, 1.0), Math.PI + 0.85, 0.15, 2.7, 32)],
  ['V79', 'shovel_up', imp('shovel_up'), (st) => orbit(mid(st, 0.95), 0.25, -0.05, 2.6, 32), ['opp']],
  ['V84', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI - 0.05, 0.05, 3.2, 30)],
  ['V86', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 0.5, 0.1, 3.0, 30)],
  ['V88', 'shovel_up', imp('shovel_up'), (st) => orbit(mid(st, 0.9), Math.PI + 0.35, -0.3, 2.4, 36)],
  ['V94', 'hook_body', imp('hook_body'), (st) => orbit(mid(st, 1.0), Math.PI + 0.4, 0.15, 3.3, 30)],
];
export const board = {
  id: 'fixbench', width: 1920, height: 1080, fps: 30, duration: S.length,
  style: {
    bg: '#C4D6C4',
    hero: { skin: 0x303137, shirt: '#0c0c0f', stripe: '#d1202f', yoke: true, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x111114, scale: 1.08 },
  },
  script: '', captions: [],
  shots: S.map(([id, move, clock, cam, hide], i) => ({ id, angle: id, start: i, end: i + 1, move, moveAt: 0, clock, cam: (u, st) => cam(st), hide: hide || [], still: true, noSpeedLines: true, noReact: true })),
};
