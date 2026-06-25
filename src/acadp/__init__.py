"""AcademiPlot — publication-ready academic figures in one line."""

__version__ = "0.2.0"

from acadp.charts import (
    lineplot, barplot, scatter, heatmap, boxplot,
    violinplot, histogram, radar, area, stacked_bar,
    pareto, contour, waterfall, dumbbell,
    bullet, supply_demand, small_multiples,
)
from acadp._style import set_style, get_style, set_dpi, set_font, set_context
from acadp._suggest import suggest, auto_plot, AutoPlotResult
from acadp._reviewer import review, review_dir, ReviewResult, BatchReport

__all__ = [
    "lineplot", "barplot", "scatter", "heatmap", "boxplot",
    "violinplot", "histogram", "radar", "area", "stacked_bar",
    "pareto", "contour", "waterfall", "dumbbell",
    "bullet", "supply_demand", "small_multiples",
    "set_style", "get_style", "set_dpi", "set_font", "set_context",
    "suggest",
    "auto_plot", "AutoPlotResult",
    "review", "review_dir", "ReviewResult", "BatchReport",
]
