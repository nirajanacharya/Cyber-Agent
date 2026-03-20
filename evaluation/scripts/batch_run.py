"""Run evaluation scenarios in batch and save results."""

import argparse
import asyncio
import csv
import json
from datetime import datetime
from pathlib import Path

from evaluation.common import create_eval_agent


def _read_scenarios(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_jsonl(path: Path, rows):
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _write_csv(path: Path, rows):
    if not rows:
        return
    keys = [
        "scenario_id",
        "question",
        "category",
        "type",
        "answer",
        "tools_used",
        "sources_used",
        "num_context_docs",
        "status",
        "error",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "scenario_id": row.get("scenario_id"),
                "question": row.get("question", ""),
                "category": row.get("category", ""),
                "type": row.get("type", ""),
                "answer": row.get("answer", ""),
                "tools_used": ", ".join(row.get("tools_used", [])),
                "sources_used": ", ".join(row.get("sources_used", [])),
                "num_context_docs": row.get("num_context_docs", 0),
                "status": row.get("status", "ok"),
                "error": row.get("error", ""),
            })


async def run_batch(scenarios_path: Path, out_dir: Path, model: str, limit: int | None):
    scenarios = _read_scenarios(scenarios_path)
    if limit:
        scenarios = scenarios[:limit]

    agent = create_eval_agent()
    results = []

    for idx, scenario in enumerate(scenarios, start=1):
        question = scenario["question"].strip()
        category = scenario.get("category", "")
        s_type = scenario.get("type", "")

        print(f"[{idx}/{len(scenarios)}] {question[:80]}")
        try:
            result = await agent.query(
                question,
                verbose=False,
                model=model,
                temperature=0.2,
            )
            results.append(
                {
                    "scenario_id": idx,
                    "question": question,
                    "category": category,
                    "type": s_type,
                    "answer": result["answer"],
                    "tools_used": result.get("tools_used", []),
                    "sources_used": result.get("sources_used", []),
                    "num_context_docs": result.get("num_context_docs", 0),
                    "search_results": result.get("search_results", []),
                    "timestamp": datetime.now().isoformat(),
                    "status": "ok",
                    "error": "",
                }
            )
        except Exception as e:
            results.append(
                {
                    "scenario_id": idx,
                    "question": question,
                    "category": category,
                    "type": s_type,
                    "answer": "",
                    "tools_used": [],
                    "sources_used": [],
                    "num_context_docs": 0,
                    "search_results": [],
                    "timestamp": datetime.now().isoformat(),
                    "status": "error",
                    "error": str(e),
                }
            )

    out_dir.mkdir(parents=True, exist_ok=True)
    _write_jsonl(out_dir / "results.jsonl", results)
    _write_csv(out_dir / "results.csv", results)

    print(f"Saved {len(results)} rows to {out_dir}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", default="evaluation/data/scenarios.csv")
    parser.add_argument("--out", default="evaluation/data")
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    asyncio.run(
        run_batch(
            scenarios_path=Path(args.scenarios),
            out_dir=Path(args.out),
            model=args.model,
            limit=args.limit,
        )
    )


if __name__ == "__main__":
    main()
