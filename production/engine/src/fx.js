// Shared visual explanation helpers (2D overlay and flat 3D floor graphics).
import * as THREE from 'three';

const RED = '#e3242f', NAVY = '#141a2e';

export function pill(g, x, y, text, { bg = RED, fg = '#fff', size = 46, alpha = 1 } = {}) {
  g.save(); g.globalAlpha = alpha;
  g.font = `${size}px "Bebas Neue"`; g.textAlign = 'center'; g.textBaseline = 'middle';
  const w = g.measureText(text).width + size * 0.8, h = size * 1.25;
  g.fillStyle = bg; g.strokeStyle = NAVY; g.lineWidth = 5;
  g.beginPath(); g.roundRect(x - w / 2, y - h / 2, w, h, h / 2); g.fill(); g.stroke();
  g.fillStyle = fg; g.fillText(text, x, y + 2); g.restore();
}

// thick line through two projected points, extended past both ends
export function bar(g, a, b, color, ext = 0.45, width = 16, alpha = 1) {
  const dx = b.x - a.x, dy = b.y - a.y;
  const p0 = { x: a.x - dx * ext, y: a.y - dy * ext }, p1 = { x: b.x + dx * ext, y: b.y + dy * ext };
  g.save(); g.globalAlpha = alpha; g.lineCap = 'round';
  g.strokeStyle = NAVY; g.lineWidth = width + 10; g.beginPath(); g.moveTo(p0.x, p0.y); g.lineTo(p1.x, p1.y); g.stroke();
  g.strokeStyle = color; g.lineWidth = width; g.beginPath(); g.moveTo(p0.x, p0.y); g.lineTo(p1.x, p1.y); g.stroke();
  for (const p of [p0, p1]) { g.fillStyle = color; g.strokeStyle = NAVY; g.lineWidth = 5; g.beginPath(); g.arc(p.x, p.y, width * 0.9, 0, 7); g.fill(); g.stroke(); }
  g.restore();
}

export function ring(g, p, r, color = RED, alpha = 1, width = 9) {
  g.save(); g.globalAlpha = alpha;
  g.strokeStyle = NAVY; g.lineWidth = width + 8; g.beginPath(); g.arc(p.x, p.y, r, 0, 7); g.stroke();
  g.strokeStyle = color; g.lineWidth = width; g.beginPath(); g.arc(p.x, p.y, r, 0, 7); g.stroke();
  g.restore();
}

export function leader(g, from, to, text, opts = {}) {
  g.save(); g.strokeStyle = NAVY; g.lineWidth = 5; g.globalAlpha = opts.alpha ?? 1;
  g.beginPath(); g.moveTo(from.x, from.y); g.lineTo(to.x, to.y); g.stroke(); g.restore();
  pill(g, to.x, to.y, text, opts);
}

// flat arc arrow on the floor around a centre point, from yaw a0 to a1 (fighter toe yaw convention)
export function floorArc(group, centre, radius, yaw0, yaw1, color = 0xe3242f, prog = 1) {
  const th0 = Math.PI - yaw0, th1 = Math.PI - (yaw0 + (yaw1 - yaw0) * prog);
  const start = Math.min(th0, th1), len = Math.abs(th1 - th0);
  if (len < 0.02) return;
  const mat = new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.95, depthWrite: false });
  const edge = new THREE.MeshBasicMaterial({ color: 0x141a2e, depthWrite: false });
  const mk = (r0, r1, m, y) => {
    const ringM = new THREE.Mesh(new THREE.RingGeometry(r0, r1, 48, 1, start, len), m);
    ringM.rotation.x = -Math.PI / 2; ringM.position.set(centre.x, y, centre.z); group.add(ringM);
  };
  mk(radius - 0.026, radius + 0.026, edge, 0.003);
  mk(radius - 0.016, radius + 0.016, mat, 0.004);
  // arrow head at th1, pointing along increasing theta direction of travel
  const dirSign = th1 > th0 ? 1 : -1;
  const hx = Math.cos(th1) * radius, hy = Math.sin(th1) * radius;
  const tx = -Math.sin(th1) * dirSign, ty = Math.cos(th1) * dirSign;
  const nx = Math.cos(th1), ny = Math.sin(th1);
  const s = 0.05;
  const shape = new THREE.Shape();
  shape.moveTo(hx + tx * s * 1.4, hy + ty * s * 1.4);
  shape.lineTo(hx + nx * s, hy + ny * s);
  shape.lineTo(hx - nx * s, hy - ny * s);
  const tri = new THREE.Mesh(new THREE.ShapeGeometry(shape), mat);
  tri.rotation.x = -Math.PI / 2; tri.position.set(centre.x, 0.005, centre.z); group.add(tri);
}

// ghost footprint outline (where the foot started)
export function footGhost(group, ball, yaw, color = 0x141a2e) {
  const shape = new THREE.Shape();
  shape.absellipse(-0.075, 0, 0.13, 0.055, 0, Math.PI * 2);
  const hole = new THREE.Path(); hole.absellipse(-0.075, 0, 0.115, 0.042, 0, Math.PI * 2, true); shape.holes.push(hole);
  const m = new THREE.Mesh(new THREE.ShapeGeometry(shape), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: 0.55, depthWrite: false }));
  m.rotation.order = 'YXZ'; m.rotation.y = -yaw; m.rotation.x = -Math.PI / 2;
  m.position.set(ball.x, 0.004, ball.z); group.add(m);
}
