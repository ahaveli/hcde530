# Project context — HCDE 530 Week 3

This file maps **what each part of this folder is for**. It is written for **you**, **graders**, and **anyone opening the project later**—especially if they are HCD practitioners, not software engineers.

---

## Goals (what “success” looks like)

- **Load and clean** structured survey data from CSV: strip text, align labels (e.g. title case for role/department/tool), and use the **same** cleaned rows for file exports and printed summaries.
- **Write outputs** other tools can open: a full cleaned table and a small two-column **metrics** CSV.
- **Analyze in the console**: counts by role, numeric summaries (e.g. average experience), and ranked lists (e.g. top satisfaction scores), with clear labels.
- Keep a **clear pipeline** in code (helpers → read → clean → write → print); favor **standard library** `csv` + UTF-8 unless the course says otherwise.

---

## Audience and takeaways

- **Primary audience:** Instructor/TAs and classmates who should see that you can **read messy tabular data**, **normalize it consistently**, and **report** both in prose-style summaries and in exported files.
- **One-sentence takeaway:** *The messy survey CSV becomes a cleaned table and a metrics file, and the same cleaned rows drive the printed role counts, averages, and top scores.*

---

## Data

- CSVs in this folder are **course / demo** material, not real participant PII. Treat them like fictional or anonymized research-style responses.
- **Survey pipeline (`week3_*.csv`):** header includes `response_id`, `participant_name`, `role`, `department`, `age_range`, `experience_years`, `satisfaction_score`, `primary_tool`, `response_text` (see `week3_survey_messy.csv` for the full header and example rows).
- **Responses pair (`responses.csv` / `responses_cleaned.csv`):** columns `name`, `role`, `response` — used by the smaller utilities; `responses_cleaned.csv` is the output of `clean_responses.py` (no blank names; roles uppercased).

---

## How to run

From the **`530 Week3 Project`** directory (so relative paths match the scripts):

1. **Week 3 survey analysis** (read messy data, write cleaned + summary, print analysis):

   ```bash
   python week3_analysis_buggy.py
   ```

   Expect writes to `week3_survey_cleaned.csv` and `week3_survey_summary.csv`, a plain-language summary line, then role tallies, average `experience_years`, and top 5 `satisfaction_score` rows (non-blank scores only).

2. **Clean the `responses` CSV** (drop blank names, uppercase roles):

   ```bash
   python clean_responses.py
   ```

   Reads `responses.csv`, writes `responses_cleaned.csv`.

3. **Count roles in `responses.csv`** (case-insensitive grouping):

   ```bash
   python count_response_roles.py
   ```

   Prints a role/count table and summary totals.

---

## File map — section → purpose

### `week3_analysis_buggy.py`

| Lines (approx.) | Purpose |
|-----------------|--------|
| 1–3 | **Intro** — script is structured as reusable helpers plus a short pipeline. |
| 6–17 | **`load_survey_rows_from_csv`** — `DictReader`, UTF-8, `newline=""` → `list[dict]`. |
| 20–28 | **`clean_survey_row`** — strip all fields; **title case** `role`, `department`, `primary_tool`. |
| 31–44 | **`write_survey_rows_to_csv`** — `DictWriter`, optional `fieldnames`, UTF-8. |
| 47–57 | **`_collect_summary_metrics`** — row count, sorted unique `role` labels (empty role labeled), empty `participant_name` count. |
| 60–72 | **`summarize_data`** — one string summarizing the metrics above. |
| 75–88 | **`write_summary_to_csv`** — two columns `metric`, `value` (`row_count`, `empty_name_field_count`, one `unique_role` per label). |
| 91–104 | **Ingest / export** — read `week3_survey_messy.csv`, clean all rows, write `week3_survey_cleaned.csv` and `week3_survey_summary.csv`, print `summarize_data`. |
| 106–140 | **Console analysis** — counts per `role`, average `experience_years`, top 5 by `satisfaction_score` (skip blank scores). |

### `week3_survey_messy.csv` / `week3_survey_cleaned.csv` / `week3_survey_summary.csv`

| File | Purpose |
|------|--------|
| `week3_survey_messy.csv` | **Input** to `week3_analysis_buggy.py` — intentionally inconsistent text (casing/spacing) to be normalized by cleaning. |
| `week3_survey_cleaned.csv` | **Output** — same logical columns as input, after `clean_survey_row`. |
| `week3_survey_summary.csv` | **Output** — `metric` / `value` rows derived from the cleaned data. |

### `clean_responses.py`

| Lines (approx.) | Purpose |
|-----------------|--------|
| 1–5 | **Paths** — `responses.csv` → `responses_cleaned.csv`. |
| 8–12 | **`is_name_empty`** — skip rows with missing/whitespace-only `name`. |
| 15–32 | **Stream** — `DictReader` / `DictWriter`, drop empty-name rows, set `role` to uppercase when present. |

### `count_response_roles.py`

| Lines (approx.) | Purpose |
|-----------------|--------|
| 1–6 | **`CSV_PATH`** — `responses.csv` next to this file (`Path(__file__).parent`). |
| 9–27 | **Tally** — strip `role`, skip blanks, group with **`casefold()`**, keep first-seen label for display. |
| 29–42 | **Print** — table sorted by count (desc), then label; footnote lines for rows-with-role and distinct roles. |
| 45–46 | **`if __name__ == "__main__"`** — run `main()`. |

### `responses.csv` / `responses_cleaned.csv`

| Part | Purpose |
|------|--------|
| `responses.csv` | Fictional-style `name` / `role` / `response` rows; input to both utilities. |
| `responses_cleaned.csv` | Output of `clean_responses.py` — no rows with empty `name`; `role` uppercased. |

### `week3.md`

| Purpose |
|--------|
| Week 3 **competency claims** (C1–C8); course reflection that ties this folder’s scripts and data to the Computational Concepts competencies (same idea as `530 Week2 Project/week2.md`). |

### `.cursorrules`

| Purpose |
|--------|
| Conventions for this folder and a **project layout** snapshot; update the layout block (and this `context.md`) when files move or are added. |

---

## Effort focus (where to spend time)

1. **One cleaning rule** applied everywhere the stats need it (same `rows` after `clean_survey_row` for files and prints).
2. **Numeric fields** — parse safely where the assignment allows; know when to skip blank satisfaction scores.
3. **Keep this `context.md` accurate** when you rename files or change the main script’s inputs/outputs.

---

## Open choices

- **Bug fixes:** If the course supplies a *buggy* filename, fix bugs **in line with the rubric** rather than replacing the whole script.
- **Tone of this doc:** Mostly **instructional** (what to run, where logic lives). Add a short “interpretation” subsection only if the assignment asks for reflection on the *content* of the responses.
