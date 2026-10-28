"""content/posts/stochastic-differential-equation.mdx の図を生成する。

出力先は public/img/sde-*.svg。ウィーナー過程はすべて sigma = 1 で描く。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-sde-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
PURPLE = "#7c3aed"
GREEN = "#16a34a"
GRAY = "#6b7280"
INK = "#111827"
BAND = "#94a3b8"

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
    # 標本路の束は rasterized=True で描いてあるので、その解像度も兼ねる
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05, dpi=110)
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


def despine(ax, sides=("top", "right")):
    for side in sides:
        ax.spines[side].set_visible(False)


def thin(t, y, target=1200):
    """SVG のパスが肥大しないよう、描画点を間引く。"""
    step = max(1, -(-len(t) // target))  # 切り上げ
    return t[::step], y[..., ::step]


def spread(paths, qs=(0.85, 0.5, 0.15)):
    """終端値が偏らないように、強調する標本路を分位点から選ぶ。"""
    order = np.argsort(paths[:, -1])
    return [paths[order[min(len(order) - 1, int(q * len(order)))]] for q in qs]


def coin_steps(rng, n):
    """+1 / -1 を等確率で n 個。"""
    return rng.choice([-1.0, 1.0], size=n)


# ---------------------------------------------------------------- figure 1


def fig_random_walk():
    """R(t) の標本路と、E[R(t)] = 0, V[R(t)] = sigma^2 t の確認。"""
    rng = np.random.RandomState(3)
    T = 50
    t = np.arange(T + 1)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8))

    ax = axes[0]
    for color in (BLUE, ORANGE, PURPLE, GREEN, GRAY):
        path = np.concatenate([[0.0], np.cumsum(coin_steps(rng, T))])
        ax.step(t, path, where="post", color=color, lw=1.3, alpha=0.9)
    band = np.sqrt(t)
    ax.plot(t, band, color=INK, lw=1.2, ls="--")
    ax.plot(t, -band, color=INK, lw=1.2, ls="--")
    ax.axhline(0, color="#d1d5db", lw=0.8)
    ax.text(T * 0.72, np.sqrt(T * 0.72) + 1.0, r"$+\sigma \sqrt{t}$", fontsize=11)
    ax.text(T * 0.72, -np.sqrt(T * 0.72) - 2.4, r"$-\sigma \sqrt{t}$", fontsize=11)
    ax.set_xlim(0, T)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$R(t)$")
    ax.set_title("ランダムウォークの標本路 ($\\sigma = 1$)")
    despine(ax)

    # 多数の試行を集めると R(T) は N(0, sigma^2 T) に近づく
    ax = axes[1]
    trials = np.cumsum(coin_steps(rng, (20000, T)), axis=1)[:, -1]
    edges = np.arange(trials.min() - 1, trials.max() + 3, 2)
    ax.hist(trials, bins=edges, density=True, color=BLUE, alpha=0.35, edgecolor="white")
    xs = np.linspace(-4 * np.sqrt(T), 4 * np.sqrt(T), 400)
    ax.plot(
        xs,
        np.exp(-(xs**2) / (2 * T)) / np.sqrt(2 * np.pi * T),
        color=INK,
        lw=1.8,
        label=r"$N(0, \sigma^2 t)$",
    )
    ax.axvline(0, color="#d1d5db", lw=0.8)
    ax.set_xlim(-4 * np.sqrt(T), 4 * np.sqrt(T))
    ax.set_xlabel("$R(50)$")
    ax.set_ylabel("確率密度")
    ax.set_title("$t = 50$ における分布 (20000 試行)")
    ax.legend(loc="upper right")
    despine(ax)

    fig.tight_layout()
    save(fig, "sde-random-walk.svg")


# ---------------------------------------------------------------- figure 2


def refined_walk(rng, levels, fine_n):
    """同じ 1 本の軌道を、粗さの異なる分割で見たもの。

    最も細かい分割で ±sigma sqrt(1/fine_n) の歩みを作り、粗い分割ではそれを
    間引いて折れ線にする。どの分割でも同じ極限の軌道を見ていることになる。
    """
    steps = coin_steps(rng, fine_n) * np.sqrt(1.0 / fine_n)
    fine = np.concatenate([[0.0], np.cumsum(steps)])
    out = []
    for n in levels:
        idx = np.arange(0, fine_n + 1, fine_n // n)
        out.append((idx / fine_n, fine[idx]))
    return out


def fig_wiener_limit():
    """Delta t -> 0 でランダムウォークがウィーナー過程に近づく様子。"""
    rng = np.random.RandomState(11)
    levels = (4, 16, 64, 4096)
    paths = refined_walk(rng, levels, fine_n=4096)

    fig, axes = plt.subplots(2, 2, figsize=(8.2, 5.4), sharex=True, sharey=True)
    for ax, n, (ts, ws) in zip(axes.ravel(), levels, paths):
        marker = "o" if n <= 16 else None
        ax.plot(ts, ws, color=BLUE, lw=1.4 if n <= 64 else 0.9, marker=marker, ms=4)
        ax.axhline(0, color="#d1d5db", lw=0.8)
        ax.set_title(
            f"$n = {n}$ " + r"$(\Delta t = 1/" + f"{n})$",
            fontsize=11,
        )
        despine(ax)
    for ax in axes[1]:
        ax.set_xlabel("$t$")
    for ax in axes[:, 0]:
        ax.set_ylabel(r"$W(t)$")
    axes[0, 0].set_xlim(0, 1)

    fig.suptitle(
        r"$\Delta W = \pm \sigma \sqrt{\Delta t}$ のまま $\Delta t$ を小さくする",
        fontsize=12.5,
    )
    fig.tight_layout()
    save(fig, "sde-wiener-limit.svg")


# ---------------------------------------------------------------- figure 3


def brownian(rng, n_paths, n_steps, T, sigma=1.0):
    dt = T / n_steps
    dW = rng.randn(n_paths, n_steps) * sigma * np.sqrt(dt)
    W = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(dW, axis=1)], axis=1)
    return np.linspace(0, T, n_steps + 1), W


def fig_wiener_paths():
    """W(t) ~ N(0, sigma^2 t) の広がり方。"""
    rng = np.random.RandomState(7)
    T, n_paths = 3.0, 250
    t, W = brownian(rng, n_paths, 1500, T)
    # ヒストグラムは滑らかにしたいので、終端の値だけ別に多く取る
    ends = rng.randn(20000) * np.sqrt(T)

    fig, axes = plt.subplots(
        1, 2, figsize=(8.4, 4.2), gridspec_kw={"width_ratios": [3.2, 1.0]}, sharey=True
    )

    ax = axes[0]
    ts, Ws = thin(t, W)
    ax.plot(ts, Ws.T, color=BAND, lw=0.5, alpha=0.18, rasterized=True)
    for path, color in zip(spread(Ws), (BLUE, ORANGE, PURPLE)):
        ax.plot(ts, path, color=color, lw=1.3)
    band = np.sqrt(t)
    for k, ls in ((1, "--"), (2, ":")):
        ax.plot(t, k * band, color=INK, lw=1.2, ls=ls)
        ax.plot(t, -k * band, color=INK, lw=1.2, ls=ls)
    ax.axhline(0, color="#d1d5db", lw=0.8)
    # 曲線と重なるので、ラベルの下は白で抜く
    label_bg = dict(facecolor="white", edgecolor="none", pad=1.5)
    ax.text(2.32, np.sqrt(2.32) + 0.2, r"$\pm \sigma \sqrt{t}$", fontsize=11, bbox=label_bg)
    ax.text(
        2.32, 2 * np.sqrt(2.32) + 0.2, r"$\pm 2 \sigma \sqrt{t}$", fontsize=11, bbox=label_bg
    )
    ax.set_xlim(0, T)
    ax.set_ylim(-4.6, 4.6)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$W(t)$")
    ax.set_title(f"ウィーナー過程の標本路 ({n_paths} 本)")
    despine(ax)

    ax = axes[1]
    ys = np.linspace(-4.6, 4.6, 400)
    ax.hist(
        ends,
        bins=40,
        density=True,
        orientation="horizontal",
        color=BLUE,
        alpha=0.35,
        edgecolor="white",
    )
    ax.plot(
        np.exp(-(ys**2) / (2 * T)) / np.sqrt(2 * np.pi * T),
        ys,
        color=INK,
        lw=1.8,
    )
    ax.set_xlabel("確率密度")
    ax.set_title("$t = 3$ の分布\n$N(0, 3\\sigma^2)$", fontsize=11)
    despine(ax)

    fig.tight_layout()
    save(fig, "sde-wiener-paths.svg")


# ---------------------------------------------------------------- figure 4


def fig_nowhere_differentiable():
    """どこまで拡大してもギザギザが消えない (= 微分できない)。"""
    rng = np.random.RandomState(21)
    n = 2**19
    t, W = brownian(rng, 1, n, 1.0)
    W = W[0]

    windows = [(0.0, 1.0), (0.50, 0.55), (0.5220, 0.5225)]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.4))
    for k, (ax, (a, b)) in enumerate(zip(axes, windows)):
        m = (t >= a) & (t <= b)
        ts, ws = thin(t[m], W[m])
        ax.plot(ts, ws, color=BLUE, lw=1.0)
        pad = (ws.max() - ws.min()) * 0.12
        ax.set_xlim(a, b)
        ax.set_ylim(ws.min() - pad, ws.max() + pad)
        ax.set_title(f"幅 ${b - a:g}$", fontsize=11)
        ax.set_xlabel("$t$")
        # 目盛りが密だとラベルが重なるので 3 本に絞る
        ticks = np.linspace(a, b, 3)
        digits = max(0, -int(np.floor(np.log10(b - a))) + 1)
        ax.set_xticks(ticks, [f"{x:.{digits}f}" for x in ticks])
        ax.tick_params(labelsize=9)
        despine(ax)

        # 次の枠で拡大する範囲を示す
        if k + 1 < len(windows):
            na, nb = windows[k + 1]
            nm = (t >= na) & (t <= nb)
            lo, hi = W[nm].min(), W[nm].max()
            ylo, yhi = ax.get_ylim()
            h = max(hi - lo, (yhi - ylo) * 0.05)
            w = max(nb - na, (b - a) * 0.02)
            ax.add_patch(
                Rectangle(
                    ((na + nb - w) / 2, (lo + hi - h) / 2),
                    w,
                    h,
                    facecolor=ORANGE,
                    edgecolor=ORANGE,
                    alpha=0.35,
                    lw=1.0,
                    zorder=4,
                )
            )
    axes[0].set_ylabel("$W(t)$")
    fig.suptitle(
        r"$\Delta W \sim \sqrt{\Delta t}$ なので傾き $\Delta W / \Delta t \sim 1/\sqrt{\Delta t}$ は発散する",
        fontsize=12,
    )
    fig.tight_layout()
    save(fig, "sde-nowhere-differentiable.svg")


# ---------------------------------------------------------------- figure 5


def fig_sde_paths():
    """ドリフト項とノイズ項が解の形をどう決めるか。"""
    rng = np.random.RandomState(2)
    T, n, m = 5.0, 2000, 40
    t, W = brownian(rng, m, n, T)
    t, W = thin(t, W)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.9))

    # dX = mu dt + nu dW
    mu, nu = 0.6, 0.8
    X = mu * t + nu * W
    ax = axes[0]
    ax.plot(t, X.T, color=BAND, lw=0.6, alpha=0.35, rasterized=True)
    for path, color in zip(spread(X), (BLUE, ORANGE, PURPLE)):
        ax.plot(t, path, color=color, lw=1.3)
    ax.plot(t, mu * t, color=INK, lw=2.0, label=r"$E[X(t)] = \mu t$")
    ax.set_xlim(0, T)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$X(t)$")
    ax.set_title(r"$dX = \mu\,dt + \nu\,dW$" + f"  $(\\mu = {mu},\\ \\nu = {nu})$")
    ax.legend(loc="upper left")
    despine(ax)

    # dX = mu X dt + nu X dW (幾何ブラウン運動)
    mu, nu, x0 = 0.35, 0.4, 1.0
    X = x0 * np.exp((mu - nu**2 / 2) * t + nu * W)
    ax = axes[1]
    ax.plot(t, X.T, color=BAND, lw=0.6, alpha=0.35, rasterized=True)
    for path, color in zip(spread(X), (BLUE, ORANGE, PURPLE)):
        ax.plot(t, path, color=color, lw=1.3)
    ax.plot(t, x0 * np.exp(mu * t), color=INK, lw=2.0, label=r"$E[X(t)] = X(0)e^{\mu t}$")
    ax.set_xlim(0, T)
    ax.set_ylim(0, np.percentile(X, 99.9))
    ax.set_xlabel("$t$")
    ax.set_title(r"$dX = \mu X\,dt + \nu X\,dW$" + f"  $(\\mu = {mu},\\ \\nu = {nu})$")
    ax.legend(loc="upper left")
    despine(ax)

    fig.tight_layout()
    save(fig, "sde-sde-paths.svg")


# ---------------------------------------------------------------- figure 6


def fig_ito_integral():
    """左端点で評価する (伊藤) か右端点で評価するかで積分の値が変わる。"""
    rng = np.random.RandomState(13)
    fine = 2**16
    t_fine, W_fine = brownian(rng, 1, fine, 1.0)
    W_fine = W_fine[0]

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))

    # 左: 粗い分割で、どちらの端点を使うかを描く
    ax = axes[0]
    n = 8
    idx = np.arange(0, fine + 1, fine // n)
    ts, ws = t_fine[idx], W_fine[idx]
    ax.plot(*thin(t_fine, W_fine), color=BAND, lw=0.7)
    ax.step(ts, ws, where="post", color=BLUE, lw=1.6, label="左端点 $W(t_{k-1})$ (伊藤)")
    ax.step(ts, ws, where="pre", color=ORANGE, lw=1.6, ls="--", label="右端点 $W(t_k)$")
    ax.plot(ts, ws, "o", color=INK, ms=4, zorder=3)
    for x in ts:
        ax.axvline(x, color="#e5e7eb", lw=0.8, zorder=0)
    ax.axhline(0, color="#d1d5db", lw=0.8)
    ax.set_xlim(0, 1)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$W(t)$")
    ax.set_title("被積分関数をどこで評価するか")
    ax.legend(loc="upper left", fontsize=9.5)
    despine(ax)

    # 右: 分割を細かくしたときの収束先
    ax = axes[1]
    ns = 2 ** np.arange(1, 15)
    left, right = [], []
    for n in ns:
        idx = np.arange(0, fine + 1, fine // n)
        w = W_fine[idx]
        dW = np.diff(w)
        left.append(np.sum(w[:-1] * dW))
        right.append(np.sum(w[1:] * dW))
    wT = W_fine[-1]
    ax.plot(ns, left, "o-", color=BLUE, ms=4, lw=1.4, label="左端点の和 (伊藤積分)")
    ax.plot(ns, right, "s-", color=ORANGE, ms=4, lw=1.4, label="右端点の和")
    lo, hi = (wT**2 - 1) / 2, (wT**2 + 1) / 2
    ax.axhline(lo, color=BLUE, lw=1.1, ls="--")
    ax.axhline(hi, color=ORANGE, lw=1.1, ls="--")
    ax.text(
        ns[-1],
        lo - 0.04,
        r"$\frac{1}{2}(W^2(t) - \sigma^2 t)$",
        color=BLUE,
        ha="right",
        va="top",
        fontsize=11,
        bbox=dict(facecolor="white", edgecolor="none", pad=1.5),
    )
    ax.text(
        ns[-1],
        hi + 0.04,
        r"$\frac{1}{2}(W^2(t) + \sigma^2 t)$",
        color=ORANGE,
        ha="right",
        va="bottom",
        fontsize=11,
        bbox=dict(facecolor="white", edgecolor="none", pad=1.5),
    )
    ax.set_xscale("log", base=2)
    # ラベルが枠外に出ないよう、上下に余白を取る
    ax.set_ylim(min(lo, min(left)) - 0.35, max(hi, max(right)) + 0.3)
    ax.set_xlabel("分割数 $n$")
    ax.set_ylabel(r"$\sum_k W(t_\ast)\,\Delta W(t_{k-1})$")
    ax.set_title("$t = 1$ での和の収束先 (差は $\\sigma^2 t$)")
    ax.legend(loc="lower center", fontsize=9.5)
    despine(ax)

    fig.tight_layout()
    save(fig, "sde-ito-integral.svg")


# ---------------------------------------------------------------- figure 7


def fig_quadratic_variation():
    """dt^2 = 0, dt dW = 0, dW^2 = sigma^2 dt の数値的な裏付け。"""
    rng = np.random.RandomState(17)
    fine = 2**18
    t_fine, W_fine = brownian(rng, 1, fine, 1.0)
    W_fine = W_fine[0]

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.9))

    # 左: 二次変分の累積が sigma^2 t に一致していく
    ax = axes[0]
    for n, color in ((2**5, GREEN), (2**9, ORANGE), (2**14, BLUE)):
        idx = np.arange(0, fine + 1, fine // n)
        w = W_fine[idx]
        qv = np.concatenate([[0.0], np.cumsum(np.diff(w) ** 2)])
        ax.plot(*thin(t_fine[idx], qv), color=color, lw=1.4, label=f"$n = {n}$")
    ax.plot([0, 1], [0, 1], color=INK, lw=1.6, ls="--", label=r"$\sigma^2 t$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.35)
    ax.set_xlabel("$t$")
    ax.set_ylabel(r"$\sum_{t_k \leq t} [W(t_k) - W(t_{k-1})]^2$")
    ax.set_title("二次変分は $\\sigma^2 t$ に収束する")
    ax.legend(loc="upper left", fontsize=9.5)
    despine(ax)

    # 右: dt^2, dt dW は消え、dW^2 だけが残る
    ax = axes[1]
    ns = 2 ** np.arange(2, 17)
    dw2, dtdw, dt2 = [], [], []
    for n in ns:
        idx = np.arange(0, fine + 1, fine // n)
        dW = np.diff(W_fine[idx])
        dt = 1.0 / n
        dw2.append(np.sum(dW**2))
        dtdw.append(abs(np.sum(dt * dW)))
        dt2.append(n * dt**2)
    ax.plot(ns, dw2, "o-", color=BLUE, ms=4, lw=1.4, label=r"$\sum (\Delta W)^2$")
    ax.plot(
        ns, dtdw, "s-", color=ORANGE, ms=4, lw=1.4, label=r"$|\sum \Delta t\, \Delta W|$"
    )
    ax.plot(ns, dt2, "^-", color=GREEN, ms=4, lw=1.4, label=r"$\sum (\Delta t)^2$")
    ax.axhline(1.0, color=INK, lw=1.1, ls="--")
    ax.text(ns[0], 1.15, r"$\sigma^2 t = 1$", fontsize=10.5, color=INK)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 6)
    ax.set_xlabel("分割数 $n$")
    ax.set_ylabel("$t = 1$ までの和")
    ax.set_title("$n \\to \\infty$ で残るのは $(\\Delta W)^2$ だけ")
    ax.legend(loc="lower left", fontsize=9.5)
    despine(ax)

    fig.tight_layout()
    save(fig, "sde-quadratic-variation.svg")


FIGURES = (
    fig_random_walk,
    fig_wiener_limit,
    fig_wiener_paths,
    fig_nowhere_differentiable,
    fig_sde_paths,
    fig_ito_integral,
    fig_quadratic_variation,
)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for figure in FIGURES:
        figure()
