# Week 6 — Competency Claims

Week 6 moves my MP1 work from **Week 5 pandas summaries** on CDC NHSN Hospital Respiratory Data (HRD) into **Plotly visualizations** that answer three analytical questions. Each question has one primary chart, documented chart-type rationale, and markdown in the notebook so someone else can run the code and follow the reasoning.

---

## Week 6 — A6 first MP1 visualization

### What this week adds to MP1

Section 4 is where my analysis becomes visual. I am still using the same CDC NHSN preliminary HRD table I explored in Week 5 (`530 Week5 Project/healthcare_US.ipynb` and `Weekly_Hospital_Respiratory_Data.csv`); Week 6 adds the plotting layer on top of that understanding. I built three figures—each answers one research thread—and exported them as **static PNGs** for submission while keeping the generating code in the notebook.

**Research questions**

1. How does hospital capacity pressure (inpatient and ICU occupancy) vary across states over time, and which states show sustained high strain?
2. Are there seasonal or temporal patterns in hospital occupancy and bed utilization?
3. Do pediatric and adult bed occupancy rates follow different patterns over time, and are pediatric ICU beds proportionally more strained than adult ICU beds?

**Artifacts in `530 Week6 Project/`**

| File | Role |
|------|------|
| `week6_mp1_starter.ipynb` | Code, markdown rationale, interactive Plotly previews |
| `viz1_state_hospital_capacity.png` | Static export — state capacity over time |
| `viz2_seasonal_heatmap.png` | Static export — national seasonality |
| `viz3_pediatric_adult_monthly.png` | Static export — adult vs pediatric by month |

Each visualization cell ends with `fig.write_image(..., engine="kaleido", scale=2)` so the PNGs match what appears in the notebook. Setup installs `pandas`, `plotly`, and `kaleido`. `plotly-exercises.ipynb` was practice only.

### Process and approach

Week 5 taught me how the HRD file behaves: percents arrive as strings, counts use comma thousands, rows repeat by week and jurisdiction, and many pathogen columns are sparse. I summarized occupancy with `describe()` and bins before I had a dependable chart stack. Week 6 reused that cleaning logic and added figures only where a table could not show the pattern I cared about.

Plotly let me iterate in the notebook, then commit the same figure objects as PNGs. The notebook resolves the CSV from paths under Week 6 or Week 5 so I do not duplicate data maintenance.

**Changes that shaped the final PNGs**

*Question 2 — seasonality.* A national line over every reporting week shows spikes in time but not whether **January in one year resembles January in another**. I switched to a year-by-month heatmap so calendar months line up vertically across years. Winter pressure reads as repeated columns, not a single long wiggle.

*Question 1 — states.* Plotting every jurisdiction produced unreadable overlap. I limited to US state/DC codes, ranked by **latest-week inpatient occupancy**, and kept the **top 12** for the export. The title/subtitle document that scope.

*Question 3 — adult vs pediatric.* Hospital-wide “percent beds occupied” does not split age groups. I computed occupancy from adult and pediatric bed and occupied columns, averaged to **months** for a legible axis, and printed national means under the chart so the ICU “proportionally more strained” clause has numeric support.

All three pipelines strip `%` and commas from percent fields before plotting.

### Chart 1: How does hospital capacity pressure vary across high-burden states?

**Files:** `viz1_state_hospital_capacity.png` · `week6_mp1_starter.ipynb` (first visualization cell)

**What the figure shows.** Two stacked panels share the same time axis (week ending date). Each colored line is one state. The **upper panel** tracks **percent of inpatient beds occupied**; the **lower panel** tracks **percent of ICU beds occupied**. Only the 12 states with the highest inpatient occupancy in the latest week in the file are drawn (latest week in my export: **2025-09-20**; includes WA, MA, RI, AK, NY, DE, GA, ME, MO, NH, MD, MI).

**Why a faceted line chart.** The question is about **persistence and change over time** within states, not a one-week ranking. Lines carry that better than bars at weekly resolution. Facets keep inpatient and ICU on comparable percent scales without merging two different bed types into one panel.

**How to read it.** Follow one color through both panels: if a state stays high for many weeks, strain is sustained, not a single reporting glitch. Compare panels for the same state—if inpatient is high while ICU is moderate (or the reverse), “capacity pressure” depends on which bed pool you mean.

**What I infer.** Occupancy is geographically uneven. Several states run hot for long stretches. Inpatient and ICU do not always move together, so a single hospital-wide percent would hide important differences between general and critical-care pressure.

### Chart 2: Are there seasonal or temporal patterns in national occupancy?

**Files:** `viz2_seasonal_heatmap.png` · `week6_mp1_starter.ipynb` (seasonal heatmap cell)

**What the figure shows.** National **USA** rows only. Each **row** is a calendar **year**, each **column** is a **month** (Jan–Dec). Cell color is the **average** of weekly inpatient or ICU occupancy for that month in that year. **Top panel:** inpatient; **bottom panel:** ICU. Color runs **60% → yellow** through **80% → red** on a **shared scale** on both panels so colors are comparable. Darker red = fuller hospitals that month.

**Why a heatmap instead of a timeline.** “Seasonal” here means **the same months recurring across years**, not “something happened in 2021.” A heatmap puts months side by side so you can scan down a November column across years. A single line chart buries that comparison in horizontal distance.

**How to read it.** Look for **vertical bands**—months that stay relatively dark across multiple years (often late fall and winter). That pattern suggests recurring demand. A single bright or dark year-row without matching neighbors looks more like a one-off event than a season.

**What I infer.** In aggregated national data, inpatient occupancy averages about **75.3%** in Nov–Feb vs **73.6%** in Jun–Aug—modest in points, but visible as repeated winter columns in the matrix. ICU should be read in the lower panel; both panels darkening together is stronger evidence of system-wide pressure than inpatient alone.

### Chart 3: Do adult and pediatric occupancy follow different patterns?

**Files:** `viz3_pediatric_adult_monthly.png` · `week6_mp1_starter.ipynb` (monthly trends cell)

**What the figure shows.** National **USA** data, aggregated to **calendar months** on the x-axis. **Top panel:** adult vs pediatric **inpatient** occupancy (%). **Bottom panel:** adult vs pediatric **ICU** occupancy (%). **Blue** = adult, **orange** = pediatric. The notebook also prints long-run averages over all USA weeks (shown on the PNG run below).

**Why monthly lines with two panels.** The question has two parts: (1) do the **timing** of peaks differ by age group—lines month by month answer that; (2) is pediatric ICU **proportionally** harder hit—panels separate ICU from general beds, and printed means answer “proportional” without guessing from line gaps.

**How to read it.** In each panel, ask whether blue and orange rise and fall **together** (similar pattern) or **peak in different months** (different pattern). Use the bottom panel plus the printed summary for ICU strain—not the top panel alone.

**What I infer (from my exported run):**

| Measure | Adult | Pediatric |
|---------|-------|-----------|
| Inpatient | 75.5% | 64.0% |
| ICU | 72.7% | 67.1% |

Pediatric ICU average ÷ adult ICU average ≈ **0.92** → pediatric ICU is **not** more strained than adult ICU nationally. Adults run higher occupancy in both bed types; monthly curves are related but not identical.

### What this shows about the work

The committed PNGs are the grading-facing snapshots; the notebook is the reproducible path to regenerate them. Together they show I can align chart type to question (lines for state trajectories, heatmap for cross-year months, dual-panel lines for two populations), document subsets and derived fields, and redo a figure when the first version answers the wrong question.

Rejected paths matter as much as finals: all-state spaghetti, a lone national timeline for seasonality, and plotting hospital-wide percents for an adult/pediatric question. Kaleido export forced me to check titles, margins, and label density in a static view—not only in interactive hover mode.

### What I would do next

Add a short interpretation paragraph under each PNG in the notebook write-up, and keep notebook and image exports in sync if I change filters or date range. If I extend the HRD analysis, new questions should get new chart types using the same rule: match geometry to the claim, export a PNG, and explain how to read it in markdown.
