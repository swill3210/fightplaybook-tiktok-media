#!/bin/bash
# One time setup per fresh cloud container for the Blender character pipeline (free, open source; no paid services).
set -e
pip install -q bpy                                     # Blender 5.3 as a Python module
apt-get install -y -q libegl1 libgl1-mesa-dri libegl-mesa0 libgl1 libglx-mesa0 >/dev/null || \
  (apt-get update -q >/dev/null && apt-get install -y -q libegl1 libgl1-mesa-dri libegl-mesa0 libgl1 libglx-mesa0 >/dev/null)  # EEVEE on software GL
D=/tmp/claude-0/bl; mkdir -p $D
[ -d $D/mpfb2 ] || git clone -q --depth 1 https://github.com/makehumancommunity/mpfb2 $D/mpfb2   # MPFB2 (code GPLv3, assets CC0)
python3 - <<'PY'
import bpy, os, shutil
repo = bpy.utils.user_resource("EXTENSIONS", path="user_default", create=True)
dst = os.path.join(repo, "mpfb")
if not os.path.exists(dst): shutil.copytree("/tmp/claude-0/bl/mpfb2/src/mpfb", dst)
import addon_utils; addon_utils.enable("bl_ext.user_default.mpfb", default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService
print("MPFB OK", len(HumanService.create_human().data.vertices), "verts")
PY
