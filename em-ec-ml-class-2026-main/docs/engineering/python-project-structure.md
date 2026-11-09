# Python Project Structure

A Python project is more than a set of `.py` files: it also holds the configuration needed to reproduce its environment, check its code quality, and document its usage. This note describes the typical content tree of a project managed by [uv](https://docs.astral.sh/uv/), and the role of each element.

## Principles

- The project is **reproducible**: anyone cloning the repository gets the exact same environment with a single command (`uv sync`).
- **Reusable code** lives in an installable package under `src/`, and is imported by everything else (scripts, notebooks, apps, tests). Code is never copy-pasted from one notebook to another.
- **Configuration is separated from code**: paths, hyperparameters and settings live in config files, not hard-coded in scripts.
- **Only source material is versioned**: data, models, virtual environments, caches and secrets stay out of git.
- Every tool (linter, formatter, type checker, test runner) is configured in `pyproject.toml` when possible, so the project has a single source of truth.

## Content tree

Folders first, then files, each in alphabetical order (as displayed by the VSCode explorer):

```
my-project/
├── .git/                     # git history (managed by git, never edited by hand)
├── .venv/                    # virtual environment (managed by uv, not versioned)
├── conf/                     # configuration files (yaml, toml, json)
│   └── webui.yaml
├── data/                     # local datasets (not versioned)
├── docs/                     # documentation and images
│   ├── imgs/
│   └── notes/
├── models/                   # trained models and checkpoints (not versioned)
├── notebooks/                # exploration and tutorials
│   └── 1 - Data exploration.ipynb
├── src/
│   └── my_package/           # the installable python package
│       ├── __init__.py
│       ├── __main__.py       # command line entry point
│       ├── plot.py
│       ├── train.py
│       ├── transforms.py
│       └── webui.py
├── tests/                    # unit tests of the package
│   └── test_transforms.py
├── .gitignore                # files and folders excluded from git
├── .pre-commit-config.yaml   # checks run automatically before each commit
├── .python-version           # python version used by the project
├── pyproject.toml            # project metadata, dependencies and tools configuration
├── README.md                 # entry point documentation
└── uv.lock                   # exact resolved versions of all dependencies
```

Not every project needs every folder, and names may vary (`scripts/`, `configs/`, `artifacts/`...), but the separation of roles stays the same.

## Folders

### `.venv/`

The virtual environment created by `uv sync`: an isolated python interpreter with the project dependencies installed. It is specific to each machine and can be deleted and recreated at any time, hence it is never versioned. Commands are run inside it with `uv run`:

```bash
uv sync                           # create / update .venv from uv.lock
uv run python -m my_package       # run the package within the environment
uv run pytest                     # run a tool within the environment
```

### `conf/`

Configuration files (often YAML) holding everything that may change between runs or environments: file paths, hyperparameters, app settings. Scripts read them at startup instead of hard-coding values. Secrets (passwords, API keys) do not belong here but in a non-versioned `.env` file or environment variables.

### `data/` and `models/`

Local storage for datasets and trained models. They are excluded from git because they are heavy and may be sensitive; the `README.md` explains how to obtain or regenerate them (download link, training command). In larger projects they are stored on a dedicated storage (cloud bucket, model registry) and possibly tracked with a tool like [DVC](https://dvc.org/).

### `docs/`

Documentation that does not fit in the README: notes, guidelines, design diagrams, and the images (`docs/imgs/`) they reference.

### `notebooks/`

Jupyter notebooks used for exploration, experiments and tutorials. They import functions from the package instead of defining them, so that any useful code ends up in `src/` where it is tested and reused. Prefixing them with a number keeps them in reading order.

### `src/` - the package

All reusable code lives in a package located in `src/<package_name>/` (the so-called *src layout*). The `__init__.py` file marks the folder as a package, and may expose its main functions. Modules are split by responsibility (`explain.py`, `plot.py`, `transforms.py`...).

Placing the package under `src/` rather than at the root forces it to be installed (which `uv sync` does) before being imported, avoiding accidental imports of local files and ensuring the code behaves the same in notebooks, scripts and tests.

#### Entry points

An entry point is the code that *uses* the package to do something concrete: launch a web app, train a model, run a batch inference. Like the rest of the code, entry points live inside the package, so they are linted and type-checked, ship with the package, and import its other modules the usual way (`from my_package.transforms import ...`).

They are split in two layers:

- **Task modules** (`webui.py`, `train.py`...) each expose a plain python function doing one task, e.g. `run_webui(config_path)`. They know nothing about the command line, so they can just as well be called from a notebook or a test.
- **`__main__.py`** is the single command line interface of the package. It maps command names to task functions, and holds no logic itself.

`__main__.py` is the module Python runs when the *package* is executed with `-m`: `python -m my_package` runs `my_package/__main__.py`. It is written with a command line library, here [Fire](https://github.com/google/python-fire), which turns python functions into commands, and their parameters into command line arguments, without any extra declaration:

```python
# src/my_package/__main__.py
from fire import Fire

from my_package.train import run_training
from my_package.webui import run_webui


def main():
    Fire(
        {
            "train": run_training,
            "webui": run_webui,
        }
    )


if __name__ == "__main__":
    main()
```

The `if __name__ == "__main__":` guard is required: `python -m` runs the module as the main program, and the guard is what calls `main()` in that case, while a plain `import my_package.__main__` does nothing.

Each task is then a sub-command of the package, its function parameters being passed as arguments:

```bash
uv run python -m my_package webui --config_path conf/webui.yaml
uv run python -m my_package train --config_path conf/train.yaml --n_estimators 200
uv run python -m my_package webui --help                # list the arguments of a command
```

Adding a new task only means writing its function in a module and adding one line in the dictionary of `__main__.py`.

The package can also be exposed as a shell command, by declaring `main` in `pyproject.toml`:

```toml
[project.scripts]
my-package = "my_package.__main__:main"
```

After `uv sync`, `uv run my-package webui --config_path conf/webui.yaml` is equivalent to the `python -m` form.

Fire is not the only option: [Typer](https://typer.tiangolo.com/) and [Click](https://click.palletsprojects.com/) give more control over help messages and argument validation through type hints and decorators, and `argparse` from the standard library requires no dependency. Fire is the most concise one, as task functions need no modification to become commands.

Entry points stay **thin**: they read the configuration and call functions of the package, but the actual work (preprocessing, training, prediction) is implemented in the other modules, where it can be reused and tested.

### `tests/`

Unit tests of the package, usually written with [pytest](https://docs.pytest.org/). Files and functions are prefixed with `test_` so pytest discovers them automatically. Its structure often mirrors the one of `src/`.

## Root files

### `.gitignore`

Lists the paths git should ignore. A typical python project excludes:

- environment and caches: `.venv/`, `__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.ipynb_checkpoints/`
- build outputs: `build/`, `dist/`, `*.egg-info/`
- heavy or generated artifacts: `data/`, `models/`, `checkpoints/`
- secrets and local settings: `.env`, `.vscode/`

A sub-folder may hold its own `.gitignore` for local rules (e.g. `notebooks/.gitignore`).

### `.pre-commit-config.yaml`

Declares the hooks run by [pre-commit](https://pre-commit.com/) before each commit. If a hook fails, the commit is aborted until the issue is fixed. Common hooks:

- `check-added-large-files`: prevent committing large files (datasets, models)
- `gitleaks`, `detect-private-key`: prevent committing secrets
- `mypy`: check type annotations
- `nbstripout`: remove outputs from notebooks, to keep diffs readable and the repository light
- `ruff-check`, `ruff-format`: lint and format the code

Hooks are installed once per clone with `uv run pre-commit install`, and can be run manually on all files with `uv run pre-commit run --all-files`.

### `.python-version`

Contains a single line, e.g. `3.12`. uv reads it to download and use the corresponding python interpreter, so the project does not depend on the python installed on the machine.

### `pyproject.toml`

The central file of the project, standardized by [PEP 621](https://peps.python.org/pep-0621/). It declares:

- **`[dependency-groups]`**: dependencies only needed for development (`jupyter`, `mypy`, `pre-commit`, `pytest`, `ruff`...), which are not installed by users of the package.
- **`[project]`**: name, version, description, authors, supported python versions (`requires-python`) and runtime `dependencies`.
- **`[tool.<name>]`**: configuration of each development tool (`[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.ruff]`...).
- **`[tool.uv]`**: uv settings, e.g. `package = true` to install the project itself in the environment, making `import my_package` work from anywhere.

Dependencies are added and removed with uv rather than by editing the file by hand:

```bash
uv add pandas              # runtime dependency
uv add --dev pytest        # development dependency
uv remove pandas
```

### `README.md`

The first file read by anyone opening the repository. It explains what the project does, its prerequisites, how to install it (`uv sync`) and how to use it (main commands, entry points).

### `uv.lock`

Generated by uv from `pyproject.toml`, it records the **exact version** (and hash) of every dependency, including transitive ones. While `pyproject.toml` states constraints (`pandas>=2.0`), the lock file pins the solution (`pandas==2.2.3`), ensuring every machine installs the same packages.

It is versioned, but never edited by hand: uv updates it on `uv add`, `uv remove`, `uv lock` or `uv sync`.

## Getting started on an existing project

```bash
git clone <repository-url>
cd my-project
uv sync                          # install python and all dependencies
uv run pre-commit install        # activate the commit hooks
uv run python -m my_package webui --config_path conf/webui.yaml   # run the project
```
