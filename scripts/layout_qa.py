import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.text import Text

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from utf8_io import configure_utf8_stdio


configure_utf8_stdio()


def _round(value):
    return round(float(value), 4)


def _draw_and_get_renderer(fig):
    canvas = fig.canvas
    canvas.draw()
    return canvas.get_renderer()


def _bbox_to_figure_fraction(fig, bbox):
    figure_bbox = bbox.transformed(fig.transFigure.inverted())
    return {
        "x0": _round(figure_bbox.x0),
        "y0": _round(figure_bbox.y0),
        "x1": _round(figure_bbox.x1),
        "y1": _round(figure_bbox.y1),
    }


def _overflow_amount(bbox):
    return {
        "left": max(0.0, -bbox["x0"]),
        "bottom": max(0.0, -bbox["y0"]),
        "right": max(0.0, bbox["x1"] - 1.0),
        "top": max(0.0, bbox["y1"] - 1.0),
    }


def _is_outside(overflow, tolerance):
    return any(amount > tolerance for amount in overflow.values())


def _visible_legends(fig):
    legends = []
    for legend in fig.legends:
        if legend.get_visible():
            legends.append(legend)
    for ax in fig.get_axes():
        legend = ax.get_legend()
        if legend is not None and legend.get_visible():
            legends.append(legend)
    return legends


def _legend_label(legend):
    labels = [text.get_text() for text in legend.get_texts() if text.get_text()]
    return "、".join(labels[:3]) if labels else "legend"


def _visible_texts(fig):
    texts = []
    for text in fig.findobj(match=Text):
        if not text.get_visible():
            continue
        value = text.get_text()
        if not value or not value.strip():
            continue
        if isinstance(text.axes, Legend):
            continue
        texts.append(text)
    return texts


def _artist_issue(fig, artist, renderer, kind, label, tolerance):
    bbox = artist.get_window_extent(renderer=renderer)
    if bbox.width <= 0 or bbox.height <= 0:
        return None
    figure_bbox = _bbox_to_figure_fraction(fig, bbox)
    overflow = {key: _round(value) for key, value in _overflow_amount(figure_bbox).items()}
    if not _is_outside(overflow, tolerance):
        return None
    return {
        "kind": kind,
        "label": label,
        "bbox": figure_bbox,
        "overflow": overflow,
        "message": f"{kind} exceeds figure bounds beyond tolerance {tolerance:.3f}.",
    }


def qa_figure_layout(fig, tolerance=0.05, check_legends=True, check_text=True):
    renderer = _draw_and_get_renderer(fig)
    issues = []

    if check_legends:
        for legend in _visible_legends(fig):
            issue = _artist_issue(fig, legend, renderer, "legend", _legend_label(legend), tolerance)
            if issue:
                issues.append(issue)

    if check_text:
        legend_text_ids = {
            id(text)
            for legend in _visible_legends(fig)
            for text in legend.get_texts()
        }
        tick_text_ids = {
            id(text)
            for ax in fig.get_axes()
            for text in [*ax.get_xticklabels(), *ax.get_yticklabels()]
        }
        for text in _visible_texts(fig):
            if id(text) in legend_text_ids or id(text) in tick_text_ids:
                continue
            issue = _artist_issue(fig, text, renderer, "text", text.get_text(), tolerance)
            if issue:
                issues.append(issue)

    legend_issues = sum(1 for issue in issues if issue["kind"] == "legend")
    text_issues = sum(1 for issue in issues if issue["kind"] == "text")
    return {
        "status": "fail" if issues else "pass",
        "summary": {
            "total_issues": len(issues),
            "legend_issues": legend_issues,
            "text_issues": text_issues,
            "tolerance": tolerance,
        },
        "issues": issues,
    }


def assert_layout_ok(fig, tolerance=0.05):
    report = qa_figure_layout(fig, tolerance=tolerance)
    if report["status"] != "pass":
        messages = "; ".join(issue["message"] for issue in report["issues"][:3])
        raise ValueError(f"Figure layout QA failed: {messages}")
    return report


def _demo_figure(mode):
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot([1, 2, 3], [2, 3, 4], label="demo series")
    ax.set_xlabel("time")
    ax.set_ylabel("value")
    ax.set_title("layout QA demo")
    if mode == "overflow":
        ax.legend(loc="upper left", bbox_to_anchor=(1.45, 1.0))
        fig.text(1.25, 0.5, "overflow text", transform=fig.transFigure)
    else:
        ax.legend(loc="upper left")
        fig.tight_layout()
    return fig


def main():
    parser = argparse.ArgumentParser(description="Check obvious legend/text overflow in Matplotlib figures.")
    parser.add_argument("--demo", choices=["clean", "overflow"], help="Run QA on a built-in demo figure.")
    parser.add_argument("--output", help="Optional JSON report path.")
    parser.add_argument("--tolerance", type=float, default=0.05, help="Allowed overflow in figure fraction.")
    args = parser.parse_args()

    if not args.demo:
        parser.error("Currently provide --demo clean|overflow, or import qa_figure_layout(fig) from Python.")

    fig = _demo_figure(args.demo)
    report = qa_figure_layout(fig, tolerance=args.tolerance)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
