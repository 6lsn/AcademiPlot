"""Complete paper figure workflow with AcademiPlot.

Demonstrates: data loading -> smart suggest -> quality review -> auto-fix
Run: python examples/paper_workflow.py
"""
import sys
sys.path.insert(0, "src")

import acadp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create sample data
np.random.seed(42)
methods = ["Method A", "Method B", "Method C", "Baseline"]
results = pd.DataFrame({
    "method": np.repeat(methods, 30),
    "accuracy": np.concatenate([
        np.random.normal(0.92, 0.03, 30),
        np.random.normal(0.88, 0.05, 30),
        np.random.normal(0.85, 0.04, 30),
        np.random.normal(0.78, 0.06, 30),
    ]),
    "runtime": np.concatenate([
        np.random.normal(2.1, 0.3, 30),
        np.random.normal(1.5, 0.2, 30),
        np.random.normal(3.2, 0.5, 30),
        np.random.normal(0.8, 0.1, 30),
    ]),
})

# Step 1: Smart suggest
print("Step 1: Smart chart selection...")
ax = acadp.suggest(results, task="Compare accuracy across methods")
ax.figure.savefig("paper_fig1_comparison.png", dpi=300, bbox_inches="tight")
plt.close("all")

# Step 2: Scatter with trend
print("Step 2: Scatter analysis...")
ax = acadp.scatter(results, x="runtime", y="accuracy", trend=True,
                    title="Runtime vs Accuracy",
                    xlabel="Runtime (s)", ylabel="Accuracy")
ax.figure.savefig("paper_fig2_scatter.png", dpi=300, bbox_inches="tight")
plt.close("all")

# Step 3: Quality review
# review() accepts a metadata dict; build one from the chart
print("Step 3: Quality review...")
metadata = {
    "figure_name": "paper_fig1_comparison",
    "plot_type": "bar",
    "problem_type": "Evaluation",
    "modeling_purpose": "Compare accuracy across methods",
    "variables": {"x": "method", "y": "accuracy"},
    "axis_labels": {"x": "method", "y": "accuracy"},
    "legend_labels": [],
    "caption": "Comparison of accuracy across methods",
    "usage": "paper",
}
report = acadp.review(metadata)
print(f"  Status: {report.status}")
print(f"  Score: {report.score}/100")
print(f"  Scores: {report.scores}")

# Step 4: Full pipeline with auto_plot
print("Step 4: Full pipeline...")
result = acadp.auto_plot(results, task="Accuracy distribution across methods")
print(f"  Status: {result.report.status}")
print(f"  Score: {result.report.score}/100")
print(f"  Changes: {result.changes}")

print("\nDone! Check the generated PNG files.")
