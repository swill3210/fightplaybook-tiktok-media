// node render.mjs [still f1,f2,...] | [video out.mp4 [from-to]]
import { bundle } from '@remotion/bundler';
import { renderMedia, renderStill, selectComposition } from '@remotion/renderer';
import path from 'node:path';
const BROWSER = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const [mode, arg, range] = process.argv.slice(2);
const serveUrl = await bundle({ entryPoint: path.resolve('src/index.ts') });
const comp = await selectComposition({ serveUrl, id: 'Liver', browserExecutable: BROWSER, chromiumOptions: { gl: 'swiftshader' } });
if (mode === 'still') {
  for (const f of arg.split(',').map(Number)) {
    await renderStill({ composition: comp, serveUrl, frame: f, output: `qc/still_${String(f).padStart(5, '0')}.png`, browserExecutable: BROWSER });
    console.log('still', f);
  }
} else {
  const fr = range ? range.split('-').map(Number) : null;
  const t0 = Date.now();
  await renderMedia({ composition: comp, serveUrl, codec: 'h264', crf: 17, audioBitrate: '192k', outputLocation: arg, browserExecutable: BROWSER, concurrency: 3, frameRange: fr,
    onProgress: ({ progress }) => { if (Math.round(progress * 100) % 5 === 0) process.stdout.write(`\r${Math.round(progress * 100)}% ${((Date.now() - t0) / 1000).toFixed(0)}s`); } });
  console.log('\ndone', arg);
}
