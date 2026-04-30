#!/usr/bin/env python3
"""
Country State City API — list all countries, or export a filtered CSV.

Docs: https://docs.countrystatecity.in/api/introduction
Key in .env: COUNTRY_STATE_CITY_API_KEY

Run:
  python3 country_state_city.py                    # print all countries
  python3 country_state_city.py --export-a-d     # write countries_A_to_D.csv
  python3 country_state_city.py --export-all     # write countries_all.csv (every country)
  # You can pass both flags to fetch once and write both CSVs.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

import requests

BASE_URL = "https://api.countrystatecity.in/v1"
COUNTRIES_PATH = "/countries"
ENV_KEY = "COUNTRY_STATE_CITY_API_KEY"
REQUEST_TIMEOUT_SEC = 60
_ENV_PATH = Path(__file__).resolve().parent / ".env"
OUTPUT_A_TO_D_CSV = _ENV_PATH.parent / "countries_A_to_D.csv"
OUTPUT_ALL_CSV = _ENV_PATH.parent / "countries_all.csv"
CSV_FIELDNAMES = ("name", "capital", "currency")
FIRST_LETTERS_AD = frozenset("ABCD")


def load_env_file() -> None:
    """Load KEY=value pairs from .env into os.environ (does not override existing env)."""
    if not _ENV_PATH.is_file():
        return
    for raw in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not key or key in os.environ:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in '\'"':
            value = value[1:-1]
        os.environ[key] = value


def get_api_key() -> str:
    """Return the CSC API key from the environment."""
    key = (os.environ.get(ENV_KEY) or "").strip()
    if not key:
        print(
            f"Missing {ENV_KEY}. Add it to {_ENV_PATH.name} in this folder.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return key


def csc_headers(api_key: str) -> dict[str, str]:
    """Headers required by the Country State City API."""
    return {
        "X-CSCAPI-KEY": api_key,
        "Accept": "application/json",
    }


def fetch_countries(api_key: str) -> list[dict[str, Any]]:
    """
    GET /v1/countries — returns a JSON array of country objects.

    Raises SystemExit on HTTP errors, timeouts, or invalid JSON.
    """
    url = f"{BASE_URL}{COUNTRIES_PATH}"
    try:
        response = requests.get(
            url,
            headers=csc_headers(api_key),
            timeout=REQUEST_TIMEOUT_SEC,
        )
    except requests.Timeout:
        print("Request timed out. Try again or increase REQUEST_TIMEOUT_SEC.", file=sys.stderr)
        raise SystemExit(1)
    except requests.ConnectionError as e:
        print(f"Connection failed (network/DNS): {e}", file=sys.stderr)
        raise SystemExit(1) from e
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        raise SystemExit(1) from e

    if response.status_code == 401:
        print("HTTP 401 Unauthorized — invalid or missing API key (check X-CSCAPI-KEY).", file=sys.stderr)
        raise SystemExit(1)
    if response.status_code == 429:
        print("HTTP 429 Too Many Requests — rate limit; try again later.", file=sys.stderr)
        raise SystemExit(1)
    if not response.ok:
        body = (response.text or "")[:500]
        print(f"HTTP {response.status_code} from API.", file=sys.stderr)
        if body:
            print(body, file=sys.stderr)
        raise SystemExit(1)

    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print("Response was not valid JSON.", file=sys.stderr)
        print(repr(response.text[:300]), file=sys.stderr)
        raise SystemExit(1) from e

    if not isinstance(data, list):
        print("Expected a JSON array of countries.", file=sys.stderr)
        raise SystemExit(1)

    return [c for c in data if isinstance(c, dict)]


def print_country_list(countries: list[dict[str, Any]]) -> None:
    """Print a readable line per country using common field names from the API."""
    if not countries:
        print("No countries returned.")
        return
    print(f"Countries ({len(countries)}):\n")
    for c in countries:
        name = c.get("name") or c.get("Name") or "—"
        iso2 = c.get("iso2") or c.get("isoCode") or "—"
        iso3 = c.get("iso3") or "—"
        print(f"  {iso2} / {iso3} — {name}")


def _safe_str(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def filter_countries_name_starts_a_to_d(
    countries: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Rows name/capital/currency where country name starts with A–D (ASCII, case-insensitive)."""
    rows: list[dict[str, str]] = []
    for c in countries:
        name = _safe_str(c.get("name"))
        if not name:
            continue
        if name[0].upper() not in FIRST_LETTERS_AD:
            continue
        rows.append(
            {
                "name": name,
                "capital": _safe_str(c.get("capital")),
                "currency": _safe_str(c.get("currency")),
            }
        )
    rows.sort(key=lambda r: r["name"].lower())
    return rows


def write_countries_csv(rows: list[dict[str, str]], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        w.writeheader()
        w.writerows(rows)


def countries_to_rows_all(countries: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Every country as name / capital / currency (sorted by name)."""
    rows: list[dict[str, str]] = []
    for c in countries:
        name = _safe_str(c.get("name"))
        if not name:
            continue
        rows.append(
            {
                "name": name,
                "capital": _safe_str(c.get("capital")),
                "currency": _safe_str(c.get("currency")),
            }
        )
    rows.sort(key=lambda r: r["name"].lower())
    return rows


def run_export_a_to_d(api_key: str, countries: list[dict[str, Any]] | None = None) -> None:
    data = countries if countries is not None else fetch_countries(api_key)
    rows = filter_countries_name_starts_a_to_d(data)
    write_countries_csv(rows, OUTPUT_A_TO_D_CSV)
    print(f"Wrote {len(rows)} row(s) to {OUTPUT_A_TO_D_CSV.name}")


def run_export_all(api_key: str, countries: list[dict[str, Any]] | None = None) -> None:
    data = countries if countries is not None else fetch_countries(api_key)
    rows = countries_to_rows_all(data)
    write_countries_csv(rows, OUTPUT_ALL_CSV)
    print(f"Wrote {len(rows)} row(s) to {OUTPUT_ALL_CSV.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Country State City API helper.")
    parser.add_argument(
        "--export-a-d",
        action="store_true",
        help="Write countries_A_to_D.csv (name, capital, currency) for names starting A–D.",
    )
    parser.add_argument(
        "--export-all",
        action="store_true",
        help="Write countries_all.csv (name, capital, currency) for every country.",
    )
    args = parser.parse_args()

    load_env_file()
    api_key = get_api_key()

    if args.export_a_d or args.export_all:
        countries = fetch_countries(api_key)
        if args.export_a_d:
            run_export_a_to_d(api_key, countries)
        if args.export_all:
            run_export_all(api_key, countries)
    else:
        countries = fetch_countries(api_key)
        print_country_list(countries)


if __name__ == "__main__":
    main()
