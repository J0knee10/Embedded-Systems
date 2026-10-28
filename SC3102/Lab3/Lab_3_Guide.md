# SC3102 Lab 3: Discrete Fourier Transforms — Quick Guide

A short overview of what this lab covers and what it's trying to teach.
For the full worked answers, see [Lab_3_Answers.md](Lab_3_Answers.md). The answers are also
written into [Lab-03-DFT.ipynb](Lab-03-DFT.ipynb) under each question, and the notebook has been
run so every plot and audio player is saved in it. Every number below comes from actually running
each experiment variation, not from theory alone.

---

## What the lab is about

You've done the Fourier transform for continuous-time signals. This lab covers the same idea once
a computer is involved, which forces two compromises. Most of the lab is about what those
compromises cost you.

### 1. Time becomes samples (Q1)

- An 8 Hz cosine sampled at 8 Hz looks exactly like a constant.
- At 16 Hz, a 3 Hz and a 13 Hz cosine give identical samples (they differ by about 1e-15, which is
  just rounding error). This is **aliasing**: sampling can't tell f apart from f ± m·fs.
- To keep a signal limited to frequency B intact, you need **fs > 2B** (the Nyquist rate).
- A sampled cosine is periodic only if f0/fs is a fraction. Its period is the denominator in lowest
  terms: 3/16 gives a period of 16, and 4/16 = 1/4 gives 4. If f0 = √2 Hz, the samples never repeat.

### 2. You only have a finite block of N samples (Q2)

That block is the DFT's input.

- A real cosine gives two spikes, at ±k, each of height A/2.
- The phases at +k and −k are mirror images, because X[−k] is the complex conjugate of X[k]. This
  holds for any real signal.
- If the block doesn't hold a whole number of cycles, energy spreads across all 64 bins. This is
  **spectral leakage**.
- The inverse DFT shows why: it rebuilds the block exactly, but it treats the block as repeating
  forever. With half a cycle in the block, that repetition has a jump at every edge, and the jump is
  what causes the leakage.

### 3. Speed (Q3)

The matrix DFT from lectures takes time proportional to N², while the FFT takes N·log N. On this
machine the FFT was 9× faster at N=32 and about 5,600× faster at N=2048.

### 4. Applications (Q4)

- **Noise removal:** filtering in the frequency domain means multiplying the spectrum by a 0/1 mask.
  A 100–1000 Hz band recovers the clean signal almost exactly (error about 7e-13). Cutting at
  300 Hz also removes the quieter 440 Hz tone. A 3000–5000 Hz band keeps only the noise.
- **AM radio:** multiplying a message by a cosine "carrier" moves its spectrum up to sit around the
  carrier frequency. That lets two messages that originally overlap (both 0–4 kHz) share one
  signal, at 8–16 kHz and 20–28 kHz, and both are recovered almost perfectly.
- The rule is that carriers must be at least 2B apart. Breaking it confirms this: with carriers only
  4 kHz apart, the recovered music is garbage (82% relative error).

---

## What you're supposed to learn

Each odd DFT effect comes from one of those two compromises:

- Sampling causes aliasing.
- Discrete time means frequency is measured in radians per sample, and only −π to π matters.
- The finite block means the DFT assumes the signal repeats, which causes leakage.

The FFT is what makes any of this practical. Q4 then connects back to Lab 2: convolving in time is
the same as multiplying in frequency. The first section of
[Lab_3_Answers.md](Lab_3_Answers.md) has a table matching each continuous-time idea you already
know to its discrete-time version.

---

## Things to know

- **Python version:** everything was run on the repo's existing `.venv` (Python 3.11, numpy 2.x),
  not the Python 3.8 the README pins. It worked without any changes. To open it as a notebook you
  need `pip install notebook` in that venv.
- **File size:** the notebook is about 6.6 MB, mostly because the saved audio players embed the sound.
- **Code cells:** no code was changed. All cells are at their default settings, so you can change
  the values marked `# EXPERIMENT` and re-run them yourself.
- **Timings will differ:** the Q3 speed numbers will vary on the lab machines, but the trend will be
  the same.

**Before the lab:** work through the "Key takeaways" list at the end of
[Lab_3_Answers.md](Lab_3_Answers.md) yourself. If you're asked about this in person, you'll need to
explain these ideas, not just have the answers.
