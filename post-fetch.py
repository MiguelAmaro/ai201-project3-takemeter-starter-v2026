
import csv
import requests

articles = []
seen = set()

for page in range(1, 9):
    response = requests.get(
        "https://dev.to/api/articles",
        params={"per_page": 30, "page": page},
        timeout=20,
    )
    response.raise_for_status()

    for post in response.json():
        if post["id"] in seen:
            continue
        seen.add(post["id"])

        articles.append({
            "id": post["id"],
            "title": post["title"],
            "description": post.get("description", ""),
            "url": post["url"],
            "label": "",
            "note": "",
        })

with open("candidate_posts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=articles[0].keys())
    writer.writeheader()
    writer.writerows(articles)

print(f"Collected {len(articles)} candidate posts")
