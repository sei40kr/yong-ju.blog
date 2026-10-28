"""content/posts/quantum-mechanics.mdx の図を生成する。

出力先は public/img/qm-*.svg。

井戸型ポテンシャルとトンネル効果の図は、記事中の式をそのまま数値的に解いて描く
(近似式や手描きではない)。単位は電子・nm・eV 系で揃えてある。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-quantum-mechanics-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
PURPLE = "#7c3aed"
GREEN = "#16a34a"
GRAY = "#6b7280"
INK = "#111827"
BAND = "#94a3b8"
FAINT = "#d1d5db"

# 物理定数 (SI)
H = 6.62607015e-34
HBAR = H / (2 * np.pi)
M_E = 9.1093837015e-31
M_N = 1.67492749804e-27
EV = 1.602176634e-19

# 電子・nm・eV 系: hbar^2 / (2 m_e) を eV*nm^2 で表した値
HB2_2M = HBAR**2 / (2 * M_E) / EV / 1e-18

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
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05, dpi=110)
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


def despine(ax, sides=("top", "right")):
    for side in sides:
        ax.spines[side].set_visible(False)


def bisect(f, lo, hi, iterations=200):
    """scipy を使わずに済ませるための二分法。f(lo) > 0 > f(hi) を仮定する。"""
    flo = f(lo)
    for _ in range(iterations):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- figure 1


def fig_de_broglie():
    """ド・ブロイ波長 lambda = h / p が運動量に反比例すること。"""
    fig, axes = plt.subplots(
        1, 2, figsize=(8.6, 3.9), gridspec_kw={"width_ratios": [1.0, 1.25]}
    )

    # 左: 運動量が大きいほど波長が短い
    ax = axes[0]
    x = np.linspace(0, 1, 800)
    for offset, lam, color, label in (
        (2.6, 0.5, BLUE, "運動量 $p$ が小さい"),
        (0.0, 0.2, ORANGE, "運動量 $p$ が大きい"),
    ):
        ax.plot(x, offset + np.sin(2 * np.pi * x / lam), color=color, lw=1.8)
        ax.axhline(offset, color=FAINT, lw=0.8, xmax=0.69, zorder=0)
        # 波長を両矢印で示す
        y = offset + 1.42
        ax.annotate(
            "",
            xy=(0.25 * lam + lam, y),
            xytext=(0.25 * lam, y),
            arrowprops=dict(
                arrowstyle="<->", color=INK, lw=1.2, shrinkA=0, shrinkB=0
            ),
        )
        ax.text(
            0.25 * lam + lam / 2,
            y + 0.1,
            r"$\lambda = h / p$",
            fontsize=11,
            ha="center",
            va="bottom",
        )
        ax.text(1.04, offset, label, fontsize=10, color=color, ha="left", va="center")

    ax.set_xlim(0, 1.45)
    ax.set_ylim(-1.5, 4.7)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_title("運動量が大きいほど波長は短い")
    despine(ax, ("top", "right", "left"))

    # 右: 実際の物体のド・ブロイ波長
    ax = axes[1]
    p = np.logspace(-29, 6, 400)
    ax.plot(p, H / p, color=INK, lw=1.8, zorder=3)

    for length, name in (
        (1e-10, "原子の大きさ $10^{-10}\\,$m"),
        (5e-7, "可視光の波長"),
    ):
        ax.axhline(length, color=BAND, lw=0.9, ls="--", zorder=1)
        ax.text(6e5, length * 2.2, name, fontsize=9, color=GRAY, ha="right")

    def momentum(mass, energy_ev=None, velocity=None):
        if energy_ev is not None:
            return np.sqrt(2 * mass * energy_ev * EV)
        return mass * velocity

    objects = [
        # ラベルは直線と重ならないよう、点から右上または左下へ逃がす
        ("電子 ($1\\,$eV)", momentum(M_E, energy_ev=1.0), BLUE, (18, 34), "left"),
        ("電子 ($100\\,$eV)", momentum(M_E, energy_ev=100.0), BLUE, (62, 26), "left"),
        ("熱中性子", momentum(M_N, energy_ev=0.025), PURPLE, (76, -4), "left"),
        ("野球ボール", momentum(0.145, velocity=40.0), ORANGE, (-10, 34), "center"),
        ("歩く人", momentum(60.0, velocity=1.0), ORANGE, (10, 76), "center"),
    ]
    for name, pv, color, offset, ha in objects:
        ax.scatter([pv], [H / pv], s=42, color=color, zorder=4, edgecolors="white")
        ax.annotate(
            name,
            xy=(pv, H / pv),
            xytext=offset,
            textcoords="offset points",
            fontsize=9.5,
            color=color,
            ha=ha,
            va="center",
            arrowprops=dict(arrowstyle="-", color=BAND, lw=0.8, shrinkB=4),
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-29, 1e6)
    ax.set_ylim(1e-37, 1e-1)
    ax.set_xticks([1e-28, 1e-22, 1e-16, 1e-10, 1e-4, 1e2])
    ax.set_yticks([1e-35, 1e-30, 1e-25, 1e-20, 1e-15, 1e-10, 1e-5])
    ax.set_xlabel("運動量 $p$ [kg m/s]")
    ax.set_ylabel("ド・ブロイ波長 $\\lambda$ [m]")
    ax.set_title("身のまわりの物体の波長は測りようがない")
    despine(ax)

    fig.tight_layout()
    save(fig, "qm-de-broglie.svg")


# ---------------------------------------------------------------- figure 2


def fig_uncertainty():
    """位置を絞るほど運動量が広がる (ガウス波束)。"""
    x = np.linspace(-6, 6, 300)
    p = np.linspace(-6, 6, 300)

    fig, axes = plt.subplots(2, 3, figsize=(8.6, 4.6), sharex="row")

    for col, (sx, title) in enumerate(
        (
            (0.35, "位置を強く絞る"),
            (1.0, "中間"),
            (2.8, "位置を絞らない"),
        )
    ):
        sp = 0.5 / sx  # hbar = 1 のとき、ガウス波束では sigma_x sigma_p = 1/2

        ax = axes[0, col]
        ax.plot(x, np.exp(-(x**2) / (2 * sx**2)), color=BLUE, lw=1.9)
        ax.fill_between(x, np.exp(-(x**2) / (2 * sx**2)), color=BLUE, alpha=0.12)
        ax.annotate(
            "",
            xy=(sx, 0.607),
            xytext=(-sx, 0.607),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1, shrinkA=0, shrinkB=0),
        )
        ax.text(0, 0.68, r"$\Delta x$", fontsize=11, ha="center", va="bottom")
        ax.set_title(title, fontsize=11)
        if col == 0:
            ax.set_ylabel("$|\\psi(x)|^2$")

        ax = axes[1, col]
        ax.plot(p, np.exp(-(p**2) / (2 * sp**2)), color=ORANGE, lw=1.9)
        ax.fill_between(p, np.exp(-(p**2) / (2 * sp**2)), color=ORANGE, alpha=0.12)
        ax.annotate(
            "",
            xy=(sp, 0.607),
            xytext=(-sp, 0.607),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1, shrinkA=0, shrinkB=0),
        )
        ax.text(0, 0.68, r"$\Delta p$", fontsize=11, ha="center", va="bottom")
        ax.set_xlabel("運動量 $p$" if col == 1 else "")
        if col == 0:
            ax.set_ylabel("$|\\phi(p)|^2$")

        for ax in (axes[0, col], axes[1, col]):
            ax.set_ylim(0, 1.28)
            ax.set_yticks([])
            ax.set_xticks([])
            despine(ax, ("top", "right", "left"))

    axes[0, 1].set_xlabel("位置 $x$", labelpad=2)
    axes[0, 1].xaxis.set_label_position("bottom")

    fig.suptitle(
        "位置の広がり $\\Delta x$ を狭めると運動量の広がり $\\Delta p$ は必ず広がり、"
        "積 $\\Delta x \\Delta p$ をいくらでも小さくすることはできない",
        fontsize=11.5,
        y=1.02,
    )
    fig.tight_layout()
    save(fig, "qm-uncertainty.svg")


# ---------------------------------------------------------------- figure 3


def fig_stationary_state():
    """定常状態では位相だけが回り、確率密度は動かない。"""
    a = 1.0
    x = np.linspace(-a, a, 400)
    # 無限に深い井戸型ポテンシャルの n = 1, 2 (どちらも規格化してある)
    phi1 = np.cos(np.pi * x / (2 * a)) / np.sqrt(a)
    phi2 = np.sin(np.pi * x / a) / np.sqrt(a)  # E_2 = 4 E_1

    fig, axes = plt.subplots(1, 3, figsize=(8.8, 3.6))
    times = np.linspace(0, 0.5, 5)  # 周期 T = 1 とした時刻 t / T
    alphas = (1.0, 0.78, 0.58, 0.42, 0.3)

    ax = axes[0]
    for t, alpha in zip(times, alphas):
        ax.plot(
            x,
            phi1 * np.cos(2 * np.pi * t),
            color=BLUE,
            lw=1.9 if t == 0 else 1.4,
            alpha=alpha,
            label=f"$t / T = {t:g}$",
        )
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.set_ylim(-1.75, 1.35)
    ax.set_title("$\\mathrm{Re}\\,\\psi(x, t)$ は振動する")
    ax.legend(fontsize=8.5, loc="lower center", ncol=3, columnspacing=0.8)

    ax = axes[1]
    ax.plot(x, phi1**2, color=PURPLE, lw=2.0)
    ax.fill_between(x, phi1**2, color=PURPLE, alpha=0.12)
    ax.text(
        0,
        1.55,
        "すべての $t$ で\n同じ曲線",
        fontsize=10,
        ha="center",
        va="center",
        color=PURPLE,
        linespacing=1.5,
    )
    ax.set_title("$|\\psi(x, t)|^2$ は動かない")

    ax = axes[2]
    # 参考: 固有状態の重ね合わせは定常状態ではない
    for t, alpha in zip(times, alphas):
        psi = (
            phi1 * np.exp(-2j * np.pi * t) + phi2 * np.exp(-2j * np.pi * 4 * t)
        ) / np.sqrt(2)
        ax.plot(x, np.abs(psi) ** 2, color=ORANGE, lw=1.6, alpha=alpha)
    ax.set_title("(参考) 重ね合わせは動く")

    for ax in axes[1:]:
        ax.set_ylim(-0.25, 2.4)  # 2 枚は同じ縦軸で比べられるようにする

    for ax in axes:
        ax.set_xlim(-a, a)
        ax.set_xticks([-a, 0, a])
        ax.set_xticklabels(["$-a$", "$0$", "$a$"])
        ax.set_yticks([])
        despine(ax, ("top", "right", "left"))

    fig.suptitle(
        "定常状態 $\\psi = \\phi(x) C e^{-i E t / \\hbar}$ では"
        "位相だけが回り、確率密度は時間に依存しない",
        fontsize=11.5,
        y=1.03,
    )
    fig.tight_layout()
    save(fig, "qm-stationary-state.svg")


# ---------------------------------------------------------------- figure 4


def infinite_well_state(n, a, x):
    """無限に深い井戸型ポテンシャルの規格化された固有関数。"""
    phi = np.where(
        np.abs(x) <= a,
        np.cos(n * np.pi * x / (2 * a)) if n % 2 == 1 else np.sin(n * np.pi * x / (2 * a)),
        0.0,
    )
    return phi / np.sqrt(a)  # int |phi|^2 dx = 1


def fig_infinite_well():
    """エネルギー固有値が n^2 に比例して離散的になること。"""
    a = 1.0
    x = np.linspace(-1.75 * a, 1.75 * a, 600)
    levels = [1, 2, 3, 4]
    e1 = 1.0  # E_1 を 1 とした目盛
    scale = 1.15  # 波動関数の描画倍率 (準位が重ならない範囲で決める)
    bottom = -1.2

    fig, axes = plt.subplots(
        1, 2, figsize=(8.6, 4.6), gridspec_kw={"width_ratios": [2.4, 1.0]}
    )

    ax = axes[0]
    top = e1 * 4**2 + 5.5
    # 無限に高い壁
    for x0 in (-1.75 * a, a):
        ax.add_patch(
            Rectangle(
                (x0, bottom), 0.75 * a, top - bottom, facecolor=BAND, alpha=0.25, lw=0
            )
        )
    ax.axvline(-a, color=INK, lw=1.4)
    ax.axvline(a, color=INK, lw=1.4)
    for x0 in (-1.37 * a, 1.37 * a):
        ax.text(x0, top - 1.4, "$V = \\infty$", fontsize=11, color=GRAY, ha="center")

    for n in levels:
        e = e1 * n**2
        ax.hlines(e, -a, a, color=FAINT, lw=0.9, zorder=0)
        ax.plot(x, e + scale * infinite_well_state(n, a, x), color=BLUE, lw=1.8)
        parity = "偶関数" if n % 2 == 1 else "奇関数"
        ax.text(
            -1.7 * a,
            e + 0.3,
            f"$n = {n}$\n({parity})",
            fontsize=9,
            color=GRAY,
            va="bottom",
            linespacing=1.4,
        )
        ax.text(
            1.7 * a,
            e + 0.3,
            f"$E_{{{n}}} = {n**2}E_1$" if n > 1 else "$E_1$",
            fontsize=9.5,
            color=INK,
            ha="right",
            va="bottom",
        )

    ax.set_xlim(-1.75 * a, 1.75 * a)
    ax.set_ylim(bottom, top)
    ax.set_xticks([-a, 0, a])
    ax.set_xticklabels(["$-a$", "$0$", "$a$"])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("エネルギー $E$")
    ax.set_title("各準位の上に $\\phi_n(x)$ を重ねて描いたもの")
    despine(ax, ("top", "right"))

    # 右: 準位間隔が n^2 で開いていく様子
    ax = axes[1]
    for n in levels:
        e = e1 * n**2
        ax.hlines(e, 0.15, 0.85, color=BLUE, lw=2.0)
        ax.text(0.9, e, f"$n = {n}$", fontsize=10, va="center", color=GRAY)
    ax.annotate(
        "",
        xy=(0.1, e1 * 16),
        xytext=(0.1, e1 * 9),
        arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1, shrinkA=0, shrinkB=0),
    )
    ax.text(0.06, e1 * 12.5, "$7 E_1$", fontsize=9.5, ha="right", va="center")
    ax.annotate(
        "",
        xy=(0.1, e1 * 4),
        xytext=(0.1, e1 * 1),
        arrowprops=dict(arrowstyle="<->", color=INK, lw=1.1, shrinkA=0, shrinkB=0),
    )
    ax.text(0.06, e1 * 2.5, "$3 E_1$", fontsize=9.5, ha="right", va="center")

    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(bottom, top)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("$E_n \\propto n^2$")
    despine(ax, ("top", "right", "bottom", "left"))

    fig.suptitle(
        "束縛状態ではとりうるエネルギーが離散的になる (無限に深い井戸型ポテンシャル)",
        fontsize=11.5,
        y=1.0,
    )
    fig.tight_layout()
    save(fig, "qm-infinite-well.svg")


# ---------------------------------------------------------------- figure 5


def finite_well_roots(radius):
    """x = ka の解を返す。even なら y = x tan x、odd なら y = -x cot x との交点。

    いずれも x^2 + y^2 = radius^2 (radius = sqrt(2 m V_0) a / hbar) 上で探す。
    """
    eps = 1e-9
    even, odd = [], []

    n = 0
    while n * np.pi < radius:
        lo = n * np.pi + eps
        hi = min((n + 0.5) * np.pi, radius) - eps
        if hi > lo:
            even.append(
                bisect(lambda x: np.sqrt(radius**2 - x**2) - x * np.tan(x), lo, hi)
            )
        n += 1

    n = 0
    while (n + 0.5) * np.pi < radius:
        lo = (n + 0.5) * np.pi + eps
        hi = min((n + 1.0) * np.pi, radius) - eps
        if hi > lo:
            odd.append(
                bisect(lambda x: np.sqrt(radius**2 - x**2) + x / np.tan(x), lo, hi)
            )
        n += 1

    return even, odd


def fig_finite_well_graphical():
    """y = x tan x, y = -x cot x と円の交点として束縛状態を数える。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2), sharey=True)

    xmax = 7.6
    for ax, radius in zip(axes, (2.0, 6.5)):
        # y = x tan x (分岐ごとに切って描く)
        for n in range(4):
            xs = np.linspace(n * np.pi + 1e-4, (n + 0.5) * np.pi - 1e-3, 400)
            ax.plot(
                xs,
                xs * np.tan(xs),
                color=BLUE,
                lw=1.7,
                label="$y = x \\tan x$ (偶関数解)" if n == 0 else None,
            )
        # y = -x cot x
        for n in range(4):
            xs = np.linspace((n + 0.5) * np.pi + 1e-4, (n + 1) * np.pi - 1e-3, 400)
            ax.plot(
                xs,
                -xs / np.tan(xs),
                color=ORANGE,
                lw=1.7,
                ls="--",
                label="$y = -x \\cot x$ (奇関数解)" if n == 0 else None,
            )

        theta = np.linspace(0, np.pi / 2, 300)
        ax.plot(
            radius * np.cos(theta),
            radius * np.sin(theta),
            color=INK,
            lw=1.8,
            label="$x^2 + y^2 = 2 m V_0 a^2 / \\hbar^2$",
        )

        even, odd = finite_well_roots(radius)
        for xs, color in ((even, BLUE), (odd, ORANGE)):
            for xr in xs:
                ax.scatter(
                    [xr],
                    [np.sqrt(radius**2 - xr**2)],
                    s=58,
                    color=color,
                    edgecolors="white",
                    linewidths=1.0,
                    zorder=5,
                )

        ax.set_xlim(0, xmax)
        ax.set_ylim(0, 8.2)
        ax.set_xticks([n * np.pi / 2 for n in range(5)])
        ax.set_xticklabels(["$0$", "$\\pi/2$", "$\\pi$", "$3\\pi/2$", "$2\\pi$"])
        ax.set_xlabel("$x = ka$")
        ax.set_title(
            f"$\\sqrt{{2 m V_0}}\\, a / \\hbar = {radius}$\n"
            f"偶関数解 {len(even)} 個・奇関数解 {len(odd)} 個",
            fontsize=11,
            linespacing=1.5,
        )
        despine(ax)

    axes[0].set_ylabel("$y = \\rho a$")
    axes[0].legend(loc="upper left", fontsize=9)

    fig.suptitle(
        "井戸が深い (半径が大きい) ほど交点が増え、束縛状態の数が増える",
        fontsize=11.5,
        y=1.0,
    )
    fig.tight_layout()
    save(fig, "qm-finite-well-graphical.svg")


# ---------------------------------------------------------------- figure 6


def fig_finite_well_states():
    """有限の深さの井戸では波動関数が壁の外に染み出す。"""
    a = 1.0
    radius = 6.5
    v0 = radius**2 * HB2_2M / a**2  # 描画には使わないが単位系の整合性のため
    even, odd = finite_well_roots(radius)

    states = sorted(
        [(x, "even") for x in even] + [(x, "odd") for x in odd], key=lambda s: s[0]
    )

    x = np.linspace(-2.6 * a, 2.6 * a, 800)
    fig, ax = plt.subplots(figsize=(8.0, 5.0))

    top = radius**2 * 1.18
    ax.add_patch(
        Rectangle((-2.6 * a, 0), 1.6 * a, radius**2, facecolor=BAND, alpha=0.25, lw=0)
    )
    ax.add_patch(
        Rectangle((a, 0), 1.6 * a, radius**2, facecolor=BAND, alpha=0.25, lw=0)
    )
    ax.hlines([radius**2], -2.6 * a, -a, color=INK, lw=1.6)
    ax.hlines([radius**2], a, 2.6 * a, color=INK, lw=1.6)
    ax.vlines([-a, a], 0, radius**2, color=INK, lw=1.6)
    ax.hlines([0], -a, a, color=INK, lw=1.6)
    ax.text(2.5 * a, radius**2 + 1.0, "$V_0$", fontsize=12, color=INK, ha="right")

    scale = 2.4
    for i, (xr, parity) in enumerate(states, start=1):
        k = xr / a
        rho = np.sqrt(radius**2 - xr**2) / a
        energy = xr**2  # y 軸は 2 m E a^2 / hbar^2 の目盛

        inside = np.cos(k * x) if parity == "even" else np.sin(k * x)
        edge = np.cos(k * a) if parity == "even" else np.sin(k * a)
        tail_r = edge * np.exp(rho * a) * np.exp(-rho * np.abs(x))
        tail_l = tail_r if parity == "even" else -tail_r
        phi = np.where(x < -a, tail_l, np.where(x > a, tail_r, inside))
        phi = phi / np.sqrt(np.trapezoid(phi**2, x))

        color = BLUE if parity == "even" else ORANGE
        ax.axhline(energy, color=FAINT, lw=0.9, zorder=0)
        ax.plot(x, energy + scale * phi, color=color, lw=1.8, zorder=3)
        ax.text(
            -2.55 * a,
            energy + 0.6,
            f"$n = {i}$ ({'偶関数' if parity == 'even' else '奇関数'})",
            fontsize=9.5,
            color=GRAY,
            va="bottom",
            bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none",
                      alpha=0.85),
        )

    # 染み出しを指し示す
    xr, _ = states[-1]
    ax.annotate(
        "壁の外にも波動関数が\n$e^{-\\rho |x|}$ で染み出す",
        xy=(1.35 * a, xr**2 + 0.5),
        xytext=(1.8 * a, xr**2 - 17.5),
        fontsize=10,
        color=INK,
        ha="center",
        va="center",
        linespacing=1.5,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none",
                  alpha=0.88),
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )

    ax.set_xlim(-2.6 * a, 2.6 * a)
    ax.set_ylim(-4.0, top)
    ax.set_xticks([-a, 0, a])
    ax.set_xticklabels(["$-a$", "$0$", "$a$"])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("エネルギー $E$")
    ax.set_title(
        f"有限の深さの井戸型ポテンシャルの束縛状態"
        f" ($\\sqrt{{2 m V_0}}\\, a / \\hbar = {radius}$, $V_0 \\simeq {v0:.2f}\\,$eV)"
    )
    despine(ax)
    fig.tight_layout()
    save(fig, "qm-finite-well-states.svg")


# ---------------------------------------------------------------- figure 7


def barrier_wavefunction(x, energy, v0, d, mass=M_E):
    """記事の (1)-(4) をそのまま解いて phi(x) を返す。F = 1 に規格化する。

    energy, v0 は eV、x, d は nm。
    """
    k = np.sqrt(2 * mass * energy * EV) / HBAR * 1e-9
    if energy < v0:
        rho = np.sqrt(2 * mass * (v0 - energy) * EV) / HBAR * 1e-9
    else:
        rho = 1j * np.sqrt(2 * mass * (energy - v0) * EV) / HBAR * 1e-9

    f = 1.0 + 0j
    c = 0.5 * (1 + 1j * k / rho) * np.exp(1j * k * d - rho * d) * f
    dd = 0.5 * (1 - 1j * k / rho) * np.exp(1j * k * d + rho * d) * f
    amp = 0.5 * (1 + rho / (1j * k)) * c + 0.5 * (1 - rho / (1j * k)) * dd
    b = c + dd - amp

    phi = np.where(
        x < 0,
        amp * np.exp(1j * k * x) + b * np.exp(-1j * k * x),
        np.where(
            x <= d,
            c * np.exp(rho * x) + dd * np.exp(-rho * x),
            f * np.exp(1j * k * x),
        ),
    )
    return phi / amp, abs(f / amp) ** 2  # A = 1 に取り直す


def transmission(energy, v0, d, mass=M_E):
    """記事の閉じた式によるトンネル確率 (E > V_0 では sinh -> sin と解析接続する)。"""
    energy = np.asarray(energy, dtype=float)
    arg = np.sqrt(2 * mass * np.abs(v0 - energy) * EV) / HBAR * 1e-9 * d
    below = 1 + v0**2 * np.sinh(arg) ** 2 / (4 * energy * (v0 - energy))
    above = 1 + v0**2 * np.sin(arg) ** 2 / (4 * energy * (energy - v0))
    return 1 / np.where(energy < v0, below, above)


def fig_tunneling():
    """障壁の中で指数的に減衰し、反対側に小さな振幅の波が漏れ出す様子。"""
    v0, d, energy = 2.0, 0.25, 1.0  # eV, nm, eV
    x = np.linspace(-2.5, 2.5, 1500)
    phi, t = barrier_wavefunction(x, energy, v0, d)

    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.add_patch(
        Rectangle((0, -2.6), d, 5.2, facecolor=BAND, alpha=0.3, lw=0, zorder=0)
    )
    ax.annotate(
        f"障壁 ($0 \\leq x \\leq d$)\n高さ $V_0 = {v0}\\,$eV・厚さ $d = {d}\\,$nm",
        xy=(d / 2, 1.7),
        xytext=(-2.45, 2.55),
        fontsize=9.5,
        ha="left",
        va="top",
        color=INK,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )

    ax.plot(x, phi.real, color=BLUE, lw=1.6, label="$\\mathrm{Re}\\,\\phi(x)$")
    ax.plot(x, np.abs(phi), color=PURPLE, lw=1.4, ls="--", label="$|\\phi(x)|$")
    ax.plot(x, -np.abs(phi), color=PURPLE, lw=1.4, ls="--")
    ax.axhline(0, color=FAINT, lw=0.8)

    ax.annotate(
        "入射波 + 反射波\n(重なって振幅が波打つ)",
        xy=(-1.55, -1.55),
        xytext=(-1.55, -2.35),
        fontsize=10,
        color=INK,
        ha="center",
        va="bottom",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )
    ax.annotate(
        "障壁の中では $e^{-\\rho x}$ で減衰",
        xy=(d * 0.6, 0.78),
        xytext=(0.62, 1.5),
        fontsize=10,
        color=INK,
        ha="left",
        va="center",
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )
    ax.annotate(
        f"透過波 (トンネル確率 $|F/A|^2 = {t:.2f}$)",
        xy=(1.75, 0.53),
        xytext=(1.3, -2.35),
        fontsize=10,
        color=INK,
        ha="center",
        va="bottom",
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.6, 2.6)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$ [nm]")
    ax.set_title(
        f"$E = {energy}\\,$eV $< V_0$ でも波動関数は障壁の向こう側に漏れ出す"
        " (入射させるのは電子)"
    )
    ax.legend(loc="upper right", fontsize=10)
    despine(ax, ("top", "right", "left"))
    save(fig, "qm-tunneling.svg")


# ---------------------------------------------------------------- figure 8


def fig_tunneling_probability():
    """トンネル確率のエネルギー依存性と障壁の厚さ依存性。"""
    v0 = 1.0
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))

    ax = axes[0]
    e = np.linspace(0.005, 3.0, 1200)
    for d, color in ((0.15, BLUE), (0.3, PURPLE), (0.5, ORANGE)):
        ax.plot(e / v0, transmission(e, v0, d), color=color, lw=1.8,
                label=f"$d = {d}\\,$nm")
    ax.plot([0, 1, 1, 3], [0, 0, 1, 1], color=GRAY, lw=1.4, ls=":",
            label="古典力学の予想")
    ax.axvline(1, color=FAINT, lw=0.9)
    ax.set_xlim(0, 3)
    ax.set_ylim(-0.03, 1.2)
    ax.set_xlabel("$E / V_0$")
    ax.set_ylabel("トンネル確率 $|F/A|^2$")
    ax.set_title("$E < V_0$ でも $0$ にならない")
    ax.legend(loc="lower right", fontsize=9)
    despine(ax)

    ax = axes[1]
    d = np.linspace(0.02, 1.2, 600)
    for energy, color in ((0.2, BLUE), (0.5, PURPLE), (0.8, ORANGE)):
        ax.semilogy(
            d,
            [transmission(np.array(energy), v0, dd) for dd in d],
            color=color,
            lw=1.8,
            label=f"$E = {energy}\\,$eV",
        )
    ax.set_xlim(0, 1.2)
    ax.set_ylim(1e-6, 3)
    ax.set_xlabel("障壁の厚さ $d$ [nm]")
    ax.set_ylabel("トンネル確率 $|F/A|^2$")
    ax.set_title("厚さに対しては指数的に小さくなる")
    ax.legend(loc="lower left", fontsize=9)
    despine(ax)

    fig.suptitle(
        f"高さ $V_0 = {v0}\\,$eV の障壁に電子を入射させたときのトンネル確率",
        fontsize=11.5,
        y=1.02,
    )
    fig.tight_layout()
    save(fig, "qm-tunneling-probability.svg")


# ---------------------------------------------------------------- figure 9


def fig_plane_wave():
    """S.eq の導出で使う平面波 psi = A exp{i(px/hbar - Et/hbar)} の姿。"""
    fig, axes = plt.subplots(
        2, 2, figsize=(8.6, 5.6), gridspec_kw={"width_ratios": [1.0, 1.25]}
    )

    x = np.linspace(0, 2, 500)
    k = 2 * np.pi  # 波長を 1 とする

    # (a) 実部と虚部
    ax = axes[0, 0]
    ax.plot(x, np.cos(k * x), color=BLUE, lw=1.8, label="$\\mathrm{Re}\\,\\psi$")
    ax.plot(
        x, np.sin(k * x), color=ORANGE, lw=1.6, ls="--", label="$\\mathrm{Im}\\,\\psi$"
    )
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.set_xlim(0, 2)
    ax.set_ylim(-1.35, 1.75)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_title("実部と虚部は $\\pi/2$ ずれる", fontsize=11)
    ax.legend(loc="upper right", fontsize=9.5, ncol=2, columnspacing=0.8)
    despine(ax, ("top", "right", "left"))

    # (b) 複素数にすると |psi|^2 が一定になる
    ax = axes[0, 1]
    ax.plot(
        x,
        np.ones_like(x),
        color=PURPLE,
        lw=2.0,
        label="$|A e^{i(kx - \\omega t)}|^2$ (一定)",
    )
    ax.plot(
        x,
        np.cos(k * x) ** 2,
        color=GRAY,
        lw=1.6,
        ls=":",
        label="$|A \\cos(kx - \\omega t)|^2$",
    )
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.annotate(
        "実数の波だけでは\n存在確率が場所によって $0$ になる",
        xy=(1.25, 0.02),
        xytext=(1.0, -0.62),
        fontsize=9.5,
        color=INK,
        ha="center",
        va="center",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )
    ax.set_xlim(0, 2)
    ax.set_ylim(-1.35, 1.75)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_ylim(-1.6, 2.7)
    ax.set_title("$\\Delta p = 0$ なら $|\\psi|^2$ は一定のはず", fontsize=11)
    ax.legend(loc="upper right", fontsize=9)
    despine(ax, ("top", "right", "left"))

    # (c) 時間発展は複素平面上の回転
    ax = axes[1, 0]
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(theta), np.sin(theta), color=FAINT, lw=1.2)
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.axvline(0, color=FAINT, lw=0.8)
    ax.text(1.42, 0.08, "$\\mathrm{Re}$", fontsize=9.5, color=GRAY, ha="right")
    ax.text(0.08, 1.32, "$\\mathrm{Im}$", fontsize=9.5, color=GRAY, va="top")
    for t, alpha in zip((0.0, 0.125, 0.25), (1.0, 0.6, 0.35)):
        angle = -2 * np.pi * t
        ax.annotate(
            "",
            xy=(np.cos(angle), np.sin(angle)),
            xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1.6, alpha=alpha),
        )
    arc = np.linspace(-0.05 * np.pi, -0.55 * np.pi, 60)
    ax.plot(0.66 * np.cos(arc), 0.66 * np.sin(arc), color=INK, lw=1.1)
    ax.annotate(
        "",
        xy=(0.66 * np.cos(arc[-1]), 0.66 * np.sin(arc[-1])),
        xytext=(0.66 * np.cos(arc[-6]), 0.66 * np.sin(arc[-6])),
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1),
    )
    ax.text(0.62, -0.92, "$-\\dfrac{E}{\\hbar} t$", fontsize=11, ha="left", va="center")
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("時間発展は複素平面上の回転", fontsize=11)
    despine(ax, ("top", "right", "bottom", "left"))

    # (d) 波は速度 omega / k で進む
    ax = axes[1, 1]
    for t, alpha, lw in ((0.0, 1.0, 1.8), (0.15, 0.55, 1.4), (0.3, 0.3, 1.4)):
        ax.plot(x, np.cos(k * x - 2 * np.pi * t), color=BLUE, lw=lw, alpha=alpha)
    ax.annotate(
        "",
        xy=(1.15, 1.4),
        xytext=(0.55, 1.4),
        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4),
    )
    ax.text(0.85, 1.46, "速度 $\\omega / k$", fontsize=10, ha="center", va="bottom")
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.set_xlim(0, 2)
    ax.set_ylim(-1.35, 1.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_title("$\\mathrm{Re}\\,\\psi(x, t)$ は右へ流れる", fontsize=11)
    despine(ax, ("top", "right", "left"))

    fig.suptitle(
        "平面波 $\\psi(x, t) = A \\exp\\left\\{ i "
        "\\left( \\frac{p}{\\hbar} x - \\frac{E}{\\hbar} t \\right) \\right\\}$ "
        "— 複素数にすると $|\\psi|^2$ を一定に保ったまま波を表せる",
        fontsize=11.5,
        y=1.03,
    )
    fig.tight_layout()
    save(fig, "qm-plane-wave.svg")


# ---------------------------------------------------------------- figure 10


def region_label(ax, x, y, text, color=GRAY):
    ax.text(x, y, text, fontsize=9.5, color=color, ha="center", va="center")


def fig_potentials():
    """記事で解く 3 つのポテンシャルの形。"""
    a, d, v0 = 1.0, 0.8, 1.0
    energy = 0.45 * v0
    xlim, top = (-2.3, 2.3), 1.62

    fig, axes = plt.subplots(1, 3, figsize=(8.8, 3.3))

    # (a) 無限に深い井戸
    ax = axes[0]
    for x0 in (xlim[0], a):
        ax.add_patch(
            Rectangle(
                (x0, energy), xlim[1] - a, top - energy, facecolor=BAND, alpha=0.22, lw=0
            )
        )
    ax.hlines(0, -a, a, color=INK, lw=2.2)
    for s in (-1, 1):
        ax.annotate(
            "",
            xy=(s * a, top),
            xytext=(s * a, 0),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.2, shrinkA=0, shrinkB=0),
        )
    region_label(ax, -1.62 * a, 1.28, "$V = \\infty$")
    region_label(ax, 1.62 * a, 1.28, "$V = \\infty$")
    ax.set_title("無限に深い井戸型ポテンシャル", fontsize=11)

    # (b) 有限の深さの井戸
    ax = axes[1]
    for x0 in (xlim[0], a):
        ax.add_patch(
            Rectangle((x0, energy), xlim[1] - a, v0 - energy, facecolor=BAND,
                      alpha=0.22, lw=0)
        )
    ax.hlines(0, -a, a, color=INK, lw=2.2)
    ax.hlines(v0, xlim[0], -a, color=INK, lw=2.2)
    ax.hlines(v0, a, xlim[1], color=INK, lw=2.2)
    ax.vlines([-a, a], 0, v0, color=INK, lw=2.2)
    region_label(ax, -1.62 * a, v0 + 0.16, "$V = V_0$")
    region_label(ax, 1.62 * a, v0 + 0.16, "$V = V_0$")
    ax.set_title("有限の深さの井戸型ポテンシャル", fontsize=11)

    # (c) エネルギー障壁
    ax = axes[2]
    ax.add_patch(
        Rectangle((0, energy), d, v0 - energy, facecolor=BAND, alpha=0.22, lw=0)
    )
    ax.hlines(0, xlim[0], 0, color=INK, lw=2.2)
    ax.hlines(0, d, xlim[1], color=INK, lw=2.2)
    ax.hlines(v0, 0, d, color=INK, lw=2.2)
    ax.vlines([0, d], 0, v0, color=INK, lw=2.2)
    region_label(ax, d / 2, v0 + 0.16, "$V = V_0$")
    ax.set_title("エネルギー障壁 (トンネル効果)", fontsize=11)

    ticks = ([-a, 0, a], [-a, 0, a], [0, d])
    labels = (
        ["$-a$", "$0$", "$a$"],
        ["$-a$", "$0$", "$a$"],
        ["$0$", "$d$"],
    )
    for ax, tick, label in zip(axes, ticks, labels):
        # 粒子のエネルギー E は 3 つとも同じ高さに引いて比べられるようにする
        ax.axhline(energy, color=ORANGE, lw=1.4, ls="--", zorder=4)
        ax.text(xlim[0] + 0.08, energy + 0.07, "$E$", color=ORANGE, fontsize=11)
        ax.set_xlim(*xlim)
        ax.set_ylim(-0.3, top)
        ax.set_xticks(tick)
        ax.set_xticklabels(label)
        ax.set_yticks([])
        ax.set_xlabel("位置 $x$")
        despine(ax, ("top", "right", "bottom", "left"))

    axes[0].set_ylabel("ポテンシャル $V(x)$")
    fig.suptitle(
        "以降で解く 3 つの問題 — 網かけは古典力学では入れない領域 ($E < V$)",
        fontsize=11.5,
        y=1.02,
    )
    fig.tight_layout()
    save(fig, "qm-potentials.svg")


# ---------------------------------------------------------------- figure 11


def fig_infinite_well_boundary():
    """境界条件 phi(±a) = 0 が ka = n pi / 2 を選び出すこと。"""
    a = 1.0
    x = np.linspace(-a, a, 500)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.0))

    # 左: 端で 0 にならない波は捨てられる
    ax = axes[0]
    for ka, color, lw, ls, label in (
        (1.05, GRAY, 1.4, "--", "$ka$ が中途半端 (捨てる)"),
        (1.95, GRAY, 1.4, "--", None),
        (np.pi / 2, BLUE, 2.1, "-", "$ka = \\pi/2$ (解)"),
    ):
        phi = np.cos(ka * x / a)
        ax.plot(x, phi, color=color, lw=lw, ls=ls, label=label)
        for s in (-1, 1):
            ax.scatter(
                [s * a],
                [np.cos(ka)],
                s=46,
                color=color,
                zorder=5,
                edgecolors="white",
                linewidths=1.0,
            )
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.vlines([-a, a], -1.25, 1.25, color=INK, lw=1.8)
    ax.annotate(
        "$\\phi(\\pm a) \\neq 0$ の波は\n$\\phi(x) = 0\\;(|x| > a)$ と\nつながらないので捨てる",
        xy=(a, np.cos(1.95)),
        xytext=(0.0, -1.75),
        fontsize=9.5,
        color=INK,
        ha="center",
        va="center",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )
    ax.set_ylim(-2.55, 2.55)
    ax.set_title("境界条件 $\\phi(\\pm a) = 0$ で候補が絞られる", fontsize=11)
    ax.legend(loc="upper center", fontsize=9)

    # 右: 井戸の幅にちょうど半波長の整数倍が収まる
    ax = axes[1]
    offsets = (3.4, 1.7, 0.0)
    for n, offset in zip((1, 2, 3), offsets):
        phi = 0.5 * (
            np.cos(n * np.pi * x / (2 * a))
            if n % 2 == 1
            else np.sin(n * np.pi * x / (2 * a))
        )
        ax.plot(x, offset + phi, color=BLUE, lw=1.8)
        ax.hlines(offset, -a, a, color=FAINT, lw=0.8, zorder=0)
        # 半波長 lambda / 2 = 2a / n が n 個ぶん収まっている
        for i in range(n):
            left = -a + 2 * a * i / n
            ax.annotate(
                "",
                xy=(left + 2 * a / n, offset + 0.78),
                xytext=(left, offset + 0.78),
                arrowprops=dict(
                    arrowstyle="<->", color=INK, lw=1.0, shrinkA=0, shrinkB=0
                ),
            )
        ax.text(
            0,
            offset + 0.86,
            f"$\\lambda / 2$ が {n} 個 → "
            + ("$ka = \\pi/2$", "$ka = \\pi$", "$ka = 3\\pi/2$")[n - 1],
            fontsize=9.5,
            ha="center",
            va="bottom",
        )
        ax.text(-1.32 * a, offset, f"$n = {n}$", fontsize=10, color=GRAY, va="center")
    ax.set_ylim(-1.05, 4.75)
    ax.set_title("許されるのは半波長が整数個収まる波", fontsize=11)

    for ax in axes:
        ax.set_xlim(-1.45 * a, 1.45 * a)
        ax.set_xticks([-a, 0, a])
        ax.set_xticklabels(["$-a$", "$0$", "$a$"])
        ax.set_yticks([])
        ax.set_xlabel("位置 $x$")
        despine(ax, ("top", "right", "left"))

    fig.suptitle(
        "$\\phi(x) = A \\sin kx + B \\cos kx$ のうち連続性を満たすものだけが残り、"
        "$k$ が離散的になる",
        fontsize=11.5,
        y=1.0,
    )
    fig.tight_layout()
    save(fig, "qm-infinite-well-boundary.svg")


# ---------------------------------------------------------------- figure 12


def fig_finite_well_setup():
    """有限の深さの井戸で、どの領域でどの式を解くのかを整理した図。"""
    a, v0 = 1.0, 1.0
    energy = 0.42 * v0
    xlim, top = (-2.6, 2.6), 1.75

    fig, ax = plt.subplots(figsize=(8.2, 4.4))

    for x0 in (xlim[0], a):
        ax.add_patch(
            Rectangle(
                (x0, energy), xlim[1] - a, v0 - energy, facecolor=BAND, alpha=0.22, lw=0
            )
        )
    ax.hlines(0, -a, a, color=INK, lw=2.2)
    ax.hlines(v0, xlim[0], -a, color=INK, lw=2.2)
    ax.hlines(v0, a, xlim[1], color=INK, lw=2.2)
    ax.vlines([-a, a], 0, v0, color=INK, lw=2.2)
    ax.text(xlim[1] - 0.18, v0 + 0.06, "$V_0$", fontsize=11, ha="right")
    ax.text(0, 0.08, "$V = 0$", fontsize=10, color=GRAY, ha="center")

    ax.axhline(energy, color=ORANGE, lw=1.4, ls="--")
    ax.text(xlim[0] + 0.08, energy + 0.06, "$E$", color=ORANGE, fontsize=11)

    for x0, cond, form in (
        (-1.8 * a, "$x < -a$", "$\\phi = C e^{\\rho x}$"),
        (0.0, "$-a \\leq x \\leq a$", "$\\phi = A \\sin kx + B \\cos kx$"),
        (1.8 * a, "$x > a$", "$\\phi = D e^{-\\rho x}$"),
    ):
        ax.text(x0, 1.62, cond, fontsize=10, color=GRAY, ha="center", va="center")
        ax.text(x0, 1.36, form, fontsize=10.5, color=INK, ha="center", va="center")

    for s in (-1, 1):
        ax.annotate(
            "$\\phi$ と $\\dfrac{d\\phi}{dx}$ が連続",
            xy=(s * a, 0.5 * energy),
            xytext=(s * 1.75 * a, -0.55),
            fontsize=10,
            color=INK,
            ha="center",
            va="center",
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
        )

    ax.text(
        0,
        -0.62,
        "$k = \\dfrac{\\sqrt{2mE}}{\\hbar},\\quad"
        " \\rho = \\dfrac{\\sqrt{2m(V_0 - E)}}{\\hbar}$",
        fontsize=11,
        ha="center",
        va="center",
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(-0.95, top)
    ax.set_xticks([-a, 0, a])
    ax.set_xticklabels(["$-a$", "$0$", "$a$"])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("ポテンシャル $V(x)$")
    ax.set_title(
        "領域ごとに解いて、$x = \\pm a$ で滑らかにつなぐ (束縛状態は $E < V_0$)"
    )
    despine(ax, ("top", "right", "bottom", "left"))
    fig.tight_layout()
    save(fig, "qm-finite-well-setup.svg")


# ---------------------------------------------------------------- figure 13


def shoot(eps, radius, u_max=1.9, n=20000):
    """phi'' = (v(u) - eps) phi を u = 0 から外向きに RK4 で積分する。

    長さは a、エネルギーは hbar^2 / (2 m a^2) を単位に取ってあるので
    井戸の外では v = radius^2、内側では v = 0 となる。偶関数解を仮定して
    phi(0) = 1, phi'(0) = 0 から出発する。

    eps は配列でもよい (その場合 phi の形は (n, len(eps)) になる)。井戸の外では
    増大解 e^{+rho u} が誤差を指数的に増幅するので、u_max は大きく取らない。
    """
    eps = np.atleast_1d(np.asarray(eps, dtype=float))
    u = np.linspace(0, u_max, n)
    h = u[1] - u[0]

    def deriv(uu, phi, dphi):
        v = 0.0 if abs(uu) <= 1.0 else radius**2
        return dphi, (v - eps) * phi

    phi = np.ones_like(eps)
    dphi = np.zeros_like(eps)
    out = np.empty((n, eps.size))
    out[0] = phi
    for i in range(n - 1):
        k1p, k1d = deriv(u[i], phi, dphi)
        k2p, k2d = deriv(u[i] + h / 2, phi + h / 2 * k1p, dphi + h / 2 * k1d)
        k3p, k3d = deriv(u[i] + h / 2, phi + h / 2 * k2p, dphi + h / 2 * k2d)
        k4p, k4d = deriv(u[i] + h, phi + h * k3p, dphi + h * k3d)
        phi = phi + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
        dphi = dphi + h / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
        out[i + 1] = phi
    return u, out.squeeze()


def fig_shooting():
    """エネルギーを固有値から少しでもずらすと解が発散すること。"""
    radius = 6.5
    u_max = 1.9
    eps0 = finite_well_roots(radius)[0][0] ** 2  # 基底状態 (偶関数解)
    delta = 0.05 * eps0

    fig, axes = plt.subplots(
        1, 2, figsize=(8.8, 4.0), gridspec_kw={"width_ratios": [1.1, 1.0]}
    )

    ax = axes[0]
    ax.add_patch(Rectangle((1, -3), u_max - 1, 6, facecolor=BAND, alpha=0.22, lw=0))
    ax.text(1.45, 2.55, "井戸の外", fontsize=9.5, color=GRAY, ha="center")
    for d, color, ls, label in (
        (-delta, ORANGE, "--", "$E$ が $5\\%$ 小さい"),
        (0.0, BLUE, "-", "$E$ がちょうど固有値"),
        (delta, GREEN, "--", "$E$ が $5\\%$ 大きい"),
    ):
        u, phi = shoot(eps0 + d, radius, u_max=u_max)
        ax.plot(u, phi, color=color, lw=1.8, ls=ls, label=label)
    ax.axhline(0, color=FAINT, lw=0.8)
    ax.annotate(
        "固有値のときだけ\n$|x| \\to \\infty$ で $0$ に収束する",
        xy=(1.6, 0.02),
        xytext=(1.05, -1.85),
        fontsize=9.5,
        color=INK,
        ha="center",
        va="center",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
    )
    ax.set_xlim(0, u_max)
    ax.set_ylim(-3, 3)
    ax.set_xticks([0, 0.5, 1, 1.5])
    ax.set_xticklabels(["$0$", "$0.5a$", "$a$", "$1.5a$"])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("$\\phi(x)$")
    ax.set_title("$\\phi(0) = 1, \\phi'(0) = 0$ から外向きに解く", fontsize=11)
    ax.legend(loc="upper left", fontsize=9)
    despine(ax, ("top", "right"))

    # 右: 遠方での phi の値をエネルギーの関数として見ると、零点が固有値
    ax = axes[1]
    eps = np.linspace(0.3, radius**2 - 0.3, 400)
    tail = shoot(eps, radius, u_max=u_max)[1][-1]
    ax.plot(eps, tail, color=INK, lw=1.6)
    ax.axhline(0, color=FAINT, lw=0.9)
    for xr in finite_well_roots(radius)[0]:
        ax.scatter([xr**2], [0], s=52, color=BLUE, zorder=5, edgecolors="white",
                   linewidths=1.0)
    ax.set_yscale("symlog", linthresh=1e-2)
    ax.set_xlim(0, radius**2)
    ax.set_xlabel("エネルギー $E$ ($\\hbar^2 / 2ma^2$ 単位)")
    ax.set_ylabel(f"$x = {u_max}a$ における $\\phi$")
    ax.set_title("零点だけが偶関数解のエネルギー固有値", fontsize=11)
    despine(ax)

    fig.suptitle(
        "束縛状態のエネルギーが離散的になる理由 "
        f"($\\sqrt{{2 m V_0}}\\, a / \\hbar = {radius}$ の井戸、偶関数解)",
        fontsize=11.5,
        y=1.0,
    )
    fig.tight_layout()
    save(fig, "qm-shooting.svg")


# ---------------------------------------------------------------- figure 14


def fig_tunneling_setup():
    """トンネル効果で、どの領域にどの波があるのかを整理した図。"""
    d, v0 = 1.0, 1.0
    energy = 0.45 * v0
    xlim, top = (-2.9, 3.4), 1.95

    fig, ax = plt.subplots(figsize=(8.4, 4.4))

    ax.add_patch(Rectangle((0, energy), d, v0 - energy, facecolor=BAND, alpha=0.22,
                           lw=0))
    ax.hlines(0, xlim[0], 0, color=INK, lw=2.2)
    ax.hlines(0, d, xlim[1], color=INK, lw=2.2)
    ax.hlines(v0, 0, d, color=INK, lw=2.2)
    ax.vlines([0, d], 0, v0, color=INK, lw=2.2)
    ax.text(d / 2, v0 + 0.1, "$V_0$", fontsize=11, ha="center", va="bottom")
    ax.annotate(
        "",
        xy=(d, -0.28),
        xytext=(0, -0.28),
        arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2, shrinkA=0, shrinkB=0),
    )
    ax.text(d / 2, -0.42, "$d$", fontsize=11, ha="center", va="top")

    ax.axhline(energy, color=ORANGE, lw=1.4, ls="--")
    ax.text(xlim[0] + 0.06, energy + 0.06, "$E$", color=ORANGE, fontsize=11)

    for x0, cond, form in (
        (-1.5, "$x < 0$", "$\\phi = A e^{ikx} + B e^{-ikx}$"),
        (d / 2, "$0 \\leq x \\leq d$", "$\\phi = C e^{\\rho x} + D e^{-\\rho x}$"),
        (2.4, "$x > d$", "$\\phi = F e^{ikx}$"),
    ):
        ax.text(x0, 1.82, cond, fontsize=10, color=GRAY, ha="center", va="center")
        ax.text(x0, 1.56, form, fontsize=10, color=INK, ha="center", va="center")

    # 入射波・反射波・透過波
    arrows = (
        (-2.7, -2.0, 1.3, BLUE, "入射波 $A$"),
        (-2.0, -2.7, 1.02, ORANGE, "反射波 $B$"),
        (1.4, 2.1, 1.3, BLUE, "透過波 $F$"),
        (2.1, 1.4, 1.02, GRAY, "存在しない波 $G = 0$"),
    )
    for x_from, x_to, y, color, label in arrows:
        faded = color == GRAY
        ax.annotate(
            "",
            xy=(x_to, y),
            xytext=(x_from, y),
            arrowprops=dict(
                arrowstyle="-|>", color=color, lw=1.8, alpha=0.45 if faded else 1.0
            ),
        )
        ax.text(
            max(x_from, x_to) + 0.14,
            y,
            label,
            fontsize=10,
            color=color,
            ha="left",
            va="center",
            alpha=0.55 if faded else 1.0,
        )
    # 存在しない波には×印を付ける
    ax.plot([1.7, 1.82], [0.95, 1.09], color=GRAY, lw=1.7)
    ax.plot([1.7, 1.82], [1.09, 0.95], color=GRAY, lw=1.7)

    for x0 in (0, d):
        ax.annotate(
            "",
            xy=(x0, 0.62 * energy),
            xytext=(x0 + (-0.55 if x0 == 0 else 0.55), -0.72),
            arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.0),
        )
    ax.text(
        d / 2,
        -0.85,
        "$x = 0, d$ で $\\phi$ と $\\dfrac{d\\phi}{dx}$ が連続 → 式 (1)〜(4)",
        fontsize=10,
        ha="center",
        va="center",
    )

    ax.set_xlim(*xlim)
    ax.set_ylim(-1.15, top)
    ax.set_xticks([0, d])
    ax.set_xticklabels(["$0$", "$d$"])
    ax.set_yticks([])
    ax.set_xlabel("位置 $x$")
    ax.set_ylabel("ポテンシャル $V(x)$")
    ax.set_title("求めたいのは入射波と透過波の強さの比 $|F/A|^2$")
    despine(ax, ("top", "right", "bottom", "left"))
    fig.tight_layout()
    save(fig, "qm-tunneling-setup.svg")


# ---------------------------------------------------------------- 自己検証


def check():
    """数値解と記事中の閉じた式が一致することを確かめる。"""
    for energy in (0.1, 0.4, 0.9):
        _, t_num = barrier_wavefunction(np.array([0.0]), energy, 1.0, 0.35)
        t_ref = float(transmission(np.array(energy), 1.0, 0.35))
        assert abs(t_num - t_ref) < 1e-9, (energy, t_num, t_ref)

    even, odd = finite_well_roots(6.5)
    for xr in even:
        assert abs(np.sqrt(6.5**2 - xr**2) - xr * np.tan(xr)) < 1e-6, xr
    for xr in odd:
        assert abs(np.sqrt(6.5**2 - xr**2) + xr / np.tan(xr)) < 1e-6, xr

    # 超越方程式の解を数値積分に入れると、井戸の外で純粋な e^{-rho x} になる
    # (増大解が混ざっていないことの確認)
    for xr in even:
        rho = np.sqrt(6.5**2 - xr**2)
        u, phi = shoot(xr**2, 6.5)
        i1, i2 = np.argmin(abs(u - 1.0)), np.argmin(abs(u - 1.4))
        expected = phi[i1] * np.exp(-rho * (u[i2] - u[i1]))
        # 井戸の縁の折れ目で RK4 が O(h) の誤差を出すので、許容は 1% 程度に取る
        assert abs(phi[i2] - expected) < 1e-2 * abs(expected), (xr, phi[i2], expected)


FIGURES = (
    fig_de_broglie,
    fig_uncertainty,
    fig_plane_wave,
    fig_stationary_state,
    fig_potentials,
    fig_infinite_well_boundary,
    fig_infinite_well,
    fig_finite_well_setup,
    fig_finite_well_graphical,
    fig_shooting,
    fig_finite_well_states,
    fig_tunneling_setup,
    fig_tunneling,
    fig_tunneling_probability,
)


if __name__ == "__main__":
    check()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for figure in FIGURES:
        figure()
