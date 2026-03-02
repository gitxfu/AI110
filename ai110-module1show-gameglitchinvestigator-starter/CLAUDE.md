# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py

# Run tests (requires logic_utils.py to be implemented first)
pytest tests/test_game_logic.py
```

## Architecture

- **`app.py`** — Streamlit UI and all game logic in one file. Session state keys: `secret`, `attempts`, `score`, `status`, `history`. The four logic functions are defined here but need to be moved to `logic_utils.py`.
- **`logic_utils.py`** — Stub file. Students refactor the four functions here: `get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`. The test suite imports from this file.

The goal is to make the tests pass by (1) fixing the bugs and (2) moving the corrected functions into `logic_utils.py`.

## Intended Behavior

- `get_range_for_difficulty`: Easy → `(1, 20)`, Normal → `(1, 100)`, Hard → `(1, 50)`
- `parse_guess`: returns `(ok, int_or_None, error_or_None)`; accepts decimals by truncating, rejects non-numeric input
- `check_guess(guess, secret)`: returns `("Win", msg)`, `("Too High", msg)`, or `("Too Low", msg)`
- `update_score`: Win awards `max(10, 100 - 10 * (attempt + 1))` points; wrong guesses adjust by ±5

## Test Contract

`tests/test_game_logic.py` expects `check_guess` to return only the outcome string (e.g., `"Win"`), not the full tuple. When refactoring into `logic_utils.py`, adjust the return signature to match what the tests assert, or update the tests to unpack the tuple.
