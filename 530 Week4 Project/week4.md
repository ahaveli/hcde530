## Week 4 Summary

This file explains what I built for Week 4, how I built it, and how it supports my competency claims.

I implemented two Python scripts using REST APIs:

- A **sports score fetcher** using TheSportsDB
- A **country data extractor** using the CountryStateCity API

Both scripts follow a shared pipeline pattern: **API request → JSON parsing → transformation → CSV export.**

---

## What I did

### Script 1 — Sports Score Fetcher

Built `sports_scores.py` to retrieve match data from a sports REST API.

- Tested multiple endpoints and identified that `livescore.php` returns **404** (not available in free tier).
- Switched to `eventspastleague.php?id=4387` for valid NBA data.
- Extracted key fields: home team, away team, scores, match date/status.
- Handled missing values for ongoing or incomplete matches.
- Added CSV export (`sports_scores_results.csv`) for structured analysis.

### Script 2 — Country Data Extractor

Built `country_state_city.py` using the CountryStateCity API.

- Retrieved structured country metadata: country name, capital city, currency code.
- Used API key authentication via headers.
- Parsed nested JSON into a flat tabular structure.
- Filtered dataset to countries starting with A–D.
- Exported results to `countries_A_to_D.csv`.

---

## Files produced

| Artifact | Description |
|----------|-------------|
| `sports_scores.py` | Sports score fetcher script |
| `sports_scores_results.csv` | Exported match data |
| `country_state_city.py` | Country metadata script |
| `countries_A_to_D.csv` | Filtered country export |

---

## Competency claims

### C1 — Vibecoding and Rapid Prototyping

I demonstrate **C1** by using AI tools and iterative development to move quickly from idea to working scripts.

I used Cursor and AI suggestions to scaffold both scripts, but most of the actual working version came from **testing real API responses** and adjusting based on what broke or didn’t exist.

A key example was the sports API: I initially expected live scores, but the endpoint returned a 404 in the free tier. Instead of stopping, I shifted to a **past-events** endpoint so the tool still worked.

Across both scripts, I didn’t design everything upfront. I built, tested, broke things, and adjusted directly from API output rather than a fixed plan.

### C2 — Code Literacy and Documentation

I demonstrate **C2** by reading API responses and turning them into structured, usable outputs.

I wrote multi-function Python scripts with clear separation of concerns.

I used **inline comments** to explain:

- why specific endpoints were chosen or replaced
- how JSON structures map to extracted fields
- why certain fields were filtered or simplified

I also used **docstrings** for core functions such as `fetch_data()`, `parse_json()`, and `export_csv()`.

I spent time understanding nested JSON structures instead of just printing raw responses, and selected only the fields that were meaningful for analysis (teams, scores, capitals, currency).

### C4 — APIs and Data Acquisition

I demonstrate **C4** by working with two REST APIs that behave differently in practice.

I made HTTP requests in Python and parsed JSON responses from real-world services.

I worked with two authentication models:

- **Public endpoint access** (sports API)
- **API key via headers** (CountryStateCity API)

I also had to handle real API constraints: the live sports endpoint was unavailable (404 in free tier), so I switched to an alternative endpoint with valid historical data.

I converted raw API responses into structured CSV outputs:

- Sports match dataset (`sports_scores_results.csv`)
- Country metadata dataset (`countries_A_to_D.csv`)

This shows ability to retrieve, adapt, and process data from external APIs under real constraints.

### C3 — Data Handling

I demonstrate **C3** by transforming unstructured JSON into clean tabular datasets.

I extracted relevant fields from nested API responses and flattened them into consistent row-based structures.

I handled inconsistencies in sports data, such as missing scores or incomplete match status, by **normalising** output values before writing to CSV.

I also filtered the country dataset using string-based logic (A–D filtering) to reduce complexity and make the dataset easier to work with.

Both outputs were structured into consistent CSV formats suitable for spreadsheet analysis.

### C7 — Critical Evaluation and Professional Judgment

I demonstrate **C7** by evaluating API reliability and making design decisions based on constraints.

I quickly realised that the sports API live endpoint was not usable in the free tier, so I adjusted the design instead of forcing an invalid approach.

I also compared the two APIs and noticed a clear difference:

- **Sports API** → dynamic, sometimes incomplete, inconsistent availability
- **Country API** → stable, structured, predictable dataset

Based on this, I made practical decisions: simplified outputs instead of forcing unreliable endpoints; filtered datasets to manageable subsets; prioritised usable CSV outputs over full raw data extraction.

This shows evaluation of data sources rather than blindly implementing API calls.

### C8 — Building and Deploying a Complete Tool

**Not addressed** in this week’s focused work. I have not run a model through a hosted ML API or written an HCD-style interpretation of model output for a practice decision.

---

