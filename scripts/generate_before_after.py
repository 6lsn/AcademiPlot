"""Generate before/after comparison for README."""
import sys
sys.path.insert(0, "src")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

out_dir = Path("gallery/before_after")
out_dir.mkdir(parents=True, exist_ok=True)

np.random.seed(42)
x = np.linspace(0, 10, 30)
y = np.sin(x) * 10 + 50 + np.random.randn(30) * 3

# BEFORE: matplotlib default
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y)
ax.set_title("Before: matplotlib default")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.grid(True)
fig.savefig(out_dir / "before.png", dpi=150, bbox_inches="tight")
plt.close()

# AFTER: AcademiPlot
import acadp
ax = acadp.lineplot(x=x, y=y, title="经济增长趋势", xlabel="年份", ylabel="GDP（万亿元）")
ax.figure.savefig(out_dir / "after.png", dpi=150, bbox_inches="tight")
plt.close()

# Side by side (if PIL available)
try:
    from PIL import Image
    before = Image.open(out_dir / "before.png")
    after = Image.open(out_dir / "after.png")
    # Resize to same height
    h = max(before.height, after.height)
    before_resized = before.resize((int(before.width * h / before.height), h))
    after_resized = after.resize((int(after.width * h / after.height), h))
    total_w = before_resized.width + after_resized.width + 20
    combined = Image.new("RGB", (total_w, h), (255, 255, 255))
    combined.paste(before_resized, (0, 0))
    combined.paste(after_resized, (before_resized.width + 20, 0))
    combined.save(out_dir / "comparison.png")
    print("Generated before/after comparison images (including side-by-side)")
except ImportError:
    print("Generated before/after comparison images (PIL not available, skipping side-by-side)")
