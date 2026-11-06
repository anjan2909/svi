"""Build all SVI website illustrations into dist/assets/illustrations/.

    python3 source-assets/illustrations/build.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from panels import PANELS  # noqa: E402

from scenes import SCENES  # noqa: E402
from components import COMPONENTS  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[2] / 'dist' / 'assets' / 'illustrations'
OUT.mkdir(parents=True, exist_ok=True)

for name, fn in {**PANELS, **SCENES, **COMPONENTS}.items():
    svg = fn()
    (OUT / name).write_text(svg)
    print(f'{name:28s} {len(svg) / 1024:6.1f} KB')
