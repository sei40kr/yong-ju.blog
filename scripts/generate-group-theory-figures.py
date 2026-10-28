"""content/posts/group-theory.mdx の図を生成する。

出力先は public/img/grp-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-group-theory-figures.py
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Arc, FancyBboxPatch, Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
PURPLE = "#7c3aed"
INK = "#111827"
GRAY = "#6b7280"
LIGHT = "#d1d5db"

# 乗積表のセル色 (文字が読めるよう淡くする)
CELL = ["#dbeafe", "#fed7aa", "#dcfce7", "#ede9fe", "#fce7f3", "#e5e7eb"]

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
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


# ---------------------------------------------------------------- 二面体群 D3

# 頂点 0,1,2 の置換として表す。p[i] は「頂点 i の移り先」。
E = (0, 1, 2)
R = (1, 2, 0)  # 120 度回転
R2 = (2, 0, 1)
S = (0, 2, 1)  # 頂点 0 を通る鏡映
RS = (1, 0, 2)  # 頂点 2 を通る鏡映
R2S = (2, 1, 0)  # 頂点 1 を通る鏡映

D3 = [E, R, R2, S, RS, R2S]
D3_LABELS = ["$e$", "$r$", "$r^2$", "$s$", "$rs$", "$r^2s$"]


def compose(a, b):
    """(a∘b)(i) = a(b(i))"""
    return tuple(a[b[i]] for i in range(3))


def d3_table(order=None):
    """order で指定した並びの乗積表 (値は D3 上の添字) を返す。"""
    order = order or list(range(6))
    table = np.zeros((6, 6), dtype=int)
    for i, gi in enumerate(order):
        for j, gj in enumerate(order):
            table[i, j] = D3.index(compose(D3[gi], D3[gj]))
    return table


def cyclic_table(n):
    return np.array([[(i + j) % n for j in range(n)] for i in range(n)])


def draw_table(ax, table, labels, row_labels=None, col_labels=None, colors=None, fontsize=11):
    """乗積表を色分けしたマス目として描く。"""
    n = len(table)
    colors = colors or CELL
    ax.imshow(table, cmap=ListedColormap(colors[: max(int(table.max()) + 1, 1)]), vmin=0, vmax=len(colors[: int(table.max()) + 1]) - 1)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, labels[table[i, j]], ha="center", va="center", fontsize=fontsize)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(col_labels or labels, fontsize=fontsize)
    ax.set_yticklabels(row_labels or labels, fontsize=fontsize)
    ax.tick_params(length=0)
    ax.xaxis.set_ticks_position("top")
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.6)
    for side in ax.spines.values():
        side.set_visible(False)


def chip(
    ax,
    x,
    y,
    label,
    facecolor="#f3f4f6",
    edgecolor=LIGHT,
    w=0.78,
    h=0.6,
    fontsize=11,
    textcolor=INK,
):
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=facecolor,
            edgecolor=edgecolor,
            lw=1.0,
            zorder=2,
        )
    )
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, color=textcolor, zorder=3)


def bare(ax, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)


# ---------------------------------------------------------------- figure 1


def fig_symmetry():
    """群の具体例としての正三角形の対称性 (二面体群 D3)。"""
    fig, axes = plt.subplots(2, 3, figsize=(8.2, 5.4))
    angles = np.array([90, 210, 330]) * math.pi / 180
    pos = np.stack([np.cos(angles), np.sin(angles)], axis=1)

    notes = ["恒等変換", "$120°$ 回転", "$240°$ 回転", "鏡映", "鏡映", "鏡映"]
    for ax, g, label, note in zip(axes.ravel(), D3, D3_LABELS, notes):
        tri = np.vstack([pos, pos[:1]])
        ax.plot(tri[:, 0], tri[:, 1], color=INK, lw=1.4, zorder=2)
        ax.fill(pos[:, 0], pos[:, 1], color=BLUE, alpha=0.06, zorder=0)

        fixed = [i for i in range(3) if g[i] == i]
        if g in (R, R2):  # 回転は円弧の矢印で示す
            ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=90, theta2=90 + (120 if g == R else 240), color=ORANGE, lw=1.6))
            end = math.radians(90 + (120 if g == R else 240))
            ax.annotate(
                "",
                xy=(0.45 * math.cos(end), 0.45 * math.sin(end)),
                xytext=(0.45 * math.cos(end - 0.15), 0.45 * math.sin(end - 0.15)),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.6),
            )
        elif len(fixed) == 1:  # 鏡映は固定される頂点を通る軸を描く
            k = fixed[0]
            axis = pos[k]
            ax.plot([-axis[0] * 0.62, axis[0] * 1.45], [-axis[1] * 0.62, axis[1] * 1.45], color=ORANGE, lw=1.3, ls="--")

        for i in range(3):
            p = pos[g[i]] * 1.24
            ax.text(p[0], p[1], f"{i + 1}", ha="center", va="center", fontsize=11, color=BLUE, zorder=3)

        ax.set_title(f"{label}  ({note})", fontsize=11)
        bare(ax, (-1.6, 1.6), (-1.5, 1.6))
        ax.set_aspect("equal")

    fig.suptitle("正三角形を重ね合わせる 6 通りの動かし方は群をなす (二面体群 $D_3$)", y=1.0)
    fig.tight_layout()
    fig.text(
        0.5,
        -0.01,
        "動かし方の合成が二項演算、「動かさない」が単位元、逆向きの操作が逆元にあたる",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "grp-symmetry.svg")


# ---------------------------------------------------------------- figure 2


def fig_cayley():
    """乗積表。可換群は対角線に関して対称になる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.4))

    ax = axes[0]
    labels = [f"${i}$" for i in range(6)]
    draw_table(ax, cyclic_table(6), labels)
    ax.plot([-0.5, 5.5], [-0.5, 5.5], color=GREEN, lw=1.6, ls="--")
    ax.set_title("$\\mathbb{Z}/6\\mathbb{Z}$ (演算は $+$) — 可換群", pad=26)
    ax.text(2.5, 6.1, "対角線について対称", color=GREEN, fontsize=9.5, ha="center", va="top")

    ax = axes[1]
    table = d3_table()
    draw_table(ax, table, D3_LABELS)
    ax.plot([-0.5, 5.5], [-0.5, 5.5], color=GREEN, lw=1.6, ls="--")
    for (i, j), color in (((1, 3), ORANGE), ((3, 1), ORANGE)):
        ax.add_patch(
            Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor=color, lw=2.2, zorder=4)
        )
    ax.annotate(
        "$rs \\neq sr$ — 対称でない",
        xy=(3, 1),
        xytext=(2.5, 6.4),
        color=ORANGE,
        fontsize=9.5,
        ha="center",
        va="top",
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9),
    )
    ax.annotate("", xy=(1, 3), xytext=(2.5, 6.2), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9))
    ax.set_title("$D_3$ — 非可換群", pad=26)

    fig.text(
        0.5,
        0.02,
        "表の $(i, j)$ 成分は「行の元 $\\circ$ 列の元」。各行・各列に全ての元がちょうど 1 回ずつ現れる",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "grp-cayley.svg")


# ---------------------------------------------------------------- figure 3


def fig_subgroup():
    """部分群は乗積表の中の閉じたブロックとして見える。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.4))

    ax = axes[0]
    order = [0, 1, 2, 3, 4, 5]  # e, r, r^2 を先頭に並べておく
    table = d3_table(order)
    draw_table(ax, table, D3_LABELS)
    ax.add_patch(Rectangle((-0.5, -0.5), 3, 3, fill=False, edgecolor=GREEN, lw=2.4, zorder=4))
    ax.set_title("$D_3$ の乗積表", pad=26)
    ax.annotate(
        "$H=\\{e,r,r^2\\}$ どうしの積は必ず $H$ に入る\n(演算について閉じている)",
        xy=(1.0, 1.0),
        xytext=(2.5, 6.2),
        color=GREEN,
        fontsize=9.5,
        ha="center",
        va="top",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9),
    )

    ax = axes[1]
    nodes = {
        "$D_3$": (0.0, 2.0),
        "$\\{e,r,r^2\\}$": (-1.25, 1.0),
        "$\\{e,s\\}$": (-0.1, 1.0),
        "$\\{e,rs\\}$": (0.85, 1.0),
        "$\\{e,r^2s\\}$": (1.85, 1.0),
        "$\\{e\\}$": (0.0, 0.0),
    }
    orders = {"$D_3$": 6, "$\\{e,r,r^2\\}$": 3, "$\\{e,s\\}$": 2, "$\\{e,rs\\}$": 2, "$\\{e,r^2s\\}$": 2, "$\\{e\\}$": 1}
    for name, (x, y) in nodes.items():
        if y == 1.0:
            for target in ("$D_3$", "$\\{e\\}$"):
                tx, ty = nodes[target]
                ax.plot([x, tx], [y, ty], color=LIGHT, lw=1.0, zorder=0)
    for name, (x, y) in nodes.items():
        color = GREEN if name == "$\\{e,r,r^2\\}$" else "#f3f4f6"
        chip(ax, x, y, name, facecolor=color if name != "$\\{e,r,r^2\\}$" else "#dcfce7", w=1.0, h=0.34, fontsize=10)
        ax.text(x, y - 0.28, f"位数 {orders[name]}", ha="center", fontsize=8.5, color=GRAY)
    ax.set_title("$D_3$ の部分群", pad=26)
    bare(ax, (-2.1, 2.6), (-0.55, 2.45))
    ax.text(
        -2.05,
        2.3,
        "部分群の位数はいつも $|G|=6$ の約数になる",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "grp-subgroup.svg")


# ---------------------------------------------------------------- figure 4


def fig_equivalence():
    """同値関係・同値類・商集合。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    classes = [[0, 4, 8], [1, 5, 9], [2, 6, 10], [3, 7, 11]]
    palette = [CELL[0], CELL[1], CELL[2], CELL[3]]
    edges = [BLUE, ORANGE, GREEN, PURPLE]

    ax = axes[0]
    for n in range(12):
        k = n % 4
        chip(ax, n % 6, -(n // 6), f"${n}$", facecolor=palette[k], edgecolor=edges[k], w=0.72, h=0.62)
    ax.set_title("集合 $S=\\{0,1,\\dots,11\\}$", pad=10)
    ax.text(-0.55, 0.72, "$x \\sim y \\ \\Leftrightarrow\\ x \\equiv y \\ (\\text{mod}\\ 4)$", fontsize=10, color=GRAY)
    bare(ax, (-0.6, 5.6), (-1.55, 1.05))

    ax = axes[1]
    for k, members in enumerate(classes):
        cx = k * 1.35
        ax.add_patch(
            FancyBboxPatch(
                (cx - 0.52, -0.95),
                1.04,
                1.75,
                boxstyle="round,pad=0.02,rounding_size=0.12",
                facecolor=palette[k],
                edgecolor=edges[k],
                lw=1.2,
                zorder=1,
            )
        )
        for i, m in enumerate(members):
            ax.text(cx, 0.45 - 0.5 * i, f"${m}$", ha="center", va="center", fontsize=10.5, zorder=3)
        ax.text(cx, 1.05, f"$C({k})$", ha="center", fontsize=10.5, color=edges[k])
    ax.set_title("商集合 $S/\\sim$ — 同値類が新しい元になる", pad=10)
    bare(ax, (-0.8, 4.75), (-1.5, 1.55))
    ax.text(
        -0.7,
        -1.32,
        "同値類は互いに重ならず、全体を覆い尽くす (類別)",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "grp-equivalence.svg")


# ---------------------------------------------------------------- figure 5


def fig_coset():
    """左剰余類による分割と、|H| = |aH| を与える全単射。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8))

    H = [0, 3]  # {e, s}
    cosets = []
    for a in (0, 1, 2):  # e, r, r^2 を代表元にとる
        cosets.append([D3.index(compose(D3[a], D3[h])) for h in H])
    names = ["$eH = H$", "$rH$", "$r^2H$"]
    edges = [GREEN, BLUE, PURPLE]
    fills = [CELL[2], CELL[0], CELL[3]]

    ax = axes[0]
    for k, (members, name) in enumerate(zip(cosets, names)):
        x0 = k * 2.1
        ax.add_patch(
            FancyBboxPatch(
                (x0 - 0.6, -0.45),
                1.9,
                0.9,
                boxstyle="round,pad=0.02,rounding_size=0.12",
                facecolor=fills[k],
                edgecolor=edges[k],
                lw=1.3,
                zorder=1,
            )
        )
        ax.text(x0 + 0.35, 0.62, name, ha="center", fontsize=11, color=edges[k])
        for i, m in enumerate(members):
            chip(ax, x0 + 0.7 * i, 0, D3_LABELS[m], facecolor="white", edgecolor=edges[k], w=0.62, h=0.56, fontsize=10.5)
    ax.set_title("$G=D_3$ を $H=\\{e,s\\}$ の左剰余類で分ける", pad=10)
    bare(ax, (-0.9, 5.9), (-1.5, 1.05))
    ax.text(
        -0.85,
        -1.0,
        "どの剰余類も大きさは $|H|=2$\n$\\Rightarrow |G| = |H| \\times ($剰余類の個数$)$",
        fontsize=9.5,
        color=GRAY,
        linespacing=1.6,
    )

    ax = axes[1]
    for i, h in enumerate(H):
        chip(ax, 0, -i, D3_LABELS[h], facecolor=CELL[2], edgecolor=GREEN, w=0.7, h=0.6)
        chip(ax, 2.2, -i, D3_LABELS[cosets[1][i]], facecolor=CELL[0], edgecolor=BLUE, w=0.7, h=0.6)
        ax.annotate(
            "",
            xy=(1.8, -i),
            xytext=(0.42, -i),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.1),
        )
        ax.text(1.1, -i + 0.16, "$h \\mapsto rh$", ha="center", fontsize=9.5, color=GRAY)
    ax.text(0, 0.75, "$H$", ha="center", fontsize=12, color=GREEN)
    ax.text(2.2, 0.75, "$rH$", ha="center", fontsize=12, color=BLUE)
    ax.set_title("$h \\mapsto ah$ は全単射", pad=10)
    bare(ax, (-0.75, 3.0), (-1.9, 1.15))
    ax.text(-0.7, -1.55, "だから $|H| = |aH|$ が成り立つ", fontsize=9.5, color=GRAY)
    save(fig, "grp-coset.svg")


# ---------------------------------------------------------------- figure 6


def fig_normal():
    """左剰余類と右剰余類が一致するかどうかが正規部分群の分かれ目。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.2))

    def cosets_of(sub, a, side):
        if side == "left":
            return [D3.index(compose(D3[a], D3[h])) for h in sub]
        return [D3.index(compose(D3[h], D3[a])) for h in sub]

    cases = (
        (axes[0], [0, 3], "$H=\\{e,s\\}$", [0, 1, 2], False),
        (axes[1], [0, 1, 2], "$N=\\{e,r,r^2\\}$", [0, 3], True),
    )
    for ax, sub, name, reps, normal in cases:
        fills = [CELL[2], CELL[0], CELL[3]]
        edges = [GREEN, BLUE, PURPLE]
        for k, a in enumerate(reps):
            left = cosets_of(sub, a, "left")
            right = cosets_of(sub, a, "right")
            width = 0.72 * len(sub) + 0.5
            x0 = k * (width + 0.55)
            for row, members, tag in ((0.55, left, "$aH$" if not normal else "$aN$"), (-0.85, right, "$Ha$" if not normal else "$Na$")):
                ax.add_patch(
                    FancyBboxPatch(
                        (x0 - 0.45, row - 0.42),
                        width,
                        0.84,
                        boxstyle="round,pad=0.02,rounding_size=0.1",
                        facecolor=fills[k],
                        edgecolor=edges[k],
                        lw=1.2,
                        zorder=1,
                    )
                )
                for i, m in enumerate(sorted(members)):
                    chip(
                        ax,
                        x0 + 0.72 * i,
                        row,
                        D3_LABELS[m],
                        facecolor="white",
                        edgecolor=edges[k],
                        w=0.64,
                        h=0.56,
                        fontsize=10,
                    )
            same = sorted(left) == sorted(right)
            ax.text(
                x0 + width / 2 - 0.45,
                -0.15,
                "$=$" if same else "$\\neq$",
                ha="center",
                va="center",
                fontsize=13,
                color=GREEN if same else ORANGE,
            )
            ax.text(
                x0 + width / 2 - 0.45,
                1.35,
                f"$a = {D3_LABELS[a][1:-1]}$",
                ha="center",
                fontsize=10,
                color=edges[k],
            )
        ax.text(-1.35, 0.55, "左剰余類", fontsize=10, color=GRAY, ha="center")
        ax.text(-1.35, -0.85, "右剰余類", fontsize=10, color=GRAY, ha="center")
        ax.set_title(name + ("（正規部分群）" if normal else "（正規部分群でない）"), pad=10)
        bare(ax, (-2.0, 6.8), (-2.1, 1.75))
        ax.text(
            -1.9,
            -1.75,
            "全ての $a$ で一致 $\\Rightarrow N \\trianglelefteq G$"
            if normal
            else "一致しない $a$ がある $\\Rightarrow$ 正規でない",
            fontsize=9.5,
            color=GREEN if normal else ORANGE,
        )
    save(fig, "grp-normal.svg")


# ---------------------------------------------------------------- figure 7


def fig_quotient():
    """剰余群 G/N は、乗積表がブロックごとにまとまることで定義できる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.4), gridspec_kw=dict(width_ratios=[1.7, 1]))

    order = [0, 1, 2, 3, 4, 5]  # N = {e,r,r^2} が先頭 3 つ
    table = d3_table(order)
    ax = axes[0]
    # セルの色は「積がどちらの剰余類に入るか」で塗り分ける
    block = (table >= 3).astype(int)
    ax.imshow(block, cmap=ListedColormap([CELL[2], CELL[1]]), vmin=0, vmax=1)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, D3_LABELS[table[i, j]], ha="center", va="center", fontsize=10.5)
    ax.set_xticks(range(6))
    ax.set_yticks(range(6))
    ax.set_xticklabels(D3_LABELS, fontsize=10.5)
    ax.set_yticklabels(D3_LABELS, fontsize=10.5)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 6, 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.4)
    for k in (2.5,):
        ax.axhline(k, color=INK, lw=1.8)
        ax.axvline(k, color=INK, lw=1.8)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("$N=\\{e,r,r^2\\}$ で区切った $D_3$ の乗積表", pad=26)
    ax.text(-1.6, 1.0, "$N$", fontsize=12, color=GREEN, va="center")
    ax.text(-1.6, 4.0, "$sN$", fontsize=12, color=ORANGE, va="center")

    ax = axes[1]
    q = np.array([[0, 1], [1, 0]])
    qlabels = ["$N$", "$sN$"]
    ax.imshow(q, cmap=ListedColormap([CELL[2], CELL[1]]), vmin=0, vmax=1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, qlabels[q[i, j]], ha="center", va="center", fontsize=12)
    ax.set_xticks(range(2))
    ax.set_yticks(range(2))
    ax.set_xticklabels(qlabels, fontsize=12)
    ax.set_yticklabels(qlabels, fontsize=12)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(-0.5, 2, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 2, 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.6)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("剰余群 $D_3/N$", pad=26)

    fig.text(
        0.5,
        0.0,
        "各ブロックの積が 1 つの剰余類に収まるので $aN \\cdot bN = abN$ が定義でき、$D_3/N \\simeq \\mathbb{Z}/2\\mathbb{Z}$",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "grp-quotient.svg")


# ---------------------------------------------------------------- figure 8


FADE = "#f9fafb"  # 像に含まれない元は薄く描く


def fig_kernel_image():
    """準同型写像 f: D3 → Z/6Z の核と像。"""
    fig, ax = plt.subplots(figsize=(8.4, 4.9))

    gx, hx = 0.0, 5.8
    ys = [2.5, 1.5, 0.5, -0.5, -1.5, -2.5]
    # 回転を 0 に、鏡映を 3 に写す。これは準同型写像になっている。
    values = [0, 0, 0, 3, 3, 3]

    for label, v, y in zip(D3_LABELS, values, ys):
        color, fill = (GREEN, CELL[2]) if v == 0 else (ORANGE, CELL[1])
        chip(ax, gx, y, label, facecolor=fill, edgecolor=color, w=0.82, h=0.62)
        ax.annotate(
            "",
            xy=(hx - 0.48, 2.5 if v == 0 else -0.5),
            xytext=(gx + 0.48, y),
            arrowprops=dict(arrowstyle="->", color=color, lw=1.0, alpha=0.7),
        )

    for i, y in enumerate(ys):
        in_image = i in (0, 3)
        color, fill = (GREEN, CELL[2]) if i == 0 else ((ORANGE, CELL[1]) if i == 3 else (LIGHT, FADE))
        chip(
            ax,
            hx,
            y,
            f"${i}$",
            facecolor=fill,
            edgecolor=color,
            w=0.82,
            h=0.62,
            textcolor=INK if in_image else GRAY,
        )
        if in_image:  # 像に入る元だけを枠で囲む
            ax.add_patch(
                Rectangle(
                    (hx - 0.58, y - 0.44), 1.16, 0.88, fill=False, edgecolor=BLUE, lw=1.5, ls="--", zorder=4
                )
            )

    # 核 = 単位元 0 に写る元全体
    ax.add_patch(Rectangle((gx - 0.58, 0.06), 1.16, 2.88, fill=False, edgecolor=GREEN, lw=1.6, ls="--", zorder=4))
    ax.text(gx - 0.68, 1.5, "$\\ker f$", fontsize=12, color=GREEN, ha="right", va="center")
    # 残りの元は核の剰余類 (ファイバー) をなす
    ax.add_patch(Rectangle((gx - 0.58, -2.94), 1.16, 2.88, fill=False, edgecolor=ORANGE, lw=1.2, ls=":", zorder=4))
    ax.text(gx - 0.68, -1.5, "$s\\ker f$", fontsize=11, color=ORANGE, ha="right", va="center")

    for y in (2.5, -0.5):
        ax.annotate(
            "",
            xy=(hx + 0.62, y),
            xytext=(7.55, 1.0),
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.9),
        )
    ax.text(7.6, 1.0, "$\\text{im}f$", fontsize=12, color=BLUE, va="center")

    ax.text(gx, 3.3, "$G = D_3$", ha="center", fontsize=12)
    ax.text(hx, 3.3, "$G' = \\mathbb{Z}/6\\mathbb{Z}$", ha="center", fontsize=12)
    ax.text(2.9, 3.3, "$f$ : 回転 $\\mapsto 0$, 鏡映 $\\mapsto 3$", ha="center", fontsize=10.5, color=GRAY)

    for i, note in enumerate(
        (
            "$\\ker f$ : 単位元 $e'=0$ に写る元を集めたもの。$G$ の正規部分群になる",
            "$\\text{im}f$ : 値として実際に現れる元を集めたもの。$G'$ の部分群になる",
            "$f$ は全射ではないので $\\text{im}f \\neq G'$。$1,2,4,5$ にはどの元も写らない",
            "行き先が同じ元の集まりは $\\ker f$ の剰余類そのもので、大きさはどれも $|\\ker f|$",
        )
    ):
        ax.text(-1.9, -3.35 - 0.45 * i, note, fontsize=9.5, color=GRAY)

    bare(ax, (-2.6, 8.4), (-5.3, 3.7))
    save(fig, "grp-kernel-image.svg")


# ---------------------------------------------------------------- figure 9


def fig_first_isomorphism():
    """準同型定理 G/ker f ≃ im f。"""
    fig, ax = plt.subplots(figsize=(8.2, 4.0))

    left = [(0.0, y) for y in (1.9, 1.15, 0.4, -0.4, -1.15, -1.9)]
    for (x, y), label, s in zip(left, D3_LABELS, [1, 1, 1, -1, -1, -1]):
        chip(ax, x, y, label, facecolor=CELL[2] if s == 1 else CELL[1], edgecolor=GREEN if s == 1 else ORANGE, w=0.8, h=0.6)
    ax.text(0, 2.6, "$G = D_3$", ha="center", fontsize=12)

    for y, label, fill, edge in ((1.15, "$\\ker f$", CELL[2], GREEN), (-1.15, "$s\\ker f$", CELL[1], ORANGE)):
        chip(ax, 3.0, y, label, facecolor=fill, edgecolor=edge, w=1.25, h=0.7, fontsize=11)
    ax.text(3.0, 2.6, "$G/\\ker f$", ha="center", fontsize=12)

    # 終域 G' のうち、実際に到達するのは im f = {0,3} だけ
    ax.add_patch(
        FancyBboxPatch(
            (5.2, -2.25),
            2.25,
            4.5,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor="#fafafa",
            edgecolor=LIGHT,
            lw=1.0,
            zorder=0,
        )
    )
    for y, label, fill, edge in ((1.15, "$0$", CELL[2], GREEN), (-1.15, "$3$", CELL[1], ORANGE)):
        chip(ax, 5.75, y, label, facecolor=fill, edgecolor=edge, w=0.8, h=0.7, fontsize=11)
    ax.add_patch(
        Rectangle((5.3, -1.65), 0.9, 3.3, fill=False, edgecolor=BLUE, lw=1.5, ls="--", zorder=4)
    )
    ax.text(5.75, -1.95, "$\\text{im}f$", ha="center", fontsize=11, color=BLUE)
    for y, label in ((1.55, "$1$"), (0.65, "$2$"), (-0.65, "$4$"), (-1.55, "$5$")):
        chip(ax, 6.85, y, label, facecolor=FADE, edgecolor=LIGHT, w=0.7, h=0.6, fontsize=10, textcolor=GRAY)
    ax.text(6.85, -1.95, "到達しない元", ha="center", fontsize=8.5, color=GRAY)
    ax.text(6.3, 2.6, "$G' = \\mathbb{Z}/6\\mathbb{Z}$", ha="center", fontsize=12)

    for ys, color in (((1.9, 1.15, 0.4), GREEN), ((-0.4, -1.15, -1.9), ORANGE)):
        for y in ys:
            ax.annotate(
                "",
                xy=(2.3, 1.15 if color is GREEN else -1.15),
                xytext=(0.45, y),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.0, alpha=0.7),
            )
    for y, color in ((1.15, GREEN), (-1.15, ORANGE)):
        ax.annotate(
            "",
            xy=(5.3, y),
            xytext=(3.7, y),
            arrowprops=dict(arrowstyle="->", color=color, lw=1.4),
        )
    # 準同型写像 f そのものは、下側を回して直接つなぐ
    ax.annotate(
        "",
        xy=(5.7, -2.85),
        xytext=(0.1, -2.85),
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2, connectionstyle="arc3,rad=0.14"),
    )

    ax.text(1.35, 0.05, "自然な射影\n$x \\mapsto x\\ker f$", ha="center", fontsize=9.5, color=GRAY, linespacing=1.5)
    ax.text(4.5, 1.35, "$\\varphi$ : 同型写像", ha="center", fontsize=10, color=INK)
    ax.text(2.9, -3.9, "$f$", ha="center", fontsize=12, color=BLUE)
    ax.text(
        3.2,
        -4.5,
        "核でつぶしてから見れば、準同型写像は像との同型写像になる  $G/\\ker f \\simeq \\text{im}f$",
        ha="center",
        fontsize=10,
        color=GRAY,
    )
    bare(ax, (-1.0, 7.8), (-5.0, 3.1))
    save(fig, "grp-first-isomorphism.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_symmetry()
    fig_cayley()
    fig_subgroup()
    fig_equivalence()
    fig_coset()
    fig_normal()
    fig_quotient()
    fig_kernel_image()
    fig_first_isomorphism()
