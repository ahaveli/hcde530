# Week 2 — Competency claims (HCDE 530)

---

## C1 — Vibecoding and rapid prototyping

*Describe what you want to build and deploy a working artifact from that description.*

This week I moved from a plain language goal (“show CSV responses, count words, and see results in a browser”) to a small working set of files: Python scripts, CSV inputs, and a dashboard page. The core pipeline is **`demo_word_count.py`** reading **`demo_responses.csv`**, a second exercise script **`app_review_word_counts.py`** reading **`app_reviews.csv`** (fifty fictional app reviews), and **`dashboard.html`** to visualize the research-style responses in the browser. I used **Cursor’s AI chat** to iterate quickly—turning rough goals into runnable code, then adjusting structure and file paths until things worked end-to-end. I also adopted **`.cursorrules`** so the project stays consistent as files are added (including keeping the layout list current), which made rapid changes less chaotic.

---

## C2 — Code reading

*Read and explain what a given block of code does.*

I spent time tracing how each script connects **data → computation → output**. I used **`context.md`** as my own map of “which section does what,” which is essentially code reading turned into documentation for future me and for anyone grading the work.

In the editor, I also learned **small reading mechanics**: **hovering** on a name to peek at its **definition**, noticing lines that start with **`#`** as **comments** (notes the author left for humans, not instructions to the computer), and using **indentation**—the way **Cursor** lines up **spaces**—to see which lines belong to the same loop, function, or block. When something still did not click, I used **AI chat** to ask for an explanation of **one selected bit of code** at a time, which helped me connect syntax to behavior.

---

## C3 — Data handling

*Load, clean, and reshape data using pandas.*

This week I loaded and iterated over CSV data using Python’s built-in **`csv`** module (**UTF-8**, **`DictReader`**). **`demo_responses.csv`** supplies **`participant_id`**, **`role`**, and **`response`** text; **`app_reviews.csv`** uses **`review_id`** and **`review`**. I have **not** yet used **pandas**.

---

## C4 — API use

*Retrieve and process data from a web API.*

I did not build a Python workflow that calls a REST API this week. My **`dashboard.html`** loads **Chart.js** from a CDN in the browser so charts render, but that is not the same as retrieving and processing API data in code. A future iteration could pull live data from an endpoint and feed the same visualization patterns.

---

## C5 — Visualization

*Produce clear, labeled data visualizations.*

I created **`dashboard.html`** to turn the same underlying response data into labeled charts and a readable table: summary metrics at the top, a **bar chart** of counts by role, a **bar chart** of word counts by participant, plus **role filtering**, **text search**, and an expandable full response in the table. The page embeds the rows as **JSON** inside the file so opening the HTML locally still works without a separate server. The layout uses clear headings, axis labels, and table column headers so a reader can understand what they are seeing without reading the source.

---

## C6 — ML evaluation

*Run an ML model via API and interpret its output.*

Not addressed in this week’s repo. I have not yet run a model through an API or written an interpretation of model outputs for an HCD decision.

---

## C7 — Critical evaluation and professional judgment

*Deploy a working tool or analysis for a real HCD problem.*

The datasets here are **fictional** and written to echo realistic UX-research themes without using real participant data—an intentional choice as it is a demo, not a study instrument. If this were tied to a real problem, the next step would be clarifying research questions, consent, and what “length” does and does not measure.

I tried to **cross-check** everything: I did **not** trust outputs that depended on **logic or data flow** until I **ran the scripts** and watched what came back. I also paid attention to how the “app” side of the work (the scripts and **`dashboard.html`**) would behave with **missing or unexpected** data. For **words** in the reweek2.md, I noticed a lot of writing still carries a **generic AI tone**; I would **not** ship that wording as-is to a real audience without rewriting it in my own voice. And that's what I did.

---

## C8 — Building and deploying a complete tool

*Describe your work in terms of HCD value, not just code.*

Not addressed in this week’s repo. I have not yet scoped, shipped, and reflected on a full end-to-end deployed tool in the MP sense; Week 2 stayed focused on the smaller pipeline and documentation pieces above.
