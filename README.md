# Embedded-Systems
Exploring Embedded Systems via BioTech project or Modules in NTU

---

## Python environments

**The repo default is Python 3.11** (`.python-version`). One course is an exception.

| Scope | Python | Venv | Dependencies |
|---|---|---|---|
| Repo-wide coursework (SC3102, SC2107, …) | **3.11** | `.venv/` | `requirements.txt` + `requirements.lock.txt` |
| `TinyML_SC4172/` | **3.8** (pinned, see below) | `TinyML_SC4172/.venv/` | `TinyML_SC4172/requirements.txt` + `.lock.txt` |
| `20250513 python driver/` | 3.11 on the Pi | — installed on target | `20250513 python driver/requirements.txt` |

### Setup on a new machine

```powershell
git clone <repo> && cd embeddedSys

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock.txt
```

For TinyML, repeat inside `TinyML_SC4172/` with `py -3.8` — see that folder's README.

### Why TinyML is stuck on 3.8

`tensorflow==2.4.1` (pinned to match the Arduino TFLite 2.4.0-ALPHA library on the board)
ships only a `cp38-cp38-win_amd64` wheel. There is no 3.9+ build. That course therefore
keeps its own interpreter and its own venv rather than following the repo default.

### Conventions

- **Pin with `==`, not `>=`.** `requirements.txt` has no field for the Python version, so
  an unpinned range silently resolves to *different* package versions on different
  interpreters — 3.8 backtracks to the last release that supported it, with no warning.
- `.python-version` records the interpreter that `requirements.txt` was resolved against.
  It is read automatically by `pyenv` and `uv`.
- `requirements.txt` = hand-maintained direct dependencies.
  `requirements.lock.txt` = full `pip freeze`, for exact reproduction. Regenerate with
  `python -m pip freeze > requirements.lock.txt` after changing the former.
- Venvs are gitignored (`.venv/` matches at any depth).

### Jupyter kernels

| Kernel | Points at |
|---|---|
| `Python 3.11 (embeddedSys)` | root `.venv` |
| `Python 3.8 (TF-Arduino)` | `TinyML_SC4172/.venv` |
