"""HCDE 530 Week 4: call the API, keep reviews with 30+ upvotes, save to a dedicated CSV.

Steps implemented:
  1) GET https://hcde530-week4-api.onrender.com/ (API info).
  2) GET /reviews and keep rows with helpful_votes >= 30 (upvotes in the API JSON).
  3) Write results to a new CSV (category + helpful_votes columns).

This script does not read or write reviews_category_helpful_votes.csv; that file stays as your original full export.
"""

import csv
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://hcde530-week4-api.onrender.com"
ROOT_PATH = "/"
REVIEWS_PATH = "/reviews"
PAGE_SIZE = 200
MIN_UPVOTES = 30
# Original full export (all reviews) — never opened for writing by this script.
ORIGINAL_CSV = Path(__file__).resolve().parent / "reviews_category_helpful_votes.csv"
# New file for 30+ upvotes only; created/overwritten on each run.
NEW_CSV = Path(__file__).resolve().parent / "reviews_30plus_upvotes.csv"


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_api_root() -> dict:
    """GET the API root (metadata)."""
    return _get_json(f"{BASE_URL}{ROOT_PATH}")


def fetch_reviews_page(limit: int, offset: int) -> dict:
    """GET /reviews with query params; return parsed JSON dict."""
    params = urllib.parse.urlencode({"limit": limit, "offset": offset})
    url = f"{BASE_URL}{REVIEWS_PATH}?{params}"
    return _get_json(url)


def fetch_all_reviews() -> list[dict]:
    """Follow pagination until all reviews are loaded."""
    all_reviews: list[dict] = []
    offset = 0
    while True:
        data = fetch_reviews_page(PAGE_SIZE, offset)
        batch = data.get("reviews", [])
        if not batch:
            break
        all_reviews.extend(batch)
        offset += len(batch)
        if offset >= data.get("total", offset):
            break
    return all_reviews


def main() -> None:
    # 1) Call the API base URL
    try:
        root = fetch_api_root()
    except urllib.error.URLError as e:
        print(f"Request failed: {e}")
        raise SystemExit(1) from e

    print(
        f"API: {root.get('name', '')} — {root.get('description', '')} "
        f"({root.get('total_reviews', '?')} reviews listed)\n"
    )

    # 2) Load reviews, then keep only 30+ upvotes (field name: helpful_votes)
    print(f"Requesting review data from {BASE_URL}{REVIEWS_PATH} …")
    try:
        reviews = fetch_all_reviews()
    except urllib.error.URLError as e:
        print(f"Request failed: {e}")
        raise SystemExit(1) from e

    filtered = [r for r in reviews if r.get("helpful_votes", 0) >= MIN_UPVOTES]
    print(
        f"Keeping {len(filtered)}/{len(reviews)} with {MIN_UPVOTES}+ upvotes — "
        "the API field is helpful_votes.\n"
    )

    rows: list[dict[str, str | int]] = []
    for r in filtered:
        category = r.get("category", "")
        helpful = r.get("helpful_votes", 0)
        print(f"Category: {category!r}  |  Helpful votes: {helpful}")
        rows.append({"category": category, "helpful_votes": helpful})

    # 3) Save only to the new CSV (do not touch ORIGINAL_CSV)
    if NEW_CSV.resolve() == ORIGINAL_CSV.resolve():
        raise ValueError("NEW_CSV must be a different file than the original full export.")
    with open(NEW_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "helpful_votes"])
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"\nWrote {len(rows)} row(s) to {NEW_CSV.name!r} "
        f"({ORIGINAL_CSV.name!r} was not modified)."
    )


if __name__ == "__main__":
    main()
