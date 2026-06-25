"""Tests for src/acadp/_style.py."""

import pytest

from acadp._style import (
    COLORS,
    get_style,
    palette,
    set_dpi,
    set_font,
    set_context,
    set_style,
)


# ---- set_style / get_style -------------------------------------------------

def test_set_style_accepts_valid_names():
    for name in ("nature", "science", "ieee"):
        set_style(name)
        assert get_style()["style"] == name


def test_set_style_rejects_unknown():
    with pytest.raises(ValueError):
        set_style("nonexistent_theme")


def test_get_style_has_required_keys():
    result = get_style()
    for key in ("dpi", "font", "style", "context"):
        assert key in result, f"Missing key: {key}"


# ---- set_dpi ----------------------------------------------------------------

def test_set_dpi_updates_config():
    set_dpi(600)
    assert get_style()["dpi"] == 600
    # reset for other tests
    set_dpi(300)


# ---- COLORS ----------------------------------------------------------------

_EXPECTED_COLOR_KEYS = {
    "blue_main", "teal", "amber", "crimson", "purple",
    "blue_light", "teal_light", "crimson_light", "purple_light",
    "grid", "axis", "text", "muted", "background",
}


def test_colors_has_expected_keys():
    for key in _EXPECTED_COLOR_KEYS:
        assert key in COLORS, f"Missing color key: {key}"


# ---- palette ---------------------------------------------------------------

def test_palette_returns_correct_length():
    result = palette(3)
    assert isinstance(result, list)
    assert len(result) == 3


def test_palette_wraps_around():
    result = palette(20)
    assert len(result) == 20
