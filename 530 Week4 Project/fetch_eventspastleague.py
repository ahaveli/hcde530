#!/usr/bin/env python3
"""
Fetch past league events from TheSportsDB (API key in URL path), keep up to 100 event rows, write CSV.
If the API returns fewer than 100 events, the file contains only what was returned (raw slice, no padding).

Endpoint: https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4387
Run:  python3 fetch_eventspastleague.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import requests

API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4387"
MAX_ROWS = 100
OUT_CSV = Path(__file__).resolve().parent / "thesportsdb_eventspast_league_100.csv"
TIMEOUT_SEC = 60


def _cell(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def main() -> None:
    try:
        r = requests.get(API_URL, timeout=TIMEOUT_SEC, headers={"Accept": "application/json"})
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        raise SystemExit(1) from e

    try:
        payload = r.json()
    except json.JSONDecodeError as e:
        print("Response was not valid JSON.", file=sys.stderr)
        raise SystemExit(1) from e

    events = payload.get("events")
    if not isinstance(events, list):
        print("JSON has no `events` list.", file=sys.stderr)
        raise SystemExit(1)

    rows = [e for e in events[:MAX_ROWS] if isinstance(e, dict)]
    if not rows:
        print("No event objects to write.", file=sys.stderr)
        raise SystemExit(1)

    fieldnames = sorted({k for row in rows for k in row.keys()})

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: _cell(row.get(k)) for k in fieldnames})

    print(f"Wrote {len(rows)} row(s) to {OUT_CSV.name}")
    print(f"Source: {API_URL}")


if __name__ == "__main__":
    main()
