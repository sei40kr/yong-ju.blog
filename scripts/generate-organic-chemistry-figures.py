"""content/posts/organic-chemistry.mdx の図を生成する。

出力先は public/img/oc-*.svg。
構造式は外部の化学ライブラリを使わず、線分と文字の配置としてここで組み立てる。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-organic-chemistry-figures.py

環境変数 OC_PNG_DIR を指定すると、目視確認用に同じ図を PNG でも書き出す。
"""

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"
PNG_DIR = os.environ.get("OC_PNG_DIR")

BLUE = "#2563eb"  # 電子豊富 (求核剤・負電荷)
ORANGE = "#ea580c"  # 電子不足 (求電子剤・正電荷)
GREEN = "#16a34a"
PURPLE = "#7c3aed"  # 巻矢印 (電子の流れ)
GRAY = "#6b7280"
LIGHT = "#cbd5e1"
INK = "#111827"

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
        "mathtext.fontset": "dejavusans",
    }
)


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05)
    if PNG_DIR:
        fig.savefig(
            Path(PNG_DIR) / name.replace(".svg", ".png"),
            format="png",
            bbox_inches="tight",
            pad_inches=0.05,
            dpi=110,
        )
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


# ------------------------------------------------------------ 描画ヘルパ


def canvas(ax, xlim, ylim, title=None):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title)


def bond(ax, p, q, order=1, color=INK, lw=1.7, trim=(0.0, 0.0), gap=0.08, ls="solid"):
    """p-q 間に結合線を引く。trim は両端を縮める量 (原子ラベルとの隙間)。"""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    d = q - p
    length = float(np.hypot(*d))
    u = d / length
    n = np.array([-u[1], u[0]])
    a = p + u * trim[0]
    b = q - u * trim[1]
    if order == 1:
        offsets = [0.0]
    elif order == 2:
        offsets = [gap, -gap]
    else:
        offsets = [0.0, 1.15 * gap, -1.15 * gap]
    for off in offsets:
        ax.plot(
            [a[0] + n[0] * off, b[0] + n[0] * off],
            [a[1] + n[1] * off, b[1] + n[1] * off],
            color=color,
            lw=lw,
            ls=ls,
            solid_capstyle="round",
            zorder=1,
        )


def partial_bond(ax, p, q, side=1, offset=0.1, color=GRAY, lw=1.3, trim=(0.0, 0.0)):
    """部分二重結合を表す破線 (実線の隣に 1 本だけ引く)。"""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    u = (q - p) / np.hypot(*(q - p))
    n = np.array([-u[1], u[0]]) * offset * side
    a = p + u * trim[0] + n
    b = q - u * trim[1] + n
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, ls=(0, (2, 2)), zorder=1)


def bracket(ax, x, y0, y1, color=GRAY, lw=1.3, tick=0.16, side=1):
    """遷移状態を囲む角かっこ。side=1 で左、-1 で右。"""
    ax.plot([x, x], [y0, y1], color=color, lw=lw, zorder=2)
    for y in (y0, y1):
        ax.plot([x, x + tick * side], [y, y], color=color, lw=lw, zorder=2)


def inner_line(ax, p, q, center, offset=0.16, shrink=0.18, color=INK, lw=1.7):
    """環の内側に平行線を 1 本引く (環内の二重結合)。"""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    c = np.asarray(center, float)
    mid = (p + q) / 2
    d = c - mid
    d = d / np.hypot(*d)
    a = p + (q - p) * shrink + d * offset
    b = q - (q - p) * shrink + d * offset
    ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=1)


def wedge(ax, p, q, color=INK, width=0.13, trim=(0.0, 0.0)):
    """手前に出る結合 (くさび)。"""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    u = (q - p) / np.hypot(*(q - p))
    n = np.array([-u[1], u[0]])
    a = p + u * trim[0]
    b = q - u * trim[1]
    ax.add_patch(
        Polygon([a, b + n * width, b - n * width], closed=True, fc=color, ec="none", zorder=1)
    )


def hashed(ax, p, q, color=INK, width=0.13, n_dash=6, lw=1.5, trim=(0.0, 0.0)):
    """奥に引っ込む結合 (破線くさび)。"""
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    u = (q - p) / np.hypot(*(q - p))
    n = np.array([-u[1], u[0]])
    a = p + u * trim[0]
    b = q - u * trim[1]
    for i in range(n_dash):
        t = (i + 1) / n_dash
        c = a + (b - a) * t
        w = width * t
        ax.plot(
            [c[0] - n[0] * w, c[0] + n[0] * w],
            [c[1] - n[1] * w, c[1] + n[1] * w],
            color=color,
            lw=lw,
            zorder=1,
        )


def atom(ax, p, text, color=INK, size=11, pad=0.16, bg="white", weight=None, zorder=3):
    ax.text(
        p[0],
        p[1],
        text,
        ha="center",
        va="center",
        fontsize=size,
        color=color,
        weight=weight,
        zorder=zorder,
        bbox=dict(boxstyle=f"round,pad={pad}", fc=bg, ec="none"),
    )


def note(ax, p, text, color=GRAY, size=9.5, ha="center", va="center", **kw):
    ax.text(p[0], p[1], text, ha=ha, va=va, fontsize=size, color=color, zorder=4, **kw)


def heading(ax, x, y, text, size=11.5):
    ax.text(x, y, text, ha="center", va="center", fontsize=size, color=INK, zorder=4)


def curly(ax, p, q, rad=0.35, color=PURPLE, lw=1.5, shrink=4, scale=11):
    """巻矢印 (電子対の移動)。"""
    ax.add_patch(
        FancyArrowPatch(
            p,
            q,
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>",
            mutation_scale=scale,
            color=color,
            lw=lw,
            shrinkA=shrink,
            shrinkB=shrink,
            zorder=5,
        )
    )


def reaction_arrow(ax, p, q, label=None, color=INK, lw=1.4, sub=None):
    ax.add_patch(
        FancyArrowPatch(
            p,
            q,
            arrowstyle="-|>",
            mutation_scale=13,
            color=color,
            lw=lw,
            shrinkA=0,
            shrinkB=0,
            zorder=2,
        )
    )
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    if label:
        note(ax, (mx, my + 0.2), label, color=GRAY, va="bottom")
    if sub:
        note(ax, (mx, my - 0.2), sub, color=GRAY, va="top")


def lone_pair(ax, p, angle_deg, color=BLUE, r=0.34, sep=0.09, size=3.2):
    """孤立電子対を 2 つの点で表す。"""
    th = np.deg2rad(angle_deg)
    c = np.array(p, float) + r * np.array([np.cos(th), np.sin(th)])
    n = np.array([-np.sin(th), np.cos(th)])
    for s in (+1, -1):
        ax.plot(*(c + n * sep * s), marker="o", ms=size, color=color, zorder=4)


def smooth_profile(points, n=160):
    """極小・極大を交互に指定してなめらかなエネルギー曲線を作る。"""
    xs, ys = [], []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        t = np.linspace(0, 1, n)
        s = 0.5 - 0.5 * np.cos(np.pi * t)
        xs.append(x0 + (x1 - x0) * t)
        ys.append(y0 + (y1 - y0) * s)
    return np.concatenate(xs), np.concatenate(ys)


def energy_axes(ax, xmax, ymax, ylabel="エネルギー"):
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("反応座標")
    ax.set_ylabel(ylabel)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def zigzag(start, n, dx=0.87, dy=0.5, up_first=True):
    pts = [np.array(start, float)]
    for i in range(n):
        step = dy if ((i % 2 == 0) == up_first) else -dy
        pts.append(pts[-1] + np.array([dx, step]))
    return pts


def ring(center, r=0.62, n=6, rot=90):
    c = np.array(center, float)
    return [
        c
        + r
        * np.array(
            [np.cos(np.deg2rad(rot + 360 * i / n)), np.sin(np.deg2rad(rot + 360 * i / n))]
        )
        for i in range(n)
    ]


def benzene(ax, center, r=0.62, rot=90, aromatic_circle=True, color=INK, lw=1.7):
    pts = ring(center, r=r, n=6, rot=rot)
    for i in range(6):
        bond(ax, pts[i], pts[(i + 1) % 6], color=color, lw=lw)
    if aromatic_circle:
        ax.add_patch(Circle(center, r * 0.58, fill=False, ec=color, lw=lw))
    return pts


# ------------------------------------------------------------------ 図 1


def fig_skeletal():
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.0))

    ax = axes[0]
    canvas(ax, (-1.6, 4.6), (-1.6, 2.0), "① ルイス構造式")
    cs = [np.array([x, 0.0]) for x in (0, 1, 2, 3)]
    for a, b in zip(cs, cs[1:]):
        bond(ax, a, b, trim=(0.22, 0.22))
    hs = [
        (cs[0], (-0.8, 0.0)),
        (cs[0], (0.0, 0.8)),
        (cs[0], (0.0, -0.8)),
        (cs[1], (1.0, -0.8)),
        (cs[2], (2.0, 0.8)),
        (cs[2], (2.0, -0.8)),
        (cs[3], (3.8, 0.0)),
        (cs[3], (3.0, 0.8)),
        (cs[3], (3.0, -0.8)),
    ]
    for c, h in hs:
        bond(ax, c, h, trim=(0.22, 0.18), color=GRAY, lw=1.3)
        atom(ax, h, "H", color=GRAY, size=10)
    o = np.array([1.0, 0.9])
    ho = np.array([1.75, 1.35])
    bond(ax, cs[1], o, trim=(0.22, 0.2))
    bond(ax, o, ho, trim=(0.2, 0.18), color=GRAY, lw=1.3)
    atom(ax, o, "O", color=BLUE, weight="bold")
    atom(ax, ho, "H", color=GRAY, size=10)
    for c in cs:
        atom(ax, c, "C", weight="bold")

    ax = axes[1]
    canvas(ax, (-3.1, 3.1), (-1.6, 2.0), "② 凝縮構造式")
    ax.text(0.0, 0.4, r"CH$_3$CH(OH)CH$_2$CH$_3$", ha="center", va="center", fontsize=15)
    note(ax, (0.0, -0.6), "結合線を省いて 1 行で書く")

    ax = axes[2]
    canvas(ax, (-1.0, 3.66), (-1.0, 1.7), "③ 骨格構造式")
    pts = zigzag((0, 0), 3)
    for a, b in zip(pts, pts[1:]):
        bond(ax, a, b)
    oh = pts[1] + np.array([0.0, 0.85])
    bond(ax, pts[1], oh, trim=(0.0, 0.22))
    atom(ax, oh, "OH", color=BLUE, weight="bold")
    ax.plot(*pts[2], marker="o", ms=5, color=ORANGE, zorder=4)
    note(ax, (1.9, -0.6), "頂点 = 炭素\n(水素は自動的に補う)", color=ORANGE, size=9)
    ax.plot(*pts[0], marker="o", ms=5, color=GREEN, zorder=4)
    note(ax, (-0.45, 0.5), "端 = CH$_3$", color=GREEN, size=9)

    fig.suptitle("同じ分子 (ブタン-2-オール) の 3 つの書き方", y=1.07, fontsize=12)
    save(fig, "oc-skeletal.svg")


# ------------------------------------------------------------------ 図 2


def fig_hybridization():
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2))
    for ax in axes:
        canvas(ax, (-2.2, 2.2), (-1.6, 1.8))

    ax = axes[0]
    ax.set_title("sp$^3$ (メタン)")
    c = np.array([0.0, 0.0])
    up = np.array([0.0, 1.05])
    left = np.array([-1.0, -0.55])
    front = np.array([0.75, -0.5])
    back = np.array([0.62, 0.7])
    bond(ax, c, up, trim=(0.2, 0.18))
    bond(ax, c, left, trim=(0.2, 0.18))
    wedge(ax, c, front, trim=(0.2, 0.18))
    hashed(ax, c, back, trim=(0.2, 0.18))
    atom(ax, c, "C", weight="bold")
    for p in (up, left, front, back):
        atom(ax, p, "H", color=GRAY, size=10)
    note(ax, (0.0, -1.15), "正四面体 / 結合角 109.5°\nσ 結合のみ・単結合まわりは自由回転", size=9)

    ax = axes[1]
    ax.set_title("sp$^2$ (エチレン)")
    c1 = np.array([-0.5, 0.0])
    c2 = np.array([0.5, 0.0])
    bond(ax, c1, c2, order=2, trim=(0.2, 0.2))
    for c, sx in ((c1, -1), (c2, 1)):
        for sy in (1, -1):
            h = c + np.array([sx * 0.75, sy * 0.65])
            bond(ax, c, h, trim=(0.2, 0.18), color=GRAY, lw=1.3)
            atom(ax, h, "H", color=GRAY, size=10)
    for c in (c1, c2):
        atom(ax, c, "C", weight="bold")
        for sy in (1, -1):
            ax.add_patch(
                Ellipse(
                    (c[0], c[1] + sy * 0.42),
                    0.42,
                    0.62,
                    fc=BLUE,
                    ec="none",
                    alpha=0.16,
                    zorder=0,
                )
            )
    note(ax, (0.0, 0.92), "π 結合", color=BLUE, size=9)
    note(ax, (0.0, -1.15), "平面 / 結合角 120°\nπ 結合があるので二重結合は回れない", size=9)

    ax = axes[2]
    ax.set_title("sp (アセチレン)")
    c1 = np.array([-0.55, 0.0])
    c2 = np.array([0.55, 0.0])
    h1 = np.array([-1.6, 0.0])
    h2 = np.array([1.6, 0.0])
    bond(ax, c1, c2, order=3, trim=(0.2, 0.2), gap=0.1)
    bond(ax, c1, h1, trim=(0.2, 0.18), color=GRAY, lw=1.3)
    bond(ax, c2, h2, trim=(0.2, 0.18), color=GRAY, lw=1.3)
    atom(ax, c1, "C", weight="bold")
    atom(ax, c2, "C", weight="bold")
    atom(ax, h1, "H", color=GRAY, size=10)
    atom(ax, h2, "H", color=GRAY, size=10)
    note(ax, (0.0, 0.92), "π 結合 2 本", color=BLUE, size=9)
    note(ax, (0.0, -1.15), "直線 / 結合角 180°\ns 性が高く、C–H の酸性度も高い", size=9)

    fig.suptitle("混成軌道が分子の形を決める", y=1.05, fontsize=12)
    save(fig, "oc-hybridization.svg")


# ------------------------------------------------------------------ 図 3


def fig_induction():
    fig = plt.figure(figsize=(9.8, 3.0))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.15, 1, 1], wspace=0.35)

    ax = fig.add_subplot(gs[0])
    canvas(ax, (-0.5, 3.6), (-1.6, 1.9), "結合の分極")
    pts = [np.array([0.0, 0.0]), np.array([0.8, 0.46]), np.array([1.6, 0.0])]
    cl = pts[2] + np.array([0.8, 0.46])
    for a, b in zip(pts, pts[1:]):
        bond(ax, a, b)
    bond(ax, pts[2], cl, trim=(0.0, 0.22))
    atom(ax, cl, "Cl", color=BLUE, weight="bold")
    note(ax, (2.9, 0.06), "δ−", color=BLUE, size=11)
    for i, p in enumerate(pts):
        note(ax, (p[0], p[1] - 0.4), ["δ+++", "δ++", "δ+"][2 - i], color=ORANGE, size=9)
    ax.add_patch(
        FancyArrowPatch(
            (0.2, -0.85),
            (2.2, -0.85),
            arrowstyle="-|>",
            mutation_scale=12,
            color=ORANGE,
            lw=1.4,
        )
    )
    note(ax, (1.3, -1.25), "電子は Cl に引かれ、その影響は\n結合を離れるほど急速に薄れる", size=9)

    ax = fig.add_subplot(gs[1])
    labels = ["CH$_3$", "ClCH$_2$", "Cl$_2$CH", "Cl$_3$C"]
    values = [4.76, 2.86, 1.29, 0.65]
    ax.bar(labels, values, color=[LIGHT, BLUE, BLUE, BLUE], width=0.62)
    for i, v in enumerate(values):
        ax.text(i, v + 0.12, f"{v:.2f}", ha="center", fontsize=9, color=INK)
    ax.set_title("Cl の数と酸性度")
    ax.set_ylabel("p$K_a$ (–COOH)")
    ax.set_ylim(0, 5.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=9)

    ax = fig.add_subplot(gs[2])
    labels = ["2 位", "3 位", "4 位", "なし"]
    values = [2.86, 4.05, 4.52, 4.82]
    ax.bar(labels, values, color=[GREEN, GREEN, GREEN, LIGHT], width=0.62)
    for i, v in enumerate(values):
        ax.text(i, v + 0.12, f"{v:.2f}", ha="center", fontsize=9, color=INK)
    ax.set_title("Cl の位置と酸性度 (ブタン酸)")
    ax.set_ylabel("p$K_a$")
    ax.set_ylim(0, 5.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=9)

    fig.suptitle(
        "誘起効果: 電気陰性な原子が電子を引き、その影響は距離とともに減衰する", y=1.06, fontsize=12
    )
    save(fig, "oc-induction.svg")


# ------------------------------------------------------------------ 図 4


def fig_resonance():
    fig, ax = plt.subplots(figsize=(9.6, 3.0))
    canvas(ax, (-0.9, 10.8), (-1.5, 2.1))

    def acetate(x0, flip=False, arrows=False):
        me = np.array([x0, 0.0])
        c = me + np.array([0.87, 0.5])
        o_dbl = c + np.array([0.87, -0.5])
        o_neg = c + np.array([0.0, 1.0])
        if flip:
            o_dbl, o_neg = o_neg, o_dbl
        bond(ax, me, c)
        bond(ax, c, o_dbl, order=2, trim=(0.0, 0.26))
        bond(ax, c, o_neg, trim=(0.0, 0.26))
        atom(ax, o_dbl, "O", color=BLUE, weight="bold")
        atom(ax, o_neg, "O$^-$", color=BLUE, weight="bold")
        if arrows:
            mid = (c + o_dbl) / 2 + np.array([0.18, 0.18])
            curly(ax, mid, o_dbl + np.array([0.34, 0.3]), rad=-0.5)
            curly(
                ax,
                o_neg + np.array([-0.34, 0.12]),
                (c + o_neg) / 2 + np.array([-0.22, 0.05]),
                rad=-0.5,
            )

    acetate(0.0, arrows=True)
    ax.text(2.6, 0.6, r"$\longleftrightarrow$", ha="center", va="center", fontsize=15)
    acetate(3.2, flip=True)
    note(ax, (6.0, 0.6), "実際は", size=10)

    me = np.array([6.8, 0.0])
    c = me + np.array([0.87, 0.5])
    o1 = c + np.array([0.87, -0.5])
    o2 = c + np.array([0.0, 1.0])
    bond(ax, me, c)
    for o, side in ((o1, -1), (o2, 1)):
        bond(ax, c, o, trim=(0.0, 0.26))
        partial_bond(ax, c, o, side=side, trim=(0.16, 0.34))
        atom(ax, o, "O", color=BLUE, weight="bold")
    note(ax, o2 + np.array([0.75, 0.05]), "δ− = −1/2", color=BLUE, size=9, ha="left")
    note(ax, o1 + np.array([0.4, -0.35]), "δ− = −1/2", color=BLUE, size=9, ha="left")
    note(
        ax,
        (8.0, -1.0),
        "2 本の C–O は完全に等価 (どちらも 1.5 重結合)\n負電荷は 2 つの O に半分ずつ",
        size=9,
    )
    note(
        ax,
        (1.6, -1.0),
        "これは「行ったり来たり」ではなく\n「重ね合わせ」を 2 枚で表現しているだけ",
        size=9,
    )

    fig.suptitle("共鳴: 酢酸イオンの負電荷は非局在化している", y=1.04, fontsize=12)
    save(fig, "oc-resonance.svg")


# ------------------------------------------------------------------ 図 5


def fig_pka():
    fig, ax = plt.subplots(figsize=(9.8, 3.6))
    ax.set_xlim(-12, 54)
    ax.set_ylim(-2.0, 1.9)
    ax.axhline(0, color=INK, lw=1.4)
    ax.set_yticks([])
    ax.set_xticks([-10, 0, 10, 20, 30, 40, 50])
    ax.set_xlabel("p$K_a$")
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", length=0, labelsize=10)

    items = [
        (-7, "HCl", 1),
        (-1.7, "H$_3$O$^+$", -1),
        (4.8, "RCOOH", 1),
        (9.2, "NH$_4^+$", -1),
        (10.0, "PhOH", 2),
        (13, "マロン酸エステル", -2),
        (15.7, "H$_2$O", 1),
        (16, "ROH", -1),
        (19, "ケトンの α–H", 2),
        (25, "エステルの α–H", 1),
        (25, "末端アルキン", -1),
        (38, "NH$_3$", -1),
        (50, "アルカン", 1),
    ]
    for x, label, level in items:
        y = 0.42 * level
        color = BLUE if x >= 15 else (ORANGE if x <= 5 else GREEN)
        ax.plot([x, x], [0, y * 0.8], color=color, lw=1.2)
        ax.plot(x, 0, marker="o", ms=5, color=color, zorder=3)
        ax.text(
            x,
            y * 0.92,
            label,
            ha="center",
            va="bottom" if level > 0 else "top",
            fontsize=9,
            color=INK,
        )
    ax.text(-11, -1.45, "強い酸 / 共役塩基は弱い", ha="left", fontsize=9.5, color=ORANGE)
    ax.text(53, -1.45, "弱い酸 / 共役塩基は強い", ha="right", fontsize=9.5, color=BLUE)
    ax.add_patch(
        FancyArrowPatch(
            (-11, -1.72),
            (53, -1.72),
            arrowstyle="<|-|>",
            mutation_scale=11,
            color=GRAY,
            lw=1.1,
        )
    )
    ax.set_title("p$K_a$ ものさし: 反応は「強い酸 → 弱い酸」の向きに進む")
    save(fig, "oc-pka.svg")


# ------------------------------------------------------------------ 図 6


def fig_arrows():
    fig, axes = plt.subplots(1, 3, figsize=(9.8, 3.0))
    for ax in axes:
        canvas(ax, (-1.8, 2.8), (-1.7, 1.6))

    ax = axes[0]
    ax.set_title("① 孤立電子対から")
    o = np.array([-1.05, -0.3])
    c = np.array([0.55, -0.3])
    br = np.array([2.1, -0.3])
    atom(ax, o, "HO$^-$", color=BLUE, weight="bold")
    atom(ax, c, "C", weight="bold")
    atom(ax, br, "Br", color=ORANGE, weight="bold")
    bond(ax, c, br, trim=(0.24, 0.28))
    bond(ax, c, np.array([0.55, 0.6]), trim=(0.24, 0.0), color=GRAY, lw=1.2)
    bond(ax, c, np.array([0.2, -1.1]), trim=(0.24, 0.0), color=GRAY, lw=1.2)
    lone_pair(ax, o, 55)
    curly(ax, o + np.array([0.2, 0.42]), c + np.array([-0.3, 0.28]), rad=-0.45)
    curly(ax, (c + br) / 2 + np.array([0.0, 0.2]), br + np.array([0.0, 0.5]), rad=-0.45)
    note(ax, (0.5, 1.25), "電子を持っている方が攻める", size=9)
    note(ax, (0.5, -1.5), "求核剤 → 求電子剤 / 結合 → 脱離基", size=9)

    ax = axes[1]
    ax.set_title("② π 結合から")
    c1 = np.array([-1.1, 0.15])
    c2 = np.array([-0.1, 0.15])
    bond(ax, c1, c2, order=2)
    bond(ax, c1, c1 + np.array([-0.7, -0.55]), color=GRAY, lw=1.2)
    bond(ax, c2, c2 + np.array([0.7, -0.55]), color=GRAY, lw=1.2)
    h = np.array([1.1, 0.95])
    brm = np.array([1.95, 0.95])
    atom(ax, h, "H", color=ORANGE, weight="bold")
    atom(ax, brm, "Br", color=BLUE, weight="bold")
    bond(ax, h, brm, trim=(0.2, 0.24))
    curly(ax, (c1 + c2) / 2 + np.array([0.0, 0.28]), h + np.array([-0.22, 0.1]), rad=-0.4)
    curly(ax, (h + brm) / 2 + np.array([0.0, 0.22]), brm + np.array([0.3, 0.3]), rad=-0.5)
    note(ax, (0.2, -1.5), "π 電子は「電子の溜まり場」\n= 求核剤としてはたらく", size=9)

    ax = axes[2]
    ax.set_title("③ やってはいけない書き方")
    c = np.array([0.2, 0.3])
    nu = np.array([-1.0, 0.3])
    atom(ax, c, "C", weight="bold")
    atom(ax, nu, "Nu$^-$", color=BLUE, weight="bold")
    for ang in (45, 135, 225, 315):
        th = np.deg2rad(ang)
        bond(
            ax, c, c + 0.72 * np.array([np.cos(th), np.sin(th)]), trim=(0.24, 0.0), color=GRAY, lw=1.2
        )
    curly(ax, nu + np.array([0.3, 0.15]), c + np.array([-0.3, 0.16]), rad=-0.4, color=ORANGE)
    ax.text(0.95, 0.95, "×", color=ORANGE, fontsize=22, ha="center", va="center", weight="bold")
    note(ax, (0.4, -1.5), "炭素に 5 本目の結合は作れない。\n結合を作るなら、必ず何かが外れる", size=9)

    fig.suptitle("巻矢印の文法: 尾は電子のある場所、先は電子の行き先", y=1.05, fontsize=12)
    save(fig, "oc-arrows.svg")


# ------------------------------------------------------------------ 図 7


def fig_carbocation():
    fig = plt.figure(figsize=(9.8, 3.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.75, 1], wspace=0.05)

    ax = fig.add_subplot(gs[0])
    canvas(ax, (-0.9, 10.6), (-1.8, 1.8))
    heading(ax, 4.8, 1.5, "カルボカチオンの安定性")
    names = ["メチル", "第一級 (1°)", "第二級 (2°)", "第三級 (3°)"]
    formulas = ["CH$_3^+$", "CH$_3$CH$_2^+$", "(CH$_3$)$_2$CH$^+$", "(CH$_3$)$_3$C$^+$"]
    for i, (n, f) in enumerate(zip(names, formulas)):
        x = 0.7 + i * 2.7
        ax.text(x, 0.6, f, ha="center", va="center", fontsize=11.5, color=ORANGE)
        note(ax, (x, 0.05), n, size=9.5)
    ax.add_patch(
        FancyArrowPatch(
            (0.3, -0.6),
            (9.2, -0.6),
            arrowstyle="-|>",
            mutation_scale=13,
            color=ORANGE,
            lw=1.5,
        )
    )
    note(ax, (4.8, -1.0), "安定 (= 生成しやすい・反応が速い)", color=ORANGE, size=9.5)
    note(
        ax,
        (4.8, -1.5),
        "アリル $\\mathrm{CH_2{=}CH{-}CH_2^+}$ / ベンジル $\\mathrm{PhCH_2^+}$ は共鳴で 3° 並みに安定",
        size=9,
    )

    ax = fig.add_subplot(gs[1])
    canvas(ax, (-1.7, 1.7), (-1.8, 1.8))
    heading(ax, 0.0, 1.5, "超共役")
    c = np.array([0.15, 0.0])
    atom(ax, c, "C$^+$", color=ORANGE, weight="bold", size=13)
    for sy in (1, -1):
        ax.add_patch(
            Ellipse((c[0], c[1] + sy * 0.55), 0.5, 0.72, fc=ORANGE, ec="none", alpha=0.18, zorder=0)
        )
    note(ax, (0.15, 1.08), "空の p 軌道", color=ORANGE, size=9)
    cn = np.array([-0.95, -0.4])
    hn = cn + np.array([-0.15, 0.75])
    bond(ax, c, cn, trim=(0.3, 0.18))
    bond(ax, cn, hn, trim=(0.18, 0.16), color=BLUE)
    atom(ax, cn, "C", size=10)
    atom(ax, hn, "H", color=GRAY, size=10)
    curly(ax, (cn + hn) / 2 + np.array([0.24, 0.0]), np.array([-0.15, 0.45]), rad=-0.4)
    note(ax, (0.0, -1.25), "隣の C–H の電子が空の p 軌道に\n少しだけ流れ込んで正電荷を薄める", size=9)

    fig.suptitle("正電荷は「まわりに配れる」ほど安定になる", y=1.02, fontsize=12)
    save(fig, "oc-carbocation.svg")


# ------------------------------------------------------------------ 図 8


def fig_sn2():
    fig = plt.figure(figsize=(9.8, 3.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.9, 1], wspace=0.16)

    ax = fig.add_subplot(gs[0])
    canvas(ax, (-1.9, 11.0), (-2.1, 2.1))
    heading(ax, 4.6, 1.8, "背面攻撃と立体反転")

    c0 = np.array([0.0, 0.0])
    atom(ax, c0, "C", weight="bold")
    bond(ax, c0, c0 + np.array([0.0, 0.85]), trim=(0.24, 0.0), color=GRAY, lw=1.3)
    wedge(ax, c0, c0 + np.array([0.55, -0.7]), trim=(0.24, 0.0), color=GRAY)
    hashed(ax, c0, c0 + np.array([-0.3, -0.85]), trim=(0.24, 0.0), color=GRAY)
    br = c0 + np.array([1.15, 0.0])
    bond(ax, c0, br, trim=(0.24, 0.3))
    atom(ax, br, "Br", color=ORANGE, weight="bold")
    nu = c0 + np.array([-1.3, 0.0])
    atom(ax, nu, "HO$^-$", color=BLUE, weight="bold")
    curly(ax, nu + np.array([0.26, 0.3]), c0 + np.array([-0.44, 0.24]), rad=-0.4, shrink=2)
    curly(ax, (c0 + br) / 2 + np.array([0.0, 0.2]), br + np.array([0.1, 0.52]), rad=-0.45)
    note(ax, (-0.1, -1.5), "① 求核剤は脱離基の\n真裏から近づく", size=9)

    reaction_arrow(ax, (2.0, 0.0), (2.7, 0.0))

    bracket(ax, 3.15, -1.05, 1.05, side=1)
    bracket(ax, 6.35, -1.05, 1.05, side=-1)
    note(ax, (6.6, 1.15), "‡", size=12)
    ct = np.array([4.75, 0.0])
    atom(ax, ct, "C", weight="bold")
    bond(ax, ct, ct + np.array([0.0, 0.8]), trim=(0.24, 0.0), color=GRAY, lw=1.3)
    bond(ax, ct, ct + np.array([-0.45, -0.7]), trim=(0.24, 0.0), color=GRAY, lw=1.3)
    bond(ax, ct, ct + np.array([0.45, -0.7]), trim=(0.24, 0.0), color=GRAY, lw=1.3)
    bond(ax, ct, ct + np.array([-1.0, 0.0]), trim=(0.26, 0.24), ls=(0, (2, 2)), color=BLUE)
    bond(ax, ct, ct + np.array([1.0, 0.0]), trim=(0.26, 0.24), ls=(0, (2, 2)), color=ORANGE)
    atom(ax, ct + np.array([-1.35, 0.0]), "HO$^{\\delta-}$", color=BLUE, size=10)
    atom(ax, ct + np.array([1.35, 0.0]), "Br$^{\\delta-}$", color=ORANGE, size=10)
    note(ax, (4.75, -1.5), "② 遷移状態\n(中間体ではない)", size=9)

    reaction_arrow(ax, (6.9, 0.0), (7.6, 0.0))

    c2 = np.array([9.1, 0.0])
    atom(ax, c2, "C", weight="bold")
    bond(ax, c2, c2 + np.array([0.0, 0.85]), trim=(0.24, 0.0), color=GRAY, lw=1.3)
    wedge(ax, c2, c2 + np.array([-0.55, -0.7]), trim=(0.24, 0.0), color=GRAY)
    hashed(ax, c2, c2 + np.array([0.3, -0.85]), trim=(0.24, 0.0), color=GRAY)
    oh = c2 + np.array([-1.15, 0.0])
    bond(ax, c2, oh, trim=(0.24, 0.32))
    atom(ax, oh, "HO", color=BLUE, weight="bold")
    note(ax, (10.3, 0.45), "Br$^-$", color=ORANGE, size=10)
    note(ax, (9.3, -1.5), "③ 傘が裏返るように\n立体が反転する", size=9)

    ax = fig.add_subplot(gs[1])
    xs, ys = smooth_profile([(0.4, 1.0), (2.0, 3.5), (3.6, 0.4)])
    ax.plot(xs, ys, color=BLUE, lw=2)
    energy_axes(ax, 4.0, 4.6)
    ax.set_title("エネルギー図 (1 段階)")
    ax.text(0.03, 0.94, "速度 $=k[\\mathrm{RBr}][\\mathrm{HO^-}]$", transform=ax.transAxes, fontsize=9, color=BLUE)
    ax.text(0.45, 0.65, "R–Br + HO$^-$", fontsize=9, color=INK)
    ax.text(2.45, 0.05, "R–OH + Br$^-$", fontsize=9, color=INK)

    fig.suptitle("S$_N$2: 結合の生成と切断が同時に起こる", y=1.03, fontsize=12)
    save(fig, "oc-sn2.svg")


# ------------------------------------------------------------------ 図 9


def fig_sn1():
    fig = plt.figure(figsize=(9.8, 3.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.9, 1], wspace=0.16)

    ax = fig.add_subplot(gs[0])
    canvas(ax, (-1.7, 11.2), (-2.1, 2.1))
    heading(ax, 4.7, 1.8, "平面カルボカチオンを経由する")

    c0 = np.array([0.0, 0.0])
    atom(ax, c0, "C", weight="bold")
    bond(ax, c0, c0 + np.array([0.0, 0.85]), trim=(0.24, 0.0), color=GRAY, lw=1.3)
    wedge(ax, c0, c0 + np.array([-0.6, -0.6]), trim=(0.24, 0.0), color=GRAY)
    hashed(ax, c0, c0 + np.array([0.12, -0.85]), trim=(0.24, 0.0), color=GRAY)
    br = c0 + np.array([1.15, 0.0])
    bond(ax, c0, br, trim=(0.24, 0.3))
    atom(ax, br, "Br", color=ORANGE, weight="bold")
    curly(ax, (c0 + br) / 2 + np.array([0.0, 0.2]), br + np.array([0.1, 0.52]), rad=-0.45)
    note(ax, (0.1, -1.5), "① 脱離基が自分から外れる\n(遅い = 律速)", size=9)

    reaction_arrow(ax, (2.2, 0.0), (3.0, 0.0))

    cc = np.array([5.2, 0.0])
    atom(ax, cc, "C$^+$", color=ORANGE, weight="bold", size=13)
    for ang in (90, 210, 330):
        th = np.deg2rad(ang)
        bond(
            ax,
            cc,
            cc + 0.85 * np.array([np.cos(th), np.sin(th)]),
            trim=(0.32, 0.0),
            color=GRAY,
            lw=1.3,
        )
    atom(ax, cc + np.array([-1.7, 0.75]), "HO$^-$", color=BLUE, size=10)
    atom(ax, cc + np.array([1.7, 0.75]), "$^-$OH", color=BLUE, size=10)
    curly(ax, cc + np.array([-1.35, 0.55]), cc + np.array([-0.5, 0.18]), rad=-0.3)
    curly(ax, cc + np.array([1.35, 0.55]), cc + np.array([0.5, 0.18]), rad=0.3)
    note(ax, (5.2, -1.5), "② 平面なので\n上下どちらからも攻撃できる", size=9)

    reaction_arrow(ax, (7.6, 0.0), (8.4, 0.0))
    note(ax, (9.6, 0.45), "R 体", size=10, color=INK)
    note(ax, (9.6, -0.35), "S 体", size=10, color=INK)
    note(ax, (9.7, -1.5), "③ ほぼ 1:1\n(ラセミ化)", size=9)

    ax = fig.add_subplot(gs[1])
    xs, ys = smooth_profile([(0.3, 0.8), (1.5, 3.9), (2.3, 2.6), (3.1, 3.1), (3.9, 0.5)])
    ax.plot(xs, ys, color=ORANGE, lw=2)
    energy_axes(ax, 4.2, 5.0)
    ax.set_title("エネルギー図 (2 段階)")
    ax.text(0.03, 0.04, "速度 $=k[\\mathrm{RBr}]$", transform=ax.transAxes, fontsize=9, color=ORANGE)
    ax.annotate(
        "カルボカチオン中間体",
        xy=(2.3, 2.6),
        xytext=(1.5, 1.5),
        fontsize=9,
        color=GRAY,
        ha="left",
        arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8),
    )
    ax.annotate(
        "律速段階",
        xy=(1.5, 3.9),
        xytext=(0.9, 4.6),
        fontsize=9,
        color=ORANGE,
        ha="center",
        arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8),
    )

    fig.suptitle("S$_N$1: まず切れて、あとから結合する", y=1.03, fontsize=12)
    save(fig, "oc-sn1.svg")


# ------------------------------------------------------------------ 図 10


def fig_e2():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.4))

    ax = axes[0]
    canvas(ax, (-2.3, 2.7), (-2.0, 2.0), "アンチペリプラナー配置")
    c1 = np.array([-0.5, 0.0])
    c2 = np.array([0.5, 0.0])
    bond(ax, c1, c2, trim=(0.22, 0.22))
    atom(ax, c1, "C", weight="bold")
    atom(ax, c2, "C", weight="bold")
    h = c1 + np.array([-0.35, 0.9])
    br = c2 + np.array([0.35, -0.9])
    wedge(ax, c1, h, trim=(0.24, 0.18))
    hashed(ax, c2, br, trim=(0.24, 0.22))
    atom(ax, h, "H", color=ORANGE, weight="bold")
    atom(ax, br, "Br", color=BLUE, weight="bold")
    for c, sx in ((c1, -1), (c2, 1)):
        for sy in (1, -1):
            bond(ax, c, c + np.array([sx * 0.7, sy * 0.55]), trim=(0.24, 0.0), color=GRAY, lw=1.2)
    base = h + np.array([-0.95, 0.25])
    atom(ax, base, "B$^-$", color=BLUE, weight="bold")
    curly(ax, base + np.array([0.3, -0.16]), h + np.array([-0.32, 0.06]), rad=-0.3, shrink=2)
    curly(
        ax,
        (c1 + h) / 2 + np.array([0.3, 0.06]),
        (c1 + c2) / 2 + np.array([-0.05, 0.3]),
        rad=-0.5,
        shrink=2,
    )
    curly(
        ax,
        (c2 + br) / 2 + np.array([-0.26, -0.02]),
        br + np.array([0.44, 0.06]),
        rad=0.45,
        shrink=2,
    )
    note(
        ax,
        (0.1, -1.6),
        "H と脱離基が 180° で向き合ったときだけ、\n生まれる π 軌道がきれいに重なる",
        size=9,
    )

    ax = axes[1]
    canvas(ax, (-0.9, 6.1), (-2.8, 2.8), "塩基の大きさで主生成物が変わる")
    pts = zigzag((0.3, 0.8), 2, dx=0.8, dy=0.42)
    bond(ax, pts[0], pts[1])
    bond(ax, pts[1], pts[2], order=2)
    bond(ax, pts[1], pts[1] + np.array([0.0, 0.8]))
    note(ax, (1.1, 0.15), "多置換アルケン (Zaitsev)", size=9)
    note(
        ax,
        (3.1, 1.1),
        "EtO$^-$ のような小さい塩基\n→ こちらが主 (およそ 7:3)",
        size=9,
        color=GREEN,
        ha="left",
    )

    pts2 = zigzag((0.3, -1.5), 2, dx=0.8, dy=0.42)
    bond(ax, pts2[0], pts2[1])
    bond(ax, pts2[1], pts2[2])
    bond(ax, pts2[1], pts2[1] + np.array([0.0, 0.85]), order=2)
    note(ax, (1.1, -2.1), "末端アルケン (Hofmann)", size=9)
    note(
        ax,
        (3.1, -1.2),
        "$t$-BuO$^-$ のようなかさ高い塩基\n→ こちらが主 (比が逆転する)",
        size=9,
        color=PURPLE,
        ha="left",
    )

    fig.suptitle("E2: 塩基が H を引き抜き、同時に脱離基が外れる", y=1.05, fontsize=12)
    save(fig, "oc-e2.svg")


# ------------------------------------------------------------------ 図 11


def fig_decision():
    fig, ax = plt.subplots(figsize=(9.8, 3.6))
    cols = [
        "弱い求核剤\n(H$_2$O, ROH)",
        "強い求核剤・弱い塩基\n(I$^-$, RS$^-$, N$_3^-$, CN$^-$)",
        "強い塩基\n(HO$^-$, EtO$^-$)",
        "かさ高い強塩基\n($t$-BuO$^-$, LDA)",
    ]
    rows = ["3° (第三級)", "2° (第二級)", "1° (第一級)", "メチル"]
    cells = [
        ["S$_N$1 / E1", "S$_N$1 / E1", "E2", "E2"],
        ["S$_N$1 / E1 (遅い)", "S$_N$2", "E2", "E2"],
        ["ほぼ反応しない", "S$_N$2", "S$_N$2 + E2", "E2"],
        ["ほぼ反応しない", "S$_N$2", "S$_N$2", "S$_N$2"],
    ]

    def color_of(text):
        if text.startswith("ほぼ"):
            return "#f3f4f6"
        if "S$_N$1" in text:
            return "#ffedd5"
        if text.startswith("E"):
            return "#dcfce7"
        return "#dbeafe"

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.axis("off")
    for i in range(4):
        for j in range(4):
            ax.add_patch(Rectangle((j, i), 1, 1, fc=color_of(cells[i][j]), ec="white", lw=2))
            ax.text(j + 0.5, i + 0.5, cells[i][j], ha="center", va="center", fontsize=10)
    for j, c in enumerate(cols):
        ax.text(j + 0.5, 4.12, c, ha="center", va="bottom", fontsize=9.5, color=INK)
    for i, r in enumerate(rows):
        ax.text(-0.12, i + 0.5, r, ha="right", va="center", fontsize=10, color=INK)
    ax.text(-0.12, 4.12, "基質 ＼ 試薬", ha="right", va="bottom", fontsize=9.5, color=GRAY)
    ax.text(
        2.0,
        -0.45,
        "温度を上げると、どのマスでも脱離 (E) の割合が増える",
        ha="center",
        fontsize=9.5,
        color=GRAY,
    )
    ax.set_title("置換か脱離か: 基質の級数と試薬の性格でほぼ決まる", pad=34)
    save(fig, "oc-decision.svg")


# ------------------------------------------------------------------ 図 12


def fig_markovnikov():
    fig, axes = plt.subplots(2, 1, figsize=(9.8, 5.4))

    ax = axes[0]
    canvas(ax, (-1.2, 11.0), (-2.0, 2.0), "Markovnikov 則の中身: 中間体が安定な道を通る")
    p = zigzag((0.0, -0.2), 2, dx=0.8, dy=0.45)
    bond(ax, p[0], p[1], order=2)
    bond(ax, p[1], p[2])
    note(ax, (0.8, -1.0), "プロペン + HBr", size=9)
    reaction_arrow(ax, (2.4, 0.1), (3.4, 0.9), color=GRAY)
    reaction_arrow(ax, (2.4, -0.3), (3.4, -1.0), color=GRAY)

    q = zigzag((3.9, 1.0), 2, dx=0.8, dy=0.4)
    bond(ax, q[0], q[1])
    bond(ax, q[1], q[2])
    atom(ax, q[1] + np.array([0.0, 0.3]), "$+$", color=ORANGE, size=13, pad=0.05)
    note(ax, (6.0, 1.2), "2° カチオン (安定・速い) → 主生成物 2-ブロモプロパン", size=9, color=GREEN, ha="left")

    r = zigzag((3.9, -1.2), 2, dx=0.8, dy=0.4)
    bond(ax, r[0], r[1])
    bond(ax, r[1], r[2])
    atom(ax, r[0] + np.array([-0.1, 0.28]), "$+$", color=ORANGE, size=13, pad=0.05)
    note(ax, (6.0, -1.0), "1° カチオン (不安定・遅い) → ほとんどできない", size=9, ha="left")
    note(
        ax,
        (1.0, 1.35),
        "「H は H の多い側につく」ではなく\n「より安定なカチオンができる側に H がつく」",
        size=9,
    )

    ax = axes[1]
    canvas(ax, (-1.2, 11.0), (-2.0, 2.0), "ハロゲン付加は必ず anti になる")
    a = np.array([-0.7, -0.35])
    b = np.array([0.15, 0.15])
    c = np.array([1.15, 0.15])
    d = np.array([2.0, -0.35])
    bond(ax, a, b)
    bond(ax, b, c, order=2)
    bond(ax, c, d)
    note(ax, (0.65, -0.95), "アルケン", size=9)
    reaction_arrow(ax, (2.6, 0.0), (3.5, 0.0), label="Br$_2$")

    b2 = np.array([4.2, 0.0])
    c2 = np.array([5.2, 0.0])
    apex = np.array([4.7, 0.95])
    bond(ax, b2, c2)
    bond(ax, b2, apex, trim=(0.0, 0.26), color=ORANGE)
    bond(ax, c2, apex, trim=(0.0, 0.26), color=ORANGE)
    atom(ax, apex, "Br$^+$", color=ORANGE, size=10)
    bond(ax, b2, b2 + np.array([-0.8, -0.5]), color=GRAY, lw=1.2)
    bond(ax, c2, c2 + np.array([0.8, -0.5]), color=GRAY, lw=1.2)
    atom(ax, (5.9, -1.05), "Br$^-$", color=BLUE, size=10)
    curly(ax, (5.65, -0.85), (5.3, -0.25), rad=0.3)
    note(ax, (4.7, -1.55), "ブロモニウムイオン (上の面がふさがれる)", size=9)

    reaction_arrow(ax, (6.8, 0.0), (7.7, 0.0))
    b3 = np.array([8.5, 0.0])
    c3 = np.array([9.5, 0.0])
    bond(ax, b3, c3)
    bond(ax, b3, b3 + np.array([-0.8, -0.5]), color=GRAY, lw=1.2)
    bond(ax, c3, c3 + np.array([0.8, -0.5]), color=GRAY, lw=1.2)
    wedge(ax, b3, b3 + np.array([-0.1, 0.8]), trim=(0.0, 0.2), color=ORANGE)
    hashed(ax, c3, c3 + np.array([0.1, -0.8]), trim=(0.0, 0.24), color=ORANGE)
    atom(ax, b3 + np.array([-0.1, 0.95]), "Br", color=ORANGE, size=10)
    atom(ax, c3 + np.array([0.1, -0.95]), "Br", color=ORANGE, size=10)
    note(ax, (8.4, 1.65), "2 つの Br は必ず反対の面に入る (anti)", size=9, color=ORANGE)

    fig.tight_layout()
    fig.suptitle("アルケンへの求電子付加", y=1.03, fontsize=12)
    save(fig, "oc-markovnikov.svg")


# ------------------------------------------------------------------ 図 13


def fig_carbonyl():
    fig = plt.figure(figsize=(9.8, 3.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.9, 1], wspace=0.1)

    ax = fig.add_subplot(gs[0])
    canvas(ax, (-2.2, 9.4), (-2.3, 2.3))
    heading(ax, 3.6, 2.0, "四面体中間体の運命は「脱離基があるか」で決まる")

    c = np.array([0.2, 0.0])
    o = c + np.array([0.0, 0.95])
    r1 = c + np.array([-0.87, -0.5])
    r2 = c + np.array([0.87, -0.5])
    bond(ax, c, o, order=2, trim=(0.0, 0.26))
    bond(ax, c, r1)
    bond(ax, c, r2, trim=(0.0, 0.2))
    atom(ax, o, "O", color=BLUE, weight="bold")
    note(ax, o + np.array([0.62, -0.06]), "δ−", color=BLUE, size=9)
    note(ax, c + np.array([0.0, -0.42]), "δ+", color=ORANGE, size=9)
    atom(ax, r2 + np.array([0.08, -0.05]), "X", color=GRAY, size=10)
    nu = c + np.array([-1.8, 0.9])
    atom(ax, nu, "Nu$^-$", color=BLUE, weight="bold")
    curly(ax, nu + np.array([0.45, -0.26]), c + np.array([-0.32, 0.18]), rad=0.3, shrink=2)
    curly(ax, c + np.array([0.2, 0.45]), o + np.array([0.34, 0.34]), rad=-0.5)
    note(ax, (0.2, -1.4), "① 求核剤が付加", size=9)

    reaction_arrow(ax, (2.0, 0.1), (2.8, 0.1))

    ct = np.array([3.9, 0.1])
    atom(ax, ct, "C", weight="bold")
    bond(ax, ct, ct + np.array([0.0, 0.95]), trim=(0.24, 0.28))
    atom(ax, ct + np.array([0.0, 0.95]), "O$^-$", color=BLUE, weight="bold")
    bond(ax, ct, ct + np.array([-0.95, -0.45]), trim=(0.24, 0.24))
    atom(ax, ct + np.array([-1.05, -0.5]), "Nu", color=BLUE, size=10)
    bond(ax, ct, ct + np.array([0.95, -0.45]), trim=(0.24, 0.2))
    atom(ax, ct + np.array([1.05, -0.5]), "X", color=GRAY, size=10)
    bond(ax, ct, ct + np.array([-0.15, -1.0]), trim=(0.24, 0.0), color=GRAY, lw=1.2)
    note(ax, (3.9, -1.4), "② 四面体中間体", size=9)

    reaction_arrow(ax, (5.3, 0.7), (6.1, 1.2), color=GRAY)
    reaction_arrow(ax, (5.3, -0.3), (6.1, -0.8), color=GRAY)
    note(ax, (6.3, 1.35), "X = H, R は脱離できない\n→ アルコール (求核付加)", size=9, ha="left", color=GREEN)
    note(
        ax,
        (6.3, -0.95),
        "X = Cl, OR は脱離できる\n→ C=O が復活 (求核置換)",
        size=9,
        ha="left",
        color=PURPLE,
    )

    ax = fig.add_subplot(gs[1])
    labels = [
        "酸ハロゲン化物 RCOCl",
        "酸無水物 (RCO)$_2$O",
        "エステル RCO$_2$R'",
        "カルボン酸 RCO$_2$H",
        "アミド RCONR$_2$",
        "カルボキシラート RCO$_2^-$",
    ]
    ax.set_xlim(-0.3, 1.0)
    ax.set_ylim(-0.7, 6.2)
    ax.axis("off")
    for i, label in enumerate(labels):
        y = 5.2 - i
        ax.add_patch(Rectangle((0.14, y - 0.32), 0.84, 0.64, fc="#eef2ff", ec="white", lw=1.5))
        ax.text(0.56, y, label, ha="center", va="center", fontsize=9.5)
    ax.add_patch(
        FancyArrowPatch(
            (0.04, 5.3),
            (0.04, -0.1),
            arrowstyle="-|>",
            mutation_scale=12,
            color=ORANGE,
            lw=1.4,
        )
    )
    ax.text(-0.14, 2.6, "反応性が下がる", rotation=90, va="center", ha="center", fontsize=9.5, color=ORANGE)
    ax.text(0.56, -0.5, "上のものから下のものは作れるが、逆は無理", ha="center", fontsize=9, color=GRAY)
    ax.set_title("カルボン酸誘導体の反応性")

    fig.suptitle("カルボニル: 炭素は δ+、酸素は δ−。攻めるのは常に求核剤", y=1.03, fontsize=12)
    save(fig, "oc-carbonyl.svg")


# ------------------------------------------------------------------ 図 14


def fig_eas():
    fig, axes = plt.subplots(2, 1, figsize=(9.8, 5.6))

    ax = axes[0]
    canvas(ax, (-1.6, 10.4), (-1.8, 1.8), "機構: いったん付加してから H$^+$ が取れる")
    benzene(ax, (0.2, 0.2))
    atom(ax, (2.0, 0.95), "E$^+$", color=ORANGE, weight="bold")
    curly(ax, (0.9, 0.75), (1.7, 0.95), rad=-0.3)
    reaction_arrow(ax, (2.7, 0.2), (3.5, 0.2))

    c = np.array([4.6, 0.2])
    pts2 = ring(c, r=0.62)
    for i in range(6):
        bond(ax, pts2[i], pts2[(i + 1) % 6])
    inner_line(ax, pts2[1], pts2[2], c)
    inner_line(ax, pts2[3], pts2[4], c)
    bond(ax, pts2[0], pts2[0] + np.array([0.55, 0.5]), trim=(0.0, 0.2))
    atom(ax, pts2[0] + np.array([0.68, 0.6]), "E", color=ORANGE, size=10)
    bond(ax, pts2[0], pts2[0] + np.array([-0.55, 0.5]), trim=(0.0, 0.2), color=GRAY, lw=1.2)
    atom(ax, pts2[0] + np.array([-0.68, 0.6]), "H", color=GRAY, size=10)
    note(ax, pts2[5] + np.array([0.42, 0.05]), "$+$", color=ORANGE, size=13)
    note(
        ax,
        (4.6, -1.1),
        "アレニウムイオン (σ 複合体)\n芳香族性が一時的に壊れる = 律速段階",
        size=9,
    )

    reaction_arrow(ax, (6.1, 0.2), (6.9, 0.2), label="$-\\,\\mathrm{H^+}$")
    pts3 = benzene(ax, (8.0, 0.2))
    bond(ax, pts3[0], pts3[0] + np.array([0.0, 0.55]), trim=(0.0, 0.18))
    atom(ax, pts3[0] + np.array([0.0, 0.72]), "E", color=ORANGE, size=10)
    note(ax, (8.0, -1.1), "置換生成物\n芳香族性が戻る", size=9)

    ax = axes[1]
    canvas(ax, (-1.6, 10.4), (-3.4, 2.3), "置換基がどこを活性化するか")
    pts4 = benzene(ax, (0.7, 0.9), r=0.58)
    bond(ax, pts4[0], pts4[0] + np.array([0.0, 0.5]), trim=(0.0, 0.18))
    atom(ax, pts4[0] + np.array([0.0, 0.7]), "OMe", color=BLUE, size=10, weight="bold")
    for i, label in ((1, "o"), (5, "o"), (3, "p")):
        d = pts4[i] - np.array([0.7, 0.9])
        d = d / np.hypot(*d)
        pos = pts4[i] + d * 0.38
        ax.plot(*pos, marker="o", ms=15, color=BLUE, alpha=0.2, zorder=0)
        note(ax, pos, label, color=BLUE, size=9)
    note(
        ax,
        (2.4, 1.0),
        "電子供与基 (OMe, NH$_2$, OH, R) → 活性化 & オルト/パラ配向\n"
        "アレニウムイオンの正電荷を置換基が直接支えられる位置が o と p だから",
        size=9,
        color=BLUE,
        ha="left",
    )

    pts5 = benzene(ax, (0.7, -2.05), r=0.58)
    bond(ax, pts5[0], pts5[0] + np.array([0.0, 0.5]), trim=(0.0, 0.16))
    atom(ax, pts5[0] + np.array([0.0, 0.7]), "NO$_2$", color=ORANGE, size=9.5, weight="bold")
    for i in (2, 4):
        d = pts5[i] - np.array([0.7, -2.05])
        d = d / np.hypot(*d)
        pos = pts5[i] + d * 0.38
        ax.plot(*pos, marker="o", ms=15, color=ORANGE, alpha=0.2, zorder=0)
        note(ax, pos, "m", color=ORANGE, size=9)
    note(
        ax,
        (2.4, -2.15),
        "電子求引基 (NO$_2$, C=O, CN) → 不活性化 & メタ配向\n"
        "o と p だと正電荷が置換基の隣に来てしまい、いちばん不安定になるから",
        size=9,
        color=ORANGE,
        ha="left",
    )

    fig.tight_layout()
    fig.suptitle("芳香族求電子置換: 芳香族性を壊してでも反応し、すぐ取り戻す", y=1.03, fontsize=12)
    save(fig, "oc-eas.svg")


# ------------------------------------------------------------------ 図 15


def fig_chirality():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.3))

    ax = axes[0]
    canvas(ax, (-3.0, 3.0), (-2.0, 1.9), "鏡像だが重ね合わせられない")
    ax.plot([0, 0], [-1.5, 1.6], color=LIGHT, lw=1.4, ls=(0, (4, 4)))
    note(ax, (0.0, 1.75), "鏡", size=9)
    for sign, x0 in ((-1, -1.55), (1, 1.55)):
        c = np.array([x0, 0.0])
        atom(ax, c, "C", weight="bold")
        bond(ax, c, c + np.array([0.0, 0.9]), trim=(0.24, 0.2))
        atom(ax, c + np.array([0.0, 1.05]), "OH", color=BLUE, size=10)
        bond(ax, c, c + np.array([sign * -0.8, -0.6]), trim=(0.24, 0.2))
        atom(ax, c + np.array([sign * -1.05, -0.78]), "COOH", size=9.5)
        wedge(ax, c, c + np.array([sign * 0.75, -0.5]), trim=(0.26, 0.16))
        atom(ax, c + np.array([sign * 0.95, -0.62]), "CH$_3$", size=9.5)
        hashed(ax, c, c + np.array([sign * 0.65, 0.45]), trim=(0.26, 0.12))
        atom(ax, c + np.array([sign * 0.85, 0.58]), "H", color=GRAY, size=10)
    note(ax, (-1.55, -1.65), "(R)-乳酸", size=9.5)
    note(ax, (1.55, -1.65), "(S)-乳酸", size=9.5)

    ax = axes[1]
    canvas(ax, (-2.4, 2.4), (-2.0, 1.9), "R / S の決め方")
    c = np.array([0.1, 0.35])
    atom(ax, c, "C", weight="bold")
    for label, ang in (("1", 90), ("2", 210), ("3", -30)):
        th = np.deg2rad(ang)
        p = c + 0.95 * np.array([np.cos(th), np.sin(th)])
        bond(ax, c, p, trim=(0.24, 0.2))
        atom(ax, p, label, color=BLUE, weight="bold")
    hashed(ax, c, c + np.array([0.72, 0.6]), trim=(0.26, 0.14), color=GRAY)
    atom(ax, c + np.array([0.9, 0.75]), "4", color=GRAY, size=10)
    ax.add_patch(
        FancyArrowPatch(
            (0.1, 0.97),
            (-0.55, -0.05),
            connectionstyle="arc3,rad=0.55",
            arrowstyle="-|>",
            mutation_scale=13,
            color=PURPLE,
            lw=1.6,
        )
    )
    note(ax, (-1.35, 0.9), "1→2→3 が\n反時計回り = S", color=PURPLE, size=9)
    note(
        ax,
        (0.1, -1.55),
        "① 原子番号で優先順位 1–4 を付ける\n② 最下位 (4) を奥に置く\n"
        "③ 1→2→3 が時計回りなら R、反時計回りなら S",
        size=9,
    )

    fig.suptitle("キラリティ: 4 つの異なる基がついた炭素は左右の手になる", y=1.05, fontsize=12)
    save(fig, "oc-chirality.svg")


# ------------------------------------------------------------------ 図 16


def fig_spectroscopy():
    fig, axes = plt.subplots(2, 1, figsize=(9.8, 4.6))

    ax = axes[0]
    ax.set_xlim(4000, 500)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("波数 [cm$^{-1}$]")
    ax.set_title("IR: どの官能基があるか")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    bands = [
        (3200, 3600, "O–H (幅広い)", BLUE, 0.72),
        (3300, 3500, "N–H", PURPLE, 0.42),
        (2850, 3100, "C–H", GRAY, 0.72),
        (2100, 2260, "C≡C / C≡N", GREEN, 0.72),
        (1630, 1800, "C=O (鋭くて強い)", ORANGE, 0.72),
        (1450, 1650, "C=C・芳香環", GREEN, 0.42),
        (500, 1400, "指紋領域", LIGHT, 0.2),
    ]
    for lo, hi, label, color, y in bands:
        ax.add_patch(Rectangle((lo, y - 0.13), hi - lo, 0.26, fc=color, ec="none", alpha=0.3))
        ax.text((lo + hi) / 2, y, label, ha="center", va="center", fontsize=8.5, color=INK)

    ax = axes[1]
    ax.set_xlim(12, 0)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("化学シフト δ [ppm]")
    ax.set_title("$^1$H NMR: 水素がどんな環境にいるか")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ranges = [
        (0.7, 1.7, "アルカン", GRAY, 0.72),
        (2.0, 2.7, "C=O の隣 / ベンジル位", GREEN, 0.42),
        (3.2, 4.5, "O や N の隣", BLUE, 0.72),
        (4.5, 6.5, "アルケン", PURPLE, 0.42),
        (6.5, 8.2, "芳香環", ORANGE, 0.72),
        (9.5, 10.2, "アルデヒド", ORANGE, 0.42),
        (10.5, 12.0, "カルボン酸", BLUE, 0.72),
    ]
    for lo, hi, label, color, y in ranges:
        ax.add_patch(Rectangle((lo, y - 0.13), hi - lo, 0.26, fc=color, ec="none", alpha=0.3))
        ax.text((lo + hi) / 2, y, label, ha="center", va="center", fontsize=8.5, color=INK)
    ax.text(0.2, 0.12, "TMS = 0", fontsize=9, color=GRAY, ha="right")

    fig.tight_layout()
    save(fig, "oc-spectroscopy.svg")


# ------------------------------------------------------------------ 図 17


def fig_retrosynthesis():
    fig, ax = plt.subplots(figsize=(9.8, 3.0))
    canvas(ax, (-1.6, 10.0), (-1.9, 1.9))

    c = np.array([0.9, 0.0])
    me1 = c + np.array([-0.87, -0.5])
    me2 = c + np.array([0.87, -0.5])
    oh = c + np.array([0.0, 0.95])
    et = c + np.array([0.0, -1.0])
    bond(ax, c, me1)
    bond(ax, c, me2)
    bond(ax, c, oh, trim=(0.0, 0.26))
    bond(ax, c, et)
    bond(ax, et, et + np.array([0.87, -0.5]))
    atom(ax, oh, "OH", color=BLUE, weight="bold")
    ax.plot([0.45, 1.35], [-0.35, -0.65], color=ORANGE, lw=1.4, ls=(0, (4, 3)))
    note(ax, (1.5, -0.85), "ここで切る", color=ORANGE, size=9, ha="left")
    note(ax, (0.6, -1.75), "目標物質 (2-メチルブタン-2-オール)", size=9)

    ax.add_patch(
        FancyArrowPatch((3.3, 0.1), (4.4, 0.1), arrowstyle="-|>", mutation_scale=13, color=INK, lw=1.4)
    )
    ax.add_patch(FancyArrowPatch((3.3, -0.08), (4.4, -0.08), arrowstyle="-", color=INK, lw=1.4))
    note(ax, (3.85, 0.5), "逆合成", size=9)

    c2 = np.array([5.6, 0.0])
    o2 = c2 + np.array([0.0, 0.95])
    bond(ax, c2, o2, order=2, trim=(0.0, 0.26))
    bond(ax, c2, c2 + np.array([0.87, -0.5]))
    bond(ax, c2, c2 + np.array([-0.87, -0.5]))
    atom(ax, o2, "O", color=BLUE, weight="bold")
    note(ax, (5.6, -1.75), "アセトン (求電子剤)", size=9)
    ax.text(7.2, 0.0, "＋", fontsize=13, ha="center", va="center", color=INK)

    p = np.array([8.3, -0.3])
    bond(ax, p, p + np.array([0.87, 0.5]), trim=(0.24, 0.0))
    atom(ax, p, "$^-$", color=BLUE, size=15, pad=0.05)
    note(ax, (8.7, -1.75), "エチルアニオン (求核剤)\n実体は EtMgBr / EtLi", size=9)
    note(ax, (8.7, 1.3), "シントン → 等価な試薬に読み替える", size=9, color=PURPLE)

    fig.suptitle("逆合成: 作りたい結合を切って、極性が逆の 2 つの断片に分ける", y=1.04, fontsize=12)
    save(fig, "oc-retrosynthesis.svg")


def main():
    if PNG_DIR:
        Path(PNG_DIR).mkdir(parents=True, exist_ok=True)
    fig_skeletal()
    fig_hybridization()
    fig_induction()
    fig_resonance()
    fig_pka()
    fig_arrows()
    fig_carbocation()
    fig_sn2()
    fig_sn1()
    fig_e2()
    fig_decision()
    fig_markovnikov()
    fig_carbonyl()
    fig_eas()
    fig_chirality()
    fig_spectroscopy()
    fig_retrosynthesis()


if __name__ == "__main__":
    main()
