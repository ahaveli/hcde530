import csv

# Below: reusable helpers to load a CSV, normalize messy text fields, save outputs,
# and compute the same summary numbers for both a sentence and a small summary CSV.

def load_survey_rows_from_csv(filepath):
    """Read a survey CSV and return all rows as a list of dicts.

    Each dict maps column names to values (all strings), matching csv.DictReader.
    The file must be UTF-8 encoded and use a header row.
    """
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def clean_survey_row(row):
    """Return a new dict with stripped fields and title-cased role, department, and tool."""
    cleaned = {}
    for key, value in row.items():
        s = value.strip() if value else ""
        if key in ("role", "department", "primary_tool"):
            s = s.title()  # e.g. "ux researcher" and "UX Researcher" become one label
        cleaned[key] = s
    return cleaned


def write_survey_rows_to_csv(rows, filepath, fieldnames=None):
    """Write survey rows to a new CSV at filepath using UTF-8 and a header row.

    Column order matches fieldnames, or the keys of the first row if fieldnames is omitted.
    """
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _collect_summary_metrics(rows):
    """Return row count, ordered unique role labels (empty role labeled), and empty name count."""
    n = len(rows)
    unique_raw = {row["role"] for row in rows}
    # List real roles first, then blank roles, so the plain-language list reads clearly.
    unique_role_labels = [
        r if r else "blank (empty string)"
        for r in sorted(unique_raw, key=lambda s: (not s, s or ""))
    ]
    empty_name_count = sum(1 for row in rows if not row["participant_name"])
    return n, unique_role_labels, empty_name_count


def summarize_data(rows):
    """Return a short plain-language summary of cleaned survey rows (list of dicts).

    Includes total row count, the distinct values found in the role column, and
    how many rows have a blank participant_name (the name field in this dataset).
    """
    n, unique_role_labels, empty_name_count = _collect_summary_metrics(rows)
    roles_text = ", ".join(unique_role_labels) if unique_role_labels else "none"
    return (
        f"The dataset has {n} row(s). "
        f"Unique values in the role column: {roles_text}. "
        f"Number of empty name fields: {empty_name_count}."
    )


def write_summary_to_csv(rows, filepath):
    """Write summary metrics to a two-column CSV: metric, value.

    One row each for row_count and empty_name_field_count; one row per unique
    role value (metric is always unique_role).
    """
    n, unique_role_labels, empty_name_count = _collect_summary_metrics(rows)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["row_count", n])
        w.writerow(["empty_name_field_count", empty_name_count])
        for label in unique_role_labels:
            w.writerow(["unique_role", label])


# --- Ingest: read the raw file, then apply cleaning so all stats use the same values ---
filename = "week3_survey_messy.csv"
rows = load_survey_rows_from_csv(filename)
rows = [clean_survey_row(r) for r in rows]

# --- Export: save the cleaned rows and a small metrics table for use outside this script ---
cleaned_path = "week3_survey_cleaned.csv"
write_survey_rows_to_csv(rows, cleaned_path)
print(f"Wrote cleaned data to {cleaned_path}\n")
summary_path = "week3_survey_summary.csv"
write_summary_to_csv(rows, summary_path)
print(f"Wrote summary to {summary_path}\n")
print(summarize_data(rows))
print()

# --- Console analysis: same dataset as the exports, printed for a quick read ---
# Tally how many people picked each job role.
role_counts = {}

for row in rows:
    role = row["role"]
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# Average self-reported years in the field (one number per response row).
total_experience = 0
for row in rows:
    total_experience += int(row["experience_years"])

avg_experience = total_experience / len(rows)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Highest satisfaction (1-5), skipping any row that left the score blank.
scored_rows = []
for row in rows:
    if row["satisfaction_score"]:
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")
