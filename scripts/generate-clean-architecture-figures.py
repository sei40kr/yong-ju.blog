"""content/posts/clean-architecture.mdx の図を生成する。

出力先は public/img/ca-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-clean-architecture-figures.py

環境変数 CA_FIG_PNG_DIR を指定すると、目視確認用の PNG も同時に書き出す。
"""

import math
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"
PNG_DIR = os.environ.get("CA_FIG_PNG_DIR")

INK = "#111827"
MUTED = "#6b7280"
LINE = "#9ca3af"
FAINT = "#e5e7eb"
BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#16a34a"
RED = "#dc2626"

plt.rcParams.update(
    {
        "font.family": ["Hiragino Sans", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "axes.edgecolor": "#9ca3af",
        "axes.linewidth": 0.8,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "path",
        "legend.frameon": False,
    }
)


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05)
    if PNG_DIR:
        fig.savefig(
            Path(PNG_DIR) / name.replace(".svg", ".png"),
            format="png",
            dpi=110,
            bbox_inches="tight",
            pad_inches=0.05,
        )
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


def bare(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(False)


# 1. 凝集性の3原則の張力
def tension_triangle():
    fig, ax = plt.subplots(figsize=(6.2, 5.2))
    bare(ax, (-1.35, 1.35), (-0.95, 1.25))

    pts = {
        "REP": (0.0, 1.0),
        "CCP": (-1.0, -0.6),
        "CRP": (1.0, -0.6),
    }
    tri = Polygon(list(pts.values()), closed=True, fill=False, ec=LINE, lw=1.2)
    ax.add_patch(tri)

    names = {
        "REP": "REP\n再利用・リリース等価",
        "CCP": "CCP\n閉鎖性共通",
        "CRP": "CRP\n全再利用",
    }
    offsets = {"REP": (0, 0.06), "CCP": (-0.08, -0.06), "CRP": (0.08, -0.06)}
    valign = {"REP": "bottom", "CCP": "top", "CRP": "top"}
    for k, (x, y) in pts.items():
        ax.add_patch(Circle((x, y), 0.045, fc=INK, ec=INK, zorder=3))
        dx, dy = offsets[k]
        ax.text(
            x + dx,
            y + dy,
            names[k],
            ha="center",
            va=valign[k],
            fontsize=10.5,
            color=INK,
            linespacing=1.5,
        )

    # 辺の中点に「捨てた頂点の代償」を書く
    def edge_label(a, b, text, dx, dy, color):
        (x1, y1), (x2, y2) = pts[a], pts[b]
        ax.text(
            (x1 + x2) / 2 + dx,
            (y1 + y2) / 2 + dy,
            text,
            ha="center",
            va="center",
            fontsize=9.5,
            color=color,
            linespacing=1.4,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=FAINT),
        )

    edge_label("REP", "CCP", "不要なリリースが多すぎる\n(CRPを捨てた)", -0.28, 0.08, ORANGE)
    edge_label("REP", "CRP", "変更が多くのコンポーネントに波及\n(CCPを捨てた)", 0.3, 0.08, ORANGE)
    edge_label("CCP", "CRP", "再利用が難しい\n(REPを捨てた)", 0.0, -0.17, ORANGE)

    ax.annotate(
        "",
        xy=(-0.55, -0.35),
        xytext=(0.55, -0.35),
        arrowprops=dict(arrowstyle="<|-", color=BLUE, lw=1.2, shrinkA=0, shrinkB=0),
    )
    ax.text(0, -0.28, "初期は開発しやすさ (CCP側)", ha="center", va="bottom", fontsize=9, color=BLUE)
    ax.text(0, -0.42, "成熟すると再利用 (REP/CRP側)", ha="center", va="top", fontsize=9, color=BLUE)

    save(fig, "ca-tension.svg")


# 2. 主系列
def main_sequence():
    fig, ax = plt.subplots(figsize=(5.8, 5.4))
    ax.set_xlim(-0.08, 1.12)
    ax.set_ylim(-0.08, 1.12)
    ax.set_aspect("equal")
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel("不安定度 I = Fan-out / (Fan-in + Fan-out)")
    ax.set_ylabel("抽象度 A = 抽象クラス数 / 全クラス数")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    # 主系列
    ax.plot([0, 1], [1, 0], color=INK, lw=1.4)
    ax.text(0.56, 0.5, "主系列\nA + I = 1", ha="left", va="bottom", fontsize=10, color=INK, linespacing=1.4)

    # ゾーン
    for (cx, cy), label, color in [
        ((0, 0), "苦痛ゾーン\n具象で安定\n(DB schema, 具象utility)", RED),
        ((1, 1), "無駄ゾーン\n抽象で不安定\n(誰も使わないinterface)", ORANGE),
    ]:
        ax.add_patch(Circle((cx, cy), 0.3, fc=color, ec="none", alpha=0.12, zorder=0))
        ax.add_patch(Circle((cx, cy), 0.3, fc="none", ec=color, lw=1.0, ls="--", zorder=1))
    ax.text(0.04, 0.2, "苦痛ゾーン\n具象で安定\n(DB schema, 具象utility)", ha="left", va="bottom", fontsize=9.5, color=RED, linespacing=1.4)
    ax.text(0.96, 0.8, "無駄ゾーン\n抽象で不安定\n(誰も使わないinterface)", ha="right", va="top", fontsize=9.5, color=ORANGE, linespacing=1.4)

    # 主系列上の2点と、外れた1点
    ax.plot([0.08, 0.9], [0.92, 0.1], "o", color=BLUE, ms=7, zorder=3)
    ax.text(0.12, 0.95, "安定した抽象\n(use case, entity)", ha="left", va="bottom", fontsize=9.5, color=BLUE, linespacing=1.4)
    ax.text(0.86, 0.05, "不安定な具象\n(UI, main)", ha="right", va="bottom", fontsize=9.5, color=BLUE, linespacing=1.4)

    px, py = 0.45, 0.25
    ax.plot([px], [py], "o", color=GREEN, ms=7, zorder=3)
    # 主系列への垂線
    fx = (px - py + 1) / 2
    fy = 1 - fx
    ax.plot([px, fx], [py, fy], color=GREEN, lw=1.0, ls=":")
    ax.text(px + 0.04, py - 0.02, "主系列からの距離\nD = |A + I − 1|", ha="left", va="top", linespacing=1.4, fontsize=9.5, color=GREEN)

    save(fig, "ca-main-sequence.svg")


# 3. 同心円
def concentric():
    fig, ax = plt.subplots(figsize=(7.0, 6.2))
    bare(ax, (-1.2, 1.2), (-1.25, 1.2))

    layers = [
        (1.0, "#dbeafe", "framework & driver"),
        (0.76, "#bfdbfe", "interface adapter"),
        (0.52, "#93c5fd", "use case"),
        (0.28, "#60a5fa", "entity"),
    ]
    for r, fc, _ in layers:
        ax.add_patch(Circle((0, 0), r, fc=fc, ec="white", lw=2, zorder=1))

    ax.text(0, 0.02, "entity", ha="center", va="center", fontsize=10.5, color="white", fontweight="bold", zorder=3)
    ax.text(0, 0.40, "use case", ha="center", va="center", fontsize=10.5, color=INK, zorder=3)
    ax.text(0, 0.64, "interface adapter", ha="center", va="center", fontsize=10.5, color=INK, zorder=3)
    ax.text(0, 0.88, "framework & driver", ha="center", va="center", fontsize=10.5, color=INK, zorder=3)

    # 各層の例
    ax.text(-0.86, -0.46, "web\nframework", ha="center", va="center", fontsize=9, color=MUTED, zorder=3, linespacing=1.3)
    ax.text(0.86, -0.46, "DB\ndriver", ha="center", va="center", fontsize=9, color=MUTED, zorder=3, linespacing=1.3)
    ax.text(-0.52, -0.42, "controller", ha="center", va="center", fontsize=9, color=MUTED, zorder=3)
    ax.text(0.52, -0.42, "gateway", ha="center", va="center", fontsize=9, color=MUTED, zorder=3)
    ax.text(0, -0.64, "presenter", ha="center", va="center", fontsize=9, color=MUTED, zorder=3)
    ax.text(0, -0.40, "interactor", ha="center", va="center", fontsize=9, color=MUTED, zorder=3)

    # 依存の矢印: 外から内へ
    for ang in (150, 30):
        a = math.radians(ang)
        start = (1.12 * math.cos(a), 1.12 * math.sin(a))
        end = (0.32 * math.cos(a), 0.32 * math.sin(a))
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=14,
                color=INK,
                lw=1.4,
                zorder=4,
            )
        )
    ax.text(0, 1.12, "依存性のルール: ソースコードの依存は内側だけに向ける", ha="center", va="bottom", fontsize=10, color=INK)
    ax.text(-1.18, -1.1, "内側ほど高レベルの方針。内側は外側の名前を一切知らない", ha="left", va="center", fontsize=9.5, color=MUTED)

    save(fig, "ca-concentric.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tension_triangle()
    main_sequence()
    concentric()
