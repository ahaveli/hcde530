# Week 4 — Competency claims (HCDE 530)

---

## C1 — Vibecoding and rapid prototyping

*Describe what you want to build and deploy a working artifact from that description.*

This week I focused on a clear goal: **call public REST APIs**, **parse JSON**, and **turn results into something I can read and save** (terminal output and CSV), while **keeping API keys out of source code** with a local **`.env`** file. What I shipped in this folder includes **`fetch_reviews.py`** (HCDE review API, filtering by helpful votes, writing a new CSV), **`seattle_weather.py`** (OpenWeatherMap for Seattle, key from **`OPENWEATHERMAP_API_KEY`**), and **`sports_scores.py`** (TheSportsDB past league events; prints games and writes **`sports_scores_results.csv`**). I also added **`week4.md`**, **`.cursorrules`**, and **`context.md`** so the folder stays easy to navigate. I used **AI in Cursor** to shape and debug small scripts, then **ran** them to confirm the pipeline end-to-end.

---

## C2 — Code reading

*Read and explain what a given block of code does.*

I traced how each script moves from **URL → request → JSON (or text) → structured output**. I used **`context.md`** as a map of filenames and purposes, and I read **`requirements.txt`** to see that **`sports_scores.py`** depends on **`requests`** while other scripts lean on the standard library. When something was unclear, I read the code in order—**`try` / `except`**, **parsing**, **printing**—and I used the editor and short AI questions on **one block at a time** when needed.

---

## C3 — Data handling

*Load, clean, and reshape data using pandas.*

I **did not** use **pandas** this week. I work with **CSV** using Python’s built-in **`csv`** module (for example writing **`sports_scores_results.csv`** with UTF-8) and I treat API fields with **defensive** access (`.get`, placeholders) when values are **null** or missing. **`reviews_category_helpful_votes.csv`** remains the full review export, while the review script writes a **separate** output file for high-upvote rows so the original stays untouched, as designed.

---

## C4 — API use

*Retrieve and process data from a web API.*

I **did** use REST-style APIs in code. **`fetch_reviews.py`** calls the course review API (JSON, pagination, filter on **`helpful_votes`**). **`seattle_weather.py`** calls OpenWeather’s current-weather endpoint with a key from **`.env`**. **`sports_scores.py`** calls TheSportsDB **`eventspastleague`** and maps fields like **`strHomeTeam`**, **`intHomeScore`**, and **`dateEvent`** into a consistent print format and rows for CSV. I also handle **HTTP errors**, **timeouts**, and **invalid JSON** where the scripts are written to do so.

---

## C5 — Visualization

*Produce clear, labeled data visualizations.*

This week’s “visualization” is **tabular and textual**: **printed** game and weather lines, **CSVs** with **header row** and **named columns**, and readable labels in the console. I did **not** add charts or a dashboard; clarity lives in **column names**, **consistent field formatting**, and **readable** `print` output.

---

## C6 — ML evaluation

*Run an ML model via API and interpret its output.*

**Not addressed** in this week’s repo. I have not run a model through a hosted ML API or written an HCD-style interpretation of model output for a practice decision.

---

## C7 — Critical evaluation and professional judgment

*Deploy a working tool or analysis for a real HCD problem.*

I treat these scripts as **learning and demonstration**, not a production study. **API keys** live in **`.env`** and should not be committed or shared casually. TheSportsDB and weather data are **public feeds**; review data in the course API is a **toy** context for practice. I **double-check** outputs by **running** scripts and spot-checking rows, and I note that **league or endpoint IDs** in a URL must match the sport or competition you think you are querying, or the labels will be misleading. If this work ever used **real** participants, consent, retention, and reporting would need a much higher bar than “it ran without error.”

---

## C8 — Building and deploying a complete tool

*Describe your work in terms of HCD value, not just code.*

This folder is a **set of small CLI-style scripts** and data artifacts—not a long-lived **deployed** product. The HCD value I can claim is **repeatable, inspectable** steps: pull structured data from APIs, make **missing data** visible instead of silent, and save **shareable** CSVs a teammate could open in a spreadsheet. A future step would be packaging, hosting, or a UI if the goal were a tool others use every week.
