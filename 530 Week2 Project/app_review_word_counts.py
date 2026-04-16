"""Load fictional app reviews from CSV and summarize word counts per review."""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "app_reviews.csv"


def word_count(text: str) -> int:
    """Words = split on whitespace (same idea as demo_word_count.py)."""
    return len(text.split())


def main() -> None:
    reviews: list[tuple[str, str]] = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            reviews.append((row["review_id"], row["review"]))

    counts: list[int] = []
    print(f"{'ID':<6} {'Words':<6} Review (first 70 chars)")
    print("-" * 90)

    for rid, text in reviews:
        n = word_count(text)
        counts.append(n)
        preview = text if len(text) <= 70 else text[:70] + "..."
        print(f"{rid:<6} {n:<6} {preview}")

    total = len(counts)
    shortest = min(counts)
    longest = max(counts)
    average = sum(counts) / total

    print()
    print("── Summary ─────────────────────────────────")
    print(f"  Reviews         : {total}")
    print(f"  Shortest review : {shortest} words")
    print(f"  Longest review  : {longest} words")
    print(f"  Average length  : {average:.1f} words")


if __name__ == "__main__":
    main()
