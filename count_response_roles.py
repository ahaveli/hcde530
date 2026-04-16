"""Load responses.csv and print how many times each role appears (case-insensitive)."""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "responses.csv"


def main() -> None:
    # key = casefolded role for grouping; value = count
    counts: dict[str, int] = {}
    # first-seen spelling after strip (per key) for display
    labels: dict[str, str] = {}

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = row.get("role")
            if raw is None:
                continue
            role = raw.strip()
            if not role:
                continue
            key = role.casefold()
            if key not in labels:
                labels[key] = role
            counts[key] = counts.get(key, 0) + 1

    # highest count first; ties alphabetical by display label
    ranked = sorted(
        counts.items(),
        key=lambda item: (-item[1], labels[item[0]].casefold()),
    )

    print(f"{'Role':<28} {'Count':>6}")
    print("-" * 36)
    for key, n in ranked:
        print(f"{labels[key]:<28} {n:>6}")

    print()
    print(f"  Rows with a role : {sum(counts.values())}")
    print(f"  Distinct roles   : {len(counts)}")


if __name__ == "__main__":
    main()
