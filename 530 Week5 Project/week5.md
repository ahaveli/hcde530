## Week 5 Summary

This file explains what I built for Week 5, how it fits the pandas and merging exercises, and how it supports competency claims.

Week 5 focused on **pandas** for inspection, filtering, grouping, and missing data, plus an introduction to **combining tables** with `pd.merge()`. The main analytical artifact for my dataset work is **`healthcare_US.ipynb`**, which loads **CDC NHSN Hospital Respiratory Data (HRD)** and answers several structured questions about national hospital capacity and reporting completeness.

---

## What I did

### Course demos

- **`week5_pandas_demo.ipynb`** — Walkthrough of core pandas patterns (loading tables, selecting columns, filtering, sorting, simple summaries).
- **`week5_merge_demo.ipynb`** — Small example merging **`reviews_mini.csv`** with **`app_info.csv`** on a shared key to show how split tables become one analysis-ready frame.

### Main deliverable — `healthcare_US.ipynb`

Built a notebook around the preliminary HRD export:

**`Weekly_Hospital_Respiratory_Data.csv`**

The notebook:

- Loads the CSV with **`thousands=","`** so comma-formatted numbers parse correctly.
- Uses **`head()`** and **`info()`** to summarize shape, columns, and dtypes.
- Uses **`value_counts()`** on geographic codes to see how jurisdictions repeat across weeks.
- **Filters** to national rows (`USA`) and adds a numeric threshold filter (inpatient beds **`>`** a cutoff) to match class patterns.
- **Groups by** jurisdiction and takes the **mean** of inpatient beds to compare areas at a summary level.
- Summarizes **missing data** with **`isnull().sum()`** (and related summaries) because many HRD columns are sparse by jurisdiction and metric.
- Includes short **`# Question:` / `# Answer:`** comments so each operation states what is being asked and how to read the output.

---

## Files in this folder (high level)

| Artifact | Description |
|----------|-------------|
| `healthcare_US.ipynb` | NHSN HRD analysis notebook (main Week 5 analytical work) |
| `Weekly_Hospital_Respiratory_Data.csv` | Source HRD metrics table |
| `week5_pandas_demo.ipynb` | In-class / practice pandas demo |
| `week5_merge_demo.ipynb` | Merge demo on small review + app tables |
| `reviews_mini.csv`, `app_info.csv`, `app_reviews_demo.csv` | Data for merge and pandas exercises |

---

# Competency claims


### C5 — Data analysis with pandas

**Notebook:** `healthcare_US.ipynb`

**Operations tied to questions (not just mechanics):**

| Idea | What I ran | What it tells me |
|------|------------|------------------|
| First look | `hrd.head()`, `hrd.info()` | Row/column scale, dtypes, and how sparse early columns are for non-national rows. |
| Common labels | `hrd["Geographic aggregation"].value_counts()` | Which jurisdiction codes repeat across weeks (many ties because the table is weekly × area). |
| Subsets | `hrd.loc[... == "USA"]` and `usa[usa["Number of Inpatient Beds"] > …]` | National time series vs. a numeric “high capacity” slice of weeks. |
| Compare groups | `groupby("Geographic aggregation")["Number of Inpatient Beds"].mean()` | Typical reported inpatient bed scale by jurisdiction (national totals dominate; sparse areas may disappear after `dropna`). |
| Gaps | `hrd.isnull().sum()` (with `%` summaries in the notebook) | Which metrics are rarely filled — HRD is wide and partially reported by design. |

**Interpretation in prose:** Inline **`# Question:` / `# Answer:`** pairs sit next to these steps so each output is tied to a plain-English question (for example: what national occupancy looks like week to week after stripping `%` from strings; how many weeks exceed a bed threshold; which columns are mostly empty).

**One-sentence stake:** *I loaded the preliminary NHSN HRD CSV, inspected it with **`head`/`info`**, ranked jurisdictions with **`value_counts`**, built USA-only and **`>`**-filtered subsets, averaged inpatient beds by **`groupby`**, and counted missing cells with **`isnull().sum()`** — and I wrote what each result implies about national strain vs. sparse reporting.*

---

### C6 — Data visualization

For **percent inpatient beds occupied** (national `USA` rows), I treat **distribution** as the core visual question: how tightly weekly occupancy clusters. After **`matplotlib` was not available in my kernel**, I did not block the assignment on charts — I showed the same idea with **`pd.cut`** into bins and **`value_counts`** (a **tabular histogram**: counts of weeks per occupancy band) plus **`describe()`** for numeric spread. That matches a **continuous** outcome without forcing a broken import.

**Design note:** A bar chart of 268 weekly labels would be unreadable; the bins summarize shape. If your environment has **`matplotlib`**, a histogram would be the parallel graphic — here the notebook still makes the **shape of the distribution** inspectable.

**One-sentence stake:** *I represented how **percent inpatient beds occupied** varies across national weeks using **binned week counts and summary statistics** so the pattern of hospital utilization is visible without relying on a plotting stack my kernel lacked.*

---

### C7 — Tool literacy / overriding bad defaults (environment)

I hit **`ModuleNotFoundError: No module named 'matplotlib'`** when the notebook kernel pointed at a Python that did not match the environment where I expected packages. Fixing that was not a prompt problem — I **checked which interpreter the notebook was using**, aligned the kernel with the **project’s intended environment**, and confirmed **`import pandas`** (and optionally **`matplotlib`**) in *that* interpreter. I also removed the hard dependency on **`matplotlib`** from the analysis path so **`healthcare_US.ipynb`** still runs with **pandas only**. That is **overriding a wrong default** (accidental kernel) after **evidence**, not after an AI guess.

---

### Supporting habits (cross-cutting)

- **C1 / rapid iteration:** Notebook cells let me re-run load → filter → summarize without rewriting scripts.
- **C2 / readable code:** Comments explain **why** a step matters for the HRD table, not only **what** function ran.
- **C3 / messy real data:** Comma thousands in **`read_csv`**, percent columns as strings until parsed — typical “government CSV” friction.

---

## If you are not reading the Python

**Open:** `healthcare_US.ipynb` in **`530 Week5 Project/`** (same folder as the long NHSN CSV filename).

**What it does:** Loads weekly hospital respiratory metrics, focuses on **United States** (`USA`) rows for national trends, summarizes **inpatient occupancy** and admissions columns, compares jurisdictions, and reports **where data is missing**.

**How to run:** Use Jupyter / VS Code with the **working directory** set to **`530 Week5 Project`** so the relative CSV path resolves. Pick a kernel where **`pandas`** is installed. Run cells **from top to bottom** after a restart so **`hrd`** and **`usa`** exist before Q1–Q4.

**Success looks like:** Printed shapes, preview tables, binned occupancy counts, jurisdiction averages, and missing-value summaries — all with short comments explaining what to take away.

---

## Notes for submission

- Ask your instructor whether this **HRD** extract should be labeled **MP1** or **Week 5 practice** for grading.
- Run the notebook top-to-bottom after any kernel restart so `hrd` and `usa` exist before later question cells.
