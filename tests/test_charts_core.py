"""Tests for lineplot, barplot, scatter, heatmap, radar, area, stacked_bar,
boxplot, violinplot, and histogram chart functions."""

import numpy as np
import pandas as pd
import pytest
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from acadp.charts._line import lineplot
from acadp.charts._bar import barplot
from acadp.charts._scatter import scatter
from acadp.charts._heatmap import heatmap
from acadp.charts._radar import radar
from acadp.charts._area import area
from acadp.charts._stacked_bar import stacked_bar
from acadp.charts._box import boxplot
from acadp.charts._violin import violinplot
from acadp.charts._hist import histogram


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


# ---- scatter ----------------------------------------------------------------

def test_scatter_returns_axes():
    np.random.seed(0)
    x = np.random.randn(50)
    y = np.random.randn(50)
    ax = scatter(x=x, y=y)
    assert isinstance(ax, Axes)
    plt.close("all")


def test_scatter_with_trend():
    np.random.seed(1)
    x = np.random.randn(50)
    y = 2 * x + np.random.randn(50)
    ax = scatter(x=x, y=y, trend=True)
    # trend line should add at least one Line2D to the axes
    assert len(ax.lines) >= 1
    plt.close("all")


# ---- heatmap ----------------------------------------------------------------

def test_heatmap_returns_axes():
    np.random.seed(2)
    data = np.random.randn(3, 100)
    corr = np.corrcoef(data)
    ax = heatmap(corr, labels=["A", "B", "C"])
    assert isinstance(ax, Axes)
    plt.close("all")


# ---- radar ------------------------------------------------------------------

def test_radar_returns_axes():
    ax = radar(["A", "B", "C"], [0.8, 0.6, 0.9])
    assert isinstance(ax, Axes)
    plt.close("all")


# ---- area -------------------------------------------------------------------

def test_area_dict():
    ax = area(x=[1, 2, 3], y={"A": [1, 2, 3], "B": [4, 5, 6]})
    assert isinstance(ax, Axes)
    plt.close("all")


# ---- stacked_bar ------------------------------------------------------------

def test_stacked_bar():
    ax = stacked_bar(["Q1", "Q2"], {"A": [10, 20], "B": [15, 25]})
    assert isinstance(ax, Axes)
    plt.close("all")
