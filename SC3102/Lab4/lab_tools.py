"""Helper functions for lab experiments.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from IPython.display import Audio, HTML, display


def spectrum(ax, x, fs, label, nfft=None):
    """Positive half of the two-sided spectrum; no factor-of-two scaling."""
    size = len(x) if nfft is None else nfft
    f = np.fft.rfftfreq(size, 1 / fs)
    ax.plot(f, np.abs(np.fft.rfft(x, size)) / len(x), label=label)
    ax.set(xlabel="Frequency (Hz)", ylabel="|X| / observed samples")
    ax.legend(fontsize=8)


def audio_signals():
    """Return 16 kHz two-second tones and a noisy first tone for filter experiments."""
    fs = 16000
    t = np.arange(2 * fs) / fs
    first = (np.sin(2 * np.pi * 220 * t) + 0.3 * np.sin(2 * np.pi * 440 * t)) / 1.3
    second = (np.sin(2 * np.pi * 330 * t) + 0.3 * np.sin(2 * np.pi * 660 * t)) / 1.3
    noise = 0.35 * np.sin(2 * np.pi * 3600 * t) + 0.25 * np.sin(2 * np.pi * 4100 * t)
    return fs, first, second, first + noise


def band_mask(f, low, high):
    """Select both signs of the frequency band low <= |f| <= high, in hertz."""
    return (np.abs(f) >= low) & (np.abs(f) <= high)


def fft_filter(x, fs, low, high):
    """Filter a real sample block by an ideal, two-sided DFT frequency mask.

    This offline operation assumes a periodic block and uses circular convolution.
    """
    return np.fft.ifft(np.fft.fft(x) * band_mask(np.fft.fftfreq(len(x), 1 / fs), low, high)).real


def listen(signals, fs):
    """One gain for the entire group; no per-player normalization."""
    gain = 0.8 / max(1.0, max(np.max(np.abs(x)) for x in signals.values()))
    for label, x in signals.items():
        print(label)
        display(Audio(gain * x, rate=fs, normalize=False))


def audio_comparison(signals, fs, title="DFT magnitude"):
    """Compare spectra, then play the named real audio arrays."""
    fig, ax = plt.subplots(figsize=(10, 3), constrained_layout=True)
    for label, x in signals.items():
        spectrum(ax, x, fs, label)
    ax.set_title(title)
    plt.show()
    listen(signals, fs)


def load_audio(path, fs=16000, duration=5):
    """Read a WAV file as mono floats at fs samples/second, trimmed/padded to duration.

    Integer PCM is scaled to roughly [-1, 1]; floating-point WAV amplitudes are
    preserved. Stereo channels are averaged, and resampling includes filtering.
    """
    source_rate, samples = wavfile.read(path)
    if samples.dtype == np.uint8:
        samples = (samples.astype(float) - 128) / 128
    elif np.issubdtype(samples.dtype, np.integer):
        samples = samples.astype(float) / (2 ** (8 * samples.dtype.itemsize - 1))
    else:
        samples = samples.astype(float)
    if samples.ndim == 2:
        samples = samples.mean(axis=1)
    samples = signal.resample_poly(samples, fs, source_rate)
    length = int(fs * duration)
    return np.pad(samples[:length], (0, max(0, length - len(samples))))


def rational_parts(b, a):
    """Return Z-plane roots and partial fractions of B(z^-1)/A(z^-1).

    Use reduced real coefficients, a[0] != 0, and distinct nonzero poles. These
    assumptions keep the inverse sequence a sum of ordinary exponential modes.
    """
    b, a = np.trim_zeros(np.asarray(b, dtype=float), "b"), np.trim_zeros(np.asarray(a, dtype=float), "b")
    # Equal powers of z convert numerator and denominator to ordinary polynomials.
    size = max(len(b), len(a))
    zeros = np.roots(np.pad(b, (0, size - len(b))))
    poles = np.roots(np.pad(a, (0, size - len(a))))
    r, p, k = signal.residuez(b, a, tol=1e-7)
    return b, a, zeros, poles, r, p, k


def _z_surface_figure(real, imag, magnitude, valid, region):
    """Build a browser-controlled surface without changing the selected model."""
    import plotly.graph_objects as go
    surface = go.Surface(
        x=real, y=imag, z=np.minimum(magnitude, 15),
        surfacecolor=valid.astype(int), cmin=0, cmax=1,
        colorscale=[[0, "#a6a6a6"], [0.499, "#a6a6a6"],
                    [0.5, "#199966"], [1, "#199966"]],
        showscale=False, connectgaps=False,
        text=np.char.add(np.char.mod("|H(z)|: %.4g<br>", magnitude),
                         np.where(valid, "Inside selected ROC", "Outside selected ROC")),
        hovertemplate=("Real part: %{x:.3f}<br>Imaginary part: %{y:.3f}"
                       "<br>%{text}<extra></extra>"),
    )
    figure = go.Figure(surface)
    figure.update_layout(
        title=dict(text="Algebraic magnitude (height capped at 15)<br>"
                        "<sup>Region %d: green = selected ROC; gray = outside</sup>" % region),
        template="plotly_white", height=540, margin=dict(l=15, r=15, b=20, t=75),
        scene=dict(xaxis_title="Real part of z", yaxis_title="Imaginary part of z",
                   zaxis=dict(title="|H(z)| (capped)", range=[0, 15]),
                   aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.85),
                   camera=dict(eye=dict(x=1.5, y=-1.7, z=1.2), up=dict(x=0, y=0, z=1)),
                   dragmode="turntable"),
    )
    return figure


def z_explorer(b, a, region=1, view="both", interactive=False):
    """Plot rational H(z) using 'plane', 'surface', or 'both'; interactive shows a surface.

    Coefficients follow rational_parts. Region numbers count annuli from the
    origin outwards, starting at 0; their boundaries are the pole magnitudes.
    """
    b, a, zeros, poles, residues, p, direct = rational_parts(b, a)
    radii = np.unique(np.round(np.abs(p), 8))
    edges = np.r_[0, radii, np.inf]
    lo, hi = edges[region:region + 2]
    bound = max(1.6, 1.4 * max(np.abs(poles), default=0))
    grid = np.linspace(-bound, bound, 151)
    real, imag = np.meshgrid(grid, grid)
    z = real + 1j * imag
    valid = (np.abs(z) > lo) & (np.abs(z) < hi)
    with np.errstate(divide="ignore", invalid="ignore"):
        magnitude = np.abs(np.polynomial.polynomial.polyval(1 / z, b) /
                           np.polynomial.polynomial.polyval(1 / z, a))
    if interactive:
        figure = _z_surface_figure(real, imag, magnitude, valid, region)
        # Bundle the JavaScript so the plot also works without internet access.
        display(HTML(figure.to_html(
            full_html=False, include_plotlyjs=True,
            config=dict(responsive=True, scrollZoom=True, displayModeBar=True, displaylogo=False,
                        modeBarButtonsToRemove=["orbitRotation"]),
        )))
        return residues, p, direct, lo, hi
    views = ("plane", "surface") if view == "both" else (view,)
    fig = plt.figure(figsize=(5.5 * len(views), 4.5), constrained_layout=True)
    if "plane" in views:
        ax = fig.add_subplot(1, len(views), views.index("plane") + 1)
        ax.contourf(real, imag, valid.astype(float), levels=[0.5, 1.5], colors=["#bfe5d5"])
        theta = np.linspace(0, 2 * np.pi, 300)
        ax.plot(np.cos(theta), np.sin(theta), "k--", label="Unit circle")
        for radius in radii:
            ax.plot(radius * np.cos(theta), radius * np.sin(theta), ":", color="gray")
        ax.scatter(zeros.real, zeros.imag, facecolors="none", edgecolors="blue", s=65, label="Zeros")
        ax.scatter(poles.real, poles.imag, marker="x", color="red", s=65, label="Poles of H")
        ax.set(xlabel="Real part of z", ylabel="Imaginary part of z",
               title="Region %d: green = selected ROC" % region, aspect="equal")
        ax.legend(fontsize=8)
    if "surface" in views:
        ax3 = fig.add_subplot(1, len(views), views.index("surface") + 1, projection="3d")
        colors = np.where(valid[..., None], np.array([0.1, 0.6, 0.4, 0.8]), np.array([0.65, 0.65, 0.65, 0.35]))
        ax3.plot_surface(real, imag, np.minimum(magnitude, 15), facecolors=colors, rstride=3, cstride=3)
        ax3.set(xlabel="Real part of z", ylabel="Imaginary part of z",
                title="Algebraic magnitude (capped at 15)\nGray is outside the selected ROC")
        # A 2D label stays visible in notebook images, unlike the clipped 3D z label.
        ax3.text2D(1.10, 0.5, "|H(z)|", transform=ax3.transAxes, rotation=90, va="center")
    plt.show()
    return residues, p, direct, lo, hi


def _demo_axes(view, names, combined="all"):
    """Allocate only the requested stage of a teaching demonstration."""
    chosen = names if view == combined else (view,)
    width = 6.8 if len(chosen) == 1 else 4.4 * len(chosen)
    _, axes = plt.subplots(1, len(chosen), figsize=(width, 3.5), squeeze=False, constrained_layout=True)
    return dict(zip(chosen, axes[0]))


def roc_sums(model, points=(0.9, 1.5), count=35, view="all"):
    """Plot the inverse sequence, weighted terms, or partial-sum convergence.

    Model comes from z_explorer; points are nonzero complex values away from
    poles. View is 'sequence', 'terms', 'sums', or 'all'.
    """
    residues, poles, direct, lo, hi = model
    n = np.arange(-count, count + 1)
    h = np.zeros(len(n), dtype=complex)
    for residue, pole in zip(residues, poles):
        right = abs(pole) <= lo + 1e-7
        keep = n >= 0 if right else n < 0
        h[keep] += (1 if right else -1) * residue * pole ** n[keep]
    for i, value in enumerate(direct):
        h[n == i] += value
    axes = _demo_axes(view, ("sequence", "terms", "sums"))
    if "sequence" in axes:
        axes["sequence"].stem(n, h.real, basefmt=" ")
        axes["sequence"].set(xlabel="Integer sample index n", ylabel="Real part of h[n]", title="Selected impulse response")
    for z in points if ("terms" in axes or "sums" in axes) else ():
        terms = h * complex(z) ** (-n)
        sums = np.array([np.sum(terms[np.abs(n) <= M]) for M in range(count + 1)])
        value = sum(r / (1 - p / z) for r, p in zip(residues, poles)) + sum(k * z ** (-i) for i, k in enumerate(direct))
        label = "z=%s (%s ROC)" % (z, "inside" if lo < abs(z) < hi else "outside")
        if "terms" in axes:
            axes["terms"].semilogy(n, np.maximum(np.abs(terms), 1e-16), label=label)
        if "sums" in axes:
            axes["sums"].semilogy(np.arange(count + 1), np.maximum(np.abs(sums - value), 1e-16), label=label)
    if "terms" in axes:
        axes["terms"].set(xlabel="Integer sample index n", ylabel="|h[n] z^(-n)|", title="Weighted terms (logarithmic scale)")
        axes["terms"].legend(fontsize=8)
    if "sums" in axes:
        axes["sums"].set(xlabel="M in sum from -M to M", ylabel="|S_M - rational value|", title="Partial-sum error (logarithmic scale)")
        axes["sums"].legend(fontsize=8)
    plt.show()


def initial_condition_demo(a=0.5, initial=4.0, input_level=1.0, view="response", steps=20):
    """Iterate y[n] = a*y[n-1] + x[n], with y[-1] given and constant x[n].

    Parameters are real and steps is a positive integer. The sample x[0] first
    affects y[0]. View is 'response', 'zero_input', 'zero_state', or 'sum'.
    """
    n = np.arange(steps + 1)

    def iterate(start, level):
        """Advance the recurrence from y[-1]=start with constant input level."""
        values = np.empty(len(n))
        previous = start
        for index in range(len(n)):
            previous = a * previous + level
            values[index] = previous
        return values

    response = iterate(initial, input_level)
    zero_input = iterate(initial, 0.0)
    zero_state = iterate(0.0, input_level)
    _, ax = plt.subplots(figsize=(8, 3.8), constrained_layout=True)
    if view == "zero_input":
        ax.plot(n, zero_input, "o-", markersize=4, label="Zero-input response")
        title = "Only the initial value contributes"
        shown_initial, shown_input = initial, 0.0
    elif view == "zero_state":
        ax.plot(n, zero_state, "o-", markersize=4, label="Zero-state response")
        title = "Only the input contributes"
        shown_initial, shown_input = 0.0, input_level
    else:
        ax.plot(n, response, "o-", markersize=5, label="Response from iteration")
        shown_initial, shown_input = initial, input_level
        if view == "sum":
            ax.plot(n, zero_input + zero_state, "x--", markersize=6,
                    label="Zero-input + zero-state")
            title = "Add the two contributions to recover the complete response"
        else:
            title = "Calculate each output from the previous output and current input"
    ax.set(xlabel="Integer sample index n", ylabel="Output y[n]",
           title="%s\na=%g; y[-1]=%g; x[n]=%g for n >= 0" %
                 (title, a, shown_initial, shown_input))
    ax.set_xticks(np.unique(np.linspace(0, steps, min(steps + 1, 11), dtype=int)))
    ax.legend(fontsize=8)
    plt.show()
    return {"n": n, "response": response, "zero_input": zero_input,
            "zero_state": zero_state, "a": a,
            "initial": initial, "input_level": input_level}


def fir_demo(lengths=(9, 33, 257), low=100, high=1000, view="all"):
    """Show a causal FIR denoising filter using odd tap counts in lengths.

    Use 0 <= low < high < 8000 Hz. View is 'response', 'time', 'errors',
    'audio', or 'all'; error measures signal distortion after delay alignment.
    """
    fs, clean, _, noisy = audio_signals()
    axes = {} if view == "audio" else _demo_axes(view, ("response", "time", "errors"))
    errors, outputs = [], {"Original": clean, "Corrupted": noisy}
    reference = fft_filter(noisy, fs, low, high)
    # Same interior samples for every M; compensate delay only for comparison.
    interior = slice(1024, len(clean) - 1024)
    shown = 400  # 25 ms shows the onset and FIR delay.
    for M in lengths:
        cutoff = high if low == 0 else [low, high]
        h = signal.firwin(M, cutoff, pass_zero=(low == 0), window="hamming", fs=fs)
        y = signal.lfilter(h, [1], np.r_[noisy, np.zeros(M)])
        delay = (M - 1) // 2
        aligned = y[delay:delay + len(clean)]
        f, H = signal.freqz(h, worN=4096, fs=fs)
        if "response" in axes:
            axes["response"].plot(f, np.abs(H), label="%d taps" % M)
        if "time" in axes:
            axes["time"].plot(np.arange(shown) / fs, y[:shown], label="%d taps" % M)
        errors.append(np.sqrt(np.mean((aligned[interior] - clean[interior]) ** 2)))
        outputs["Filtered: %d taps" % M] = aligned[interior]
    if "response" in axes:
        axes["response"].plot(f, band_mask(f, low, high), "k--", label="Ideal magnitude")
        axes["response"].set(xlabel="Frequency (Hz)", ylabel="Gain", xlim=(0, 2500), title="Compare the frequency selection")
    if "time" in axes:
        axes["time"].plot(np.arange(shown) / fs, clean[:shown], "k--", label="Original")
        axes["time"].set(xlabel="Time (s)", ylabel="Amplitude", title="Original and filtered signals")
    if "errors" in axes:
        axes["errors"].plot(lengths, errors, "o-", label="Finite filter")
        axes["errors"].axhline(np.sqrt(np.mean((reference[interior] - clean[interior]) ** 2)), color="black", linestyle="--", label="Offline FFT mask")
        axes["errors"].set(xlabel="Number of taps M", ylabel="RMS error vs clean", title="Same interior samples for all M")
    for axis in axes.values():
        axis.legend(fontsize=7)
    if axes:
        plt.show()
    if view in ("all", "audio"):
        listen(outputs, fs)
    return np.array(errors)


def fir_radio_demo(messages, fs=60000, lengths=(9, 33, 513), carriers=(12000, 24000),
                   view="recovery", labels=("Music", "Dialogue"), bandwidth=4000):
    """Receive the two cosine-modulated Lab 3 messages using causal FIR filters.

    Messages is a 2-by-N real array, already lowpassed to bandwidth Hz. Use odd
    tap counts and bands [fc-bandwidth, fc+bandwidth] separated inside (0, fs/2).
    The recovery lowpass also uses bandwidth Hz, matching Lab 3's filter bands.
    View is 'response', 'recovery', or 'audio'.

    A bandpass and a lowpass of length M each delay the signal by (M-1)/2
    samples. Only the plotted, measured, and played comparisons remove the
    total M-1 sample delay; the returned recovered arrays retain that delay.
    """
    carriers = np.asarray(carriers)
    messages = np.asarray(messages)
    time = np.arange(messages.shape[1]) / fs
    channels = messages * np.cos(2 * np.pi * carriers[:, None] * time)
    combined = channels.sum(axis=0)
    padded = np.pad(combined, (0, 2 * (max(lengths) - 1)))
    n = np.arange(len(padded))
    interior = slice(1024, -1024)
    bandpass_taps, lowpass_taps = {}, {}
    selected, recovered, aligned = {}, {}, {}
    errors, delays = [], []

    for M in lengths:
        delay = (M - 1) // 2
        bandpass_taps[M] = np.stack([
            signal.firwin(M, [fc - bandwidth, fc + bandwidth], pass_zero=False, window="hamming", fs=fs)
            for fc in carriers
        ])
        lowpass_taps[M] = signal.firwin(M, bandwidth, window="hamming", fs=fs)
        selected[M] = np.stack([signal.lfilter(h, [1], padded) for h in bandpass_taps[M]])
        # Match the local carrier phase to the bandpass filter's known delay.
        mixed = 2 * selected[M] * np.cos(2 * np.pi * carriers[:, None] * (n - delay) / fs)
        recovered[M] = np.stack([signal.lfilter(lowpass_taps[M], [1], row) for row in mixed])
        aligned[M] = recovered[M][:, 2 * delay:2 * delay + len(combined)]
        errors.append(np.sqrt(np.mean((aligned[M][:, interior] - messages[:, interior]) ** 2, axis=1)))
        delays.append(2 * delay)
    errors, delays = np.asarray(errors), np.asarray(delays)

    if view == "audio":
        recordings = {}
        for j in range(2):
            recordings["Original " + labels[j]] = messages[j, interior]
            for M in lengths:
                recordings["%s: %d taps" % (labels[j], M)] = aligned[M][j, interior]
        listen(recordings, fs)
    else:
        _, axes = plt.subplots(1, 2, figsize=(11, 3.8), constrained_layout=True)
        for j, ax in enumerate(axes):
            if view == "response":
                for M in lengths:
                    frequencies, gain = signal.freqz(bandpass_taps[M][j], worN=4096, fs=fs)
                    ax.plot(frequencies, np.abs(gain), label="%d taps" % M)
                ax.plot(frequencies, band_mask(frequencies, carriers[j] - bandwidth, carriers[j] + bandwidth),
                        "k--", label="Ideal band")
                ax.set(xlabel="Frequency (Hz)", ylabel="Gain", xlim=(0, fs / 2),
                       title="%s: select the band around %g Hz" % (labels[j], carriers[j]))
            else:
                spectrum(ax, messages[j, interior], fs, "Original")
                for M in lengths:
                    spectrum(ax, aligned[M][j, interior], fs, "%d taps" % M)
                ax.set_title("%s: original and recovered spectra" % labels[j])
            ax.legend(fontsize=8)
        plt.show()
    return {"fs": fs, "messages": messages, "channels": channels, "combined": combined,
            "lengths": lengths, "carriers": carriers, "bandwidth": bandwidth, "bandpass_taps": bandpass_taps,
            "lowpass_taps": lowpass_taps, "selected": selected, "recovered": recovered,
            "aligned": aligned, "errors": errors, "delays": delays, "interior": interior}
