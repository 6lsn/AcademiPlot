"""Tests for lineplot, barplot, scatter, and heatmap chart functions."""

import numpy as np
import pandas as pd
import pytest
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from acadp.charts._line import lineplot
from acadp.charts._bar import barplot
from acadp.charts._scatter import scatter
from acadp.charts._heatmap import heatmap


# ---- lineplot ----------------------------------------------------------------

def test_lineplot_returns_axes():
    ax = lineplot(x=np.arange(10), y=np.arange(10))
    assert isinstance(ax, Axes)


def test_lineplot_accepts_dataframe():
    df = pd.DataFrame({"year": [2020, 2021, 2022], "val": [10, 20, 15]})
    ax = lineplot(data=df, x="year", y="val", title="Test DF")
    assert isinstance(ax, Axes)
    assert ax.get_xlabel() == "year"


# ---- barplot -----------------------------------------------------------------

def test_barplot_returns_axes():
    ax = barplot(x=["A", "B", "C"], y=[10, 20, 30])
    assert isinstance(ax, Axes)


def test_barplot_highlight_max():
    ax = barplot(x=["A", "B", "C"], y=[10, 30, 20], highlight="max")
    assert isinstance(ax, Axes)
    # Verify that an annotation text "30" exists
    texts = [t.get_text() for t in ax.texts]
    assert "30" in texts, f"Expected '30' annotation, got {texts}"
