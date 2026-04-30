#!/usr/bin/env python3
"""
Fetch past games for a league from TheSportsDB (eventspastleague) — NBA
per the provided league id 4387. Prints to the terminal and saves a CSV next to this script.
Run:  python sports_scores.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping

import requests

# ---------------------------------------------------------------------------
# Endpoint: API key in path; league id 4387 (assignment URL for NBA past events)
# ---------------------------------------------------------------------------
API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4387"
TIMEOUT_SEC = 45
HEADERS = {
    "User-Agent": "sports_scores.py (TheSportsDB / Python 3)",
    "Accept": "application/json",
}
# CSV written beside this file (overwritten on each run)
OUTPUT_CSV = Path(__file__).resolve().parent / "sports_scores_results.csv"
CSV_FIELDNAMES = (
    "event_name",
    "home_team",
    "away_team",
    "home_score",
    "away_score",
    "event_date",
)


# ---------------------------------------------------------------------------
# HTTP: single GET with clear errors
# ---------------------------------------------------------------------------


def fetch_json_text() -> str:
    """Return response body as text. Raises on network/HTTP failure."""
    response = requests.get(API_URL, timeout=TIMEOUT_SEC, headers=HEADERS)
    response.raise_for_status()
    return response.text


# ---------------------------------------------------------------------------
# JSON: parse and pull the events list
# ---------------------------------------------------------------------------


def parse_json(text: str) -> Any:
    """Parse JSON; json.loads raises json.JSONDecodeError on bad input."""
    return json.loads(text)


def extract_events(payload: Any) -> list[Mapping[str, Any]]:
    """Return list of event dicts, or empty list if missing/invalid."""
    if not isinstance(payload, dict):
        return []
    events = payload.get("events")
    if events is None:
        return []
    if not isinstance(events, list):
        return []
    return [e for e in events if isinstance(e, dict)]


# ---------------------------------------------------------------------------
# Field helpers: null-safe display strings
# ---------------------------------------------------------------------------


def _text(value: Any, placeholder: str = "—") -> str:
    if value is None:
        return placeholder
    s = str(value).strip()
    return s if s else placeholder


def format_event_for_print(event: Mapping[str, Any]) -> dict[str, str]:
    """Map API fields to the labels we print; never KeyError on missing keys."""
    return {
        "event_name": _text(event.get("strEvent")),
        "home_team": _text(event.get("strHomeTeam")),
        "away_team": _text(event.get("strAwayTeam")),
        "home_score": _text(event.get("intHomeScore")),
        "away_score": _text(event.get("intAwayScore")),
        "event_date": _text(
            event.get("dateEvent")
            or event.get("dateEventLocal")
            or event.get("strTimestamp")
        ),
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def print_events(rows: list[Mapping[str, Any]]) -> None:
    if not rows:
        print("No events in this response (empty or null `events` list).")
        return
    print(f"League past events: {len(rows)} game(s)\n")
    for i, event in enumerate(rows, start=1):
        f = format_event_for_print(event)
        print(f"--- Game {i} ---")
        print(f"  Event name:  {f['event_name']}")
        print(f"  Home team:   {f['home_team']}")
        print(f"  Away team:   {f['away_team']}")
        print(f"  Home score:  {f['home_score']}")
        print(f"  Away score:  {f['away_score']}")
        print(f"  Event date:  {f['event_date']}")
        print()


def write_events_csv(
    rows: list[Mapping[str, Any]], csv_path: Path, fieldnames: tuple[str, ...]
) -> None:
    """Write all rows to UTF-8 CSV (header + one line per event). Overwrites the file."""
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for event in rows:
            if not isinstance(event, dict):
                continue
            writer.writerow(format_event_for_print(event))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> None:
    try:
        text = fetch_json_text()
    except requests.Timeout:
        print("Error: request timed out.", file=sys.stderr)
        raise SystemExit(1)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        if e.response is not None:
            print(f"  Status: {e.response.status_code}", file=sys.stderr)
        raise SystemExit(1)
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        raise SystemExit(1)

    try:
        payload = parse_json(text)
    except json.JSONDecodeError as e:
        print("Invalid JSON from server. First 300 characters:", file=sys.stderr)
        print(repr(text[:300]), file=sys.stderr)
        print(f"Parse error: {e}", file=sys.stderr)
        raise SystemExit(1)

    events = extract_events(payload)
    print(f"Source: {API_URL}\n")
    print_events(events)

    try:
        write_events_csv(events, OUTPUT_CSV, CSV_FIELDNAMES)
    except OSError as e:
        print(f"Could not write CSV to {OUTPUT_CSV}: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    print(f"Saved: {OUTPUT_CSV} ({len(events)} row(s), UTF-8)")


if __name__ == "__main__":
    main()
