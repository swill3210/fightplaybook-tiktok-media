// Method C of the generation comparison: the rigged characters animated directly (cel shaded, ink outlines).
// 4 techniques x 2 cameras, each move at half speed with a hold on contact. No image generation.
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
import { CAMS, board as lib } from './motionlib.js';
const MV = [['jab', 'jab_high'], ['cross', 'cross_body'], ['lead_body_hook', 'hook_body'], ['shovel_uppercut', 'shovel_up']];
const SEG = 2.2; // seconds per clip
const shots = []; let t = 0;
for (const [name, move] of MV) for (const cam of ['liver34', 'side']) {
  const mv = MOVES[move], imp = mv.impact * mv.dur;
  // half speed through the strike, hold 0.4 s on contact, then finish the move
  const close = move === 'hook_body' || move === 'shovel_up'; // pocket range: no held stance (guards would overlap); entry footwork is backlog
  const clock = (tl) => { const pre = close ? 0 : 0.35; if (tl < pre) return -1; const u = (tl - pre) * 0.5; return u < imp ? u : (tl - pre) * 0.5 < imp + 0.2 ? imp : u - 0.2; };
  shots.push({ id: `${name}.${cam}`, angle: cam, start: t, end: t + SEG, move, moveAt: 0, clock, cam: (u, st) => CAMS[cam](st), noSpeedLines: false });
  t += SEG;
}
export const board = { ...lib, id: 'methodc', duration: t, shots };
