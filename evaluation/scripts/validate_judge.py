"""Validate LLM judge against human labels and compare prompt versions."""

import argparse
import asyncio
import csv
import json
import os
from collections import Counter
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from evaluation.scripts.judge import judge_response


def read_jsonl(path: Path):
    rows = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            rows[int(row["scenario_id"])] = row
    return rows


def read_labels(path: Path):
    labels = []
    if not path.exists():
        return labels
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            labels.append(
                {
                    "scenario_id": int(row["scenario_id"]),
                    "label": row["label"].strip().lower(),
                    "failure_category": row.get("failure_category", "").strip().lower(),
                    "notes": row.get("notes", ""),
                }
            )
    return labels


def metrics(gold: list[str], pred: list[str]):
    tp = sum(1 for g, p in zip(gold, pred) if g == "bad" and p == "bad")
    tn = sum(1 for g, p in zip(gold, pred) if g == "good" and p == "good")
    fp = sum(1 for g, p in zip(gold, pred) if g == "good" and p == "bad")
    fn = sum(1 for g, p in zip(gold, pred) if g == "bad" and p == "good")

    total = max(len(gold), 1)
    acc = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {
        "accuracy": round(acc, 4),
        "precision_bad": round(precision, 4),
        "recall_bad": round(recall, 4),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


async def score_version(client, labeled_rows, results_by_id, version: str, frequent_failures: list[str]):
    predictions = []
    for row in labeled_rows:
        result = results_by_id.get(row["scenario_id"])
        if not result:
            continue
        judged = await judge_response(
            client=client,
            question=result["question"],
            answer=result.get("answer", ""),
            prompt_version=version,
            frequent_failures=frequent_failures,
        )
        predictions.append(
            {
                "scenario_id": row["scenario_id"],
                "gold_label": row["label"],
                "judge_label": judged.label,
                "reasoning": judged.reasoning,
                "question": result["question"],
            }
        )

    gold = [p["gold_label"] for p in predictions]
    pred = [p["judge_label"] for p in predictions]
    return predictions, metrics(gold, pred)


def write_predictions(path: Path, rows):
    fieldnames = ["scenario_id", "gold_label", "judge_label", "question", "reasoning"]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def build_iteration_report(
    report_path: Path,
    m1: dict,
    m2: dict,
    v1_rows: list[dict],
    v2_rows: list[dict],
):
    fixed_example = None
    by_id_v1 = {r["scenario_id"]: r for r in v1_rows}
    for row in v2_rows:
        old = by_id_v1.get(row["scenario_id"])
        if old and old["judge_label"] != old["gold_label"] and row["judge_label"] == row["gold_label"]:
            fixed_example = {
                "scenario_id": row["scenario_id"],
                "question": row["question"],
                "gold": row["gold_label"],
                "v1": old["judge_label"],
                "v2": row["judge_label"],
            }
            break

    report = {
        "v1": m1,
        "v2": m2,
        "fixed_disagreement_example": fixed_example,
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


async def main_async(results_path: Path, labels_path: Path, out_dir: Path):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found")

    results_by_id = read_jsonl(results_path)
    labeled_rows = read_labels(labels_path)

    if len(labeled_rows) < 15:
        raise ValueError("Label at least 15 rows in labels.csv before judge validation")

    failure_counts = Counter(r["failure_category"] for r in labeled_rows if r["label"] == "bad" and r["failure_category"])
    frequent_failures = [k for k, _ in failure_counts.most_common(3)]

    client = AsyncOpenAI(api_key=api_key)

    v1_rows, m1 = await score_version(client, labeled_rows, results_by_id, "v1", frequent_failures)
    v2_rows, m2 = await score_version(client, labeled_rows, results_by_id, "v2", frequent_failures)

    out_dir.mkdir(parents=True, exist_ok=True)
    write_predictions(out_dir / "judge_predictions_v1.csv", v1_rows)
    write_predictions(out_dir / "judge_predictions_v2.csv", v2_rows)

    (out_dir / "judge_metrics.json").write_text(
        json.dumps({"v1": m1, "v2": m2, "frequent_failures": frequent_failures}, indent=2),
        encoding="utf-8",
    )
    build_iteration_report(out_dir / "judge_iteration_report.json", m1, m2, v1_rows, v2_rows)

    print("Judge validation complete")
    print(json.dumps({"v1": m1, "v2": m2}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default="evaluation/data/results.jsonl")
    parser.add_argument("--labels", default="evaluation/data/labels.csv")
    parser.add_argument("--out", default="evaluation/reports")
    args = parser.parse_args()

    asyncio.run(main_async(Path(args.results), Path(args.labels), Path(args.out)))


if __name__ == "__main__":
    main()
