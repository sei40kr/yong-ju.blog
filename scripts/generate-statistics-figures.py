"""content/posts/statistics.mdx の図を生成する。

出力先は public/img/stat-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-statistics-figures.py
"""

import math
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


def despine(ax, sides=("top", "right")):
    for side in sides:
        ax.spines[side].set_visible(False)


def stem_bars(ax, xs, ps, color=BLUE, label=None, width=0.62, alpha=0.85):
    return ax.bar(
        xs, ps, width=width, color=color, alpha=alpha, edgecolor="white", label=label
    )


# ---------------------------------------------------------------- 確率質量/密度


def binom_pmf(n, p, k):
    k = np.asarray(k)
    return np.array([math.comb(n, int(i)) * p**i * (1 - p) ** (n - i) for i in k])


def poisson_pmf(lam, k):
    return np.array([lam**i * math.exp(-lam) / math.factorial(int(i)) for i in k])


def geom_pmf(p, k):
    return p * (1 - p) ** (np.asarray(k) - 1)


def normal_pdf(x, mu=0.0, sigma=1.0):
    return np.exp(-((x - mu) ** 2) / (2 * sigma**2)) / (math.sqrt(2 * math.pi) * sigma)


def normal_cdf(x):
    return 0.5 * (1 + np.vectorize(math.erf)(np.asarray(x) / math.sqrt(2)))


def chi2_pdf(x, k):
    return (
        x ** (k / 2 - 1) * np.exp(-x / 2) / (2 ** (k / 2) * math.gamma(k / 2))
    )


def t_pdf(x, n):
    coef = math.gamma((n + 1) / 2) / (math.sqrt(n * math.pi) * math.gamma(n / 2))
    return coef * (1 + x**2 / n) ** (-(n + 1) / 2)


# ---------------------------------------------------------------- figure 1


def fig_central_tendency():
    """平均値・中央値・最頻値。左右対称なら一致し、裾を引くとずれる。"""
    rng = np.random.default_rng(3)
    sym = rng.normal(50, 10, 4000)
    skew = rng.lognormal(mean=math.log(40), sigma=0.55, size=4000)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))

    for ax, data, title, bins in (
        (axes[0], sym, "左右対称な分布", np.linspace(15, 85, 36)),
        (axes[1], skew, "右に裾を引く分布", np.linspace(0, 180, 46)),
    ):
        counts, edges, _ = ax.hist(
            data, bins=bins, color=BLUE, alpha=0.25, edgecolor="white"
        )
        centers = (edges[:-1] + edges[1:]) / 2
        mode = centers[np.argmax(counts)]  # 最頻値は最も度数の多い階級の代表値で近似
        stats = (
            ("最頻値", mode, PURPLE, "-"),
            ("中央値", float(np.median(data)), GREEN, "--"),
            ("平均値", float(np.mean(data)), ORANGE, "-."),
        )
        for i, (name, value, color, ls) in enumerate(stats):
            ax.axvline(value, color=color, ls=ls, lw=1.6)
            ax.annotate(
                f"{name} {value:.0f}",
                xy=(value, counts.max() * (0.97 - 0.13 * i)),
                xytext=(8, 0),
                textcoords="offset points",
                color=color,
                fontsize=9.5,
            )
        ax.set_title(title)
        ax.set_yticks([])
        ax.set_ylim(0, counts.max() * 1.15)
        despine(ax, ("top", "right", "left"))

    axes[0].text(
        0.03,
        0.5,
        "3 つの代表値が\nほぼ一致する",
        transform=axes[0].transAxes,
        fontsize=9.5,
        color=GRAY,
        linespacing=1.5,
    )
    axes[1].annotate(
        "少数の大きい値に\n平均値だけが引っ張られる",
        xy=(125, 12),
        xytext=(78, 175),
        fontsize=9.5,
        color=GRAY,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    fig.suptitle("最頻値 < 中央値 < 平均値 のずれは分布の非対称性を映す", y=1.02)
    save(fig, "stat-central-tendency.svg")


# ---------------------------------------------------------------- figure 2


def fig_dispersion():
    """偏差・分散・標準偏差。平均が同じでもばらつきが違う。"""
    rng = np.random.default_rng(11)
    mu = 60.0
    a = rng.normal(mu, 4, 18)
    b = rng.normal(mu, 12, 18)
    a = a - a.mean() + mu  # 平均をぴったり揃えて比較しやすくする
    b = b - b.mean() + mu

    fig, axes = plt.subplots(2, 1, figsize=(8.0, 4.4), sharex=True)
    for ax, data, label, color in (
        (axes[0], a, "データ A", BLUE),
        (axes[1], b, "データ B", ORANGE),
    ):
        sigma = float(np.sqrt(np.mean((data - mu) ** 2)))
        ax.axvspan(mu - sigma, mu + sigma, color=color, alpha=0.10, zorder=0)
        ax.axvline(mu, color=INK, lw=1.4, zorder=2)
        ys = np.linspace(0.22, 0.78, len(data))
        for x, y in zip(data, ys):
            # 偏差 = 平均からの差。この線分の長さの 2 乗平均が分散。
            ax.plot([mu, x], [y, y], color=color, lw=1.0, alpha=0.55, zorder=1)
        ax.scatter(data, ys, s=32, color=color, edgecolors="white", zorder=3)
        ax.annotate(
            f"$\\sigma = {sigma:.1f}$",
            xy=(mu + sigma, 0.92),
            xytext=(6, 0),
            textcoords="offset points",
            color=color,
            fontsize=10,
        )
        ax.annotate(
            "",
            xy=(mu, 0.9),
            xytext=(mu + sigma, 0.9),
            arrowprops=dict(arrowstyle="<->", color=color, lw=1.0),
        )
        ax.set_ylabel(label)
        ax.set_yticks([])
        ax.set_ylim(0, 1.05)
        despine(ax, ("top", "right", "left"))

    axes[0].text(mu, 1.13, "平均 $\\mathbb{E}[X]$", ha="center", fontsize=10, color=INK)
    axes[0].text(
        0.015,
        0.08,
        "横線 1 本 1 本が偏差 $x_i - \\mathbb{E}[X]$、その 2 乗平均が分散 $\\mathbb{V}[X]$",
        transform=axes[0].transAxes,
        fontsize=9.5,
        color=GRAY,
    )
    axes[1].set_xlabel("値")
    fig.suptitle("平均が同じでも標準偏差はばらつきの大きさを区別する", y=1.0)
    save(fig, "stat-dispersion.svg")


# ---------------------------------------------------------------- figure 3


def fig_quartile():
    """四分位数と箱ひげ図。"""
    rng = np.random.default_rng(7)
    data = np.concatenate(
        [rng.normal(52, 9, 260), rng.normal(72, 6, 90), rng.normal(96, 3, 8)]
    )
    q1, q2, q3 = np.percentile(data, [25, 50, 75])
    iqr = q3 - q1

    fig, axes = plt.subplots(
        2, 1, figsize=(8.0, 4.4), sharex=True, gridspec_kw=dict(height_ratios=[3, 1])
    )

    ax = axes[0]
    counts, edges, _ = ax.hist(
        data, bins=np.linspace(20, 110, 46), color=BLUE, alpha=0.22, edgecolor="white"
    )
    top = counts.max()
    ax.axvspan(q1, q3, color=BLUE, alpha=0.12, zorder=0)
    for value, name, color in ((q1, "$Q_1$", GRAY), (q2, "$Q_2$", GREEN), (q3, "$Q_3$", GRAY)):
        ax.axvline(value, color=color, lw=1.5, ls="--" if color is GRAY else "-")
        ax.text(value, top * 1.06, name, ha="center", color=color, fontsize=10.5)
    ax.annotate(
        "",
        xy=(q1, top * 0.7),
        xytext=(q3, top * 0.7),
        arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.2),
    )
    ax.text(
        (q1 + q3) / 2,
        top * 0.78,
        f"$\\text{{IQR}} = Q_3 - Q_1 = {iqr:.1f}$",
        ha="center",
        color=BLUE,
        fontsize=10,
    )
    ax.set_yticks([])
    ax.set_ylim(0, top * 1.22)
    despine(ax, ("top", "right", "left"))
    ax.set_title("四分位数は下位 25% / 50% / 75% の位置でデータを 4 等分する")

    ax = axes[1]
    bp = ax.boxplot(
        data,
        vert=False,
        widths=0.5,
        patch_artist=True,
        flierprops=dict(marker="o", markersize=3.5, markerfacecolor=ORANGE, markeredgecolor="none"),
        medianprops=dict(color=GREEN, lw=1.8),
        boxprops=dict(facecolor="#dbeafe", edgecolor=GRAY),
        whiskerprops=dict(color=GRAY),
        capprops=dict(color=GRAY),
    )
    del bp
    ax.set_yticks([])
    ax.set_xlabel("値")
    ax.text(
        0.015, 0.05, "箱ひげ図", transform=ax.transAxes, fontsize=9.5, color=GRAY
    )
    despine(ax, ("top", "right", "left"))
    save(fig, "stat-quartile.svg")


# ---------------------------------------------------------------- figure 4


def fig_covariance():
    """共分散の符号は偏差積の符号がどちらに偏るかで決まる。"""
    rng = np.random.default_rng(2)

    def make(rho, n=40):
        z1 = rng.normal(size=n)
        z2 = rng.normal(size=n)
        x = z1
        y = rho * z1 + math.sqrt(1 - rho**2) * z2
        return x * 1.0, y * 1.0

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 4.3))
    for ax, rho, title in ((axes[0], 0.85, "正の共分散"), (axes[1], -0.85, "負の共分散")):
        x, y = make(rho)
        mx, my = x.mean(), y.mean()
        cov = float(np.mean((x - mx) * (y - my)))
        lim = 3.0
        ax.axhspan(my, my + lim, xmin=0.5, xmax=1.0, color=BLUE, alpha=0.07)
        ax.axhspan(my - lim, my, xmin=0.0, xmax=0.5, color=BLUE, alpha=0.07)
        ax.axhspan(my, my + lim, xmin=0.0, xmax=0.5, color=ORANGE, alpha=0.07)
        ax.axhspan(my - lim, my, xmin=0.5, xmax=1.0, color=ORANGE, alpha=0.07)
        ax.axvline(mx, color=INK, lw=1.0)
        ax.axhline(my, color=INK, lw=1.0)

        pos = (x - mx) * (y - my) > 0
        ax.scatter(x[pos], y[pos], s=34, color=BLUE, edgecolors="white", zorder=3)
        ax.scatter(x[~pos], y[~pos], s=34, color=ORANGE, edgecolors="white", zorder=3)

        # 代表点 1 つだけ偏差積を長方形として描く
        idx = int(np.argmax((x - mx) ** 2 + (y - my) ** 2))
        ax.add_patch(
            Rectangle(
                (mx, my),
                x[idx] - mx,
                y[idx] - my,
                facecolor=BLUE if pos[idx] else ORANGE,
                alpha=0.22,
                edgecolor=BLUE if pos[idx] else ORANGE,
                lw=1.0,
                zorder=2,
            )
        )
        ax.annotate(
            "$(x_i-\\mathbb{E}[X])(y_i-\\mathbb{E}[Y])$",
            xy=((mx + x[idx]) / 2, (my + y[idx]) / 2),
            xytext=(0, 10 if y[idx] > my else -22),
            textcoords="offset points",
            ha="center",
            fontsize=9,
            color=INK,
        )
        ax.text(mx + 0.12, lim - 0.35, "$+$", color=BLUE, fontsize=13)
        ax.text(-lim + 0.12, lim - 0.35, "$-$", color=ORANGE, fontsize=13)
        ax.text(-lim + 0.12, -lim + 0.15, "$+$", color=BLUE, fontsize=13)
        ax.text(mx + 0.12, -lim + 0.15, "$-$", color=ORANGE, fontsize=13)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")
        ax.set_title(f"{title}  $\\text{{Cov}}[X,Y] = {cov:+.2f}$")
        despine(ax, ("top", "right", "bottom", "left"))

    fig.legend(
        handles=[
            Line2D([], [], color=BLUE, marker="o", ls="none", label="偏差積が正"),
            Line2D([], [], color=ORANGE, marker="o", ls="none", label="偏差積が負"),
        ],
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, -0.03),
    )
    save(fig, "stat-covariance.svg")


# ---------------------------------------------------------------- figure 5


def fig_correlation():
    """相関係数の値と散布図の見え方。"""
    rng = np.random.default_rng(19)
    n = 120

    def gauss(rho):
        z1, z2 = rng.normal(size=n), rng.normal(size=n)
        return z1, rho * z1 + math.sqrt(1 - rho**2) * z2

    panels = [gauss(r) for r in (0.95, 0.6, 0.0, -0.6, -0.95)]
    # x を左右対称に取ると x と x^2 の相関は厳密に 0 になる (非線形だが無相関)
    x = np.linspace(-2, 2, n)
    panels.append((x, x**2 - 2 + rng.normal(0, 0.35, n)))

    titles = [None] * 5 + ["非線形な関係"]

    fig, axes = plt.subplots(2, 3, figsize=(8.4, 5.4))
    for ax, (px, py), title in zip(axes.ravel(), panels, titles):
        r = float(np.corrcoef(px, py)[0, 1])
        color = BLUE if r > 0.05 else ORANGE if r < -0.05 else GRAY
        ax.scatter(px, py, s=18, color=color, alpha=0.7, edgecolors="none")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(
            f"$r_{{xy}} = {r:+.2f}$" if title is None else f"{title}  $r_{{xy}} = {r:+.2f}$",
            fontsize=11,
        )
        for side in ax.spines.values():
            side.set_color(LIGHT)

    fig.suptitle("相関係数は直線的な関係の向きと強さを $-1 \\sim 1$ で測る", y=0.99)
    fig.tight_layout()
    fig.text(
        0.5,
        -0.02,
        "右下: $r_{xy}=0$ は「直線的な関係がない」ことを言うだけで、関係がないことは意味しない",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "stat-correlation.svg")


# ---------------------------------------------------------------- figure 6


def fig_standardization():
    """標準化すると単位の違う変数を同じ物差しで比べられる。"""
    rng = np.random.default_rng(5)
    height = rng.normal(170, 6, 600)
    weight = rng.normal(63, 11, 600)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))

    ax = axes[0]
    ax.hist(height, bins=30, color=BLUE, alpha=0.45, edgecolor="white", label="身長 (cm)")
    ax.hist(weight, bins=30, color=ORANGE, alpha=0.45, edgecolor="white", label="体重 (kg)")
    ax.set_title("標準化前 — 単位も散らばりもばらばら")
    ax.set_yticks([])
    ax.legend(fontsize=9.5)
    despine(ax, ("top", "right", "left"))

    ax = axes[1]
    for data, color, label in ((height, BLUE, "身長"), (weight, ORANGE, "体重")):
        z = (data - data.mean()) / data.std()
        ax.hist(
            z,
            bins=np.linspace(-4, 4, 33),
            color=color,
            alpha=0.45,
            edgecolor="white",
            label=f"{label} の $z$",
        )
    ax.axvline(0, color=INK, lw=1.0)
    ax.set_title("標準化後 — 平均 $0$, 標準偏差 $1$")
    ax.set_xlabel("$z = (x - \\mu) / \\sigma$")
    ax.set_yticks([])
    ax.legend(fontsize=9.5)
    despine(ax, ("top", "right", "left"))
    save(fig, "stat-standardization.svg")


# ---------------------------------------------------------------- figure 7


def fig_population_sample():
    """母集団・標本・標本平均の分布。"""
    rng = np.random.default_rng(23)
    mu, sigma, n = 60.0, 12.0, 25
    population = rng.normal(mu, sigma, 200000)

    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))

    ax = axes[0]
    xs = np.linspace(15, 105, 400)
    ax.plot(xs, normal_pdf(xs, mu, sigma), color=GRAY, lw=1.6)
    ax.fill_between(xs, normal_pdf(xs, mu, sigma), color=GRAY, alpha=0.12)
    ax.axvline(mu, color=INK, lw=1.2)
    ax.text(mu + 1.5, normal_pdf(mu, mu, sigma) * 1.02, "母平均 $\\mu$", fontsize=10)
    for i, (color, y) in enumerate(((BLUE, 0.0075), (ORANGE, 0.0047), (GREEN, 0.0019))):
        sample = rng.choice(population, n, replace=False)
        ax.scatter(sample, np.full(n, y), s=16, color=color, alpha=0.7, edgecolors="none")
        ax.scatter(
            [sample.mean()],
            [y],
            s=70,
            marker="v",
            color=color,
            edgecolors="white",
            linewidths=0.6,
            zorder=3,
        )
        ax.text(16, y, f"標本 {i + 1}", fontsize=9, color=color, va="center")
    ax.text(
        104,
        0.0112,
        "▼ は標本平均 $\\bar{X}$",
        fontsize=9,
        color=GRAY,
        ha="right",
        va="center",
    )
    ax.set_title(f"母集団から大きさ $n={n}$ の標本を取る")
    ax.set_xlim(12, 108)
    ax.set_yticks([])
    ax.set_ylim(-0.001, 0.0385)
    despine(ax, ("top", "right", "left"))

    ax = axes[1]
    means = rng.normal(mu, sigma, (20000, n)).mean(axis=1)
    ax.hist(
        means,
        bins=np.linspace(45, 75, 61),
        density=True,
        color=BLUE,
        alpha=0.35,
        edgecolor="white",
        label="標本平均 $\\bar{X}$ の分布",
    )
    ax.plot(xs, normal_pdf(xs, mu, sigma), color=GRAY, lw=1.4, label="母集団の分布")
    ax.plot(
        xs,
        normal_pdf(xs, mu, sigma / math.sqrt(n)),
        color=BLUE,
        lw=1.6,
        ls="--",
        label="$\\text{N}(\\mu, \\sigma^2/n)$",
    )
    ax.axvline(mu, color=INK, lw=1.0)
    ax.set_xlim(30, 92)
    ax.set_ylim(0, 0.215)
    ax.set_yticks([])
    ax.set_title("標本平均は母平均のまわりに集まる")
    ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(-0.02, 1.02))
    despine(ax, ("top", "right", "left"))

    fig.suptitle("標本統計量のばらつきは $n$ を増やすと $1/\\sqrt{n}$ で縮む", y=1.02)
    save(fig, "stat-population-sample.svg")


# ---------------------------------------------------------------- figure 8


def fig_pmf_pdf():
    """確率質量関数は高さ、確率密度関数は面積が確率。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))

    ax = axes[0]
    ks = np.arange(0, 11)
    ps = binom_pmf(10, 0.4, ks)
    bars = stem_bars(ax, ks, ps)
    bars[3].set_color(ORANGE)
    ax.annotate(
        "$P[X=3] = f(3)$\n棒の高さがそのまま確率",
        xy=(3, ps[3]),
        xytext=(5.0, 0.245),
        fontsize=9.5,
        color=INK,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    ax.set_xticks(ks)
    ax.set_title("離散型 — 確率質量関数 $f(x)$")
    ax.set_xlabel("$x$")
    ax.set_ylim(0, 0.31)
    despine(ax)

    ax = axes[1]
    xs = np.linspace(-4, 4, 500)
    ys = normal_pdf(xs)
    ax.plot(xs, ys, color=BLUE, lw=1.8)
    mask = (xs >= -0.5) & (xs <= 1.5)
    ax.fill_between(xs[mask], ys[mask], color=ORANGE, alpha=0.35)
    prob = float(normal_cdf(1.5) - normal_cdf(-0.5))
    ax.annotate(
        f"$P[x_0 \\leq X \\leq x_1] = \\int_{{x_0}}^{{x_1}} f(x)dx = {prob:.2f}$\n"
        "面積が確率 (高さは確率ではない)",
        xy=(0.6, 0.16),
        xytext=(-3.95, 0.44),
        fontsize=9.5,
        color=INK,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    ax.set_xticks([-0.5, 1.5])
    ax.set_xticklabels(["$x_0$", "$x_1$"])
    ax.set_title("連続型 — 確率密度関数 $f(x)$")
    ax.set_xlabel("$x$")
    ax.set_ylim(0, 0.52)
    despine(ax)
    save(fig, "stat-pmf-pdf.svg")


# ---------------------------------------------------------------- figure 9


def fig_binomial():
    """ベルヌーイ分布と二項分布。"""
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.4))

    p = 0.3
    ax = axes[0]
    stem_bars(ax, [0, 1], [1 - p, p], width=0.42)
    ax.set_xticks([0, 1])
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, 0.95)
    ax.set_title(f"$\\text{{Bern}}({p})$")
    ax.text(1, p + 0.04, "$p$", ha="center", color=BLUE)
    ax.text(0, 1 - p + 0.04, "$1-p$", ha="center", color=BLUE)
    despine(ax)

    ax = axes[1]
    n = 10
    ks = np.arange(0, n + 1)
    ps = binom_pmf(n, p, ks)
    stem_bars(ax, ks, ps)
    mean, sd = n * p, math.sqrt(n * p * (1 - p))
    ax.axvline(mean, color=ORANGE, lw=1.4)
    ax.annotate(
        "",
        xy=(mean - sd, 0.30),
        xytext=(mean + sd, 0.30),
        arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.0),
    )
    ax.text(mean, 0.315, "$\\pm\\sigma$", ha="center", color=ORANGE, fontsize=9.5)
    ax.text(mean + 0.3, 0.26, "$\\mathbb{E}[X]=np$", color=ORANGE, fontsize=9.5)
    ax.set_xticks(ks[::2])
    ax.set_ylim(0, 0.37)
    ax.set_title(f"$\\text{{Bin}}({n},{p})$ — 成功回数")
    despine(ax)

    ax = axes[2]
    for i, (n_, color) in enumerate(((5, GREEN), (15, BLUE), (40, PURPLE))):
        ks = np.arange(0, n_ + 1)
        ax.plot(
            ks,
            binom_pmf(n_, p, ks),
            marker="o",
            ms=3.2,
            lw=1.2,
            color=color,
            label=f"$n={n_}$",
        )
        del i
    ax.set_xlim(-0.5, 26)
    ax.set_title("$n$ を増やすと山は右へ広がる")
    ax.legend(fontsize=9.5)
    despine(ax)

    for ax in axes:
        ax.set_xlabel("$x$ (成功回数)")
    fig.tight_layout()
    save(fig, "stat-binomial.svg")


# ---------------------------------------------------------------- figure 10


def fig_geometric():
    """幾何分布。初めて成功するまでの試行回数。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4))

    ks = np.arange(1, 21)
    for ax, p, color in ((axes[0], 0.5, BLUE), (axes[1], 0.2, PURPLE)):
        ps = geom_pmf(p, ks)
        stem_bars(ax, ks, ps, color=color)
        ax.axvline(1 / p, color=ORANGE, lw=1.4, ls="--")
        ax.text(
            1 / p + 0.4,
            ps.max() * 0.85,
            f"$\\mathbb{{E}}[X]=1/p={1 / p:.0f}$",
            color=ORANGE,
            fontsize=9.5,
        )
        ax.set_title(f"$\\text{{Ge}}({p})$")
        ax.set_xlabel("$x$ (初成功までの試行回数)")
        ax.set_xticks([1, 5, 10, 15, 20])
        despine(ax)

    fig.suptitle("確率は公比 $1-p$ の等比数列で単調に減る", y=1.02)
    fig.tight_layout()
    save(fig, "stat-geometric.svg")


# ---------------------------------------------------------------- figure 11


def fig_poisson():
    """ポアソン分布と、二項分布からの極限。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))

    ax = axes[0]
    ks = np.arange(0, 21)
    for lam, color in ((1, GREEN), (4, BLUE), (10, PURPLE)):
        ax.plot(
            ks,
            poisson_pmf(lam, ks),
            marker="o",
            ms=3.4,
            lw=1.3,
            color=color,
            label=f"$\\lambda={lam}$",
        )
    ax.set_title("$\\text{Poi}(\\lambda)$ — 平均も分散も $\\lambda$")
    ax.set_xlabel("$x$ (単位時間あたりの件数)")
    ax.legend(fontsize=9.5)
    despine(ax)

    ax = axes[1]
    lam = 3
    ks = np.arange(0, 13)
    stem_bars(ax, ks, poisson_pmf(lam, ks), color=ORANGE, width=0.72, alpha=0.35)
    for n, color, ls in ((5, GREEN, ":"), (20, BLUE, "--"), (200, PURPLE, "-")):
        ax.plot(
            ks[ks <= n],
            binom_pmf(n, lam / n, ks[ks <= n]),
            marker="o",
            ms=3.0,
            lw=1.2,
            ls=ls,
            color=color,
            label=f"$\\text{{Bin}}({n}, {lam}/{n})$",
        )
    ax.plot([], [], color=ORANGE, lw=6, alpha=0.35, label=f"$\\text{{Poi}}({lam})$")
    ax.set_title("$np=\\lambda$ を保って $n\\to\\infty$")
    ax.set_xlabel("$x$")
    ax.legend(fontsize=9)
    despine(ax)
    fig.tight_layout()
    save(fig, "stat-poisson.svg")


# ---------------------------------------------------------------- figure 12


def fig_exponential():
    """同じポアソン過程を、件数で見るか間隔で見るか。"""
    rng = np.random.default_rng(31)
    lam = 3.0
    fig = plt.figure(figsize=(8.6, 5.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 2.1], hspace=0.55, wspace=0.25)

    # 上段: 事象の発生時刻を並べたタイムライン
    ax = fig.add_subplot(gs[0, :])
    span = 8.0
    gaps = rng.exponential(1 / lam, 400)
    times = np.cumsum(gaps)
    times = times[times < span]
    ax.hlines(0, 0, span, color=LIGHT, lw=1.4)
    ax.vlines(times, -0.28, 0.28, color=BLUE, lw=1.6)
    for t in range(int(span) + 1):
        ax.vlines(t, -0.62, 0.62, color=GRAY, lw=0.8, ls=":")

    # 間隔が見やすいように、いちばん広く空いたところを選んで寸法線を引く
    gap_idx = int(np.argmax(np.diff(times)))
    left, right = times[gap_idx], times[gap_idx + 1]
    ax.annotate(
        "",
        xy=(left, 0.45),
        xytext=(right, 0.45),
        arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.2),
    )
    ax.text((left + right) / 2, 0.62, "発生間隔", ha="center", color=ORANGE, fontsize=9.5)

    # 単位区間 1 本を取り出して「件数」を数える対象を示す
    lo, hi = 4.0, 5.0
    ax.axvspan(lo, hi, color=BLUE, alpha=0.10)
    ax.text(
        (lo + hi) / 2,
        -0.95,
        f"この区間の本数 = 件数 ({int(((times >= lo) & (times < hi)).sum())} 件)",
        ha="center",
        color=BLUE,
        fontsize=9.5,
    )
    ax.set_xlim(-0.1, span + 0.1)
    ax.set_ylim(-1.1, 1.0)
    ax.set_yticks([])
    ax.set_xlabel("時刻")
    ax.set_title(f"平均 $\\lambda={lam:.0f}$ 回 / 単位時間で起こる事象")
    despine(ax, ("top", "right", "left"))

    # 上のタイムラインは 1 本だけなので、分布は別途たくさんシミュレートして描く
    sim_gaps = rng.exponential(1 / lam, 60000)
    sim_times = np.cumsum(sim_gaps)
    edges = np.arange(0, sim_times[-1], 1.0)
    sim_counts = np.diff(np.searchsorted(sim_times, edges))

    ax = fig.add_subplot(gs[1, 0])
    ks = np.arange(0, 13)
    ax.hist(
        sim_counts,
        bins=np.arange(-0.5, 12.6, 1),
        density=True,
        color=BLUE,
        alpha=0.35,
        edgecolor="white",
        label="シミュレーション",
    )
    ax.plot(ks, poisson_pmf(lam, ks), marker="o", ms=3.6, lw=1.4, color=INK, label="$\\text{Poi}(\\lambda)$")
    ax.set_title("件数の分布 → ポアソン分布")
    ax.set_xlabel("単位時間あたりの件数")
    ax.legend(fontsize=9)
    despine(ax)

    ax = fig.add_subplot(gs[1, 1])
    xs = np.linspace(0, 2.2, 300)
    ax.hist(
        sim_gaps,
        bins=np.linspace(0, 2.2, 45),
        density=True,
        color=ORANGE,
        alpha=0.35,
        edgecolor="white",
        label="シミュレーション",
    )
    ax.plot(xs, lam * np.exp(-lam * xs), color=INK, lw=1.6, label="$\\text{Ex}(\\lambda)$")
    ax.axvline(1 / lam, color=GREEN, lw=1.3, ls="--")
    ax.text(1 / lam + 0.05, 2.3, "$\\mathbb{E}[X]=1/\\lambda$", color=GREEN, fontsize=9.5)
    ax.set_title("間隔の分布 → 指数分布")
    ax.set_xlabel("発生間隔")
    ax.legend(fontsize=9)
    despine(ax)
    save(fig, "stat-exponential.svg")


# ---------------------------------------------------------------- figure 13


def fig_normal():
    """正規分布のパラメータと 68-95-99.7 則。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))

    ax = axes[0]
    xs = np.linspace(-8, 10, 600)
    for mu, sigma, color in ((0, 1, BLUE), (0, 2.2, PURPLE), (3, 1, GREEN)):
        ax.plot(
            xs,
            normal_pdf(xs, mu, sigma),
            color=color,
            lw=1.7,
            label=f"$\\mu={mu},\\ \\sigma={sigma}$",
        )
    ax.set_title("$\\mu$ は位置、$\\sigma$ は幅を決める")
    ax.set_xlabel("$x$")
    ax.set_yticks([])
    ax.legend(fontsize=9.5)
    despine(ax, ("top", "right", "left"))

    ax = axes[1]
    xs = np.linspace(-4, 4, 600)
    ys = normal_pdf(xs)
    ax.plot(xs, ys, color=INK, lw=1.7)
    # 帯が重ならないように、内側から順に 0〜1σ, 1〜2σ, 2〜3σ を塗り分ける
    for k, color, alpha in ((1, ORANGE, 0.30), (2, BLUE, 0.22), (3, PURPLE, 0.16)):
        m = (np.abs(xs) <= k) & (np.abs(xs) >= k - 1)
        if k == 1:
            ax.fill_between(xs[m], ys[m], color=color, alpha=alpha, lw=0)
        else:  # 中心をまたがないよう左右に分けて塗る
            for side in (xs >= 0, xs < 0):
                ax.fill_between(xs[m & side], ys[m & side], color=color, alpha=alpha, lw=0)
        prob = float(normal_cdf(k) - normal_cdf(-k))
        ax.annotate(
            f"$\\pm{k}\\sigma$ に {prob * 100:.1f}%",
            xy=(k - 0.4, normal_pdf(k - 0.4) * 0.5),
            xytext=(24, 16 + 26 * (3 - k)),
            textcoords="offset points",
            fontsize=9.5,
            color=color,
            arrowprops=dict(arrowstyle="-", color=color, lw=0.8),
        )
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_xticklabels(["$-3\\sigma$", "", "$-\\sigma$", "$\\mu$", "$\\sigma$", "", "$3\\sigma$"])
    ax.set_title("標準正規分布 $\\text{N}(0,1)$")
    ax.set_yticks([])
    ax.set_ylim(0, 0.52)
    despine(ax, ("top", "right", "left"))
    fig.tight_layout()
    save(fig, "stat-normal.svg")


# ---------------------------------------------------------------- figure 14


def fig_chi2_t():
    """カイ二乗分布と t 分布を、定義どおりの標本から作って確かめる。"""
    rng = np.random.default_rng(43)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))

    ax = axes[0]
    xs = np.linspace(0.02, 18, 600)
    for n, color in ((1, GREEN), (2, BLUE), (5, PURPLE), (10, ORANGE)):
        ax.plot(xs, chi2_pdf(xs, n), color=color, lw=1.6, label=f"$n={n}$")
    sample = (rng.normal(size=(40000, 5)) ** 2).sum(axis=1)  # 定義: N(0,1) の 2 乗和
    ax.hist(
        sample,
        bins=np.linspace(0, 18, 60),
        density=True,
        color=PURPLE,
        alpha=0.18,
        edgecolor="white",
        label="$\\sum_{i=1}^{5} Z_i^2$ の実験",
    )
    ax.set_ylim(0, 0.55)
    ax.set_xlabel("$x$")
    ax.set_title("$\\chi^2(n)$ — 標準正規の 2 乗和")
    ax.set_yticks([])
    ax.legend(fontsize=9)
    despine(ax, ("top", "right", "left"))

    ax = axes[1]
    xs = np.linspace(-5, 5, 600)
    ax.plot(xs, normal_pdf(xs), color=INK, lw=1.8, ls="--", label="$\\text{N}(0,1)$")
    for n, color in ((1, GREEN), (3, BLUE), (10, PURPLE)):
        ax.plot(xs, t_pdf(xs, n), color=color, lw=1.5, label=f"$t({n})$")
    ax.set_xlabel("$t$")
    ax.set_title("$t(n)$ — $n$ が小さいほど裾が重い")
    ax.set_yticks([])
    ax.set_ylim(0, 0.44)
    ax.legend(fontsize=9)
    ax.annotate(
        "自由度が小さいほど\n極端な値が出やすい",
        xy=(3.3, t_pdf(3.3, 1)),
        xytext=(1.15, 0.30),
        fontsize=9,
        color=GRAY,
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color=LIGHT, lw=0.9),
    )
    despine(ax, ("top", "right", "left"))
    fig.tight_layout()
    save(fig, "stat-chi2-t.svg")


# ---------------------------------------------------------------- figure 15


def fig_inequalities():
    """マルコフ・チェビシェフの不等式が与える上界と実際の確率。"""
    rng = np.random.default_rng(101)
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8))

    # マルコフ: 非負の確率変数 (ここでは Ex(1))
    ax = axes[0]
    cs = np.linspace(1.0, 5.0, 60)
    actual = np.exp(-cs)  # P[X >= c] (Ex(1))
    bound = 1.0 / cs  # E[X] / c = 1 / c
    ax.plot(cs, bound, color=ORANGE, lw=1.8, label="上界 $\\mathbb{E}[X]/c$")
    ax.plot(cs, actual, color=BLUE, lw=1.8, label="実際の $P[X \\geq c]$")
    ax.fill_between(cs, actual, bound, color=ORANGE, alpha=0.12)
    ax.set_xlabel("$c$")
    ax.set_ylim(0, 1.05)
    ax.set_title("マルコフの不等式 ($X \\sim \\text{Ex}(1)$)")
    ax.legend(fontsize=9.5)
    ax.text(
        2.4,
        0.62,
        "分布の形を一切使わずに\n裾の確率を上から押さえる",
        fontsize=9,
        color=GRAY,
        linespacing=1.5,
    )
    despine(ax)

    # チェビシェフ: 分布によらず 1/a^2 で押さえられる
    ax = axes[1]
    a = np.linspace(1.0, 4.0, 40)
    ax.plot(a, 1 / a**2, color=ORANGE, lw=1.8, label="上界 $1/a^2$")
    for name, data, color in (
        ("$\\text{N}(0,1)$", rng.normal(size=400000), BLUE),
        ("$\\text{Ex}(1)$", rng.exponential(size=400000), GREEN),
        ("一様分布", rng.uniform(-1, 1, 400000), PURPLE),
    ):
        z = (data - data.mean()) / data.std()
        ax.plot(
            a,
            [(np.abs(z) >= ai).mean() for ai in a],
            color=color,
            lw=1.4,
            label=name,
        )
    ax.set_xlabel("$a$")
    ax.set_ylim(0, 1.05)
    ax.set_title("チェビシェフの不等式")
    ax.set_ylabel("$P[|X-\\mu| \\geq a\\sigma]$")
    ax.legend(fontsize=9)
    despine(ax)
    fig.tight_layout()
    save(fig, "stat-inequalities.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_central_tendency()
    fig_dispersion()
    fig_quartile()
    fig_covariance()
    fig_correlation()
    fig_standardization()
    fig_population_sample()
    fig_pmf_pdf()
    fig_binomial()
    fig_geometric()
    fig_poisson()
    fig_exponential()
    fig_normal()
    fig_chi2_t()
    fig_inequalities()
