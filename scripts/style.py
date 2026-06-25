"""Compatibility shim — imports everything from the canonical acadp._style module.

Old scripts that do ``from style import ...`` will keep working.
All real logic lives in src/acadp/_style.py.
"""

import sys
from pathlib import Path

# Ensure acadp is importable (installed via pip install -e .)
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from acadp._style import (  # noqa: F401 — re-export everything
    COLORS,
    PALETTE,
    PAPER_CMAP,
    DIVERGING_CMAP,
    palette,
    style_axis,
    set_chart_title,
    finalize_plot,
    save_current_figure,
    write_figure_metadata,
    build_figure_metadata,
    style_3d_axis,
    annotate_point,
    add_event_line,
    add_threshold_line,
    add_phase_span,
    annotate_extreme,
    validate_annotation_config,
    ANNOTATION_ALLOWED_MODES,
    ANNOTATION_LIMITS,
    ANNOTATION_SUITABLE_CHARTS,
    ANNOTATION_CAUTION_CHARTS,
    AUTO_ANNOTATION_DISABLED_CHARTS,
    PROBLEM_TYPE_BY_PLOT,
    _ensure_style,
)


def apply_paper_style():
    """Compatibility shim — triggers lazy style application in acadp._style."""
    _ensure_style()
