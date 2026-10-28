"""content/posts/complex-function-theory.mdx の図を生成する。

出力先は public/img/cx-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-complex-analysis-figures.py
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Circle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
PURPLE = "#7c3aed"
INK = "#111827"
GRAY = "#6b7280"
LIGHT = "#d1d5db"

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


def plane(ax, xlim, ylim, re="$\\text{Re}$", im="$\\text{Im}$", equal=True):
    """複素平面の実軸・虚軸だけを描く。"""
    ax.axhline(0, color=LIGHT, lw=1.0, zorder=0)
    ax.axvline(0, color=LIGHT, lw=1.0, zorder=0)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    if equal:
        ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(False)
    if re:
        ax.text(xlim[1], 0, re, fontsize=9.5, color=GRAY, ha="right", va="bottom")
    if im:
        ax.text(0, ylim[1], im, fontsize=9.5, color=GRAY, ha="left", va="top")


def cplot(ax, zs, **kwargs):
    return ax.plot(np.real(zs), np.imag(zs), **kwargs)


def cscatter(ax, zs, **kwargs):
    zs = np.atleast_1d(zs)
    return ax.scatter(np.real(zs), np.imag(zs), **kwargs)


def carrow(ax, z0, z1, color=INK, lw=1.2, style="->", **kwargs):
    ax.annotate(
        "",
        xy=(z1.real, z1.imag),
        xytext=(z0.real, z0.imag),
        arrowprops=dict(arrowstyle=style, color=color, lw=lw, **kwargs),
    )


def contour_sum(f, z, n=800):
    """z(t) を離散化した積分路に沿う f の部分和 (台形則) を順に返す。"""
    zs = z(np.linspace(0, 1, n + 1))
    mid = (zs[:-1] + zs[1:]) / 2
    terms = f(mid) * np.diff(zs)
    return zs, np.concatenate([[0], np.cumsum(terms)])


# ---------------------------------------------------------------- figure 1


def fig_de_moivre():
    """ド・モアブルの定理: n 乗は偏角を n 倍・絶対値を n 乗する。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2))

    r, theta = 1.55, math.radians(38)
    z = r * np.exp(1j * theta)

    ax = axes[0]
    plane(ax, (-0.45, 2.0), (-0.45, 1.75))
    ax.add_patch(
        Circle((0, 0), r, fill=False, color=LIGHT, ls="--", lw=1.0, zorder=0)
    )
    carrow(ax, 0j, z, color=BLUE, lw=1.6)
    cscatter(ax, z, s=42, color=BLUE, zorder=3)
    ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=0, theta2=math.degrees(theta), color=ORANGE, lw=1.4))
    ax.text(0.52, 0.13, "$\\theta$", color=ORANGE, fontsize=11)
    ax.text(z.real / 2 - 0.28, z.imag / 2 + 0.05, "$r$", color=BLUE, fontsize=11)
    ax.plot([z.real, z.real], [0, z.imag], color=LIGHT, ls=":", lw=1.0)
    ax.plot([0, z.real], [z.imag, z.imag], color=LIGHT, ls=":", lw=1.0)
    ax.text(z.real, z.imag + 0.08, "$z = r(\\cos\\theta + i\\sin\\theta)$", fontsize=10, color=BLUE)
    ax.text(z.real + 0.02, -0.16, "$r\\cos\\theta$", fontsize=9, color=GRAY, ha="center")
    ax.text(-0.42, z.imag, "$r\\sin\\theta$", fontsize=9, color=GRAY, va="center")
    ax.set_title("極形式")

    ax = axes[1]
    r2, theta2 = 1.2, math.radians(40)
    lim = 2.5
    plane(ax, (-lim, lim), (-2.0, lim))
    powers = np.array([r2**n * np.exp(1j * n * theta2) for n in range(0, 6)])
    dense = np.array(
        [r2**t * np.exp(1j * t * theta2) for t in np.linspace(0, 5, 400)]
    )
    cplot(ax, dense, color=LIGHT, lw=1.2, zorder=0)
    for n in range(1, len(powers)):
        carrow(ax, powers[n - 1], powers[n], color=BLUE, lw=1.1)
    cscatter(ax, powers, s=38, color=BLUE, zorder=3)
    for n, p in enumerate(powers):
        label = "$1$" if n == 0 else ("$z$" if n == 1 else f"$z^{n}$")
        ax.annotate(
            label,
            xy=(p.real, p.imag),
            xytext=(7, 7),
            textcoords="offset points",
            fontsize=10,
            color=INK,
        )
    ax.add_patch(
        Arc((0, 0), 1.4, 1.4, theta1=0, theta2=math.degrees(theta2), color=ORANGE, lw=1.3)
    )
    ax.text(0.8, 0.14, "$\\theta$", color=ORANGE, fontsize=10)
    ax.set_title("$z$ を繰り返し掛ける")
    fig.text(
        0.5,
        -0.01,
        "1 回かけるごとに偏角は $\\theta$ ずつ回り、絶対値は $r$ 倍される "
        "$\\Rightarrow\\ z^n = r^n(\\cos n\\theta + i\\sin n\\theta)$",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "cx-de-moivre.svg")


# ---------------------------------------------------------------- figure 2


def fig_differentiability():
    """複素微分は「どの向きから近づいても同じ値」を要求する。"""
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.6))
    z0 = 0.8 + 0.6j

    ax = axes[0]
    plane(ax, (-0.15, 1.75), (-0.15, 1.45))
    for phi in np.linspace(0, 2 * math.pi, 12, endpoint=False):
        d = 0.45 * np.exp(1j * phi)
        color = ORANGE if abs(math.sin(phi)) < 1e-9 else (GREEN if abs(math.cos(phi)) < 1e-9 else LIGHT)
        carrow(ax, z0 + d, z0 + d * 0.18, color=color, lw=1.1)
    cscatter(ax, z0, s=44, color=INK, zorder=3)
    ax.text(z0.real + 0.06, z0.imag + 0.06, "$z$", fontsize=11)
    ax.text(1.32, 0.62, "$\\Delta y \\to 0$", fontsize=9, color=ORANGE)
    ax.text(0.86, 1.12, "$\\Delta x \\to 0$", fontsize=9, color=GREEN)
    ax.set_title("$\\Delta z \\to 0$ の近づけ方", fontsize=11)

    for ax, f, name, note in (
        (axes[1], lambda w: w**2, "$f(z) = z^2$", "どの向きでも同じ値 $2z$ に収束\n$\\Rightarrow$ 微分可能"),
        (
            axes[2],
            np.conj,
            "$f(z) = \\bar{z}$",
            "向きごとに値が違い、\n細かくしても縮まない\n$\\Rightarrow$ 微分不可能",
        ),
    ):
        phis = np.linspace(0, 2 * math.pi, 24, endpoint=False)
        for h, alpha, size in ((0.5, 0.3, 20), (0.25, 0.6, 26), (0.1, 1.0, 32)):
            dz = h * np.exp(1j * phis)
            q = (f(z0 + dz) - f(z0)) / dz
            cscatter(ax, q, s=size, color=BLUE, alpha=alpha, edgecolors="none", zorder=2)
        if name.endswith("z^2$"):
            cscatter(ax, 2 * z0, s=70, marker="*", color=ORANGE, zorder=4)
            ax.text(2 * z0.real + 0.1, 2 * z0.imag, "$2z$", color=ORANGE, fontsize=10)
            # 原点を含まない範囲なので実軸・虚軸のラベルは出さない
            plane(ax, (0.55, 2.65), (0.15, 2.25), re=None, im=None)
            ax.legend(
                handles=[
                    Line2D([], [], color=BLUE, marker="o", ls="none", ms=5, alpha=0.35, label="$|\\Delta z|$ 大"),
                    Line2D([], [], color=BLUE, marker="o", ls="none", ms=5, label="$|\\Delta z|$ 小"),
                ],
                loc="upper left",
                fontsize=8.5,
                handletextpad=0.3,
                borderpad=0.1,
            )
        else:
            plane(ax, (-1.5, 1.5), (-1.5, 1.5))
        ax.set_title(name, fontsize=11)
        ax.text(
            0.5,
            -0.05,
            note,
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=9,
            color=GRAY,
            linespacing=1.5,
        )

    fig.suptitle("差分商 $\\{f(z+\\Delta z)-f(z)\\}/\\Delta z$ が近づけ方によらないこと = CR の関係式", y=1.02)
    save(fig, "cx-differentiability.svg")


# ---------------------------------------------------------------- figure 3


def fig_conformal():
    """CR の関係式の幾何的な意味: u と v の等位線は直交し、写像は角を保つ。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.2))

    ax = axes[0]
    xs = np.linspace(-1.6, 1.6, 400)
    ys = np.linspace(-1.6, 1.6, 400)
    X, Y = np.meshgrid(xs, ys)
    U = X**2 - Y**2  # u = Re(z^2)
    V = 2 * X * Y  # v = Im(z^2)
    levels = np.arange(-2.4, 2.5, 0.5)
    ax.contour(X, Y, U, levels=levels, colors=BLUE, linewidths=1.0, linestyles="solid")
    ax.contour(X, Y, V, levels=levels, colors=ORANGE, linewidths=1.0, linestyles="solid")
    plane(ax, (-1.6, 1.6), (-1.6, 1.6), re=None, im=None)
    ax.set_title("$f(z)=z^2$ の $u,v$ の等位線")
    ax.legend(
        handles=[
            Line2D([], [], color=BLUE, label="$u(x,y) = \\text{const}$"),
            Line2D([], [], color=ORANGE, label="$v(x,y) = \\text{const}$"),
        ],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=2,
        fontsize=9.5,
    )

    ax = axes[1]
    # z 平面の直交格子を w = z^2 で写す
    grid = np.arange(0.15, 1.06, 0.15)
    t = np.linspace(0.15, 1.05, 200)
    for c in grid:
        cplot(ax, (c + 1j * t) ** 2, color=BLUE, lw=1.0)
        cplot(ax, (t + 1j * c) ** 2, color=ORANGE, lw=1.0)
    p = (0.75 + 0.75j) ** 2
    cscatter(ax, p, s=30, color=INK, zorder=4)
    ax.annotate(
        "格子の直角は写した後も直角",
        xy=(p.real, p.imag),
        xytext=(-1.15, 1.9),
        fontsize=9,
        color=GRAY,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    plane(ax, (-1.3, 1.3), (-0.15, 2.4), re=None, im=None)
    ax.set_title("直交格子の像 $w = z^2$")
    fig.text(
        0.5,
        -0.02,
        "CR の関係式は $\\nabla u \\perp \\nabla v$ と同値 — 正則関数は角度を保つ (等角写像)",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "cx-conformal.svg")


# ---------------------------------------------------------------- figure 4


def fig_contour_integral():
    """複素積分は f(z_k)Δz_k という複素数の足し算。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0))

    def path(t):  # 0 から 1+i へ向かう放物線状の積分路
        return t + 1j * t**2

    f = lambda w: w**2 + 0.5

    ax = axes[0]
    ts = np.linspace(0, 1, 300)
    cplot(ax, path(ts), color=BLUE, lw=1.8)
    nodes = path(np.linspace(0, 1, 9))
    cscatter(ax, nodes, s=24, color=BLUE, zorder=3)
    for a, b in zip(nodes[:-1], nodes[1:]):
        carrow(ax, a, b, color=ORANGE, lw=1.1)
    cscatter(ax, [nodes[0], nodes[-1]], s=46, color=INK, zorder=4)
    ax.text(-0.13, -0.02, "$z(a)$", fontsize=10)
    ax.text(nodes[-1].real - 0.1, nodes[-1].imag + 0.07, "$z(b)$", fontsize=10)
    ax.text(0.62, 0.2, "$\\Delta z_k$", color=ORANGE, fontsize=10)
    ax.text(-0.2, 1.02, "$C:\\ z(t) = x(t) + iy(t)$", color=BLUE, fontsize=10)
    plane(ax, (-0.25, 1.3), (-0.25, 1.2))
    ax.set_title("積分路 $C$ を細かく刻む")

    ax = axes[1]
    for n, color, alpha, lw in ((8, LIGHT, 1.0, 1.2), (24, GREEN, 0.9, 1.2), (400, BLUE, 1.0, 1.8)):
        _, partial = contour_sum(f, path, n=n)
        cplot(ax, partial, color=color, lw=lw, alpha=alpha, marker="o" if n <= 24 else None, ms=3)
    exact = partial[-1]
    cscatter(ax, exact, s=70, marker="*", color=ORANGE, zorder=4)
    ax.text(
        exact.real - 0.05,
        exact.imag + 0.08,
        f"$\\int_C f(z)dz = {exact.real:.2f}{exact.imag:+.2f}i$",
        fontsize=10,
        color=ORANGE,
        ha="center",
    )
    plane(ax, (-0.75, 0.95), (-0.2, 1.5))
    ax.legend(
        handles=[
            Line2D([], [], color=LIGHT, marker="o", ms=3, label="$n=8$"),
            Line2D([], [], color=GREEN, marker="o", ms=3, label="$n=24$"),
            Line2D([], [], color=BLUE, label="$n\\to\\infty$"),
        ],
        loc="lower left",
        fontsize=9,
        borderpad=0.1,
    )
    ax.set_title("部分和 $f(z_k)\\Delta z_k$ の足し上げ")
    fig.suptitle("複素積分は「値 $\\times$ 微小変位」を複素平面上で足し上げたもの", y=1.02)
    save(fig, "cx-contour-integral.svg")


# ---------------------------------------------------------------- figure 5


def fig_cauchy_theorem():
    """コーシーの積分定理: 内部に特異点がなければ一周して 0 に戻る。"""
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 6.6))

    circle = lambda t: 1.0 * np.exp(2j * math.pi * t) + (0.35 + 0.15j)

    cases = (
        (lambda w: w**2, "$f(z) = z^2$ — $C$ の内部で正則", None),
        (lambda w: 1 / w, "$f(z) = 1/z$ — $z=0$ が特異点", 0j),
    )

    for row, (f, title, pole) in enumerate(cases):
        ax = axes[row, 0]
        ts = np.linspace(0, 1, 400)
        zs = circle(ts)
        cplot(ax, zs, color=BLUE, lw=1.8)
        ax.fill(np.real(zs), np.imag(zs), color=BLUE, alpha=0.06)
        for t in (0.08, 0.33, 0.58, 0.83):  # 進む向きを示す矢印
            a, b = circle(t), circle(t + 0.02)
            carrow(ax, a, b, color=BLUE, lw=1.4)
        if pole is not None:
            cscatter(ax, pole, s=90, marker="x", color=ORANGE, linewidths=2.0, zorder=4)
            ax.text(pole.real + 0.08, pole.imag + 0.08, "特異点", color=ORANGE, fontsize=9.5)
        ax.text(1.05, 1.0, "$C$", color=BLUE, fontsize=11)
        plane(ax, (-1.1, 1.7), (-1.2, 1.5))
        ax.set_title(title, fontsize=11)

        ax = axes[row, 1]
        _, partial = contour_sum(f, circle, n=2000)
        cplot(ax, partial, color=GREEN, lw=1.6)
        cscatter(ax, partial[0], s=44, color=INK, zorder=4)
        end = partial[-1]
        cscatter(ax, end, s=80, marker="*", color=ORANGE, zorder=4)
        if pole is None:
            lim = 1.9
            plane(ax, (-lim, lim), (-lim, lim))
            ax.text(
                -1.8,
                -1.6,
                "出発点に戻る $\\Rightarrow\\ \\oint_C f(z)dz = 0$",
                fontsize=10,
                color=ORANGE,
            )
        else:
            plane(ax, (-3.4, 3.4), (-1.2, 7.6))
            ax.text(
                -3.2,
                6.6,
                f"$\\oint_C f(z)dz = 2\\pi i \\approx {end.imag:.2f}i$",
                fontsize=10,
                color=ORANGE,
            )
        ax.set_title("部分和の軌跡", fontsize=11)

    fig.suptitle("同じ形の周回積分でも、内部の特異点の有無で結果が変わる", y=0.98)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    save(fig, "cx-cauchy-theorem.svg")


# ---------------------------------------------------------------- figure 6


def fig_path_deformation():
    """積分路の変形 I (単連結) と II (環状領域)。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))

    ax = axes[0]
    start, goal = -1.1 - 0.5j, 1.2 + 0.7j
    f = lambda w: w**2 + 1
    ax.add_patch(
        plt.Circle((0.05, 0.05), 1.75, color=GREEN, alpha=0.07, zorder=0)
    )
    ax.text(-1.65, 1.35, "単連結領域 $D$ (正則)", color=GREEN, fontsize=9.5)
    for bend, color, label in ((1.15, BLUE, "$C_1$"), (-0.95, ORANGE, "$C_2$")):
        t = np.linspace(0, 1, 200)
        mid = (start + goal) / 2 + 1j * bend * (goal - start) / abs(goal - start)
        curve = (1 - t) ** 2 * start + 2 * (1 - t) * t * mid + t**2 * goal
        cplot(ax, curve, color=color, lw=1.8)
        value = contour_sum(f, lambda s: (1 - s) ** 2 * start + 2 * (1 - s) * s * mid + s**2 * goal)[1][-1]
        k = curve[len(curve) // 2]
        ax.text(k.real - 0.15, k.imag + (0.12 if bend > 0 else -0.28), label, color=color, fontsize=11)
        ax.text(
            -1.75,
            -1.35 if bend > 0 else -1.65,
            f"{label} 上: ${value.real:.2f}{value.imag:+.2f}i$",
            color=color,
            fontsize=9.5,
        )
    cscatter(ax, [start, goal], s=48, color=INK, zorder=4)
    ax.text(start.real - 0.05, start.imag - 0.28, "始点", fontsize=9.5)
    ax.text(goal.real - 0.2, goal.imag + 0.12, "終点", fontsize=9.5)
    plane(ax, (-1.95, 1.95), (-1.95, 1.75), re=None, im=None)
    ax.set_title("積分路の変形 I — 端点が同じなら等しい")

    ax = axes[1]
    outer, inner = 1.7, 0.75
    ax.add_patch(plt.Circle((0, 0), outer, color=GREEN, alpha=0.09, zorder=0))
    ax.add_patch(plt.Circle((0, 0), inner, color="white", zorder=0))
    ax.add_patch(plt.Circle((0, 0), inner, color=GREEN, alpha=0.0, zorder=0))
    for radius, color, label in ((outer, BLUE, "$C_1$"), (inner, ORANGE, "$C_2$")):
        ts = np.linspace(0, 1, 300)
        zs = radius * np.exp(2j * math.pi * ts)
        cplot(ax, zs, color=color, lw=1.8)
        value = contour_sum(lambda w: 1 / w, lambda s: radius * np.exp(2j * math.pi * s), n=3000)[1][-1]
        ax.text(radius * 0.72, radius * 0.72, label, color=color, fontsize=11)
        ax.text(
            -2.05,
            -1.95 if radius == outer else -2.25,
            f"{label} 上: $\\oint f(z)dz \\approx {value.imag:.2f}i$",
            color=color,
            fontsize=9.5,
        )
    for angle in np.linspace(0, 2 * math.pi, 8, endpoint=False):  # 変形の向き
        a = outer * np.exp(1j * angle) * 0.96
        b = inner * np.exp(1j * angle) * 1.08
        carrow(ax, a, b, color=LIGHT, lw=1.0)
    cscatter(ax, 0j, s=90, marker="x", color=INK, linewidths=2.0, zorder=4)
    ax.text(0.08, -0.32, "特異点", fontsize=9.5)
    ax.text(-2.05, 1.85, "環状領域 (正則)", color=GREEN, fontsize=9.5)
    plane(ax, (-2.1, 2.1), (-2.1, 2.1), re=None, im=None)
    ax.set_title("積分路の変形 II — 穴を囲む限り等しい")
    save(fig, "cx-path-deformation.svg")


# ---------------------------------------------------------------- figure 7


def fig_cauchy_formula():
    """コーシーの積分公式: 周囲の値の平均が中心の値になる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))
    z0 = 0.3 + 0.2j
    f = lambda w: w**3 - 1.2 * w + 0.8

    ax = axes[0]
    ts = np.linspace(0, 1, 300)
    circle = z0 + 0.95 * np.exp(2j * math.pi * ts)
    cplot(ax, circle, color=BLUE, lw=1.8)
    marks = z0 + 0.95 * np.exp(2j * math.pi * np.linspace(0, 1, 12, endpoint=False))
    cscatter(ax, marks, s=26, color=BLUE, zorder=3)
    for m in marks:
        carrow(ax, m, z0 + (m - z0) * 0.16, color=LIGHT, lw=0.9)
    cscatter(ax, z0, s=52, color=ORANGE, zorder=4)
    ax.text(z0.real + 0.08, z0.imag - 0.02, "$z$", color=ORANGE, fontsize=11)
    ax.text(marks[1].real + 0.05, marks[1].imag + 0.05, "$\\zeta$", color=BLUE, fontsize=11)
    ax.text(-0.95, 1.28, "$C$", color=BLUE, fontsize=11)
    plane(ax, (-1.15, 1.65), (-1.2, 1.5))
    ax.set_title("境界 $C$ 上の値だけを使う")

    ax = axes[1]
    values = f(circle)
    cplot(ax, values, color=BLUE, lw=1.6)
    centre = f(z0)
    # 平均値の性質: 円周上の f の平均がちょうど中心の値になる
    mean = values[:-1].mean()
    cscatter(ax, mean, s=170, marker="*", color=GREEN, zorder=4)
    cscatter(ax, centre, s=26, color=ORANGE, zorder=5)
    ax.legend(
        handles=[
            Line2D([], [], color=GREEN, marker="*", ms=11, ls="none", label="$f(\\zeta)$ の平均"),
            Line2D([], [], color=ORANGE, marker="o", ms=5, ls="none", label="中心の値 $f(z)$"),
        ],
        loc="lower left",
        fontsize=9,
        borderpad=0.1,
    )
    for m in f(marks):
        carrow(ax, m, m + (centre - m) * 0.12, color=LIGHT, lw=0.9)
    ax.annotate(
        f"$\\dfrac{{1}}{{2\\pi i}}\\oint_C \\dfrac{{f(\\zeta)}}{{\\zeta - z}}d\\zeta"
        f" = f(z) \\approx {centre.real:.2f}{centre.imag:+.2f}i$",
        xy=(centre.real, centre.imag),
        xytext=(-2.5, 2.2),
        fontsize=10,
        color=ORANGE,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    ax.text(values[40].real, values[40].imag + 0.25, "$f(\\zeta)$ の描く曲線", color=BLUE, fontsize=9.5)
    plane(ax, (-2.9, 3.4), (-2.8, 3.1))
    ax.set_title("その値の「平均」が中心の値になる")
    save(fig, "cx-cauchy-formula.svg")


# ---------------------------------------------------------------- figure 8


def fig_taylor():
    """テイラー展開の収束円は最も近い特異点までの距離で決まる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0))

    alpha = 0.0
    f = lambda w: 1 / (1 - w)

    def partial_sum(w, N):
        return sum(w**n for n in range(N + 1))

    ax = axes[0]
    g = np.linspace(-1.9, 1.9, 400)
    X, Y = np.meshgrid(g, g)
    Z = X + 1j * Y
    err = np.abs(f(Z) - partial_sum(Z, 12))
    im = ax.imshow(
        np.log10(np.clip(err, 1e-6, 1e6)),
        extent=(-1.9, 1.9, -1.9, 1.9),
        origin="lower",
        cmap="magma_r",
        vmin=-6,
        vmax=3,
    )
    ax.add_patch(Circle((0, 0), 1.0, fill=False, color=GREEN, lw=1.8, ls="--"))
    cscatter(ax, 1 + 0j, s=90, marker="x", color=GREEN, linewidths=2.2, zorder=4)
    ax.text(1.05, 0.12, "$z=1$", color=GREEN, fontsize=9.5)
    ax.text(0.15, -1.72, "$\\times$ は特異点", color=GREEN, fontsize=9.5)
    cscatter(ax, alpha, s=40, color=GREEN, zorder=4)
    ax.text(-0.32, -0.22, "$\\alpha$", color=GREEN, fontsize=11)
    ax.text(-1.82, 1.6, "収束円 $|z-\\alpha| < R$", color=GREEN, fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("$\\log_{10}|f(z) - S_{12}(z)|$", fontsize=9)
    cbar.ax.tick_params(labelsize=8)
    ax.set_title("$f(z)=1/(1-z)$ を $\\alpha=0$ で展開")

    ax = axes[1]
    ts = np.linspace(0, 1.6, 400)
    zs = ts * np.exp(1j * 0.6)  # 原点から放射状に伸びる半直線上で誤差を見る
    for N, color in ((2, GREEN), (5, BLUE), (12, PURPLE)):
        ax.semilogy(ts, np.abs(f(zs) - partial_sum(zs, N)), color=color, lw=1.5, label=f"$N={N}$")
    ax.axvline(1.0, color=ORANGE, lw=1.4, ls="--")
    ax.text(1.04, 1e-6, "$|z-\\alpha| = R$", color=ORANGE, fontsize=9.5, rotation=90, va="bottom")
    ax.set_xlabel("$|z - \\alpha|$")
    ax.set_ylabel("$|f(z) - S_N(z)|$")
    ax.set_ylim(1e-8, 1e4)
    ax.set_title("収束円の内側でのみ $N$ とともに誤差が減る")
    ax.legend(fontsize=9.5)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    save(fig, "cx-taylor.svg")


# ---------------------------------------------------------------- figure 9


def fig_laurent():
    """ローラン展開: 展開できる環状領域と主要部。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))

    ax = axes[0]
    lim = 3.1
    ax.add_patch(Circle((0, 0), lim, color=PURPLE, alpha=0.08))
    ax.add_patch(Circle((0, 0), 2.0, color=BLUE, alpha=0.12))
    ax.add_patch(Circle((0, 0), 2.0, fill=False, color=BLUE, lw=1.4, ls="--"))
    ax.add_patch(Circle((0, 0), 0.0001, color="white"))
    cscatter(ax, [0j, 2 + 0j], s=90, marker="x", color=ORANGE, linewidths=2.0, zorder=5)
    ax.text(0.08, -0.34, "$z=0$", color=ORANGE, fontsize=9.5)
    ax.text(2.05, -0.34, "$z=2$", color=ORANGE, fontsize=9.5)
    ts = np.linspace(0, 1, 200)
    cplot(ax, 1.35 * np.exp(2j * math.pi * ts), color=GREEN, lw=1.6)
    ax.text(0.85, 1.0, "$C$", color=GREEN, fontsize=11)
    ax.text(-1.15, 1.72, "$0 < |z| < 2$", color=BLUE, fontsize=10)
    ax.text(-1.35, 2.55, "$|z| > 2$ では別の展開", color=PURPLE, fontsize=9.5)
    plane(ax, (-lim, lim), (-lim, lim), re=None, im=None)
    ax.set_title("展開できる環状領域は特異点で区切られる")

    ax = axes[1]
    # f(z) = 1/(z(z-2)) を 0 < |z| < 2 で展開すると c_n = -1/2^{n+2} (n >= -1)
    ns = np.arange(-3, 5)
    cs = np.array([0.0 if n < -1 else -1 / 2 ** (n + 2) for n in ns])
    colors = [ORANGE if n < 0 else BLUE for n in ns]
    ax.bar(ns, cs, width=0.6, color=colors, edgecolor="white")
    ax.axvspan(-3.6, -0.4, color=ORANGE, alpha=0.07)
    ax.axhline(0, color=LIGHT, lw=1.0)
    ax.text(-2.0, 0.06, "主要部", color=ORANGE, fontsize=10, ha="center")
    ax.text(2.0, 0.06, "正べきの部分", color=BLUE, fontsize=10, ha="center")
    ax.annotate(
        "$c_{-1} = \\text{Res}(f, 0)$",
        xy=(-1, -0.5),
        xytext=(-0.6, -0.42),
        fontsize=10,
        color=ORANGE,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    ax.set_xticks(ns)
    ax.set_xlabel("$n$")
    ax.set_ylabel("$c_n$")
    ax.set_ylim(-0.62, 0.16)
    ax.set_title("$f(z) = \\dfrac{1}{z(z-2)}$ の係数 $c_n$")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    save(fig, "cx-laurent.svg")


# ---------------------------------------------------------------- figure 10


def fig_singularities():
    """孤立特異点の 3 分類を |f(z)| の様子で見る。"""
    fig, axes = plt.subplots(1, 3, figsize=(8.8, 3.6))

    lim = 1.0
    g = np.linspace(-lim, lim, 500)
    X, Y = np.meshgrid(g, g)
    Z = X + 1j * Y
    Z = np.where(np.abs(Z) < 1e-3, 1e-3, Z)  # 原点での 0 除算を避ける

    cases = (
        (np.sin(Z) / Z, "$\\dfrac{\\sin z}{z}$", "可除特異点\n主要部なし"),
        (1 / Z**2, "$\\dfrac{1}{z^2}$", "$2$ 位の極\n主要部が有限個"),
        (np.exp(1 / Z), "$e^{1/z}$", "真性特異点\n主要部が無限個"),
    )

    for ax, (values, title, note) in zip(axes, cases):
        m = ax.imshow(
            np.log10(np.clip(np.abs(values), 1e-4, 1e4)),
            extent=(-lim, lim, -lim, lim),
            origin="lower",
            cmap="magma",
            vmin=-4,
            vmax=4,
        )
        cscatter(ax, 0j, s=60, marker="x", color="white", linewidths=1.6, zorder=3)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=12)
        ax.text(
            0.5,
            -0.04,
            note,
            transform=ax.transAxes,
            ha="center",
            va="top",
            fontsize=9.5,
            color=GRAY,
            linespacing=1.5,
        )

    cbar = fig.colorbar(m, ax=axes, fraction=0.025, pad=0.02)
    cbar.set_label("$\\log_{10}|f(z)|$", fontsize=9)
    cbar.ax.tick_params(labelsize=8)
    fig.suptitle("$z=0$ に近づけたときの $|f(z)|$ のふるまい", y=1.03)
    save(fig, "cx-singularities.svg")


# ---------------------------------------------------------------- figure 11


def fig_residue():
    """留数定理: 周回積分は特異点まわりの小円に分解できる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))

    poles = np.array([-0.9 + 0.3j, 0.8 + 0.7j, 0.5 - 0.8j])
    residues = np.array([0.5, -1.0, 0.75])
    f = lambda w: sum(r / (w - p) for p, r in zip(poles, residues))

    ax = axes[0]
    ts = np.linspace(0, 1, 400)
    big = 1.85 * np.exp(2j * math.pi * ts)
    cplot(ax, big, color=BLUE, lw=1.8)
    ax.fill(np.real(big), np.imag(big), color=BLUE, alpha=0.05)
    for t in (0.1, 0.35, 0.6, 0.85):
        carrow(ax, 1.85 * np.exp(2j * math.pi * t), 1.85 * np.exp(2j * math.pi * (t + 0.02)), color=BLUE, lw=1.4)
    for p, r in zip(poles, residues):
        small = p + 0.3 * np.exp(2j * math.pi * ts)
        cplot(ax, small, color=ORANGE, lw=1.4)
        carrow(ax, p + 0.3, p + 0.3 * np.exp(2j * math.pi * 0.03), color=ORANGE, lw=1.2)
        cscatter(ax, p, s=70, marker="x", color=ORANGE, linewidths=1.8, zorder=4)
        ax.text(p.real - 0.05, p.imag + 0.36, f"$\\text{{Res}} = {r:g}$", color=ORANGE, fontsize=9, ha="center")
    ax.text(1.15, 1.5, "$C$", color=BLUE, fontsize=11)
    plane(ax, (-2.1, 2.1), (-2.1, 2.1), re=None, im=None)
    ax.set_title("$C$ を特異点まわりの小円に分解する")

    ax = axes[1]
    _, partial = contour_sum(f, lambda t: 1.85 * np.exp(2j * math.pi * t), n=4000)
    cplot(ax, partial, color=GREEN, lw=1.6)
    end = partial[-1]
    cscatter(ax, partial[0], s=40, color=INK, zorder=4)
    cscatter(ax, end, s=90, marker="*", color=ORANGE, zorder=5)
    total = 2j * math.pi * residues.sum()
    ax.axhline(total.imag, color=ORANGE, lw=1.0, ls="--")
    ax.text(
        -1.9,
        total.imag + 0.15,
        f"$2\\pi i\\sum_k \\text{{Res}} = {total.imag:.2f}i$",
        color=ORANGE,
        fontsize=10,
    )
    ax.text(
        -1.9,
        -1.75,
        f"数値計算した周回積分\n${end.real:+.2f}{end.imag:+.2f}i$",
        color=GREEN,
        fontsize=10,
        linespacing=1.6,
    )
    plane(ax, (-2.0, 2.0), (-2.0, 2.0))
    ax.set_title("部分和は $2\\pi i \\times$ (留数の和) に到達する")
    fig.suptitle("周回積分の値は、囲まれた特異点の留数の和だけで決まる", y=1.02)
    save(fig, "cx-residue.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_de_moivre()
    fig_differentiability()
    fig_conformal()
    fig_contour_integral()
    fig_cauchy_theorem()
    fig_path_deformation()
    fig_cauchy_formula()
    fig_taylor()
    fig_laurent()
    fig_singularities()
    fig_residue()
