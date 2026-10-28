"""content/posts/theory-of-computation.mdx の図を生成する。

出力先は public/img/toc-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-theory-of-computation-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GRAY = "#6b7280"
INK = "#111827"
FAINT = "#d1d5db"

plt.rcParams.update(
    {
        "font.family": ["Hiragino Sans", "DejaVu Sans"],
        "font.size": 11,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "path",
    }
)


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05, dpi=110)
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


def nested(ax, layers, x0=0.0, y0=0.0, dx=0.0, dy=0.9):
    """下端を揃えて入れ子にした楕円を描く。layers は内側から (幅, 高さ, 名前, 例)。"""
    # 外側から描かないと内側が隠れる
    for i, (w, h, name, examples) in reversed(list(enumerate(layers))):
        ax.add_patch(
            Ellipse(
                (x0, y0 + h / 2),
                w,
                h,
                facecolor=plt.cm.Blues(0.05 + 0.055 * (len(layers) - i)),
                edgecolor=GRAY,
                linewidth=0.8,
            )
        )
    for i, (w, h, name, examples) in enumerate(layers):
        # 1つ内側の楕円の上端と、この楕円の上端の間に名前を置く
        inner_top = y0 + layers[i - 1][1] if i > 0 else y0
        y = (inner_top + y0 + h) / 2
        ax.text(x0, y + 0.12, name, ha="center", va="center", color=INK, fontweight="bold")
        ax.text(x0, y - 0.2, examples, ha="center", va="center", color=GRAY, fontsize=9)


def fig_diagonalization():
    n = 5
    rng_table = [
        [1, 0, 1, 1, 0],
        [0, 0, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 1, 1],
    ]
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    cell = 1.0
    mark = {1: "受理", 0: "拒否"}

    for j in range(n):
        ax.text(j + 0.5, n + 0.45, f"⟨M{j + 1}⟩", ha="center", va="center", color=INK)
    ax.text(n + 0.6, n + 0.45, "…", ha="center", va="center", color=GRAY)
    for i in range(n):
        y = n - 1 - i
        ax.text(-0.3, y + 0.5, f"M{i + 1}", ha="right", va="center", color=INK)
        for j in range(n):
            on_diag = i == j
            ax.add_patch(
                FancyBboxPatch(
                    (j + 0.05, y + 0.05),
                    cell - 0.1,
                    cell - 0.1,
                    boxstyle="round,pad=0,rounding_size=0.08",
                    facecolor="#dbeafe" if on_diag else "white",
                    edgecolor=BLUE if on_diag else FAINT,
                    linewidth=1.2 if on_diag else 0.8,
                )
            )
            ax.text(
                j + 0.5,
                y + 0.5,
                mark[rng_table[i][j]],
                ha="center",
                va="center",
                color=INK if on_diag else GRAY,
                fontsize=10,
            )
        ax.text(n + 0.6, y + 0.5, "…", ha="center", va="center", color=GRAY)

    # D の行: 対角線を反転
    y = -1.3
    ax.text(-0.3, y + 0.5, "D", ha="right", va="center", color=ORANGE, fontweight="bold")
    for j in range(n):
        ax.add_patch(
            FancyBboxPatch(
                (j + 0.05, y + 0.05),
                cell - 0.1,
                cell - 0.1,
                boxstyle="round,pad=0,rounding_size=0.08",
                facecolor="#ffedd5",
                edgecolor=ORANGE,
                linewidth=1.2,
            )
        )
        ax.text(
            j + 0.5,
            y + 0.5,
            mark[1 - rng_table[j][j]],
            ha="center",
            va="center",
            color=INK,
            fontsize=10,
        )
    ax.text(n + 0.6, y + 0.5, "…", ha="center", va="center", color=GRAY)
    ax.text(
        n + 1.0,
        y + 0.5,
        "⟨D⟩ の列は?",
        ha="left",
        va="center",
        color=ORANGE,
        fontsize=10,
    )
    ax.text(
        n / 2,
        -1.9,
        "D の行は対角線 (M_i が ⟨M_i⟩ を受理するか) を反転したもの。どの行とも必ず1箇所で食い違う",
        ha="center",
        va="center",
        color=GRAY,
        fontsize=9,
    )

    ax.set_xlim(-1.2, n + 3.2)
    ax.set_ylim(-2.3, n + 0.9)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "toc-diagonalization.svg")


def fig_complexity_classes():
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    layers = [
        (2.2, 0.9, "P", "到達可能性、2-SAT、素数判定"),
        (3.8, 1.8, "NP", "SAT、Hamilton閉路、部分和"),
        (5.4, 2.7, "PSPACE", "TQBF、一般化したリバーシ"),
        (7.0, 3.6, "EXPTIME", "一般化した囲碁・チェス"),
        (8.6, 4.5, "判定可能", ""),
    ]
    nested(ax, layers)
    # NP の上端に NP完全
    ax.annotate(
        "NP完全 (NP の中で最も難しい)",
        xy=(1.7, 1.3),
        xytext=(2.6, 0.5),
        color=ORANGE,
        fontsize=9,
        ha="left",
        arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 0.8},
    )
    ax.text(
        0,
        -0.5,
        "P ≠ NP と信じられているが、隣り合うどの包含が真かは未解決",
        ha="center",
        va="center",
        color=GRAY,
        fontsize=9,
    )
    ax.set_xlim(-4.6, 4.6)
    ax.set_ylim(-0.8, 4.8)
    ax.set_aspect("equal")
    ax.axis("off")
    save(fig, "toc-complexity-classes.svg")


if __name__ == "__main__":
    fig_diagonalization()
    fig_complexity_classes()
