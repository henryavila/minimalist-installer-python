# minimalist-installer (Python)

Python variation of [`@henryavila/minimalist-installer`](https://github.com/henryavila/minimalist-installer): a reversible, **userland** installer engine for CLI tools and AI agent skills.

The Node package remains in the original repository. This repository is the **Python** distribution (`import minimalist_installer`, console script `minimalist-installer`).

## Install

```bash
python3 -m pip install \
  "minimalist-installer @ git+https://github.com/henryavila/minimalist-installer-python.git@main"
```

Editable (clone):

```bash
git clone git@github.com:henryavila/minimalist-installer-python.git
cd minimalist-installer-python
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev,tui]"
```

## Quick use

```bash
minimalist-installer detect --json
minimalist-installer install path/to/distribution.toml --yes --hosts grok,codex
```

```python
from pathlib import Path
from minimalist_installer import define_installer
from minimalist_installer.providers import FileSetProvider

installer = define_installer(
    config={"consumer": "demo", "consumer_version": "0.1.0"},
    providers=[FileSetProvider()],
)
installer.install(base_path=Path.home() / "tmp-install-root")
```

## Layout

- `src/minimalist_installer/` — core, effects, providers, skills, optional TUI
- `spec/` — shared conformance vectors and JSON schemas
- `tests/` — pytest suite

## Interactive TUI (`[tui]`)

Install with the optional extra:

```bash
python3 -m pip install \
  "minimalist-installer[tui] @ git+https://github.com/henryavila/minimalist-installer-python.git@main"
```

Interactive install (TTY required; cancels before confirm leave no transaction):

```bash
minimalist-installer install path/to/distribution.toml
```

The flow mirrors Atomic Skills (`@clack/prompts`):

```text
intro/version
  → scope (user | project)
  → detected hosts + evidence
  → host multiselect (preselect by confidence)
  → language (en | pt)
  → planned files / conflicts
  → confirm → progress → per-host summary
```

Presentation:

| Layer | Role |
|---|---|
| Rich | Intro, evidence, plan listing, spinner, summary |
| Questionary | Select, checkbox, confirm |

Questionary’s stock styles leave the active row nearly invisible. This package
applies a clack-like chrome in `tui/prompt_style.py`: cyan focused row + `❯`
pointer, green checked items, `◆` question mark, and short navigation hints.
`NO_COLOR` and non-Unicode terminals fall back to bold/ASCII glyphs (`>` / `*`).

Consumers (for example lacuna-signer `skill setup --menu`) call the same
`run_install_flow` + `create_questionary_prompts` path — they do not ship a
separate menu UI.

## Development

```bash
.venv/bin/pytest -q
.venv/bin/python -m build
```

## Related

- Node engine: https://github.com/henryavila/minimalist-installer
- Atomic Skills TUI reference: `@clack/prompts` in `atomic-skills` `src/ui.js`
- Design/plan: `docs/plans/2026-09-10-python-port*.md`

## Platform support

Linux and macOS are exercised in CI. Windows currently **fails closed** for filesystem mutations (no safe no-follow backend yet); detection/planning APIs still import.
