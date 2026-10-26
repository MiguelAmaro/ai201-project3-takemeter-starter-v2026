# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

This project uses posts from the DEV Community (dev.to) to train a text classifier. The classifier sorts posts into two categories: **DevLog** and **Informative**. DevLog posts primarily document the development or progress of a specific software project, while Informative posts primarily explain technical concepts, tools, or techniques. This classification helps readers distinguish project-focused content from educational content.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `informative`

**Definition:**
A post primarily explaining an existing technology, its capabilities, or how it can be used.
**Example 1:**
>An article explaining how Redis caching works and when to use it.

**Example 2:**
>An article explaining React hooks, their capabilities, and their appropriate use cases.

### `dev_log`

**Definition:**
A post primarily documenting the development, implementation, or capabilities of a specific software project created by the author.
**Example 1:**
>https://dev.to/gramli/i-vibe-coded-my-way-out-of-angular-upgrades-4fkh?utm_source=chatgpt.com

**Example 2:**
>An article documenting the development of a personal application, including its features and implementation decisions.

### The hardest boundary

**Which two labels:**

informative and dev_log

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If the post primarily explains a technology or technique independently of a specific project, classify it as informative. If the post primarily documents the author's own software project, its implementation, or its capabilities, classify it as dev_log.


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** 250 public dev.to posts, collected through the dev.to API (`https://dev.to/api/articles`) and saved whole (title + full markdown body, nothing trimmed) in a single unsplit `labels.csv`. The first 220 came from the site's latest-articles feed. That feed skewed heavily toward `informative` (83%), so I added 57 posts from the `showdev`, `buildinpublic`, `sideprojects` and `devjournal` tags to bring in thin `dev_log` examples. I removed 27 posts that fit neither label (welcome threads, meme threads, "win this week" prompts, weekly roundups, challenge announcements, one-line model-availability notices) and de-duplicated by text and URL. Posts are 948 to 56,101 characters long (median about 10,000). Each row's `note` records the reason for the label and the post URL.

**How I labelled them:** Pre-labelled with AI, not cold. GitHub Copilot read the title and opening of each post and applied my taxonomy and decision rule; I have not yet re-read each full post and am correcting labels as I spot-check. Because it worked from previews, the borderline posts (below) are the most likely to be wrong.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `informative` | 156 | 62.4% |
| `dev_log` | 94 | 37.6% |
| **Total** | 250 | 100% |

Neither label is above the 70% limit. There are no duplicate posts.

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* "Publishing Markdown to Substack from an Agent Skill", a step-by-step walkthrough of one destination in the author's own `publishing-kit`.
>
> *Could have been:* `informative` (it teaches Substack's publishing quirks) or `dev_log` (it documents the author's own tool).
>
> *I chose:* `dev_log`, because the post is built around the implementation and capabilities of the author's own project rather than a technique that stands apart from it.

**2.**
> *The post:* "Gemma 4 on a Used 8 GB RTX 3050: 116 Tokens/s for One User, 618 for 64", and the other benchmark and deployment write-ups in the same series.
>
> *Could have been:* `dev_log` (a first-person build with measured results) or `informative` (it explains what an existing model can do on given hardware).
>
> *I chose:* `informative`, because the subject is an existing technology (Gemma 4) and what it can do, and the author's own code is only a vehicle for the measurements.

**3.**
> *The post:* "Building Better Agents through End-to-End Evals", where the author describes building Ramp Stack, with advice for other teams.
>
> *Could have been:* `dev_log` (it describes a specific product the author's team built) or `informative` (it teaches a general technique).
>
> *I chose:* `informative`, because the lessons about evals are meant to apply regardless of that project; the project is an illustration, not the subject.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* A rewrite of `post-fetch.py` so it produces a single unsplit `labels.csv` with `text`, `label` and `note` columns, holding at least 200 whole posts.
- *What came back:* A script that pulls dev.to posts, fetches each full post body (the list endpoint only returns summaries), de-duplicates, and writes 220 rows with blank labels. The first version of my old script had only collected titles and descriptions into a different file.
- *What I changed:* I kept the script's output as-is but removed the old `candidate_posts.csv`. When the first 220 posts came back 83% `informative`, I had it collect 57 more from `showdev`, `buildinpublic`, `sideprojects` and `devjournal` to get under the 70% limit, and I dropped 27 posts that fit neither label.

**Moment 2**

- *What I asked for:* Labels for all posts using my taxonomy, my definitions of `informative` and `dev_log`, and my decision rule.
- *What came back:* A label for every post, made from each post's title and opening, with a short reason in `note`. This produced 156 `informative` and 94 `dev_log`.
- *What I changed:* I treated the labels as a first pass and am spot-checking them against the full text, because the AI only read previews. Borderline posts, such as benchmark write-ups of existing tech versus write-ups of the author's own tool, are the ones I am checking most closely. <!-- add which labels you actually flipped -->

**Pre-labelling disclosure:** Yes, I did not label the data cold. GitHub Copilot pre-labelled all 250 posts from their titles and openings, using the definitions and decision rule above. It did not read every post in full. I am reviewing and correcting them myself. <!-- state how many you reviewed/changed when done -->

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |0.605  | 0.632 |  +0.026|
| Macro F1 | 0.553 | -0.166 | -0.166 |
| F1 — `label_one` | 0.400 | 0.00 |-0.400  | 
| F1 — `label_two` | 0.706 | 0.774 |+0.068  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
I predict my fine-tuned model will outperform the baseline when distinguishing informative posts from dev_log posts that contain technical explanations, because it was trained on examples reflecting my taxonomy.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall classification Accuracy  |≥75% | 63.2%| 63.2% | 63.2% | Missed |
| 2. Informative classification Performance |≥0.70  | - | - | - | Pending |
| 3. Dev log classification performance |≥0.70  | - | - | - | Pending |
| 4. Dataset label balance | ≤60% per label | n/a | n/a | n/a |  Missed |
| 5. Classification consistency | ≥85% agreement | n/a | n/a | n/a | Pending |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |informative| dev_log | n/a |
|---|---|---|---|
| informative | 24 | 0 | n/a |
| dev_log | 14 | 0 | n/a |
| **** | n/a | n/a | n/a |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 =100%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**
No disagreements were reported between my submitted labels and the staff reference labels.

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**

he submitted labels matched the staff reference labels on all 30 posts. Therefore, the agreement test produced no disagreements to adjudicate.

However, this result does not independently establish the clarity of the taxonomy or my ability to apply it consistently.

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
