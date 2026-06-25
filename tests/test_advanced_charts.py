"""Smoke tests for advanced chart modules."""
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from acadp.charts import bullet, supply_demand, small_multiples


def test_bullet_returns_axes():
    ax = bullet(
        categories=["指标A", "指标B", "指标C"],
        actual=[85, 72, 91],
        threshold=[80, 75, 88],
        directions=[">=", ">=", ">="],
        title="指标达标状态",
    )
    assert hasattr(ax, "barh")
    plt.close("all")


def test_supply_demand_returns_figure():
    time = np.arange(24)
    supply = {"风电": np.random.rand(24) * 50, "光伏": np.random.rand(24) * 30}
    demand = np.random.rand(24) * 60 + 20
    fig = supply_demand(time, supply, demand, title="供需匹配")
    assert hasattr(fig, "savefig")
    plt.close("all")


def test_small_multiples_returns_figure():
    factors = [
        {"name": "温度", "x": [20, 25, 30, 35], "y": [10, 15, 12, 8]},
        {"name": "湿度", "x": [30, 40, 50, 60], "y": [20, 25, 22, 18]},
    ]
    fig = small_multiples(factors, title="敏感性分析")
    assert hasattr(fig, "savefig")
    plt.close("all")
