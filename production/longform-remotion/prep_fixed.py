# Claude's 22 replacement stills -> base layers: flat background (border connected near background pixels) repainted to sage #C4D6C4
import glob, os, numpy as np
from PIL import Image
from scipy import ndimage
SAGE = np.array([196, 214, 196])
for f in sorted(glob.glob('/home/user/the-fight-playbook-claude-handoff/CLAUDE-EXPORT/FINAL-CUT/fixed-stills/*.png')):
    sid = os.path.basename(f)[:-4]; a = np.asarray(Image.open(f).convert('RGB').resize((1920, 1080), Image.LANCZOS)).astype(int)
    border = np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)])
    bg = np.median(border, axis=0); near = np.abs(a - bg).sum(axis=2) < 30
    lab, _ = ndimage.label(near); edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    m = np.isin(lab, list(edge)); a[m] = SAGE
    Image.fromarray(a.astype(np.uint8)).save(f'public/layers/{sid}_base.png'); print(sid, int(m.mean() * 100), '% bg')
