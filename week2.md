# Week 2 — Competency claims (HCDE 530)

Short reflections on the eight competency domains. **C1, C2, and C5** include more detail because they match the work completed in this repository during Week 2.

---

## C1 — Vibecoding and rapid prototyping

*Describe what you want to build and deploy a working artifact from that description.*

This week I moved from a plain language goal (“show CSV responses, count words, and see results in a browser”) to a small working set of files: Python scripts, CSV inputs, and a dashboard page. I used **Cursor’s AI chat** to iterate quickly—turning rough goals into runnable code, then adjusting structure and file paths until things worked end-to-end. I also adopted a **`.cursorrules`** file so the project stays consistent as files are added, which made rapid changes less chaotic. Together, that felt like prototyping with guardrails: fast drafts, then small fixes until the pipeline behaved.

---

## C2 — Code reading

*Read and explain what a given block of code does.*

I spent time tracing how each script connects **data → computation → output**. For example, in `demo_word_count.py` and `app_review_word_counts.py`, the important blocks are loading rows with `csv.DictReader`, applying a small `word_count` helper, and aggregating min/max/average—once I could narrate that path, debugging and small edits got easier. I used **`context.md`** as my own map of “which section does what,” which is essentially code reading turned into documentation for future me and for anyone grading the work.

---

## C3 — Data handling

*Load, clean, and reshape data using pandas.*

This week I loaded and iterated over CSV data using Python’s built-in **`csv`** module (UTF-8, `DictReader`), which was enough for tidy demo files. I have **not** yet used **pandas** for cleaning or reshaping; when tables get messier (missing fields, inconsistent columns, merges), I expect pandas will be the next step.

---

## C4 — API use

*Retrieve and process data from a web API.*

I did not build a Python workflow that calls a REST API this week. My dashboard loads **Chart.js from a CDN** in the browser so charts render, but that is not the same as retrieving and processing API data in code. A future iteration could pull live data from an endpoint and feed the same visualization patterns.

---

## C5 — Visualization

*Produce clear, labeled data visualizations.*

I created **`dashboard.html`** to turn the same underlying response data into **labeled charts and a readable table**: summary metrics, a bar chart of counts by role, a bar chart of word counts by participant, plus filtering and search. The layout uses clear headings, axis labels, and table column headers so a reader can understand what they are seeing without reading the source. This was the main place where “data in a file” became something a stakeholder could scan quickly in a browser.

---

## C6 — ML evaluation

*Run an ML model via API and interpret its output.*

Not addressed in this week’s repo. I have not yet run a model through an API or written an interpretation of model outputs for an HCD decision.

---

## C7 — Critical evaluation and professional judgment

*Deploy a working tool or analysis for a real HCD problem.*

The datasets here are **fictional** and written to echo realistic UX-research themes without using real participant data—an intentional choice for privacy and classroom use. The scripts support a simple, explainable analysis (response length) that could support prioritization or spot-checking in a research workflow, but it is a demo, not a study instrument. If this were tied to a real problem, the next step would be clarifying research questions, consent, and what “length” does and does not measure.

---

## C8 — Building and deploying a complete tool

*Describe your work in terms of HCD value, not just code.*

The value I am practicing is **legible analysis**: making it obvious how text responses were processed, what was computed, and where to look in the repo for each step (`context.md`, scripts, dashboard). From an HCD perspective, the point is not the word count itself—it is showing how lightweight computation can summarize qualitative material for comparison, while keeping documentation honest about limitations and data provenance.
