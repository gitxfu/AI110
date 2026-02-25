# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

Two-file structure:

- **`playlist_logic.py`** — All pure logic with no UI dependencies: song normalization, mood classification, playlist building/merging, search, stats, lucky pick, history summary. The `Song` and `PlaylistMap` types are defined here.
- **`app.py`** — Streamlit UI layer. Imports everything from `playlist_logic`. Manages session state (`songs`, `profile`, `history`). Calls `build_playlists` → `merge_playlists` on every render, then passes the result to the playlist tabs, lucky pick, and stats sections.

The profile dict (keyed by `hype_min_energy`, `chill_max_energy`, `favorite_genre`, `include_mixed`) drives classification in `classify_song`. Songs flow: raw dict → `normalize_song` → `classify_song` → placed into `Hype`, `Chill`, or `Mixed` bucket.

## Intended Behavior

Use these rules as the benchmark for how the app should function correctly:

**Song Classification:**
- `Hype`: energy >= `hype_min_energy` (default 7), OR genre matches `favorite_genre`, OR genre contains a hype keyword (`rock`, `punk`, `party`).
- `Chill`: energy <= `chill_max_energy` (default 3), OR title contains a chill keyword (`lofi`, `ambient`, `sleep`).
- `Mixed`: anything that doesn't meet Hype or Chill criteria.

**Search:** Case-insensitive partial match — query must be contained within the field value (e.g., searching `"AC"` should match `"AC/DC"`).

**Stats:**
- `total_songs`: unique count of all songs across all buckets.
- `avg_energy`: mean energy of **all** songs (not just one bucket).
- `hype_ratio`: `len(Hype) / total_songs`.

**Lucky Pick:** `hype`/`chill` mode picks only from that bucket. `any` picks from the combined pool of Hype + Chill + Mixed.

**Normalization:** Titles are stripped of whitespace; artists and genres are lowercased and stripped.

## Known Bugs (intentionally seeded)

These are the confirmed bugs present in the starter code — all are in `playlist_logic.py`:

| Location | Bug | Fix |
|---|---|---|
| `compute_playlist_stats` L119 | `total = len(hype)` — uses only Hype count, so `hype_ratio` divides by wrong denominator | Change to `total = len(all_songs)` |
| `compute_playlist_stats` L124 | `sum(... for song in hype)` — avg energy only sums Hype songs instead of all songs | Change `hype` to `all_songs` |
| `search_songs` L172 | `if value and value in q` — condition is inverted; checks if the field is a substring of the query, not the other way around | Change to `if q in value` |
| `random_choice_or_none` L196 | `random.choice(songs)` crashes with `IndexError` when `songs` is empty; never returns `None` | Guard with `if not songs: return None` |
| `lucky_pick` L187 | `any` mode combines only Hype + Chill, excluding Mixed | Append `playlists.get("Mixed", [])` to the pool |
