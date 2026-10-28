"""Helper functions for lab experiments.
"""
import timeit
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from IPython.display import Audio, display


def spectrum(ax, x, fs, label, nfft=None):
    """Positive half of the two-sided spectrum; no factor-of-two scaling."""
    size = len(x) if nfft is None else nfft
    f = np.fft.rfftfreq(size, 1 / fs)
    ax.plot(f, np.abs(np.fft.rfft(x, size)) / len(x), label=label)
    ax.set(xlabel="Frequency (Hz)", ylabel="|X| / observed samples")
    ax.legend(fontsize=8)


def _sampling_grid(sample_rate, duration):
    """Return sample indices/times and a dense grid; rate and duration are positive."""
    n = np.arange(int(np.ceil(sample_rate * duration)))
    return n, n / sample_rate, np.linspace(0, duration, max(2000, 20 * len(n)))


def sampling_view(frequency=3, sample_rate=16, duration=1, phase=0):
    """Observe a continuous cosine, then display its discrete sample sequence."""
    n, times, dense_times = _sampling_grid(sample_rate, duration)
    samples = np.cos(2 * np.pi * frequency * times + phase)
    fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), constrained_layout=True)
    ax[0].plot(dense_times, np.cos(2 * np.pi * frequency * dense_times + phase),
               label="Continuous-time cosine")
    ax[0].plot(times, samples, "o", label="Samples at t = n / sample_rate")
    ax[0].set(xlabel="Time t (seconds)", ylabel="Amplitude", title="Continuous time and sample times")
    ax[0].legend(fontsize=8)
    ax[1].stem(n, samples, basefmt=" ")
    ax[1].set(xlabel="Integer sample index n", ylabel="x[n]", title="The discrete sequence: values only at integer n")
    plt.show()
    return n, samples


def aliasing_view(frequency=3, alias_frequency=13, sample_rate=16, duration=1):
    """Compare two continuous cosines and the samples they produce."""
    n, times, dense_times = _sampling_grid(sample_rate, duration)
    samples = [np.cos(2 * np.pi * f * times) for f in (frequency, alias_frequency)]
    fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), constrained_layout=True)
    for j, (f, values) in enumerate(zip((frequency, alias_frequency), samples)):
        label = "%g Hz cosine" % f
        ax[0].plot(dense_times, np.cos(2 * np.pi * f * dense_times),
                   color="C%d" % j, alpha=0.8, label=label)
        ax[0].plot(times, values, "o", color="C%d" % j, fillstyle="none", markersize=7 + 3 * j)
        ax[1].stem(n, values, linefmt="C%d-" % j, markerfmt="C%d%s" % (j, "o" if j == 0 else "x"),
                   basefmt=" ", label="Samples of " + label)
    ax[0].set(xlabel="Time t (seconds)", ylabel="Amplitude", title="Distinct continuous signals; circles mark sample times")
    ax[1].set(xlabel="Integer sample index n", ylabel="Sample value", title="Do the two discrete sequences differ?")
    for axis in ax:
        axis.legend(fontsize=8)
    plt.show()
    return samples[0], samples[1]


def _stem_values(ax, n, values, label=None, color=0):
    """Display real samples directly; expose both components for complex samples."""
    values = np.real_if_close(values)
    real_label = label if not np.iscomplexobj(values) else (label or "Signal") + " (real part)"
    ax.stem(n, values.real, linefmt="C%d-" % color, markerfmt="C%do" % color,
            basefmt=" ", label=real_label)
    if np.iscomplexobj(values):
        ax.stem(n, values.imag, linefmt="C%d--" % color, markerfmt="C%dx" % color,
                basefmt=" ", label=(label or "Signal") + " (imaginary part)")
    if label is not None or np.iscomplexobj(values):
        ax.legend(fontsize=8)


def _phase_points(ax, X, label=None, color=0):
    """Plot phase only where the DFT magnitude is appreciably nonzero."""
    threshold = 1e-9 * np.max(np.abs(X))
    keep = np.abs(X) > threshold
    frequencies = 2 * np.pi * np.fft.fftfreq(len(X))
    ax.plot(frequencies[keep], np.angle(X[keep]), "o" if color == 0 else "x", color="C%d" % color, label=label)
    ax.set(xlabel="Angular frequency (radians/sample)", ylabel="Phase (radians)",
           xlim=(-np.pi, np.pi), ylim=(-3.5, 3.5))
    ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    ax.set_yticks([-np.pi, 0, np.pi])
    ax.set_yticklabels(["-pi", "0", "pi"])


def dft_signal(x):
    """Display a finite discrete signal without introducing a sampling rate."""
    x = np.asarray(x)
    fig, ax = plt.subplots(figsize=(10, 2.8), constrained_layout=True)
    _stem_values(ax, np.arange(len(x)), x)
    ax.set(xlabel="Integer sample index n", ylabel="x[n]", title="The input block: N = %d discrete values" % len(x))
    plt.show()


def dft_magnitude(x):
    """Show the full two-sided DFT magnitude with signed discrete frequencies."""
    x = np.asarray(x)
    X = np.fft.fft(x)
    frequencies = 2 * np.pi * np.fft.fftfreq(len(x))
    order = np.argsort(frequencies)
    fig, ax = plt.subplots(figsize=(10, 2.8), constrained_layout=True)
    ax.stem(frequencies[order], np.abs(X[order]) / len(x), basefmt=" ")
    ax.set(xlabel="Angular frequency (radians/sample)", ylabel="|X[k]| / N", title="DFT magnitude: the weight of each frequency", xlim=(-np.pi, np.pi))
    ax.set_xticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
    ax.set_xticklabels([r"$-\pi$", r"$-\pi/2$", "0", r"$\pi/2$", r"$\pi$"])
    plt.show()
    return X


def dft_phase(x):
    """Omit negligible coefficients because phase is undefined at zero magnitude."""
    x = np.asarray(x)
    X = np.fft.fft(x)
    fig, ax = plt.subplots(figsize=(10, 2.8), constrained_layout=True)
    _phase_points(ax, X)
    ax.set_title("DFT phase: only coefficients with nonnegligible magnitude are shown")
    plt.show()
    return X


def dft_reconstruction(x, periods=3):
    """Show the periodic IDFT extension of a nonempty vector; periods is at least 2."""
    x = np.asarray(x)
    N = len(x)
    X = np.fft.fft(x)
    inside = np.fft.ifft(X)
    n_extended = np.arange(-N, (periods - 1) * N)
    reconstructed = np.exp(2j * np.pi * n_extended[:, None] * np.arange(N) / N) @ X / N
    fig, ax = plt.subplots(2, 1, figsize=(10, 5.5), constrained_layout=True)
    _stem_values(ax[0], np.arange(N), x, "Input", 0)
    ax[0].plot(np.arange(N), inside.real, "x", color="C1", label="IDFT (real part)")
    if np.iscomplexobj(np.real_if_close(inside)):
        ax[0].plot(np.arange(N), inside.imag, "+", color="C1", label="IDFT (imaginary part)")
    ax[0].legend(fontsize=8)
    ax[0].set(xlabel="Integer sample index n", ylabel="Sample value", title="Inverse DFT recovers the input block")
    _stem_values(ax[1], n_extended, reconstructed.real if np.isrealobj(x) else reconstructed)
    ax[1].axvspan(-0.5, N - 0.5, alpha=0.1, color="green", label="Original input indices")
    for edge in range(-N, (periods - 1) * N, N):
        ax[1].axvline(edge - 0.5, linestyle=":", color="gray", linewidth=0.8)
    ax[1].set(xlabel="Integer sample index n", ylabel="IDFT sum", title="The same IDFT sum repeats every N indices")
    ax[1].legend(fontsize=8)
    plt.show()
    return n_extended, reconstructed


def benchmark(dense_dft, sizes=(32, 64, 128, 256, 512, 1024)):
    """Plot measured times, calibrated runtime models, and the dense/FFT ratio.

    sizes is a nonempty sequence of integers greater than 1. The N^2 and
    N*log2(N) models match each algorithm's measured time at the largest N;
    they illustrate scaling, not exact runtime guarantees.
    """
    sizes = np.sort(np.asarray(sizes))
    elapsed = []
    for N in sizes:
        x = np.cos(2 * np.pi * 3 * np.arange(N) / N) + 0.3 * np.sin(2 * np.pi * 5 * np.arange(N) / N)
        # Median of three batches reduces timing noise.
        elapsed.append([np.median(timeit.repeat(lambda: fn(x), number=count, repeat=3)) / count
                        for fn, count in [(dense_dft, 3), (np.fft.fft, 100)]])
    elapsed = np.array(elapsed)

    # Convert growth formulas to seconds using one measured reference per method.
    growth = np.column_stack((sizes.astype(float) ** 2, sizes * np.log2(sizes)))
    predicted = growth / growth[-1] * elapsed[-1]

    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), constrained_layout=True)
    for j, label in enumerate(["Build matrix + product", "FFT"]):
        ax[0].loglog(sizes, elapsed[:, j], "o-", label=label)
    ax[0].set(xlabel="N samples", ylabel="Seconds / transform", title="Measured runtime")
    ax[1].loglog(sizes, predicted[:, 0], "o-", label=r"Dense DFT: $aN^2$")
    ax[1].loglog(sizes, predicted[:, 1], "o-", label=r"FFT: $bN\log_2 N$")
    ax[1].set(xlabel="N samples", ylabel="Seconds / transform",
              title="Predicted runtime")
    # Matching scales make measured and predicted times directly comparable.
    limits = (0.7 * min(elapsed.min(), predicted.min()),
              1.4 * max(elapsed.max(), predicted.max()))
    for axis in ax[:2]:
        axis.set_ylim(limits)
        axis.legend(fontsize=8)
    ax[2].loglog(sizes, elapsed[:, 0] / elapsed[:, 1], "o-")
    ax[2].set(xlabel="N samples", ylabel="Dense time / FFT time",
              title="Measured runtime ratio")
    for axis in ax:
        axis.grid(True, which="major", alpha=0.25)
    plt.show()
    return sizes, elapsed


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


def audio_comparison(signals, fs):
    """Plot the first 10 ms and spectra, then play the named real audio arrays."""
    fig, ax = plt.subplots(1, 2, figsize=(11, 3), constrained_layout=True)
    shown = int(0.01 * fs)
    for label, x in signals.items():
        ax[0].plot(np.arange(shown) / fs, x[:shown], label=label, alpha=0.8)
        spectrum(ax[1], x, fs, label)
    ax[0].set(xlabel="Time (s)", ylabel="Normalized amplitude", title="First 10 ms")
    ax[0].legend(fontsize=8)
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


def load_radio_audio(path, fs=96000, duration=5):
    """Prepare a real radio input with frequencies up to 4000 Hz.

    Apply the lab's whole-block lowpass after loading/resampling, so both
    bundled recordings and replacement WAV files use the same preparation.
    """
    return fft_filter(load_audio(path, fs=fs, duration=duration), fs, 0, 4000)
