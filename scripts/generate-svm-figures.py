"""content/posts/support-vector-machine.mdx の図を生成する。

出力先は public/img/svm-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy scikit-learn
    .venv/bin/python scripts/generate-svm-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from sklearn.svm import SVC

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

POS = "#2563eb"  # クラス +1
NEG = "#ea580c"  # クラス -1
BOUNDARY = "#111827"
MARGIN_FILL = "#94a3b8"

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


def scatter(ax, X, y, size=42, sv_mask=None):
    for label, color, marker in ((1, POS, "o"), (-1, NEG, "s")):
        m = y == label
        ax.scatter(
            X[m, 0],
            X[m, 1],
            c=color,
            marker=marker,
            s=size,
            linewidths=0.8,
            edgecolors="white",
            zorder=3,
            label=f"$y_i = {label:+d}$",
        )
    if sv_mask is not None:
        ax.scatter(
            X[sv_mask, 0],
            X[sv_mask, 1],
            s=size * 4.5,
            facecolors="none",
            edgecolors=BOUNDARY,
            linewidths=1.2,
            zorder=2,
        )


def shade(ax, zz, xlim, ylim, rgb_where_true, rgb_where_false, alpha, mask=None):
    """決定領域の塗りは SVG のパスではなくラスタで描く (ファイルサイズ対策)。"""
    rgba = np.zeros(zz.shape + (4,))
    rgba[..., :3] = np.where(
        (zz > 0)[..., None], to_rgb(rgb_where_true), to_rgb(rgb_where_false)
    )
    rgba[..., 3] = alpha if mask is None else np.where(mask, alpha, 0.0)
    ax.imshow(
        rgba,
        extent=(*xlim, *ylim),
        origin="lower",
        interpolation="nearest",
        aspect="auto",
        zorder=0,
    )


def draw_boundary(ax, clf, xlim, ylim, margins=True, fill=False, n=300):
    xx, yy = np.meshgrid(
        np.linspace(*xlim, n),
        np.linspace(*ylim, n),
    )
    zz = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    if fill:
        shade(ax, zz, xlim, ylim, POS, NEG, 0.08)
    if margins:
        shade(ax, zz, xlim, ylim, MARGIN_FILL, MARGIN_FILL, 0.15, mask=np.abs(zz) <= 1)
    levels = [-1, 0, 1] if margins else [0]
    styles = ["--", "-", "--"] if margins else ["-"]
    widths = [1.0, 1.8, 1.0] if margins else [1.8]
    ax.contour(
        xx, yy, zz, levels=levels, colors=BOUNDARY, linestyles=styles, linewidths=widths
    )


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


def class_handles():
    return [
        Line2D(
            [],
            [],
            color=color,
            ls="none",
            marker=marker,
            markersize=7,
            label=f"$y_i = {label}$",
        )
        for label, color, marker in (("+1", POS, "o"), ("-1", NEG, "s"))
    ]


def class_legend(fig, y_offset=-0.02):
    fig.legend(
        handles=class_handles(),
        loc="lower center",
        ncol=2,
        bbox_to_anchor=(0.5, y_offset),
    )


def separable_data(seed=5, n=14):
    rng = np.random.RandomState(seed)
    Xp = rng.randn(n, 2) * 0.55 + np.array([2.1, 2.4])
    Xn = rng.randn(n, 2) * 0.55 + np.array([-0.5, -0.3])
    X = np.vstack([Xp, Xn])
    y = np.hstack([np.ones(n), -np.ones(n)])
    return X, y


def overlapping_data(seed=1, n=25, center=1.4, scale=0.9):
    rng = np.random.RandomState(seed)
    Xp = rng.randn(n, 2) * scale + np.array([center, center + 0.1])
    Xn = rng.randn(n, 2) * scale + np.array([-center + 0.8, -center + 0.9])
    X = np.vstack([Xp, Xn])
    y = np.hstack([np.ones(n), -np.ones(n)])
    return X, y


# ---------------------------------------------------------------- figure 1


def fig_hyperplanes():
    X, y = separable_data()
    xlim, ylim = (-2.6, 4.4), (-2.4, 4.4)

    # 記事の本文幅は 768px なので、これより大きくすると図中の文字が縮む
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 4.0))

    ax = axes[0]
    xs = np.linspace(*xlim, 2)
    drawn = 0
    for x0, y0, slope in (
        (0.8, 1.05, -1.0),
        (0.4, 1.5, -0.45),
        (1.2, 0.7, -2.4),
        (0.95, 1.0, -8.0),
        (0.6, 1.3, -0.15),
    ):
        above = X[:, 1] > y0 + slope * (X[:, 0] - x0)
        pos, neg = above[y == 1], above[y == -1]
        separates = (pos.all() and not neg.any()) or (not pos.any() and neg.all())
        if not separates:
            continue  # 分離できていない候補は描かない
        ax.plot(xs, y0 + slope * (xs - x0), color="#6b7280", lw=1.1, alpha=0.85, zorder=1)
        drawn += 1
    assert drawn >= 4, drawn
    scatter(ax, X, y)
    bare(ax, xlim, ylim, "分離超平面は無数にある")

    ax = axes[1]
    clf = SVC(kernel="linear", C=1e6).fit(X, y)
    draw_boundary(ax, clf, xlim, ylim)
    sv = np.zeros(len(X), dtype=bool)
    sv[clf.support_] = True
    scatter(ax, X, y, sv_mask=sv)
    bare(ax, xlim, ylim, "マージン最大の超平面はただ 1 つ")

    # 図中に置くと決定境界と重なるので、凡例は figure の下にまとめる
    fig.legend(
        handles=class_handles()
        + [
            Line2D([], [], color=BOUNDARY, lw=1.8, label="決定境界 $f(x)=0$"),
            Line2D([], [], color=BOUNDARY, lw=1.0, ls="--", label="マージン境界"),
            Line2D(
                [],
                [],
                color=BOUNDARY,
                lw=1.2,
                ls="none",
                marker="o",
                markerfacecolor="none",
                markersize=9,
                label="サポートベクター",
            ),
        ],
        loc="lower center",
        ncol=5,
        fontsize=9.5,
        bbox_to_anchor=(0.5, -0.04),
    )

    save(fig, "svm-hyperplanes.svg")


# ---------------------------------------------------------------- figure 2


def fig_margin():
    X, y = separable_data()
    clf = SVC(kernel="linear", C=1e6).fit(X, y)
    w = clf.coef_[0]
    b = clf.intercept_[0]
    norm = np.linalg.norm(w)

    xlim, ylim = (-2.6, 4.4), (-2.4, 4.4)
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    draw_boundary(ax, clf, xlim, ylim)
    sv = np.zeros(len(X), dtype=bool)
    sv[clf.support_] = True
    scatter(ax, X, y, sv_mask=sv)

    unit = w / norm  # 決定境界の単位法線ベクトル
    along = np.array([-w[1], w[0]]) / norm  # 決定境界に沿う向き (左上を向くようにする)
    if along[0] > 0:
        along = -along
    origin = -b * w / norm**2  # 決定境界上の点

    # 決定境界からマージン境界までの距離が 1 / ||w||
    anchor = origin - along * 0.6
    ax.annotate(
        "",
        xy=anchor - unit / norm,
        xytext=anchor,
        arrowprops=dict(arrowstyle="<->", color=BOUNDARY, lw=1.3, shrinkA=0, shrinkB=0),
    )
    ax.text(
        *(anchor - unit / norm * 0.5 - along * 0.55),
        r"$\gamma = \dfrac{1}{\Vert w \Vert}$",
        fontsize=13,
        ha="left",
        va="center",
    )

    # 法線ベクトル w
    tail = origin - along * 2.9
    ax.annotate(
        "",
        xy=tail + unit * 1.1,
        xytext=tail,
        arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=1.7),
    )
    ax.text(
        *(tail + unit * 1.25 - along * 0.1),
        r"$w$",
        color="#7c3aed",
        fontsize=13,
        ha="left",
        va="center",
    )

    # 決定境界に沿ってラベルを置く
    ax.text(
        *(origin + along * 3.3 + unit * 0.18),
        r"$f(x) = w^{\top} x + b = 0$",
        fontsize=11,
        color=BOUNDARY,
        ha="center",
        va="bottom",
        rotation=np.degrees(np.arctan2(along[1], along[0])) + 180,
        rotation_mode="anchor",
    )
    bare(ax, xlim, ylim, "マージンとサポートベクター")
    class_legend(fig)
    save(fig, "svm-margin.svg")


# ---------------------------------------------------------------- figure 3


def fig_slack():
    X, y = overlapping_data(seed=4, n=22, center=1.0, scale=0.95)
    clf = SVC(kernel="linear", C=0.5).fit(X, y)
    w = clf.coef_[0]
    norm = np.linalg.norm(w)
    xi = np.maximum(0, 1 - y * clf.decision_function(X))

    xlim, ylim = (-3.6, 4.0), (-3.6, 4.0)
    fig, ax = plt.subplots(figsize=(7.6, 5.6))
    draw_boundary(ax, clf, xlim, ylim)
    scatter(ax, X, y)

    # xi_i がゼロ / マージン内 / 誤分類 の代表点をひとつずつ選ぶ
    margin_score = y * clf.decision_function(X)
    i_zero = int(np.argmax(margin_score))
    i_mis = int(np.argmax(xi))
    in_margin = np.where((xi > 0.15) & (xi < 0.85))[0]
    # 誤分類の例とラベルが重ならないよう、離れた点を選ぶ
    i_in = int(in_margin[np.argmax(np.linalg.norm(X[in_margin] - X[i_mis], axis=1))])

    cases = [
        (i_zero, "$\\xi_i = 0$\nマージンの外側", (16, 16), "left"),
        (i_in, "$0 < \\xi_i \\leq 1$\nマージンの内側", (-16, -30), "right"),
        (i_mis, "$\\xi_i > 1$\n誤分類", (26, -16), "left"),
    ]
    for i, label, offset, ha in cases:
        # 点から、そのクラスのマージン境界へ下ろした垂線の長さが xi_i / ||w||
        if xi[i] > 1e-9:
            target = X[i] + y[i] * w / norm * xi[i] / norm
            ax.annotate(
                "",
                xy=target,
                xytext=X[i],
                arrowprops=dict(arrowstyle="->", color=BOUNDARY, lw=1.4),
            )
        ax.annotate(
            label,
            xy=X[i],
            xytext=offset,
            textcoords="offset points",
            fontsize=10,
            ha=ha,
            va="center",
            linespacing=1.5,
            arrowprops=dict(arrowstyle="-", color="#9ca3af", lw=0.9),
        )

    bare(ax, xlim, ylim, "スラック変数 $\\xi_i$")
    class_legend(fig)
    save(fig, "svm-slack.svg")


# ---------------------------------------------------------------- figure 4


def fig_c_comparison():
    X, y = overlapping_data()
    xlim, ylim = (-3.4, 4.2), (-3.4, 4.2)

    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.6))
    for ax, C in zip(axes, (0.01, 1.0, 100.0)):
        clf = SVC(kernel="linear", C=C).fit(X, y)
        draw_boundary(ax, clf, xlim, ylim)
        sv = np.zeros(len(X), dtype=bool)
        sv[clf.support_] = True
        scatter(ax, X, y, size=26, sv_mask=sv)
        width = 2 / np.linalg.norm(clf.coef_[0])
        bare(ax, xlim, ylim, f"$C = {C:g}$")
        ax.set_xlabel(
            f"マージン幅 ${width:.2f}$\nサポートベクター {sv.sum()} 個", fontsize=10
        )
    class_legend(fig)
    save(fig, "svm-c-comparison.svg")


# ---------------------------------------------------------------- figure 5


def fig_losses():
    z = np.linspace(-3, 3, 601)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))

    ax.step(
        z,
        (z < 0).astype(float),
        where="post",
        color="#6b7280",
        lw=1.6,
        ls=":",
        label="0-1 損失",
    )
    ax.plot(z, np.maximum(0, 1 - z), color=POS, lw=2.2, label="ヒンジ損失 (SVM)")
    ax.plot(
        z,
        np.log2(1 + np.exp(-z)),
        color=NEG,
        lw=1.8,
        label="ロジスティック損失",
    )
    ax.plot(z, np.exp(-z), color="#16a34a", lw=1.8, ls="--", label="指数損失 (AdaBoost)")

    ax.axvline(1, color="#9ca3af", lw=0.8, ls=":")
    ax.text(1.06, 1.72, "$z = 1$", fontsize=10, color="#6b7280")
    ax.annotate(
        "$z \\geq 1$ で損失が完全に $0$ になるため\nマージンの外側の点は解に影響しない",
        xy=(1.9, 0.02),
        xytext=(1.28, 0.82),
        fontsize=9.5,
        color="#374151",
        linespacing=1.5,
        arrowprops=dict(arrowstyle="->", color="#9ca3af", lw=0.9),
    )

    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.15, 3.2)
    ax.set_xlabel("$z = y_i f(x_i)$")
    ax.set_ylabel("損失")
    ax.set_title("マージンに対する損失関数の比較")
    ax.axhline(0, color="#d1d5db", lw=0.8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="upper right")
    save(fig, "svm-hinge-loss.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_hyperplanes()
    fig_margin()
    fig_slack()
    fig_c_comparison()
    fig_losses()
