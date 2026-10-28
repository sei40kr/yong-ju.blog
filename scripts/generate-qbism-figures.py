"""content/posts/qbism.mdx の図を生成する。

出力先は public/img/qbism-*.svg。

SIC の確率表示や Born 則との比較は、記事中の式を実際の行列で計算して描く。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-qbism-figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"

BLUE = "#2563eb"
ORANGE = "#ea580c"
GRAY = "#6b7280"
INK = "#111827"
BAND = "#94a3b8"
FAINT = "#d1d5db"

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


# ---------------------------------------------------------------- 量子力学の部品

# qubitのSIC: Bloch球に内接する正四面体の 4 頂点
TETRA = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) / np.sqrt(3)
PAULI = np.array(
    [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=complex
)


def projector(n):
    """Bloch ベクトル n の純粋状態 (I + n·σ) / 2。"""
    return (np.eye(2) + np.tensordot(n, PAULI, axes=1)) / 2


def sic_qubit():
    return np.array([projector(n) for n in TETRA])


def sic_qutrit():
    """d = 3 の SIC (Hesse SIC)。基準ベクトル (0, 1, -1)/√2 の Weyl-Heisenberg 軌道。"""
    d = 3
    omega = np.exp(2j * np.pi / d)
    x = np.roll(np.eye(d), 1, axis=0)
    z = np.diag(omega ** np.arange(d))
    psi = np.array([0, 1, -1]) / np.sqrt(2)
    vectors = [
        np.linalg.matrix_power(x, a) @ np.linalg.matrix_power(z, b) @ psi
        for a in range(d)
        for b in range(d)
    ]
    return np.array([np.outer(v, v.conj()) for v in vectors])


def sic_probabilities(rho, pis):
    """SIC 測定の結果分布 p(i) = Tr(ρ Π_i) / d。"""
    d = rho.shape[0]
    return np.real(np.einsum("ab,iba->i", rho, pis)) / d


def conditional(pis, effects):
    """r(j|i) = Tr(Π_i D_j): 空の結果 i のあとの状態 Π_i で地上の測定をしたときの分布。"""
    return np.real(np.einsum("iab,jba->ij", pis, effects))


def urgleichung(p, r):
    """Born 則を SIC で書き直したもの: q(j) = (d+1) Σ_i p(i) r(j|i) - 1。"""
    d = int(np.sqrt(len(p)))
    return (d + 1) * p @ r - 1


def random_state(d, rng):
    a = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    rho = a @ a.conj().T
    return rho / np.trace(rho)


def check():
    rng = np.random.default_rng(0)
    for pis in (sic_qubit(), sic_qutrit()):
        d = pis.shape[1]
        # SIC の定義: Σ Π_i = d I, Tr(Π_i Π_j) = 1/(d+1) (i ≠ j)
        assert np.allclose(pis.sum(axis=0), d * np.eye(d))
        gram = np.real(np.einsum("iab,jba->ij", pis, pis))
        off = 1 - np.eye(d * d)
        assert np.allclose(gram * off, off / (d + 1))
        # Urgleichung が Born 則と一致する (地上の測定は計算基底)
        effects = np.array([np.outer(e, e) for e in np.eye(d)])
        r = conditional(pis, effects)
        for _ in range(20):
            rho = random_state(d, rng)
            born = np.real(np.einsum("ab,jba->j", rho, effects))
            assert np.allclose(urgleichung(sic_probabilities(rho, pis), r), born)


# ---------------------------------------------------------------- figure 1


def setup_3d(ax, elev=22, azim=-55):
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)
    lim = 1.15
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)


def draw_sphere(ax, radius, color, alpha, wire=True):
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, np.pi, 24)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0, shade=False)
    if wire:
        ax.plot_wireframe(x, y, z, rstride=8, cstride=6, color=FAINT, lw=0.5)


def draw_tetrahedron(ax, vertices, color, lw):
    for i in range(4):
        for j in range(i + 1, 4):
            ax.plot(*zip(vertices[i], vertices[j]), color=color, lw=lw)


def fig_sic():
    """qubit の SIC-POVM は Bloch 球に内接する正四面体。"""
    fig = plt.figure(figsize=(4.8, 4.6))
    ax = fig.add_subplot(projection="3d")
    setup_3d(ax)
    draw_sphere(ax, 1.0, "#eff6ff", 0.35)

    for axis, label in zip(np.eye(3), ("x", "y", "z")):
        ax.plot(*zip(-axis, axis), color=BAND, lw=0.8, ls="--")
        ax.text(*(axis * 1.22), f"${label}$", color=GRAY, ha="center", va="center")

    draw_tetrahedron(ax, TETRA, BLUE, 1.4)
    for i, n in enumerate(TETRA):
        ax.scatter(*n, color=BLUE, s=36, depthshade=False, zorder=5)
        ax.text(*(n * 1.18), f"$\\Pi_{i + 1}$", color=INK, ha="center", va="center")

    ax.set_title("qubitのSIC: Bloch球に内接する正四面体", pad=0)
    save(fig, "qbism-sic.svg")


# ---------------------------------------------------------------- figure 2


def fig_state_space():
    """SIC の確率ベクトルで見ると、qubit の状態空間は確率単体の内接球。"""
    fig = plt.figure(figsize=(5.0, 4.8))
    ax = fig.add_subplot(projection="3d")
    setup_3d(ax, elev=12, azim=-35)

    # 確率単体 {p} を、頂点 e_i を正四面体の頂点 TETRA[i] に送って R^3 に描く。
    # このとき p ↦ Σ p_i TETRA[i] = (Bloch ベクトル) / 3 なので、
    # 純粋状態の球は半径 1/3、すなわち正四面体の内接球になる。
    draw_tetrahedron(ax, TETRA, GRAY, 1.0)
    draw_sphere(ax, 1 / 3, BLUE, 0.45, wire=False)

    for i, n in enumerate(TETRA):
        ax.text(
            *(n * 1.24),
            f"$p=e_{i + 1}$",
            color=GRAY,
            ha="center",
            va="center",
            fontsize=10,
        )
        # 内接球が面に触れる点は -TETRA[i]/3: Π_i と直交する状態 (p_i = 0)
        ax.scatter(*(-n / 3), color=ORANGE, s=22, depthshade=False, zorder=6)

    fig.text(
        0.5,
        0.17,
        "橙点: $p_i=0$ となる状態 ($\\Pi_i$ と直交する純粋状態)",
        color=INK,
        ha="center",
        fontsize=10,
    )
    ax.set_title("qubitの状態空間 (青) は確率単体 (灰) の内接球", pad=0)
    save(fig, "qbism-state-space.svg")


# ---------------------------------------------------------------- figure 3


def fig_urgleichung():
    """空の SIC 測定を行う場合 (全確率の法則) と行わない場合 (Born 則) の違い。"""
    pis = sic_qubit()
    effects = np.array([np.outer(e, e) for e in np.eye(2)])
    r = conditional(pis, effects)

    theta = np.linspace(0, np.pi, 200)
    born, classical = [], []
    for t in theta:
        rho = projector(np.array([np.sin(t), 0, np.cos(t)]))
        p = sic_probabilities(rho, pis)
        classical.append((p @ r)[0])
        born.append(urgleichung(p, r)[0])

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(theta, born, color=BLUE, lw=2.0, label="Born則 (空の測定を行わない)")
    ax.plot(
        theta,
        classical,
        color=ORANGE,
        lw=2.0,
        ls="--",
        label="全確率の法則 (空の測定を行い、結果を捨てる)",
    )
    for y in (1 / 3, 2 / 3):
        ax.axhline(y, color=FAINT, lw=0.8, zorder=0)
    ax.text(np.pi + 0.05, 2 / 3, "2/3", color=GRAY, va="center", fontsize=10)
    ax.text(np.pi + 0.05, 1 / 3, "1/3", color=GRAY, va="center", fontsize=10)
    ax.annotate(
        "$q(0)=3\\,\\sum_i p(i)\\,r(0|i)-1$",
        xy=(0.55, float(np.interp(0.55, theta, born))),
        xytext=(1.2, 0.82),
        color=BLUE,
        arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.8),
    )
    ax.annotate(
        "$\\sum_i p(i)\\,r(0|i)$",
        xy=(2.3, float(np.interp(2.3, theta, classical))),
        xytext=(2.45, 0.12),
        color=ORANGE,
        arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.8),
    )

    ax.set_xlim(0, np.pi + 0.35)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xticks([0, np.pi / 2, np.pi])
    ax.set_xticklabels(["0", "π/2", "π"])
    ax.set_xlabel("測定前の状態 $|\\psi(\\theta)\\rangle$ のBloch球上の極角 $\\theta$")
    ax.set_ylabel("地上の測定で 0 が出る確率")
    ax.set_title("空の測定を実際に行うかどうかで、地上の確率は変わる")
    ax.legend(loc="lower left", fontsize=10)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    save(fig, "qbism-urgleichung.svg")


# ---------------------------------------------------------------- figure 4


def fig_update():
    """測定結果を見たあとの状態の変化は、SIC の確率ベクトルの書き換え。"""
    pis = sic_qubit()
    theta = 2 * np.pi / 3
    before = sic_probabilities(projector(np.array([np.sin(theta), 0, np.cos(theta)])), pis)
    after = sic_probabilities(projector(np.array([0, 0, 1])), pis)

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    x = np.arange(4)
    w = 0.38
    ax.bar(x - w / 2 - 0.01, before, w, color=BAND, label="測定前 $p(i)$")
    ax.bar(x + w / 2 + 0.01, after, w, color=BLUE, label="結果 0 を見たあと $p'(i)$")
    for xi, (b, a) in enumerate(zip(before, after)):
        ax.text(xi - w / 2 - 0.01, b + 0.01, f"{b:.2f}", ha="center", fontsize=9, color=INK)
        ax.text(xi + w / 2 + 0.01, a + 0.01, f"{a:.2f}", ha="center", fontsize=9, color=INK)
    ax.axhline(0.25, color=FAINT, lw=0.8, zorder=0)
    ax.text(3.6, 0.25, "1/4", color=GRAY, va="center", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels([f"$\\Pi_{i + 1}$" for i in x])
    ax.set_xlim(-0.6, 3.9)
    ax.set_ylim(0, 0.66)
    ax.set_ylabel("SIC測定の結果への確率")
    ax.set_title("「状態の収縮」は確率ベクトルの書き換え")
    ax.legend(loc="upper right", fontsize=10)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    save(fig, "qbism-update.svg")


FIGURES = (fig_sic, fig_state_space, fig_urgleichung, fig_update)


if __name__ == "__main__":
    check()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for figure in FIGURES:
        figure()
