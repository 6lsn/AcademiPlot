"""Generate before/after comparison for README — visually dramatic.

Run: python scripts/generate_before_after.py
"""
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
x = np.linspace(0, 10, 50)
y = np.sin(x) * 10 + 50 + np.random.randn(50) * 2

# ═══ BEFORE: matplotlib default ═══
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(x, y, color="#1f77b4", linewidth=2)
ax.fill_between(x, y - 3, y + 3, color="#1f77b4", alpha=0.15)
ax.set_title("Figure 1", fontsize=14, pad=10)
ax.set_xlabel("X-axis", fontsize=12)
ax.set_ylabel("Y-axis", fontsize=12)
ax.grid(True, linestyle="-", alpha=0.7)
ax.legend(["Data"], fontsize=11)
fig.savefig(out_dir / "before.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ═══ AFTER: AcademiPlot ═══
from acadp._style import COLORS
import acadp
acadp.set_style("nature")

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(x, y, color=COLORS["navy"], linewidth=1.8, alpha=0.9)
ax.fill_between(x, y - 3, y + 3, color=COLORS["navy"], alpha=0.08)
ax.set_title("Renewable Energy Output Profile", fontsize=11, fontweight="bold", color="#333333", pad=8)
ax.set_xlabel("Time (h)", fontsize=9)
ax.set_ylabel("Output (MW)", fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=8, colors="#555555")
fig.savefig(out_dir / "after.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close()

# ═══ Side-by-side comparison ═══
try:
    from PIL import Image, ImageDraw, ImageFont
    before = Image.open(out_dir / "before.png")
    after = Image.open(out_dir / "after.png")
    h = max(before.height, after.height)
    before_r = before.resize((int(before.width * h / before.height), h), Image.LANCZOS)
    after_r = after.resize((int(after.width * h / after.height), h), Image.LANCZOS)
    gap = 30
    total_w = before_r.width + after_r.width + gap
    combined = Image.new("RGB", (total_w, h), (255, 255, 255))
    combined.paste(before_r, (0, 0))
    combined.paste(after_r, (before_r.width + gap, 0))
    draw = ImageDraw.Draw(combined)
    # Add labels
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    draw.text((before_r.width // 2 - 40, 5), "BEFORE", fill=(200, 60, 60), font=font)
    draw.text((before_r.width + gap + after_r.width // 2 - 30, 5), "AFTER", fill=(40, 120, 80), font=font)
    combined.save(out_dir / "comparison.png")
    print("Generated: before.png, after.png, comparison.png")
except ImportError:
    print("Generated: before.png, after.png (PIL not available for comparison)")
