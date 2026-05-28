## Week 7 Summary

This file explains what I built for **Mini Project 1 (MP1)**, how I built it, and how it supports my competency claims.

I completed an end-to-end analysis of **CDC NHSN Hospital Respiratory Data (HRD)**—weekly U.S. hospital capacity and respiratory-related utilization—using a Jupyter notebook, pandas, and Plotly. The work spans data profiling, three research questions with visualizations, written conclusions, and a process reflection.

The pipeline pattern for this project: **load CSV → profile and clean → filter and aggregate → visualize → interpret for HCD stakeholders.**

---

## What I did

### Dataset and research framing

Selected the **CDC NHSN Hospital Respiratory Data** from [data.cdc.gov](https://data.cdc.gov/)—a public, weekly dataset with ~17,956 rows and 190 columns covering inpatient/ICU beds, COVID-19/influenza/RSV patients, admissions by age, and pre-calculated occupancy percentages by geography and week.

Defined three analytical questions:

1. **Which regions consistently operate near high occupancy levels over time?**
2. **Are there seasonal or temporal patterns in hospital occupancy and bed utilization?**
3. **Do pediatric and adult bed occupancy rates follow different patterns, and is pediatric ICU proportionally more strained than adult ICU?**

Documented why the dataset matters for HCD (system-level capacity constraints affecting access and experience) and who might use the findings (public health officials, hospital administrators, policy planners).

### Data profile (`MP1 Analysis Notebook.ipynb` — Section 2)

- Loaded `MP1_Weekly_Hospital_Respiratory_Data.csv` with pandas.
- Ran `head()`, `info()`, `describe()`, and `isnull().sum()` to understand shape, dtypes, and missingness.
- Interpreted results in markdown: one record per geographic unit per week; heavy missingness in admission breakdown columns; core occupancy fields more complete (~17,600+ non-null).
- Identified columns used in analysis: `Week Ending Date`, `Geographic aggregation`, occupancy percentages, adult/pediatric bed counts.

### Analysis 1 — Regional capacity pressure

Built a **faceted line chart** (weekly time series by state) in Plotly.

- Filtered to U.S. state codes; parsed `Week Ending Date` as datetime.
- Stripped `%` from occupancy fields and converted to numeric.
- Selected the **top 12 states** by most recent inpatient occupancy for readable comparison.
- Compared **inpatient** and **ICU** occupancy over time.
- Exported `viz1_state_hospital_capacity.png` via Kaleido.

**Finding:** Several states (e.g., Rhode Island, Massachusetts, Maryland, Washington) run **persistently high** occupancy (often 75–80%+ inpatient), suggesting **localized** capacity pressure rather than only a national average story.

### Analysis 2 — Seasonal patterns (national)

Built a **year × month heatmap** for national `USA` rows.

- Aggregated weekly data to average occupancy by calendar year and month.
- Visualized inpatient and ICU capacity in separate heatmaps with a consistent color scale.
- Exported `viz2_seasonal_heatmap.png`.

**Finding:** **Recurring winter-heavy occupancy** at the national level, with year-to-year variation as reporting and respiratory drivers shifted—supports planning around **predictable seasonal demand**.

### Analysis 3 — Adult vs pediatric occupancy

Built a **monthly average line chart** comparing adult and pediatric inpatient and ICU occupancy nationally.

- Filtered to `USA`; derived adult/pediatric occupancy from bed counts where needed.
- Grouped by calendar month; printed average occupancy for the write-up (e.g., adult inpatient ~75.5% vs pediatric ~64%).
- Compared pediatric-to-adult ICU strain ratio (~0.92).
- Exported `viz3_pediatric_adult_monthly.png`.

**Finding:** **Adult occupancy is higher on average** than pediatric; trends are related but not identical. **Pediatric ICU is not proportionally more strained** than adult ICU in this dataset—adult critical-care capacity carries the higher typical load.

### Conclusions and process (notebook Sections 4–5)

- Summarized answers to all three questions in plain language.
- Listed next steps (facility-level data, linking occupancy to admission type, reporting gaps).
- Documented how work evolved across **MP1a**, **Week 5 (pandas)**, and **Week 6 (visualization starter)**, AI use for cleaning/chart sanity checks, and challenges (190-column width, uneven reporting, Kaleido static export).

---

## Files produced

| Artifact | Description |
|----------|-------------|
| `MP1 Analysis Notebook.ipynb` | Full MP1 notebook: overview, data profile, three analyses, conclusions, process |
| `MP1_Weekly_Hospital_Respiratory_Data.csv` | CDC NHSN weekly hospital respiratory dataset (source data) |
| `viz1_state_hospital_capacity.png` | Faceted state line chart — inpatient vs ICU occupancy over time |
| `viz2_seasonal_heatmap.png` | National year × month heatmap — seasonal occupancy patterns |
| `viz3_pediatric_adult_monthly.png` | Monthly adult vs pediatric occupancy comparison (USA) |
| `week7.md` | This summary and competency claims document |

---

## Competency claims

### C1 — Vibecoding and Rapid Prototyping

I demonstrate **C1** by moving from a dataset search (MP1a) to a working analysis notebook through iterative builds across course weeks.

I used **Cursor and AI** to scaffold pandas cleaning (e.g., stripping `%` from occupancy strings) and to check chart choices against the Week 6 visualization guide, but the **research questions, column choices, and interpretations** came from inspecting real CDC output.

When the raw file proved too wide (190 columns), I scoped down to a **small set of occupancy fields** rather than stalling—prototype, test, narrow, repeat.

Visualization code started in `week6_mp1_starter.ipynb` and was carried into the final MP1 notebook once patterns were visible.

### C2 — Code Literacy and Documentation

I demonstrate **C2** by reading and explaining a non-trivial pandas workflow in a notebook meant for graders and future readers.

The notebook is structured in **five sections** (Overview, Data Profile, Analysis, Conclusions, Process) with markdown that explains *why* each chart exists, not only *what* code runs.

I documented data profile operations (`head`, `info`, `describe`, null counts) with **plain-language interpretation**—what each result implies about reporting completeness and analysis limits.

Chart cells use **labeled axes, finding-oriented titles**, and exported PNGs embedded in the notebook so results are reviewable without re-running every cell.

### C3 — Data Handling

I demonstrate **C3** by loading, cleaning, reshaping, and aggregating real-world tabular data at scale.

I loaded a **17,956 × 190** CSV, parsed dates, converted string percentages to numeric, and filtered rows by geography (`USA`, state codes).

I used **groupby** and aggregation for national month/year heatmaps and monthly adult/pediatric averages.

I made explicit judgments about **missing data**: admission breakdown columns are often sparse; occupancy percentages are complete enough for the capacity questions asked.

### C4 — APIs and Data Acquisition

**Partially addressed.** This project uses a **downloaded public CDC CSV**, not a live REST call in the notebook.

I acquired data from the CDC data portal, validated file structure on load, and treated the export as an external source with its own reporting rules and gaps—similar discipline to API work (provenance, schema surprises, incomplete fields), but without HTTP authentication or endpoint switching in code.

### C5 — Visualization

I demonstrate **C5** by producing **three clear, labeled visualizations** matched to each research question.

| Question | Chart type | Design choice |
|----------|------------|----------------|
| Regional pressure | Faceted line chart | Compare top high-burden states over time; separate inpatient vs ICU panels |
| Seasonality | Year × month heatmap | Show recurring monthly patterns at national scale |
| Adult vs pediatric | Monthly line chart | Compare two populations on the same axes for direct reading |

Titles state **findings** (e.g., capacity pressure varies across states), not just variable names. Static PNGs (`viz1`–`viz3`) make the project portable for submission and review.

### C6 — ML Evaluation

**Not addressed** in this project. I did not run a model through a hosted ML API or interpret model scores for a practice decision.

### C7 — Critical Evaluation and Professional Judgment

I demonstrate **C7** by evaluating data quality and limiting claims to what the charts support.

I recognized that **state averages hide facility-level variation** and that territories with sparse reporting can skew early rows.

I compared **inpatient vs ICU** lines and **adult vs pediatric** metrics rather than collapsing everything into a single “hospitals are full” headline.

I noted **pediatric ICU is not proportionally more strained** (ratio ≈ 0.92) even though pediatric capacity still matters for surge planning—avoiding overstatement from a single aggregate.

I listed **honest next steps** (facility-level data, admission-type linkage, reporting-gap checks) instead of treating this notebook as a finished policy product.

### C8 — Building and Deploying a Complete Tool

I demonstrate **C8** by delivering a **standalone, end-to-end analysis artifact** for a real HCD-relevant problem.

The `MP1 Project` folder contains everything needed to review the work: source data, executable notebook, saved charts, and this write-up—without depending on other weekly folders.

The deliverable answers defined research questions, connects findings to **who would use them**, and reflects on process (weeks 5–7, AI use, challenges)—not just isolated code cells.

---

## HCD Connection

As someone with a UX and design background, I approached this project by asking **who experiences hospital capacity pressure** and whether the analysis makes that visible at a useful level—not whether the code runs.

The CDC file is public and authoritative, but **190 columns of weekly metrics are not actionable** for most stakeholders on their own. Choosing occupancy percentages, filtering to states or national `USA`, and exporting charts are decisions about **what a hospital administrator or public health planner can actually take in** during a meeting or briefing.

The three questions deliberately split the problem: **where** strain concentrates (states), **when** it tends to spike (seasonal heatmap), and **for whom** beds are tighter (adult vs pediatric). That mirrors how HCD work breaks complex systems into dimensions people can reason about instead of one overwhelming aggregate.

I also treated **missing and uneven reporting** as a human factors issue: if admission fields are empty for many weeks, conclusions about capacity must lean on the fields hospitals actually reported consistently—otherwise we risk telling a false story about access and strain.

HCD here is not a separate section pasted onto a stats exercise. It is in the **question selection**, the **chart types**, the **honest limits** in conclusions, and the intent that someone planning care delivery could use these views as a starting point—not as raw CDC export.
