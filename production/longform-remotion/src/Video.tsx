// The Fight Playbook long form: "3 Ways to Target the Liver" upgraded edit.
// Every frame is a pure function of the frame number (deterministic render).
import React from 'react';
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame, interpolate, Easing } from 'remotion';
import { initGraphics, Overlays, Progress, Annotate } from './Graphics';
import TL from '../public/timeline.json';
import CUT from '../public/cutinfo.json';

const W = 1920, H = 1080, FPS = 30;
const SAGE = '#C4D6C4', WHITE = '#ffffff', DARK = '#141a2e', RED = '#d6282a', NAVY = '#1d2a4a', AMBER = '#ffb000';
type Shot = typeof TL.shots[number];
const shots = TL.shots as Shot[];
const sections = TL.sections as any[];
const words: { w: string; s: number; e: number }[] = sections.flatMap((s) => s.words);

// ---------- easing (ported from Grok's build_v4 motion system) ----------
const cl = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const outExpo = (t: number) => { t = cl(t); return t >= 1 ? 1 : 1 - Math.pow(2, -10 * t); };
const inQuad = (t: number) => { t = cl(t); return t * t; };
const ioSine = (t: number) => { t = cl(t); return -(Math.cos(Math.PI * t) - 1) / 2; };
const ioCubic = (t: number) => { t = cl(t); return t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2; };
const outBack = (t: number, s = 1.4) => { t = cl(t); return 1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2; };

const PAYOFF = new Set(['V20', 'V21', 'V22', 'V23', 'V24', 'V25']);
const SECTION_START = new Set(['V13', 'V20', 'V26', 'V44', 'V64', 'V83', 'V102', 'V103']);
const DOOR_START: Record<string, number> = { V26: 1, V44: 2, V64: 3 };
const doorAt = (t: number) => { // door tracker state from section
  const s = sections.find((x) => t >= x.start && t < x.start + x.len);
  return s ? ({ 'STEP 1': 1, 'STEP 2': 2, 'STEP 3': 3, 'COMBO AND RETEST': 4 } as any)[s.name] || 0 : 0;
};
const wordTime = (re: RegExp, after = 0) => words.find((w) => w.s >= after && re.test(w.w.toLowerCase()))?.s;

// ---------- camera per angle (Grok's move(), with contact push and decaying shake) ----------
function camera(s: Shot, i: number) {
  const n = s.dur; const t = i / Math.max(n - 1, 1); const e = ioSine(t);
  let z = 1.0, cx = W / 2, cy = H / 2, rot = 0, sh = [0, 0];
  const g = s.glove as any;
  if (s.id === 'V35' && g) { const u = ioCubic((i - 9) / 63); return { z: 1 + 0.65 * u, cx: g[0], cy: g[1], rot: 0, sh }; }
  if (g) {
    const k0 = s.phase_frames || 0;
    if (i < k0) { const u = i / Math.max(k0 - 1, 1); return { z: 1 + 0.015 * ioSine(u), cx, cy, rot, sh }; }
    const j = i - k0, m = n - k0;
    z = j < 7 ? 1.02 + 0.05 * outBack(j / 7, 1.2) : 1.07 + 0.02 * ioSine((j - 7) / Math.max(m - 8, 1));
    const bz = (s as any).bz || 1; z *= bz;
    const w = Math.min(1, 0.35 + 0.6 * (bz - 1)) * outExpo(j / 7); cx += (g[0] - cx) * w; cy += (g[1] - cy) * w;
    const amp = [7, -6, 4, -2, 1]; if (j < 5) sh = [amp[j], -amp[j] * 0.6];
    if (PAYOFF.has(s.id)) z += 0.12 * (1 - outExpo(i / 6));
    return { z, cx, cy, rot, sh };
  }
  const a = s.angle;
  if (a.includes('wide')) z = 1 + 0.06 * e;
  else if (['medium side', 'low side', 'front three quarter'].includes(a)) { z = 1.02 + 0.03 * e; cx += -20 + 40 * e; }
  else if (a.includes('over the shoulder')) { z = 1.03 + 0.04 * e; cx += 30 * e; }
  else if (a.includes('behind the opponent')) z = 1.07 - 0.05 * e;
  else if (a.includes('overhead')) { z = 1.06 + 0.03 * e; rot = 1.5 * e; }
  else if (a.includes('worms eye')) { z = 1.03 + 0.04 * e; cy += 15 - 30 * e; }
  else if (a.includes('Dutch')) { z = 1.05 + 0.03 * e; rot = -1.0 * e; }
  else if (a.includes('eyes')) z = 1 + 0.10 * e;
  else if (a.includes('first person')) z = 1.02 + 0.04 * e;
  else z = 1 + 0.06 * e;
  if (s.section === 'CALL TO ACTION' || s.section === 'SUBSCRIBE') z += 0.08 * e;
  if (PAYOFF.has(s.id)) z += 0.12 * (1 - outExpo(i / 6));
  return { z, cx, cy, rot, sh };
}
initGraphics({ W, H, FPS, WHITE, DARK, RED, AMBER, wordTime, sections, shots, cl, outExpo, outBack, ioCubic });
// stills redrawn on the liver side (hero on the right): whip pan when the screen side changes
const FLIP = new Set(['V3', 'V9', 'V15', 'V20', 'V21', 'V23', 'V24', 'V33', 'V34', 'V53', 'V70', 'V84', 'V86', 'V88', 'V94']);
const PARALLAX = (a: string) => /wide|side|three quarter|overhead|behind|over the shoulder|worms eye/.test(a);

// ---------- one shot (stills and motion) ----------
const ShotView: React.FC<{ s: Shot; i: number }> = ({ s, i }) => {
  const c = camera(s, i);
  const hw = W / (2 * c.z), hh = H / (2 * c.z);
  const cx = Math.min(Math.max(c.cx - c.sh[0] / c.z, hw), W - hw), cy = Math.min(Math.max(c.cy - c.sh[1] / c.z, hh), H - hh);
  const L = s.layers as any; const phase = L.a && i < (s.phase_frames || 0);
  const info = (CUT as any)[s.id];
  const par = !phase && info && PARALLAX(s.angle) && !s.glove;
  const pz = par ? 1 + 0.022 * ioSine(i / Math.max(s.dur - 1, 1)) : 1; // characters grow slightly faster than the plate, about the feet
  const g = s.glove as any; const j = i - (s.phase_frames || 0);
  const p = s.id === 'V35' ? 1 : outExpo((j + 1) / 4);
  const mask = g ? `radial-gradient(circle at ${g[0]}px ${g[1]}px, black ${120 + 600 * p}px, transparent ${121 + 600 * p}px)` : undefined;
  const bg = info ? `rgb(${info.bg.map((x: number) => Math.round(x)).join(',')})` : SAGE;
  const si = shots.indexOf(s); const prev = si > 0 ? shots[si - 1] : null; const whip = prev && FLIP.has(s.id) !== FLIP.has(prev.id) && i < 7 ? 1 - outExpo(i / 7) : 0;
  const wdir = FLIP.has(s.id) ? -1 : 1;
  return (
    <AbsoluteFill style={{ background: bg, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', width: W, height: H, transformOrigin: '0 0', filter: whip ? `blur(${18 * whip}px)` : undefined,
        transform: `translateX(${wdir * whip * 420}px) translate(${W / 2}px, ${H / 2}px) scale(${c.z}) rotate(${c.rot}deg) translate(${-cx}px, ${-cy}px)` }}>
        {phase ? <Img src={staticFile(L.a)} style={{ position: 'absolute', width: W, height: H }} /> : par ? (
          <>
            <Img src={staticFile(L.base.replace('_base', '_plate'))} style={{ position: 'absolute', width: W, height: H }} />
            <Img src={staticFile(L.base.replace('_base', '_cut'))} style={{ position: 'absolute', width: W, height: H, transformOrigin: `${W / 2}px ${info.feet}px`, transform: `scale(${pz})` }} />
          </>
        ) : <Img src={staticFile(L.base)} style={{ position: 'absolute', width: W, height: H }} />}
        {!phase && L.lines && j >= 0 ? <Img src={staticFile(L.lines)} style={{ position: 'absolute', width: W, height: H, WebkitMaskImage: mask, maskImage: mask }} /> : null}
        <Annotate id={s.id} i={i} dur={s.dur} />
      </div>
    </AbsoluteFill>
  );
};

// ---------- kinetic headline: words slam in on the spoken word ----------
const Headline: React.FC<{ s: Shot; i: number }> = ({ s, i }) => {
  if (!s.text.length || s.id === 'V102' || s.id === 'V107') return null;
  const t0 = s.from / FPS;
  return (
    <div style={{ position: 'absolute', top: 54, width: W, textAlign: 'center' }}>
      {s.text.map((line, li) => {
        const first = line.split(' ')[0].toLowerCase().replace(/[^a-z]/g, '');
        const spoken = wordTime(new RegExp('^' + first), t0 - 0.6);
        const startF = s.id === 'V2' ? -2 : Math.max(0, Math.round(((spoken !== undefined && spoken < s.to / FPS ? spoken : t0) - t0) * FPS) - 2) + li * 4;
        return (
          <div key={li} style={{ lineHeight: 1.02 }}>
            {line.split(' ').map((wd, wi) => {
              const k = i - startF - wi * 3; const u = outBack(k / 8, 1.6); const op = cl(k / 3);
              return <span key={wi} style={{ display: 'inline-block', margin: '0 14px', fontFamily: 'Bebas', fontSize: 142, color: li === s.text.length - 1 && s.text.length > 1 ? RED : WHITE,
                WebkitTextStroke: `10px ${DARK}`, paintOrder: 'stroke fill', opacity: op, transform: `translateY(${(1 - cl(k / 6)) * 30}px) scale(${0.6 + 0.4 * u})`, filter: `drop-shadow(0 6px 0 ${DARK})` }}>{wd}</span>;
            })}
          </div>
        );
      })}
    </div>
  );
};

// ---------- door tracker (3 pips, top right) and door count in ----------
const DoorUI: React.FC<{ f: number }> = ({ f }) => {
  const t = f / FPS; const d = doorAt(t); if (!d) return null;
  const sec = sections.find((x) => t >= x.start && t < x.start + x.len); const k = f - Math.round(sec.start * FPS);
  const ent = outExpo(k / 12);
  return (
    <div style={{ position: 'absolute', right: 64, top: 48, display: 'flex', gap: 18 }}>
      {[1, 2, 3].map((p) => { const on = d === 4 || p === d; const pop = on && k < 10 ? 1 + 0.35 * Math.sin(Math.PI * cl(k / 10)) : 1;
        return <div key={p} style={{ width: 34 * pop, height: 34 * pop, borderRadius: 99, background: on ? RED : WHITE, border: `5px solid ${DARK}`, transform: `translateY(${-20 * (1 - ent)}px)` }} />; })}
    </div>
  );
};
const DoorCountIn: React.FC<{ s: Shot; i: number }> = ({ s, i }) => {
  const n = DOOR_START[s.id]; if (!n) return null;
  const roll = outExpo((i - 4) / 10); const out = cl((i - 32) / 8);
  return (
    <div style={{ position: 'absolute', left: 60, top: 40, display: 'flex', alignItems: 'center', gap: 16, opacity: 1 - out, transform: `translateX(${-60 * (1 - outExpo(i / 8))}px)` }}>
      <div style={{ fontFamily: 'Bebas', fontSize: 64, color: WHITE, WebkitTextStroke: `8px ${DARK}`, paintOrder: 'stroke fill' }}>DOOR</div>
      <div style={{ width: 96, height: 96, borderRadius: 99, background: RED, border: `6px solid ${DARK}`, overflow: 'hidden', position: 'relative' }}>
        {[n - 1, n].map((v, k) => <div key={k} style={{ position: 'absolute', width: '100%', textAlign: 'center', fontFamily: 'Bebas', fontSize: 84, lineHeight: '96px', color: WHITE, transform: `translateY(${(k - roll) * 96}px)` }}>{v}</div>)}
      </div>
    </div>
  );
};

// ---------- animated numbers: 90 degree elbow gauge, dose counters ----------
const NINETY = wordTime(/^ninety/);
const Gauge: React.FC<{ f: number }> = ({ f }) => {
  if (NINETY === undefined) return null; const k = f - Math.round(NINETY * FPS) + 6; if (k < 0 || k > 60) return null;
  const u = ioCubic(k / 18); const v = Math.round(90 * u); const out = cl((k - 50) / 10); const r = 70, a = (u * 90 * Math.PI) / 180;
  return (
    <div style={{ position: 'absolute', right: 70, top: 120, opacity: 1 - out, transform: `scale(${0.8 + 0.2 * outBack(k / 8)})`, display: 'flex', alignItems: 'center', gap: 14, background: WHITE, border: `6px solid ${DARK}`, borderRadius: 22, padding: '10px 22px' }}>
      <svg width={170} height={170} viewBox="-20 -150 170 170">
        <line x1={0} y1={0} x2={r * 1.6} y2={0} stroke={DARK} strokeWidth={14} strokeLinecap="round" />
        <line x1={0} y1={0} x2={Math.cos(a) * r * 1.6} y2={-Math.sin(a) * r * 1.6} stroke={RED} strokeWidth={14} strokeLinecap="round" />
        <path d={`M ${r} 0 A ${r} ${r} 0 0 0 ${Math.cos(a) * r} ${-Math.sin(a) * r}`} fill="none" stroke={AMBER} strokeWidth={8} />
      </svg>
      <div style={{ fontFamily: 'Bebas', fontSize: 120, color: DARK, minWidth: 150 }}>{v}°</div>
    </div>
  );
};
const Dose: React.FC<{ f: number }> = ({ f }) => {
  const s = shots.find((x) => { if (!x.dose || f < x.from || f >= x.from + 3 * FPS) return false; const sec = sections.find((y) => y.name === x.section); return f < Math.round((sec.start + sec.len) * FPS) - 2; }); if (!s) return null;
  const k = f - s.from; const u = outExpo((k - 3) / 12); const out = cl((k - 80) / 10);
  const parts = s.dose.includes(', ') ? s.dose.split(', ') : s.dose.replace(/^(\d+ ROUNDS) (.+)$/, '$1|$2').split('|'); // max 3 words per line
  const count = (txt: string, idx: number) => idx === 0 ? txt : txt.replace(/\d+/, (m) => String(Math.max(2, Math.round(Number(m) * ioCubic((k - 6) / 20)))));
  return (
    <div style={{ position: 'absolute', right: 60, bottom: 70, transform: `translateX(${(1 - u) * 520}px)`, opacity: 1 - out, background: RED, border: `6px solid ${WHITE}`, borderRadius: 20, padding: '10px 30px', boxShadow: `0 10px 0 ${DARK}` }}>
      {parts.map((p, i) => <div key={i} style={{ fontFamily: 'Bebas', fontSize: 68, color: WHITE, lineHeight: 1.05 }}>{count(p, i)}</div>)}
    </div>
  );
};

// ---------- self test chips synced to the words ----------
const SelfTest: React.FC<{ f: number }> = ({ f }) => {
  const sec = sections.find((x) => x.name === 'SELF TEST'); const t = f / FPS; if (t < sec.start || t >= sec.start + sec.len) return null;
  const items: [string, number | undefined, string][] = [['JAB', wordTime(/^jabs/, sec.start), WHITE], ['JAB', (wordTime(/^jabs/, sec.start) ?? 0) + 0.25, WHITE], ['HOOK LOW', wordTime(/^hook/, sec.start), RED], ['RIBS OPEN?', wordTime(/^liver/, sec.start), AMBER]];
  return (
    <div style={{ position: 'absolute', left: 60, bottom: 70, display: 'flex', gap: 18 }}>
      {items.map(([label, at, col], i) => { if (at === undefined) return null; const k = f - Math.round(at * FPS); if (k < 0) return null; const u = outBack(k / 8);
        return <div key={i} style={{ fontFamily: 'Bebas', fontSize: 58, padding: '6px 24px', borderRadius: 16, background: col, color: col === WHITE || col === AMBER ? DARK : WHITE, border: `5px solid ${DARK}`, transform: `scale(${u})` }}>{label}</div>; })}
    </div>
  );
};
const FullSpeed: React.FC<{ f: number }> = ({ f }) => {
  const sec = sections.find((x) => x.name === 'PAYOFF AT SPEED'); const k = f - Math.round(sec.start * FPS); if (k < 0 || k >= sec.len * FPS) return null;
  return <div style={{ position: 'absolute', left: 60, top: 50, fontFamily: 'Bebas', fontSize: 62, background: RED, color: WHITE, padding: '4px 26px', borderRadius: 14, border: `5px solid ${DARK}`, transform: `scale(${outBack(k / 8)})` }}>FULL SPEED</div>;
};

// ---------- summary board, word by word, door cards on their spoken words ----------
const Board: React.FC<{ s: Shot; i: number }> = ({ s, i }) => {
  const t0 = s.from / FPS; const f = s.from + i;
  const at = (re: RegExp) => { const w = wordTime(re, t0 - 0.3); return w === undefined ? s.from : Math.round(w * FPS); };
  const tThree = wordTime(/^three/, t0 - 0.3) ?? t0; const tHigh = wordTime(/^high\.$/, tThree) ?? tThree; const tLow = wordTime(/^low\.$/, tHigh) ?? tHigh; const tLiv = wordTime(/^liver\.$/, tLow) ?? tLow;
  const mantra: [string, number][] = [['HIGH.', Math.round(tHigh * FPS)], ['LOW.', Math.round(tLow * FPS)], ['LIVER.', Math.round(tLiv * FPS)]];
  const doors = [['DOOR ONE', 'JAB HIGH', 'HOOK LOW', at(/^one/)], ['DOOR TWO', 'SLIP THE JAB', 'DIG THE LIVER', at(/^two/)], ['DOOR THREE', 'SHOVEL UPPERCUT', 'UP CLOSE', at(/^three/)]] as [string, string, string, number][];
  const chip = outExpo((i - 16) / 12);
  return (
    <AbsoluteFill style={{ background: SAGE, transform: `scale(${1 + 0.05 * ioSine(i / Math.max(s.dur - 1, 1))})` }}>
      <div style={{ position: 'absolute', top: 30, width: W, textAlign: 'center' }}>
        {mantra.map(([w, f0], k) => { const u = outExpo((f - f0) / 8); return <span key={k} style={{ display: 'inline-block', margin: '0 22px', fontFamily: 'Bebas', fontSize: 190, color: WHITE, WebkitTextStroke: `11px ${DARK}`, paintOrder: 'stroke fill', opacity: cl(u * 1.3), transform: `scale(${1.18 - 0.18 * u})` }}>{w}</span>; })}
      </div>
      <div style={{ position: 'absolute', top: 250, width: W, textAlign: 'center', opacity: chip, transform: `translateY(${30 * (1 - chip)}px)` }}>
        <span style={{ fontFamily: 'Bebas', fontSize: 64, background: RED, color: WHITE, padding: '8px 28px', borderRadius: 18, border: `5px solid ${WHITE}` }}>SCREENSHOT THIS</span>
      </div>
      <div style={{ position: 'absolute', top: 400, left: (W - 3 * 520 - 2 * 60) / 2, display: 'flex', gap: 60 }}>
        {doors.map(([a, b, c2, f0], k) => { const u = outExpo((f - f0) / 14); const next = k < 2 ? doors[k + 1][3] : Math.round(tHigh * FPS); const live = f >= f0 && f < next;
          return <div key={k} style={{ width: 520, height: 610, background: WHITE, border: `8px solid ${live ? RED : NAVY}`, borderRadius: 30, boxShadow: '10px 12px 0 #000', opacity: cl(u * 1.3), transform: `translateY(${-80 * (1 - u)}px) scale(${live ? 1.04 : 1})`, textAlign: 'center', paddingTop: 40 }}>
            <div style={{ fontFamily: 'Bebas', fontSize: 96, color: RED }}>{a}</div>
            <div style={{ height: 5, background: NAVY, margin: '20px 60px 40px' }} />
            <div style={{ fontFamily: 'Bebas', fontSize: b.length > 13 ? 76 : 88, color: NAVY, lineHeight: 1.7 }}>{b}<br />{c2}</div>
          </div>; })}
      </div>
    </AbsoluteFill>
  );
};

// ---------- call to action chips and subscribe card ----------
const CTA: React.FC<{ f: number }> = ({ f }) => {
  const sec = sections.find((x) => x.name === 'CALL TO ACTION'); const t = f / FPS; if (t < sec.start || t >= sec.start + sec.len + 3.2) return null;
  const ts = [wordTime(/^1,?/, sec.start), wordTime(/^2,?/, sec.start), wordTime(/^3,?/, sec.start)];
  return (
    <div style={{ position: 'absolute', top: 60, width: W, display: 'flex', justifyContent: 'center', gap: 30 }}>
      {ts.map((at, k) => { if (at === undefined) return null; const kk = f - Math.round(at * FPS); if (kk < 0) return null;
        return <div key={k} style={{ width: 130, height: 130, borderRadius: 99, background: RED, border: `7px solid ${WHITE}`, fontFamily: 'Bebas', fontSize: 104, color: WHITE, textAlign: 'center', lineHeight: '130px', transform: `scale(${outBack(kk / 8)})`, boxShadow: `0 8px 0 ${DARK}` }}>{k + 1}</div>; })}
    </div>
  );
};
const Subscribe: React.FC<{ s: Shot; i: number }> = ({ s, i }) => {
  if (s.id !== 'V107') return null; const u = outExpo((i - 6) / 12); const press = i >= 36 && i <= 44 ? 1 - 0.06 * Math.sin(Math.PI * (i - 36) / 8) : 1;
  return (
    <div style={{ position: 'absolute', right: 120, bottom: 150, transform: `translateX(${(1 - u) * 900}px) scale(${press})`, fontFamily: 'Bebas', fontSize: 120, background: RED, color: WHITE, padding: '10px 60px', borderRadius: 24, border: `8px solid ${WHITE}`, boxShadow: `0 12px 0 ${DARK}` }}>SUBSCRIBE</div>
  );
};

// ---------- section push transition ----------
const Push: React.FC<{ k: number; f: number }> = ({ k, f }) => {
  const s = shots[k]; const i = f - s.from;
  const prev = shots[k - 1]; const po = i < 6 ? inQuad(i / 6) : 1; const pi = outExpo((i + 1) / 9);
  return (
    <AbsoluteFill style={{ background: SAGE }}>
      {po < 1 ? <AbsoluteFill style={{ transform: `translateX(${-W * po}px)` }}>{prev.id === 'V102' ? <Board s={prev} i={prev.dur - 1} /> : <ShotView s={prev} i={prev.dur - 1} />}</AbsoluteFill> : null}
      <AbsoluteFill style={{ transform: `translateX(${W * (1 - pi)}px)` }}>{s.id === 'V102' ? <Board s={s} i={i} /> : <ShotView s={s} i={i} />}</AbsoluteFill>
    </AbsoluteFill>
  );
};

export const LiverVideo: React.FC = () => {
  const f = useCurrentFrame();
  const k = shots.findIndex((s) => f >= s.from && f < s.to); const s = shots[Math.max(0, k)]; const i = f - s.from;
  const music = (fr: number) => {
    let v = 0.085; for (const m of TL.music_lifts as number[]) if (fr >= m && fr < m + 45) v *= 1.26;
    return v * interpolate(fr, [TL.frames - 60, TL.frames], [1, 0.2], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  };
  return (
    <AbsoluteFill style={{ background: SAGE }}>
      <style>{`@font-face { font-family: 'Bebas'; src: url('${staticFile('BebasNeue-Regular.ttf')}'); }`}</style>
      {SECTION_START.has(s.id) && i < 9 && k > 0 ? <Push k={k} f={f} /> : s.id === 'V102' ? <Board s={s} i={i} /> : <ShotView s={s} i={i} />}
      <Headline s={s} i={i} />
      <DoorUI f={f} /><DoorCountIn s={s} i={i} /><Gauge f={f} /><Dose f={f} /><SelfTest f={f} /><FullSpeed f={f} /><CTA f={f} /><Subscribe s={s} i={i} />
      <Overlays f={f} /><Progress f={f} />
      <Audio src={staticFile('lofi_bed.mp3')} volume={music} loop />
      {sections.filter((x) => x.vo).map((x, n) => <Sequence key={n} from={Math.round(x.vo_at * FPS)}><Audio src={staticFile(x.vo)} volume={1} /></Sequence>)}
      {(TL.sfx as any[]).map((e, n) => <Sequence key={'s' + n} from={e.frame} durationInFrames={20}><Audio src={staticFile(e.type === 'whoosh' ? 'whoosh.mp3' : 'thud.mp3')} volume={e.type === 'whoosh' ? 0.16 : 0.22} /></Sequence>)}
    </AbsoluteFill>
  );
};
