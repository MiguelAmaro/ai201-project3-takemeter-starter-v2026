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
>"[AI in Practice] Upgrading from Gemini 3.5/3.6 to Gemini 4 Argon: Migration Notes and Pitfalls for LINE Bot Developers" — explains a technology migration and its pitfalls.

**Example 2:**
>"Gemma 4 on a Used 8 GB RTX 3050: 116 Tokens/s for One User, 618 for 64" — focuses on the capabilities and measured performance of an existing model.

### `dev_log`

**Definition:**
A post primarily documenting the development, implementation, or capabilities of a specific software project created by the author.
**Example 1:**
>"Building ora-tui with Google Antigravity & Gemini 4 Argon: An MS-DOS Retro TUI & OpenTelemetry Exporter for Oracle RAC, DB & SAN Multipath" — documents the author's own project and its implementation.

**Example 2:**
>"DuckLess: serverless DuckDB on Google Cloud, in your own project" — presents a tool the author built and how it works.

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

Neither label is above the 70% limit, but `informative` is 62.4%, so the
dataset misses my stricter 60% balance target. There are no duplicate posts.

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

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate `2e-5`, batch size 16, seed 42,
maximum sequence length 128 tokens.

**Anything I changed from the defaults, and why:** Nothing. I used the
notebook's default training settings.

**Split sizes:**

Train: 174; validation: 38; test: 38. The test set contains 24 `informative`
and 14 `dev_log` posts; neither label is below eight examples.

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
- *What I changed:* I treated the labels as a first pass and am spot-checking them against the full text, because the AI only read previews. Borderline posts, such as benchmark write-ups of existing tech versus write-ups of the author's own tool, are the ones I am checking most closely. I have not yet completed a full review of all 250 posts, and I do not have a verified count of labels checked or changed.

**Pre-labelling disclosure:** Yes, I did not label the data cold. GitHub Copilot pre-labelled all 250 posts from their titles and openings, using the definitions and decision rule above. It did not read every post in full. I am still reviewing and correcting them; the full review is not complete.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.605 | 0.632 | +0.026 |
| Macro F1 | 0.553 | 0.387 | -0.166 |
| F1 — `informative` | 0.706 | 0.774 | +0.068 |
| F1 — `dev_log` | 0.400 | 0.000 | -0.400 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->
I predict my fine-tuned model will outperform the baseline when distinguishing informative posts from dev_log posts that contain technical explanations, because it was trained on examples reflecting my taxonomy.

**What the gap actually means:**
Fine-tuning raised accuracy by only 2.6 percentage points, while macro F1
dropped by 16.6 points. The trained model predicted every test post as
`informative`: it improved that label's F1 but failed completely on `dev_log`.
So the small accuracy gain hides a serious failure on one class.


---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥75% | 63.2% | 63.2% | 63.2% | Missed |
| 2. `informative` F1 | ≥0.70 | 0.774 | 0.774 | 0.774 | Met |
| 3. `dev_log` F1 | ≥0.70 | 0.000 | 0.000 | 0.000 | Missed |
| 4. Dataset label balance | ≤60% per label | 62.4% | 62.4% | 62.4% | Missed |
| 5. Classification consistency | ≥85% agreement | 100% | 100% | 100% | Met |

The consistency result is one fixed 30-post staff comparison, not three
independent runs; it is repeated in the columns because the measure does not
depend on the training seed.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| True \ Predicted | `informative` | `dev_log` |
|---|---:|---:|
| `informative` | 24 | 0 |
| `dev_log` | 14 | 0 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

All 14 actual `dev_log` posts were predicted as `informative`, while no
`informative` posts were predicted as `dev_log`. The model did not learn the
`dev_log` side of this boundary at all on this test set.

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥75% | Missed | All three seeds scored 63.2%. |
| 2 | `informative` F1 | ≥0.70 | Met | All three seeds scored 0.774. |
| 3 | `dev_log` F1 | ≥0.70 | Missed | All three seeds scored 0.000. |
| 4 | Dataset label balance | ≤60% per label | Missed | `informative` is 62.4% of the 250 posts. |
| 5 | Classification consistency | ≥85% agreement | Met | Agreement report: 30 of 30 staff-taxonomy posts matched. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Accuracy and `dev_log` performance:** The repeated result across all three
seeds is a systematic `informative`-only prediction, not a one-seed fluctuation.
There were 14 `dev_log` examples in each test split, so the zero F1 is not due
to having fewer than eight test examples. The dataset is also over my balance
limit (`informative` is 62.4%); that imbalance may contribute, but it does not
by itself prove the cause. Posts can be very long while the model reads at
most 128 tokens, so truncation may hide project-specific details. This is a
plausible cause to test, not a confirmed diagnosis.

**Consistency evidence and its limit:** I matched the staff labels on all 30
posts under the separate staff taxonomy, exceeding the 85% target. This is
evidence that I could apply that written taxonomy on this sample; it does not
validate my `informative`/`dev_log` labels, which use a different taxonomy.
The staff agreement result therefore cannot explain away the model's failure
on `dev_log`.

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = 100%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**
No disagreements were reported between my submitted labels and the staff reference labels.

**What the pattern in my disagreements tells me:**

There were no disagreements to adjudicate: my labels matched the staff
reference on all 30 posts. That is a perfect result on this sample, but it
does not independently establish that the taxonomy is always clear or that my
separate project labels are consistent.

---

## The Improvement

**What I changed:** No improvement run is recorded yet. I have not changed
the training setup or produced an after-run results file, so I cannot claim
that a fix helped.

**Which diagnosis pointed at it:** The model predicts every test post as
`informative` and has 0.000 `dev_log` F1 across all three seeds. A next
experiment should address the `dev_log` false negatives and test whether
longer input or a training adjustment helps, while keeping the same held-out
evaluation protocol.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥75% | Not run | Not run | Not run | Pending |
| 2. `informative` F1 | ≥0.70 | Not run | Not run | Not run | Pending |
| 3. `dev_log` F1 | ≥0.70 | Not run | Not run | Not run | Pending |
| 4. Dataset label balance | ≤60% per label | Not changed | Not changed | Not changed | Missed |
| 5. Classification consistency | ≥85% agreement | Not retested | Not retested | Not retested | Pending |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

I cannot tell yet because no after run has been completed. The before-run
results remain the only measured model results.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

The overall-accuracy and `dev_log` F1 targets remain missed. I would first
review the `dev_log` examples and experiment with giving the model more of
each post than the current 128-token limit, then rerun all three seeds. I
would also bring the dataset within the 60% balance target by collecting and
reviewing more `dev_log` posts rather than relabelling examples just to change
the ratio. These follow-up experiments have not been run yet, so I am not
claiming they will fix the problem.

**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->

I meant `dev_log` to identify posts centered on the author's own software
project, but the model labeled every held-out post `informative`. It therefore
did not learn the distinction I intended, even though it correctly identified
all 24 informative examples in this test split.

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
