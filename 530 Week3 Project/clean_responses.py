import csv
from pathlib import Path

INPUT_CSV = Path("responses.csv")
OUTPUT_CSV = Path("responses_cleaned.csv")


def is_name_empty(name) -> bool:
    """True if name is missing or only whitespace."""
    if name is None:
        return True
    return str(name).strip() == ""


with open(INPUT_CSV, newline="", encoding="utf-8") as infile, open(
    OUTPUT_CSV, "w", newline="", encoding="utf-8"
) as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    if not fieldnames:
        raise ValueError(f"{INPUT_CSV} has no header row.")

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        if is_name_empty(row.get("name")):
            continue
        role = row.get("role")
        if role is not None:
            row["role"] = str(role).upper()
        writer.writerow(row)
