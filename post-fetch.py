
import csv
import time

import requests

API = "https://dev.to/api/articles"
TARGET = 220  # comfortably above the 200-post minimum
MAX_PAGES = 20
OUTPUT = "labels.csv"

session = requests.Session()
session.headers["User-Agent"] = "takemeter-class-project"


def get_json(url, **params):
    for attempt in range(3):
        response = session.get(url, params=params, timeout=20)
        if response.status_code == 429:
            time.sleep(2 ** attempt * 2)
            continue
        response.raise_for_status()
        return response.json()
    response.raise_for_status()


rows = []
seen_ids = set()
seen_text = set()

for page in range(1, MAX_PAGES + 1):
    if len(rows) >= TARGET:
        break
    for item in get_json(API, per_page=30, page=page):
        if len(rows) >= TARGET:
            break
        if item["id"] in seen_ids:
            continue
        seen_ids.add(item["id"])

        # The list endpoint omits the body; fetch the whole post.
        full = get_json(f"{API}/{item['id']}")
        body = (full.get("body_markdown") or "").strip()
        if not body:
            continue

        text = f"{full['title']}\n\n{body}"
        if text in seen_text:
            continue
        seen_text.add(text)

        # label is filled in by hand; note keeps the source for traceability.
        rows.append({"text": text, "label": "", "note": full["url"]})
        time.sleep(0.3)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "label", "note"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} full posts to {OUTPUT} (unsplit, labels blank)")
