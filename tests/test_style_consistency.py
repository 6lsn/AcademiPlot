"""Tests for unified color palette and annotation labels."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from acadp._style import COLORS, annotate_extreme
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def test_backward_compat_aliases_point_to_correct_colors():
    """Legacy aliases must resolve to the same hex as their canonical name."""
    pairs = {
        "blue": "navy",
        "seagreen": "teal",
        "blue_main": "navy",
        "blue_light": "sky",
        "teal_light": "teal",
        "crimson": "coral",
        "crimson_light": "rose",
        "purple": "lavender",
        "purple_light": "mauve",
    }
    for alias, canonical in pairs.items():
        assert COLORS[alias] == COLORS[canonical], (
            f"COLORS['{alias}'] = {COLORS[alias]!r} != "
            f"COLORS['{canonical}'] = {COLORS[canonical]!r}"
        )


def test_all_primary_colors_exist():
    """The 10 primary colors must all be present."""
    primary = ["navy", "coral", "teal", "amber", "slate",
               "lavender", "rose", "sky", "mauve", "sand"]
    for name in primary:
        assert name in COLORS, f"Missing primary color: {name}"
        assert COLORS[name].startswith("#"), f"COLORS['{name}'] is not a hex color"


def test_neutral_colors_exist():
    """Neutral colors must be present."""
    for name in ["grid", "axis", "text", "muted", "background"]:
        assert name in COLORS, f"Missing neutral color: {name}"


def test_annotate_extreme_uses_chinese_labels():
    """annotate_extreme default text must be in Chinese."""
    fig, ax = plt.subplots()
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([10.0, 50.0, 30.0])

    annotate_extreme(ax, x, y, mode="max")
    texts = [t.get_text() for t in ax.texts]
    assert any("最高" in t for t in texts), f"Expected '最高' in texts, got: {texts}"

    annotate_extreme(ax, x, y, mode="min")
    texts = [t.get_text() for t in ax.texts]
    assert any("最低" in t for t in texts), f"Expected '最低' in texts, got: {texts}"
    plt.close(fig)
