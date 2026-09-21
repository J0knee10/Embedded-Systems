# SC4172 TinyML — environment

> **This course is the one exception to the repo-wide Python 3.11 rule.**
> It is pinned to **Python 3.8** and must stay there. See below.

## Why 3.8 and not 3.11

`requirements.txt` pins `tensorflow==2.4.1` to match the **Arduino TensorFlow Lite
2.4.0-ALPHA** library running on the board. The model you train here has to be
convertible to a TFLite flatbuffer that the on-device interpreter can actually load —
so the host-side TensorFlow version is a hardware constraint, not a preference.

TensorFlow 2.4.1 ships exactly one Windows wheel:

```
tensorflow-2.4.1-cp38-cp38-win_amd64.whl
```

`cp38` = CPython 3.8 only. There is no 3.9, 3.11 or 3.13 build, and never will be.
If you try to install it on 3.11 pip will just say "no matching distribution".

Everything else in the pin set follows from that (numpy 1.19.5, h5py 2.10.0 — TF 2.4.1
will not import with newer ones).

## Setup on a new machine

Needs **Python 3.8** installed (this is EOL, so download it explicitly from
python.org — it is not offered by default anymore).

```powershell
# from this folder
py -3.8 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock.txt
```

Use `requirements.lock.txt` (92 packages, fully resolved) for an exact reproduction.
`requirements.txt` is the hand-maintained direct-dependency list — edit that one, then
regenerate the lock:

```powershell
python -m pip freeze > requirements.lock.txt
```

## Jupyter

The venv is registered as the kernel **"Python 3.8 (TF-Arduino)"**. To re-register after
recreating the venv:

```powershell
python -m ipykernel install --user --name .venv --display-name "Python 3.8 (TF-Arduino)"
```

## Note on pip

Modern pip refuses to run on 3.8 (`This version of pip does not support python 3.8`).
The venv's bundled pip 21.1.1 works fine — just don't upgrade it.
