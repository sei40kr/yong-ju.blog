"""content/posts/reinforcement-learning.mdx の図を生成する。

出力先は public/img/rl-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-reinforcement-learning-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

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


def bare(ax, xlim, ylim, equal=True):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_xticks([])
    ax.set_yticks([])
    if equal:
        ax.set_aspect("equal")
    for side in ax.spines.values():
        side.set_visible(False)


def box(ax, x, y, label, w=1.7, h=0.8, facecolor="#eff6ff", edgecolor=BLUE, fontsize=11):
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.03,rounding_size=0.12",
            facecolor=facecolor,
            edgecolor=edgecolor,
            lw=1.4,
            zorder=2,
        )
    )
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, zorder=3)


def state_node(ax, x, y, label, r=0.24, color=BLUE, fill="white", fontsize=10.5):
    ax.scatter([x], [y], s=(r * 92) ** 2, facecolors=fill, edgecolors=color, linewidths=1.4, zorder=3)
    ax.text(x, y, label, ha="center", va="center", fontsize=fontsize, zorder=4)


def action_node(ax, x, y, color, r=0.14):
    ax.scatter([x], [y], s=(r * 92) ** 2, color=color, zorder=3)


def arrow(ax, p0, p1, color=INK, lw=1.2, style="->", **kwargs):
    ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle=style, color=color, lw=lw, **kwargs))


# ---------------------------------------------------------------- figure 1


def fig_policy():
    """エージェントと環境のやり取り、決定論的な方策と確率的な方策。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.8), gridspec_kw=dict(width_ratios=[1.1, 1]))

    ax = axes[0]
    box(ax, 0, 1.0, "エージェント", w=2.2, h=0.85)
    box(ax, 0, -1.0, "環境", w=2.2, h=0.85, facecolor="#fff7ed", edgecolor=ORANGE)
    arrow(ax, (1.2, 0.85), (1.2, -0.85), color=BLUE, lw=1.5, connectionstyle="arc3,rad=-0.35")
    arrow(ax, (-1.2, -0.85), (-1.2, 0.85), color=ORANGE, lw=1.5, connectionstyle="arc3,rad=-0.35")
    ax.text(2.15, 0, "行動 $a_t$\n$\\pi(a\\mid s)$ で選ぶ", ha="center", va="center", fontsize=9.5, color=BLUE, linespacing=1.6)
    ax.text(-2.15, 0, "状態 $s_{t+1}$\n報酬 $R_t$", ha="center", va="center", fontsize=9.5, color=ORANGE, linespacing=1.6)
    bare(ax, (-3.3, 3.3), (-1.9, 1.9))
    ax.set_title("エージェントと環境のやり取り")

    ax = axes[1]
    for k, (cx, title, color) in enumerate(((0.0, "決定論的な方策", GREEN), (3.2, "確率的な方策", PURPLE))):
        ax.add_patch(Rectangle((cx - 0.55, -0.55), 1.1, 1.1, facecolor="#f9fafb", edgecolor=LIGHT, lw=1.2))
        state_node(ax, cx, 0, "$s$", r=0.26, color=INK)
        if k == 0:
            arrow(ax, (cx, 0.32), (cx, 1.15), color=GREEN, lw=2.0)
            ax.text(cx + 0.12, 0.95, "$a=\\mu(s)$", fontsize=10, color=GREEN)
        else:
            for (dx, dy), p in (((0, 1), 0.5), ((1, 0), 0.3), ((0, -1), 0.1), ((-1, 0), 0.1)):
                length = 0.35 + 1.3 * p
                arrow(
                    ax,
                    (cx + dx * 0.32, dy * 0.32),
                    (cx + dx * length, dy * length),
                    color=PURPLE,
                    lw=0.8 + 3.2 * p,
                )
                ax.text(
                    cx + dx * (length + 0.3),
                    dy * (length + 0.26),
                    f"${p}$",
                    ha="center",
                    va="center",
                    fontsize=9.5,
                    color=PURPLE,
                )
        ax.text(cx, 1.75, title, ha="center", fontsize=11, color=color)
    ax.text(1.6, -1.9, "確率的な方策では $\\pi(a\\mid s)$ の分だけ行動がばらつく", ha="center", fontsize=9.5, color=GRAY)
    bare(ax, (-1.5, 4.9), (-2.2, 2.1))
    save(fig, "rl-policy.svg")


# ---------------------------------------------------------------- figure 2


def fig_transition():
    """状態遷移確率。同じ行動でも遷移先はばらつく。"""
    fig, ax = plt.subplots(figsize=(7.2, 4.0))

    probs = {(0, 1): 0.8, (-1, 0): 0.1, (1, 0): 0.1}
    for i in range(-1, 2):
        for j in range(-1, 2):
            p = probs.get((i, j), 0.0)
            ax.add_patch(
                Rectangle(
                    (i - 0.5, j - 0.5),
                    1,
                    1,
                    facecolor=BLUE if p else "#f9fafb",
                    alpha=0.12 + 0.8 * p if p else 1.0,
                    edgecolor=LIGHT,
                    lw=1.2,
                )
            )
            if p:
                ax.text(i, j + 0.3, f"$p={p}$", ha="center", fontsize=9.5, color=BLUE)
                arrow(ax, (0, 0), (i * 0.72, j * 0.72), color=BLUE, lw=0.8 + 3.0 * p)
    state_node(ax, 0, 0, "$s$", r=0.2, color=INK)
    ax.text(0, -1.05, "行動 $a$ = 「上へ」", ha="center", fontsize=10.5, color=ORANGE)
    ax.text(
        2.1,
        0.5,
        "$p(s'\\mid s,a)$\n\n意図した向きに $0.8$、\n横にすべる確率が\nそれぞれ $0.1$",
        fontsize=10,
        color=GRAY,
        linespacing=1.6,
        va="center",
    )
    ax.set_title("同じ行動でも次の状態は 1 つに決まらない")
    bare(ax, (-1.7, 4.4), (-1.7, 1.9))
    save(fig, "rl-transition.svg")


# ---------------------------------------------------------------- figure 3


def fig_markov():
    """マルコフ性: 未来は今の状態と行動だけで決まる。"""
    fig, ax = plt.subplots(figsize=(8.2, 3.8))

    # 別々の経路をたどっても、同じ状態に着けば未来の分布は同じ
    for y, color, tag in ((1.05, BLUE, "経路 1"), (-1.05, ORANGE, "経路 2")):
        xs = [-3.6, -2.5, -1.4]
        for k, x in enumerate(xs):
            state_node(ax, x, y, f"$s_{{{k}}}$" if y > 0 else f"$s_{{{k}}}'$", color=color)
            if k:
                arrow(ax, (xs[k - 1] + 0.26, y), (x - 0.26, y), color=color, lw=1.2)
        arrow(ax, (xs[-1] + 0.26, y), (-0.36, 0.18 if y > 0 else -0.18), color=color, lw=1.2)
        ax.text(-3.6, y + 0.45, tag, ha="center", fontsize=9.5, color=color)

    state_node(ax, 0, 0, "$s$", r=0.3, color=INK)
    ax.text(0, -0.62, "今の状態", ha="center", fontsize=9.5, color=INK)

    for k, (y, p) in enumerate(((1.15, 0.6), (0.0, 0.3), (-1.15, 0.1))):
        state_node(ax, 2.6, y, "$s'$", color=GREEN)
        arrow(ax, (0.32, 0.0), (2.3, y), color=GREEN, lw=1.0)
        ax.text(1.45, y * 0.66 + 0.26, f"$p(s'\\mid s,a)={p}$", fontsize=9, color=GREEN, ha="center")

    ax.text(
        0.6,
        -1.95,
        "どちらの経路で来たかによらず、次に何が起こるかは今の $s$ と $a$ だけで決まる (マルコフ性)",
        ha="center",
        fontsize=9.5,
        color=GRAY,
    )
    ax.set_title("履歴を忘れてよいのがマルコフ決定過程")
    bare(ax, (-4.3, 4.3), (-2.3, 1.9), equal=False)
    save(fig, "rl-markov.svg")


# ---------------------------------------------------------------- figure 4


def fig_return():
    """収益と割引率。遠い未来の報酬ほど軽く見積もる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.7))

    ax = axes[0]
    gamma = 0.8
    ks = np.arange(0, 9)
    weights = gamma**ks
    ax.bar(ks, np.ones_like(weights), width=0.62, color=LIGHT, alpha=0.55, label="報酬 $R_{t+k}$")
    ax.bar(ks, weights, width=0.62, color=BLUE, alpha=0.9, label="割引後 $\\gamma^k R_{t+k}$")
    for k in (0, 1, 2, 4):
        ax.text(k, weights[k] + 0.05, f"$\\gamma^{k}$" if k else "$1$", ha="center", fontsize=9, color=BLUE)
    ax.set_xticks(ks)
    ax.set_xticklabels([f"$t+{k}$" if k else "$t$" for k in ks], fontsize=9)
    ax.set_ylim(0, 1.35)
    ax.set_yticks([0, 0.5, 1])
    ax.set_title(f"割引率 $\\gamma={gamma}$ の重み付け")
    ax.legend(fontsize=9, ncol=2, loc="upper right")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    ax = axes[1]
    ks = np.arange(0, 61)
    for g, color in ((0.5, GREEN), (0.8, BLUE), (0.95, PURPLE)):
        ax.plot(ks, np.cumsum(g**ks), color=color, lw=1.6, label=f"$\\gamma={g}$")
        ax.axhline(1 / (1 - g), color=color, lw=0.9, ls=":")
        ax.text(61, 1 / (1 - g), f"$\\frac{{1}}{{1-\\gamma}}={1 / (1 - g):.0f}$", fontsize=9, color=color, va="center")
    ax.set_xlabel("足し合わせた項数 $k$")
    ax.set_ylabel("$G_t$ (報酬が常に $1$ の場合)")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 23)
    ax.set_title("$\\gamma<1$ なら無限に足しても発散しない")
    ax.legend(fontsize=9, loc="center right")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    save(fig, "rl-return.svg")


# ---------------------------------------------------------------- figure 5


def backup_tree(ax, take_max=False):
    """ベルマン方程式のバックアップ図を描く。"""
    root = (0.0, 1.75)
    actions = ((-1.15, 0.55), (1.15, 0.55))
    nexts = (((-1.85, -0.75), (-0.5, -0.75)), ((0.5, -0.75), (1.85, -0.75)))
    pis = ("$\\pi(a_1\\mid s)$", "$\\pi(a_2\\mid s)$")

    state_node(ax, *root, "$s$", r=0.3, color=INK)
    for k, (ax_, ay) in enumerate(actions):
        best = take_max and k == 1
        color = ORANGE if best else (LIGHT if take_max else BLUE)
        ax.plot([root[0], ax_], [root[1] - 0.28, ay + 0.16], color=color, lw=2.2 if best else 1.3, zorder=1)
        action_node(ax, ax_, ay, color if not take_max or best else LIGHT)
        ax.text(ax_ + (0.24 if k else -0.24), ay + 0.02, f"$a_{k + 1}$", fontsize=10, ha="left" if k else "right", color=INK)
        if not take_max:
            ax.text((root[0] + ax_) / 2 + (0.1 if k else -0.1), (root[1] + ay) / 2 + 0.16, pis[k], fontsize=9, color=BLUE, ha="center")
        for m, (nx, ny) in enumerate(nexts[k]):
            sub = ORANGE if best else (LIGHT if take_max else GREEN)
            ax.plot([ax_, nx], [ay - 0.14, ny + 0.26], color=sub, lw=1.8 if best else 1.1, zorder=1)
            state_node(ax, nx, ny, "$s'$", r=0.26, color=INK if (not take_max or best) else LIGHT)
            if (not take_max) and k == 0:
                ax.text(
                    (ax_ + nx) / 2 - 0.38,
                    (ay + ny) / 2 + 0.04,
                    "$p(s'\\mid s,a)$" if m == 0 else "",
                    fontsize=9,
                    color=GREEN,
                    ha="center",
                )
            del sub
    for nx in (-1.85, -0.5, 0.5, 1.85):
        ax.text(nx, -1.28, "$r+\\gamma v(s')$", fontsize=8.5, color=GRAY, ha="center")
    bare(ax, (-2.7, 2.7), (-1.75, 2.35), equal=False)


def fig_bellman():
    """ベルマン方程式とベルマン最適方程式のバックアップ図。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 4.0))

    backup_tree(axes[0], take_max=False)
    axes[0].set_title("ベルマン方程式 $v_\\pi(s)$")
    axes[0].text(
        0,
        -1.62,
        "行動は $\\pi$ で、遷移は $p$ で平均をとる",
        ha="center",
        fontsize=9.5,
        color=GRAY,
    )

    backup_tree(axes[1], take_max=True)
    axes[1].set_title("ベルマン最適方程式 $v_*(s)$")
    axes[1].text(1.15, 0.92, "$\\max$", fontsize=11, color=ORANGE, ha="center")
    axes[1].text(
        0,
        -1.62,
        "行動は平均せず、最良のものだけを選ぶ",
        ha="center",
        fontsize=9.5,
        color=GRAY,
    )

    fig.suptitle("1 段先の状態の価値から、今の状態の価値を計算する", y=1.0)
    save(fig, "rl-bellman.svg")


# ---------------------------------------------------------------- figure 6


def fig_value_q():
    """状態価値関数と Q 関数の関係。"""
    fig, ax = plt.subplots(figsize=(7.6, 4.2))

    root = (0.0, 1.7)
    actions = ((-1.3, 0.5), (1.3, 0.5))
    state_node(ax, *root, "$s$", r=0.32, color=INK)
    ax.text(-0.5, 1.95, "$v_\\pi(s)$", fontsize=12, color=BLUE, ha="right")

    for k, (ax_, ay) in enumerate(actions):
        ax.plot([root[0], ax_], [root[1] - 0.3, ay + 0.18], color=BLUE, lw=1.4, zorder=1)
        action_node(ax, ax_, ay, PURPLE, r=0.16)
        ax.text((root[0] + ax_) / 2 + (0.15 if k else -0.15), (root[1] + ay) / 2 + 0.16, f"$\\pi(a_{k + 1}\\mid s)$", fontsize=9.5, color=BLUE, ha="center")
        ax.text(ax_ + (0.3 if k else -0.3), ay - 0.04, f"$q_\\pi(s,a_{k + 1})$", fontsize=10.5, color=PURPLE, ha="left" if k else "right")
        for nx in (ax_ - 0.75, ax_ + 0.75):
            ax.plot([ax_, nx], [ay - 0.16, -0.75 + 0.26], color=GREEN, lw=1.1, zorder=1)
            state_node(ax, nx, -0.75, "$s'$", r=0.26, color=INK)
            ax.text(nx, -1.28, "$r+\\gamma v_\\pi(s')$", fontsize=8.5, color=GRAY, ha="center")

    ax.text(
        0,
        -1.95,
        "$v_\\pi(s)=\\sum_a \\pi(a\\mid s)\\, q_\\pi(s,a)$",
        ha="center",
        fontsize=12,
        color=INK,
    )
    ax.text(
        0,
        -2.5,
        "Q 関数は「行動 $a$ を選んだ直後」の価値。状態の価値はそれを方策で平均したもの",
        ha="center",
        fontsize=9.5,
        color=GRAY,
    )
    ax.set_title("状態価値関数と Q 関数の関係")
    bare(ax, (-3.0, 3.0), (-2.8, 2.3), equal=False)
    save(fig, "rl-value-q.svg")


# ---------------------------------------------------------------- figure 7

ROWS, COLS = 3, 4
WALL = (1, 1)
TERMINALS = {(0, 3): 1.0, (1, 3): -1.0}
STEP_REWARD = -0.04
GAMMA = 0.9
MOVES = {"↑": (-1, 0), "↓": (1, 0), "←": (0, -1), "→": (0, 1)}


def _next_cell(cell, delta):
    r, c = cell[0] + delta[0], cell[1] + delta[1]
    if not (0 <= r < ROWS and 0 <= c < COLS) or (r, c) == WALL:
        return cell  # 壁や外壁にぶつかったらその場に留まる
    return (r, c)


def _outcomes(cell, action):
    """意図した向きに 0.8、直交する向きに 0.1 ずつすべる。"""
    dr, dc = MOVES[action]
    slips = [(-dc, dr), (dc, -dr)]
    result = {}
    for delta, p in ((MOVES[action], 0.8), (slips[0], 0.1), (slips[1], 0.1)):
        nxt = _next_cell(cell, delta)
        result[nxt] = result.get(nxt, 0.0) + p
    del dr, dc
    return result


def _states():
    return [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) != WALL and (r, c) not in TERMINALS
    ]


def _value(v, cell):
    return TERMINALS.get(cell, v.get(cell, 0.0))


def evaluate_random_policy(sweeps=2000):
    v = {s: 0.0 for s in _states()}
    for _ in range(sweeps):
        v = {
            s: sum(
                0.25 * sum(p * (STEP_REWARD + GAMMA * _value(v, nxt)) for nxt, p in _outcomes(s, a).items())
                for a in MOVES
            )
            for s in _states()
        }
    return v


def value_iteration(sweeps=2000):
    v = {s: 0.0 for s in _states()}
    for _ in range(sweeps):
        v = {
            s: max(
                sum(p * (STEP_REWARD + GAMMA * _value(v, nxt)) for nxt, p in _outcomes(s, a).items())
                for a in MOVES
            )
            for s in _states()
        }
    greedy = {
        s: max(
            MOVES,
            key=lambda a: sum(p * (STEP_REWARD + GAMMA * _value(v, nxt)) for nxt, p in _outcomes(s, a).items()),
        )
        for s in _states()
    }
    return v, greedy


def draw_grid(ax, v, greedy=None):
    grid = np.full((ROWS, COLS), np.nan)
    for cell, value in list(v.items()) + list(TERMINALS.items()):
        grid[cell] = value
    ax.imshow(grid, cmap="RdYlGn", vmin=-1.0, vmax=1.0, alpha=0.55)
    ax.add_patch(Rectangle((WALL[1] - 0.5, WALL[0] - 0.5), 1, 1, facecolor="#9ca3af"))
    ax.text(WALL[1], WALL[0], "壁", ha="center", va="center", fontsize=10, color="white")
    for cell in list(v) + list(TERMINALS):
        r, c = cell
        terminal = cell in TERMINALS
        ax.text(
            c,
            r - (0.18 if greedy and not terminal else 0.0),
            f"{grid[cell]:+.2f}",
            ha="center",
            va="center",
            fontsize=10.5 if terminal else 9.5,
            color=INK,
        )
        if terminal:
            ax.text(c, r + 0.28, "ゴール" if grid[cell] > 0 else "落とし穴", ha="center", fontsize=8, color=GRAY)
        elif greedy:
            ax.text(c, r + 0.22, greedy[cell], ha="center", va="center", fontsize=15, color=BLUE)
    ax.set_xticks(np.arange(-0.5, COLS, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, ROWS, 1), minor=True)
    ax.grid(which="minor", color="white", lw=2.0)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)


def fig_gridworld():
    """小さな迷路でベルマン方程式を実際に解いてみる。"""
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.6))

    draw_grid(axes[0], evaluate_random_policy())
    axes[0].set_title("ランダム方策の $v_\\pi$")

    v_star, greedy = value_iteration()
    draw_grid(axes[1], v_star, greedy)
    axes[1].set_title("最適方策の $v_*$ と貪欲な行動")

    fig.suptitle(
        f"1 歩ごとに ${STEP_REWARD}$ の報酬、割引率 $\\gamma={GAMMA}$、意図した向きに進む確率 $0.8$", y=1.03
    )
    fig.text(
        0.5,
        -0.02,
        "落とし穴の隣では、すべって落ちる危険を避けるように矢印が向く",
        ha="center",
        va="top",
        fontsize=9.5,
        color=GRAY,
    )
    save(fig, "rl-gridworld.svg")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_policy()
    fig_transition()
    fig_markov()
    fig_return()
    fig_bellman()
    fig_value_q()
    fig_gridworld()
