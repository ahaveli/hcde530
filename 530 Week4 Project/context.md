# Week 4 — context for this folder

Use this as a **quick map** for humans and tools working in `530 Week4 Project`.

## What lives here
- **Course / API practice:** HTTP JSON APIs, CSV read/write, environment-based API keys.
- **Not a full web app** — small CLI-style Python scripts.

## Files (current)
- `fetch_reviews.py` — HCDE Week 4 review API on Render; filters `helpful_votes`; output CSV separate from the original full export.
- `seattle_weather.py` — OpenWeather current weather for Seattle; loads `OPENWEATHERMAP_API_KEY` from `.env` in this directory.
- `sports_scores.py` — TheSportsDB `eventspastleague` for league id in `API_URL`; prints games and writes `sports_scores_results.csv`.
- `requirements.txt` — e.g. `requests` for `sports_scores.py`.
- `reviews_category_helpful_votes.csv` — full reviews dataset (original).
- `sports_scores_results.csv` — **generated**; safe to delete or ignore in version control if you prefer.
- `.env` — local secrets (`OPENWEATHERMAP_API_KEY`, `SPORTS_DATA_API_KEY`, etc.); **not** for git.

## Conventions
- Run scripts with `python3` from this directory.
- For new keys: one `.env` in this folder; use clear `UPPER_SNAKE` names.
- TheSportsDB public URL pattern: `https://www.thesportsdb.com/api/v1/json/{key}/...`

## Pointers
- `week4.md` — short overview and run commands.
- `.cursorrules` — editor/agent behavior for this project folder.
