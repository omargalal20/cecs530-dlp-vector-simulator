"""Question 2c graph: memory access cycles for each stride.

Needs matplotlib (pip install -r requirements.txt).
Run: python plot_results.py   ->   output/q2_stride_cycles.png
"""

import os

import matplotlib

matplotlib.use("Agg")  # draw to a file, no window needed
import matplotlib.pyplot as plt

from vector_simulator import NUM_BANKS, VECTOR_LENGTH, question_2

OUTPUT_FILE = os.path.join("output", "q2_stride_cycles.png")

SURFACE = "#fcfcfb"
BAR = "#2a78d6"
TEXT = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"


def draw_stride_chart(rows, path=OUTPUT_FILE):
    """Bar chart of total cycles per stride, labeled with cycles and conflicts."""
    strides = [str(r["stride"]) for r in rows]
    cycles = [r["cycles"] for r in rows]

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    bars = ax.bar(strides, cycles, width=0.55, color=BAR, zorder=3)

    for bar, r in zip(bars, rows):
        x = bar.get_x() + bar.get_width() / 2
        ax.text(x, r["cycles"] + 8, f"{r['cycles']}", ha="center", va="bottom",
                fontsize=12, fontweight="bold", color=TEXT)
        ax.text(x, r["cycles"] + 40, f"{r['conflicts']} conflicts", ha="center",
                va="bottom", fontsize=9, color=TEXT_SECONDARY)

    ax.set_title(f"Memory access cycles by stride ({VECTOR_LENGTH} elements, "
                 f"{NUM_BANKS} banks)", loc="left", fontsize=13, color=TEXT)
    ax.set_xlabel("Stride (elements)", color=TEXT_SECONDARY)
    ax.set_ylabel("Total cycles, including memory latency", color=TEXT_SECONDARY)
    ax.set_ylim(0, max(cycles) * 1.18)
    ax.tick_params(colors=TEXT_SECONDARY, length=0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return path


def main():
    path = draw_stride_chart(question_2())
    print(f"Saved {path}")


if __name__ == "__main__":
    main()
