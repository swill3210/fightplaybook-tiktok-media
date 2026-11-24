"""Head geometry fit to the sheet (Sean 2026-11-24 final head pass): the head and neck vertices are warped so their
front (x) and side (y) silhouettes match the sheet's front and right views row by row, after the face front is
smoothed (no nose, mouth, lip or cheek dents). Smooth falloffs keep the traps and body untouched."""
import numpy as np
import cv2
import compare_ref as CR

Z0, Z1 = 1.68, 1.72  # g8: 1.64 rows include the shoulders and warped the traps
LAST_CHIN = 1.775  # warp fades in over the traps


def sheet_rows(view):
    """per sheet row: (left, right) figure extents in model units (x relative to figure centre), z in model units"""
    img = cv2.imread(CR.REF); x0, y0, x1, y1 = CR.BOXES[view]; crop = img[y0:y1, x0:x1]
    g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY).astype(int); fig = np.abs(g - g[2, 2]) > 60
    ys, xs = np.nonzero(fig); bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max(), ys.max()
    sc = (by1 - by0) / 2.0; mid = (bx0 + bx1) / 2; rows = {}
    for y in range(by0, by0 + int(0.25 * (by1 - by0))):
        c = np.nonzero(fig[y])[0]
        if len(c):
            rows[(by1 - y) / sc] = ((c.min() - mid) / sc, (c.max() - mid) / sc)
    zs = np.array(sorted(rows)); L = np.array([rows[z][0] for z in zs]); R = np.array([rows[z][1] for z in zs])
    return zs, L, R


def smooth_face(vs, adj, yc, chin, top, iters=90):
    """Laplacian smoothing of the face front (between chin and brow), strongest at the centre, ears excluded"""
    z = vs[:, 2]; front = vs[:, 1] < yc - 0.02
    band = np.clip(1 - np.abs(z - (chin + 0.4 * (top - chin))) / (0.38 * (top - chin)), 0, 1)
    side = np.clip(1 - np.abs(vs[:, 0]) / 0.085, 0, 1)
    w = band * side * front; idx = np.nonzero(w > 0)[0]
    for _ in range(iters):
        avg = np.array([vs[adj[i]].mean(0) for i in idx])
        vs[idx] += (avg - vs[idx]) * (0.6 * w[idx])[:, None]
    return vs


def convex_face(vs, yc, chin, brow):
    """push the face front out to the head's convex envelope along -y: fills every nose, mouth, lip and cheek dent,
    leaving one smooth slope from brow to chin (g3: smoothing alone left a concave lower face and a hooked chin)"""
    import bmesh
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    head = vs[(vs[:, 2] > chin - 0.01) & (np.abs(vs[:, 0]) < 0.075)]
    bm = bmesh.new(); vv = [bm.verts.new(p) for p in head]
    hull = bmesh.ops.convex_hull(bm, input=vv)
    drop = {g for g in hull.get("geom_interior", []) + hull.get("geom_unused", []) if isinstance(g, bmesh.types.BMVert)}
    bmesh.ops.delete(bm, geom=list(drop), context="VERTS")
    tree = BVHTree.FromBMesh(bm)
    sel = np.nonzero((vs[:, 1] < yc - 0.02) & (vs[:, 2] > chin - 0.005) & (vs[:, 2] < brow) & (np.abs(vs[:, 0]) < 0.085))[0]
    for i in sel:
        p = Vector(vs[i]); hit = tree.ray_cast(p, Vector((0, -1, 0)))
        if hit[0] is not None:
            wx = np.clip((0.085 - abs(p.x)) / 0.025, 0, 1); wz = np.clip((brow - p.z) / 0.03, 0, 1) * np.clip((p.z - chin + 0.005) / 0.015, 0, 1)
            vs[i, 1] = p.y + (hit[0].y - p.y) * wx * wz
    bm.free()
    return vs


def fit(ob):
    me = ob.data; vs = np.array([v.co[:] for v in me.vertices])
    ed = np.zeros(len(me.edges) * 2, int); me.edges.foreach_get("vertices", ed); ed = ed.reshape(-1, 2)
    adj = [[] for _ in range(len(vs))]
    for a, b in ed:
        adj[a].append(b); adj[b].append(a)
    z = vs[:, 2]; top = z.max()
    yc = vs[np.abs(z - 1.72) < 0.01, 1].mean()
    # sheet targets
    fz, fL, fR = sheet_rows("front"); sz, sL, sR = sheet_rows("right")  # right view: image right = model -y (front)
    s_top = fz.max()
    # vertical: model head (above Z1) remapped so its top meets the sheet top
    k = np.clip((z - Z0) / (Z1 - Z0), 0, 1); k = k * k * (3 - 2 * k)
    # chin underside = where the front profile jumps from neck to face (midpoint crossing); g5: argmax picked 1.83
    def chin_of(zs_, fe_):
        lo = np.interp(1.68, zs_, fe_); hi = np.interp(1.80, zs_, fe_); m = (lo + hi) / 2
        zq = np.arange(1.68, 1.80, 0.002); fq = np.interp(zq, zs_, fe_); return zq[np.argmax(fq > m)]
    nk0 = np.abs(sz - 1.70).argmin(); c0 = (sL[nk0] + sR[nk0]) / 2
    o = np.argsort(sz); s_chin = chin_of(sz[o], (sR - c0)[o])
    zz = np.arange(1.62, 1.86, 0.004)
    fe = np.array([yc - vs[(np.abs(z - q) < 0.003) & (np.abs(vs[:, 0]) < 0.03), 1].min() for q in zz])
    m_chin = chin_of(zz, fe)
    kv = np.clip((z - 1.63) / 0.03, 0, 1)  # g6: starting at 1.56 dragged the yoke art  # vertical remap: neck lengthened, face shortened to the sheet chin
    zn = np.interp(z, [0, 1.66, m_chin, top, 9], [0, 1.66, s_chin, s_top, 9]); vs[:, 2] = z + kv * (zn - z); z = vs[:, 2]
    print("chin model", round(m_chin, 3), "-> sheet", round(s_chin, 3))
    chin = s_chin; global LAST_CHIN; LAST_CHIN = s_chin
    vs = convex_face(vs, yc, chin, chin + 0.62 * (s_top - chin))
    vs = smooth_face(vs, adj, yc, chin, s_top, iters=25)
    # jaw underside ring: the face shortening folded it and the ink shell poked through as a jagged line (g6, g7)
    ring = np.nonzero((np.abs(vs[:, 2] - chin) < 0.05) & (np.hypot(vs[:, 0], vs[:, 1] - yc) < 0.16))[0]
    wr_ = 1 - np.abs(vs[ring, 2] - chin) / 0.05
    for _ in range(60):
        avg = np.array([vs[adj[i]].mean(0) for i in ring]); vs[ring] += (avg - vs[ring]) * (0.7 * wr_)[:, None]
    # chin underside: noisy normals drew a jagged shadow spike and an ink crease under the jaw (g10, Sean item 3)
    fr_ = (np.abs(vs[:, 2] - chin) < 0.01) & (np.abs(vs[:, 0]) < 0.02)
    tip = np.array([0.0, vs[fr_, 1].min(), chin]) if fr_.any() else np.array([0.0, yc - 0.17, chin])
    dloc = np.linalg.norm(vs - tip, axis=1); loc = np.nonzero(dloc < 0.07)[0]; wl = (1 - dloc[loc] / 0.07) ** 0.5
    for _ in range(120):
        avg = np.array([vs[adj[i]].mean(0) for i in loc]); vs[loc] += (avg - vs[loc]) * (0.8 * wl)[:, None]
    z = vs[:, 2]
    # per row scale factors from silhouettes (model rows measured after the remap)
    zb = np.arange(Z0, s_top - 0.005, 0.005)
    hw_m, fr_m, bk_m = [], [], []
    for zz in zb:
        sl = vs[np.abs(z - zz) < 0.004]
        sl = sl[np.abs(sl[:, 0]) < 0.2]
        hw_m.append(np.abs(sl[:, 0]).max() if len(sl) else np.nan)
        fr_m.append(yc - sl[:, 1].min() if len(sl) else np.nan); bk_m.append(sl[:, 1].max() - yc if len(sl) else np.nan)
    hw_s = np.interp(zb, fz, (fR - fL) / 2)
    # side: sheet front (face) extent = right edge, back extent = left edge, measured about the sheet neck centre
    nk = np.abs(sz - 1.72).argmin(); sc_c = (sL[nk] + sR[nk]) / 2
    fr_s = np.interp(zb, sz, sR - sc_c); bk_s = np.interp(zb, sz, sc_c - sL)
    def factor(t, m):
        f = np.where(np.isfinite(m), t / np.maximum(m, 1e-3), 1.0); f = np.clip(f, 0.4, 1.9)  # g9: 1.45 cap left the dome narrow  # g2: 0.75 floor left the throat and lower face bulging
        fp = np.pad(f, 2, mode="edge"); return np.convolve(fp, np.ones(5) / 5, mode="valid")  # g1: zero padding shrank the ends
    fx, ff, fb = factor(hw_s, np.array(hw_m)), factor(fr_s, np.array(fr_m)), factor(bk_s, np.array(bk_m))
    kk = np.clip((z - Z0) / (Z1 - Z0), 0, 1); kk = kk * kk * (3 - 2 * kk)
    rad = np.hypot(vs[:, 0], vs[:, 1] - yc); kr = np.clip((0.24 - rad) / 0.06, 0, 1)  # traps far from the neck untouched
    w = kk * np.where(z < Z1 + 0.02, kr, 1.0)
    sx = 1 + w * (np.interp(z, zb, fx) - 1)
    sy = 1 + w * (np.where(vs[:, 1] < yc, np.interp(z, zb, ff), np.interp(z, zb, fb)) - 1)
    vs[:, 0] *= sx; vs[:, 1] = yc + (vs[:, 1] - yc) * sy
    me.vertices.foreach_set("co", vs.ravel()); me.update()
    print("head fit: top", round(top, 3), "->", round(s_top, 3), "x factor range", np.round([np.nanmin(fx), np.nanmax(fx)], 2),
          "front", np.round([np.nanmin(ff), np.nanmax(ff)], 2), "back", np.round([np.nanmin(fb), np.nanmax(fb)], 2))
    return yc


def sheet_eyes(head_obj, mat_fn):
    """eyes traced from the sheet's own front view eye blobs (upsampled 8x): exact shape, slant and position"""
    import bpy, bmesh
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    img = cv2.imread(CR.REF); x0, y0, x1, y1 = CR.BOXES["front"]; crop = img[y0:y1, x0:x1]
    g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY).astype(int); fig = np.abs(g - g[2, 2]) > 60
    ys, xs = np.nonzero(fig); bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max(), ys.max()
    sc = (by1 - by0) / 2.0; mid = (bx0 + bx1) / 2
    hy1 = by0 + int(0.15 * (by1 - by0)); hx0, hx1 = int(mid - 0.12 * (by1 - by0)), int(mid + 0.12 * (by1 - by0))
    sub = crop[by0:hy1, hx0:hx1]; up = cv2.resize(sub, None, fx=8, fy=8, interpolation=cv2.INTER_CUBIC).astype(int)
    white = ((up.min(2) > 185) & (np.abs(up[..., 0] - up[..., 2]) < 18)).astype(np.uint8)
    cs, _ = cv2.findContours(white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cs = sorted([c for c in cs if 150 < cv2.contourArea(c) < 20000], key=cv2.contourArea, reverse=True)[:2]
    tree = BVHTree.FromObject(head_obj, bpy.context.evaluated_depsgraph_get()); mat = mat_fn(); obs = []
    for c in cs:
        c = cv2.approxPolyDP(c, 1.5, True)[:, 0, :].astype(float)
        px = hx0 + c[:, 0] / 8; py = by0 + c[:, 1] / 8
        X = (px - mid) / sc; Z = (by1 - py) / sc; cx, cz = X.mean(), Z.mean()
        hit = tree.ray_cast(Vector((cx, -2, cz)), Vector((0, 1, 0)))
        if hit[0] is None:
            print("eye miss"); continue
        me = bpy.data.meshes.new("eye"); bm = bmesh.new()
        ring = [bm.verts.new((x - cx, 0, z - cz)) for x, z in zip(X, Z)]
        ctr = bm.verts.new((0, 0, 0))
        for i in range(len(ring)):
            bm.faces.new((ctr, ring[i], ring[(i + 1) % len(ring)]))
        bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
        bm.to_mesh(me); bm.free()
        e = bpy.data.objects.new("eye", me); bpy.context.collection.objects.link(e); me.materials.append(mat)
        e.location = hit[0] + Vector((0, -0.02, 0))
        sw = e.modifiers.new("hug", "SHRINKWRAP"); sw.target = head_obj; sw.wrap_method = "PROJECT"
        sw.use_project_y = True; sw.use_negative_direction = True; sw.use_positive_direction = True; sw.offset = 0.003
        obs.append(e); print("sheet eye", round(cx, 3), round(cz, 3), "pts", len(X))
    return obs
