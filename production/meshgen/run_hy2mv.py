"""Hunyuan3D-2mv (free HF Space) from the four-view turnaround sheet. Token is injected by the session proxy."""
import sys, shutil, json, time
from gradio_client import Client, handle_file
api = sys.argv[1] if len(sys.argv) > 1 else "/shape_generation"
c = Client('tencent/Hunyuan3D-2mv', verbose=False)
t = time.time()
r = c.predict(caption=None, image=None, mv_image_front=handle_file('input/front.png'), mv_image_back=handle_file('input/back.png'),
              mv_image_left=handle_file('input/left.png'), mv_image_right=handle_file('input/right.png'),
              steps=30, guidance_scale=5.0, seed=1234, octree_resolution=380, check_box_rembg=True, num_chunks=8000,
              randomize_seed=False, api_name=api)
print("secs", round(time.time() - t), [str(x)[:120] for x in r])
for i, x in enumerate(r):
    x = x.get("value", x) if isinstance(x, dict) else x
    if isinstance(x, str) and x.endswith(('.glb', '.obj', '.ply')):
        shutil.copy(x, f"out/hy2mv_{api.strip('/')}_{i}{x[-4:]}")
