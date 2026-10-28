"""content/posts/control-engineering.mdx の図を生成する。

出力先は public/img/ctl-*.svg。

    python3 -m venv .venv
    .venv/bin/pip install matplotlib numpy
    .venv/bin/python scripts/generate-control-engineering-figures.py

環境変数 CTL_FIG_PNG_DIR を指定すると、目視確認用の PNG も同時に書き出す。
"""

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent.parent / "public" / "img"
PNG_DIR = os.environ.get("CTL_FIG_PNG_DIR")

INK = "#111827"
MUTED = "#6b7280"
LINE = "#9ca3af"
FAINT = "#e5e7eb"
BLUE = "#2563eb"
ORANGE = "#ea580c"
GREEN = "#16a34a"
PURPLE = "#7c3aed"
RED = "#dc2626"

plt.rcParams.update(
    {
        "font.family": ["Hiragino Sans", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "axes.edgecolor": "#9ca3af",
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "grid.color": FAINT,
        "grid.linewidth": 0.8,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "svg.fonttype": "path",
        "legend.frameon": False,
        "mathtext.fontset": "cm",
    }
)


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.05)
    if PNG_DIR:
        fig.savefig(
            Path(PNG_DIR) / name.replace(".svg", ".png"),
            format="png",
            dpi=110,
            bbox_inches="tight",
            pad_inches=0.05,
        )
    plt.close(fig)
    print(f"wrote {path.relative_to(OUT_DIR.parent.parent)}")


# ---------------------------------------------------------------------------
# 数値計算のヘルパー (scipy に頼らず numpy だけで書く)
# ---------------------------------------------------------------------------


def expm(M):
    """スケーリング・アンド・スクエアリング + Taylor 展開による行列指数関数。"""
    norm = np.linalg.norm(M, 1)
    k = max(0, int(np.ceil(np.log2(norm))) + 1) if norm > 0 else 0
    A = M / 2**k
    E = np.eye(len(M))
    term = np.eye(len(M))
    for i in range(1, 20):
        term = term @ A / i
        E = E + term
    for _ in range(k):
        E = E @ E
    return E


def c2d(A, B, dt):
    """零次ホールドによる厳密な離散化。"""
    n, m = B.shape
    M = np.zeros((n + m, n + m))
    M[:n, :n] = A
    M[:n, n:] = B
    E = expm(M * dt)
    return E[:n, :n], E[:n, n:]


def tf2ss(num, den):
    """伝達関数 num/den (厳密にプロパー) の可制御正準形。"""
    num = np.atleast_1d(np.asarray(num, float))
    den = np.atleast_1d(np.asarray(den, float))
    num, den = num / den[0], den / den[0]
    n = len(den) - 1
    num = np.concatenate([np.zeros(n - len(num)), num])
    A = np.zeros((n, n))
    A[:-1, 1:] = np.eye(n - 1)
    A[-1, :] = -den[1:][::-1]
    B = np.zeros((n, 1))
    B[-1, 0] = 1.0
    C = num[::-1].reshape(1, n)
    return A, B, C


def step(num, den, t):
    A, B, C = tf2ss(num, den)
    Ad, Bd = c2d(A, B, t[1] - t[0])
    x = np.zeros((len(A), 1))
    y = np.empty_like(t)
    for i in range(len(t)):
        y[i] = (C @ x)[0, 0]
        x = Ad @ x + Bd
    return y


def impulse_from_poles(poles, t):
    """極 (共役対は片方だけ渡す) から代表的なインパルス応答を作る。"""
    p = poles[0]
    if abs(p.imag) < 1e-9:
        return np.exp(p.real * t)
    return np.exp(p.real * t) * np.sin(p.imag * t)


def freq(num, den, w):
    s = 1j * w
    return np.polyval(num, s) / np.polyval(den, s)


def db(x):
    return 20 * np.log10(np.abs(x))


# ---------------------------------------------------------------------------
# 1 次遅れ系のステップ応答
# ---------------------------------------------------------------------------


def fig_first_order():
    t = np.linspace(0, 6, 600)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for T, c in [(0.5, BLUE), (1.0, ORANGE), (2.0, GREEN)]:
        y = 1 - np.exp(-t / T)
        ax.plot(t, y, color=c, lw=2, label=f"$T={T}$")
        ax.plot([T], [1 - np.exp(-1)], "o", color=c, ms=5, zorder=5)
    # T=1 の接線: 原点での傾きは 1/T
    ax.plot([0, 1], [0, 1], color=ORANGE, ls="--", lw=1)
    ax.axhline(1 - np.exp(-1), color=LINE, lw=1, ls=":")
    ax.axhline(1, color=LINE, lw=1)
    ax.text(5.95, 1 - np.exp(-1) + 0.02, "63.2%", ha="right", va="bottom", color=MUTED)
    ax.annotate(
        "原点での接線は\n$t=T$ で最終値に届く",
        xy=(0.75, 0.75),
        xytext=(1.6, 0.42),
        color=ORANGE,
        fontsize=10,
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1),
    )
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 1.1)
    ax.set_xlabel("時間 $t$")
    ax.set_ylabel("出力 $y(t)$")
    ax.set_title(r"1 次遅れ系 $G(s)=\dfrac{1}{Ts+1}$ のステップ応答")
    ax.legend(loc="lower right")
    save(fig, "ctl-first-order.svg")


# ---------------------------------------------------------------------------
# 2 次遅れ系のステップ応答と行き過ぎ量
# ---------------------------------------------------------------------------


def fig_second_order():
    t = np.linspace(0, 15, 1500)
    zetas = [0.1, 0.3, 0.5, 0.707, 1.0, 2.0]
    colors = [RED, ORANGE, "#ca8a04", GREEN, BLUE, PURPLE]
    fig, (ax, ax2) = plt.subplots(
        1, 2, figsize=(10.5, 3.9), gridspec_kw=dict(width_ratios=[1.7, 1])
    )
    for z, c in zip(zetas, colors):
        y = step([1.0], [1.0, 2 * z, 1.0], t)
        ax.plot(t, y, color=c, lw=1.8, label=rf"$\zeta={z}$")
    ax.axhline(1, color=LINE, lw=1)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1.85)
    ax.set_xlabel(r"正規化時間 $\omega_n t$")
    ax.set_ylabel("出力 $y(t)$")
    ax.set_title(r"$G(s)=\dfrac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}$ のステップ応答")
    ax.legend(loc="upper right", ncol=2, fontsize=9.5)

    z = np.linspace(0.01, 0.999, 400)
    os_ = 100 * np.exp(-z * np.pi / np.sqrt(1 - z**2))
    ax2.plot(z, os_, color=INK, lw=2)
    for zz, c in zip(zetas[:4], colors[:4]):
        v = 100 * np.exp(-zz * np.pi / np.sqrt(1 - zz**2))
        ax2.plot([zz], [v], "o", color=c, ms=6, zorder=5)
    ax2.annotate(
        r"$\zeta=1/\sqrt{2}$ で約 4.3%",
        xy=(0.707, 4.3),
        xytext=(0.45, 45),
        fontsize=10,
        color=GREEN,
        arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1),
    )
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 100)
    ax2.set_xlabel(r"減衰係数 $\zeta$")
    ax2.set_ylabel("行き過ぎ量 [%]")
    ax2.set_title(r"行き過ぎ量 $e^{-\zeta\pi/\sqrt{1-\zeta^2}}$")
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-second-order.svg")


# ---------------------------------------------------------------------------
# 極の位置とインパルス応答
# ---------------------------------------------------------------------------


def fig_poles():
    cases = [
        ("A", [-1.5 + 0j], BLUE),
        ("B", [-0.4 + 3j], GREEN),
        ("C", [0 + 3j], ORANGE),
        ("D", [0.25 + 3j], RED),
        ("E", [0.5 + 0j], PURPLE),
        ("F", [-0.4 + 1.2j], "#0891b2"),
    ]
    fig = plt.figure(figsize=(10.5, 4.6))
    gs = fig.add_gridspec(2, 5, width_ratios=[1.9, 0.15, 1, 1, 1], hspace=0.55, wspace=0.35)
    ax = fig.add_subplot(gs[:, 0])
    ax.axvspan(-2.2, 0, color="#dbeafe", alpha=0.6, lw=0)
    ax.axvspan(0, 1.2, color="#fee2e2", alpha=0.6, lw=0)
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=INK, lw=0.9)
    ax.text(-2.1, -3.85, "安定 (左半平面)", color=BLUE, fontsize=10)
    ax.text(0.08, -3.85, "不安定", color=RED, fontsize=10)
    for name, ps, c in cases:
        for p in ps:
            pts = [p] if abs(p.imag) < 1e-9 else [p, p.conjugate()]
            for q in pts:
                ax.plot(q.real, q.imag, "x", color=c, ms=10, mew=2.4)
            ax.text(p.real + 0.1, p.imag + 0.25, name, color=c, fontsize=11, weight="bold")
    ax.set_xlim(-2.2, 1.2)
    ax.set_ylim(-4.1, 4.1)
    ax.set_xlabel(r"実部 $\mathrm{Re}\,s$")
    ax.set_ylabel(r"虚部 $\mathrm{Im}\,s$")
    ax.set_title("$s$ 平面上の極")

    t = np.linspace(0, 8, 800)
    for i, (name, ps, c) in enumerate(cases):
        a = fig.add_subplot(gs[i // 3, 2 + i % 3])
        y = impulse_from_poles(ps, t)
        a.plot(t, y, color=c, lw=1.8)
        a.axhline(0, color=LINE, lw=0.8)
        a.set_title(name, color=c, weight="bold")
        a.set_xticks([])
        a.set_yticks([])
        lim = max(1.05, np.abs(y).max() * 1.1)
        a.set_ylim(-lim, lim)
    save(fig, "ctl-poles.svg")


# ---------------------------------------------------------------------------
# ボード線図 (1 次遅れと 2 次遅れ)
# ---------------------------------------------------------------------------


def fig_bode():
    w = np.logspace(-2, 2, 800)
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 5.6), sharex="col")

    g = freq([1.0], [1.0, 1.0], w)
    ax, axp = axes[0, 0], axes[1, 0]
    ax.semilogx(w, db(g), color=BLUE, lw=2, label="厳密")
    asym = np.where(w < 1, 0, -20 * np.log10(w))
    ax.semilogx(w, asym, color=ORANGE, lw=1.3, ls="--", label="折れ線近似")
    ax.plot([1], [-3.01], "o", color=BLUE, ms=5)
    ax.annotate("$-3$ dB", xy=(1, -3), xytext=(0.06, -18), color=BLUE,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1))
    ax.text(12, -15, "$-20$ dB/dec", color=ORANGE, fontsize=10)
    ax.set_ylim(-42, 6)
    ax.set_ylabel("ゲイン [dB]")
    ax.set_title(r"1 次遅れ $\dfrac{1}{s+1}$ (折れ点 $\omega=1/T=1$)")
    ax.legend(loc="lower left", fontsize=9.5)
    axp.semilogx(w, np.degrees(np.angle(g)), color=BLUE, lw=2)
    axp.plot([1], [-45], "o", color=BLUE, ms=5)
    axp.text(1.3, -40, "$-45^\\circ$", color=BLUE)
    axp.set_ylim(-95, 5)
    axp.set_yticks([0, -45, -90])
    axp.set_ylabel("位相 [deg]")
    axp.set_xlabel(r"角周波数 $\omega$ [rad/s]")

    ax, axp = axes[0, 1], axes[1, 1]
    for z, c in [(0.1, RED), (0.3, ORANGE), (0.707, GREEN), (1.0, BLUE)]:
        g = freq([1.0], [1.0, 2 * z, 1.0], w)
        ax.semilogx(w, db(g), color=c, lw=1.8, label=rf"$\zeta={z}$")
        axp.semilogx(w, np.degrees(np.unwrap(np.angle(g))), color=c, lw=1.8)
    ax.text(8, -30, "$-40$ dB/dec", color=MUTED, fontsize=10)
    ax.annotate("共振ピーク", xy=(1, 14), xytext=(0.04, 10), color=RED,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1))
    ax.set_ylim(-62, 18)
    ax.set_title(r"2 次遅れ $\dfrac{1}{s^2+2\zeta s+1}$")
    ax.legend(loc="lower left", fontsize=9.5)
    axp.set_ylim(-185, 5)
    axp.set_yticks([0, -90, -180])
    axp.set_xlabel(r"正規化角周波数 $\omega/\omega_n$")
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-bode.svg")


# ---------------------------------------------------------------------------
# 安定余裕: ナイキスト線図とボード線図
# L(s) = 2 / (s (s+1) (s+2))
# ---------------------------------------------------------------------------

L_NUM = [2.0]
L_DEN = np.polymul([1.0, 0.0], np.polymul([1.0, 1.0], [1.0, 2.0]))


def fig_margins():
    w = np.logspace(-1.3, 1.3, 2000)
    L = freq(L_NUM, L_DEN, w)
    phase = np.degrees(np.unwrap(np.angle(L)))
    # 位相交差: 位相が -180 度になる周波数 (= sqrt 2)
    wpc = np.sqrt(2.0)
    gm = 1 / abs(freq(L_NUM, L_DEN, np.array([wpc]))[0])
    # ゲイン交差: |L| = 1 となる周波数
    i = np.argmin(np.abs(np.abs(L) - 1))
    wgc = w[i]
    pm = 180 + phase[i]
    print(f"  GM = {gm:.3f} ({20*np.log10(gm):.2f} dB) at w={wpc:.3f},"
          f" PM = {pm:.1f} deg at w={wgc:.3f}")

    fig = plt.figure(figsize=(10.5, 4.8))
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.25], hspace=0.12, wspace=0.28)
    ax = fig.add_subplot(gs[:, 0])
    wn = np.logspace(-0.6, 2, 2000)
    Ln = freq(L_NUM, L_DEN, wn)
    ax.plot(Ln.real, Ln.imag, color=BLUE, lw=2, label=r"$\omega>0$")
    ax.plot(Ln.real, -Ln.imag, color=BLUE, lw=1.3, ls="--", label=r"$\omega<0$")
    k = len(wn) // 3
    ax.annotate("", xy=(Ln.real[k + 5], Ln.imag[k + 5]), xytext=(Ln.real[k], Ln.imag[k]),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5))
    ax.plot([-1], [0], "+", color=RED, ms=14, mew=2.4)
    ax.text(-1, 0.1, "$-1$", color=RED, ha="center")
    ax.plot([-1 / gm], [0], "o", color=ORANGE, ms=6, zorder=5)
    ax.annotate(rf"$-1/3$ (GM $={gm:.0f}$ 倍)", xy=(-1 / gm, 0), xytext=(-0.55, 0.45),
                color=ORANGE, fontsize=10,
                arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1))
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(th), np.sin(th), color=LINE, lw=1, ls=":")
    Lg = freq(L_NUM, L_DEN, np.array([wgc]))[0]
    ax.plot([0, Lg.real], [0, Lg.imag], color=GREEN, lw=1.2)
    ax.plot([0, -1], [0, 0], color=GREEN, lw=1.2)
    arc = np.linspace(np.pi, np.angle(Lg) + 2 * np.pi, 50)
    ax.plot(0.35 * np.cos(arc), 0.35 * np.sin(arc), color=GREEN, lw=1.5)
    ax.text(-0.5, -0.35, rf"PM $\approx{pm:.0f}^\circ$", color=GREEN, fontsize=10)
    ax.set_xlim(-1.6, 0.6)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.set_xlabel(r"$\mathrm{Re}\,L(j\omega)$")
    ax.set_ylabel(r"$\mathrm{Im}\,L(j\omega)$")
    ax.set_title("ナイキスト線図")
    ax.legend(loc="upper right", fontsize=9.5)

    axg = fig.add_subplot(gs[0, 1])
    axp = fig.add_subplot(gs[1, 1], sharex=axg)
    axg.semilogx(w, db(L), color=BLUE, lw=2)
    axg.axhline(0, color=INK, lw=0.9)
    axg.plot([wpc, wpc], [db(1 / gm), 0], color=ORANGE, lw=2.5)
    axg.text(wpc * 1.12, -6, f"GM ≈ {20*np.log10(gm):.1f} dB", color=ORANGE, fontsize=10)
    axg.axvline(wgc, color=GREEN, lw=0.8, ls=":")
    axg.axvline(wpc, color=ORANGE, lw=0.8, ls=":")
    axg.set_ylim(-45, 35)
    axg.set_ylabel("ゲイン [dB]")
    axg.set_title(r"ボード線図  $L(s)=\dfrac{2}{s(s+1)(s+2)}$")
    plt.setp(axg.get_xticklabels(), visible=False)
    axp.semilogx(w, phase, color=BLUE, lw=2)
    axp.axhline(-180, color=INK, lw=0.9)
    axp.plot([wgc, wgc], [-180, phase[i]], color=GREEN, lw=2.5)
    axp.text(wgc * 0.25, -168, f"PM ≈ {pm:.0f}°", color=GREEN, fontsize=10)
    axp.axvline(wgc, color=GREEN, lw=0.8, ls=":")
    axp.axvline(wpc, color=ORANGE, lw=0.8, ls=":")
    axp.set_ylim(-260, -80)
    axp.set_yticks([-90, -135, -180, -225])
    axp.set_ylabel("位相 [deg]")
    axp.set_xlabel(r"角周波数 $\omega$ [rad/s]")
    save(fig, "ctl-margins.svg")


# ---------------------------------------------------------------------------
# 根軌跡: 1 + K / (s (s+1) (s+2)) = 0
# ---------------------------------------------------------------------------


def fig_root_locus():
    Ks = np.concatenate([np.linspace(0, 1, 400), np.logspace(0, 2.2, 1200)])
    roots = np.array([np.sort_complex(np.roots([1, 3, 2, K])) for K in Ks])
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    ax.axvspan(0, 2, color="#fee2e2", alpha=0.6, lw=0)
    ax.axhline(0, color=INK, lw=0.9)
    ax.axvline(0, color=INK, lw=0.9)
    # 漸近線: 重心 -1, 角度 ±60°, 180°
    for ang in [np.pi / 3, -np.pi / 3]:
        ax.plot([-1, -1 + 6 * np.cos(ang)], [0, 6 * np.sin(ang)], color=LINE, lw=1, ls="--")
    pts = roots.flatten()
    # 枝ごとに描くと分岐点で並びが入れ替わるので、点の集まりとして描く
    ax.plot(pts.real, pts.imag, ".", color=BLUE, ms=1.6)
    for p in [0, -1, -2]:
        ax.plot(p, 0, "x", color=INK, ms=10, mew=2.2)
    sb = -1 + 1 / np.sqrt(3)
    ax.plot(sb, 0, "o", color=PURPLE, ms=6, zorder=5)
    ax.annotate(f"分岐点 $s\\approx{sb:.2f}$\n($K\\approx0.38$)", xy=(sb, 0), xytext=(-2.9, 1.2),
                color=PURPLE, fontsize=10,
                arrowprops=dict(arrowstyle="-|>", color=PURPLE, lw=1))
    for sgn in [1, -1]:
        ax.plot(0, sgn * np.sqrt(2), "o", color=RED, ms=7, zorder=5)
    ax.annotate(r"$K=6$ で虚軸を横切る ($s=\pm j\sqrt{2}$)", xy=(0, np.sqrt(2)), xytext=(-3.0, 2.6),
                color=RED, fontsize=10,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1))
    r2 = np.sort_complex(np.roots([1, 3, 2, 2]))
    ax.plot(r2.real, r2.imag, "s", color=GREEN, ms=6, zorder=6, label="$K=2$ の閉ループ極")
    ax.text(-1.0, -0.35, "漸近線の重心 $-1$", color=MUTED, fontsize=9.5, ha="center")
    ax.set_xlim(-3.2, 1.2)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect("equal")
    ax.set_xlabel(r"実部 $\mathrm{Re}\,s$")
    ax.set_ylabel(r"虚部 $\mathrm{Im}\,s$")
    ax.set_title(r"根軌跡  $1+\dfrac{K}{s(s+1)(s+2)}=0$")
    ax.legend(loc="lower left", fontsize=9.5)
    save(fig, "ctl-root-locus.svg")


# ---------------------------------------------------------------------------
# PID 制御: G(s) = 1/(s+1)^3, ジーグラー・ニコルスの限界感度法
# ---------------------------------------------------------------------------

G_DEN = np.polymul([1.0, 1.0], np.polymul([1.0, 1.0], [1.0, 1.0]))


def closed_loop_pid(Kp, Ti=None, Td=0.0):
    """C(s) = Kp (1 + 1/(Ti s) + Td s), G(s) = 1/(s+1)^3 の閉ループ伝達関数。"""
    if Ti is None:
        c_num, c_den = np.array([Kp * Td, Kp]), np.array([1.0])
        if Td == 0:
            c_num = np.array([Kp])
    else:
        c_num = Kp * np.array([Ti * Td, Ti, 1.0])
        c_den = np.array([Ti, 0.0])
    ol_num = c_num
    ol_den = np.polymul(c_den, G_DEN)
    return ol_num, np.polyadd(ol_den, ol_num)


def fig_pid():
    t = np.linspace(0, 25, 2500)
    Ku, Tu = 8.0, 2 * np.pi / np.sqrt(3)
    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.5, 3.9), gridspec_kw=dict(width_ratios=[1, 1.5])
    )
    for K, c in [(4.0, BLUE), (Ku, RED)]:
        y = step(*closed_loop_pid(K), t)
        lab = rf"$K_p={K:g}$" + (r"$\,(=K_u)$" if K == Ku else "")
        ax1.plot(t, y, color=c, lw=1.8, label=lab)
    # 最初の山から 1 周期分の矢印を引く
    tp = t[np.argmax(np.where(t < 4, y, 0))]
    for x in (tp, tp + Tu):
        ax1.plot([x, x], [y.max(), 1.85], color=RED, lw=0.8, ls=":")
    ax1.annotate("", xy=(tp + Tu, 1.8), xytext=(tp, 1.8),
                 arrowprops=dict(arrowstyle="<->", color=RED, lw=1, shrinkA=0, shrinkB=0))
    ax1.text(tp + Tu + 0.3, 1.8, rf"$T_u\approx{Tu:.2f}$", color=RED, ha="left", va="center")
    ax1.axhline(1, color=LINE, lw=1)
    ax1.set_xlim(0, 20)
    ax1.set_ylim(0, 2.3)
    ax1.set_xlabel("時間 $t$")
    ax1.set_ylabel("出力 $y(t)$")
    ax1.set_title("P 制御でゲインを上げて持続振動を探す")
    ax1.legend(loc="upper right", ncol=2, fontsize=9.5)

    cfgs = [
        ("P", dict(Kp=0.5 * Ku), BLUE),
        ("PI", dict(Kp=0.45 * Ku, Ti=Tu / 1.2), ORANGE),
        ("PID", dict(Kp=0.6 * Ku, Ti=0.5 * Tu, Td=0.125 * Tu), GREEN),
    ]
    for name, p, c in cfgs:
        y = step(*closed_loop_pid(**p), t)
        ax2.plot(t, y, color=c, lw=1.9, label=name)
        print(f"  {name}: final={y[-1]:.3f} max={y.max():.3f}")
    ax2.axhline(1, color=LINE, lw=1)
    ax2.axhline(0.8, color=BLUE, lw=0.8, ls=":")
    ax2.annotate("定常偏差 $1/(1+K_p)=0.2$", xy=(22, 0.8), xytext=(14, 0.35), color=BLUE, fontsize=10,
                 arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1))
    ax2.set_xlim(0, 25)
    ax2.set_ylim(0, 2.3)
    ax2.set_xlabel("時間 $t$")
    ax2.set_title(r"ジーグラー・ニコルスの調整則  $G(s)=\dfrac{1}{(s+1)^3}$")
    ax2.legend(loc="upper right", fontsize=10)
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-pid.svg")


# ---------------------------------------------------------------------------
# 定常偏差: 0 型と 1 型にステップ・ランプを入れる
# ---------------------------------------------------------------------------


def fig_steady_state():
    t = np.linspace(0, 12, 1200)
    # 0 型: L = 4/(s+1)^2 → 閉ループ 4/(s^2+2s+5)
    # 1 型: L = 2/(s(s+1)) → 閉ループ 2/(s^2+s+2)
    sys0 = ([4.0], [1.0, 2.0, 5.0])
    sys1 = ([2.0], [1.0, 1.0, 2.0])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    ax1.axhline(1, color=INK, lw=1.2, label="目標値 $r(t)$")
    ax1.plot(t, step(*sys0, t), color=ORANGE, lw=1.9, label=r"0 型 $L=\frac{4}{(s+1)^2}$")
    ax1.plot(t, step(*sys1, t), color=BLUE, lw=1.9, label=r"1 型 $L=\frac{2}{s(s+1)}$")
    ax1.annotate("", xy=(11, 0.8), xytext=(11, 1.0),
                 arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1))
    ax1.text(10.85, 0.9, "$e_\\infty=1/(1+K_p)=0.2$", color=ORANGE, ha="right", va="center", fontsize=10)
    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 1.5)
    ax1.set_xlabel("時間 $t$")
    ax1.set_title("ステップ目標値")
    ax1.legend(loc="lower right", fontsize=9.5)

    # ランプ応答 = ステップ応答の積分 → 分母に s を掛ける
    y0 = step(sys0[0], np.polymul(sys0[1], [1.0, 0.0]), t)
    y1 = step(sys1[0], np.polymul(sys1[1], [1.0, 0.0]), t)
    ax2.plot(t, t, color=INK, lw=1.2, label="目標値 $r(t)=t$")
    ax2.plot(t, y0, color=ORANGE, lw=1.9, label="0 型 (偏差が発散)")
    ax2.plot(t, y1, color=BLUE, lw=1.9, label="1 型")
    ax2.annotate("", xy=(11, 10.5), xytext=(11, 11),
                 arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1, shrinkA=0, shrinkB=0))
    ax2.text(10.8, 10.75, "$e_\\infty=1/K_v=0.5$", color=BLUE, ha="right", va="bottom", fontsize=10)
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 12.5)
    ax2.set_xlabel("時間 $t$")
    ax2.set_title("ランプ目標値")
    ax2.legend(loc="upper left", fontsize=9.5)
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-steady-state.svg")


# ---------------------------------------------------------------------------
# 状態フィードバック (極配置) と LQR: 倒立振子 x'' = x + u
# ---------------------------------------------------------------------------

A_PEN = np.array([[0.0, 1.0], [1.0, 0.0]])
B_PEN = np.array([[0.0], [1.0]])
C_PEN = np.array([[1.0, 0.0]])


def simulate_sf(K, x0, t):
    Acl = A_PEN - B_PEN @ K
    Ad = expm(Acl * (t[1] - t[0]))
    x = np.array(x0, float).reshape(2, 1)
    xs = np.empty((len(t), 2))
    for i in range(len(t)):
        xs[i] = x[:, 0]
        x = Ad @ x
    us = -(xs[:, 0] * K[0, 0] + xs[:, 1] * K[0, 1])
    return xs, us


def care(A, B, Q, R):
    """ハミルトン行列の安定固有空間から連続時間リカッチ方程式を解く。"""
    n = len(A)
    Rinv = np.linalg.inv(R)
    H = np.block([[A, -B @ Rinv @ B.T], [-Q, -A.T]])
    vals, vecs = np.linalg.eig(H)
    V = vecs[:, vals.real < 0]
    P = np.real(V[n:] @ np.linalg.inv(V[:n]))
    return (P + P.T) / 2


def fig_state_feedback():
    t = np.linspace(0, 6, 1200)
    x0 = [0.2, 0.0]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    xs_ol, _ = simulate_sf(np.zeros((1, 2)), x0, t)
    ax1.plot(t, xs_ol[:, 0], color=LINE, lw=1.6, ls="--", label="フィードバックなし")
    for p, c in [(1, BLUE), (2, GREEN), (4, ORANGE)]:
        K = np.array([[p**2 + 1, 2 * p]])
        xs, us = simulate_sf(K, x0, t)
        lab = rf"極 $-{p},-{p}$  $K=({p**2+1},{2*p})$"
        ax1.plot(t, xs[:, 0], color=c, lw=1.9, label=lab)
        ax2.plot(t, us, color=c, lw=1.9, label=lab)
    ax1.axhline(0, color=INK, lw=0.9)
    ax1.set_xlim(0, 6)
    ax1.set_ylim(-0.05, 0.6)
    ax1.set_xlabel("時間 $t$")
    ax1.set_ylabel(r"角度 $\theta(t)$")
    ax1.set_title(r"倒立振子 $\ddot\theta=\theta+u$ を $u=-Kx$ で安定化")
    ax1.legend(loc="upper right", fontsize=9)
    ax2.axhline(0, color=INK, lw=0.9)
    ax2.set_xlim(0, 6)
    ax2.set_xlabel("時間 $t$")
    ax2.set_ylabel("操作量 $u(t)$")
    ax2.set_title("速い極ほど大きな入力が要る")
    ax2.legend(loc="lower right", fontsize=9)
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-state-feedback.svg")

    for r in [0.1, 1.0, 10.0]:
        P = care(A_PEN, B_PEN, np.eye(2), np.array([[r]]))
        K = (B_PEN.T @ P) / r
        eig = np.linalg.eigvals(A_PEN - B_PEN @ K)
        print(f"  LQR R={r}: K={K.round(3)}, poles={eig.round(3)}")


def fig_lqr():
    t = np.linspace(0, 8, 1600)
    x0 = [0.2, 0.0]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    for r, c in [(0.1, ORANGE), (1.0, GREEN), (10.0, BLUE)]:
        P = care(A_PEN, B_PEN, np.eye(2), np.array([[r]]))
        K = (B_PEN.T @ P) / r
        xs, us = simulate_sf(K, x0, t)
        lab = rf"$R={r:g}$  $K=({K[0,0]:.2f},{K[0,1]:.2f})$"
        ax1.plot(t, xs[:, 0], color=c, lw=1.9, label=lab)
        ax2.plot(t, us, color=c, lw=1.9, label=lab)
    for a in (ax1, ax2):
        a.axhline(0, color=INK, lw=0.9)
        a.set_xlim(0, 8)
        a.set_xlabel("時間 $t$")
        a.legend(loc="lower right" if a is ax2 else "upper right", fontsize=9.5)
    ax1.set_ylabel(r"角度 $\theta(t)$")
    ax1.set_title(r"LQR ($Q=I$) の応答")
    ax2.set_ylabel("操作量 $u(t)$")
    ax2.set_title("$R$ を大きくすると入力を節約する")
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-lqr.svg")


# ---------------------------------------------------------------------------
# オブザーバ: 角度だけを測って角速度を推定する
# ---------------------------------------------------------------------------


def fig_observer():
    t = np.linspace(0, 5, 1000)
    dt = t[1] - t[0]
    K = np.array([[5.0, 4.0]])  # 極 -2, -2
    q = 6.0
    Lg = np.array([[2 * q], [q**2 + 1]])  # 推定誤差の極 -6, -6
    # 拡大系 [x; xhat]
    Abig = np.block(
        [
            [A_PEN, -B_PEN @ K],
            [Lg @ C_PEN, A_PEN - B_PEN @ K - Lg @ C_PEN],
        ]
    )
    Ad = expm(Abig * dt)
    z = np.array([[0.2], [0.0], [0.0], [0.0]])
    zs = np.empty((len(t), 4))
    for i in range(len(t)):
        zs[i] = z[:, 0]
        z = Ad @ z
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 3.7))
    ax1.plot(t, zs[:, 0], color=BLUE, lw=2, label=r"真値 $\theta$ (測定できる)")
    ax1.plot(t, zs[:, 2], color=BLUE, lw=1.6, ls="--", label=r"推定値 $\hat\theta$")
    ax1.set_title("角度")
    ax2.plot(t, zs[:, 1], color=ORANGE, lw=2, label=r"真値 $\dot\theta$ (測定できない)")
    ax2.plot(t, zs[:, 3], color=ORANGE, lw=1.6, ls="--", label=r"推定値 $\hat{\dot\theta}$")
    ax2.set_title("角速度")
    for a in (ax1, ax2):
        a.axhline(0, color=INK, lw=0.9)
        a.set_xlim(0, 5)
        a.set_xlabel("時間 $t$")
        a.legend(loc="upper right", fontsize=9.5)
    fig.tight_layout(w_pad=2.5)
    save(fig, "ctl-observer.svg")


# ---------------------------------------------------------------------------
# ラプラス変換の像 |F(s)| を s 平面上の曲面として描く
# F(s) = 1 / ((s + 0.5)^2 + 4)  (f(t) = e^{-0.5t} sin(2t) / 2)
# ---------------------------------------------------------------------------


def fig_laplace_surface():
    def F(s):
        return 1 / ((s + 0.5) ** 2 + 4)

    cap = 1.5
    sig = np.linspace(-2.0, 1.0, 241)
    om = np.linspace(-3.5, 3.5, 281)
    S, W = np.meshgrid(sig, om)
    Z = np.minimum(np.abs(F(S + 1j * W)), cap)

    fig = plt.figure(figsize=(10.5, 4.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.45, 1], wspace=0.3)
    ax = fig.add_subplot(gs[0], projection="3d", computed_zorder=False)
    ax.plot_surface(S, W, Z, cmap="Blues", vmin=-0.4, vmax=cap, rstride=4, cstride=4,
                    linewidth=0.15, edgecolor="#93c5fd", alpha=0.95, zorder=1)
    # 虚軸での断面 = 周波数応答
    wj = np.linspace(-3.5, 3.5, 400)
    ax.plot(np.zeros_like(wj), wj, np.abs(F(1j * wj)), color=RED, lw=2.4, zorder=5)
    for w0 in (2.0, -2.0):
        ax.plot([-0.5, -0.5], [w0, w0], [0, cap], color=INK, lw=1.2, ls="--", zorder=6)
        ax.scatter([-0.5], [w0], [0], color=INK, marker="x", s=40, zorder=6)
    ax.text(-0.5, 2.0, cap + 0.12, "極 $-0.5+2j$", color=INK, fontsize=10, ha="center")
    ax.text2D(0.02, 0.86, r"赤線: $s=j\omega$ (虚軸) での断面", transform=ax.transAxes, color=RED, fontsize=10)
    ax.set_xlabel(r"$\sigma=\mathrm{Re}\,s$", labelpad=4)
    ax.set_ylabel(r"$\omega=\mathrm{Im}\,s$", labelpad=4)
    ax.set_zlabel(r"$|F(s)|$", labelpad=8)
    ax.set_xticks([-2, -1, 0, 1])
    ax.set_yticks([-3, 0, 3])
    ax.set_zlim(0, cap)
    ax.set_zticks([0, 0.5, 1.0, 1.5])
    ax.tick_params(axis="z", pad=4)
    ax.view_init(elev=28, azim=-58)
    ax.set_box_aspect((1.1, 1.6, 0.9))
    ax.set_title(r"$|F(s)|,\ F(s)=\dfrac{1}{(s+0.5)^2+4}$" + "\n(1.5 で頭打ちにして表示)", fontsize=11)

    ax2 = fig.add_subplot(gs[1])
    wp = np.linspace(0, 6, 600)
    ax2.plot(wp, np.abs(F(1j * wp)), color=RED, lw=2.2)
    wpk = np.sqrt(4 - 0.25)
    ax2.plot([wpk], [np.abs(F(1j * wpk))], "o", color=RED, ms=6)
    ax2.annotate("極の真横を通るので\n盛り上がる (共振)", xy=(wpk, np.abs(F(1j * wpk))),
                 xytext=(3.0, 0.42), color=RED, fontsize=10,
                 arrowprops=dict(arrowstyle="-|>", color=RED, lw=1))
    ax2.set_xlim(0, 6)
    ax2.set_ylim(0, 0.6)
    ax2.set_xlabel(r"角周波数 $\omega$")
    ax2.set_ylabel(r"$|F(j\omega)|$")
    ax2.set_title("虚軸に沿った断面 = 周波数応答")
    save(fig, "ctl-laplace-surface.svg")


def main():
    fig_laplace_surface()
    fig_first_order()
    fig_second_order()
    fig_poles()
    fig_bode()
    fig_margins()
    fig_root_locus()
    fig_pid()
    fig_steady_state()
    fig_state_feedback()
    fig_lqr()
    fig_observer()


if __name__ == "__main__":
    main()
