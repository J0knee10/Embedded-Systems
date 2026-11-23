"""Draws every figure used in the SC3102 past-paper solutions.

Run:  python make_figures.py      (writes PNGs into ./figs)
Each figure is computed from the formula derived in the solution, and where
possible cross-checked against a brute-force numerical computation, so the
plots double as a check on the algebra.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 9, "axes.grid": True, "grid.alpha": 0.3,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 10, "axes.titleweight": "bold",
})
BLUE, RED, GREEN, ORANGE, GREY = "#1f5fa8", "#c0392b", "#2e7d32", "#e67e22", "#777777"


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=110)
    plt.close(fig)
    print("wrote", name)


def axes0(ax):
    ax.axhline(0, color="k", lw=0.8)
    ax.axvline(0, color="k", lw=0.8)


def impulse(ax, t0, area, color=BLUE, text=None, dy=0.15):
    ax.annotate("", xy=(t0, area), xytext=(t0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=color, shrinkA=0, shrinkB=0))
    if text is not None:
        ax.text(t0, area + (dy if area >= 0 else -dy), text, ha="center",
                va="bottom" if area >= 0 else "top", color=color, fontsize=8)


def lines(ax, f, v, color=BLUE, fmt="{:g}", yoff=None):
    f, v = np.asarray(f, float), np.asarray(v, float)
    ax.vlines(f, 0, v, color=color, lw=2)
    ax.plot(f, v, "o", color=color, ms=5)
    span = max(abs(v).max(), 1e-9)
    yoff = 0.06 * span if yoff is None else yoff
    for fi, vi in zip(f, v):
        ax.text(fi, vi + (yoff if vi >= 0 else -yoff), fmt.format(vi), ha="center",
                va="bottom" if vi >= 0 else "top", fontsize=8, color=color)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xticks(f)


def stems(ax, n, v, color=BLUE, label=None):
    ax.vlines(n, 0, v, color=color, lw=1.5)
    ax.plot(n, v, "o", color=color, ms=4, label=label)
    ax.axhline(0, color="k", lw=0.8)


def splane(ax, zeros, poles, roc_from, lim=(-3, 3, -2.5, 2.5), roc_text=None):
    x0, x1, y0, y1 = lim
    ax.axvspan(roc_from, x1, color=GREEN, alpha=0.13)
    ax.axvline(roc_from, color=GREEN, ls="--", lw=1)
    axes0(ax)
    ax.plot(np.real(poles), np.imag(poles), "x", color=RED, ms=10, mew=2.5, label="pole")
    if len(zeros):
        ax.plot(np.real(zeros), np.imag(zeros), "o", mfc="none", mec=BLUE, ms=10, mew=2, label="zero")
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_xlabel(r"$\sigma=\mathrm{Re}(s)$"); ax.set_ylabel(r"$j\omega=\mathrm{Im}(s)$")
    ax.text(0.98, 0.95, roc_text or "ROC", transform=ax.transAxes, ha="right", va="top",
            color=GREEN, fontsize=9, bbox=dict(fc="white", ec=GREEN, alpha=0.8))
    ax.legend(loc="lower left", fontsize=8)


def zplane(ax, zeros, poles, r_roc, lim=1.6, roc_text=None):
    ax.add_patch(Rectangle((-lim, -lim), 2 * lim, 2 * lim, color=GREEN, alpha=0.13, zorder=0))
    ax.add_patch(Circle((0, 0), r_roc, color="white", zorder=1))
    ax.add_patch(Circle((0, 0), r_roc, fill=False, ec=GREEN, ls="--", zorder=2))
    ax.add_patch(Circle((0, 0), 1, fill=False, ec="k", ls=":", lw=1.2, zorder=2))
    axes0(ax)
    ax.plot(np.real(poles), np.imag(poles), "x", color=RED, ms=10, mew=2.5, label="pole", zorder=3)
    if len(zeros):
        ax.plot(np.real(zeros), np.imag(zeros), "o", mfc="none", mec=BLUE, ms=10, mew=2, label="zero", zorder=3)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
    ax.set_xlabel("Re(z)"); ax.set_ylabel("Im(z)")
    ax.text(0.98, 0.95, roc_text or "ROC", transform=ax.transAxes, ha="right", va="top",
            color=GREEN, fontsize=9, bbox=dict(fc="white", ec=GREEN, alpha=0.8), zorder=4)
    ax.legend(loc="lower left", fontsize=8)


def sinc(x):  # course convention sinc(x) = sin(pi x)/(pi x)
    return np.sinc(x)


# =====================================================================
# 2023-24 Semester 1 (CE3102-23S1)
# =====================================================================
def fig_23s1():
    # Q1(a)(ii)
    t = np.linspace(-4.5, 6.5, 4001)
    g = lambda t: ((t >= -1) & (t < 0)) * 1.0 - ((t >= 0) & (t < 1)) * 1.0
    x = sum(g(t - 3 * n) for n in range(-3, 4))
    fig, ax = plt.subplots(figsize=(7.5, 2.4))
    ax.plot(t, x, color=BLUE, lw=2)
    ax.axvspan(-1, 2, color=ORANGE, alpha=0.12)
    ax.text(0.5, 1.25, "one period $T_0=3$", ha="center", color=ORANGE)
    ax.set_ylim(-1.5, 1.6); ax.set_xticks(range(-4, 7)); ax.set_yticks([-1, 0, 1])
    ax.set_xlabel("t"); ax.set_title(r"Q1(a)(ii)  $x(t)=\sum_n g(t-3n)$,  $g$ = +1 on (-1,0), -1 on (0,1)")
    save(fig, "23S1_Q1a_x.png")

    # Q1(b)
    f = [-200, -100, 100, 200]
    fig, axs = plt.subplots(1, 3, figsize=(10, 2.6))
    lines(axs[0], f, [10, 10, 10, 10]); axs[0].set_title("Amplitude $|c_k|$"); axs[0].set_ylim(0, 13)
    lines(axs[1], f, [-45, 45, -45, 45], color=RED, fmt="{:+g}°"); axs[1].set_title("Phase (degrees)")
    axs[1].set_ylim(-70, 70)
    lines(axs[2], f, [100, 100, 100, 100], color=GREEN); axs[2].set_title(r"Power $|c_k|^2$"); axs[2].set_ylim(0, 125)
    for a in axs: a.set_xlabel("f (Hz)")
    save(fig, "23S1_Q1b_spectra.png")

    # Q2(a): graphical convolution
    def y_an(t):
        t = np.asarray(t, float); y = np.zeros_like(t)
        m = (t >= 5) & (t < 7); y[m] = 0.8 * (np.exp(-15) - np.exp(-5 * (t[m] - 2)))
        m = (t >= 7) & (t < 8); y[m] = 0.8 * (np.exp(-5 * (t[m] - 4)) - np.exp(-5 * (t[m] - 2)))
        m = (t >= 8) & (t < 10); y[m] = 0.8 * (np.exp(-5 * (t[m] - 4)) - np.exp(-30))
        return y
    dt = 1e-4; T = np.arange(0, 12, dt)
    h = 4 * np.exp(-5 * T) * ((T >= 3) & (T < 6)); xx = ((T >= 2) & (T <= 4)) * 1.0
    y_num = np.convolve(xx, h)[: len(T)] * dt
    assert np.max(abs(y_num - y_an(T))) < 1e-8
    fig = plt.figure(figsize=(10, 4.6))
    gs = fig.add_gridspec(2, 3)
    tau = np.linspace(0, 11, 3000)
    hs = 4 * np.exp(-5 * tau) * ((tau >= 3) & (tau < 6)) * 1e6
    for i, (tv, lab) in enumerate([(6, "t = 6: partial overlap [3, t-2]"),
                                   (7.5, "t = 7.5: box inside [t-4, t-2]"),
                                   (9, "t = 9: partial overlap [t-4, 6]")]):
        ax = fig.add_subplot(gs[0, i])
        ax.plot(tau, hs, color=RED, lw=2, label=r"$h(\tau)\times10^6$")
        ax.fill_between(tau, 0, 1.4, where=(tau >= tv - 4) & (tau <= tv - 2), color=BLUE, alpha=0.25,
                        label=r"$x(t-\tau)$ (height 1)")
        ax.set_ylim(0, 1.6); ax.set_title(lab, fontsize=9); ax.set_xlabel(r"$\tau$")
        if i == 0: ax.legend(fontsize=7, loc="upper right")
    ax = fig.add_subplot(gs[1, :])
    tt = np.linspace(3, 11, 3000)
    ax.plot(tt, y_an(tt) * 1e7, color=BLUE, lw=2)
    for b in [5, 7, 8, 10]: ax.axvline(b, color=GREY, ls=":")
    ax.set_xlabel("t"); ax.set_ylabel(r"$y(t)\times10^{7}$")
    ax.set_title("Q2(a) output: zero outside 5 ≤ t < 10 (peak ≈ 2.45e-7 at t = 7)")
    save(fig, "23S1_Q2a_conv.png")

    # Q2(c)
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.8))
    t = np.linspace(-3, 3, 2000)
    axs[0].plot(t, (abs(t) <= 2) * (1 + np.cos(np.pi * t)), color=BLUE, lw=2)
    axs[0].set_title(r"$x(t)=\Pi(t/4)\,(1+\cos\pi t)$"); axs[0].set_xlabel("t")
    f = np.linspace(-2, 2, 4001)
    X = 4 * sinc(4 * f) + 2 * sinc(4 * f - 2) + 2 * sinc(4 * f + 2)
    axs[1].plot(f, 4 * sinc(4 * f), "--", color=GREY, lw=1, label=r"$4\,\mathrm{sinc}(4f)$")
    axs[1].plot(f, 2 * sinc(4 * f - 2), "--", color=ORANGE, lw=1, label=r"$2\,\mathrm{sinc}(4f\mp2)$")
    axs[1].plot(f, 2 * sinc(4 * f + 2), "--", color=ORANGE, lw=1)
    axs[1].plot(f, X, color=BLUE, lw=2, label="X(f) (sum)")
    axs[1].axhline(0, color="k", lw=0.8); axs[1].legend(fontsize=7); axs[1].set_xlabel("f (Hz)")
    axs[1].set_title("X(f): main lobe to |f| = 0.5, X(0) = 4")
    save(fig, "23S1_Q2c_X.png")

    # Q3(b)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.2))
    splane(axs[0], [0.5], [-1], -1, lim=(-2.5, 2, -2, 2), roc_text="ROC: Re(s) > -1\nincludes jω-axis → stable")
    axs[0].set_title(r"Q3(b)(i)  $H(s)=\frac{s-0.5}{s+1}$")
    t = np.linspace(0, 8, 2000)
    axs[1].plot(t, -1 + 3 * np.exp(-t), color=BLUE, lw=2, label=r"(ii) $-1+3e^{-t}$")
    sysH = signal.lti([1, -0.5], [1, 1])
    _, y3, _ = signal.lsim(sysH, 2 + 3 * np.cos(2 * t), t)
    Hj2 = (2j - 0.5) / (2j + 1)
    axs[1].plot(t, y3, color=ORANGE, lw=1.5, label="(iii) full response (simulated)")
    axs[1].plot(t, -1 + 3 * abs(Hj2) * np.cos(2 * t + np.angle(Hj2)), "--", color=RED, lw=1.2,
                label=r"(iii) steady state $-1+2.766\cos(2t+40.6^\circ)$")
    axs[1].legend(fontsize=7, loc="upper right"); axs[1].set_xlabel("t"); axs[1].set_ylim(-4.5, 5.5)
    axs[1].set_title("Outputs")
    save(fig, "23S1_Q3b.png")

    # Q4(b)
    n = np.arange(0, 16)
    y = np.where(n >= 2, 1.8 + 1.2 * (-0.75) ** (n - 2.0), 0)
    fig, ax = plt.subplots(figsize=(7.5, 2.6))
    stems(ax, n, y)
    ax.axhline(1.8, color=GREEN, ls="--", lw=1); ax.text(15.3, 2.6, "steady state 1.8 (dashed)", color=GREEN, ha="right")
    ax.set_xlabel("n"); ax.set_title(r"Q4(b)(ii)  $y[n]=[1.8+1.2(-0.75)^{n-2}]\,u[n-2]$")
    save(fig, "23S1_Q4b_y.png")


# =====================================================================
# 2023-24 Semester 2 (CE3102-23S2)
# =====================================================================
def fig_23s2():
    # Q1(b) redraw from the singularity-function answer (checks the expression)
    r = lambda t: np.maximum(t, 0)
    u = lambda t: (t >= 0) * 1.0
    t = np.linspace(-3, 8, 5001)
    x = r(t + 2) - r(t) - 4 * u(t - 2) + r(t - 2) - r(t - 4) + u(t - 4) + u(t - 6) - 2 * u(t - 7)
    fig, ax = plt.subplots(figsize=(7.5, 2.6))
    ax.plot(t, x, color=BLUE, lw=2)
    ax.set_xticks(range(-3, 9)); ax.set_yticks([-2, -1, 0, 1, 2]); ax.set_xlabel("t")
    ax.set_title("Q1(b)(i) plotted from the singularity-function answer (matches Figure Q1(b))")
    save(fig, "23S2_Q1b_check.png")

    # Q2(b)
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.7))
    t = np.linspace(-1, 9, 2000)
    axs[0].plot(t, np.sin(np.pi * t / 2), color=GREY, lw=1.2, label=r"$x(t)=\sin(\pi t/2)$")
    axs[0].plot(t, -np.cos(np.pi * t / 2), color=BLUE, lw=2, label=r"$y(t)=x(t-1)=-\cos(\pi t/2)$")
    axs[0].legend(fontsize=7, loc="lower right"); axs[0].set_xlabel("t"); axs[0].set_title("(i) delay by 1 s")
    t = np.linspace(0, 7, 2000)
    y = np.where(t < 2, 0, np.where(t < 4, (t - 2) ** 2 / 2, 2 * t - 6))
    axs[1].plot(t, ((t >= 2) & (t < 4)) * 1.0, color=GREY, lw=1.2, label="x(t)")
    axs[1].plot(t, y, color=BLUE, lw=2, label="y(t)")
    for b in [2, 4]: axs[1].axvline(b, color=GREY, ls=":")
    axs[1].legend(fontsize=7); axs[1].set_xlabel("t")
    axs[1].set_title(r"(ii) $0$ | $\frac{(t-2)^2}{2}$ | $2t-6$")
    save(fig, "23S2_Q2b.png")

    # Q2(c)
    f = np.linspace(-9, 9, 6000)  # in units of 1/T, fc = 5/T for the picture
    X = 0.5 * (sinc(f - 5) + sinc(f + 5))
    fig, ax = plt.subplots(figsize=(8, 2.8))
    ax.plot(f, abs(X), color=BLUE, lw=2)
    ax.set_xticks([-6, -5, -4, 0, 4, 5, 6])
    ax.set_xticklabels([r"$-f_c-\frac{1}{T}$", r"$-f_c$", r"$-f_c+\frac{1}{T}$", "0", r"$f_c-\frac{1}{T}$", r"$f_c$", r"$f_c+\frac{1}{T}$"])
    ax.set_yticks([0, 0.5]); ax.set_yticklabels(["0", r"$\frac{AT}{2}$"])
    ax.set_xlabel("f"); ax.set_title(r"Q2(c)  $|X(f)|$: two sinc lobes of height $AT/2$ at $\pm f_c$, null-to-null width $2/T$ (drawn with $f_c=5/T$)")
    save(fig, "23S2_Q2c_spec.png")

    # Q3(b)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.1))
    splane(axs[0], [0], [-1.5], -1.5, lim=(-3, 2, -2, 2), roc_text="ROC: Re(s) > -1.5\nincludes jω-axis → stable")
    axs[0].set_title(r"Q3(b)(i)  $H(s)=\frac{2s}{s+1.5}$")
    t = np.linspace(0, 5, 1000)
    axs[1].plot(t, 3 * np.exp(-1.5 * t), color=BLUE, lw=2, label=r"$3e^{-1.5t}u(t)$")
    impulse(axs[1], 0.02, 2.0, color=RED, text=r"$2\delta(t)$")
    axs[1].set_ylim(0, 3.6); axs[1].legend(fontsize=8); axs[1].set_xlabel("t")
    axs[1].set_title(r"(ii) $y(t)=2\delta(t)+3e^{-1.5t}u(t)$")
    save(fig, "23S2_Q3b.png")

    # Q3(c)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.3))
    splane(axs[0], [], [-1], -1, lim=(-3, 3, -2.5, 2.5), roc_text="ROC Re(s) > -1\ncontains jω-axis\n→ CTFT exists")
    axs[0].plot([0, 0], [-2.5, 2.5], color=ORANGE, lw=3, alpha=0.8)
    axs[0].text(0.1, -1.6, r"on $s=j\omega$: $X(s)\to X(\omega)$", color=ORANGE)
    axs[0].set_title(r"$x(t)=e^{-t}u(t)$:  $X(s)=\frac{1}{s+1}$")
    splane(axs[1], [], [2], 2, lim=(-3, 3, -2.5, 2.5), roc_text="ROC Re(s) > 2\nmisses jω-axis\n→ no CTFT")
    axs[1].plot([0, 0], [-2.5, 2.5], color=ORANGE, lw=3, alpha=0.8)
    axs[1].set_title(r"$x(t)=e^{2t}u(t)$:  $X(s)=\frac{1}{s-2}$")
    save(fig, "23S2_Q3c_splane.png")

    # Q4(a): zero-padding diagram + wrap-around demo
    fig = plt.figure(figsize=(10, 4.3))
    ax = fig.add_axes([0.02, 0.38, 0.96, 0.6]); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 40)
    def bar(x0, y0, wdata, wzero, lab, nd, nz):
        ax.add_patch(Rectangle((x0, y0), wdata, 5, fc=BLUE, alpha=0.6))
        ax.add_patch(Rectangle((x0 + wdata, y0), wzero, 5, fc="white", ec=GREY, hatch="//"))
        ax.text(x0 + wdata / 2, y0 + 2.5, nd, ha="center", va="center", color="white", fontsize=8, weight="bold")
        ax.text(x0 + wdata + wzero / 2, y0 + 2.5, nz, ha="center", va="center", fontsize=8)
        ax.text(x0 - 1, y0 + 2.5, lab, ha="right", va="center", fontsize=9)
    bar(8, 30, 23, 6, "x[n]", "128 samples", "+19 0s")
    bar(8, 18, 4, 25, "h[n]", "20", "127 zeros")
    for y0, lab in [(32.5, "X[k]"), (20.5, "H[k]")]:
        ax.annotate("", xy=(48, y0), xytext=(38, y0), arrowprops=dict(arrowstyle="-|>", lw=1.5))
        ax.text(43, y0 + 1.3, "DFT (N=147)", ha="center", fontsize=8)
        ax.text(49, y0, lab, va="center", fontsize=9)
    ax.add_patch(Circle((60, 26.5), 2.2, fc="white", ec="k")); ax.text(60, 26.5, "×", ha="center", va="center", fontsize=13)
    ax.annotate("", xy=(58, 27.5), xytext=(53, 32), arrowprops=dict(arrowstyle="-|>"))
    ax.annotate("", xy=(58, 25.5), xytext=(53, 21), arrowprops=dict(arrowstyle="-|>"))
    ax.annotate("", xy=(72, 26.5), xytext=(62.3, 26.5), arrowprops=dict(arrowstyle="-|>", lw=1.5))
    ax.text(67, 28, "Y[k]=X[k]H[k]", ha="center", fontsize=8)
    ax.annotate("", xy=(83, 26.5), xytext=(75, 26.5), arrowprops=dict(arrowstyle="-|>", lw=1.5))
    ax.text(73.5, 26.5, "Y", va="center"); ax.text(79, 28, "IDFT", ha="center", fontsize=8)
    ax.add_patch(Rectangle((84, 24), 14, 5, fc=GREEN, alpha=0.6))
    ax.text(91, 26.5, "y[n]: 147", ha="center", va="center", color="white", fontsize=8, weight="bold")
    ax.text(50, 7, "N ≥ Lx + Lh − 1 = 128 + 20 − 1 = 147  (pick N = 256 if a radix-2 FFT is used; samples 147…255 come out 0)",
            ha="center", fontsize=9, color=GREEN, weight="bold")
    # demo: short sequences showing the wrap
    rng = np.random.default_rng(0)
    xs = rng.integers(1, 4, 8).astype(float); hs = np.array([1.0, 1.0, 1.0])
    lin = np.convolve(xs, hs)
    circ8 = np.real(np.fft.ifft(np.fft.fft(xs, 8) * np.fft.fft(hs, 8)))
    circ10 = np.real(np.fft.ifft(np.fft.fft(xs, 10) * np.fft.fft(hs, 10)))
    a1 = fig.add_axes([0.07, 0.07, 0.4, 0.27]); a2 = fig.add_axes([0.56, 0.07, 0.4, 0.27])
    stems(a1, np.arange(10), lin, color=GREY, label="linear x*h"); stems(a1, np.arange(8), circ8, color=RED, label="IDFT(X·H), N=8")
    a1.legend(fontsize=7, loc="upper right"); a1.set_title("Too short (N = Lx): tail wraps onto the start", fontsize=8)
    stems(a2, np.arange(10), lin, color=GREY, label="linear x*h"); stems(a2, np.arange(10), circ10, color=GREEN, label="IDFT(X·H), N=10")
    a2.legend(fontsize=7, loc="upper right"); a2.set_title("Padded (N = Lx+Lh-1 = 10): identical", fontsize=8)
    assert np.allclose(lin, circ10)
    fig.savefig(os.path.join(OUT, "23S2_Q4a_padding.png"), dpi=110); plt.close(fig); print("wrote 23S2_Q4a_padding.png")

    # Q4(c)(i): Direct Form I
    fig, ax = plt.subplots(figsize=(8, 3.4)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 45)
    arr = dict(arrowstyle="-|>", lw=1.4, color="k")
    def box(x, y, txt, w=9, h=6):
        ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="#eef3fb", ec="k")); ax.text(x, y, txt, ha="center", va="center", fontsize=10)
    def summ(x, y):
        ax.add_patch(Circle((x, y), 2.5, fc="white", ec="k")); ax.text(x, y, "+", ha="center", va="center", fontsize=12)
    def gain(x, y, txt, left=False):
        tri = np.array([[x - 3.5, y - 3], [x - 3.5, y + 3], [x + 3.5, y]]) if not left else np.array([[x + 3.5, y - 3], [x + 3.5, y + 3], [x - 3.5, y]])
        ax.add_patch(plt.Polygon(tri, fc="#fff4e5", ec="k")); ax.text(x + (-0.8 if not left else 0.8), y, txt, ha="center", va="center", fontsize=8)
    ax.text(3, 36, "x[n]", va="center", fontsize=11)
    ax.plot([10, 20], [36, 36], "k", lw=1.4); ax.plot(20, 36, "ko", ms=4)
    gain(30, 36, "1"); ax.annotate("", xy=(26.5, 36), xytext=(20, 36), arrowprops=arr)
    summ(45, 36); ax.annotate("", xy=(42.5, 36), xytext=(33.5, 36), arrowprops=arr)
    ax.annotate("", xy=(20, 22.5), xytext=(20, 36), arrowprops=arr); box(20, 19.5, r"$z^{-1}$")
    ax.plot([20, 20], [16.5, 8], "k", lw=1.4); ax.annotate("", xy=(26.5, 8), xytext=(20, 8), arrowprops=arr)
    gain(30, 8, "2"); ax.plot([33.5, 45], [8, 8], "k", lw=1.4); ax.annotate("", xy=(45, 33.5), xytext=(45, 8), arrowprops=arr)
    summ(60, 36); ax.annotate("", xy=(57.5, 36), xytext=(47.5, 36), arrowprops=arr)
    ax.annotate("", xy=(90, 36), xytext=(62.5, 36), arrowprops=arr); ax.text(91, 36, "y[n]", va="center", fontsize=11)
    ax.plot(78, 36, "ko", ms=4)
    ax.annotate("", xy=(78, 22.5), xytext=(78, 36), arrowprops=arr); box(78, 19.5, r"$z^{-1}$")
    ax.plot([78, 78], [16.5, 8], "k", lw=1.4); ax.annotate("", xy=(71.5, 8), xytext=(78, 8), arrowprops=arr)
    gain(68, 8, "0.8", left=True); ax.plot([64.5, 60], [8, 8], "k", lw=1.4); ax.annotate("", xy=(60, 33.5), xytext=(60, 8), arrowprops=arr)
    ax.text(32, 42, "feed-forward (zeros)", ha="center", color=BLUE, fontsize=8)
    ax.text(70, 42, "feedback (poles)", ha="center", color=RED, fontsize=8)
    ax.text(50, 1, r"$y[n]=x[n]+2x[n-1]+0.8\,y[n-1]$", ha="center", fontsize=10)
    fig.savefig(os.path.join(OUT, "23S2_Q4c_df1.png"), dpi=110, bbox_inches="tight"); plt.close(fig); print("wrote 23S2_Q4c_df1.png")

    n = np.arange(0, 11)
    y = np.where(n == 0, 2.0, 7 * 0.8 ** n)
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    stems(ax, n, y); ax.set_xlabel("n")
    for i in range(5): ax.text(i, y[i] + 0.25, f"{y[i]:.4g}", ha="center", fontsize=8)
    ax.set_ylim(0, 6.5); ax.set_title(r"Q4(c)(ii)  $y[n]=-5\delta[n]+7(0.8)^n u[n]$")
    save(fig, "23S2_Q4c_y.png")


# =====================================================================
# 2024-25 Semester 1 (CE3102-24S1)
# =====================================================================
def fig_24s1():
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.7))
    lines(axs[0], [-3, 3, 5], [2.5, 2.5, 8]); axs[0].set_ylim(0, 9.5); axs[0].set_title("Amplitude"); axs[0].set_xlabel("f (Hz)")
    lines(axs[1], [-3, 3, 5], [90, -90, 120], color=RED, fmt="{:+g}°", yoff=8); axs[1].set_ylim(-130, 160)
    axs[1].set_title("Phase (degrees)"); axs[1].set_xlabel("f (Hz)")
    save(fig, "24S1_Q1a_spectra.png")

    t = np.linspace(-1, 9, 3000)
    r = lambda t: np.maximum(t, 0); u = lambda t: (t >= 0) * 1.0
    x = 3 * u(t) - r(t - 2) + r(t - 3) + u(t - 4)
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    ax.plot(t, x, color=BLUE, lw=2); ax.set_xticks(range(-1, 10)); ax.set_ylim(-0.3, 3.6)
    ax.text(6.5, 3.1, "stays at 3 for all t ≥ 4 → power signal", color=RED)
    ax.set_xlabel("t"); ax.set_title(r"Q1(b)  $x(t)=3u(t)-r(t-2)+r(t-3)+u(t-4)$")
    save(fig, "24S1_Q1b_x.png")

    t = np.linspace(0, 10, 3000)
    y = np.exp(-(t - 2)) * (t >= 2) - np.exp(-(t - 4)) * (t >= 4)
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    ax.plot(t, y, color=BLUE, lw=2); ax.set_xlabel("t")
    ax.set_title(r"Q1(c)  $y(t)=e^{-(t-2)}u(t-2)-e^{-(t-4)}u(t-4)$")
    save(fig, "24S1_Q1c_y.png")

    t = np.linspace(-5, 9, 3000)
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.6))
    axs[0].plot(t, ((t >= 0) & (t <= 4)) * 1.0, color=BLUE, lw=2); axs[0].set_title(r"$x(t)=\Pi\left(\frac{t-2}{4}\right)$"); axs[0].set_xlabel("t")
    y = 2 * ((t >= 3) & (t <= 7)) - ((t >= -3) & (t <= 1))
    axs[1].plot(t, y, color=BLUE, lw=2); axs[1].set_xlabel("t")
    axs[1].set_title(r"$y(t)=2x(t-3)-x(t+3)$: non-zero before the input starts")
    save(fig, "24S1_Q2a_y.png")

    fig, axs = plt.subplots(1, 2, figsize=(10, 2.7))
    f = np.linspace(-0.6, 0.6, 3000)
    axs[0].plot(f, np.pi * (abs(f) < 1 / np.pi), color=GREY, lw=1.5, label=r"$G_1(f)=\pi\,\Pi(\pi f/2)$, $|f|<1/\pi$")
    axs[0].plot(f, np.pi * (abs(f) < 1 / (2 * np.pi)), color=ORANGE, lw=1.5, label=r"$G_2(f)=\pi\,\Pi(\pi f)$, $|f|<1/2\pi$")
    axs[0].plot(f, np.pi ** 2 * (abs(f) < 1 / (2 * np.pi)), color=BLUE, lw=2, label=r"$G_1G_2=\pi^2\,\Pi(\pi f)$")
    axs[0].legend(fontsize=7); axs[0].set_xlabel("f"); axs[0].set_title("Multiply in frequency")
    tt = np.linspace(-20, 20, 4000)
    axs[1].plot(tt, np.pi * np.sinc(tt / np.pi), color=BLUE, lw=2); axs[1].set_xlabel("t")
    axs[1].set_title(r"Result $=\pi\,\frac{\sin t}{t}$ (value $\pi$ at $t=0$)")
    save(fig, "24S1_Q2b_conv.png")

    t = np.linspace(0, 6, 1000)
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    ax.plot(t, 10 / 3 - 2 * np.exp(-t) - 4 / 3 * np.exp(-3 * t), color=BLUE, lw=2)
    ax.axhline(10 / 3, color=GREEN, ls="--"); ax.text(6, 3.45, "H(0) = 10/3", ha="right", color=GREEN)
    ax.set_xlabel("t"); ax.set_title(r"Q3(b)(i) step response $\frac{10}{3}-2e^{-t}-\frac{4}{3}e^{-3t}$")
    save(fig, "24S1_Q3b_step.png")

    fig, axs = plt.subplots(2, 2, figsize=(10, 7))
    pz = [-0.5, -0.5 - 0.5j, -0.5 + 0.5j]
    splane(axs[0, 0], [2], pz, -0.5, lim=(-2, 2.6, -1.5, 1.5), roc_text="ROC: Re(s) > -0.5\ncontains jω-axis → stable")
    axs[0, 0].set_title("s-domain H(s)")
    zplane(axs[0, 1], [2], pz, abs(pz[1]), lim=2.3, roc_text="ROC: |z| > 0.707\ncontains unit circle → stable")
    axs[0, 1].set_title("z-domain H(z)")
    w = np.linspace(0, 10, 2000); s = 1j * w
    Hs = (s - 2) / ((s + 0.5) * (s + 0.5 + 0.5j) * (s + 0.5 - 0.5j))
    axs[1, 0].plot(w, abs(Hs), color=BLUE, lw=2); axs[1, 0].set_xlabel(r"$\omega$ (rad/s)")
    axs[1, 0].set_title(r"$|H(j\omega)|$: 8 at DC, falls like $1/\omega^2$ → low-pass")
    W = np.linspace(-np.pi, np.pi, 2001); z = np.exp(1j * W)
    Hz = (z - 2) / ((z + 0.5) * (z + 0.5 + 0.5j) * (z + 0.5 - 0.5j))
    axs[1, 1].plot(W, abs(Hz), color=BLUE, lw=2); axs[1, 1].set_xlabel(r"$\Omega$ (rad/sample)")
    axs[1, 1].set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi]); axs[1, 1].set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    axs[1, 1].set_title(r"$|H(e^{j\Omega})|$: 0.27 at $\Omega=0$, 12 at $\Omega=\pi$ → high-pass")
    save(fig, "24S1_Q4a.png")

    n = np.arange(0, 11); y = 8 - 6 * 0.5 ** n
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    stems(ax, n, y); ax.axhline(8, color=GREEN, ls="--"); ax.set_ylim(0, 9.5)
    for i in range(6): ax.text(i, y[i] + 0.3, f"{y[i]:g}", ha="center", fontsize=8)
    ax.set_xlabel("n"); ax.set_title(r"Q4(b)  $y[n]=[8-6(1/2)^n]u[n]$")
    save(fig, "24S1_Q4b_y.png")


# =====================================================================
# 2025-26 Semester 1 (CE3102-25S1)
# =====================================================================
def fig_25s1():
    t = np.linspace(-6, 10, 6000)
    p = lambda t: ((t >= -1) & (t < 1)) * np.exp(-abs(t))
    fig, ax = plt.subplots(figsize=(9, 2.7))
    x = sum(p(t - 4 * n) for n in range(-3, 4))
    ax.plot(t, x, color=GREY, lw=1, label="x(t)")
    ax.fill_between(t, 0, p(t), color=BLUE, alpha=0.35, label="term n = 0: pulse on [-1, 1)")
    ax.fill_between(t, 0, p(t - 4), color=ORANGE, alpha=0.35, label="term n = 1: pulse on [3, 5)")
    for c in [-4, 0, 4, 8]: ax.text(c, 1.05, "1", ha="center", fontsize=8)
    ax.text(1.05, np.exp(-1) + 0.05, r"$e^{-1}=0.368$", fontsize=8)
    ax.set_xticks(range(-6, 11)); ax.set_ylim(0, 1.55); ax.set_xlabel("t"); ax.legend(fontsize=7, loc="upper center", ncol=3)
    ax.set_title(r"Q1(a)(ii)  $\alpha=1$: pulses never overlap (width 2 < period 4)")
    save(fig, "25S1_Q1a_x.png")

    fig, axs = plt.subplots(1, 3, figsize=(11, 2.7))
    t = np.linspace(-1, 6, 2000)
    for ax in axs: ax.axhline(0, color="k", lw=0.8); ax.set_xlabel("t")
    axs[0].plot(t, ((t >= 2) & (t <= 4)) * 1.0, color=BLUE, lw=2); impulse(axs[0], 1, 2, text=r"$2\delta(t-1)$")
    axs[0].set_ylim(-0.2, 2.6); axs[0].set_title("given step response s(t)")
    t2 = np.linspace(2, 14, 3000)
    axs[1].plot(t2, 3 * ((t2 >= 4) & (t2 <= 8)), color=BLUE, lw=2); axs[1].set_ylim(-0.2, 3.6); axs[1].set_title(r"$x(t)=3\Pi\left(\frac{t-6}{4}\right)=3[u(t-4)-u(t-8)]$")
    y = 3 * ((t2 >= 6) & (t2 <= 8)) - 3 * ((t2 >= 10) & (t2 <= 12))
    axs[2].plot(t2, y, color=BLUE, lw=2); impulse(axs[2], 5, 6, text=r"$6\delta(t-5)$", dy=0.3); impulse(axs[2], 9, -6, color=RED, text=r"$-6\delta(t-9)$", dy=0.3)
    axs[2].set_ylim(-7.5, 7.5); axs[2].set_title("y(t) = 3s(t-4) - 3s(t-8)")
    save(fig, "25S1_Q2a.png")

    tri = lambda t: np.where((t >= 0) & (t < 1), t, np.where((t >= 1) & (t < 2), 2 - t, 0))
    t = np.linspace(-0.5, 12, 4000)
    fig, axs = plt.subplots(1, 3, figsize=(11, 2.6))
    axs[0].plot(t, tri(t), color=BLUE, lw=2); axs[0].set_title("x(t)"); axs[0].set_xlim(-0.5, 3)
    for t0, a, c in [(2, 1, BLUE), (5, -1, RED), (9, 1, BLUE)]: impulse(axs[1], t0, a, color=c, text=f"{a:+d}", dy=0.08)
    axs[1].set_xlim(-0.5, 12); axs[1].set_ylim(-1.4, 1.4); axs[1].axhline(0, color="k", lw=0.8); axs[1].set_title("h(t)")
    axs[2].plot(t, tri(t - 2) - tri(t - 5) + tri(t - 9), color=BLUE, lw=2); axs[2].set_ylim(-1.3, 1.3); axs[2].axhline(0, color="k", lw=0.8)
    axs[2].set_title("y(t) = x(t-2) - x(t-5) + x(t-9)")
    for a in axs: a.set_xlabel("t")
    save(fig, "25S1_Q2b.png")

    t = np.linspace(0, 10, 3000)
    a = np.exp(-(t - 3)) * (t >= 3); b = (np.exp(-(t - 2)) - np.exp(-2 * (t - 2))) * (t >= 2)
    fig, ax = plt.subplots(figsize=(8, 2.7))
    ax.plot(t, a, "--", color=ORANGE, label=r"$e^{-(t-3)}u(t-3)$ (via $\delta(t-1)$)")
    ax.plot(t, b, "--", color=GREEN, label=r"$[e^{-(t-2)}-e^{-2(t-2)}]u(t-2)$ (via $e^{-2t}u(t)$)")
    ax.plot(t, a + b, color=BLUE, lw=2, label="y(t)"); ax.legend(fontsize=7); ax.set_xlabel("t")
    ax.set_title("Q2(c)(ii) received signal")
    save(fig, "25S1_Q2c_y.png")

    t = np.linspace(0, 2.5, 500)
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    ax.plot(t, 1 + (1 - t) * np.exp(t), color=BLUE, lw=2); ax.set_xlabel("t")
    ax.set_title(r"Q3(c)(i)  $y(t)=1+(1-t)e^{t}$: double pole at s = +1 → blows up")
    save(fig, "25S1_Q3c_y.png")

    fig, axs = plt.subplots(1, 2, figsize=(10, 3.2))
    zplane(axs[0], [-0.5], [0.1], 0.1, lim=1.4, roc_text="ROC: |z| > 0.1\ncontains unit circle")
    axs[0].set_title(r"Q4(a)(ii)  $H(z)=\frac{z+0.5}{z-0.1}$")
    n = np.arange(0, 12)
    y = 6 / 11 * 0.1 ** n + 5 / 11 * (-1.0) ** n
    stems(axs[1], n, y, label="y[n] (full)")
    axs[1].plot(n, 5 / 11 * (-1.0) ** n, "s", mfc="none", color=GREEN, ms=7, label=r"steady state $\frac{5}{11}(-1)^n$")
    axs[1].legend(fontsize=7, loc="upper right"); axs[1].set_xlabel("n"); axs[1].set_ylim(-0.7, 1.25)
    axs[1].set_title(r"(iv) input $\cos(\pi n)u[n]$")
    save(fig, "25S1_Q4a.png")


# =====================================================================
# 2025-26 Semester 2 (SC3102-25S2)
# =====================================================================
def fig_25s2():
    t = np.linspace(-2, 5, 4000)
    r = lambda t: np.maximum(t, 0); u = lambda t: (t >= 0) * 1.0
    x = r(t) - r(t - 1) + u(t - 2) - r(t) * u(t - 3)
    fig, ax = plt.subplots(figsize=(7.5, 2.7))
    ax.plot(t, x, color=BLUE, lw=2); ax.set_xticks(range(-2, 6)); ax.set_yticks([-3, -2, -1, 0, 1, 2])
    ax.text(4.9, -2.4, "keeps falling as 2 - t", ha="right", color=RED); ax.set_xlabel("t")
    ax.set_title(r"Q1(a)(i)  $x(t)=r(t)-r(t-1)+u(t-2)-r(t)u(t-3)$")
    save(fig, "25S2_Q1a_x.png")

    f = [-150, -120, -50, 0, 50, 120, 150]
    fig, axs = plt.subplots(1, 2, figsize=(11, 2.8))
    lines(axs[0], f, [3, 2, 3, 4, 3, 2, 3]); axs[0].set_ylim(0, 5); axs[0].set_title("Amplitude $|c_k|$"); axs[0].set_xlabel("f (Hz)")
    lines(axs[1], f, [90, -90, -90, 0, 90, 90, -90], color=RED, fmt="{:+g}°", yoff=8); axs[1].set_ylim(-125, 125)
    axs[1].set_title("Phase (degrees)"); axs[1].set_xlabel("f (Hz)")
    save(fig, "25S2_Q1b_spectra.png")

    t = np.linspace(0, 6, 1000)
    fig, ax = plt.subplots(figsize=(7.5, 2.6))
    ax.plot(t, np.exp(-t), "--", color=GREY, label=r"$x(t)=e^{-t}u(t)$")
    ax.plot(t, np.exp(-2 * t), ":", color=GREY, label=r"$h(t)=e^{-2t}u(t)$")
    ax.plot(t, np.exp(-t) - np.exp(-2 * t), color=BLUE, lw=2, label=r"$y(t)=e^{-t}-e^{-2t}$ (peak 1/4 at $t=\ln 2$)")
    ax.legend(fontsize=7); ax.set_xlabel("t"); ax.set_title("Q2(b)")
    save(fig, "25S2_Q2b_y.png")

    xn = np.array([0.25, -0.75, -0.75, -2.75])
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.7))
    stems(axs[0], np.arange(8), np.tile(xn, 2)); axs[0].set_xlabel("n"); axs[0].set_title("x[n]: two periods (input to the 8-point DFT)")
    X8 = np.fft.fft(np.tile(xn, 2))
    stems(axs[1], np.arange(8), abs(X8), color=GREEN)
    for k in range(8): axs[1].text(k, abs(X8[k]) + 0.3, f"{X8[k].real:+.0f}{X8[k].imag:+.0f}j" if abs(X8[k]) > 1e-9 else "0", ha="center", fontsize=7)
    axs[1].set_ylim(0, 10); axs[1].set_xlabel("k"); axs[1].set_title("|X8[k]|: odd bins 0, even bins = 2·X4[k/2]")
    save(fig, "25S2_Q3a.png")

    k = np.arange(20); mag = np.zeros(20); mag[[0, 1, 2, 18]] = [2, 3, 2, 2]
    fig, ax = plt.subplots(figsize=(8, 2.5))
    stems(ax, k, mag); ax.set_xticks(k); ax.set_xlabel("k   (Ω = 2πk/20 = kπ/10)")
    for kk, lab in [(0, "2"), (1, "3"), (2, "2"), (18, "2")]: ax.text(kk, mag[kk] + 0.15, lab, ha="center", fontsize=8)
    ax.set_ylim(0, 3.7); ax.set_title(r"Q3(b) line spectrum $|a_k|$, N = 20 (course DTFS $X[k]=20a_k$ → 40, 60, 40, 40)")
    save(fig, "25S2_Q3b_lines.png")

    n = np.arange(0, 24)
    Hw = lambda W: (-1 + 0.5 * np.exp(-1j * W)) / (1 - 0.1 * np.exp(-1j * W))
    x = 1 + 2 * np.cos(np.pi * n / 4 + np.pi / 3)
    yss = Hw(0).real + 2 * abs(Hw(np.pi / 4)) * np.cos(np.pi * n / 4 + np.pi / 3 + np.angle(Hw(np.pi / 4)))
    fig, ax = plt.subplots(figsize=(8, 2.7))
    stems(ax, n, x, color=GREY, label="x[n]"); stems(ax, n + 0.2, yss, color=BLUE, label=r"$y_{ss}[n]$")
    ax.set_ylim(-2.6, 4.2); ax.legend(fontsize=7, loc="upper center", ncol=2); ax.set_xlabel("n")
    ax.set_title(r"Q3(c)  $y_{ss}[n]=-\frac{5}{9}+1.581\cos(\frac{\pi}{4}n-95.7^\circ)$")
    save(fig, "25S2_Q3c_y.png")

    # Q4(a): geometric evaluation picture with example numbers
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    ax = axs[0]; a, b = 2.0, 0.5
    splane(ax, [-a], [-b], -b, lim=(-3, 1.5, -2, 2.5), roc_text="causal ROC: Re(s) > -b\nstable ⇔ b > 0")
    wpt = 1.6
    ax.plot([0], [wpt], "o", color=ORANGE)
    ax.annotate("", xy=(0, wpt), xytext=(-a, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE))
    ax.annotate("", xy=(0, wpt), xytext=(-b, 0), arrowprops=dict(arrowstyle="-|>", color=RED))
    ax.text(0.08, wpt + 0.12, r"$j\omega$", color=ORANGE)
    ax.set_title(r"s-plane: $|H(j\omega)|=\frac{|j\omega+a|}{|j\omega+b|}$  (example a=2, b=0.5)", fontsize=9)
    ax = axs[1]; a, b = 0.9, -0.6
    zplane(ax, [-a], [-b], abs(b), lim=1.5, roc_text="causal ROC: |z| > |b|\nstable ⇔ |b| < 1")
    W = 1.1; zp = np.exp(1j * W)
    ax.plot([zp.real], [zp.imag], "o", color=ORANGE)
    ax.annotate("", xy=(zp.real, zp.imag), xytext=(-a, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE))
    ax.annotate("", xy=(zp.real, zp.imag), xytext=(-b, 0), arrowprops=dict(arrowstyle="-|>", color=RED))
    ax.text(zp.real + 0.05, zp.imag + 0.08, r"$e^{j\Omega}$", color=ORANGE)
    ax.set_title(r"z-plane: $|H(e^{j\Omega})|=\frac{|e^{j\Omega}+a|}{|e^{j\Omega}+b|}$  (example a=0.9, b=-0.6)", fontsize=9)
    save(fig, "25S2_Q4a.png")

    t = np.linspace(0, 4, 1000)
    fig, axs = plt.subplots(1, 2, figsize=(10, 2.6))
    axs[0].plot(t, -23 / 24 - np.exp(-2 * t) / 24, color=BLUE, lw=2)
    axs[0].axhline(-23 / 24, color=GREEN, ls="--"); axs[0].text(4, -0.9595, "final value -23/24", ha="right", va="bottom", color=GREEN)
    axs[0].set_title(r"(i) $y(0)=-1$: $y=-\frac{23}{24}-\frac{1}{24}e^{-2t}$"); axs[0].set_xlabel("t")
    axs[1].plot(t, 2 + (1 - np.exp(-2 * t)) / 24, color=ORANGE, lw=2)
    axs[1].axhline(49 / 24, color=GREEN, ls="--"); axs[1].text(4, 2.0405, "final value 49/24 (FVT)", ha="right", va="top", color=GREEN)
    axs[1].set_title(r"(ii) $y(0)=2$: $y=2+\frac{1}{24}(1-e^{-2t})$"); axs[1].set_xlabel("t")
    save(fig, "25S2_Q4b_y.png")


if __name__ == "__main__":
    fig_23s1(); fig_23s2(); fig_24s1(); fig_25s1(); fig_25s2()
