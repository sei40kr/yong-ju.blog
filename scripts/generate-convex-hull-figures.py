"""content/posts/convex-hull.mdx の図を生成する。

出力先は public/img/hull-*.svg。
アルゴリズムは記事の説明とずれないよう、外部ライブラリを使わずここで実装する。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-convex-hull-figures.py

環境変数 HULL_PNG_DIR を指定すると、目視確認用に同じ図を PNG でも書き出す。
"""

import os
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.path import Path as MplPath
from matplotlib.patches import Circle, Polygon

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"
PNG_DIR = os.environ.get("HULL_PNG_DIR")

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
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


# ------------------------------------------------------------------ 幾何


def cross(o, a, b):
    """ベクトル oa と ob の外積 (z 成分)。正なら o->a->b は反時計回り。"""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def monotone_chain(points):
    """Andrew's monotone chain。反時計回りの凸包頂点列を返す。"""
    pts = sorted(map(tuple, points))
    if len(pts) <= 2:
        return pts

    def build(seq):
        chain = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        return chain

    lower = build(pts)
    upper = build(reversed(pts))
    return lower[:-1] + upper[:-1]


def jarvis_march(points, record=False):
    """ギフト包装法。record=True なら各ステップの (始点, 候補列, 採用点) も返す。"""
    pts = [tuple(p) for p in points]
    start = min(pts)
    hull, steps = [], []
    p = start
    while True:
        q = pts[0] if pts[0] != p else pts[1]
        tried = []
        for r in pts:
            if r == p:
                continue
            tried.append((r, q))
            # r が現在の候補 q より右側にあれば、より外側の候補として乗り換える
            c = cross(p, q, r)
            if c < 0 or (c == 0 and np.hypot(*np.subtract(r, p)) > np.hypot(*np.subtract(q, p))):
                q = r
        hull.append(p)
        if record:
            steps.append((p, tried, q))
        p = q
        if p == start:
            break
    return (hull, steps) if record else hull


def graham_scan(points, record=False):
    """Graham scan。基準点からの偏角順に走査し、右折したら pop する。"""
    pts = [tuple(p) for p in points]
    p0 = min(pts, key=lambda p: (p[1], p[0]))
    rest = sorted(
        (p for p in pts if p != p0),
        key=lambda p: (np.arctan2(p[1] - p0[1], p[0] - p0[0]), np.hypot(p[0] - p0[0], p[1] - p0[1])),
    )
    stack, events = [p0], []
    for p in rest:
        while len(stack) >= 2 and cross(stack[-2], stack[-1], p) <= 0:
            popped = stack.pop()
            events.append((list(stack), popped, p))
        stack.append(p)
    return (stack, [p0] + rest, events) if record else stack


def quickhull_upper(points, a, b, depth=0, log=None):
    """線分 ab の左側にある点だけを対象に、a から b への上側の鎖を返す。"""
    outside = [p for p in points if cross(a, b, p) > 0]
    if log is not None:
        log.append((depth, a, b, outside))
    if not outside:
        return [a]
    # ab から最も遠い点が凸包の頂点になる
    c = max(outside, key=lambda p: abs(cross(a, b, p)))
    return quickhull_upper(outside, a, c, depth + 1, log) + quickhull_upper(
        outside, c, b, depth + 1, log
    )


def bridges(left, right):
    """左右の部分凸包を結ぶ 2 本の接線 (下接線, 上接線) を返す。"""
    hull = monotone_chain(left + right)
    ls, rs = set(map(tuple, left)), set(map(tuple, right))
    edges = [(hull[i], hull[(i + 1) % len(hull)]) for i in range(len(hull))]
    cut = [(u, v) for u, v in edges if (u in ls) != (v in ls)]
    assert rs
    assert len(cut) == 2, cut
    # y の平均が小さいほうが下接線
    cut.sort(key=lambda e: e[0][1] + e[1][1])
    return cut[0], cut[1]


def tangent_from(p, hull):
    """点 p から凸包 hull への「最も時計回り側」の接点 (ギフト包装法の候補)。"""
    q = hull[0] if hull[0] != p else hull[1]
    for r in hull:
        if r == p:
            continue
        if cross(p, q, r) < 0:
            q = r
    return q


# ------------------------------------------------------------------ 作画


def bare(ax, xlim, ylim, title=None):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(False)
    if title:
        ax.set_title(title)


def dots(ax, pts, color=GRAY, size=34, zorder=3, **kw):
    pts = np.asarray(list(pts), dtype=float)
    if len(pts) == 0:
        return
    ax.scatter(
        pts[:, 0], pts[:, 1], c=color, s=size, zorder=zorder, linewidths=0.8, edgecolors="white", **kw
    )


def hull_patch(ax, hull, color=BLUE, alpha=0.12, lw=1.8, ls="-", zorder=1, fill=True):
    ax.add_patch(
        Polygon(
            np.asarray(hull, dtype=float),
            closed=True,
            facecolor=color if fill else "none",
            edgecolor=color,
            alpha=alpha if fill else 1.0,
            lw=0,
            zorder=zorder,
        )
    )
    pts = np.asarray(list(hull) + [hull[0]], dtype=float)
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, ls=ls, zorder=zorder + 1)


def arrow(ax, p, q, color=INK, lw=1.6, ls="-", alpha=1.0, zorder=4, shrink=6):
    ax.annotate(
        "",
        xy=q,
        xytext=p,
        zorder=zorder,
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=lw,
            ls=ls,
            alpha=alpha,
            shrinkA=shrink,
            shrinkB=shrink,
            mutation_scale=13,
        ),
    )


def label(ax, p, text, dx=0.0, dy=0.22, color=INK, size=10, **kw):
    ax.text(p[0] + dx, p[1] + dy, text, color=color, fontsize=size, ha="center", va="center", zorder=6, **kw)


def legend(fig, entries, y=-0.02, ncol=None):
    handles = [
        Line2D([], [], color=c, ls=ls, marker=m, markersize=7, lw=lw, label=t)
        for t, c, m, ls, lw in entries
    ]
    fig.legend(handles=handles, loc="lower center", ncol=ncol or len(entries), bbox_to_anchor=(0.5, y))


# ------------------------------------------------------------------ データ

SAMPLE = [
    (0.4, 1.0),
    (1.3, 3.5),
    (1.7, 0.4),
    (2.3, 2.1),
    (2.6, 4.3),
    (3.1, 1.3),
    (3.4, 3.0),
    (4.2, 0.7),
    (4.5, 2.5),
    (4.9, 4.1),
    (5.6, 1.6),
    (5.9, 3.3),
    (6.4, 2.2),
    (3.8, 4.6),
    (2.0, 2.9),
]

XLIM, YLIM = (-0.2, 7.0), (-0.3, 5.3)


def random_points(n, seed, shape="disk"):
    rng = np.random.RandomState(seed)
    if shape == "disk":
        r = np.sqrt(rng.rand(n))
        t = rng.rand(n) * 2 * np.pi
    else:  # 円周上 (すべての点が凸包の頂点になる最悪ケース)
        r = np.ones(n)
        t = np.sort(rng.rand(n) * 2 * np.pi)
    return list(zip(r * np.cos(t), r * np.sin(t)))


# ------------------------------------------------------------- figure 1


def fig_convex_set():
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.6))

    convex = [(0.3, 0.4), (2.4, 0.1), (3.4, 1.6), (2.6, 3.2), (0.8, 2.9), (0.0, 1.6)]
    concave = [(0.3, 0.4), (2.4, 0.1), (3.4, 1.6), (1.7, 1.5), (2.6, 3.2), (0.8, 2.9), (0.0, 1.6)]

    for ax, poly, seg, title in (
        (axes[0], convex, ((0.7, 0.9), (2.9, 2.6)), "凸集合"),
        (axes[1], concave, ((0.9, 0.7), (2.9, 2.7)), "凸集合でない"),
    ):
        path = MplPath(poly)
        ax.add_patch(Polygon(poly, closed=True, facecolor=BLUE, alpha=0.1, lw=0))
        ax.add_patch(Polygon(poly, closed=True, facecolor="none", edgecolor=BLUE, lw=1.6))

        ts = np.linspace(0, 1, 400)[:, None]
        line = np.array(seg[0]) * (1 - ts) + np.array(seg[1]) * ts
        inside = path.contains_points(line)
        for mask, color, lw in ((inside, INK, 1.8), (~inside, ORANGE, 2.6)):
            xs = np.where(mask, line[:, 0], np.nan)
            ys = np.where(mask, line[:, 1], np.nan)
            ax.plot(xs, ys, color=color, lw=lw, zorder=4, solid_capstyle="round")
        dots(ax, seg, color=INK, size=40, zorder=5)
        label(ax, seg[0], "$\\mathbf{x}$", dx=-0.28, dy=-0.05)
        label(ax, seg[1], "$\\mathbf{y}$", dx=0.3, dy=0.05)
        if not inside.all():
            out = line[~inside]
            label(ax, out[len(out) // 2], "はみ出す", dx=0.95, dy=0.28, color=ORANGE, size=10)
        bare(ax, (-0.5, 4.2), (-0.5, 3.7), title)

    fig.tight_layout()
    save(fig, "hull-convex-set.svg")


# ------------------------------------------------------------- figure 2


def fig_definition():
    hull = monotone_chain(SAMPLE)
    interior = [p for p in SAMPLE if p not in set(hull)]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))

    dots(axes[0], SAMPLE, color=INK)
    bare(axes[0], XLIM, YLIM, "点集合 $S$")

    ax = axes[1]
    hull_patch(ax, hull)
    dots(ax, interior, color=GRAY)
    dots(ax, hull, color=BLUE, size=52)
    bare(ax, XLIM, YLIM, "凸包 $\\mathrm{conv}(S)$")

    legend(
        fig,
        [
            ("凸包の頂点 (極点)", BLUE, "o", "none", 0),
            ("内部の点", GRAY, "o", "none", 0),
        ],
        y=-0.03,
    )
    fig.tight_layout()
    save(fig, "hull-definition.svg")


# ------------------------------------------------------------- figure 3


def fig_orientation():
    fig, axes = plt.subplots(1, 3, figsize=(8.4, 3.2))

    o, a = (0.4, 0.5), (2.4, 1.0)
    cases = (
        ((3.1, 2.6), "反時計回り (左折)", "$\\mathrm{cross} > 0$", BLUE),
        ((3.4, 0.0), "時計回り (右折)", "$\\mathrm{cross} < 0$", ORANGE),
        ((4.4, 1.5), "一直線", "$\\mathrm{cross} = 0$", GRAY),
    )

    for ax, (b, title, sign, color) in zip(axes, cases):
        ax.add_patch(Polygon([o, a, b], closed=True, facecolor=color, alpha=0.12, lw=0))
        arrow(ax, o, a, color=INK, shrink=7)
        arrow(ax, a, b, color=color, shrink=7)
        dots(ax, [o, a, b], color=INK, size=40, zorder=5)
        label(ax, o, "$\\mathbf{o}$", dy=-0.42)
        label(ax, a, "$\\mathbf{a}$", dy=-0.42)
        label(ax, b, "$\\mathbf{b}$", dy=0.42)
        ax.text(
            0.5,
            -0.02,
            sign,
            transform=ax.transAxes,
            ha="center",
            va="top",
            color=color,
            fontsize=11,
        )
        bare(ax, (-0.3, 5.0), (-0.9, 3.3), title)

    fig.tight_layout()
    save(fig, "hull-orientation.svg")


# ------------------------------------------------------------- figure 4


def fig_jarvis():
    hull, steps = jarvis_march(SAMPLE, record=True)

    fig, axes = plt.subplots(2, 2, figsize=(8.2, 6.0))
    shown = [0, 1, 2, len(steps) - 1]

    for ax, k in zip(axes.ravel(), shown):
        p, tried, q = steps[k]
        last = k == len(steps) - 1
        if not last:
            for r, _ in tried:
                ax.plot([p[0], r[0]], [p[1], r[1]], color=LIGHT, lw=0.7, zorder=1)
        chain = [s[0] for s in steps[: k + 1]] + [q]
        for u, v in zip(chain, chain[1:]):
            arrow(ax, u, v, color=BLUE, lw=1.8, shrink=5)
        dots(ax, SAMPLE, color=GRAY)
        dots(ax, chain, color=BLUE, size=48, zorder=4)
        dots(ax, [p], color=INK, size=54, zorder=5)
        label(ax, p, "$\\mathbf{p}$", dy=-0.4)
        if not last:
            label(ax, q, "採用", dy=0.42, color=BLUE)
        title = "1. 最も左の点から始める" if k == 0 else f"{k + 1}. 最も右回りの点を選ぶ"
        if last:
            title = f"{k + 1}. 出発点に戻って終了"
        bare(ax, XLIM, YLIM, title)

    fig.tight_layout()
    save(fig, "hull-jarvis.svg")


# ------------------------------------------------------------- figure 5


def fig_graham():
    stack, order, events = graham_scan(SAMPLE, record=True)
    p0 = order[0]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.6))

    ax = axes[0]
    for i, p in enumerate(order[1:], start=1):
        ax.plot([p0[0], p[0]], [p0[1], p[1]], color=LIGHT, lw=0.8, zorder=1)
        label(ax, p, str(i), dy=0.36, color=GRAY, size=9)
    ax.add_patch(Circle(p0, 0.6, facecolor=ORANGE, alpha=0.13, lw=0, zorder=1))
    dots(ax, SAMPLE, color=GRAY)
    dots(ax, [p0], color=ORANGE, size=54, zorder=5)
    label(ax, p0, "$\\mathbf{p}_0$", dy=-0.42, color=ORANGE)
    bare(ax, XLIM, YLIM, "基準点 $\\mathbf{p}_0$ からの偏角でソート")

    ax = axes[1]
    keep, popped, nxt = events[len(events) // 2]
    chain = np.array(keep + [popped], dtype=float)
    ax.plot(chain[:, 0], chain[:, 1], color=BLUE, lw=1.8, zorder=2)
    ax.plot(
        [popped[0], nxt[0]],
        [popped[1], nxt[1]],
        color=ORANGE,
        lw=1.6,
        ls=":",
        zorder=2,
    )
    arrow(ax, keep[-1], nxt, color=BLUE, lw=1.8, ls="--", shrink=5)
    dots(ax, SAMPLE, color=GRAY)
    dots(ax, keep, color=BLUE, size=48, zorder=4)
    ax.scatter(
        [popped[0]], [popped[1]], marker="x", c=ORANGE, s=90, linewidths=2.2, zorder=6
    )
    label(ax, popped, "右折 → pop", dx=-0.95, dy=-0.28, color=ORANGE)
    label(ax, nxt, "次の点", dx=-0.55, dy=0.35, color=BLUE)
    bare(ax, XLIM, YLIM, "右折になったらスタックから捨てる")

    fig.tight_layout()
    save(fig, "hull-graham.svg")


# ------------------------------------------------------------- figure 6


def fig_monotone_chain():
    pts = sorted(map(tuple, SAMPLE))

    def build(seq):
        chain = []
        for p in seq:
            while len(chain) >= 2 and cross(chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
        return chain

    lower, upper = build(pts), build(list(reversed(pts)))

    fig, axes = plt.subplots(1, 3, figsize=(8.4, 3.0))

    ax = axes[0]
    for i, p in enumerate(pts, start=1):
        label(ax, p, str(i), dy=0.4, color=GRAY, size=9)
    dots(ax, pts, color=INK)
    ax.annotate(
        "",
        xy=(6.6, -0.05),
        xytext=(0.1, -0.05),
        arrowprops=dict(arrowstyle="-|>", color=LIGHT, lw=1.4, mutation_scale=13),
    )
    bare(ax, XLIM, YLIM, "1. $x$ 座標でソート")

    for ax, chain, color, title in (
        (axes[1], lower, BLUE, "2. 下側チェーン"),
        (axes[2], upper, ORANGE, "3. 上側チェーン → 連結して完成"),
    ):
        if ax is axes[2]:
            low = np.array(lower, dtype=float)
            ax.plot(low[:, 0], low[:, 1], color=BLUE, lw=1.8, zorder=2)
            dots(ax, lower, color=BLUE, size=44, zorder=3)
        arr = np.array(chain, dtype=float)
        ax.plot(arr[:, 0], arr[:, 1], color=color, lw=1.8, zorder=2)
        dots(ax, SAMPLE, color=GRAY)
        dots(ax, chain, color=color, size=44, zorder=4)
        bare(ax, XLIM, YLIM, title)

    fig.tight_layout()
    save(fig, "hull-monotone-chain.svg")


# ------------------------------------------------------------- figure 7


def fig_quickhull():
    a, b = min(SAMPLE), max(SAMPLE)
    log = []
    quickhull_upper(SAMPLE, a, b, log=log)

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))

    _, a0, b0, outside0 = log[0]
    c0 = max(outside0, key=lambda p: abs(cross(a0, b0, p)))

    ax = axes[0]
    ax.add_patch(Polygon([a0, b0, c0], closed=True, facecolor=GREEN, alpha=0.12, lw=0))
    ax.plot([a0[0], b0[0]], [a0[1], b0[1]], color=INK, lw=1.6, zorder=2)
    for u, v in ((a0, c0), (c0, b0)):
        ax.plot([u[0], v[0]], [u[1], v[1]], color=GREEN, lw=1.6, zorder=2)
    dropped = [
        p
        for p in outside0
        if p != c0 and cross(a0, c0, p) < 0 and cross(c0, b0, p) < 0
    ]
    dots(ax, SAMPLE, color=GRAY)
    dots(ax, [a0, b0], color=BLUE, size=52, zorder=4)
    dots(ax, [c0], color=GREEN, size=54, zorder=4)
    if dropped:
        arr = np.array(dropped, dtype=float)
        ax.scatter(arr[:, 0], arr[:, 1], marker="x", c=ORANGE, s=70, linewidths=1.8, zorder=5)
        label(ax, dropped[0], "三角形の内側は捨てる", dx=0.55, dy=0.55, color=ORANGE, size=9)
    label(ax, a0, "$\\mathbf{a}$", dx=-0.3, dy=-0.1, color=BLUE)
    label(ax, b0, "$\\mathbf{b}$", dx=0.3, dy=0.0, color=BLUE)
    label(ax, c0, "最遠点 $\\mathbf{c}$", dy=0.42, color=GREEN)
    bare(ax, XLIM, YLIM, "$\\mathbf{ab}$ から最も遠い点で分割")

    ax = axes[1]
    depth1 = [e for e in log if e[0] == 1]
    for _, u, v, out in depth1:
        if not out:
            continue
        w = max(out, key=lambda p: abs(cross(u, v, p)))
        ax.add_patch(Polygon([u, v, w], closed=True, facecolor=PURPLE, alpha=0.12, lw=0))
        for s, t in ((u, w), (w, v)):
            ax.plot([s[0], t[0]], [s[1], t[1]], color=PURPLE, lw=1.5, zorder=2)
    ax.plot([a0[0], c0[0]], [a0[1], c0[1]], color=GREEN, lw=1.4, ls="--", zorder=2)
    ax.plot([c0[0], b0[0]], [c0[1], b0[1]], color=GREEN, lw=1.4, ls="--", zorder=2)
    ax.plot([a0[0], b0[0]], [a0[1], b0[1]], color=INK, lw=1.4, zorder=2)
    chain = quickhull_upper(SAMPLE, a0, b0) + [b0]
    arr = np.array(chain, dtype=float)
    ax.plot(arr[:, 0], arr[:, 1], color=GREEN, lw=2.0, zorder=3)
    dots(ax, SAMPLE, color=GRAY)
    dots(ax, chain, color=GREEN, size=48, zorder=4)
    bare(ax, XLIM, YLIM, "$\\mathbf{ac}$ 側・$\\mathbf{cb}$ 側で再帰")

    fig.tight_layout()
    save(fig, "hull-quickhull.svg")


# ------------------------------------------------------------- figure 8


def fig_divide_conquer():
    pts = sorted(map(tuple, SAMPLE))
    mid = len(pts) // 2
    left, right = pts[:mid], pts[mid:]
    lh, rh = monotone_chain(left), monotone_chain(right)
    lower, upper = bridges(left, right)
    merged = monotone_chain(SAMPLE)

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))

    for ax, title in ((axes[0], "1. $x$ 座標で二分して部分凸包を作る"), (axes[1], "2. 上下 2 本の接線で貼り合わせる")):
        hull_patch(ax, lh, color=BLUE, alpha=0.1, lw=1.5)
        hull_patch(ax, rh, color=ORANGE, alpha=0.1, lw=1.5)
        dots(ax, SAMPLE, color=GRAY)
        dots(ax, lh, color=BLUE, size=44, zorder=4)
        dots(ax, rh, color=ORANGE, size=44, zorder=4)
        bare(ax, XLIM, YLIM, title)

    ax = axes[1]
    for (u, v), name, dy in ((upper, "上接線", 0.42), (lower, "下接線", -0.5)):
        ax.plot([u[0], v[0]], [u[1], v[1]], color=GREEN, lw=2.0, zorder=5)
        mx, my = (u[0] + v[0]) / 2, (u[1] + v[1]) / 2
        label(ax, (mx, my), name, dy=dy, color=GREEN)
    hull_patch(ax, merged, color=GREEN, alpha=0.07, lw=0.0, fill=True)

    fig.tight_layout()
    save(fig, "hull-divide-conquer.svg")


# ------------------------------------------------------------- figure 9


def fig_chan():
    ordered = sorted(map(tuple, SAMPLE))
    size = len(ordered) // 3
    groups = [ordered[i * size : (i + 1) * size] for i in range(2)] + [ordered[2 * size :]]
    colors = (BLUE, ORANGE, PURPLE)
    minis = [monotone_chain(g) for g in groups]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))

    ax = axes[0]
    for g, h, c in zip(groups, minis, colors):
        hull_patch(ax, h, color=c, alpha=0.1, lw=1.4)
        dots(ax, g, color=c, size=40, zorder=4)
    bare(ax, XLIM, YLIM, "1. $m$ 点ずつに分けて部分凸包 ($O(n \\log m)$)")

    ax = axes[1]
    p = min(SAMPLE)
    for g, h, c in zip(groups, minis, colors):
        hull_patch(ax, h, color=c, alpha=0.07, lw=1.0)
        dots(ax, g, color=c, size=32, zorder=3)
    cands = [tangent_from(p, h) for h in minis if p not in h or len(h) > 1]
    for q in cands:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.0, ls="--", zorder=2)
        dots(ax, [q], color=GRAY, size=42, zorder=4)
    best = cands[0]
    for q in cands[1:]:
        if cross(p, best, q) < 0:
            best = q
    arrow(ax, p, best, color=GREEN, lw=2.0, shrink=6)
    dots(ax, [p], color=INK, size=52, zorder=5)
    dots(ax, [best], color=GREEN, size=52, zorder=5)
    label(ax, p, "$\\mathbf{p}$", dx=-0.3, dy=-0.1)
    label(ax, best, "最も右回りの接点", dx=1.05, dy=-0.35, color=GREEN, size=9)
    bare(ax, XLIM, YLIM, "2. 各部分凸包への接線からギフト包装 ($O(\\log m)$/回)")

    fig.tight_layout()
    save(fig, "hull-chan.svg")


# ------------------------------------------------------------ figure 10


def fig_benchmark():
    sizes = [500, 1000, 2000, 4000, 8000]
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4))

    for ax, shape, title in (
        (axes[0], "disk", "円板内に一様 ($h = \\Theta(n^{1/3})$)"),
        (axes[1], "circle", "円周上 ($h = n$ の最悪ケース)"),
    ):
        rows = {"ギフト包装法": [], "Andrew の monotone chain": []}
        for n in sizes:
            pts = random_points(n, seed=7, shape=shape)
            for name, fn in (
                ("ギフト包装法", jarvis_march),
                ("Andrew の monotone chain", monotone_chain),
            ):
                t0 = time.perf_counter()
                fn(pts)
                rows[name].append(time.perf_counter() - t0)
        for (name, ts), color, marker in zip(rows.items(), (ORANGE, BLUE), ("s", "o")):
            ax.plot(sizes, ts, color=color, marker=marker, ms=5, lw=1.6, label=name)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("点の数 $n$")
        ax.set_ylabel("実行時間 [s]")
        ax.set_title(title)
        ax.grid(alpha=0.25, lw=0.6)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    legend(
        fig,
        [
            ("ギフト包装法", ORANGE, "s", "-", 1.6),
            ("Andrew の monotone chain", BLUE, "o", "-", 1.6),
        ],
        y=-0.06,
    )
    fig.tight_layout()
    save(fig, "hull-benchmark.svg")


FIGURES = (
    fig_convex_set,
    fig_definition,
    fig_orientation,
    fig_jarvis,
    fig_graham,
    fig_monotone_chain,
    fig_quickhull,
    fig_divide_conquer,
    fig_chan,
    fig_benchmark,
)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if PNG_DIR:
        Path(PNG_DIR).mkdir(parents=True, exist_ok=True)
    for figure in FIGURES:
        figure()
