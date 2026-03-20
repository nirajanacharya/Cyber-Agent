"""Summarize manual labels for failure pattern analysis."""

import csv
from collections import Counter
from pathlib import Path


LABELS_PATH = Path("evaluation/data/labels.csv")


def main():
    if not LABELS_PATH.exists():
        raise FileNotFoundError("labels.csv not found")

    with LABELS_PATH.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    good = sum(1 for r in rows if r["label"] == "good")
    bad_rows = [r for r in rows if r["label"] == "bad"]
    bad = len(bad_rows)

    failure_counts = Counter(r["failure_category"] for r in bad_rows if r["failure_category"])
    print(f"total_labeled={total}")
    print(f"good={good}")
    print(f"bad={bad}")
    print("failure_categories=")
    for cat, count in failure_counts.most_common():
        print(f"  - {cat}: {count}")


if __name__ == "__main__":
    main()
