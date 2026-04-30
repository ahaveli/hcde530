# Week 3 — Competency claims (HCDE 530)

---

## C1 — Vibecoding and rapid prototyping

*Describe what you want to build and deploy a working artifact from that description.*

This week I started from a practical goal: take a **messy survey CSV**, **clean** it in a consistent way, **write** the cleaned table and a small **summary** file, and **print** simple stats in the terminal (role tallies, averages, top scores). I also used the smaller utilities to work with the **`responses`** pipeline: filter rows, normalize roles, and count roles. What I shipped in this folder includes **`week3_analysis_buggy.py`**, the survey inputs/outputs **`week3_survey_messy.csv`**, **`week3_survey_cleaned.csv`**, and **`week3_survey_summary.csv`**, plus **`clean_responses.py`**, **`count_response_roles.py`**, **`responses.csv`**, and **`responses_cleaned.csv`**. I relied on **AI prompting** in Cursor: I asked the model to **describe what the script was doing**, **explain** small pieces of code, and then I **prompted again** when I needed a tighter or clearer walkthrough.

---

## C2 — Code reading

*Read and explain what a given block of code does.*

I engaged with the code in two ways. First, I **ran the scripts** at multiple touchpoints and watched for what the outputs were. Second, I used **AI chat** as a reading partner: I **copy-pasted** a small bit of code and asked the model to **explain** it, and I also asked the model to **describe** what a run was doing step by step. Together, that gave me a mental model of **data → cleaning → exports → console analysis**.

---

## C3 — Data handling

*Load, clean, and reshape data using pandas.*

I **did not** use **pandas**; I worked directly with Python’s **`csv`** module and manual list/dictionary transformations. The messy survey file and the responses file gave me a realistic feel for **why** cleaning has to happen before summary numbers mean anything.

### Critical bug discovery (what actually broke)

The most important issue was - it was a **type + logic failure** that broke aggregation correctness.

#### `experience_years` and mixed numeric types

The script failed with:

```text
ValueError: invalid literal for int() with base 10: 'fifteen'
```

This occurred when converting **`experience_years`** to an integer during averaging. This was not a single bad value — it revealed that the dataset had **mixed-type numeric fields** (strings + integers).

#### Satisfaction pipeline

**`satisfaction_score`** values were sometimes blank or non-numeric. This caused incorrect ordering in the “top satisfaction” output. The bug was not a crash, but a **silent logic error** where sorting produced unstable rankings.

#### Structural: empty `role` fields

Some rows had empty **`role`** fields. These rows were still being included in grouping logic, which distorted role-based averages and counts.

### How I traced the problems

I first isolated them by identifying which specific record caused the **`ValueError`**


### How I fixed them

- I added explicit **`try` / `except` `ValueError`** handling around numeric conversions, preventing malformed numeric fields from breaking execution.
- I enforced numeric conversion before sorting, fixing the satisfaction ranking bug where strings were being compared inconsistently.
- I added row-level filtering (`if not role: continue`) to prevent empty categorical values from contaminating grouped statistics.
- I standardized strings using **`.strip()`** and **`.title()`** to prevent duplicate role keys caused by formatting differences.

### Result

After these fixes:

- the script no longer crashes on malformed numeric input
- satisfaction ranking becomes stable and consistent
- grouped outputs reflect only valid rows
- cleaned datasets match expected structure for downstream analysis

---

## C4 — API use

*Retrieve and process data from a web API.*

**Not addressed** in this week’s work.

---

## C5 — Visualization

*Produce clear, labeled data visualizations.*

My outputs for Week 3 were **tabular**: **cleaned CSVs** and a **summary CSV**, plus **printed** tables and lines in the terminal. For this assignment, the “clarity” live in **column names**, **consistent labels after cleaning**, and **readable** console output—rather than a graphic.

---

## C6 — ML evaluation

*Run an ML model via API and interpret its output.*

**Not addressed** in this week’s repo. 

---

## C7 — Critical evaluation and professional judgment

*Deploy a working tool or analysis for a real HCD problem.*

The data used this week was still **demonstration data**, not a live study. Even so, I tried **not** to treat the successful running of a script as automatic truth one that is without bugs. I **spot-checked** rows, compared **before and after** cleaning, and thought through **edge cases**—for example, what happens when **`satisfaction_score`** is **empty** and a ranking or average could be misleading. If this work were ever tied to **real participants**, the bar would go beyond clean columns: **writing style** and the **meaning behind people’s words** would matter for how we report and decide, not just whether the CSV parses. 

---

## C8 — Building and deploying a complete tool

*Describe your work in terms of HCD value, not just code.*

Week 3 in this folder is best described as a **small analysis** and **repeatable cleaning** path—not a full **deployed product** the way a production app or live service would be. The HCD value I can claim is: the scripts make it easier to get from **messy tabular input** to **shared artifacts** (cleaned data and a small summary file) that a team could, in principle, open, audit, and discuss.
