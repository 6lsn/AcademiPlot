"""AcademiPlot Quick Start -- 3 lines to a publication-ready figure.

Run: python examples/quick_start.py
"""
import sys
sys.path.insert(0, "src")

import acadp
import numpy as np
import matplotlib.pyplot as plt

# 1. Simple line chart
ax = acadp.lineplot(
    x=np.linspace(0, 10, 50),
    y=np.sin(np.linspace(0, 10, 50)),
    title="Sine Wave",
    xlabel="x", ylabel="sin(x)"
)
ax.figure.savefig("quick_start_line.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 2. Bar chart with highlight
ax = acadp.barplot(
    x=["Python", "R", "MATLAB", "Julia", "Stata"],
    y=[95, 78, 85, 60, 45],
    highlight="max",
    title="Data Science Language Popularity"
)
ax.figure.savefig("quick_start_bar.png", dpi=150, bbox_inches="tight")
plt.close("all")

# 3. Smart suggest
import pandas as pd
df = pd.DataFrame({
    "year": range(2018, 2024),
    "revenue": [100, 120, 115, 140, 165, 190]
})
ax = acadp.suggest(df, task="Show revenue growth trend")
ax.figure.savefig("quick_start_suggest.png", dpi=150, bbox_inches="tight")
plt.close("all")

print("Generated 3 example figures!")
