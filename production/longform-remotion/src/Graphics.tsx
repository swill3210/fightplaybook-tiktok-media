// Engagement graphics (Sean's mandatory rules update, 2026-11-24): keyword chips, liver body map, door counter,
// arrows and target rings drawn in image space, correct vs incorrect cards, beat timing bar, combo chips, chapter progress.
import React from 'react';
import { Img, staticFile } from 'remotion';
import OCC from '../public/occ.json';

type Ctx = { W: number; H: number; FPS: number; WHITE: string; DARK: string; RED: string; AMBER: string;
  wordTime: (re: RegExp, after?: number) => number | undefined; sections: any[]; shots: any[];
  cl: (x: number, a?: number, b?: number) => number; outExpo: (t: number) => number; outBack: (t: number, s?: number) => number; ioCubic: (t: number) => number };
let C: Ctx;
export const initGraphics = (c: Ctx) => { C = c; };

const GREEN = '#1f9d55';
const secStart = (n: string) => C.sections.find((x) => x.name === n).start;
const wt = (re: RegExp, after: number, fb: number) => C.wordTime(re, after) ?? fb;
const shotT = (id: string) => { const s = C.shots.find((x) => x.id === id); return [s.from / C.FPS, s.to / C.FPS]; };

const chipStyle = (bg: string, fg: string, size = 58): React.CSSProperties => ({ fontFamily: 'Bebas', fontSize: size, padding: '4px 24px', borderRadius: 16, background: bg, color: fg, border: `5px solid ${C.DARK}`, boxShadow: `0 8px 0 ${C.DARK}`, whiteSpace: 'nowrap', display: 'inline-flex', alignItems: 'center', gap: 12 });
const Mark: React.FC<{ ok: boolean; s?: number }> = ({ ok, s = 44 }) => (
  <svg width={s} height={s} viewBox="0 0 40 40"><circle cx={20} cy={20} r={18} fill={ok ? GREEN : C.RED} stroke={C.DARK} strokeWidth={3} />
    {ok ? <path d="M11 21 L18 28 L30 13" fill="none" stroke="#fff" strokeWidth={5} strokeLinecap="round" strokeLinejoin="round" />
      : <path d="M13 13 L27 27 M27 13 L13 27" stroke="#fff" strokeWidth={5} strokeLinecap="round" />}</svg>);
const Arrow: React.FC<{ dir: 'up' | 'down' | 'left' | 'right'; s?: number; col?: string }> = ({ dir, s = 44, col = '#fff' }) => {
  const rot = { up: 0, right: 90, down: 180, left: 270 }[dir];
  return <svg width={s} height={s} viewBox="0 0 40 40" style={{ transform: `rotate(${rot}deg)` }}><path d="M20 4 L34 20 H25 V36 H15 V20 H6 Z" fill={col} stroke={C.DARK} strokeWidth={3} strokeLinejoin="round" /></svg>;
};

// ---------- timed screen space events ----------
type Ev = { t0: number; t1: number; at: 'bl' | 'tl' | 'bc' | 'left' | 'center' | 'full'; render: (k: number, t: number) => React.ReactNode; size?: [number, number] };
let EVENTS: Ev[] | null = null;
const chip = (label: string, bg: string, fg: string, icon?: React.ReactNode) => (k: number) =>
  <div style={{ ...chipStyle(bg, fg), transform: `scale(${C.outBack(k / 8)})`, transformOrigin: 'left center' }}>{icon}{label}</div>;
const seq = (items: [number, string, string, string, React.ReactNode?][]) => (k: number, t: number) => {
  const cur = [...items].reverse().find((x) => t >= x[0]); if (!cur) return null; const kk = Math.round((t - cur[0]) * C.FPS);
  return <div style={{ ...chipStyle(cur[2], cur[3]), transform: `scale(${C.outBack(kk / 8)})`, transformOrigin: 'left center' }}>{cur[4]}{cur[1]}</div>;
};
const stack = (items: [number, React.ReactNode][]) => (k: number, t: number) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: 16, alignItems: 'flex-start' }}>
    {items.map(([at, node], n) => { if (t < at) return null; const kk = (t - at) * C.FPS; return <div key={n} style={{ transform: `translateX(${-40 * (1 - C.outExpo(kk / 8))}px) scale(${C.outBack(kk / 8)})`, transformOrigin: 'left center', opacity: C.cl(kk / 3) }}>{node}</div>; })}
  </div>);

function buildEvents(): Ev[] {
  // v3 (visual creative director review 2026-11-24): text adds information instead of echoing the narration;
  // treatments rotate (chips, giant word, wipe labels, diagrams, scoreboard) and each stays at about 3 to 6 uses.
  const { WHITE, DARK, RED, AMBER } = C; const E: Ev[] = [];
  // HOOK
  const tHead = wt(/^head\.$/, 2, 3.1), tChin = wt(/^chin\.$/, 3, 4.2), tLiv = wt(/^liver\.$/, 4.5, 5.3);
  E.push({ t0: tHead - 0.3, t1: tLiv + 1.3, at: 'left', render: (k, t) => <BodyMap k={k} t={t} tHead={tHead} tChin={tChin} tLiv={tLiv} /> });
  const tPow = wt(/^power/, 6, 7.2), tDoor = wt(/^door\.$/, 8, 9.2);
  E.push({ t0: tPow - 0.1, t1: tDoor + 0.9, at: 'bl', render: chip('ANGLE BEATS POWER', RED, WHITE) });
  const tThree = wt(/^three/, 10, 10.7), tOnly = wt(/^only/, 12, 13.0);
  E.push({ t0: tThree - 0.1, t1: Math.min(tOnly + 1.6, secStart('SELF TEST') - 0.15), at: 'bc', render: (k, t) => <Doors k={k} t={t} tOnly={tOnly} />, size: [440, 290] });
  // PAYOFF AT SPEED: door number per strike
  ([['V21', 1], ['V23', 2], ['V24', 3]] as [string, number][]).forEach(([id, n]) => { const [a, b] = shotT(id);
    E.push({ t0: a, t1: b, at: 'bl', render: (k) => <div style={{ ...chipStyle(RED, WHITE, 64), transform: `scale(${C.outBack(k / 6)})` }}>DOOR {n}</div> }); });
  // STEP 1
  const s1 = secStart('STEP 1');
  const tNot = wt(/^not/, s1 + 1.5, 33.1); E.push({ t0: tNot - 0.05, t1: tNot + 0.65, at: 'full', render: (k) => <Giant k={k} word="BAIT" /> });
  const tUp = wt(/^up\.$/, s1 + 5, 36.9); E.push({ t0: tUp - 0.15, t1: tUp + 1.6, at: 'bl', render: chip('RIBS LEFT BARE', AMBER, DARK, <LiverDot />) });
  const tHips = wt(/^hips/, s1, 45.2), tKn = wt(/^knuckles/, s1, 46.2);
  E.push({ t0: tHips - 0.15, t1: tKn - 0.2, at: 'bl', render: (k, t) => <Wipe k={k} left={(tKn - 0.2 - t) * C.FPS} text="POWER FROM HIPS" /> });
  E.push({ t0: tKn - 0.2, t1: tKn + 2.0, at: 'center', render: (k) => <Compare k={k} title="THE HOOK ARM" a={{ src: 'layers/V86_base.png', cx: 760, cy: 430, z: 1.05, ok: true, label: '90 DEGREE L' }} b={{ src: 'layers/ref_V94_old_straightarm.png', cx: 1180, cy: 620, z: 1.0, ok: false, label: 'STRAIGHT ARM' }} /> });
  const tCan = wt(/^cannot/, s1 + 15, 48.3);
  E.push({ t0: tCan - 0.1, t1: secStart('STEP 2') - 0.2, at: 'tl', render: stack([[tCan - 0.1, <div style={chipStyle(WHITE, DARK)}><Mark ok />HEAD COVERED</div>], [tCan + 0.9, <div style={chipStyle(RED, WHITE)}><Mark ok={false} />LIVER OPEN</div>]]) });
  // STEP 2
  const s2 = secStart('STEP 2');
  const tDig = wt(/^dig/, s2, 53.9); E.push({ t0: tDig - 0.1, t1: tDig + 1.9, at: 'bl', render: chip('SLIP = SETUP', WHITE, DARK) });
  const tOut = wt(/^outside/, s2, 56.8); E.push({ t0: tOut - 0.15, t1: tOut + 1.9, at: 'bl', render: (k, t) => <Wipe k={k} left={(tOut + 1.9 - t) * C.FPS} text="HEAD OFF LINE" /> });
  const tOpen = wt(/^open\.$/, s2 + 5, 61.1); E.push({ t0: tOpen - 0.3, t1: tOpen + 1.8, at: 'left', render: (k, t) => <BodyMap k={k} t={t} tHead={1e9} tChin={1e9} tLiv={tOpen} mini /> });
  const tMis = wt(/^mistake/, s2 + 10, 68.1), tSame = wt(/^slip/, tMis + 1.5, 70.7);
  E.push({ t0: tMis - 0.1, t1: tSame + 2.0, at: 'bc', render: (k, t) => <Beat k={k} t={t} tGood={tSame} /> });
  const tMiss = wt(/^misses/, s2 + 15, 73.6), tPays = wt(/^pays/, tMiss, 74.7);
  E.push({ t0: tMiss - 0.1, t1: tPays + 1.4, at: 'tl', render: (k, t) => <Score t={t} tMiss={tMiss} tPays={tPays} /> });
  // STEP 3
  const s3 = secStart('STEP 3');
  const tCrowd = wt(/^crowd/, s3, 80.7); E.push({ t0: tCrowd - 0.1, t1: tCrowd + 1.8, at: 'bl', render: chip('CROWDING? GOOD.', RED, WHITE) });
  const tDrop = wt(/^drop/, s3, 82.7), tBend = wt(/^bend/, tDrop, 83.8);
  E.push({ t0: tDrop - 0.1, t1: tBend - 0.1, at: 'bl', render: chip('LEVEL CHANGE', WHITE, DARK, <Arrow dir="down" col={AMBER} />) });
  E.push({ t0: tBend - 0.1, t1: tBend + 1.0, at: 'bl', render: (k, t) => <Wipe k={k} left={(tBend + 1.0 - t) * C.FPS} text="KNEES, NOT BACK" /> });
  const tShov = wt(/^shovel,/, s3 + 8, 88.6);
  E.push({ t0: tShov - 0.1, t1: tShov + 2.3, at: 'center', render: (k) => <Compare k={k} title="SHOVEL VS HOOK" a={{ src: 'layers/V66_base.png', cx: 1000, cy: 560, z: 0.52, ok: true, label: 'SHOVEL GOES UP', icon: 'up' }} b={{ src: 'layers/V86_base.png', cx: 760, cy: 430, z: 1.05, ok: null, label: 'HOOK GOES ACROSS', icon: 'left' }} /> });
  const tUnder = wt(/^under/, s3 + 10, 91.5); E.push({ t0: tUnder - 0.05, t1: tUnder + 0.7, at: 'full', render: (k) => <Giant k={k} word="BLIND SPOT" /> });
  const tTight = wt(/^tight\.$/, s3 + 15, 94.5); E.push({ t0: tTight - 0.2, t1: tTight + 1.6, at: 'bl', render: chip('ELBOW ON HIP', AMBER, DARK) });
  const tCan3 = wt(/^cannot/, s3 + 18, 96.7); E.push({ t0: tCan3 - 0.1, t1: secStart('COMBO AND RETEST') - 0.2, at: 'tl', render: chip('TOO CLOSE TO BLOCK', RED, WHITE, <Mark ok={false} />) });
  // COMBO AND RETEST
  const s4 = secStart('COMBO AND RETEST');
  const c1 = wt(/^jab/, s4, 101.3), c2 = wt(/^slip/, s4, 104.1), c3 = wt(/^shovel/, s4, 107.2);
  E.push({ t0: c1 - 0.1, t1: c3 + 1.6, at: 'bl', render: (k, t) => <Combo t={t} ts={[c1, c2, c3]} /> });
  const tRe = wt(/^retest/, s4 + 10, 112.2), j1 = wt(/^jabs,/, tRe, 113.4), hk = wt(/^hook\.$/, tRe, 114.6);
  E.push({ t0: tRe - 0.1, t1: hk + 0.9, at: 'bl', render: (k, t) => <div style={{ display: 'flex', gap: 16 }}>{([[tRe, 'ROUND 2', RED, WHITE], [j1, 'JAB', WHITE, DARK], [j1 + 0.3, 'JAB', WHITE, DARK], [hk, 'HOOK LOW', AMBER, DARK]] as [number, string, string, string][]).map(([a, l, bg, fg], n) => t < a - 0.1 ? null : <div key={n} style={{ ...chipStyle(bg, fg), transform: `scale(${C.outBack(((t - a + 0.1) * C.FPS) / 8)})` }}>{l}</div>)}</div> });
  const tCl = wt(/^climbs/, s4 + 15, 116.0), tOwn = wt(/^own/, tCl, 117.4);
  E.push({ t0: tCl - 0.2, t1: tOwn + 1.9, at: 'left', render: (k, t) => <BodyMap k={k} t={t} tHead={tCl} tChin={1e9} tLiv={tOwn - 0.3} covered /> });
  return E;
}

// v4 (Sean 2026-11-25: graphics must never cover the demonstration): every corner overlay goes to the allowed slot with the
// least character coverage over the shots it spans (occ.json from occ.py). Sizes are generous estimates of each overlay.
const SIZE: Partial<Record<Ev['at'], [number, number]>> = { bl: [560, 100], tl: [480, 160], bc: [820, 190], left: [300, 420] };
type Slot = { css: React.CSSProperties; x: number; y: number; right?: boolean };
const SLOTS = (w: number, h: number): Record<string, Slot> => ({
  tl: { css: { left: 60, top: 150 }, x: 60, y: 150 }, tr: { css: { right: 60, top: 150 }, x: C.W - 60 - w, y: 150 },
  bl: { css: { left: 60, bottom: 140 }, x: 60, y: C.H - 140 - h }, br: { css: { right: 60, bottom: 260 }, x: C.W - 60 - w, y: C.H - 260 - h },
  bc: { css: { left: 0, right: 0, bottom: 140, display: 'flex', justifyContent: 'center' }, x: (C.W - w) / 2, y: C.H - 140 - h } });
const PREF: Record<string, string[]> = { bl: ['bl', 'br', 'tl', 'tr', 'bc'], tl: ['tl', 'tr', 'bl', 'br'], bc: ['bc', 'bl', 'br', 'tl', 'tr'], left: ['tl', 'tr', 'bl', 'br'] };
const cover = (id: string, x: number, y: number, w: number, h: number) => { const g = (OCC as any)[id]; if (!g) return 0; let s2 = 0, n = 0;
  for (let r = Math.max(0, Math.floor(y / 40)); r < Math.min(27, Math.ceil((y + h) / 40)); r++) for (let c = Math.max(0, Math.floor(x / 40)); c < Math.min(48, Math.ceil((x + w) / 40)); c++) { s2 += +g[r][c]; n++; }
  return n ? s2 / (9 * n) : 0; };
// the slot is chosen per shot: an overlay may change corner on a cut, never sit on a character
const SLOT_CACHE = new Map<string, React.CSSProperties>();
const pickSlot = (e: Ev, n0: number, f: number): React.CSSProperties => {
  if (!SIZE[e.at]) return POS[e.at]; const sh = C.shots.find((x) => f >= x.from && f < x.to); const key = n0 + '|' + (sh ? sh.id : ''); const hit = SLOT_CACHE.get(key); if (hit) return hit;
  const [w, h] = e.size ?? SIZE[e.at]!; const sl = SLOTS(w, h); const span = sh ? [sh] : [];
  let best = PREF[e.at][0], bs = 1e9;
  PREF[e.at].forEach((k, n) => { const v = span.reduce((a, x) => Math.max(a, cover(x.id, sl[k].x, sl[k].y, w, h)), 0) + 0.01 * n; if (v < bs) { bs = v; best = k; } });
  const css = sl[best].css; SLOT_CACHE.set(key, css); return css; };
const POS: Record<Ev['at'], React.CSSProperties> = {
  bl: { left: 60, bottom: 140 }, tl: { left: 60, top: 150 }, bc: { left: 0, right: 0, bottom: 140, display: 'flex', justifyContent: 'center' },
  left: { left: 60, top: 170 }, center: { inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center', backdropFilter: 'blur(12px)', background: 'rgba(196,214,196,0.25)' },
  full: { inset: 0, display: 'flex', justifyContent: 'center', alignItems: 'center' } };

export const Overlays: React.FC<{ f: number }> = ({ f }) => {
  if (!EVENTS) EVENTS = buildEvents();
  const t = f / C.FPS;
  return <>{EVENTS.map((e, n) => { if (t < e.t0 || t >= e.t1) return null; const k = Math.round((t - e.t0) * C.FPS); const out = C.cl((e.t1 - t) * C.FPS / 6);
    return <div key={n} style={{ position: 'absolute', ...pickSlot(e, n, f), opacity: out }}>{e.render(k, t)}</div>; })}</>;
};

// ---------- pieces ----------
const Rot = () => <svg width={44} height={44} viewBox="0 0 40 40"><path d="M8 22 A12 12 0 1 0 14 10" fill="none" stroke={C.AMBER} strokeWidth={6} strokeLinecap="round" /><path d="M6 4 L16 9 L7 16 Z" fill={C.AMBER} /></svg>;
const LiverDot = () => <svg width={44} height={44} viewBox="0 0 40 40"><path d="M5 18 C6 8 26 6 35 12 C37 20 27 30 14 30 C8 29 5 24 5 18 Z" fill="#8a2b2b" stroke={C.DARK} strokeWidth={3} /></svg>;

const BodyMap: React.FC<{ k: number; t: number; tHead: number; tChin: number; tLiv: number; mini?: boolean; covered?: boolean }> = ({ k, t, tHead, tChin, tLiv, mini, covered }) => {
  const { DARK, RED, AMBER, WHITE } = C; const ent = C.outBack(k / 9) * (mini ? 0.85 : 1);
  const x = (at: number) => C.outBack(((t - at) * C.FPS) / 7);
  const liv = C.cl(((t - tLiv) * C.FPS) / 8); const pulse = liv > 0 ? 1 + 0.08 * Math.sin((t - tLiv) * 9) : 1;
  return (
    <div style={{ width: 400, background: WHITE, border: `6px solid ${DARK}`, borderRadius: 26, boxShadow: `0 10px 0 ${DARK}`, transform: `scale(${ent})`, transformOrigin: 'left top', padding: '10px 0 6px' }}>
      <div style={{ fontFamily: 'Bebas', fontSize: 54, color: DARK, textAlign: 'center', lineHeight: 1 }}>{covered ? 'LIVER OPEN' : mini ? 'OPEN NOW' : 'THE TARGET'}</div>
      <svg width={400} height={460} viewBox="0 0 400 460">
        <circle cx={200} cy={78} r={52} fill="#3a3b41" stroke={DARK} strokeWidth={5} />
        <path d="M168 70 L188 78 M232 70 L212 78" stroke={WHITE} strokeWidth={6} strokeLinecap="round" />
        <rect x={180} y={126} width={40} height={24} fill="#3a3b41" stroke={DARK} strokeWidth={5} />
        <path d="M95 160 Q200 135 305 160 L290 330 Q200 350 110 330 Z" fill={RED} stroke={DARK} strokeWidth={5} />
        {[205, 235, 262].map((y, n) => <path key={n} d={`M${128 + n * 4} ${y} Q200 ${y + 26} ${272 - n * 4} ${y}`} fill="none" stroke="#7d1214" strokeWidth={5} />)}
        <path d="M110 330 L102 440 L190 440 L200 360 L210 440 L298 440 L290 330" fill="#131316" stroke={DARK} strokeWidth={5} />
        {liv > 0 ? <g transform={`translate(150 300) scale(${pulse * liv}) translate(-150 -300)`}>
          <circle cx={150} cy={300} r={58} fill={AMBER} opacity={0.35} />
          <path d="M108 286 C112 266 160 262 192 276 C198 296 172 318 140 318 C120 316 106 304 108 286 Z" fill="#8a2b2b" stroke={DARK} strokeWidth={5} />
        </g> : null}
        {t >= tHead && covered ? <g transform={`translate(200 78) scale(${x(tHead)})`}><circle r={40} fill={GREEN} stroke={DARK} strokeWidth={5} /><path d="M-18 2 L-4 16 L20 -14" fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" /></g> : null}
        {t >= tHead && !covered ? <g transform={`translate(200 78) scale(${x(tHead)})`}><path d="M-44 -44 L44 44 M44 -44 L-44 44" stroke={RED} strokeWidth={14} strokeLinecap="round" /></g> : null}
        {t >= tChin ? <g transform={`translate(200 122) scale(${x(tChin) * 0.55})`}><path d="M-44 -44 L44 44 M44 -44 L-44 44" stroke={RED} strokeWidth={18} strokeLinecap="round" /></g> : null}
      </svg>
      {liv > 0 ? <div style={{ ...chipStyle(AMBER, DARK, 50), position: 'absolute', left: 230, top: 330, transform: `scale(${C.outBack(((t - tLiv) * C.FPS) / 8)})` }}>LIVER</div> : null}
    </div>
  );
};

const Doors: React.FC<{ k: number; t: number; tOnly: number }> = ({ k, t, tOnly }) => {
  const { DARK, WHITE, RED } = C; const dim = C.cl(((t - tOnly) * C.FPS) / 10);
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 14 }}><div style={{ display: 'flex', alignItems: 'flex-end', gap: 26 }}>
      {[1, 2, 3].map((n) => { const u = C.outBack((k - (n - 1) * 5) / 8); const off = n > 1 ? dim : 0;
        return <div key={n} style={{ width: 120, height: 170, borderRadius: '60px 60px 10px 10px', background: off ? '#8b938b' : RED, border: `6px solid ${DARK}`, boxShadow: `0 8px 0 ${DARK}`, transform: `scale(${Math.max(0, u)})`, transformOrigin: 'bottom center', opacity: 1 - 0.45 * off, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Bebas', fontSize: 96, color: WHITE, WebkitTextStroke: `4px ${DARK}`, paintOrder: 'stroke fill' }}>{n}</div>; })}
      </div>{dim > 0 ? <div style={{ ...chipStyle(WHITE, DARK), transformOrigin: 'left center', transform: `scale(${C.outBack(((t - tOnly) * C.FPS) / 8)})` }}>2 DOORS WASTED</div> : null}
    </div>
  );
};

type Panel = { src: string; cx: number; cy: number; z: number; ok: boolean | null; label: string; icon?: 'up' | 'left' };
const Compare: React.FC<{ k: number; title: string; a: Panel; b: Panel }> = ({ k, title, a, b }) => {
  const { DARK, WHITE, RED } = C; const PW = 560, PH = 400;
  const panel = (p: Panel, n: number) => { const u = C.outBack((k - n * 6) / 9); const z = p.z * (1 + 0.04 * C.cl(k / 60));
    const col = p.ok === null ? DARK : p.ok ? GREEN : RED;
    return (
      <div style={{ transform: `scale(${Math.max(0, u)})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10 }}>
        <div style={{ width: PW, height: PH, overflow: 'hidden', position: 'relative', borderRadius: 18, border: `7px solid ${col}`, boxShadow: `0 10px 0 ${DARK}`, background: '#c4d6c4' }}>
          <Img src={staticFile(p.src)} style={{ position: 'absolute', width: 1920 * z, height: 1080 * z, left: PW / 2 - p.cx * z, top: PH / 2 - p.cy * z }} />
          <div style={{ position: 'absolute', right: 12, top: 12 }}>{p.ok === null ? (p.icon ? <Arrow dir={p.icon} col={C.AMBER} s={64} /> : null) : <Mark ok={p.ok} s={64} />}</div>
          {p.ok !== null && p.icon ? <div style={{ position: 'absolute', left: 12, top: 12 }}><Arrow dir={p.icon} col={C.AMBER} s={64} /></div> : null}
        </div>
        <div style={chipStyle(p.ok === false ? RED : WHITE, p.ok === false ? WHITE : DARK, 54)}>{p.label}</div>
      </div>);
  };
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
      <div style={{ ...chipStyle(DARK, WHITE, 50), transform: `scale(${C.outBack(k / 7)})` }}>{title}</div>
      <div style={{ display: 'flex', gap: 46 }}>{panel(a, 0)}{panel(b, 1)}</div>
    </div>);
};

const Beat: React.FC<{ k: number; t: number; tGood: number }> = ({ k, t, tGood }) => {
  const { DARK, WHITE, RED } = C;
  const row = (ok: boolean, cells: string[], at: number) => { if (t < at) return null; const kk = (t - at) * C.FPS;
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: 14, transform: `scale(${C.outBack(kk / 8)})` }}>
        <Mark ok={ok} s={56} />
        {cells.map((c, n) => { const on = kk > 6 + n * 9; return <div key={n} style={{ ...chipStyle(c === '' ? 'transparent' : (ok ? WHITE : '#e9e3d4'), c === '' ? WHITE : DARK, 52), border: c === '' ? `5px dashed ${WHITE}` : `5px solid ${DARK}`, boxShadow: c === '' ? 'none' : `0 8px 0 ${DARK}`, opacity: on ? 1 : 0.12 }}>{c || 'WAIT'}</div>; })}
      </div>);
  };
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 18, alignItems: 'flex-start', background: 'rgba(20,26,46,0.78)', padding: '18px 26px', borderRadius: 22 }}>
      {row(false, ['SLIP', '', 'PUNCH'], t - k / C.FPS)}
      {row(true, ['SLIP + PUNCH', 'SAME BEAT'], tGood - 0.1)}
    </div>);
};

const Combo: React.FC<{ t: number; ts: number[] }> = ({ t, ts }) => {
  const { DARK, WHITE, RED } = C; const labels = ['JAB HOOK', 'SLIP DIG', 'SHOVEL UP'];
  return (
    <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
      {ts.map((a, n) => { if (t < a - 0.1) return null; const kk = (t - a + 0.1) * C.FPS; const cur = n === ts.filter((x) => t >= x - 0.1).length - 1;
        return <React.Fragment key={n}>{n > 0 ? <Arrow dir="right" col={WHITE} s={40} /> : null}
          <div style={{ ...chipStyle(cur ? RED : WHITE, cur ? WHITE : DARK, 50), transform: `scale(${C.outBack(kk / 8)})` }}>
            <span style={{ background: cur ? WHITE : RED, color: cur ? RED : WHITE, borderRadius: 99, width: 46, height: 46, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', border: `4px solid ${DARK}` }}>{n + 1}</span>{labels[n]}</div></React.Fragment>; })}
    </div>);
};

// ---------- chapter progress bar ----------
export const Progress: React.FC<{ f: number }> = ({ f }) => {
  const { W, FPS, DARK, WHITE, RED } = C; const t = f / FPS;
  const ch: [string, string][] = [['HOOK', 'HOOK'], ['SELF TEST', 'TEST'], ['STEP 1', 'DOOR 1'], ['STEP 2', 'DOOR 2'], ['STEP 3', 'DOOR 3'], ['COMBO AND RETEST', 'COMBO'], ['SUMMARY BOARD', 'RECAP'], ['CALL TO ACTION', 'NEXT']];
  const st = ch.map(([n]) => secStart(n)); const end = secStart('SUBSCRIBE'); if (t >= end) return null;
  const total = end, gap = 6, pad = 60, w = W - 2 * pad;
  return (
    <div style={{ position: 'absolute', left: pad, bottom: 26, width: w, height: 14, display: 'flex', gap }}>
      {ch.map(([, lab], n) => { const a = st[n], b = n + 1 < st.length ? st[n + 1] : end; const fill = C.cl((t - a) / (b - a)); const cur = t >= a && t < b;
        return <div key={n} style={{ position: 'relative', flex: `${b - a} 0 0`, height: 14, borderRadius: 7, background: 'rgba(20,26,46,0.35)', overflow: 'visible' }}>
          <div style={{ width: `${fill * 100}%`, height: '100%', borderRadius: 7, background: cur ? RED : WHITE, border: fill > 0 ? `2px solid ${DARK}` : 'none', boxSizing: 'border-box' }} />
          {cur ? <div style={{ position: 'absolute', left: 0, bottom: 18, fontFamily: 'Bebas', fontSize: 52, color: WHITE, WebkitTextStroke: `6px ${DARK}`, paintOrder: 'stroke fill' }}>{lab}</div> : null}
        </div>; })}
    </div>);
};

// ---------- image space annotations (inside the camera transform): arrows, target rings, freeze frame tags ----------
type Ann = { ring?: [number, number, number]; label?: [string, number, number]; arrow?: string; freeze?: boolean };
export const ANN: Record<string, Ann> = {
  V15: { ring: [800, 470, 95], label: ['LIVER', 960, 330] },
  V34: { arrow: 'M1720 250 Q1420 120 1010 400', ring: [940, 450, 120], label: ['TO THE RIBS', 1250, 120] },
  V53: { ring: [690, 460, 90], label: ['DIG THE KNUCKLES', 900, 320], freeze: true },
  V70: { arrow: 'M960 570 Q1010 780 1228 462', ring: [1248, 435, 56], label: ['UP FROM BELOW', 1510, 520], freeze: true },
  V79: { ring: [440, 655, 105] },
  V84: { ring: [810, 460, 95], label: ['DOOR 1', 960, 330] },
  V86: { ring: [700, 460, 95], label: ['DOOR 2', 860, 330] },
  V88: { arrow: 'M1210 650 Q1060 640 905 495', ring: [885, 480, 60] },
};
export const Annotate: React.FC<{ id: string; i: number; dur: number }> = ({ id, i, dur }) => {
  const a = ANN[id]; if (!a) return null; const { DARK, WHITE, AMBER } = C;
  const d0 = 5; const p = C.ioCubic((i - d0) / 12); const ring = C.outBack((i - d0 - 4) / 9);
  return (
    <>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute', left: 0, top: 0 }}>
        {a.arrow ? <>
          <path d={a.arrow} fill="none" stroke={DARK} strokeWidth={22} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} />
          <path d={a.arrow} fill="none" stroke={AMBER} strokeWidth={12} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} />
        </> : null}
        {a.arrow && p > 0.92 ? <ArrowHead path={a.arrow} /> : null}
        {a.ring && ring > 0 ? <g transform={`translate(${a.ring[0]} ${a.ring[1]}) scale(${ring}) rotate(${i * 3})`}>
          <circle r={a.ring[2]} fill="none" stroke={DARK} strokeWidth={16} />
          <circle r={a.ring[2]} fill="none" stroke={AMBER} strokeWidth={9} strokeDasharray="26 16" />
        </g> : null}
        {a.ring && a.label && ring > 0.6 ? <line x1={a.ring[0] + a.ring[2] * 0.7} y1={a.ring[1] - a.ring[2] * 0.7} x2={a.label[1]} y2={a.label[2] + 40} stroke={DARK} strokeWidth={6} /> : null}
      </svg>
      {a.label && i > d0 + 6 ? <div style={{ position: 'absolute', left: a.label[1], top: a.label[2], ...chipStyle(WHITE, DARK, 56), transform: `scale(${C.outBack((i - d0 - 6) / 8)})`, transformOrigin: 'left center' }}>{a.label[0]}</div> : null}
    </>);
};
const ArrowHead: React.FC<{ path: string }> = ({ path }) => {
  const n = path.match(/-?\d+(\.\d+)?/g)!.map(Number); const [x2, y2] = [n[n.length - 2], n[n.length - 1]]; const [x1, y1] = [n[n.length - 4], n[n.length - 3]];
  const ang = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
  return <g transform={`translate(${x2} ${y2}) rotate(${ang})`}><path d="M18 0 L-34 -34 L-22 0 L-34 34 Z" fill={C.AMBER} stroke={C.DARK} strokeWidth={6} strokeLinejoin="round" /></g>;
};
// freeze on contact (v3): no flash (R11); the shot desaturates and viewfinder brackets snap in after the whip lands
export const freezeAmt = (id: string, i: number) => { const a = ANN[id]; if (!a || !a.freeze || i < 8) return 0; return C.cl((i - 8) / 5) * (1 - C.cl((i - 40) / 6)); };
export const FreezeBrackets: React.FC<{ id: string; i: number }> = ({ id, i }) => {
  const u = freezeAmt(id, i); if (u <= 0) return null; const L = 60, T = 8, m = 70 - 20 * u;
  const corner = (x: number, y: number, sx: number, sy: number) => <path key={`${x}${y}`} d={`M${x + sx * L} ${y} H${x} V${y + sy * L}`} fill="none" stroke={C.DARK} strokeWidth={T} />;
  return <svg width={C.W} height={C.H} style={{ position: 'absolute', left: 0, top: 0, opacity: u }}>{[corner(m, m, 1, 1), corner(C.W - m, m, -1, 1), corner(m, C.H - m - 40, 1, -1), corner(C.W - m, C.H - m - 40, -1, -1)]}</svg>;
};

// ---------- v3 treatments: one beat giant word, mask wipe label, scoreboard ----------
const Giant: React.FC<{ k: number; word: string }> = ({ k, word }) => {
  const u = C.cl(k / 4);
  return <>
    <div style={{ position: 'absolute', inset: 0, background: 'rgba(20,26,46,0.35)' }} />
    <div style={{ fontFamily: 'Bebas', fontSize: word.length > 5 ? 330 : 520, lineHeight: 0.9, color: C.WHITE, WebkitTextStroke: `16px ${C.DARK}`, paintOrder: 'stroke fill', transform: `scale(${1.15 - 0.15 * u})`, filter: `blur(${(1 - u) * 6}px)`, letterSpacing: 6, whiteSpace: 'nowrap' }}>{word}</div>
  </>;
};
const Wipe: React.FC<{ k: number; left: number; text: string }> = ({ k, left, text }) => {
  const inn = C.ioCubic(k / 8), out = C.ioCubic((6 - left) / 6);
  const clip = left < 6 ? `inset(0 0 0 ${out * 100}%)` : `inset(0 ${(1 - inn) * 100}% 0 0)`;
  return <div style={{ clipPath: clip }}>
    <div style={{ fontFamily: 'Bebas', fontSize: 84, lineHeight: 1, color: C.WHITE, WebkitTextStroke: `8px ${C.DARK}`, paintOrder: 'stroke fill' }}>{text}</div>
    <div style={{ height: 12, width: `${C.outExpo((k - 4) / 10) * 100}%`, background: C.AMBER, border: `3px solid ${C.DARK}`, marginTop: 6 }} />
  </div>;
};
const Score: React.FC<{ t: number; tMiss: number; tPays: number }> = ({ t, tMiss, tPays }) => {
  const cell = (label: string, n: number, at: number, bg: string, fg: string) => { const kk = (t - at) * C.FPS; const pop = kk >= 0 && kk < 8 ? 1 + 0.2 * Math.sin(Math.PI * kk / 8) : 1;
    return <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}><div style={chipStyle(bg, fg, 56)}>{label}</div><div style={{ ...chipStyle(C.WHITE, C.DARK, 72), minWidth: 60, justifyContent: 'center', transform: `scale(${pop})` }}>{t >= at ? n : 0}</div></div>; };
  return <div style={{ display: 'flex', flexDirection: 'column', gap: 14, transform: `scale(${C.outBack(((t - tMiss + 0.1) * C.FPS) / 8)})`, transformOrigin: 'left top' }}>
    {cell('JAB', 0, 1e9, C.WHITE, C.DARK)}{cell('LIVER', 1, tPays, C.RED, C.WHITE)}
  </div>;
};
