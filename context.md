# Project context — HCDE 530 Week 2

This file maps **what each part of the repo is for**. It is written for **you**, **graders**, and **anyone running the demo**—especially if they are HCD practitioners, not software engineers.

---

## Goals (what “success” looks like)

- Show **effective processing of a data file**: load structured rows, derive a simple metric (word count), report per row and in summary.
- Make the **important logic easy to find** without reading every line—use this doc plus short section headers in code.
- Let someone **run the Python script** and optionally **view results in a browser** (`dashboard.html`).
- Prefer a **clear pipeline** over clever architecture; favor **standard library** Python unless the course asks otherwise.

---

## Audience and takeaways

- **Primary audience:** Instructor/TAs and classmates who should see that you can **read data**, **compute something meaningful**, and **explain where that happens**.
- **One-sentence takeaway:** *The CSV is loaded cleanly, each response is measured consistently, and the same idea appears in both the terminal output and the dashboard.*

---

## Data

- **`demo_responses.csv` is fully fictional** demo material. Themes are **paraphrased** from real practice so it reads like research-style quotes without using real participant data.
- Columns: `participant_id`, `role`, `response` (see header row in the file).

---

## How to run

1. **Terminal summary** (from the project folder):

   ```bash
   python demo_word_count.py
   ```

   Expect a table of IDs, roles, word counts, and a short text preview, then min/max/average word counts.

2. **Web dashboard:** open **`dashboard.html`** in a browser (double-click or “Open with…”).

   - Uses **Chart.js** from a CDN for charts; network access may be required the first time it loads.
   - Word counts use the **same whitespace-splitting idea** as the script (see footer on the page).

3. **App reviews word counts** (optional exercise — fictional store reviews):

   ```bash
   python app_review_word_counts.py
   ```

   Reads `app_reviews.csv` and prints per-review word counts plus shortest, longest, and average.

---

## File map — section → purpose

### `demo_word_count.py`

| Lines (approx.) | Purpose |
|-----------------|--------|
| 4–11 | **Load CSV** into a list of row dicts (`csv.DictReader`, UTF-8, correct newline handling for CSV). |
| 14–20 | **`count_words`** — the core metric: split on whitespace, return length. |
| 23–46 | **Per-row processing** — read fields, call `count_words`, print aligned preview (truncated). |
| 48–54 | **Summary stats** — count, min, max, average over all word counts. |

### `demo_responses.csv`

| Part | Purpose |
|------|--------|
| Header | Defines fields used by the script and dashboard. |
| Rows | One fictional “participant” per line; `response` holds the text analyzed for word count. |

### `app_review_word_counts.py`

| Lines (approx.) | Purpose |
|-----------------|--------|
| 6 | **`CSV_PATH`** — data file lives next to the script (`pathlib`). |
| 9–11 | **`word_count`** — whitespace split; same metric idea as `demo_word_count.py`. |
| 14–29 | **Load CSV → print** each review’s word count and a short preview. |
| 31–41 | **Summary** — total reviews, shortest, longest, average length. |

### `app_reviews.csv`

| Part | Purpose |
|------|--------|
| Header | `review_id`, `review` — 50 fictional app-store-style reviews (made-up text). |
| Rows | One review per line; used only by `app_review_word_counts.py`. |

### `dashboard.html`

| Part (approx.) | Purpose |
|----------------|--------|
| `<head>` + `<style>` | Page layout, colors, table/chart presentation. |
| Header + `<section class="metrics">` | Titles and placeholders for summary numbers. |
| `.charts` | Bar charts: counts by role, word count per participant (Chart.js). |
| Table + toolbar | Filter by role, search text, expandable full response. |
| `<script id="embedded-data">` | **Embedded JSON copy** of the rows (keeps the page self-contained when opened as a file). |
| `<script>` (main) | **Parse JSON → `wordCount` per row → metrics → charts → table**; `escapeHtml` for safe display. |

### `README.md`

| Purpose |
|--------|
| Course/project label; add **run commands** here if the syllabus expects a single entry point for graders. |

### `.cursorrules`

| Purpose |
|--------|
| Conventions for this repo and a **project layout** snapshot; update the layout block when files move or are added. |

### `week2.md`

| Purpose |
|--------|
| Week 2 **competency claims** (eight domains); course reflection submitted with the repo. |

---

## Effort focus (where to spend time)

1. **Clear data path** in the script (load → metric → table → summary).
2. **Keep this `context.md` accurate** when you rename or split files.
3. **Run instructions** that work on a fresh clone (Python command + how to open the HTML).
4. If both script and dashboard are submitted, **keep metrics consistent** in definition (word splitting), or document any intentional difference.

---

## Open choices from the interview

- **Tooling:** No hard constraint—**Python + opening HTML** is enough; optional later: generate the dashboard from the script if the course encourages it.
- **Tone of this doc:** Mostly **instructional** (what to run, where logic lives). You can add a short “research lens” subsection later (e.g., what themes the quotes illustrate) if the assignment asks for interpretation.
