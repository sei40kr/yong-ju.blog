"""content/posts/mathematical-analysis.mdx の図を生成する。

出力先は public/img/ana-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-analysis-figures.py
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Arc, Circle, Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#059669"
PURPLE = "#7c3aed"
PINK = "#db2777"
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


def despine(ax, sides=("top", "right")):
    for side in sides:
        ax.spines[side].set_visible(False)


def axes_through_origin(ax, xlim, ylim, equal=True):
    ax.axhline(0, color=LIGHT, lw=1.0, zorder=0)
    ax.axvline(0, color=LIGHT, lw=1.0, zorder=0)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(False)


# ---------------------------------------------------------------- figure 1


def fig_taylor():
    """テイラー展開は展開の中心の近くから一致していく。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))

    def taylor_sin(x, n_terms):
        # sin の展開は奇数次のみ: x - x^3/3! + x^5/5! - ...
        out = np.zeros_like(x)
        for k in range(n_terms):
            out = out + (-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1)
        return out

    xs = np.linspace(-8, 8, 800)
    ax = axes[0]
    ax.plot(xs, np.sin(xs), color=INK, lw=2.0, label="$f(x)=\\sin x$", zorder=5)
    for terms, color in ((1, GREEN), (2, BLUE), (3, PURPLE), (5, PINK)):
        ax.plot(
            xs,
            taylor_sin(xs, terms),
            color=color,
            lw=1.3,
            label=f"$N={2 * terms - 1}$ 次まで",
        )
    ax.scatter([0], [0], s=40, color=ORANGE, zorder=6)
    ax.text(0.35, -1.05, "展開の中心 $a=0$", color=ORANGE, fontsize=9.5)
    ax.set_ylim(-2.4, 2.4)
    ax.set_xlabel("$x$")
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.set_title("項を増やすほど遠くまで一致する")
    ax.legend(fontsize=8.5, ncol=2, loc="upper center")
    despine(ax)

    ax = axes[1]
    xs = np.linspace(0.05, 8, 500)
    for terms, color in ((1, GREEN), (2, BLUE), (3, PURPLE), (5, PINK)):
        ax.semilogy(
            xs,
            np.abs(np.sin(xs) - taylor_sin(xs, terms)),
            color=color,
            lw=1.4,
            label=f"$N={2 * terms - 1}$",
        )
    ax.set_ylim(1e-12, 1e3)
    ax.set_xlabel("$|x-a|$")
    ax.set_ylabel("誤差 $|f(x)-S_N(x)|$")
    ax.set_title("中心から離れるほど誤差が急に増える")
    ax.legend(fontsize=9, ncol=2)
    despine(ax)
    fig.tight_layout()
    save(fig, "ana-taylor.svg")


# ---------------------------------------------------------------- figure 2


def fig_euler():
    """オイラーの公式と、指数関数の級数が単位円上に収束する様子。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2))

    theta = 1.15
    ax = axes[0]
    ts = np.linspace(0, 2 * math.pi, 400)
    ax.plot(np.cos(ts), np.sin(ts), color=LIGHT, lw=1.4)
    z = np.exp(1j * theta)
    ax.annotate(
        "",
        xy=(z.real, z.imag),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.8),
    )
    ax.plot([z.real, z.real], [0, z.imag], color=ORANGE, lw=1.4, ls=":")
    ax.plot([0, z.real], [z.imag, z.imag], color=GREEN, lw=1.4, ls=":")
    ax.scatter([z.real], [z.imag], s=44, color=BLUE, zorder=4)
    ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=math.degrees(theta), color=PURPLE, lw=1.4))
    ax.text(0.33, 0.12, "$y$", color=PURPLE, fontsize=11)
    ax.text(z.real + 0.04, z.imag + 0.06, "$e^{iy}$", color=BLUE, fontsize=12)
    ax.text(z.real / 2 - 0.06, -0.16, "$\\cos y$", color=ORANGE, fontsize=10, ha="center")
    ax.text(-0.1, z.imag, "$\\sin y$", color=GREEN, fontsize=10, ha="right", va="center")
    ax.text(-1.25, 1.15, "$|e^{iy}|=1$", color=GRAY, fontsize=10)
    axes_through_origin(ax, (-1.35, 1.35), (-1.35, 1.35))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("$e^{iy}$ は単位円上の点")

    ax = axes[1]
    y = 2.4
    terms = np.array([(1j * y) ** n / math.factorial(n) for n in range(14)])
    partial = np.cumsum(terms)
    ax.plot(np.cos(ts), np.sin(ts), color=LIGHT, lw=1.2)
    ax.plot(partial.real, partial.imag, color=BLUE, lw=1.2, marker="o", ms=3.4, zorder=3)
    for k in range(4):
        ax.annotate(
            "",
            xy=(partial[k + 1].real, partial[k + 1].imag),
            xytext=(partial[k].real, partial[k].imag),
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.2),
        )
    target = np.exp(1j * y)
    ax.scatter([target.real], [target.imag], s=90, marker="*", color=PURPLE, zorder=5)
    ax.text(target.real - 0.1, target.imag + 0.18, "$e^{iy}$", color=PURPLE, fontsize=11)
    ax.scatter([1], [0], s=36, color=INK, zorder=5)
    ax.text(1.06, -0.24, "$n=0$ の項 $1$", color=INK, fontsize=9.5, ha="right", va="top")
    ax.text(
        -3.2,
        -1.9,
        "$\\sum_{n=0}^{N}\\frac{(iy)^n}{n!}$ の部分和 ($y=2.4$)",
        color=GRAY,
        fontsize=10,
    )
    axes_through_origin(ax, (-3.3, 1.9), (-2.1, 2.9))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("級数は $\\cos y + i\\sin y$ に収束する")
    save(fig, "ana-euler.svg")


# ---------------------------------------------------------------- figure 3


def fig_epsilon_delta():
    """ε-δ 論法。どんな ε に対しても δ が取れるか。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0))
    a = 1.0

    def draw_bands(ax, f, eps, delta, color):
        ax.axhspan(f(a) - eps, f(a) + eps, color=ORANGE, alpha=0.10, zorder=0)
        ax.axvspan(a - delta, a + delta, color=BLUE, alpha=0.10, zorder=0)
        ax.add_patch(
            Rectangle(
                (a - delta, f(a) - eps),
                2 * delta,
                2 * eps,
                fill=False,
                edgecolor=color,
                lw=1.4,
                zorder=3,
            )
        )

    ax = axes[0]
    f = lambda x: 0.35 * x**3 + 0.6 * x + 0.4
    xs = np.linspace(0, 2, 400)
    ax.plot(xs, f(xs), color=INK, lw=1.8, zorder=4)
    for eps, delta, color in ((0.55, 0.35, ORANGE), (0.22, 0.14, PURPLE)):
        draw_bands(ax, f, eps, delta, color)
    ax.scatter([a], [f(a)], s=44, color=BLUE, zorder=5)
    ax.text(a + 0.04, f(a) - 0.28, "$(a, b)$", fontsize=10, color=BLUE)
    ax.annotate(
        "$\\varepsilon$ を小さくしても\n対応する $\\delta$ が取れる",
        xy=(a + 0.14, f(a) + 0.22),
        xytext=(1.3, 0.55),
        fontsize=9.5,
        color=GRAY,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    ax.text(0.04, f(a) + 0.62, "$b+\\varepsilon$", fontsize=9.5, color=ORANGE)
    ax.text(0.04, f(a) - 0.75, "$b-\\varepsilon$", fontsize=9.5, color=ORANGE)
    ax.text(a - 0.02, 0.06, "$a$", fontsize=10, color=BLUE, ha="center")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 3.4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("$x=a$ で連続")
    despine(ax)

    ax = axes[1]
    g = lambda x: np.where(x < a, 0.6 * x + 0.4, 0.6 * x + 1.4)
    for lo, hi in ((0.0, a), (a, 2.0)):
        xs = np.linspace(lo, hi, 200)
        ax.plot(xs, g(xs), color=INK, lw=1.8, zorder=4)
    b = 0.6 * a + 1.4
    eps = 0.4
    ax.axhspan(b - eps, b + eps, color=ORANGE, alpha=0.10, zorder=0)
    ax.axvspan(a - 0.3, a + 0.3, color=BLUE, alpha=0.10, zorder=0)
    ax.scatter([a], [b], s=44, color=BLUE, zorder=5)
    ax.scatter([a], [0.6 * a + 0.4], s=44, facecolors="white", edgecolors=INK, zorder=5)
    ax.annotate(
        "$\\delta$ をどれだけ小さくしても\n左側の値が $\\varepsilon$ の帯から外れる",
        xy=(a - 0.06, 0.6 * a + 0.4),
        xytext=(0.06, 0.55),
        fontsize=9.5,
        color=GRAY,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    ax.text(0.04, b + eps + 0.06, "$b+\\varepsilon$", fontsize=9.5, color=ORANGE)
    ax.text(0.04, b - eps - 0.2, "$b-\\varepsilon$", fontsize=9.5, color=ORANGE)
    ax.text(a - 0.02, 0.06, "$a$", fontsize=10, color=BLUE, ha="center")
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 3.4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("$x=a$ で連続でない")
    despine(ax)

    fig.suptitle("「どんな $\\varepsilon$ にも $\\delta$ が取れる」が連続の定義", y=1.02)
    save(fig, "ana-epsilon-delta.svg")


# ---------------------------------------------------------------- figure 4


def fig_gaussian():
    """ガウス積分。2 乗して極座標に移すと面積要素が r dr dθ になる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))

    ax = axes[0]
    xs = np.linspace(-3.4, 3.4, 500)
    ys = np.exp(-(xs**2))
    ax.plot(xs, ys, color=BLUE, lw=1.8)
    ax.fill_between(xs, ys, color=BLUE, alpha=0.15)
    ax.text(0, 0.42, "面積 $=\\sqrt{\\pi}$", ha="center", fontsize=11, color=BLUE)
    ax.set_xlabel("$x$")
    ax.set_title("$e^{-x^2}$ と $x$ 軸で挟まれる面積")
    ax.set_ylim(0, 1.15)
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.set_yticks([0, 0.5, 1])
    despine(ax)

    ax = axes[1]
    lim = 2.6
    g = np.linspace(-lim, lim, 400)
    X, Y = np.meshgrid(g, g)
    ax.imshow(
        np.exp(-(X**2 + Y**2)),
        extent=(-lim, lim, -lim, lim),
        origin="lower",
        cmap="Blues",
    )
    for r in np.arange(0.4, 2.5, 0.4):  # 極座標での輪切り
        ax.add_patch(Circle((0, 0), r, fill=False, color="white", lw=1.0, alpha=0.8))
    theta, dtheta = 0.75, 0.34
    for angle in (theta, theta + dtheta):
        ax.plot([0, lim * math.cos(angle)], [0, lim * math.sin(angle)], color=ORANGE, lw=1.0, alpha=0.7)
    # 微小な面積要素 (半径方向 dr、角度方向 r dθ) を塗って示す
    arc = np.linspace(theta, theta + dtheta, 30)
    r0, r1 = 1.2, 1.6
    ax.fill(
        np.concatenate([r0 * np.cos(arc), r1 * np.cos(arc[::-1])]),
        np.concatenate([r0 * np.sin(arc), r1 * np.sin(arc[::-1])]),
        color=ORANGE,
        alpha=0.8,
    )
    ax.annotate(
        "$rdrd\\theta$",
        xy=(1.4 * math.cos(theta + dtheta / 2), 1.4 * math.sin(theta + dtheta / 2)),
        xytext=(0.55, 2.1),
        fontsize=10,
        color=ORANGE,
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9),
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_title("$I^2=\\iint e^{-(x^2+y^2)}dxdy=\\pi$", fontsize=11)
    fig.tight_layout()
    save(fig, "ana-gaussian.svg")


# ---------------------------------------------------------------- figure 5


def fig_hyperbolic():
    """双曲線関数は「円」を「双曲線」に置き換えたもの。"""
    fig, axes = plt.subplots(1, 3, figsize=(8.8, 3.6))
    t = 1.05

    ax = axes[0]
    ts = np.linspace(0, 2 * math.pi, 400)
    ax.plot(np.cos(ts), np.sin(ts), color=LIGHT, lw=1.4)
    sector = np.linspace(0, t, 60)
    ax.fill(
        np.concatenate([[0], np.cos(sector)]),
        np.concatenate([[0], np.sin(sector)]),
        color=BLUE,
        alpha=0.2,
    )
    ax.plot([0, math.cos(t)], [0, math.sin(t)], color=BLUE, lw=1.4)
    ax.scatter([math.cos(t)], [math.sin(t)], s=36, color=BLUE, zorder=4)
    ax.text(math.cos(t) + 0.06, math.sin(t) + 0.06, "$(\\cos t, \\sin t)$", fontsize=9.5, color=BLUE)
    ax.text(0.28, 0.18, "面積 $t/2$", fontsize=9, color=BLUE)
    axes_through_origin(ax, (-1.5, 1.9), (-1.5, 1.6))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("単位円 $x^2+y^2=1$", fontsize=11)

    ax = axes[1]
    us = np.linspace(-1.35, 1.35, 200)
    ax.plot(np.cosh(us), np.sinh(us), color=LIGHT, lw=1.4)
    ax.plot(-np.cosh(us), np.sinh(us), color=LIGHT, lw=1.0, alpha=0.5)
    sector = np.linspace(0, t, 60)
    ax.fill(
        np.concatenate([[0], np.cosh(sector)]),
        np.concatenate([[0], np.sinh(sector)]),
        color=ORANGE,
        alpha=0.2,
    )
    ax.plot([0, math.cosh(t)], [0, math.sinh(t)], color=ORANGE, lw=1.4)
    ax.scatter([math.cosh(t)], [math.sinh(t)], s=36, color=ORANGE, zorder=4)
    ax.text(math.cosh(t) - 1.5, math.sinh(t) + 0.2, "$(\\cosh t, \\sinh t)$", fontsize=9.5, color=ORANGE)
    ax.text(0.45, 0.2, "面積 $t/2$", fontsize=9, color=ORANGE)
    axes_through_origin(ax, (-2.3, 2.7), (-2.0, 2.1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("単位双曲線 $x^2-y^2=1$", fontsize=11)

    ax = axes[2]
    xs = np.linspace(-2.4, 2.4, 400)
    ax.plot(xs, np.cosh(xs), color=ORANGE, lw=1.6, label="$\\cosh x$")
    ax.plot(xs, np.sinh(xs), color=BLUE, lw=1.6, label="$\\sinh x$")
    ax.plot(xs, np.tanh(xs), color=GREEN, lw=1.6, label="$\\tanh x$")
    ax.plot(xs, np.exp(xs) / 2, color=GRAY, lw=1.0, ls="--", label="$e^{x}/2$")
    ax.plot(xs, -np.exp(-xs) / 2, color=GRAY, lw=1.0, ls=":", label="$-e^{-x}/2$")
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.set_ylim(-3.2, 3.6)
    ax.set_xlabel("$x$")
    ax.set_title("グラフ", fontsize=11)
    ax.legend(fontsize=8, ncol=2, loc="upper left")
    despine(ax)

    fig.suptitle("$\\cosh^2 t - \\sinh^2 t = 1$ — 三角関数と同じ形の関係が双曲線で成り立つ", y=1.03)
    fig.tight_layout()
    save(fig, "ana-hyperbolic.svg")


# ---------------------------------------------------------------- figure 6


def fig_lhopital():
    """ロピタルの定理。0/0 の比は接線の傾きの比に等しい。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))
    f = lambda x: x + np.sin(x)
    g = lambda x: x
    df, dg = 2.0, 1.0  # x=0 での微分係数

    ax = axes[0]
    xs = np.linspace(-1.2, 1.2, 400)
    ax.plot(xs, f(xs), color=BLUE, lw=1.8, label="$f(x)=x+\\sin x$")
    ax.plot(xs, g(xs), color=ORANGE, lw=1.8, label="$g(x)=x$")
    ax.plot(xs, df * xs, color=BLUE, lw=1.0, ls="--", alpha=0.8, label="$f'(0)x$")
    ax.plot(xs, dg * xs, color=ORANGE, lw=1.0, ls=":", alpha=0.8, label="$g'(0)x$")
    ax.scatter([0], [0], s=40, color=INK, zorder=5)
    ax.text(0.06, -0.42, "$x\\to0$ で\nどちらも $0$", fontsize=9.5, color=GRAY, linespacing=1.5)
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.axvline(0, color=LIGHT, lw=0.8)
    ax.set_xlabel("$x$")
    ax.set_ylim(-2.4, 2.4)
    ax.set_title("$a$ の近くでは接線で置き換えられる")
    ax.legend(fontsize=8.5, ncol=2, loc="upper left")
    despine(ax)

    ax = axes[1]
    xs = np.linspace(-1.2, 1.2, 400)
    xs = xs[np.abs(xs) > 1e-3]
    ax.plot(xs, f(xs) / g(xs), color=PURPLE, lw=1.8, label="$f(x)/g(x)$")
    ax.plot(xs, 1 + np.cos(xs), color=GREEN, lw=1.4, ls="--", label="$f'(x)/g'(x)$")
    ax.axhline(df / dg, color=ORANGE, lw=1.2, ls=":")
    ax.text(-1.15, df / dg + 0.06, "$f'(0)/g'(0) = 2$", color=ORANGE, fontsize=10)
    ax.axvline(0, color=LIGHT, lw=0.8)
    ax.set_xlabel("$x$")
    ax.set_ylim(1.2, 2.35)
    ax.set_title("比はどちらも同じ極限に近づく")
    ax.legend(fontsize=9, loc="lower center")
    despine(ax)
    fig.tight_layout()
    save(fig, "ana-lhopital.svg")


# ---------------------------------------------------------------- figure 7


def fig_fourier():
    """フーリエ級数展開。三角関数を足して矩形波を作る。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))

    xs = np.linspace(-math.pi, math.pi, 2000)
    square = np.sign(xs)

    ax = axes[0]
    ax.plot(xs, square, color=INK, lw=1.6, label="$f(x)$ (矩形波)")
    for n_max, color in ((1, GREEN), (3, BLUE), (9, PURPLE), (49, PINK)):
        partial = np.zeros_like(xs)
        for n in range(1, n_max + 1, 2):
            partial = partial + 4 / (n * math.pi) * np.sin(n * xs)
        ax.plot(xs, partial, color=color, lw=1.2, label=f"$n\\leq{n_max}$")
    ax.set_xticks([-math.pi, 0, math.pi])
    ax.set_xticklabels(["$-\\pi$", "$0$", "$\\pi$"])
    ax.set_ylim(-1.6, 1.9)
    ax.set_title("三角関数の重ね合わせ")
    ax.legend(fontsize=8.5, ncol=3, loc="upper center")
    despine(ax)

    ax = axes[1]
    ns = np.arange(1, 16)
    bs = np.array([4 / (n * math.pi) if n % 2 else 0.0 for n in ns])
    ax.bar(ns, bs, width=0.55, color=BLUE, alpha=0.85, edgecolor="white")
    ax.set_xticks(ns[::2])
    ax.set_xlabel("$n$")
    ax.set_ylabel("$b_n$")
    ax.set_title("フーリエ係数 $b_n$ (偶数次は $0$)")
    ax.text(
        4.4,
        1.05,
        "$b_n=\\dfrac{1}{\\pi}\\int_{-\\pi}^{\\pi}f(x)\\sin nx\\,dx$",
        fontsize=10,
        color=GRAY,
    )
    ax.set_ylim(0, 1.65)
    despine(ax)
    fig.tight_layout()
    save(fig, "ana-fourier.svg")


# ---------------------------------------------------------------- figure 8


def fig_orthogonality():
    """三角関数系の直交性。内積を総当たりで計算すると対角行列になる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2), gridspec_kw=dict(width_ratios=[1.15, 1]))

    xs = np.linspace(-math.pi, math.pi, 4000)
    basis = [("$1$", np.ones_like(xs))]
    for n in (1, 2, 3):
        basis.append((f"$\\cos {n}x$" if n > 1 else "$\\cos x$", np.cos(n * xs)))
        basis.append((f"$\\sin {n}x$" if n > 1 else "$\\sin x$", np.sin(n * xs)))
    labels = [name for name, _ in basis]
    gram = np.array([[np.trapezoid(u * v, xs) for _, v in basis] for _, u in basis])

    ax = axes[0]
    ax.imshow(np.abs(gram), cmap="Blues", vmin=0, vmax=7)
    for i in range(len(basis)):
        for j in range(len(basis)):
            value = gram[i, j]
            if abs(value) < 1e-6:
                text = "$0$"
            else:
                text = "$2\\pi$" if abs(value - 2 * math.pi) < 1e-3 else "$\\pi$"
            ax.text(
                j,
                i,
                text,
                ha="center",
                va="center",
                fontsize=9,
                color="white" if i == j else GRAY,
            )
    ax.set_xticks(range(len(basis)))
    ax.set_yticks(range(len(basis)))
    ax.set_xticklabels(labels, fontsize=9, rotation=45, ha="left")
    ax.set_yticklabels(labels, fontsize=9)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(length=0)
    ax.tick_params(which="minor", length=0)
    ax.set_xticks(np.arange(-0.5, len(basis), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(basis), 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.4)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("内積 $\\int_{-\\pi}^{\\pi}\\varphi_m\\varphi_n dx$", pad=42)

    ax = axes[1]
    prod = np.sin(2 * xs) * np.sin(3 * xs)
    ax.plot(xs, np.sin(2 * xs), color=BLUE, lw=1.2, alpha=0.5, label="$\\sin 2x$")
    ax.plot(xs, np.sin(3 * xs), color=ORANGE, lw=1.2, alpha=0.5, label="$\\sin 3x$")
    ax.plot(xs, prod, color=PURPLE, lw=1.6, label="$\\sin 2x \\cdot \\sin 3x$")
    ax.fill_between(xs, prod, where=prod > 0, color=PURPLE, alpha=0.2)
    ax.fill_between(xs, prod, where=prod < 0, color=PINK, alpha=0.2)
    ax.axhline(0, color=LIGHT, lw=0.8)
    ax.set_xticks([-math.pi, 0, math.pi])
    ax.set_xticklabels(["$-\\pi$", "$0$", "$\\pi$"])
    ax.set_ylim(-1.5, 1.9)
    ax.set_title("$m\\ne n$ では正負の面積が打ち消し合う")
    ax.legend(fontsize=8.5, ncol=3, loc="upper center")
    despine(ax)
    fig.tight_layout()
    save(fig, "ana-orthogonality.svg")


# ---------------------------------------------------------------- figure 9


def fig_sup_inf():
    """max/min は集合に入る必要があるが、sup/inf は入らなくてよい。"""
    fig, ax = plt.subplots(figsize=(8.2, 3.4))

    rows = (
        (1.0, "$A_1=[0,1)$", True, False),
        (0.0, "$A_2=(0,1]$", False, True),
    )
    for y, name, left_closed, right_closed in rows:
        ax.plot([0, 1], [y, y], color=BLUE, lw=4.0, alpha=0.35, solid_capstyle="butt")
        for x, closed in ((0.0, left_closed), (1.0, right_closed)):
            ax.scatter(
                [x],
                [y],
                s=70,
                facecolors=BLUE if closed else "white",
                edgecolors=BLUE,
                linewidths=1.6,
                zorder=4,
            )
        ax.text(-0.16, y, name, fontsize=11, ha="right", va="center")
        ax.text(
            0.0,
            y - 0.28,
            "$\\inf A=\\min A=0$" if left_closed else "$\\inf A=0$ (最小値なし)",
            fontsize=9.5,
            ha="center",
            color=GREEN if left_closed else ORANGE,
        )
        ax.text(
            1.0,
            y - 0.28,
            "$\\sup A=1$ (最大値なし)" if not right_closed else "$\\sup A=\\max A=1$",
            fontsize=9.5,
            ha="center",
            color=ORANGE if not right_closed else GREEN,
        )

    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(-0.55, 1.55)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["$0$", "$1$"])
    ax.set_yticks([])
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_title("端点が集合に入るかどうかで最大値・最小値の有無が変わる")
    ax.text(
        -0.5,
        1.35,
        "● は集合に含まれる点、○ は含まれない点",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "ana-sup-inf.svg")


# ---------------------------------------------------------------- figure 10


def fig_gamma():
    """ガンマ関数は階乗を実数へ延長したもの。"""
    fig, ax = plt.subplots(figsize=(7.4, 4.0))

    xs = np.linspace(0.16, 5.3, 600)
    ax.plot(xs, np.vectorize(math.gamma)(xs), color=BLUE, lw=1.8, label="$\\Gamma(s)$")
    ks = np.arange(1, 5)
    ax.scatter(ks, [math.gamma(k) for k in ks], s=44, color=ORANGE, zorder=4)
    for k in ks:
        ax.annotate(
            f"$\\Gamma({k})={math.factorial(k - 1)}$",
            xy=(k, math.gamma(k)),
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=9,
            color=ORANGE,
        )
    ax.scatter([0.5], [math.gamma(0.5)], s=70, marker="*", color=PURPLE, zorder=5)
    ax.annotate(
        "$\\Gamma(1/2)=\\sqrt{\\pi}$",
        xy=(0.5, math.gamma(0.5)),
        xytext=(0.75, 6.4),
        fontsize=10,
        color=PURPLE,
        arrowprops=dict(arrowstyle="->", color=PURPLE, lw=0.9),
    )
    ax.set_xlabel("$s$")
    ax.set_ylim(0, 15)
    ax.set_xlim(0, 5.4)
    ax.set_title("$\\Gamma(s)$ は正の整数で $(s-1)!$ を通る")
    ax.text(2.5, 12.4, "$\\Gamma(s)=(s-1)\\Gamma(s-1)$", fontsize=11, color=GRAY)
    despine(ax)
    save(fig, "ana-gamma.svg")


# ---------------------------------------------------------------- figure 11


def fig_lagrange():
    """ラグランジュの未定乗数法と KKT 条件。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.2))

    f = lambda x, y: (x - 0.2) ** 2 + 2 * (y - 0.1) ** 2
    g = np.linspace(-2.6, 2.6, 400)
    X, Y = np.meshgrid(g, g)

    ax = axes[0]
    ax.contour(X, Y, f(X, Y), levels=np.arange(0.5, 12, 1.2), colors=LIGHT, linewidths=1.0)
    # 制約 x + y = 2 の上で f を最小化する
    xs = np.linspace(-2.6, 2.6, 200)
    ax.plot(xs, 2 - xs, color=BLUE, lw=1.8)
    ax.text(-0.25, 2.25, "$g(\\mathbf{x})=0$", color=BLUE, fontsize=10)
    # 最小点: f を x+y=2 上で最小化 → 解析的に求める
    xopt = (2 * 2 + 0.2 - 0.1 * 1) / 3  # d/dx[(x-0.2)^2 + 2(2-x-0.1)^2] = 0
    xopt = (0.2 + 2 * (2 - 0.1)) / 3
    yopt = 2 - xopt
    ax.contour(X, Y, f(X, Y), levels=[f(xopt, yopt)], colors=[ORANGE], linewidths=1.8)
    ax.scatter([xopt], [yopt], s=54, color=ORANGE, zorder=5)
    ax.annotate(
        "",
        xy=(xopt + 0.5 * 2 * (xopt - 0.2) / 3, yopt + 0.5 * 4 * (yopt - 0.1) / 3),
        xytext=(xopt, yopt),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.6),
    )
    ax.annotate(
        "",
        xy=(xopt + 0.62, yopt + 0.62),
        xytext=(xopt, yopt),
        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.6),
    )
    ax.text(xopt - 0.1, yopt + 0.78, "$\\nabla g$", color=BLUE, fontsize=10, ha="right")
    ax.text(xopt + 0.72, yopt - 0.38, "$\\nabla f$", color=ORANGE, fontsize=10)
    ax.text(-2.5, -2.35, "接点では $\\nabla f = -\\lambda\\nabla g$ (勾配が平行)", fontsize=9.5, color=GRAY)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_title("等式制約 — 等高線と制約が接する点")
    for side in ax.spines.values():
        side.set_color(LIGHT)

    ax = axes[1]
    ax.contour(X, Y, f(X, Y), levels=np.arange(0.5, 12, 1.2), colors=LIGHT, linewidths=1.0)
    ax.add_patch(Circle((-1.35, -1.15), 1.1, color=GREEN, alpha=0.10))
    ax.add_patch(Circle((-1.35, -1.15), 1.1, fill=False, color=GREEN, lw=1.6))
    ax.text(-1.35, -1.15, "実行可能領域\n$h(\\mathbf{x})\\leq 0$", color=GREEN, fontsize=9.5, ha="center", va="center", linespacing=1.6)
    ax.scatter([0.2], [0.1], s=48, facecolors="white", edgecolors=GRAY, linewidths=1.4, zorder=4)
    ax.text(0.42, 0.1, "制約なしの最小点", fontsize=9, color=GRAY, va="center")
    # 実行可能領域の境界上で f が最小になる点を数値的に求める
    ts = np.linspace(0, 2 * math.pi, 2000)
    bx, by = -1.35 + 1.1 * np.cos(ts), -1.15 + 1.1 * np.sin(ts)
    k = int(np.argmin(f(bx, by)))
    ax.scatter([bx[k]], [by[k]], s=54, color=ORANGE, zorder=5)
    ax.contour(X, Y, f(X, Y), levels=[f(bx[k], by[k])], colors=[ORANGE], linewidths=1.8)
    ax.annotate(
        "$\\mu>0$ (制約が有効)",
        xy=(bx[k], by[k]),
        xytext=(-1.9, 1.75),
        fontsize=9.5,
        color=ORANGE,
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9),
    )
    ax.text(
        -2.55,
        -2.35,
        "最小点が内部にあれば $\\mu=0$ — これが相補性条件 $\\mu h(\\mathbf{x})=0$",
        fontsize=9.5,
        color=GRAY,
    )
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ax.set_title("不等式制約 — 有効な制約だけが効く")
    for side in ax.spines.values():
        side.set_color(LIGHT)
    save(fig, "ana-lagrange.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_taylor()
    fig_euler()
    fig_epsilon_delta()
    fig_gaussian()
    fig_hyperbolic()
    fig_lhopital()
    fig_fourier()
    fig_orthogonality()
    fig_sup_inf()
    fig_gamma()
    fig_lagrange()
