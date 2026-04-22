import csv


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
            s = s.title()
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


# Load the survey data from a CSV file
filename = "week3_survey_messy.csv"
rows = load_survey_rows_from_csv(filename)
rows = [clean_survey_row(r) for r in rows]
cleaned_path = "week3_survey_cleaned.csv"
write_survey_rows_to_csv(rows, cleaned_path)
print(f"Wrote cleaned data to {cleaned_path}\n")

# Count responses by role
# Normalize role names so "ux researcher" and "UX Researcher" are counted together
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

# Calculate the average years of experience
total_experience = 0
for row in rows:
    total_experience += int(row["experience_years"])

avg_experience = total_experience / len(rows)
print(f"\nAverage years of experience: {avg_experience:.1f}")

# Find the top 5 highest satisfaction scores
scored_rows = []
for row in rows:
    if row["satisfaction_score"]:
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")
