// Thumbnail pose: the much bigger opponent, low angle, lead body hook landing in the liver (for redraw)
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const orbit = (t, az, el, d, fov) => ({ pos: t.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(d)), target: t, fov });
export const board = {
  id: 'thumbbench', width: 1920, height: 1080, fps: 30, duration: 2,
  style: {
    bg: '#C4D6C4',
    hero: { skin: 0x303137, shirt: '#0c0c0f', stripe: '#d1202f', yoke: true, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x111114, scale: 1.32 },
  },
  script: '', captions: [],
  shots: [0, 1].map((i) => ({ id: 'T' + i, angle: 'low', start: i, end: i + 1, move: 'hook_body', moveAt: 0, still: true, noSpeedLines: true, noReact: true,
    clock: () => MOVES.hook_body.impact * MOVES.hook_body.dur,
    cam: (u, st) => orbit(st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.45).setY(1.05), [Math.PI - 0.55, Math.PI + 0.45][i], -0.16, 3.3, 34) })),
};
