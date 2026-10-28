"""content/posts/secure-computation.mdx の図を生成する。

出力先は public/img/mpc-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-mpc-figures.py

環境変数 MPC_FIG_PNG_DIR を指定すると、目視確認用の PNG も同時に書き出す。
"""

import math
import os
import random
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, FancyArrowPatch, FancyBboxPatch, Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"
PNG_DIR = os.environ.get("MPC_FIG_PNG_DIR")

INK = "#111827"
MUTED = "#6b7280"
LINE = "#9ca3af"
FAINT = "#e5e7eb"
BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
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


def bare(ax, xlim, ylim, title=None, equal=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    if equal:
        ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(False)
    if title:
        ax.set_title(title)


def box(ax, xy, w, h, text, *, fc="white", ec=INK, color=INK, fontsize=10.5, lw=1.2):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.015,rounding_size=0.09",
            facecolor=fc,
            edgecolor=ec,
            linewidth=lw,
            zorder=3,
        )
    )
    ax.text(
        x,
        y,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color,
        zorder=4,
        linespacing=1.5,
    )


def arrow(
    ax,
    start,
    end,
    *,
    color=INK,
    lw=1.3,
    style="-|>",
    ls="-",
    rad=0.0,
    shrink=7,
    label=None,
    dx=0.0,
    dy=0.14,
    off=0.0,
    fontsize=9.5,
    ha="center",
    va="bottom",
    labelcolor=None,
):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            color=color,
            lw=lw,
            linestyle=ls,
            shrinkA=shrink,
            shrinkB=shrink,
            mutation_scale=13,
            connectionstyle=f"arc3,rad={rad}",
            zorder=2,
        )
    )
    if label:
        # 曲がった矢印では、弧の中点 (弦の中点から法線方向に rad/2 だけずれる) を基準にする
        vx, vy = end[0] - start[0], end[1] - start[1]
        norm = np.hypot(vx, vy) or 1.0
        px, py = -vy / norm, vx / norm
        bulge = rad / 2 * norm + off
        ax.text(
            (start[0] + end[0]) / 2 + px * bulge + dx,
            (start[1] + end[1]) / 2 + py * bulge + dy,
            label,
            fontsize=fontsize,
            color=labelcolor or color,
            ha=ha,
            va=va,
            zorder=5,
            linespacing=1.4,
        )


# ------------------------------------------------------- figure 1: 問題設定


def fig_overview():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2))
    pos = [
        (r * np.cos(np.deg2rad(a)), r * np.sin(np.deg2rad(a)))
        for a in (90, 210, 330)
        for r in (1.55,)
    ]
    inputs = ["$x_1$", "$x_2$", "$x_3$"]

    ax = axes[0]
    box(ax, (0, 0), 1.65, 0.76, "信頼できる\n第三者", fc="#f3f4f6", ec=MUTED)
    for i, ((x, y), label) in enumerate(zip(pos, inputs)):
        box(ax, (x, y), 0.72, 0.44, label.replace("x", "P"), fc="white")
        arrow(
            ax,
            (x, y),
            (0, 0),
            rad=0.24,
            color=BLUE,
            shrink=18,
            label=label,
            off=0.5,
            dy=0,
            va="center",
        )
        arrow(
            ax,
            (0, 0),
            (x, y),
            rad=0.24,
            color=LINE,
            ls="--",
            shrink=18,
            label="$y$" if i == 0 else None,
            off=0.42,
            dy=0,
            va="center",
            labelcolor=MUTED,
        )
    bare(ax, (-2.6, 2.6), (-2.4, 2.6), "理想世界: 全員が第三者に入力を預ける")

    ax = axes[1]
    for i, ((x, y), label) in enumerate(zip(pos, inputs)):
        box(ax, (x, y), 0.72, 0.44, label.replace("x", "P"))
        ax.text(
            x * 1.40,
            y * 1.40,
            "$y$",
            color=GREEN,
            fontsize=10,
            ha="center",
            va="center",
        )
        arrow(
            ax,
            (x, y),
            (x * 1.26, y * 1.26),
            color=GREEN,
            ls="--",
            shrink=13,
            lw=1.1,
        )
    for i in range(3):
        arrow(
            ax,
            pos[i],
            pos[(i + 1) % 3],
            style="<|-|>",
            color=PURPLE,
            rad=0.16,
            shrink=15,
        )
    ax.text(
        0,
        -0.05,
        "シェア・暗号文の\nやりとりだけ",
        color=PURPLE,
        fontsize=10,
        ha="center",
        va="center",
        linespacing=1.5,
    )
    bare(ax, (-2.6, 2.6), (-2.4, 2.6), "現実世界: 第三者なしで同じ出力を得る")

    save(fig, "mpc-overview.svg")


# ------------------------------------------------- figure 2: 加法的秘密分散


def fig_additive():
    p = 32
    secret = 21

    fig, axd = plt.subplot_mosaic(
        [["circle", "scatter"], ["circle", "hist"]],
        figsize=(8.4, 4.8),
        height_ratios=[2.6, 1.0],
        gridspec_kw=dict(hspace=0.55, wspace=0.15),
    )

    # --- 左: Z_p を円と見て、シェアを弧としてつなぐ
    ax = axd["circle"]
    ax.add_patch(
        plt.Circle((0, 0), 1.0, fill=False, edgecolor=LINE, lw=1.2, zorder=1)
    )
    shares = [11, 26, 16]  # 11 + 26 + 16 = 53 = 21 + 32
    assert sum(shares) % p == secret
    colors = [BLUE, ORANGE, GREEN]
    start = 90.0
    for s, c, name in zip(shares, colors, ("$s_1$", "$s_2$", "$s_3$")):
        span = 360.0 * s / p
        ax.add_patch(
            Arc(
                (0, 0),
                2.0,
                2.0,
                theta1=start - span,
                theta2=start,
                color=c,
                lw=5.0,
                zorder=2,
            )
        )
        mid = np.deg2rad(start - span / 2)
        ax.text(
            1.34 * np.cos(mid),
            1.34 * np.sin(mid),
            f"{name} = {s}",
            color=c,
            fontsize=10.5,
            ha="left" if np.cos(mid) > 0.1 else ("right" if np.cos(mid) < -0.1 else "center"),
            va="center",
        )
        start -= span
    for ang, lab in ((90, "$0$"), (90 - 360 * secret / p, f"$s = {secret}$")):
        r = np.deg2rad(ang)
        ax.plot(
            [0.82 * np.cos(r), 1.16 * np.cos(r)],
            [0.82 * np.sin(r), 1.16 * np.sin(r)],
            color=INK,
            lw=1.2,
            zorder=4,
        )
        ax.text(
            1.30 * np.cos(r),
            1.30 * np.sin(r),
            lab,
            fontsize=11,
            ha="left" if np.cos(r) > 0.1 else ("right" if np.cos(r) < -0.1 else "center"),
            va="bottom" if np.sin(r) > 0 else "top",
        )
    ax.text(
        0,
        0,
        f"$\\mathbb{{Z}}_{{{p}}}$",
        fontsize=14,
        color=MUTED,
        ha="center",
        va="center",
    )
    ax.text(
        0,
        -1.72,
        f"$s_1 + s_2 + s_3 \\equiv {secret} \\; (\\mathrm{{mod}} \\; {p})$",
        fontsize=10.5,
        color=INK,
        ha="center",
        va="center",
    )
    bare(ax, (-2.15, 2.15), (-2.0, 1.9), "秘密を 3 つの弧に分ける")

    # --- 右上: 2 者の場合、(s_1, s_2) は秘密ごとに違う集合になるが……
    ax = axd["scatter"]
    q = 32
    cases = ((21, BLUE, "o", (18, 10.5)), (5, ORANGE, "s", (16, 26.5)))
    for sec, color, marker, at in cases:
        s1 = np.arange(q)
        s2 = (sec - s1) % q
        ax.scatter(s1, s2, s=13, color=color, marker=marker, zorder=3)
        ax.text(*at, f"$s = {sec}$", color=color, fontsize=10, ha="left")
    ax.set_xlim(-1, q)
    ax.set_ylim(-1, q)
    ax.set_xticks([0, q // 2, q - 1])
    ax.set_xticklabels([])
    ax.set_yticks([0, q // 2, q - 1])
    ax.set_ylabel("$s_2$")
    ax.set_title("$2$ 者の場合の $(s_1, s_2)$ の取りうる値", fontsize=11)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    # --- 右下: 上の点集合を s_1 軸に射影すると、どちらも 0..q-1 を 1 回ずつ
    ax = axd["hist"]
    for i, (sec, color, _, _) in enumerate(cases):
        counts = np.bincount((sec - np.arange(q)) % q, minlength=q) * 0 + 1
        ax.bar(np.arange(q) + (i - 0.5) * 0.42, counts, width=0.42, color=color)
    ax.set_xlim(-1, q)
    ax.set_ylim(0, 1.6)
    ax.set_xticks([0, q // 2, q - 1])
    ax.set_yticks([0, 1])
    ax.set_xlabel("$s_1$")
    ax.set_title("$s_1$ の分布は秘密によらず一様", fontsize=10.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    save(fig, "mpc-additive-sharing.svg")


# --------------------------------------------- figure 3: Shamir の秘密分散


def lagrange_interpolate_real(xs, ys, grid):
    out = np.zeros_like(grid, dtype=float)
    for xi, yi in zip(xs, ys):
        term = np.ones_like(grid, dtype=float) * yi
        for xj in xs:
            if xj != xi:
                term = term * (grid - xj) / (xi - xj)
        out = out + term
    return out


def fig_shamir():
    secret = 6.0
    coeffs = [secret, -3.4, 1.05]  # f(x) = 6 - 3.4x + 1.05x^2
    f = lambda x: coeffs[0] + coeffs[1] * x + coeffs[2] * x**2
    xs = np.arange(1, 6)
    grid = np.linspace(-0.4, 5.6, 400)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9), sharey=True)

    ax = axes[0]
    ax.plot(grid, f(grid), color=BLUE, lw=2.0, zorder=2)
    ax.scatter(xs, f(xs), s=52, color=BLUE, edgecolors="white", zorder=4)
    for x in xs:
        ax.plot([x, x], [0, f(x)], color=LINE, lw=0.7, ls=":", zorder=1)
        ax.annotate(
            f"$s_{{{int(x)}}}$",
            xy=(x, f(x)),
            xytext=(0, 12),
            textcoords="offset points",
            fontsize=9.5,
            color=BLUE,
            ha="center",
        )
    ax.scatter([0], [secret], s=90, color=RED, marker="*", zorder=5)
    ax.annotate(
        "秘密 $s = f(0)$",
        xy=(0, secret),
        xytext=(0.85, 12.6),
        fontsize=10,
        color=RED,
        ha="left",
        arrowprops=dict(arrowstyle="->", color=RED, lw=0.9),
    )
    ax.set_title("分散: $f(0) = s$ なる 2 次多項式を作る")

    ax = axes[1]
    pick = np.array([1, 3, 5])
    ax.plot(grid, f(grid), color=LINE, lw=1.2, ls="--", zorder=1)
    ax.plot(
        grid,
        lagrange_interpolate_real(pick, f(pick), grid),
        color=GREEN,
        lw=2.0,
        zorder=2,
    )
    ax.scatter(pick, f(pick), s=52, color=GREEN, edgecolors="white", zorder=4)
    ax.scatter(
        [2, 4], f(np.array([2.0, 4.0])), s=42, facecolors="none", edgecolors=LINE, zorder=3
    )
    ax.scatter([0], [secret], s=90, color=RED, marker="*", zorder=5)
    ax.annotate(
        "$3$ 点で多項式が定まり\n$f(0)$ が復元できる",
        xy=(0, secret),
        xytext=(1.1, 12.0),
        fontsize=10,
        color=INK,
        ha="left",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LINE, lw=0.9),
    )
    ax.annotate(
        "使わないシェア",
        xy=(2, f(2.0)),
        xytext=(2.3, 1.0),
        fontsize=9,
        color=MUTED,
        ha="left",
        arrowprops=dict(arrowstyle="->", color=LINE, lw=0.8),
    )
    ax.set_title("復元: $k = 3$ 個のシェアがあれば十分")

    for ax in axes:
        ax.axhline(0, color=FAINT, lw=1.0)
        ax.axvline(0, color=FAINT, lw=1.0)
        ax.set_xlim(-0.6, 5.8)
        ax.set_ylim(-1.5, 17.5)
        ax.set_xlabel("$x$")
        ax.set_xticks(range(6))
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    axes[0].set_ylabel("$f(x)$")

    save(fig, "mpc-shamir.svg")


# ------------------------------------- figure 4: 情報理論的安全性


def fig_shamir_security():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9))

    # --- 左: 2 点を通る 2 次多項式は f(0) をいくらでも取れる
    ax = axes[0]
    known = np.array([2.0, 4.0])
    known_y = np.array([3.5, 6.8])
    grid = np.linspace(-0.4, 5.4, 400)
    for s0 in np.linspace(-2.0, 14.0, 9):
        ys = lagrange_interpolate_real(
            np.array([0.0, *known]), np.array([s0, *known_y]), grid
        )
        ax.plot(grid, ys, color=BLUE, lw=1.0, alpha=0.5, zorder=1)
        ax.scatter([0], [s0], s=22, color=BLUE, alpha=0.6, zorder=3)
    ax.scatter(known, known_y, s=60, color=INK, zorder=5, edgecolors="white")
    ax.annotate(
        "知っている 2 つのシェア",
        xy=(known[1], known_y[1]),
        xytext=(-6, 22),
        textcoords="offset points",
        fontsize=9.5,
        color=INK,
        ha="right",
        arrowprops=dict(arrowstyle="->", color=LINE, lw=0.9),
    )
    ax.text(
        1.15,
        14.6,
        "$f(0)$ はどの値でもありうる",
        fontsize=9.5,
        color=BLUE,
        ha="left",
    )
    ax.axhline(0, color=FAINT, lw=1.0)
    ax.axvline(0, color=FAINT, lw=1.0)
    ax.set_xlim(-0.6, 5.4)
    ax.set_ylim(-4, 17)
    ax.set_xlabel("$x$")
    ax.set_xticks(range(6))
    ax.set_title("$k - 1$ 点では多項式が定まらない")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    # --- 右: GF(p) 上で、候補となる多項式の個数を数え上げる
    p = 31
    a1_true, a2_true = 17, 8
    secret = 13
    obs = {x: (secret + a1_true * x + a2_true * x * x) % p for x in (1, 2)}
    counts = np.zeros(p, dtype=int)
    for s in range(p):
        for a1 in range(p):
            for a2 in range(p):
                if all((s + a1 * x + a2 * x * x) % p == y for x, y in obs.items()):
                    counts[s] += 1
    assert counts.tolist() == [1] * p, counts.tolist()

    ax = axes[1]
    ax.bar(np.arange(p), counts, color=ORANGE, width=0.8)
    ax.set_xlim(-1, p)
    ax.set_ylim(0, 2.2)
    ax.set_yticks([0, 1, 2])
    ax.set_xlabel("候補となる秘密 $s$")
    ax.set_ylabel("整合する多項式の個数")
    ax.set_title(f"$\\mathrm{{GF}}({p})$ 上での数え上げ ($k = 3$, シェア 2 個)")
    ax.text(
        p / 2,
        1.75,
        "どの $s$ もちょうど 1 通り\n= 事後分布は一様 = 何も分からない",
        fontsize=9.5,
        color=INK,
        ha="center",
        va="center",
        linespacing=1.5,
    )
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    save(fig, "mpc-shamir-security.svg")


# --------------------------------------------- figure 5: 乗算と次数の増加


def fig_degree():
    f = lambda x: 3.0 - 1.6 * x + 0.42 * x**2
    g = lambda x: 1.2 + 1.15 * x - 0.22 * x**2
    grid = np.linspace(-0.3, 6.4, 500)
    xs = np.arange(1, 6)

    fig, ax = plt.subplots(figsize=(7.6, 4.8))
    ax.plot(grid, f(grid), color=BLUE, lw=1.8, label="$f$ (次数 $t = 2$), $f(0) = x$")
    ax.plot(grid, g(grid), color=GREEN, lw=1.8, label="$g$ (次数 $t = 2$), $g(0) = y$")
    ax.plot(
        grid,
        f(grid) * g(grid),
        color=ORANGE,
        lw=2.2,
        label="$h = fg$ (次数 $2t = 4$), $h(0) = xy$",
    )
    ax.scatter(xs, f(xs) * g(xs), s=44, color=ORANGE, edgecolors="white", zorder=4)
    ax.scatter([0], [f(0) * g(0)], s=120, color=RED, marker="*", zorder=5)

    ax.annotate(
        "各者はローカルに $f(i) \\cdot g(i)$ を掛けるだけ\nしかし復元には $2t + 1 = 5$ 点が必要",
        xy=(4.0, f(4.0) * g(4.0)),
        xytext=(0.35, 11.6),
        fontsize=10,
        color=INK,
        linespacing=1.6,
        arrowprops=dict(arrowstyle="->", color=LINE, lw=0.9),
    )
    ax.annotate(
        "秘密は $x = 0$ での値\n$h(0) = f(0) \\, g(0) = xy$",
        xy=(0, f(0) * g(0)),
        xytext=(0.15, -8.4),
        fontsize=10,
        color=RED,
        ha="left",
        linespacing=1.6,
        arrowprops=dict(arrowstyle="->", color=RED, lw=0.9),
    )
    ax.axhline(0, color=FAINT, lw=1.0)
    ax.axvline(0, color=FAINT, lw=1.0)
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-11.5, 15)
    ax.set_xlabel("$x$")
    ax.set_xticks(range(7))
    ax.set_title("シェアの積は「次数が倍の多項式のシェア」になる")
    ax.legend(loc="lower right", fontsize=9.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    save(fig, "mpc-degree.svg")


# ------------------------------------------------- figure 6: Beaver triple


def sequence_chart(ax, cols, *, top=0.0, bottom=-1.0, colw=1.5):
    for x, name in cols:
        box(ax, (x, top), colw, 0.5, name, fc="#f3f4f6", ec=MUTED, fontsize=11)
        ax.plot([x, x], [top - 0.3, bottom], color=LINE, lw=0.9, ls=(0, (3, 4)), zorder=1)


def note(ax, x, y, w, text, *, fc="#f9fafb", ec=FAINT, fontsize=9.8, h=0.52, color=INK):
    box(ax, (x, y), w, h, text, fc=fc, ec=ec, fontsize=fontsize, lw=1.0, color=color)


def fig_beaver():
    fig, ax = plt.subplots(figsize=(8.0, 5.4))
    left, right = 0.0, 4.2
    sequence_chart(ax, [(left, "$P_1$"), (right, "$P_2$")], top=3.5, bottom=-2.9)

    mid = (left + right) / 2
    note(
        ax,
        mid,
        2.72,
        5.6,
        "オフライン (入力を知る前): 乱数三つ組 $[a], [b], [c]$  ただし $c = ab$  を配布しておく",
        fc="#eff6ff",
        ec=BLUE,
        color=BLUE,
        h=0.5,
    )
    note(
        ax,
        mid,
        1.95,
        5.6,
        "① 各者がローカルに $[d] = [x] - [a]$,  $[e] = [y] - [b]$ を計算",
        h=0.46,
    )
    arrow(ax, (left, 1.34), (right, 1.34), color=ORANGE, label="$d_1, e_1$", dy=0.1)
    arrow(ax, (right, 0.74), (left, 0.74), color=ORANGE, label="$d_2, e_2$", dy=0.1)
    ax.text(
        mid,
        0.30,
        "② 部分シェアを公開して $d = x - a$,  $e = y - b$ を復元",
        fontsize=9.8,
        color=ORANGE,
        ha="center",
        va="center",
    )
    note(
        ax,
        mid,
        -0.55,
        5.6,
        "③ 通信なしで $[z] = [c] + d\\,[b] + e\\,[a] + de$",
        h=0.46,
    )
    note(
        ax,
        mid,
        -1.45,
        5.6,
        "$z = ab + (x-a)b + (y-b)a + (x-a)(y-b) = xy$",
        fc="#f0fdf4",
        ec=GREEN,
        color=GREEN,
        h=0.5,
    )
    note(
        ax,
        mid,
        -2.42,
        5.6,
        "$d$, $e$ は一様乱数 $a$, $b$ でマスクされているので、公開しても $x$, $y$ は漏れない",
        fc="white",
        ec=FAINT,
        color=MUTED,
        h=0.5,
        fontsize=9.3,
    )

    bare(
        ax,
        (-1.15, 5.35),
        (-2.95, 3.95),
        "Beaver triple による乗算 (通信は 1 ラウンド)",
        equal=False,
    )
    save(fig, "mpc-beaver.svg")


# --------------------------------------------------------- figure 7: OT


def fig_ot():
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    left, right = 0.4, 5.0
    sequence_chart(
        ax,
        [(left, "送信者 $S$\n$m_0, m_1$"), (right, "受信者 $R$\n選択ビット $b$")],
        top=3.3,
        bottom=-2.6,
        colw=2.2,
    )

    note(
        ax,
        right,
        2.35,
        4.0,
        "① 鍵ペア $(sk, pk_b)$ を作り、\n$pk_{1-b}$ は秘密鍵を知らずに選ぶ",
        h=0.72,
    )
    arrow(ax, (right, 1.50), (left, 1.50), color=BLUE, label="$pk_0,\\; pk_1$", dy=0.12)
    note(
        ax,
        left,
        0.72,
        4.0,
        "② $c_0 = \\mathrm{Enc}_{pk_0}(m_0)$\n   $c_1 = \\mathrm{Enc}_{pk_1}(m_1)$",
        h=0.72,
    )
    arrow(ax, (left, -0.08), (right, -0.08), color=ORANGE, label="$c_0,\\; c_1$", dy=0.12)
    note(
        ax,
        right,
        -0.88,
        4.0,
        "③ $m_b = \\mathrm{Dec}_{sk}(c_b)$\n   $m_{1-b}$ は復号できない",
        h=0.72,
        fc="#f0fdf4",
        ec=GREEN,
        color=GREEN,
    )
    note(
        ax,
        (left + right) / 2,
        -2.00,
        7.4,
        "$S$ は $b$ を知らない ($pk_0$ と $pk_1$ が区別できない)\n"
        "$R$ は $m_{1-b}$ を知らない (対応する秘密鍵を持たない)",
        fc="white",
        ec=FAINT,
        color=MUTED,
        h=0.84,
        fontsize=9.5,
    )

    bare(ax, (-1.6, 7.0), (-2.7, 4.0), "1-out-of-2 紛失通信 (OT)", equal=False)
    save(fig, "mpc-ot.svg")


# --------------------------------------------- figure 8: Garbled Circuit


def fig_garbled():
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.4), width_ratios=[1.0, 0.95, 1.5])

    # --- 左: AND ゲートとワイヤラベル
    ax = axes[0]
    box(ax, (1.15, 0.5), 0.9, 0.6, "AND", fc="#f3f4f6", ec=INK, fontsize=10.5)
    arrow(ax, (0.05, 0.95), (0.68, 0.68), shrink=2, lw=1.1)
    arrow(ax, (0.05, 0.05), (0.68, 0.32), shrink=2, lw=1.1)
    arrow(ax, (1.62, 0.5), (2.25, 0.5), shrink=2, lw=1.1)
    ax.text(-0.02, 1.02, "$a$", fontsize=11, ha="right", va="center")
    ax.text(-0.02, -0.02, "$b$", fontsize=11, ha="right", va="center")
    ax.text(2.32, 0.5, "$c$", fontsize=11, ha="left", va="center")
    ax.text(
        1.15,
        -0.62,
        "各ワイヤに\n$0$ 用・$1$ 用の鍵を割り当てる\n$(k_a^0, k_a^1)$, $(k_b^0, k_b^1)$, $(k_c^0, k_c^1)$",
        fontsize=9,
        color=MUTED,
        ha="center",
        va="center",
        linespacing=1.6,
    )
    bare(ax, (-0.5, 2.6), (-1.25, 1.45), "回路のゲート", equal=False)

    # --- 中央: 真理値表
    rows = [("0", "0", "0"), ("0", "1", "0"), ("1", "0", "0"), ("1", "1", "1")]
    ax = axes[1]
    for j, head in enumerate(("$a$", "$b$", "$c$")):
        ax.text(j, 4.35, head, fontsize=10.5, ha="center", va="center", color=MUTED)
    for i, row in enumerate(rows):
        y = 3.5 - i
        ax.add_patch(
            Rectangle(
                (-0.5, y - 0.42),
                3.0,
                0.84,
                facecolor="#f9fafb" if i % 2 else "white",
                edgecolor=FAINT,
                lw=0.8,
            )
        )
        for j, v in enumerate(row):
            ax.text(
                j,
                y,
                v,
                fontsize=10.5,
                ha="center",
                va="center",
                color=BLUE if j < 2 else INK,
            )
    bare(ax, (-0.7, 2.7), (-1.25, 4.9), "真理値表", equal=False)

    # --- 右: garbled table
    garbled = [
        "$\\mathrm{Enc}_{k_a^1,\\, k_b^0}(k_c^0)$",
        "$\\mathrm{Enc}_{k_a^1,\\, k_b^1}(k_c^1)$",
        "$\\mathrm{Enc}_{k_a^0,\\, k_b^0}(k_c^0)$",
        "$\\mathrm{Enc}_{k_a^0,\\, k_b^1}(k_c^0)$",
    ]
    ax = axes[2]
    for i, cell in enumerate(garbled):
        y = 3.5 - i
        ax.add_patch(
            Rectangle(
                (-1.05, y - 0.42),
                2.1,
                0.84,
                facecolor="#fff7ed",
                edgecolor=ORANGE,
                lw=0.9,
            )
        )
        ax.text(0, y, cell, fontsize=9.5, ha="center", va="center", color=INK)
    ax.text(
        0,
        -0.62,
        "行はシャッフル済み\n評価者は自分が持つ 2 つの鍵で\n復号できる 1 行だけを開ける",
        fontsize=9,
        color=MUTED,
        ha="center",
        va="center",
        linespacing=1.6,
    )
    bare(ax, (-1.3, 1.3), (-1.25, 4.9), "garbled table", equal=False)

    save(fig, "mpc-garbled-circuit.svg")


# ------------------------------------------------ figure 9: FHE のノイズ


def fig_fhe_noise():
    limit = 1e6
    base, growth = 1.0, 3.1
    depth = np.arange(0, 21)
    plain = base * growth**depth

    boot_level, trigger = 20.0, limit / growth**2
    noise, cur, boots = [], base, []
    for d in depth:
        if cur > trigger:
            cur = boot_level
            boots.append(d)
        noise.append(cur)
        cur *= growth
    noise = np.array(noise)

    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.axhspan(limit, 1e11, color="#fef2f2", zorder=0)
    ax.axhline(limit, color=RED, lw=1.3, ls="--", zorder=2)
    ax.text(20.2, limit * 1.7, "復号可能な上限", color=RED, fontsize=9.5, ha="right")

    ax.plot(depth, plain, color=ORANGE, lw=2.0, marker="o", ms=3.5, label="そのまま計算")
    ax.plot(
        depth, noise, color=BLUE, lw=2.0, marker="o", ms=3.5, label="bootstrapping あり"
    )
    for d in boots:
        ax.annotate(
            "bootstrap",
            xy=(d, noise[d]),
            xytext=(0, -34),
            textcoords="offset points",
            fontsize=8.5,
            color=BLUE,
            ha="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9),
        )
    cross = int(np.argmax(plain > limit))
    ax.annotate(
        f"深さ {cross} で復号不能",
        xy=(cross, plain[cross]),
        xytext=(-12, 26),
        textcoords="offset points",
        fontsize=9.5,
        color=ORANGE,
        ha="right",
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9),
    )

    ax.set_yscale("log")
    ax.set_xlim(-0.5, 20.5)
    ax.set_ylim(1, 1e11)
    ax.set_xticks(range(0, 21, 2))
    ax.set_xlabel("乗算の深さ")
    ax.set_ylabel("暗号文に含まれるノイズ (対数)")
    ax.set_title("準同型演算はノイズを増やす")
    ax.legend(loc="upper left")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    save(fig, "mpc-fhe-noise.svg")


# ------------------------------------------------- figure 10: 実測ベンチ


def is_probable_prime(n, rounds=24, rng=None):
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    rng = rng or random.Random(0)
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def gen_prime(bits, rng):
    while True:
        cand = rng.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(cand, rng=rng):
            return cand


class Paillier:
    """教科書どおりの Paillier 暗号 (g = n + 1 の簡略版)。"""

    def __init__(self, bits, rng):
        half = bits // 2
        p = gen_prime(half, rng)
        q = gen_prime(half, rng)
        while q == p:
            q = gen_prime(half, rng)
        self.n = p * q
        self.n2 = self.n * self.n
        lam = (p - 1) * (q - 1) // math.gcd(p - 1, q - 1)
        self.lam = lam
        self.mu = pow((pow(self.n + 1, lam, self.n2) - 1) // self.n, -1, self.n)
        self.rng = rng

    def encrypt(self, m):
        r = self.rng.randrange(1, self.n)
        return (1 + m * self.n) % self.n2 * pow(r, self.n, self.n2) % self.n2

    def add(self, c1, c2):
        return c1 * c2 % self.n2

    def decrypt(self, c):
        return (pow(c, self.lam, self.n2) - 1) // self.n * self.mu % self.n


def bench(fn, seconds=0.35):
    """1 回あたりの所要時間 (マイクロ秒) を返す。"""
    n = 1
    while True:
        t0 = time.perf_counter()
        for _ in range(n):
            fn()
        dt = time.perf_counter() - t0
        if dt > seconds:
            return dt / n * 1e6
        n = max(n * 2, int(n * seconds / max(dt, 1e-9)) + 1)


def fig_benchmark():
    rng = random.Random(20240917)
    p61 = (1 << 61) - 1

    # --- 加法的秘密分散 (3 者、Z_p 上)
    def share(secret=12345):
        s1 = rng.getrandbits(61) % p61
        s2 = rng.getrandbits(61) % p61
        return s1, s2, (secret - s1 - s2) % p61

    sh_a, sh_b = share(3), share(4)

    results = {}
    results["秘密分散\n$\\mathbb{Z}_p$, $p = 2^{61}-1$"] = {
        "分散 / 暗号化": bench(lambda: share(3)),
        "加算": bench(lambda: tuple((x + y) % p61 for x, y in zip(sh_a, sh_b))),
        "復元 / 復号": bench(lambda: sum(sh_a) % p61),
    }

    for bits in (1024, 2048):
        pai = Paillier(bits, rng)
        c1, c2 = pai.encrypt(3), pai.encrypt(4)
        assert pai.decrypt(pai.add(c1, c2)) == 7  # 暗号文の積 = 平文の和
        assert pai.decrypt(pow(c1, 5, pai.n2)) == 15  # 暗号文のべき = 平文の定数倍
        results[f"Paillier\n{bits} bit"] = {
            "分散 / 暗号化": bench(lambda: pai.encrypt(3)),
            "加算": bench(lambda: pai.add(c1, c2)),
            "復元 / 復号": bench(lambda: pai.decrypt(c1)),
        }
        print(f"Paillier {bits} bit: 暗号文 {2 * bits // 8} B")

    for label, ops_ in results.items():
        print(
            label.replace("\n", " "),
            {k: round(v, 3) for k, v in ops_.items()},
        )

    labels = list(results)
    ops = ["分散 / 暗号化", "加算", "復元 / 復号"]
    colors = [BLUE, GREEN, ORANGE]
    x = np.arange(len(labels))
    width = 0.26

    fig, ax = plt.subplots(figsize=(7.8, 4.4))
    for i, (op, color) in enumerate(zip(ops, colors)):
        vals = [results[l][op] for l in labels]
        bars = ax.bar(x + (i - 1) * width, vals, width, color=color, label=op)
        for rect, v in zip(bars, vals):
            ax.text(
                rect.get_x() + rect.get_width() / 2,
                v * 1.25,
                f"{v:,.2f}" if v < 10 else f"{v:,.0f}",
                fontsize=8,
                ha="center",
                color=MUTED,
            )
    ax.set_yscale("log")
    ax.set_xticks(x, labels, fontsize=10)
    ax.set_ylabel("1 回あたりの時間 [$\\mu$s] (対数)")
    ax.set_title("秘密分散と準同型暗号のコスト (CPython 3.9 実測)")
    ax.set_ylim(bottom=min(min(r.values()) for r in results.values()) / 4)
    ax.legend(loc="upper left", ncol=3, fontsize=9.5)
    ax.grid(axis="y", color=FAINT, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xlabel(
        "1 個の値のサイズ: シェア 8 B / 暗号文 256 B (1024 bit) / 512 B (2048 bit)",
        fontsize=9.5,
        color=MUTED,
        labelpad=10,
    )

    save(fig, "mpc-benchmark.svg")


# ------------------------------------------------------ 本文コードの検証

P = (1 << 61) - 1


def shamir_share(secret, n, k, rng):
    coeffs = [secret] + [rng.randrange(P) for _ in range(k - 1)]
    out = []
    for i in range(1, n + 1):
        y, xp = 0, 1
        for c in coeffs:
            y = (y + c * xp) % P
            xp = xp * i % P
        out.append((i, y))
    return out


def shamir_reconstruct(shares):
    total = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = num * (-xj) % P
                den = den * (xi - xj) % P
        total = (total + yi * num * pow(den, -1, P)) % P
    return total


def verify_snippets():
    rng = random.Random(1)

    # Shamir: k 個で復元でき、線形性が成り立つ
    s = 424242
    shares = shamir_share(s, n=5, k=3, rng=rng)
    assert shamir_reconstruct(shares[:3]) == s
    assert shamir_reconstruct(shares[1:4]) == s
    a, b = 111, 222
    sa, sb = shamir_share(a, 5, 3, rng), shamir_share(b, 5, 3, rng)
    summed = [(x, (ya + yb) % P) for (x, ya), (_, yb) in zip(sa, sb)]
    assert shamir_reconstruct(summed[:3]) == a + b

    # 次数が倍になるので、積は 2t + 1 = 5 点ないと復元できない
    prod = [(x, ya * yb % P) for (x, ya), (_, yb) in zip(sa, sb)]
    assert shamir_reconstruct(prod[:5]) == a * b
    assert shamir_reconstruct(prod[:3]) != a * b

    # Beaver triple による乗算
    x, y = 7, 9
    av, bv = rng.randrange(P), rng.randrange(P)
    cv = av * bv % P
    xs, ys = [rng.randrange(P) for _ in range(2)], [rng.randrange(P) for _ in range(2)]
    xs.append((x - sum(xs)) % P)
    ys.append((y - sum(ys)) % P)
    as_ = [rng.randrange(P) for _ in range(2)]
    as_.append((av - sum(as_)) % P)
    bs = [rng.randrange(P) for _ in range(2)]
    bs.append((bv - sum(bs)) % P)
    cs = [rng.randrange(P) for _ in range(2)]
    cs.append((cv - sum(cs)) % P)
    d = sum((xi - ai) % P for xi, ai in zip(xs, as_)) % P
    e = sum((yi - bi) % P for yi, bi in zip(ys, bs)) % P
    zs = [
        (ci + d * bi + e * ai + (d * e if i == 0 else 0)) % P
        for i, (ci, ai, bi) in enumerate(zip(cs, as_, bs))
    ]
    assert sum(zs) % P == x * y

    print("verified: Shamir / 線形性 / 次数の増加 / Beaver triple")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if PNG_DIR:
        Path(PNG_DIR).mkdir(parents=True, exist_ok=True)
    verify_snippets()
    fig_overview()
    fig_additive()
    fig_shamir()
    fig_shamir_security()
    fig_degree()
    fig_beaver()
    fig_ot()
    fig_garbled()
    fig_fhe_noise()
    fig_benchmark()
