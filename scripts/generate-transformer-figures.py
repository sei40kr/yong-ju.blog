"""content/posts/transformer.mdx の図を生成する。

出力先は public/img/tf-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-transformer-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
INK = "#111827"
GRAY = "#6b7280"
LIGHT = "#d1d5db"

# attention 重み (0 以上 1 以下) 用の単色カラーマップ
ATTN_CMAP = LinearSegmentedColormap.from_list("attn", ["#ffffff", BLUE])

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


def softmax(x, axis=-1):
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


def box(ax, xy, w, h, label, fc="white", ec=INK, fontsize=10, lw=1.2, color=None):
    """角丸の箱をテキストつきで描く。xy は中心。"""
    x, y = xy
    patch = FancyBboxPatch(
        (x - w / 2, y - h / 2),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.06",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=color or INK,
        zorder=3,
        linespacing=1.4,
    )
    return patch


def arrow(ax, start, end, color=GRAY, lw=1.1, style="-|>", ls="-", rad=0.0, z=1):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=11,
            color=color,
            lw=lw,
            linestyle=ls,
            connectionstyle=f"arc3,rad={rad}",
            shrinkA=2,
            shrinkB=2,
            zorder=z,
        )
    )


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


def clean_axes(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


# ---------------------------------------------------------------- figure 1
# RNN と self-attention の情報経路長


def fig_dependency_path():
    n = 6
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.6))
    xs = np.arange(n)

    def nodes(ax, symbol):
        for t in xs:
            box(ax, (t, 1.0), 0.5, 0.44, f"${symbol}_{t + 1}$", fontsize=9.5)
            ax.text(t, 0.05, f"$x_{t + 1}$", ha="center", va="center", fontsize=9.5)
            arrow(ax, (t, 0.25), (t, 0.76), color=LIGHT)

    def caption(ax, text):
        ax.text(
            (n - 1) / 2, -0.62, text, ha="center", va="center", fontsize=9.5, color="#374151"
        )

    # --- RNN: 隣どうしを順に伝わる
    ax = axes[0]
    nodes(ax, "h")
    for t in xs[:-1]:
        arrow(ax, (t + 0.27, 1.0), (t + 0.73, 1.0), color=ORANGE, lw=1.8)
    caption(ax, "$x_1$ の情報が $h_6$ に届くまでに $n - 1$ 回の逐次的な変換を通る")
    bare(ax, (-0.7, n - 0.3), (-0.95, 1.85), "RNN: 経路長 $O(n)$・逐次計算", equal=False)

    # --- self-attention: z_6 が全位置を直接参照する
    ax = axes[1]
    nodes(ax, "z")
    for t in xs[:-1]:
        color = ORANGE if t == 0 else LIGHT
        lw = 1.8 if t == 0 else 1.0
        # 箱の上を通す弧。距離が長いほど大きく膨らむ
        arrow(
            ax,
            (t, 1.24),
            (n - 1, 1.24),
            color=color,
            lw=lw,
            rad=-0.22,
            z=1 if t else 3,
        )
    # 自分自身への参照 (対角成分)
    arrow(ax, (n - 1.22, 1.24), (n - 0.86, 1.24), color=LIGHT, lw=1.0, rad=-1.6)
    caption(ax, "$z_6$ は自分自身を含むどの位置にも 1 ステップで到達できる")
    bare(
        ax,
        (-0.7, n - 0.3),
        (-0.95, 1.85),
        "self-attention: 経路長 $O(1)$・並列計算",
        equal=False,
    )

    fig.tight_layout()
    save(fig, "tf-dependency-path.svg")


# ---------------------------------------------------------------- figure 2
# Q, K, V と行列の形


def fig_qkv():
    fig, ax = plt.subplots(figsize=(9.0, 4.2))

    def mat(x, y, w, h, label, sub, fc):
        box(ax, (x, y), w, h, "", fc=fc, ec=INK, lw=1.1)
        ax.text(x, y, label, ha="center", va="center", fontsize=12, zorder=4)
        ax.text(x, y - h / 2 - 0.16, sub, ha="center", va="top", fontsize=9, color=GRAY)

    mat(0.0, 1.5, 0.55, 1.2, "$X$", "$n \\times d_\\text{model}$", "#f3f4f6")

    for y, name, color, fc, shape in (
        (2.45, "$Q$", BLUE, "#dbeafe", "$n \\times d_k$"),
        (1.5, "$K$", GREEN, "#dcfce7", "$n \\times d_k$"),
        (0.55, "$V$", PURPLE, "#ede9fe", "$n \\times d_v$"),
    ):
        arrow(ax, (0.3, 1.5), (1.05, y), color=GRAY)
        ax.text(
            0.67,
            (1.5 + y) / 2 + (0.1 if y != 1.5 else 0.12),
            f"$W_{name.strip('$')}$",
            ha="center",
            va="bottom",
            fontsize=9.5,
            color=color,
        )
        mat(1.35, y, 0.5, 0.62, name, shape, fc)

    # QK^T
    arrow(ax, (1.62, 2.45), (2.4, 2.1), color=GRAY)
    arrow(ax, (1.62, 1.5), (2.4, 1.9), color=GRAY)
    mat(2.85, 2.0, 0.9, 0.9, "$QK^\\top / \\sqrt{d_k}$", "$n \\times n$", "#fef3c7")

    arrow(ax, (3.32, 2.0), (3.85, 2.0), color=GRAY)
    ax.text(3.58, 2.12, "softmax", ha="center", va="bottom", fontsize=9.5, color=GRAY)
    mat(4.3, 2.0, 0.9, 0.9, "$A$", "$n \\times n$ (行和 $1$)", "#fde68a")

    arrow(ax, (4.77, 2.0), (5.5, 1.35), color=GRAY)
    arrow(ax, (1.62, 0.55), (5.5, 1.15), color=GRAY, rad=0.06)
    mat(5.95, 1.25, 0.55, 0.9, "$AV$", "$n \\times d_v$", "#e0e7ff")

    ax.text(
        3.0,
        -0.25,
        "出力の第 $i$ 行は $\\sum_j A_{ij} \\mathbf{v}_j$ — バリューベクトルの重み付き平均",
        ha="center",
        va="center",
        fontsize=10,
        color="#374151",
    )

    bare(ax, (-0.45, 6.4), (-0.45, 3.0), equal=False)
    fig.tight_layout()
    save(fig, "tf-qkv.svg")


# ---------------------------------------------------------------- figure 3
# 1 / sqrt(d_k) スケーリング


def fig_scaling():
    rng = np.random.default_rng(0)
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.4))

    # (a) 内積の分布
    ax = axes[0]
    for d_k, color in ((8, GREEN), (64, BLUE), (512, ORANGE)):
        q = rng.standard_normal((20000, d_k))
        k = rng.standard_normal((20000, d_k))
        dots = (q * k).sum(axis=1)
        ax.hist(
            dots,
            bins=80,
            density=True,
            histtype="step",
            color=color,
            lw=1.6,
            label=f"$d_k = {d_k}$ (標準偏差 ${np.sqrt(d_k):.1f}$)",
        )
    ax.set_xlim(-70, 70)
    ax.set_ylim(0, 0.20)
    ax.set_xlabel("$\\mathbf{q}^\\top \\mathbf{k}$")
    ax.set_ylabel("確率密度")
    ax.set_title("内積の分布は $d_k$ とともに広がる")
    ax.legend(fontsize=8.5, loc="upper left")
    clean_axes(ax)

    # (b) softmax の最大確率
    d_ks = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
    n_keys, trials = 64, 400
    max_raw, max_scaled, jac_raw, jac_scaled = [], [], [], []
    for d_k in d_ks:
        q = rng.standard_normal((trials, 1, d_k))
        k = rng.standard_normal((trials, n_keys, d_k))
        s = (q * k).sum(axis=-1)
        for scores, mx, jac in (
            (s, max_raw, jac_raw),
            (s / np.sqrt(d_k), max_scaled, jac_scaled),
        ):
            a = softmax(scores, axis=-1)
            mx.append(a.max(axis=-1).mean())
            # softmax ヤコビ行列 diag(a) - a a^T のトレース
            jac.append((1 - (a**2).sum(-1)).mean())

    ax = axes[1]
    ax.plot(d_ks, max_raw, "o-", color=ORANGE, lw=1.8, ms=4, label="スケーリングなし")
    ax.plot(
        d_ks,
        max_scaled,
        "o-",
        color=BLUE,
        lw=1.8,
        ms=4,
        label="$1 / \\sqrt{d_k}$ でスケーリング",
    )
    ax.axhline(1 / n_keys, color=GRAY, lw=0.8, ls=":")
    ax.text(2.4, 1 / n_keys * 1.35, "一様分布 $1/n$", fontsize=8.5, color=GRAY)
    ax.set_xscale("log", base=2)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("$d_k$")
    ax.set_ylabel("最大の attention 重み")
    ax.set_title(f"attention の集中度 (キー ${n_keys}$ 個)")
    ax.legend(fontsize=8.5, loc="center left")
    clean_axes(ax)

    # (c) 勾配の大きさ
    ax = axes[2]
    ax.plot(d_ks, jac_raw, "o-", color=ORANGE, lw=1.8, ms=4, label="スケーリングなし")
    ax.plot(d_ks, jac_scaled, "o-", color=BLUE, lw=1.8, ms=4, label="スケーリングあり")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("$d_k$")
    ax.set_ylabel("$\\text{tr}(\\partial \\mathbf{a} / \\partial \\mathbf{s})$")
    ax.set_title("softmax の勾配")
    ax.legend(fontsize=8.5, loc="lower left")
    clean_axes(ax)

    fig.tight_layout()
    save(fig, "tf-scaling.svg")


# ------------------------------------------------ attention 重みを手で設計するための道具

CONTENT = ["名詞", "主格", "対格", "動詞", "過去"]


def toy_sentence():
    """トークンと、その内容特徴 (5 次元) を返す。

    実際の Transformer では下層の処理を経てこのような特徴が現れると期待されるが、
    ここでは attention の働きを見るために手で与えている。
    """
    tokens = ["私", "は", "本", "を", "読ん", "だ"]
    content = np.array(
        [
            [1, 1, 0, 0, 0],  # 私   … 主格の名詞
            [0, 1, 0, 0, 0],  # は   … 主格の格助詞
            [1, 0, 1, 0, 0],  # 本   … 対格の名詞
            [0, 0, 1, 0, 0],  # を   … 対格の格助詞
            [0, 0, 0, 1, 0],  # 読ん … 動詞
            [0, 0, 0, 0, 1],  # だ   … 過去の助動詞
        ],
        dtype=float,
    )
    return tokens, content


def toy_attention(content, queries, w_pos=1.0, temp=1.0, causal=False, self_bonus=0.0):
    """内容ベースと位置ベースを足したキー・クエリから attention 重みを計算する。

    queries[i] = (内容の希望ベクトル, 位置オフセット, 位置の重み)
    キーは k_j = [c_j, w_pos * (cos θ_j, sin θ_j)]、θ_j = π j / n。
    クエリの位置部分を角度 φ = π * offset / n だけ回転させると、
    内積の位置成分は cos(θ_j - θ_i - φ) となり j = i + offset で最大になる。
    """
    n = len(content)
    theta = np.pi * np.arange(n) / n
    scores = np.zeros((n, n))
    for i, (want, offset, w_q) in enumerate(queries):
        phi = np.pi * offset / n
        content_term = content @ np.asarray(want, dtype=float)
        pos_term = w_q * w_pos * np.cos(theta - theta[i] - phi)
        scores[i] = content_term + pos_term
        scores[i, i] += self_bonus  # 自分自身 (対角成分) への重み
    if causal:
        scores = np.where(np.tril(np.ones((n, n), dtype=bool)), scores, -np.inf)
    return softmax(scores / temp, axis=-1)


def draw_attention(ax, weights, rows, cols, title=None, fontsize=9, annotate=True):
    ax.imshow(weights, cmap=ATTN_CMAP, vmin=0, vmax=1)
    ax.set_xticks(range(len(cols)))
    ax.set_yticks(range(len(rows)))
    ax.set_xticklabels(cols, fontsize=fontsize)
    ax.set_yticklabels(rows, fontsize=fontsize)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(len(cols) + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(rows) + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", lw=1.2)
    for side in ax.spines.values():
        side.set_visible(False)
    if annotate:
        for i in range(weights.shape[0]):
            for j in range(weights.shape[1]):
                w = weights[i, j]
                if w >= 0.06:
                    ax.text(
                        j,
                        i,
                        f"{w:.2f}",
                        ha="center",
                        va="center",
                        fontsize=fontsize - 1.5,
                        color="white" if w > 0.5 else "#374151",
                    )
    if title:
        ax.set_title(title)


# ---------------------------------------------------------------- figure 4
# attention 重み行列の例


def fig_attention_map():
    tokens, content = toy_sentence()
    idx = {name: i for i, name in enumerate(CONTENT)}

    def want(**kwargs):
        v = np.zeros(len(CONTENT))
        for key, value in kwargs.items():
            v[idx[key]] = value
        return v

    queries = [
        (want(動詞=2.5), 0, 0.0),  # 私   → 述語を探す
        (want(名詞=2.0, 主格=1.0), -1, 2.0),  # は   → 直前の名詞
        (want(動詞=2.5), 0, 0.0),  # 本   → 述語を探す
        (want(名詞=2.0, 対格=1.0), -1, 2.0),  # を   → 直前の名詞
        (want(名詞=1.4, 主格=1.4, 対格=1.4), 0, 0.0),  # 読ん → 主格と対格の名詞
        (want(動詞=2.5), -1, 1.5),  # だ   → 直前の動詞
    ]
    weights = toy_attention(content, queries, self_bonus=1.5)

    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    draw_attention(ax, weights, tokens, tokens, fontsize=10)
    ax.set_xlabel("キー (参照される側)")
    ax.set_ylabel("クエリ (参照する側)")
    ax.set_title("attention 重み $A_{ij}$ (各行の和は $1$)")
    fig.tight_layout()
    save(fig, "tf-attention-map.svg")


# ---------------------------------------------------------------- figure 5
# マスク


def fig_mask():
    rng = np.random.default_rng(3)
    n = 7
    tokens = [f"$t_{i + 1}$" for i in range(n)]
    scores = rng.normal(0, 1.2, size=(n, n))

    mask = np.tril(np.ones((n, n), dtype=bool))
    masked = np.where(mask, scores, -np.inf)
    weights = softmax(masked, axis=-1)

    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.5))

    ax = axes[0]
    lim = np.abs(scores).max()
    ax.imshow(scores, cmap="RdBu_r", vmin=-lim, vmax=lim)
    ax.set_title("スコア $QK^\\top / \\sqrt{d_k}$")

    ax = axes[1]
    shown = np.where(mask, scores, np.nan)
    ax.imshow(shown, cmap="RdBu_r", vmin=-lim, vmax=lim)
    ax.imshow(
        np.where(mask, np.nan, 1.0),
        cmap="Greys",
        vmin=0,
        vmax=1.6,
        interpolation="none",
    )
    for i in range(n):
        for j in range(i + 1, n):
            ax.text(j, i, "$-\\infty$", ha="center", va="center", fontsize=7, color=INK)
    ax.set_title("未来の位置を $-\\infty$ に")

    ax = axes[2]
    ax.imshow(weights, cmap=ATTN_CMAP, vmin=0, vmax=1)
    ax.set_title("softmax 後の attention 重み")

    for ax in axes:
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(tokens, fontsize=8.5)
        ax.set_yticklabels(tokens, fontsize=8.5)
        ax.tick_params(length=0)
        ax.set_xticks(np.arange(n + 1) - 0.5, minor=True)
        ax.set_yticks(np.arange(n + 1) - 0.5, minor=True)
        ax.grid(which="minor", color="white", lw=1.0)
        for side in ax.spines.values():
            side.set_visible(False)
        ax.set_xlabel("キー", fontsize=9.5)
    axes[0].set_ylabel("クエリ", fontsize=9.5)

    fig.tight_layout()
    save(fig, "tf-mask.svg")


# ---------------------------------------------------------------- figure 6
# multi-head attention の構造


def fig_multi_head():
    fig, ax = plt.subplots(figsize=(9.4, 3.4))
    h = 4

    box(ax, (0.5, 1.45), 0.7, 1.5, "$X$\n$n \\times d_\\text{model}$", fc="#f3f4f6")

    colors = [BLUE, GREEN, ORANGE, PURPLE]
    fills = ["#dbeafe", "#dcfce7", "#ffedd5", "#ede9fe"]
    xs = np.linspace(2.1, 5.1, h)
    for i, (x, color, fc) in enumerate(zip(xs, colors, fills)):
        arrow(ax, (0.87, 1.45), (x - 0.5, 1.45), color=LIGHT, rad=0.14)
        box(
            ax,
            (x, 1.45),
            0.92,
            1.5,
            f"ヘッド {i + 1}\n\n"
            f"$\\text{{Attn}}(Q_{i + 1}, K_{i + 1}, V_{i + 1})$\n\n"
            "$n \\times d_k$",
            fc=fc,
            ec=color,
            fontsize=8,
        )

    for x in xs:
        arrow(ax, (x + 0.5, 1.45), (6.05, 1.45), color=LIGHT, rad=-0.14)
    box(
        ax,
        (6.55, 1.45),
        0.95,
        1.5,
        "連結\n$n \\times h d_k$",
        fc="#f3f4f6",
    )
    arrow(ax, (7.05, 1.45), (7.65, 1.45), color=GRAY)
    ax.text(7.35, 1.6, "$W_O$", ha="center", va="bottom", fontsize=9.5, color=GRAY)
    box(ax, (8.2, 1.45), 0.85, 1.5, "出力\n$n \\times d_\\text{model}$", fc="#e0e7ff")

    ax.text(
        4.4,
        0.35,
        "$d_k = d_v = d_\\text{model} / h$ とすれば、ヘッドを増やしても計算量は変わらない",
        ha="center",
        va="center",
        fontsize=10,
        color="#374151",
    )

    bare(ax, (0.0, 8.75), (0.15, 2.45), equal=False)
    fig.tight_layout()
    save(fig, "tf-multi-head.svg")


# ---------------------------------------------------------------- figure 7
# ヘッドごとに異なる attention パターン


def fig_head_patterns():
    tokens, content = toy_sentence()
    idx = {name: i for i, name in enumerate(CONTENT)}
    zero = np.zeros(len(CONTENT))

    def want(**kwargs):
        v = np.zeros(len(CONTENT))
        for key, value in kwargs.items():
            v[idx[key]] = value
        return v

    n = len(tokens)
    patterns = []

    # 自分自身を見るヘッド (対角成分)
    patterns.append(
        (
            "自分自身 (対角)",
            toy_attention(
                content, [(zero, 0, 0.0)] * n, temp=0.5, causal=True, self_bonus=3.0
            ),
        )
    )
    # 直前のトークンを見るヘッド (位置ベース)
    patterns.append(
        (
            "直前のトークン",
            toy_attention(content, [(zero, -1, 6.0)] * n, temp=0.35, causal=True),
        )
    )
    # 文頭を見るヘッド: 先頭トークンにだけ立つ特徴をキーに足す
    head_content = content.copy()
    head_content[0] += 3.0
    patterns.append(
        (
            "文頭のトークン",
            toy_attention(
                head_content,
                [(np.ones(len(CONTENT)) * 1.2, 0, 0.0)] * n,
                temp=0.6,
                causal=True,
            ),
        )
    )
    # 述語 (動詞) を見るヘッド (内容ベース)
    patterns.append(
        (
            "述語 (動詞)",
            toy_attention(
                content, [(want(動詞=4.0), 0, 0.0)] * n, temp=0.6, causal=False
            ),
        )
    )
    # スコアがほぼ一様なヘッド
    patterns.append(
        (
            "広く平均を取る",
            toy_attention(content, [(zero, 0, 0.3)] * n, temp=3.0, causal=True),
        )
    )

    fig, axes = plt.subplots(1, 5, figsize=(12.0, 2.9))
    for ax, (title, weights) in zip(axes, patterns):
        draw_attention(ax, weights, tokens, tokens, title, fontsize=8.0, annotate=False)
    fig.tight_layout()
    save(fig, "tf-head-patterns.svg")


# ---------------------------------------------------------------- figure 8
# 位置エンコーディング


def positional_encoding(n, d, base=10000.0):
    pos = np.arange(n)[:, None]
    i = np.arange(d // 2)[None, :]
    angle = pos / np.power(base, 2 * i / d)
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(angle)
    pe[:, 1::2] = np.cos(angle)
    return pe


def fig_positional_encoding():
    n, d = 100, 128
    pe = positional_encoding(n, d)

    fig, axes = plt.subplots(1, 2, figsize=(7.8, 3.3))

    ax = axes[0]
    im = ax.imshow(pe.T, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto", origin="lower")
    ax.set_xlabel("位置 $t$")
    ax.set_ylabel("次元 $i$")
    ax.set_title("$\\mathbf{p}(t)$ の第 $i$ 成分")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    clean_axes(ax)

    ax = axes[1]
    for i, color in ((8, BLUE), (24, GREEN), (48, ORANGE), (72, PURPLE)):
        wavelength = 2 * np.pi * 10000 ** (2 * (i // 2) / d)
        ax.plot(
            pe[:, i],
            color=color,
            lw=1.6,
            label=f"$i = {i}$ ($\\lambda \\approx {wavelength:.0f}$)",
        )
    ax.set_xlabel("位置 $t$")
    ax.set_ylabel("値")
    ax.set_ylim(-1.3, 3.0)
    ax.set_title("次元ごとに波長が変わる")
    ax.legend(fontsize=8, ncol=2, loc="upper center")
    clean_axes(ax)

    fig.tight_layout()
    save(fig, "tf-positional-encoding.svg")


# ---------------------------------------------------------------- figure 9
# 位置エンコーディングの幾何 (回転・2 進カウンタ・波長)


def _unit_circle(ax, center, omega, k, color, caption, labels=True):
    """単位円上で pos から pos + k へのずらしが回転になる様子を描く。"""
    cx, cy = center
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + np.cos(t), cy + np.sin(t), color=LIGHT, lw=1.2, zorder=1)
    ax.plot([cx], [cy], marker="o", ms=2.5, color=GRAY, zorder=2)

    pos = 0.6
    for angle, c, label in (
        (omega * pos, GRAY, "$\\mathbf{p}_i(t)$"),
        (omega * (pos + k), color, "$\\mathbf{p}_i(t + k)$"),
    ):
        # (sin, cos) なので角度は +y 軸から時計回りに測る
        x, y = cx + np.sin(angle), cy + np.cos(angle)
        arrow(ax, (cx, cy), (x, y), color=c, lw=1.6, z=3)
        ax.plot([x], [y], marker="o", ms=4, color=c, zorder=4)
        if labels:
            ax.text(
                cx + 1.32 * np.sin(angle),
                cy + 1.32 * np.cos(angle),
                label,
                ha="center",
                va="center",
                fontsize=8.5,
                color=c,
            )

    # 回転角 omega_i k の弧
    a = np.linspace(omega * pos, omega * (pos + k), 60)
    ax.plot(cx + 0.42 * np.sin(a), cy + 0.42 * np.cos(a), color=color, lw=1.4, zorder=3)
    mid = omega * (pos + k / 2)
    r = 0.62 if labels else 1.05
    ax.text(
        cx + r * np.sin(mid) + (0.0 if labels else 0.35),
        cy + r * np.cos(mid),
        "$\\omega_i k$",
        ha="center",
        va="center",
        fontsize=9,
        color=color,
    )
    ax.text(cx, cy - 1.55, caption, ha="center", va="center", fontsize=9, color=INK)


def fig_pe_geometry():
    fig, axes = plt.subplots(
        1, 3, figsize=(11.4, 3.4), gridspec_kw={"width_ratios": (1.7, 1.0, 1.0)}
    )

    ax = axes[0]
    bare(ax, (-2.6, 2.6), (-1.9, 1.45), title="同じ $k$ のずらしが、ペアごとに違う角度の回転になる")
    _unit_circle(ax, (-1.3, 0.0), 1.0, 2.0, BLUE, "高周波ペア ($\\lambda = 2\\pi$)")
    _unit_circle(
        ax,
        (1.3, 0.0),
        0.1,
        2.0,
        ORANGE,
        "低周波ペア ($\\lambda \\approx 63$)",
        labels=False,
    )

    ax = axes[1]
    n_bits, n_pos = 6, 32
    bits = ((np.arange(n_pos)[None, :] >> np.arange(n_bits)[:, None]) & 1).astype(float)
    ax.imshow(bits, cmap="Greys", vmin=0, vmax=1.4, aspect="auto", origin="lower")
    ax.set_yticks(range(n_bits))
    ax.set_yticklabels([f"$2^{j}$" for j in range(n_bits)], fontsize=9)
    ax.set_xlabel("位置 $t$")
    ax.set_ylabel("桁")
    ax.set_title("2 進カウンタとの類推")
    clean_axes(ax)

    ax = axes[2]
    d = 512
    i = np.arange(d // 2)
    lam = 2 * np.pi * 10000 ** (2 * i / d)
    ax.plot(i, lam, color=PURPLE, lw=1.8)
    ax.axhline(512, color=GRAY, lw=0.9, ls=":")
    ax.text(4, 620, "系列長 $n = 512$", fontsize=9, color=GRAY)
    ax.set_yscale("log")
    ax.set_xlabel("ペアの番号 $i$")
    ax.set_ylabel("波長 $\\lambda_i = 2\\pi / \\omega_i$")
    ax.set_title(f"波長は幾何級数的に伸びる ($d = {d}$)")
    clean_axes(ax)

    fig.tight_layout()
    save(fig, "tf-pe-geometry.svg")


# ---------------------------------------------------------------- figure 10
# 位置エンコーディングの内積の減衰


def fig_pe_similarity():
    d = 512
    k = np.arange(1, 20001)
    gamma = 0.5772156649015329  # オイラーの定数

    def phi(base):
        i = np.arange(d // 2)
        omega = base ** (-2 * i / d)
        return np.cos(np.outer(k, omega)).mean(axis=1)

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 3.4))

    # (a) 絶対位置によらないこと
    ax = axes[0]
    pe = positional_encoding(220, d)
    for pos, color, ls in ((40, BLUE, "-"), (100, GREEN, "--"), (160, ORANGE, ":")):
        offsets = np.arange(-40, 41)
        ax.plot(
            offsets,
            (pe[pos + offsets] * pe[pos]).sum(axis=1) / (d / 2),
            color=color,
            lw=1.8,
            ls=ls,
            label=f"$t = {pos}$",
        )
    ax.set_xlabel("相対位置 $k$")
    ax.set_ylabel("正規化した内積")
    ax.set_title("絶対位置によらず完全に重なる")
    ax.legend(fontsize=8.5, loc="lower center")
    clean_axes(ax)

    ax = axes[1]
    ax.plot(k, phi(10000.0), color=BLUE, lw=1.6, label="$\\varphi(k) / (d/2)$ (数値)")
    approx = 1 - (np.log(k) + gamma) / np.log(10000.0)
    ax.plot(
        k,
        approx,
        color=ORANGE,
        lw=1.6,
        ls="--",
        label="$1 - (\\ln k + \\gamma) / \\ln b$",
    )
    ax.axhline(0, color=GRAY, lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_ylim(-0.35, 1.05)
    ax.set_xlabel("相対位置 $k$")
    ax.set_ylabel("正規化した内積")
    ax.set_title(f"対数的にゆっくり減衰する ($b = 10^4$, $d = {d}$)")
    ax.legend(fontsize=8.5, loc="lower left")
    clean_axes(ax)

    ax = axes[2]
    for base, color in ((100.0, GREEN), (10000.0, BLUE), (1000000.0, PURPLE)):
        ax.plot(
            k,
            phi(base),
            color=color,
            lw=1.6,
            label=f"$b = 10^{{{int(np.log10(base))}}}$",
        )
    ax.axhline(0, color=GRAY, lw=0.8, ls=":")
    ax.set_xscale("log")
    ax.set_ylim(-0.35, 1.05)
    ax.set_xlabel("相対位置 $k$")
    ax.set_ylabel("正規化した内積")
    ax.set_title("底 $b$ が区別できる距離を決める")
    ax.legend(fontsize=8.5, loc="lower left")
    clean_axes(ax)

    fig.tight_layout()
    save(fig, "tf-pe-similarity.svg")


# ---------------------------------------------------------------- figure 11
# Post-LN と Pre-LN


def _layer_norm(x, eps=1e-5):
    mu = x.mean()
    var = x.var()
    std = np.sqrt(var + eps)
    y = (x - mu) / std
    return y, (y, std)


def _residual_stream_norms(kind, n_layers=24, d=64, seed=0):
    """残差ストリーム $\\| x_\\ell \\| / \\sqrt{d}$ が深さとともにどう育つかを測る。

    ブロックは F(x) = W_2 max(W_1 x, 0) (He 初期化) とし、attention は省いている。
    """
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(d)
    x /= np.linalg.norm(x) / np.sqrt(d)

    norms = [np.linalg.norm(x) / np.sqrt(d)]
    for _ in range(n_layers):
        w1 = rng.standard_normal((4 * d, d)) * np.sqrt(2 / d)
        w2 = rng.standard_normal((d, 4 * d)) * np.sqrt(2 / (4 * d))
        if kind == "post":
            f = w2 @ np.maximum(w1 @ x, 0)
            x, _ = _layer_norm(x + f)
        else:
            u, _ = _layer_norm(x)
            x = x + w2 @ np.maximum(w1 @ u, 0)
        norms.append(np.linalg.norm(x) / np.sqrt(d))
    return np.array(norms)


def fig_layernorm():
    fig = plt.figure(figsize=(9.6, 4.2))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.22)

    # --- 構造の比較
    ax = fig.add_subplot(gs[0, 0])
    for x0, title, blocks in (
        (0.0, "Post-LN (原論文)", ["部分層", "$+ \\, \\mathbf{x}$", "LN"]),
        (2.2, "Pre-LN", ["LN", "部分層", "$+ \\, \\mathbf{x}$"]),
    ):
        ax.text(x0 + 0.5, 4.05, title, ha="center", fontsize=11)
        ys = [0.85, 1.85, 2.85]
        for y, label in zip(ys, blocks):
            fc = "#dbeafe" if label == "部分層" else "#f3f4f6"
            box(ax, (x0 + 0.5, y), 1.05, 0.55, label, fc=fc, fontsize=9.5)
        for y in ys[:-1]:
            arrow(ax, (x0 + 0.5, y + 0.28), (x0 + 0.5, y + 0.72), color=GRAY)
        arrow(ax, (x0 + 0.5, 0.2), (x0 + 0.5, 0.57), color=GRAY)
        arrow(ax, (x0 + 0.5, 3.13), (x0 + 0.5, 3.6), color=GRAY)
        ax.text(x0 + 0.5, 0.06, "$\\mathbf{x}$", ha="center", fontsize=10)
        # 残差の迂回路 (「$+ \, x$」の箱に横から入る)
        add_y = 1.85 if x0 == 0.0 else 2.85
        ax.plot(
            [x0 + 0.5, x0 - 0.2, x0 - 0.2],
            [0.35, 0.35, add_y],
            color=ORANGE,
            lw=1.4,
            solid_capstyle="round",
            zorder=1,
        )
        ax.plot([x0 + 0.5], [0.35], marker="o", ms=3.5, color=ORANGE)
        arrow(ax, (x0 - 0.2, add_y), (x0 - 0.03, add_y), color=ORANGE, lw=1.4)
    ax.text(
        1.35,
        -0.2,
        "残差の経路 (橙) が LN を通るか通らないかの違い",
        ha="center",
        fontsize=9.5,
        color="#374151",
    )
    bare(ax, (-0.65, 3.35), (-0.4, 4.35), equal=False)

    # --- 残差ストリームのノルム
    ax = fig.add_subplot(gs[0, 1])
    n_layers = 24
    depth = np.arange(n_layers + 1)
    for kind, color, label in (
        ("post", ORANGE, "Post-LN"),
        ("pre", BLUE, "Pre-LN"),
    ):
        runs = np.array(
            [_residual_stream_norms(kind, n_layers=n_layers, seed=s) for s in range(16)]
        )
        ax.plot(
            depth,
            np.median(runs, axis=0),
            "o-",
            color=color,
            lw=1.8,
            ms=3.5,
            label=label,
        )
        ax.fill_between(
            depth, runs.min(axis=0), runs.max(axis=0), color=color, alpha=0.15, lw=0
        )
    ax.plot(
        depth,
        np.sqrt(depth + 1),
        color=GRAY,
        lw=1.0,
        ls=":",
        label="$\\sqrt{\\ell + 1}$",
    )
    ax.set_xlabel("層 $\\ell$")
    ax.set_ylabel("$\\| \\mathbf{x}_\\ell \\| / \\sqrt{d}$")
    ax.set_title(f"残差ストリームの大きさ ($L = {n_layers}$, 初期化直後)")
    ax.legend(fontsize=9.5, loc="upper left")
    clean_axes(ax)

    save(fig, "tf-layernorm.svg")


# ---------------------------------------------------------------- figure 11
# 埋め込み (one-hot 行列との積 = 行の取り出し)


def fig_embedding():
    tokens = ["私", "は", "本", "を", "読ん", "だ"]
    ids = [3, 0, 5, 1, 7, 8]
    n, vocab = len(tokens), 9

    fig, ax = plt.subplots(figsize=(10.4, 3.8))

    y_top, h = 3.2, 2.4
    rows_y = [y_top - h * (r + 0.5) / n for r in range(n)]

    # --- トークンと ID
    for r, (tok, i) in enumerate(zip(tokens, ids)):
        ax.text(0.1, rows_y[r], tok, ha="center", va="center", fontsize=10)
        ax.text(0.72, rows_y[r], f"${i}$", ha="center", va="center", fontsize=9, color=GRAY)
    ax.text(0.1, y_top + 0.2, "トークン", ha="center", va="center", fontsize=9, color=GRAY)
    ax.text(0.72, y_top + 0.2, "ID", ha="center", va="center", fontsize=9, color=GRAY)

    def label(x, text, sub):
        ax.text(x, y_top + 0.2, text, ha="center", va="center", fontsize=10)
        ax.text(x, y_top - h - 0.16, sub, ha="center", va="top", fontsize=9, color=GRAY)

    # --- one-hot 行列 O
    x0, w_o = 1.25, 1.5
    onehot = np.zeros((n, vocab))
    onehot[np.arange(n), ids] = 1.0
    ax.imshow(
        onehot,
        cmap=LinearSegmentedColormap.from_list("onehot", ["#f3f4f6", INK]),
        vmin=0,
        vmax=1.4,
        extent=(x0, x0 + w_o, y_top - h, y_top),
        aspect="auto",
        zorder=2,
    )
    _cell_grid(ax, n, vocab, x0, y_top - h, w_o, h)
    label(x0 + w_o / 2, "$O$ (one-hot)", "$n \\times |V|$")
    ax.text(x0 + w_o + 0.2, y_top - h / 2, "$\\times$", ha="center", va="center", fontsize=13)

    # --- 埋め込み行列 E
    x1, w_e = x0 + w_o + 0.4, 1.5
    rng = np.random.default_rng(7)
    emb = rng.normal(0, 1, size=(vocab, 12))
    ax.imshow(
        emb,
        cmap="RdBu_r",
        vmin=-2.5,
        vmax=2.5,
        extent=(x1, x1 + w_e, y_top - h, y_top),
        aspect="auto",
        zorder=2,
    )
    _cell_grid(ax, vocab, 12, x1, y_top - h, w_e, h)
    label(x1 + w_e / 2, "$E$ (埋め込み行列)", "$|V| \\times d_\\text{model}$・学習される")
    ax.text(x1 + w_e + 0.2, y_top - h / 2, "$=$", ha="center", va="center", fontsize=13)

    # --- 取り出された埋め込み
    x2, w_x = x1 + w_e + 0.4, 1.5
    ax.imshow(
        emb[ids],
        cmap="RdBu_r",
        vmin=-2.5,
        vmax=2.5,
        extent=(x2, x2 + w_x, y_top - h, y_top),
        aspect="auto",
        zorder=2,
    )
    _cell_grid(ax, n, 12, x2, y_top - h, w_x, h)
    label(x2 + w_x / 2, "$OE$ (行の取り出し)", "$n \\times d_\\text{model}$")

    # --- スケーリングと位置エンコーディングの加算
    mid = y_top - h / 2
    cx = x2 + w_x + 1.15
    arrow(ax, (x2 + w_x + 0.1, mid), (cx - 0.2, mid))
    ax.text(
        cx - 0.55,
        mid + 0.12,
        "$\\times \\sqrt{d_\\text{model}}$",
        ha="center",
        va="bottom",
        fontsize=9,
        color=GRAY,
    )
    ax.add_patch(Circle((cx, mid), 0.13, fc="white", ec=INK, lw=1.1, zorder=3))
    ax.text(cx, mid, "$+$", ha="center", va="center", fontsize=9, zorder=4)
    arrow(ax, (cx, y_top - h - 0.05), (cx, mid - 0.2), color=PURPLE)
    ax.text(
        cx,
        y_top - h - 0.16,
        "位置エンコーディング\n$\\mathbf{p}(t)$",
        ha="center",
        va="top",
        fontsize=9,
        color=PURPLE,
        linespacing=1.4,
    )

    arrow(ax, (cx + 0.2, mid), (cx + 0.72, mid))
    box(ax, (cx + 1.15, mid), 0.7, h, "$X$", fc="#e0e7ff", fontsize=12)
    ax.text(
        cx + 1.15,
        y_top - h - 0.16,
        "$n \\times d_\\text{model}$",
        ha="center",
        va="top",
        fontsize=9,
        color=GRAY,
    )

    ax.text(
        4.7,
        -0.35,
        "one-hot 行列を掛けることは、$E$ の行を引くことにほかならない",
        ha="center",
        va="center",
        fontsize=10,
        color="#374151",
    )

    bare(ax, (-0.35, cx + 1.65), (-0.62, 3.6), equal=False)
    fig.tight_layout()
    save(fig, "tf-embedding.svg")


def _cell_grid(ax, rows, cols, x0, y0, w, h):
    """imshow の上に白い格子線を引く。"""
    for j in range(1, cols):
        ax.plot(
            [x0 + j * w / cols] * 2, [y0, y0 + h], color="white", lw=0.8, zorder=3
        )
    for i in range(1, rows):
        ax.plot(
            [x0, x0 + w], [y0 + i * h / rows] * 2, color="white", lw=0.8, zorder=3
        )


# ------------------------------------------------ アーキテクチャ図を組むための道具

ARCH_W, ARCH_H, ARCH_GAP, ARCH_FS = 2.0, 0.4, 0.58, 8.2
ARCH_JUMP = 0.85  # 枠 (×N) の外へ出るときの間隔
ARCH_ATTN = ("#dbeafe", BLUE)
ARCH_NORM = ("#f3f4f6", GRAY)
ARCH_FFN = ("#dcfce7", GREEN)
ARCH_CROSS = ("#ffedd5", ORANGE)
ARCH_EMB = ("#ede9fe", PURPLE)
ARCH_HEAD = ("#fef3c7", "#d97706")

ENCODER_BLOCK = [
    ("multi-head\nself-attention", ARCH_ATTN),
    ("Add & Norm", ARCH_NORM),
    ("位置ごとの FFN", ARCH_FFN),
    ("Add & Norm", ARCH_NORM),
]
DECODER_BLOCK = [
    ("マスク付き multi-head\nself-attention", ARCH_ATTN),
    ("Add & Norm", ARCH_NORM),
    ("位置ごとの FFN", ARCH_FFN),
    ("Add & Norm", ARCH_NORM),
]
CROSS_DECODER_BLOCK = [
    ("マスク付き multi-head\nself-attention", ARCH_ATTN),
    ("Add & Norm", ARCH_NORM),
    ("cross-attention", ARCH_CROSS),
    ("Add & Norm", ARCH_NORM),
    ("位置ごとの FFN", ARCH_FFN),
    ("Add & Norm", ARCH_NORM),
]


def _levels(y0, count):
    return [y0 + ARCH_GAP * i for i in range(count)]


def _blocks(ax, x, y0, items):
    """箱を縦に積んで矢印で繋ぐ。枠を先に描いてから呼ぶこと。"""
    ys = _levels(y0, len(items))
    for y, (label, (fc, ec)) in zip(ys, items):
        box(ax, (x, y), ARCH_W, ARCH_H, label, fc=fc, ec=ec, fontsize=ARCH_FS)
    for a, b in zip(ys, ys[1:]):
        arrow(ax, (x, a + ARCH_H / 2), (x, b - ARCH_H / 2), color=LIGHT)
    return ys


def _frame(ax, x, ys, label, side=-1):
    y0, y1 = ys[0] - ARCH_H / 2 - 0.14, ys[-1] + ARCH_H / 2 + 0.14
    box(
        ax,
        (x, (y0 + y1) / 2),
        ARCH_W + 0.34,
        y1 - y0,
        "",
        fc="#fafafa",
        ec=LIGHT,
        lw=1.0,
    )
    ax.text(
        x + side * (ARCH_W / 2 + 0.34),
        (y0 + y1) / 2,
        label,
        ha="center",
        va="center",
        fontsize=8.5,
        color=GRAY,
        rotation=90,
    )


def _input_stage(ax, x, note, side=-1):
    """入力系列 → 埋め込み → 位置エンコーディングの加算。戻り値は次に積む y。"""
    ax.text(x, -0.62, note, ha="center", va="center", fontsize=8.5, color=GRAY)
    arrow(ax, (x, -0.44), (x, -0.2), color=LIGHT)
    box(ax, (x, 0.0), ARCH_W, ARCH_H, "埋め込み", fc=ARCH_EMB[0], ec=ARCH_EMB[1], fontsize=ARCH_FS)
    arrow(ax, (x, 0.2), (x, 0.33), color=LIGHT)
    ax.add_patch(Circle((x, 0.44), 0.11, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.text(x, 0.44, "$+$", ha="center", va="center", fontsize=8, zorder=4)
    arrow(ax, (x + side * 0.78, 0.44), (x + side * 0.13, 0.44), color=PURPLE)
    ax.text(
        x + side * 0.92,
        0.44,
        "位置エンコーディング\n$\\mathbf{p}(t)$",
        ha="right" if side < 0 else "left",
        va="center",
        fontsize=8,
        color=PURPLE,
        linespacing=1.4,
    )
    return 1.0


def _generator_head(ax, x, y):
    """線形変換 → softmax → 次トークンの確率。"""
    ys = _blocks(ax, x, y, [("線形変換", ARCH_NORM), ("softmax", ARCH_HEAD)])
    arrow(ax, (x, ys[-1] + ARCH_H / 2), (x, ys[-1] + 0.44), color=LIGHT)
    ax.text(
        x,
        ys[-1] + 0.64,
        "次トークンの確率",
        ha="center",
        va="center",
        fontsize=8.5,
        color=INK,
    )


# ---------------------------------------------------------------- figure 12
# encoder-decoder (元の Transformer)


def fig_architecture():
    fig, ax = plt.subplots(figsize=(7.6, 7.4))
    x_enc, x_dec = 0.0, 2.75

    y = _input_stage(ax, x_enc, "入力系列 (原文)")
    _frame(ax, x_enc, _levels(y, len(ENCODER_BLOCK)), "encoder  $\\times N$")
    enc_ys = _blocks(ax, x_enc, y, ENCODER_BLOCK)

    _input_stage(ax, x_dec, "出力系列 (訳文を 1 つ右にずらす)", side=1)
    _frame(ax, x_dec, _levels(y, len(CROSS_DECODER_BLOCK)), "decoder  $\\times N$", side=1)
    dec_ys = _blocks(ax, x_dec, y, CROSS_DECODER_BLOCK)

    arrow(
        ax,
        (x_dec, dec_ys[-1] + ARCH_H / 2 + 0.16),
        (x_dec, dec_ys[-1] + ARCH_JUMP - ARCH_H / 2),
        color=LIGHT,
    )
    _generator_head(ax, x_dec, dec_ys[-1] + ARCH_JUMP)

    # encoder の出力を cross-attention の K, V として渡す (枠の外を通す)
    y_out = enc_ys[-1] + ARCH_H / 2 + 0.14
    y_cross = dec_ys[2]
    x_turn = (x_enc + x_dec) / 2
    y_over = y_out + 0.34
    ax.plot(
        [x_enc, x_enc, x_turn, x_turn],
        [y_out, y_over, y_over, y_cross],
        color=ORANGE,
        lw=1.3,
        zorder=1,
    )
    arrow(
        ax,
        (x_turn, y_cross),
        (x_dec - ARCH_W / 2 - 0.02, y_cross),
        color=ORANGE,
        lw=1.3,
    )
    ax.text(
        x_enc - 0.95,
        y_over + 0.1,
        "encoder の出力を $K, V$ として渡す",
        ha="left",
        va="bottom",
        fontsize=8.5,
        color=ORANGE,
    )

    bare(ax, (-1.75, 4.75), (-0.95, 6.3), equal=False)
    fig.tight_layout()
    save(fig, "tf-architecture.svg")


# ---------------------------------------------------------------- figure 13
# encoder のみ / decoder のみ


def fig_variants():
    fig, axes = plt.subplots(1, 2, figsize=(7.8, 5.6))
    ylim = (-0.95, 5.15)

    # --- encoder のみ
    ax = axes[0]
    y = _input_stage(ax, 0.0, "入力系列 (全体を一度に)")
    _frame(ax, 0.0, _levels(y, len(ENCODER_BLOCK)), "encoder  $\\times N$")
    ys = _blocks(ax, 0.0, y, ENCODER_BLOCK)
    arrow(ax, (0.0, ys[-1] + ARCH_H / 2 + 0.16), (0.0, ys[-1] + ARCH_JUMP - ARCH_H / 2), color=LIGHT)
    box(
        ax,
        (0.0, ys[-1] + ARCH_JUMP),
        ARCH_W,
        ARCH_H,
        "各位置の表現",
        fc="#f3f4f6",
        ec=GRAY,
        fontsize=ARCH_FS,
    )
    ax.text(
        0.0,
        ys[-1] + ARCH_JUMP + 0.46,
        "分類・穴埋め・文の埋め込み",
        ha="center",
        va="center",
        fontsize=8.5,
        color=GRAY,
    )
    bare(ax, (-1.75, 1.35), ylim, "encoder のみ (BERT)", equal=False)

    # --- decoder のみ
    ax = axes[1]
    y = _input_stage(ax, 0.0, "先頭から現在までのトークン")
    _frame(ax, 0.0, _levels(y, len(DECODER_BLOCK)), "decoder  $\\times N$")
    ys = _blocks(ax, 0.0, y, DECODER_BLOCK)
    arrow(ax, (0.0, ys[-1] + ARCH_H / 2 + 0.16), (0.0, ys[-1] + ARCH_JUMP - ARCH_H / 2), color=LIGHT)
    _generator_head(ax, 0.0, ys[-1] + ARCH_JUMP)
    bare(ax, (-1.75, 1.35), ylim, "decoder のみ (GPT)", equal=False)

    fig.tight_layout()
    save(fig, "tf-variants.svg")


# ---------------------------------------------------------------- figure 14
# 3 構成の attention マスクの違い


def fig_masks():
    n = 6
    full = np.ones((n, n), dtype=bool)
    causal = np.tril(np.ones((n, n), dtype=bool))
    cross = np.ones((n, 4), dtype=bool)

    fig, axes = plt.subplots(1, 3, figsize=(10.2, 2.9))

    def masks(ax, items, title):
        # どのパネルでも升目の大きさが揃うように、幅は固定して中央寄せする
        left = (3.45 - (1.25 * len(items) - 0.25)) / 2
        for j, (mask, label, color) in enumerate(items):
            x0 = left + j * 1.25
            rows, cols = mask.shape
            disp = np.where(mask, 0.55, np.nan)
            ax.imshow(
                disp,
                cmap=ATTN_CMAP.with_extremes(bad="#f3f4f6"),
                vmin=0,
                vmax=1.0,
                extent=(x0, x0 + 1.0, 0.0, 1.0),
                aspect="auto",
                zorder=2,
            )
            _cell_grid(ax, rows, cols, x0, 0.0, 1.0, 1.0)
            ax.text(
                x0 + 0.5, -0.1, label, ha="center", va="top", fontsize=8.5, color=color
            )
        ax.set_title(title, fontsize=11)
        bare(ax, (-0.15, 3.6), (-0.5, 1.1), equal=False)

    masks(axes[0], [(full, "全位置を参照 (双方向)", BLUE)], "encoder のみ (BERT)")
    masks(axes[1], [(causal, "過去だけを参照 (因果)", ORANGE)], "decoder のみ (GPT)")
    masks(
        axes[2],
        [
            (full, "encoder\nself (双方向)", BLUE),
            (causal, "decoder\nself (因果)", ORANGE),
            (cross, "cross\n$n \\times m$", "#b45309"),
        ],
        "encoder-decoder",
    )

    fig.tight_layout()
    save(fig, "tf-masks.svg")



# ---------------------------------------------------------------- figure 13
# 計算量とメモリ


def fig_complexity():
    d = 512
    n = np.logspace(np.log10(16), np.log10(65536), 200)

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))

    ax = axes[0]
    proj = 4 * n * d * d  # Q, K, V, 出力の射影
    attn = 2 * n * n * d  # QK^T と AV
    rnn = 2 * n * d * d  # 入力と隠れ状態の行列積
    ax.plot(n, proj, color=BLUE, lw=1.8, label="射影 $4 n d^2$")
    ax.plot(n, attn, color=ORANGE, lw=1.8, label="attention $2 n^2 d$")
    ax.plot(n, proj + attn, color=INK, lw=2.0, ls="--", label="self-attention 合計")
    ax.plot(n, rnn, color=GREEN, lw=1.6, label="RNN $2 n d^2$ (逐次)")
    ax.axvline(2 * d, color=GRAY, lw=0.8, ls=":")
    ax.text(2 * d * 1.2, 2e5, f"$n = 2d = {2 * d}$", fontsize=9, color=GRAY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("系列長 $n$")
    ax.set_ylabel("層あたりの乗算回数")
    ax.set_title(f"計算量 ($d_\\text{{model}} = {d}$)")
    ax.legend(fontsize=8.5, loc="upper left")
    clean_axes(ax)

    ax = axes[1]
    for h, batch, color in ((8, 1, BLUE), (8, 32, ORANGE)):
        mem = batch * h * n * n * 4 / 1024**3  # float32, GiB
        ax.plot(n, mem, color=color, lw=1.8, label=f"$h = {h}$, バッチ $= {batch}$")
    ax.axhline(80, color=GRAY, lw=0.8, ls=":")
    ax.text(20, 130, "80 GiB (GPU 1 枚のメモリの目安)", fontsize=9, color=GRAY)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 1e5)
    ax.set_xlabel("系列長 $n$")
    ax.set_ylabel("attention 行列のメモリ (GiB)")
    ax.set_title("attention 行列は $O(n^2)$ のメモリを食う")
    ax.legend(fontsize=8.5, loc="upper left")
    clean_axes(ax)

    fig.tight_layout()
    save(fig, "tf-complexity.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_dependency_path()
    fig_qkv()
    fig_scaling()
    fig_attention_map()
    fig_mask()
    fig_multi_head()
    fig_head_patterns()
    fig_positional_encoding()
    fig_pe_geometry()
    fig_pe_similarity()
    fig_layernorm()
    fig_embedding()
    fig_architecture()
    fig_variants()
    fig_masks()
    fig_complexity()
