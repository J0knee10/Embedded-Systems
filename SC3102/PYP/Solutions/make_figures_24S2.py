"""Draws every figure used in SC3102-24S2_Solutions.md (prefix 24S2_).

Run:  python make_figures_24S2.py      (writes PNGs into ./figs)
Same house style as make_figures.py (which is left untouched). Every figure is
computed from the formula derived in the solution, and the asserts below
re-check each numerical answer by brute force (numerical integration,
np.convolve, inverse FFT, running the difference equation, an ODE solver),
so a slip in the algebra stops the script.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from scipy import integrate

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


def impulse(ax, t0, area, color=BLUE, text=None, dy=0.15, fs=8):
    ax.annotate("", xy=(t0, area), xytext=(t0, 0),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=color, shrinkA=0, shrinkB=0))
    if text is not None:
        ax.text(t0, area + (dy if area >= 0 else -dy), text, ha="center",
                va="bottom" if area >= 0 else "top", color="k", fontsize=fs)


def stems(ax, n, v, color=BLUE, label=None, ms=4):
    ax.vlines(n, 0, v, color=color, lw=1.5)
    ax.plot(n, v, "o", color=color, ms=ms, label=label)
    ax.axhline(0, color="k", lw=0.8)


def splane(ax, zeros, poles, roc_from, lim=(-3, 3, -2.5, 2.5), roc_text=None, legend=True):
    x0, x1, y0, y1 = lim
    ax.axvspan(roc_from, x1, color=GREEN, alpha=0.13)
    ax.axvline(roc_from, color=GREEN, ls="--", lw=1)
    axes0(ax)
    ax.plot([0, 0], [y0, y1], color="k", lw=2)  # the j-omega axis, drawn bold
    ax.plot(np.real(poles), np.imag(poles), "x", color=RED, ms=10, mew=2.5, label="pole")
    if len(zeros):
        ax.plot(np.real(zeros), np.imag(zeros), "o", mfc="none", mec=BLUE, ms=10, mew=2, label="zero")
    ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_xlabel(r"$\sigma=\mathrm{Re}(s)$"); ax.set_ylabel(r"$\omega=\mathrm{Im}(s)$")
    ax.text(0.98, 0.95, roc_text or "ROC", transform=ax.transAxes, ha="right", va="top",
            color="k", fontsize=8, bbox=dict(fc="white", ec=GREEN, alpha=0.9))
    if legend:
        ax.legend(loc="lower left", fontsize=7)


def zplane(ax, zeros, poles, r_roc, lim=1.6, roc_text=None, legend=True, zero_label="zero"):
    ax.add_patch(Rectangle((-lim, -lim), 2 * lim, 2 * lim, color=GREEN, alpha=0.13, zorder=0))
    ax.add_patch(Circle((0, 0), r_roc, color="white", zorder=1))
    ax.add_patch(Circle((0, 0), r_roc, fill=False, ec=GREEN, ls="--", zorder=2))
    ax.add_patch(Circle((0, 0), 1, fill=False, ec="k", lw=1.8, zorder=2))
    axes0(ax)
    ax.plot(np.real(poles), np.imag(poles), "x", color=RED, ms=10, mew=2.5, label="pole", zorder=3)
    if len(zeros):
        ax.plot(np.real(zeros), np.imag(zeros), "o", mfc="none", mec=BLUE, ms=10, mew=2, label=zero_label, zorder=3)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
    ax.set_xlabel("Re(z)"); ax.set_ylabel("Im(z)")
    ax.text(0.98, 0.97, roc_text or "ROC", transform=ax.transAxes, ha="right", va="top",
            color="k", fontsize=8, bbox=dict(fc="white", ec=GREEN, alpha=0.9), zorder=4)
    if legend:
        ax.legend(loc="lower left", fontsize=7)


u = lambda t: (np.asarray(t, float) >= 0) * 1.0
r = lambda t: np.maximum(np.asarray(t, float), 0)
PI_TICKS = ([-2 * np.pi, -4 * np.pi / 3, -np.pi, -2 * np.pi / 3, 0, 2 * np.pi / 3, np.pi, 4 * np.pi / 3, 2 * np.pi],
            [r"$-2\pi$", r"$-\frac{4\pi}{3}$", r"$-\pi$", r"$-\frac{2\pi}{3}$", "0", r"$\frac{2\pi}{3}$", r"$\pi$",
             r"$\frac{4\pi}{3}$", r"$2\pi$"])


# =====================================================================
# Question 1
# =====================================================================
def fig_q1():
    # ---- Q1(a): the boxed singularity expression, checked against the figure
    def x_expr(t):
        return (u(t - 1) + u(t - 2) + u(t - 3) + r(t - 3) - 2 * u(t - 4) - r(t - 4)
                - r(t - 7) + r(t - 8) - u(t - 9))

    def x_fig(t):
        t = np.asarray(t, float); out = np.zeros_like(t)
        out[(t >= 1) & (t < 2)] = 1
        out[(t >= 2) & (t < 3)] = 2
        m = (t >= 3) & (t < 4); out[m] = t[m]
        out[(t >= 4) & (t < 7)] = 2
        m = (t >= 7) & (t < 8); out[m] = 9 - t[m]
        out[(t >= 8) & (t < 9)] = 1
        return out

    t = np.linspace(-0.5, 10.5, 22001)
    assert np.max(abs(x_expr(t) - x_fig(t))) < 1e-12
    fig, ax = plt.subplots(figsize=(9, 3.4))
    # draw piece by piece so the jumps are vertical lines
    ax.plot(t, x_expr(t), color=BLUE, lw=2)
    for tj, (a, b) in {1: (0, 1), 2: (1, 2), 3: (2, 3), 4: (4, 2), 9: (1, 0)}.items():
        ax.plot([tj, tj], [a, b], color=BLUE, lw=2)
    jumps = [(1, 0.5, "+1·u(t-1)"), (2, 1.5, "+1·u(t-2)"), (3, 2.5, "+1·u(t-3)"),
             (4, 3.0, "-2·u(t-4)"), (9, 0.5, "-1·u(t-9)")]
    for tj, yj, lab in jumps:
        ax.text(tj + 0.08, yj, lab, fontsize=7.5, color=RED, va="center")
    bends = [(3, 3, "slope 0→1: +r(t-3)", (1.0, 4.4)), (4, 4, "slope 1→0: -r(t-4)", (4.4, 4.4)),
             (7, 2, "slope 0→-1: -r(t-7)", (6.3, 3.0)), (8, 1, "slope -1→0: +r(t-8)", (7.6, 0.25))]
    for tb, yb, lab, (tx, ty) in bends:
        ax.plot(tb, yb, "o", color=GREEN, ms=5)
        ax.annotate(lab, xy=(tb, yb), xytext=(tx, ty), fontsize=7.5, color=GREEN,
                    arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.8))
    ax.set_xticks(range(0, 11)); ax.set_yticks(range(-1, 6)); ax.set_ylim(-0.5, 5); ax.set_xlim(-0.3, 10.3)
    ax.set_xlabel("t"); ax.set_ylabel("x(t)")
    ax.set_title("Q1(a)  plotted from the boxed expression: jumps (red) are steps, bends (green) are ramps")
    save(fig, "24S2_Q1a_x.png")

    # ---- Q1(b): the damped cosine, its energy, and why it is not periodic
    x = lambda t: np.exp(-2 * t) * np.cos(5 * np.pi * t) * (np.asarray(t) >= 0)
    E_exact = 1 / 8 + 1 / (8 + 50 * np.pi ** 2)
    E_num, _ = integrate.quad(lambda t: x(t) ** 2, 0, 20, limit=2000)
    assert abs(E_num - E_exact) < 1e-9 and abs(E_exact - 0.126994) < 1e-6
    assert abs(x(0.4) - np.exp(-0.8)) < 1e-12
    val = 0.5 * np.exp(-2) * np.cos(5 * np.pi)        # Q1(b)(iii)
    assert abs(val + np.exp(-2) / 2) < 1e-15

    fig, axs = plt.subplots(1, 2, figsize=(11, 3.2))
    ax = axs[0]
    tt = np.linspace(-0.4, 2.0, 4000)
    ax.plot(tt, x(tt), color=BLUE, lw=2, label=r"$x(t)=e^{-2t}\cos(5\pi t)u(t)$")
    te = np.linspace(0, 2.0, 500)
    ax.plot(te, np.exp(-2 * te), "--", color=GREY, lw=1, label=r"envelope $\pm e^{-2t}$")
    ax.plot(te, -np.exp(-2 * te), "--", color=GREY, lw=1)
    pk = np.array([0, 0.4, 0.8, 1.2])
    ax.plot(pk, x(pk), "o", color=ORANGE, ms=6, label="one period (0.4 s) apart")
    for p in pk:
        ax.text(p + 0.03, x(p) + 0.05, f"{x(p):.3f}", fontsize=7.5)
    ax.plot([1.0], [x(1.0)], "s", color=RED, ms=6, label=r"(iii) $x(1)=-e^{-2}=-0.135$")
    ax.set_xlabel("t (s)"); ax.set_ylim(-1.05, 1.25); ax.legend(fontsize=7, loc="upper right")
    ax.set_title("(ii) each 0.4 s the peak shrinks ×0.449, so it never repeats")
    ax = axs[1]
    Tw = np.linspace(0.01, 3, 600)
    Ecum = np.array([integrate.quad(lambda s: x(s) ** 2, 0, L, limit=400)[0] for L in Tw])
    ax.plot(Tw, Ecum, color=BLUE, lw=2, label=r"energy collected up to time $L$")
    ax.axhline(E_exact, color=GREEN, ls="--")
    ax.text(3, E_exact + 0.003, f"E = 1/8 + 1/(8+50π²) = {E_exact:.4f}", ha="right", va="bottom", fontsize=8)
    ax.set_xlabel("L (s)"); ax.set_ylim(0, 0.15); ax.legend(fontsize=7, loc="lower right")
    ax.set_title("(i) energy levels off at 0.127, so it is an energy signal (P = 0)")
    save(fig, "24S2_Q1b_x.png")


# =====================================================================
# Question 2
# =====================================================================
def fig_q2():
    xn = np.array([1, 2, 3, 2, 1]); hn = np.array([1, -1, 1])
    y = np.convolve(xn, hn)
    assert list(y) == [1, 1, 2, 1, 2, 1, 1]

    # ---- Q2(b): flip-and-slide panels
    m = np.arange(-3, 9)
    xm = np.array([xn[k] if 0 <= k < 5 else 0 for k in m])
    fig, axs = plt.subplots(2, 4, figsize=(13, 5.6), sharey=True)
    axs = axs.ravel()
    ax = axs[0]
    stems(ax, m - 0.1, xm, color=BLUE, label=r"$x[m]$ (stays put)")
    hflip = np.array([hn[-k] if 0 <= -k < 3 else 0 for k in m])
    stems(ax, m + 0.1, hflip, color=ORANGE, label=r"$h[-m]$ (flipped)")
    ax.set_title("step 1: flip h  (h[-m] sits on m = -2, -1, 0)", fontsize=9)
    ax.legend(fontsize=7, loc="upper right")
    for n in range(7):
        ax = axs[n + 1]
        hs = np.array([hn[n - k] if 0 <= n - k < 3 else 0 for k in m])
        stems(ax, m - 0.1, xm, color=BLUE)
        stems(ax, m + 0.1, hs, color=ORANGE)
        prods = [(k, xn[k], hn[n - k]) for k in range(5) if 0 <= n - k < 3]
        expr = " + ".join(f"{a}·({b})" if b < 0 else f"{a}·{b}" for _, a, b in prods)
        ax.set_title(f"n = {n}:  {expr} = {y[n]}", fontsize=8.5)
        ax.axvspan(n - 2 - 0.4, n + 0.4, color=ORANGE, alpha=0.08)
    for ax in axs:
        ax.set_xticks(range(-3, 9)); ax.set_ylim(-1.6, 3.8); ax.set_xlabel("m")
    fig.suptitle(r"Q2(b) graphical convolution: $y[n]=\sum_m x[m]\,h[n-m]$; blue $x[m]$, orange $h[n-m]$ "
                 r"(the flipped $h$ slid right by $n$); shaded = overlap", fontsize=10)
    save(fig, "24S2_Q2b_slide.png")

    # ---- Q2(b): output
    fig, ax = plt.subplots(figsize=(7.5, 2.8))
    n = np.arange(-2, 9)
    yy = np.array([y[k] if 0 <= k < 7 else 0 for k in n])
    stems(ax, n, yy, color=BLUE)
    for k in range(7):
        ax.text(k, y[k] + 0.12, str(y[k]), ha="center", fontsize=9)
    ax.set_xticks(n); ax.set_ylim(-0.3, 2.7); ax.set_xlabel("n"); ax.set_ylabel("y[n]")
    ax.set_title(r"Q2(b)  $y[n]=x[n]*h[n]=\{1,1,2,1,2,1,1\}$ for $n=0..6$, zero elsewhere")
    save(fig, "24S2_Q2b_y.png")

    # ---- Q2(c): two echoes in time = a cosine factor in frequency (t0 = 1 as an example)
    t0 = 1.0
    X = lambda f: 1 / (1 + 2j * np.pi * f)
    Y = lambda f: 2 * np.cos(2 * np.pi * f * t0) * X(f)
    yfun = lambda t: np.exp(-(t - t0)) * (t >= t0) + np.exp(-(t + t0)) * (t >= -t0)
    for f in [0.1, 0.3, 0.5]:
        re = integrate.quad(lambda t: yfun(t) * np.cos(2 * np.pi * f * t), -t0, 60, points=[t0], limit=4000)[0]
        im = integrate.quad(lambda t: -yfun(t) * np.sin(2 * np.pi * f * t), -t0, 60, points=[t0], limit=4000)[0]
        assert abs(re + 1j * im - Y(f)) < 1e-7
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.0))
    t = np.linspace(-2.5, 5, 3000)
    axs[0].plot(t, np.exp(-t) * (t >= 0), "--", color=GREY, label=r"$x(t)=e^{-t}u(t)$")
    axs[0].plot(t, yfun(t), color=BLUE, lw=2, label=r"$y(t)=x(t-1)+x(t+1)$")
    axs[0].legend(fontsize=7); axs[0].set_xlabel("t"); axs[0].set_title(r"time: two copies, $t_0=1$ either side")
    f = np.linspace(-1.2, 1.2, 4000)
    axs[1].plot(f, 2 * abs(X(f)), "--", color=GREY, label=r"$2|X(f)|$ (envelope)")
    axs[1].plot(f, abs(Y(f)), color=BLUE, lw=2, label=r"$|Y(f)|=2|\cos(2\pi f t_0)|\,|X(f)|$")
    for fz in [-0.75, -0.25, 0.25, 0.75]:
        axs[1].plot(fz, 0, "o", color=RED, ms=4)
    axs[1].text(-1.18, 1.75, "red dots: zeros at f = ±1/4, ±3/4 Hz\n(f = odd number / (4t₀))", fontsize=7.5, color="k")
    axs[1].legend(fontsize=7, loc="upper right"); axs[1].set_xlabel("f (Hz)")
    axs[1].set_title(r"frequency: $|Y(0)|=2$ = area of $y$")
    save(fig, "24S2_Q2c.png")


# =====================================================================
# Question 3
# =====================================================================
def fig_q3():
    Xk = np.array([18, 0, 12 + 10j, 0, 12 - 10j, 0])
    x6 = np.fft.ifft(Xk)
    n6 = np.arange(6)
    formula = 3 + 4 * np.cos(2 * np.pi * n6 / 3) - (10 / 3) * np.sin(2 * np.pi * n6 / 3)
    assert np.max(abs(x6 - formula)) < 1e-12
    assert abs(formula[1] - (1 - 5 / np.sqrt(3))) < 1e-12 and abs(formula[2] - (1 + 5 / np.sqrt(3))) < 1e-12
    R = np.sqrt(244) / 3; phi = np.degrees(np.arctan2(10, 12))
    assert np.max(abs(formula - (3 + R * np.cos(2 * np.pi * n6 / 3 + np.radians(phi))))) < 1e-12

    # ---- Q3(a)(i): the samples
    fig, ax = plt.subplots(figsize=(8, 2.8))
    n = np.arange(-3, 12)
    xv = 3 + 4 * np.cos(2 * np.pi * n / 3) - (10 / 3) * np.sin(2 * np.pi * n / 3)
    stems(ax, n, xv, color=BLUE)
    ax.axvspan(-0.4, 5.4, color=ORANGE, alpha=0.10)
    ax.axvspan(-0.4, 2.4, color=GREEN, alpha=0.10)
    for k in range(6):
        ax.text(k + 0.12, xv[k + 3] + (0.3 if xv[k + 3] >= 0 else -0.6), f"{xv[k + 3]:.3f}", fontsize=7.5)
    ax.text(5.3, 8.3, "orange: the 6 DFT samples (n = 0..5)", ha="right", fontsize=8, color="k")
    ax.text(-0.3, -3.85, "green: one fundamental period (n = 0..2)", ha="left", fontsize=8, color="k")
    ax.set_ylim(-4.3, 9.3); ax.set_xticks(n); ax.set_xlabel("n")
    ax.set_title(r"Q3(a)(i)  $x[n]=3+4\cos\frac{2\pi n}{3}-\frac{10}{3}\sin\frac{2\pi n}{3}=3+5.207\cos(\frac{2\pi n}{3}+39.8^\circ)$")
    save(fig, "24S2_Q3a_x.png")

    # ---- Q3(a)(ii): DTFT = impulses of area 2*pi*a_k, repeating every 2*pi
    a0, a1 = 3.0, (12 + 10j) / 6
    lines = []   # (Omega, complex area)
    for c in [-2 * np.pi, 0, 2 * np.pi]:
        lines += [(c, 2 * np.pi * a0), (c + 2 * np.pi / 3, 2 * np.pi * a1), (c - 2 * np.pi / 3, 2 * np.pi * np.conj(a1))]
    lines = [(w, A) for w, A in lines if -2 * np.pi - 1e-9 <= w <= 2 * np.pi + 1e-9]
    fig, axs = plt.subplots(2, 1, figsize=(10, 5.6))
    for ax in axs:
        ax.axvspan(-np.pi, np.pi, color=ORANGE, alpha=0.08)
        ax.set_xticks(*PI_TICKS); ax.set_xlim(-2 * np.pi - 0.4, 2 * np.pi + 0.4)
        ax.set_xlabel(r"$\Omega$ (rad/sample)")
    for w, A in lines:
        main = -np.pi <= w < np.pi
        col = BLUE if main else GREY
        lab = None
        if main:
            lab = r"$6\pi$" + "\n(=18.85)" if abs(w) < 1e-9 else r"$5.21\pi$" + "\n(=16.36)"
        impulse(axs[0], w, abs(A), color=col, text=lab, dy=0.4)
    axs[0].set_ylim(0, 25); axs[0].axhline(0, color="k", lw=0.8)
    axs[0].set_title(r"magnitude $|X(\Omega)|$: impulses of area $2\pi|a_k|$ (shaded = one period $-\pi\leq\Omega<\pi$; grey = $2\pi$ repeats)")
    for w, A in lines:
        main = -np.pi <= w < np.pi
        ph = np.degrees(np.angle(A)) if abs(A) > 0 else 0.0
        col = RED if main else GREY
        axs[1].vlines(w, 0, ph, color=col, lw=2); axs[1].plot(w, ph, "o", color=col, ms=5)
        if main:
            axs[1].text(w, ph + (5 if ph >= 0 else -5), "0°" if abs(ph) < 1e-9 else f"{ph:+.1f}°", ha="center",
                        va="bottom" if ph >= 0 else "top", fontsize=8)
    axs[1].axhline(0, color="k", lw=0.8); axs[1].set_ylim(-60, 60)
    axs[1].set_title(r"phase $\angle X(\Omega)$: $0$ at $\Omega=0$, $+39.8^\circ$ at $+\frac{2\pi}{3}$, $-39.8^\circ$ at $-\frac{2\pi}{3}$")
    save(fig, "24S2_Q3a_dtft.png")

    # ---- Q3(b): steady state of y = x + 2x[n-1] + 0.2y[n-1]
    Hw = lambda W: (1 + 2 * np.exp(-1j * W)) / (1 - 0.2 * np.exp(-1j * W))
    H0, H1 = Hw(0).real, Hw(np.pi / 5)
    assert abs(H0 - 3.75) < 1e-12 and abs(abs(H1) - 3.39066) < 1e-5
    amp, ph = 2 * abs(H1), np.pi / 3 + np.angle(H1)
    assert abs(amp - 6.7813) < 1e-4 and abs(np.degrees(ph) - 27.835) < 1e-3
    N = 200; n = np.arange(N)
    xin = 1 + 2 * np.cos(np.pi * n / 5 + np.pi / 3)
    y = np.zeros(N); xp = yp = 0.0
    for k in range(N):
        y[k] = xin[k] + 2 * xp + 0.2 * yp; xp, yp = xin[k], y[k]
    yss = H0 + amp * np.cos(np.pi * n / 5 + ph)
    assert np.max(abs(y[40:] - yss[40:])) < 1e-12
    fig, ax = plt.subplots(figsize=(9, 3.0))
    nn = n[:25]
    stems(ax, nn - 0.15, xin[:25], color=GREY, label="input x[n]", ms=3)
    stems(ax, nn, y[:25], color=BLUE, label="y[n] from rest (running the equation)", ms=3)
    ax.plot(nn + 0.15, yss[:25], "s", mfc="none", color=GREEN, ms=6, label=r"$y_{ss}[n]=3.75+6.781\cos(\frac{\pi}{5}n+27.8^\circ)$")
    ax.set_xlabel("n"); ax.set_ylim(-5, 13.5); ax.legend(fontsize=7, loc="upper center", ncol=3)
    ax.set_title("Q3(b)  after the first few samples the output sits on the steady-state formula (transient = -7.75(0.2)^n)")
    save(fig, "24S2_Q3b_y.png")


# =====================================================================
# Question 4
# =====================================================================
def fig_q4():
    # ---- Q4(a): step response of H(z) = z/(z - 1/2)
    n = np.arange(0, 13)
    yrec = np.zeros(len(n)); yp = 0.0
    for k in n:
        yrec[k] = 0.5 * yp + 1.0; yp = yrec[k]
    yform = 2 - 0.5 ** n
    assert np.max(abs(yrec - yform)) < 1e-15
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.6), gridspec_kw=dict(width_ratios=[1, 1.6]))
    zplane(axs[0], [0], [0.5, 1.0], 1.0, lim=1.5,
           roc_text="Y(z) = z² / ((z-½)(z-1))\nROC |z| > 1\nFVT check: 0.5 inside,\nsimple pole at z = 1 → OK",
           zero_label="double zero at 0")
    axs[0].set_title("poles of Y(z) (for the final value theorem)", fontsize=9)
    ax = axs[1]
    stems(ax, n, yform, color=BLUE, label=r"$y[n]=2-(\frac{1}{2})^n$")
    stems(ax, n + 0.2, np.ones(len(n)), color=GREY, label="input u[n]", ms=3)
    ax.axhline(2, color=GREEN, ls="--")
    ax.text(12.3, 2.04, "final value 2", ha="right", va="bottom", fontsize=8)
    for k in range(4):
        ax.text(k, yform[k] + 0.07, f"{yform[k]:g}", ha="center", fontsize=8)
    ax.set_ylim(0, 2.5); ax.set_xlabel("n"); ax.legend(fontsize=7, loc="lower right")
    ax.set_title("Q4(a)(i) step response of the relaxed system")
    save(fig, "24S2_Q4a_step.png")

    # ---- Q4(b): 2y'' + 3y' + y = u(t), zero initial conditions
    sol = integrate.solve_ivp(lambda t, Y: [Y[1], (1 - 3 * Y[1] - Y[0]) / 2], [0, 14], [0, 0],
                              rtol=1e-10, atol=1e-12, dense_output=True)
    t = np.linspace(0, 14, 1400)
    yf = 1 - 2 * np.exp(-t / 2) + np.exp(-t)
    assert np.max(abs(sol.sol(t)[0] - yf)) < 1e-7
    fig, axs = plt.subplots(1, 2, figsize=(10.5, 3.6), gridspec_kw=dict(width_ratios=[1, 1.6]))
    splane(axs[0], [], [0, -0.5, -1], 0, lim=(-1.6, 0.8, -1.2, 1.2),
           roc_text="Y(s) = 1/(s(2s+1)(s+1))\nFVT check: simple pole at 0,\n-0.5 and -1 in the left half → OK")
    axs[0].set_title("poles of Y(s) (for the final value theorem)", fontsize=9)
    ax = axs[1]
    ax.plot(t, yf, color=BLUE, lw=2, label=r"$y(t)=1-2e^{-t/2}+e^{-t}$")
    ax.plot(t, -2 * np.exp(-t / 2), "--", color=ORANGE, lw=1, label=r"$-2e^{-t/2}$ (pole $-\frac{1}{2}$)")
    ax.plot(t, np.exp(-t), ":", color=GREY, lw=1.5, label=r"$e^{-t}$ (pole $-1$)")
    ax.axhline(1, color=GREEN, ls="--"); ax.text(14, 1.03, "y(∞) = 1", ha="right", va="bottom", fontsize=8)
    ax.set_ylim(-2.1, 1.4); ax.set_xlabel("t (s)"); ax.legend(fontsize=7, loc="lower right")
    ax.set_title("Q4(b) step response from rest: starts flat at 0, settles at 1")
    save(fig, "24S2_Q4b_step.png")

    # ---- Q4(c): ROC and stability, continuous time vs discrete time
    fig, axs = plt.subplots(2, 4, figsize=(15, 7.2), gridspec_kw=dict(width_ratios=[1, 1.15, 1, 1.15]))
    splane(axs[0, 0], [], [-0.5, -1], -0.5, lim=(-2, 1.5, -1.5, 1.5),
           roc_text="H(s)=1/((2s+1)(s+1))\nROC Re(s) > -0.5\ncontains the jω-axis\n→ STABLE")
    axs[0, 0].set_title("CT, causal, poles in left half", fontsize=9)
    tt = np.linspace(0, 10, 1000)
    axs[0, 1].plot(tt, np.exp(-tt / 2) - np.exp(-tt), color=BLUE, lw=2)
    axs[0, 1].set_title(r"$h(t)=(e^{-t/2}-e^{-t})u(t)$ dies out", fontsize=9); axs[0, 1].set_xlabel("t")
    splane(axs[0, 2], [], [0.5], 0.5, lim=(-2, 1.5, -1.5, 1.5),
           roc_text="H(s)=1/(s-0.5)\nROC Re(s) > 0.5\nmisses the jω-axis\n→ UNSTABLE")
    axs[0, 2].set_title("CT, causal, pole in right half", fontsize=9)
    axs[0, 3].plot(tt, np.exp(0.5 * tt), color=RED, lw=2)
    axs[0, 3].set_title(r"$h(t)=e^{0.5t}u(t)$ grows (148 at t = 10)", fontsize=9); axs[0, 3].set_xlabel("t")
    zplane(axs[1, 0], [0], [0.5], 0.5, lim=2.4,
           roc_text="H(z)=z/(z-0.5)\nROC |z| > 0.5\ncontains the unit circle\n→ STABLE")
    axs[1, 0].set_title("DT, causal, pole inside unit circle", fontsize=9)
    nn = np.arange(0, 11)
    stems(axs[1, 1], nn, 0.5 ** nn, color=BLUE)
    axs[1, 1].set_title(r"$h[n]=(0.5)^n u[n]$: 1, 0.5, 0.25, ... dies", fontsize=9); axs[1, 1].set_xlabel("n")
    zplane(axs[1, 2], [0], [2.0], 2.0, lim=2.4,
           roc_text="H(z)=z/(z-2)\nROC |z| > 2\nmisses the unit circle\n→ UNSTABLE")
    axs[1, 2].set_title("DT, causal, pole outside unit circle", fontsize=9)
    stems(axs[1, 3], nn, 2.0 ** nn, color=RED)
    axs[1, 3].set_title(r"$h[n]=2^n u[n]$: 1, 2, 4, ... grows (1024 at n = 10)", fontsize=9); axs[1, 3].set_xlabel("n")
    fig.suptitle("Q4(c)  causal ROC = right of the rightmost pole (s) / outside the outermost pole (z); "
                 "stable ⇔ that ROC contains the jω-axis / the unit circle (bold black)", fontsize=10)
    save(fig, "24S2_Q4c_roc.png")


if __name__ == "__main__":
    fig_q1(); fig_q2(); fig_q3(); fig_q4()
    print("all 24S2 checks passed")
