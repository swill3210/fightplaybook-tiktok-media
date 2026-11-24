// Rig poses for the 17 liver shots that failed the combat accuracy audit (redraw references).
// Hero on the right facing left where the liver contact must be visible (camera on the hero's lead side).
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const orbit = (t, az, el, d, fov, up) => ({ pos: t.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(d)), target: t, fov, up });
const imp = (m, dt = 0) => () => MOVES[m].impact * MOVES[m].dur + dt;
const mid = (st, y) => st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5).setY(y);
const S = [
  ['V2', 'hook_body', imp('hook_body', 0), (st) => orbit(st.OJ.liverW.clone(), 2.6, 0.05, 1.5, 32)],
  ['V3', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.6, 0.12, 3.3, 30)],
  ['V9', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.5, 0.1, 3.8, 30)],
  ['V15', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.7, 0.45, 3.2, 30)],
  ['V21', 'hook_body', imp('hook_body', 0), (st) => orbit(st.OJ.liverW.clone(), 2.6, -0.3, 2.3, 38)],
  ['V23', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.3, 0.05, 2.3, 32)],
  ['V33', 'hook_body', imp('hook_body', -0.08), (st) => orbit(mid(st, 1.0), 2.35, 0.06, 3.4, 30)],
  ['V34', 'hook_body', imp('hook_body', 0), (st) => orbit(st.OJ.liverW.clone(), 2.65, -0.2, 1.8, 36)],
  ['V38', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.3, 0.08, 2.7, 30)],
  ['V39', 'hook_body', imp('hook_body', 0), (st) => orbit(st.OJ.liverW.clone(), 2.7, -0.15, 1.3, 36)],
  ['V53', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.75, 0.5, 2.3, 32)],
  ['V84', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.6, 0.08, 2.7, 30)],
  ['V86', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.8, 0.55, 2.4, 32)],
  ['V94', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.55, 0.35, 2.9, 30)],
  ['V57', 'hook_body', imp('hook_body', -0.1), (st) => orbit(mid(st, 1.0), 2.6, 0.1, 2.9, 30)],
  ['V61', 'hook_body', imp('hook_body', 0), (st) => orbit(mid(st, 1.0), 2.6, 0.08, 2.9, 30), ["opp"]],
  ['V59', 'hook_body', imp('hook_body', -0.12), (st) => ({ pos: st.OJ.headW.clone().add(V(0, 0.05, 0)), target: st.J.pelvisW.clone().setY(1.05), fov: 50 }), ['opp']],
];
export const board = {
  id: 'liverfix2', width: 1920, height: 1080, fps: 30, duration: S.length,
  style: {
    bg: '#C4D6C4',
    hero: { skin: 0x303137, shirt: '#0c0c0f', stripe: '#d1202f', yoke: true, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x111114, scale: 1.08 },
  },
  script: '', captions: [],
  shots: S.map(([id, move, clock, cam, hide], i) => ({ id, angle: id, start: i, end: i + 1, move, moveAt: 0, clock, cam: (u, st) => cam(st), hide: hide || [], still: true, noSpeedLines: true, noReact: true })),
};
