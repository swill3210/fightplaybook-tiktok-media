// Usage: node render.mjs <board> <outdir> [--frames a:b] [--still t1,t2,...]
// Renders frames headless, pipes them to ffmpeg, writes per frame QC metrics to qc_frames.json
import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_PATH || '/opt/node22/lib/node_modules/playwright');
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';

const [board, outdir, ...rest] = process.argv.slice(2);
const arg = (k) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : null; };
fs.mkdirSync(outdir, { recursive: true });
const root = path.dirname(new URL(import.meta.url).pathname);
const types = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.html': 'text/html', '.woff2': 'font/woff2', '.json': 'application/json' };
const srv = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(res);
}).listen(0);
const port = srv.address().port;

const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1920 } });
page.on('console', (m) => { if (m.type() === 'error') console.error('PAGE', m.text()); });
page.on('pageerror', (e) => { console.error('PAGEERR', e.message, e.stack); process.exit(1); });
await page.goto(`http://localhost:${port}/index.html?board=${board}`);
await page.waitForFunction('window.FP_READY === true', null, { timeout: 120000 });
const meta = await page.evaluate(() => window.FP.board);
console.log('stage', JSON.stringify(await page.evaluate(() => window.FP.stage)));
if (process.env.FP_SHOV) await page.evaluate((v) => { window.FP_SHOV = JSON.parse(v); }, process.env.FP_SHOV);
if (rest.includes('--pose')) await page.evaluate(() => { window.FP_POSE = true; });
if (arg('--cam')) await page.evaluate((c) => { window.FP_CAM = c.split(',').map(Number); }, arg('--cam'));

const grab = async (t) => {
  const m = await page.evaluate((t) => window.FP.render(t), t);
  const b64 = await page.evaluate(() => document.querySelectorAll('canvas')[document.querySelectorAll('canvas').length - 1].toDataURL('image/png').split(',')[1]);
  return [m, Buffer.from(b64, 'base64')];
};

const stills = arg('--still');
if (stills) {
  for (const t of stills.split(',').map(Number)) {
    const [m, png] = await grab(t);
    fs.writeFileSync(path.join(outdir, `still_${t.toFixed(2)}.png`), png);
    console.log(t, m.shot, 'elbowR', m.elbowR, 'elbowL', m.elbowL, 'forearmUpR', m.forearmUpR, 'reach', m.reach, m.issues.join('; '));
  }
} else {
  const fps = meta.fps, N = Math.round(meta.duration * fps);
  const [a, b] = (arg('--frames') || `0:${N}`).split(':').map(Number);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', path.join(outdir, 'video_silent.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const qc = [];
  const t0 = Date.now();
  for (let f = a; f < b; f++) {
    const [m, png] = await grab(f / fps);
    qc.push({ f, ...m });
    if (!ff.stdin.write(png)) await new Promise((r) => ff.stdin.once('drain', r));
    if (f % 60 === 0) console.log(`frame ${f}/${b} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
  fs.writeFileSync(path.join(outdir, 'qc_frames.json'), JSON.stringify({ meta, frames: qc }, null, 1));
}
await browser.close(); srv.close();
