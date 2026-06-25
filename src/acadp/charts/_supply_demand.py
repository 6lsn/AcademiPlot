"""Supply-demand balance chart."""
import matplotlib.pyplot as plt
import numpy as np
from acadp._style import COLORS, palette, _ensure_style, finalize_plot, set_chart_title


def supply_demand(time, supply_components, demand, secondary=None,
                  title=None, xlabel=None, ylabel=None, ax=None, **kwargs):
    """Stacked area + demand line + net balance bar chart.

    Args:
        time: array of time values
        supply_components: dict mapping supply name -> value array
        demand: array of demand values
        secondary: optional dict of secondary line series
        title: chart title

    Returns:
        matplotlib.figure.Figure (2-panel: stacked area + net balance)
    """
    _ensure_style()
    time = np.asarray(time)
    supply = {name: np.asarray(values) for name, values in supply_components.items()}
    demand = np.asarray(demand)
    supply_total = np.sum(np.vstack(list(supply.values())), axis=0)
    net = supply_total - demand

    fig = plt.figure(figsize=(10.8, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.15], hspace=0.1)
    ax_top = fig.add_subplot(gs[0])
    ax_bottom = fig.add_subplot(gs[1], sharex=ax_top)

    colors = palette(len(supply))
    ax_top.stackplot(time, list(supply.values()), labels=list(supply.keys()),
                     colors=colors, alpha=0.72)
    ax_top.plot(time, demand, color=COLORS["coral"], linewidth=2.4, label="需求")

    if secondary:
        for name, values in secondary.items():
            ax_top.plot(time, np.asarray(values), color=COLORS["muted"],
                        linestyle="--", linewidth=1.6, label=name)

    ax_top.set_ylabel(ylabel or "功率/数量")
    if title:
        set_chart_title(ax_top, title)
    else:
        set_chart_title(ax_top, "供需匹配与净差")
    ax_top.legend(loc="upper left", ncol=4, frameon=False)
    plt.setp(ax_top.get_xticklabels(), visible=False)

    bar_colors = [COLORS["teal"] if v >= 0 else COLORS["coral"] for v in net]
    ax_bottom.bar(time, net, color=bar_colors, alpha=0.85, width=0.72)
    ax_bottom.axhline(0, color=COLORS["axis"], linewidth=0.9)
    ax_bottom.set_xlabel(xlabel or "时间")
    ax_bottom.set_ylabel("净差")

    finalize_plot(fig)
    return fig
