// Storyboard: "Punch With Your Body" (Fight Playbook Short), rebuilt on Grok's original voice track.
// Every shot names its angle; the QC pass refuses repeats back to back.
import * as THREE from 'three';
import { MOVES } from '../src/motion.js';
import { bar, ring, pill, leader, floorArc, footGhost } from '../src/fx.js';

const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const sm = (x) => x * x * (3 - 2 * x);
const io = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);

// orbit camera: az 0 = side view from the hero's right (+Z), az > 0 swings toward the opponent side
function orbit(target, az, el, dist, fov) {
  const pos = target.clone().add(V(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(dist));
  return { pos, target, fov };
}
function camMove(a, b, u, f = io) {
  const k = f(Math.max(0, Math.min(1, u)));
  const L = (x, y) => x + (y - x) * k;
  return (tgt) => orbit(tgt, L(a.az, b.az), L(a.el, b.el), L(a.dist, b.dist), L(a.fov, b.fov));
}
const mid = (st) => st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5);

// action clock helpers: play a move so its impact lands at video time `hitAt` (shot local), at speed k
const hitClock = (move, hitAt, k = 1) => ({
  move, moveAt: 0,
  clock: (tl) => (tl - hitAt) * k + MOVES[move].impact * MOVES[move].dur,
});
const loopClock = (move, period, k, offset = 0) => ({
  move, moveAt: 0.08,
  clock: (tl) => ((tl * k + offset) % period),
});
const freezeClock = (move, at, drift = 0) => ({ move, moveAt: 0, clock: (tl) => MOVES[move].impact * MOVES[move].dur + at + tl * drift });

// light each link of the chain while it is moving, so the glow travels foot to fist
const wave = (x) => Math.min(1, 4.5 * x * (1 - x));
const chainHL = (st) => ({ foot: wave(st.c.foot), hips: wave(st.c.hips), shoulders: wave(st.c.shoulders), arm: wave(st.c.arm) });
const AMBER = '#ffb000';
// fixed aim point just in front of the opponent's jaw, so the camera does not chase the head snap
const contactPt = (st) => V(st.OJ.pelvisW.x - 0.2, 1.5, 0.03);

export const board = {
  id: 'punch_with_body',
  duration: 22.667,
  fps: 30,
  style: {
    bg: '#D8EEFE', // pale blue: not the cream used in the previous upload
    // Short form outfit (Sean, Nov 23 2026): gray tank top. Long form uses the black shirt with red side stripes.
    hero: { skin: 0x303137, shirt: '#8a8e96', stripe: null, shorts: 0x1c2747, trim: 0xd1202f, glove: 0x111114, strap: 0xd1202f, scale: 1 },
    opponent: { skin: 0x3a3b41, shirt: '#c41e2a', stripe: null, shorts: 0x131316, trim: 0x131316, glove: 0x111114, strap: 0x9a1520, scale: 1.1 },
  },
  // script, verbatim from Grok's narration, with spoken timings measured from its captions and audio
  script: "You're punching with your arm, not your body. That's why it lands soft. Step one. Pivot the rear foot, heel turning out. Step two. Turn the hips and shoulders through the punch. Step three. Extend the arm last. Snap it back to your guard, chin behind the shoulder. Drive from the ground and it lands hard. So if this is you",
  captions: [
    { start: 0.17, end: 0.85, text: "YOU'RE PUNCHING WITH YOUR" },
    { start: 0.85, end: 1.40, text: 'ARM' },
    { start: 1.58, end: 2.30, text: 'NOT YOUR BODY' },
    { start: 2.62, end: 3.70, text: "THAT'S WHY IT LANDS SOFT" },
    { start: 4.30, end: 4.95, text: 'STEP ONE' },
    { start: 5.18, end: 6.20, text: 'PIVOT THE REAR FOOT' },
    { start: 6.35, end: 7.20, text: 'HEEL TURNING OUT' },
    { start: 7.78, end: 8.45, text: 'STEP TWO' },
    { start: 8.62, end: 9.15, text: 'TURN THE HIPS AND' },
    { start: 9.15, end: 9.66, text: 'SHOULDERS' },
    { start: 9.66, end: 10.30, text: 'THROUGH THE PUNCH' },
    { start: 11.57, end: 12.25, text: 'STEP THREE' },
    { start: 12.38, end: 13.60, text: 'EXTEND THE ARM LAST' },
    { start: 13.97, end: 14.85, text: 'SNAP IT BACK TO' },
    { start: 14.85, end: 15.45, text: 'YOUR GUARD' },
    { start: 15.50, end: 16.45, text: 'CHIN BEHIND THE SHOULDER' },
    { start: 18.07, end: 19.20, text: 'DRIVE FROM THE GROUND' },
    { start: 19.22, end: 20.10, text: 'AND IT LANDS HARD' },
    { start: 20.37, end: 21.95, text: 'SO IF THIS IS YOU' },
  ],
  shots: [
    // HOOK: the mistake, at real speed, from frame 1
    {
      id: 'A', angle: 'side-medium', start: 0, end: 1.30, move: 'cross_arm', moveAt: 0, clock: (tl) => (tl + 0.047) % 0.73,
      top: { text: 'ARM PUNCH' }, mustSee: ['heroHead', 'oppHead'],
      cam: (u, st) => camMove({ az: 0.10, el: 0.05, dist: 5.0, fov: 34 }, { az: 0.16, el: 0.06, dist: 4.5, fov: 34 }, u)(mid(st).setY(1.0)),
      highlight: (u, st) => ({ arm: st.c.arm }),
    },
    {
      id: 'B', angle: 'low-rear-three-quarter', start: 1.30, end: 2.62, ...hitClock('cross_arm', 0.70, 0.6),
      top: { text: ['ZERO', 'HIP TURN'], red: true }, mustSee: ['rearFoot'],
      cam: (u, st) => camMove({ az: -0.75, el: 0.10, dist: 3.4, fov: 34 }, { az: -0.62, el: 0.10, dist: 3.1, fov: 34 }, u)(st.J.pelvisW.clone().setY(0.72)),
      draw2d: (g, st, P, u) => {
        bar(g, P(st.J.hipW.L), P(st.J.hipW.R), '#9aa3b2', 0.5, 16, Math.min(1, u * 4));
        ring(g, P(st.J.ballW.R.clone().add(V(-0.04, 0.03, 0))), 60, '#9aa3b2', Math.min(1, u * 4));
        leader(g, P(st.J.ballW.R), { x: P(st.J.ballW.R).x - 40, y: P(st.J.ballW.R).y + 150 }, 'FOOT STUCK', { bg: '#59606e', alpha: Math.min(1, u * 3) });
      },
    },
    {
      id: 'C', angle: 'contact-close', start: 2.62, end: 4.25, ...hitClock('cross_arm', 0.55, 0.32),
      top: { text: 'LANDS SOFT' }, mustSee: ['oppHead', 'gloveR'],
      cam: (u, st) => camMove({ az: -1.12, el: 0.06, dist: 2.3, fov: 30 }, { az: -1.08, el: 0.07, dist: 1.85, fov: 30 }, u)(contactPt(st)),
      draw2d: (g, st, P, u, tau) => {
        const after = tau - st.impactTau;
        if (after > -0.02 && after < 0.6) ring(g, P(st.OJ.chinW), 70 + after * 120, '#ffffff', Math.max(0, 1 - after * 2), 7);
        if (after > 0.08) pill(g, 540, 1180, 'BARELY MOVES', { bg: '#59606e', alpha: Math.min(1, (after - 0.08) * 6) });
      },
    },
    // STEP 1: feet
    {
      id: 'D1', angle: 'wide-front-low', start: 4.25, end: 5.18, step: 1, ...loopClock('cross_body', 1.6, 0.5, 0.1),
      top: { text: ['IT STARTS', 'AT THE FEET'] }, mustSee: ['rearFoot', 'heroHead'],
      cam: (u, st) => camMove({ az: 0.50, el: 0.10, dist: 4.8, fov: 34 }, { az: 0.42, el: 0.10, dist: 4.4, fov: 34 }, u)(st.J.pelvisW.clone().setY(0.85)),
      noSpeedLines: true,
    },
    {
      id: 'D2', angle: 'rear-foot-ground', start: 5.18, end: 6.32, step: 1, ...loopClock('cross_body', 1.4, 0.55, 0.0),
      top: { text: 'PIVOT REAR FOOT' }, mustSee: ['rearFoot'],
      cam: (u, st) => camMove({ az: 0.10, el: 0.42, dist: 1.9, fov: 32 }, { az: 0.22, el: 0.40, dist: 1.65, fov: 32 }, u)(V(-0.36, 0.02, 0.16)),
      highlight: (u, st) => ({ foot: st.c.foot }),
      fx3d: (grp, st) => { floorArc(grp, st.J.ballW.R, 0.26, 0.78, 0.12, 0xffb000, Math.max(0.15, st.c.foot)); },
      noSpeedLines: true,
    },
    {
      id: 'E', angle: 'feet-overhead', start: 6.32, end: 7.75, ...loopClock('cross_body', 1.45, 0.5, 0.0),
      top: { text: 'HEEL TURNS OUT' }, mustSee: ['rearFoot'],
      cam: (u, st) => {
        const tgt = V(-0.08, 0, 0.02);
        const h = 2.6 - 0.25 * io(u);
        return { pos: tgt.clone().add(V(-0.01, h, 0.001)), target: tgt, fov: 34, up: V(1, 0, 0) };
      },
      highlight: (u, st) => ({ foot: st.c.foot }),
      fx3d: (grp, st) => { footGhost(grp, st.J.ballW.R, 0.78); floorArc(grp, st.J.ballW.R, 0.26, 0.78, 0.12, 0xffb000, 1); },
      draw2d: (g, st, P) => { leader(g, P(st.J.heelW.R), { x: P(st.J.heelW.R).x + 230, y: P(st.J.heelW.R).y + 60 }, 'HEEL', { size: 50 }); },
      noSpeedLines: true,
    },
    // STEP 2: hips then shoulders
    {
      id: 'F', angle: 'high-front-three-quarter', start: 7.75, end: 9.20, step: 2, ...hitClock('cross_body', 0.95, 0.55),
      top: { text: 'TURN THE HIPS' }, mustSee: ['heroHead'],
      cam: (u, st) => camMove({ az: 1.05, el: 0.42, dist: 3.4, fov: 34 }, { az: 0.95, el: 0.40, dist: 3.1, fov: 34 }, u)(st.J.pelvisW.clone().setY(0.95)),
      highlight: (u, st) => ({ hips: st.c.hips }),
      draw2d: (g, st, P) => { bar(g, P(st.J.hipW.L), P(st.J.hipW.R), AMBER, 0.6, 16); },
    },
    {
      id: 'G', angle: 'high-rear-three-quarter', start: 9.20, end: 10.30, ...hitClock('cross_body', 0.95, 0.42),
      top: { text: ['HIPS, THEN', 'SHOULDERS'] }, mustSee: ['heroHead'],
      cam: (u, st) => camMove({ az: -0.55, el: 0.95, dist: 3.6, fov: 34 }, { az: -0.45, el: 0.9, dist: 3.3, fov: 34 }, u)(st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.3).setY(0.95)),
      highlight: (u, st) => ({ hips: st.c.hips * 0.6, shoulders: st.c.shoulders * 0.6 }),
      draw2d: (g, st, P) => {
        bar(g, P(st.J.hipW.L), P(st.J.hipW.R), AMBER, 0.55, 16);
        bar(g, P(st.J.shoulderW.L), P(st.J.shoulderW.R), '#ffffff', 0.35, 16);
        const hp = P(st.J.hipW.R), sp = P(st.J.shoulderW.R);
        pill(g, 800, 1180, 'HIPS', { bg: AMBER, fg: '#141a2e', size: 46 });
        pill(g, 800, 1100, 'SHOULDERS', { bg: '#ffffff', fg: '#141a2e', size: 46 });
      },
    },
    {
      id: 'G2', angle: 'high-front-wide', start: 10.30, end: 11.45, ...hitClock('cross_body', 0.25, 0.5),
      top: { text: ['HIPS, THEN', 'SHOULDERS'] }, mustSee: ['heroHead'],
      cam: (u, st) => camMove({ az: 0.75, el: 0.85, dist: 3.4, fov: 34 }, { az: 0.68, el: 0.8, dist: 3.1, fov: 34 }, u)(st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.3).setY(0.95)),
      highlight: (u, st) => ({ hips: st.c.hips * 0.6, shoulders: st.c.shoulders * 0.6 }),
      draw2d: (g, st, P) => {
        bar(g, P(st.J.hipW.L), P(st.J.hipW.R), AMBER, 0.55, 16);
        bar(g, P(st.J.shoulderW.L), P(st.J.shoulderW.R), '#ffffff', 0.35, 16);
        const hp = P(st.J.hipW.R), sp = P(st.J.shoulderW.R);
        pill(g, 800, 1180, 'HIPS', { bg: AMBER, fg: '#141a2e', size: 46 });
        pill(g, 800, 1100, 'SHOULDERS', { bg: '#ffffff', fg: '#141a2e', size: 46 });
      },
    },
    // STEP 3: arm last, slow motion with the kinetic chain lit in order
    {
      id: 'H1', angle: 'hero-front-medium', start: 11.45, end: 12.38, step: 3,
      move: 'cross_body', moveAt: 0, clock: (tl) => -0.2 + tl * 0.3,
      top: { text: 'ARM GOES LAST' }, mustSee: ['heroHead'],
      cam: (u, st) => camMove({ az: 0.62, el: 0.06, dist: 3.2, fov: 32 }, { az: 0.55, el: 0.06, dist: 2.9, fov: 32 }, u)(st.J.chestW.clone().setY(1.18)),
      noSpeedLines: true,
    },
    {
      id: 'H2', angle: 'side-slow-chain', start: 12.38, end: 13.95, step: 3,
      move: 'cross_body', moveAt: 0, clock: (tl) => 0.0 + tl * 0.24,
      top: { text: 'ARM GOES LAST' }, mustSee: ['heroHead', 'oppHead'],
      cam: (u, st) => camMove({ az: 0.18, el: 0.05, dist: 4.8, fov: 34 }, { az: 0.24, el: 0.05, dist: 4.4, fov: 34 }, u)(mid(st).setY(0.95)),
      highlight: (u, st) => chainHL(st),
      draw2d: (g, st, P) => {
        const items = [['1 FOOT', st.c.foot], ['2 HIPS', st.c.hips], ['3 SHOULDERS', st.c.shoulders], ['4 ARM', st.c.arm]];
        const xs = [140, 340, 590, 830];
        items.forEach(([t, v], i) => pill(g, xs[i], 475, t, v > 0.5 ? { bg: AMBER, fg: '#141a2e', size: 46 } : { bg: '#8b93a3', size: 46 }));
      },
      noSpeedLines: true,
    },
    // snap back: real speed, opponent side angle so the return path is visible
    {
      id: 'I', angle: 'opponent-side', start: 13.95, end: 15.45, ...hitClock('cross_body', 0.30, 1.0),
      top: { text: 'SNAP IT BACK' }, mustSee: ['heroHead', 'gloveR'],
      cam: (u, st) => camMove({ az: 0.42, el: 0.08, dist: 4.0, fov: 32 }, { az: 0.36, el: 0.08, dist: 3.6, fov: 32 }, u)(st.J.headW.clone().lerp(st.OJ.headW, 0.25).setY(1.25)),
      draw2d: (g, st, P, u, tau) => {
        const back = tau - st.impactTau;
        if (back > 0.12 && st.c.arm < 0.2) pill(g, P(st.J.headW).x, P(st.J.headW).y - 190, 'GUARD BACK', { alpha: Math.min(1, (back - 0.12) * 5) });
      },
    },
    {
      id: 'J', angle: 'chin-close', start: 15.45, end: 16.50, ...freezeClock('cross_body', 0.03, 0.012),
      top: { text: 'HIDE THE CHIN' }, mustSee: ['heroHead'],
      cam: (u, st) => camMove({ az: 0.30, el: 0.04, dist: 1.5, fov: 30 }, { az: 0.24, el: 0.04, dist: 1.3, fov: 30 }, u)(st.J.headW.clone().lerp(st.J.shoulderW.R, 0.5)),
      draw2d: (g, st, P, u) => {
        const sp = P(st.J.shoulderW.R);
        leader(g, sp, { x: Math.max(220, sp.x - 230), y: sp.y - 300 }, 'SHOULDER UP', { alpha: Math.min(1, u * 4), size: 52 });
      },
      noSpeedLines: true,
    },
    // narration pause: reset the exchange, build anticipation for the payoff
    {
      id: 'K', angle: 'wide-low-orbit', start: 16.50, end: 18.08, move: 'cross_body', moveAt: 10, clock: (tl) => tl,
      top: { text: 'NOW FULL SPEED' }, mustSee: ['heroHead', 'oppHead'],
      cam: (u, st) => camMove({ az: 0.45, el: 0.0, dist: 5.6, fov: 32 }, { az: 0.05, el: 0.02, dist: 5.1, fov: 32 }, u, sm)(mid(st).setY(1.0)),
    },
    {
      id: 'L', angle: 'ground-behind-rear-leg', start: 18.08, end: 19.28, ...hitClock('cross_body', 0.85, 0.7),
      top: { text: 'FROM THE GROUND' }, mustSee: ['oppHead'],
      cam: (u, st) => camMove({ az: -0.50, el: 0.02, dist: 3.6, fov: 36 }, { az: -0.42, el: 0.03, dist: 3.2, fov: 36 }, u)(st.J.pelvisW.clone().lerp(st.OJ.pelvisW, 0.5).setY(1.0)),
      highlight: (u, st) => chainHL(st),
    },
    // money moment: slow motion hard zoom on contact
    {
      id: 'M', angle: 'contact-hard-zoom', start: 19.28, end: 20.38, ...hitClock('cross_body', 0.42, 0.28),
      top: { text: 'LANDS HARD', red: false }, mustSee: ['oppHead'],
      cam: (u, st) => camMove({ az: -1.25, el: 0.12, dist: 2.9, fov: 30 }, { az: -1.22, el: 0.12, dist: 1.5, fov: 30 }, u, (x) => 1 - Math.pow(1 - x, 4))(contactPt(st)),
      draw2d: (g, st, P, u, tau) => {
        const after = tau - st.impactTau;
        if (after > -0.01 && after < 0.25) ring(g, P(st.OJ.chinW), 80 + after * 600, '#ffffff', Math.max(0, 1 - after * 5), 10);
      },
    },
    // loop back into the hook
    {
      id: 'N1', angle: 'front-three-quarter', start: 20.38, end: 21.40, move: 'cross_arm', moveAt: 10, clock: (tl) => tl,
      top: { text: 'IS THIS YOU' }, mustSee: ['heroHead'],
      cam: (u, st) => camMove({ az: 0.85, el: 0.12, dist: 3.5, fov: 32 }, { az: 0.78, el: 0.12, dist: 3.2, fov: 32 }, u)(st.J.chestW.clone().lerp(st.OJ.chestW, 0.25).setY(1.1)),
    },
    {
      id: 'N2', angle: 'side-low', start: 21.40, end: 22.667, ...hitClock('cross_arm', 0.55),
      top: { text: 'IS THIS YOU' }, mustSee: ['heroHead', 'oppHead'],
      cam: (u, st) => camMove({ az: -0.12, el: 0.0, dist: 5.2, fov: 34 }, { az: -0.05, el: 0.01, dist: 4.8, fov: 34 }, u)(mid(st).setY(1.1)),
      highlight: (u, st) => ({ arm: st.c.arm }),
    },
  ],
};
