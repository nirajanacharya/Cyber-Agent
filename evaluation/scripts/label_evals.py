"""Simple Streamlit labeling app for evaluation results."""

import csv
import json
from pathlib import Path

import streamlit as st

RESULTS_PATH = Path("evaluation/data/results.jsonl")
LABELS_PATH = Path("evaluation/data/labels.csv")


FAILURE_CATEGORIES = [
    "hallucination",
    "wrong_scope",
    "incomplete",
    "wrong_tool",
    "unsafe",
    "other",
]


@st.cache_data(show_spinner=False)
def load_results(path: Path):
    rows = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))
    return rows


@st.cache_data(show_spinner=False)
def load_labels(path: Path):
    data = {}
    if not path.exists():
        return data
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            data[int(row["scenario_id"])] = row
    return data


def save_labels(path: Path, labels: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["scenario_id", "label", "failure_category", "notes"]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for scenario_id in sorted(labels):
            writer.writerow(labels[scenario_id])
    load_labels.clear()


def main():
    st.set_page_config(page_title="Cyber Sachet Labeling", layout="wide")
    st.title("Label Evaluation Results")

    results = load_results(RESULTS_PATH)
    if not results:
        st.warning("No results found. Run batch_run.py first.")
        return

    if "labels_map" not in st.session_state:
        st.session_state.labels_map = load_labels(LABELS_PATH)
    labels = st.session_state.labels_map

    if "idx" not in st.session_state:
        st.session_state.idx = 0

    total = len(results)
    st.caption(f"Item {st.session_state.idx + 1} of {total}")
    row = results[st.session_state.idx]

    st.subheader("Question")
    st.write(row.get("question", ""))

    st.subheader("Response")
    st.write(row.get("answer", ""))

    st.subheader("Retrieved Context (top 3)")
    search_results = row.get("search_results", [])[:3]
    for i, hit in enumerate(search_results, start=1):
        with st.expander(f"Context {i}: {hit.get('source', 'unknown')}"):
            st.write(hit.get("content", ""))

    current = labels.get(row["scenario_id"], {})
    default_label = current.get("label", "good")
    default_failure = current.get("failure_category", "")
    default_notes = current.get("notes", "")

    label = st.radio("Label", ["good", "bad"], index=0 if default_label == "good" else 1)
    failure_category = ""
    if label == "bad":
        failure_category = st.selectbox(
            "Failure category",
            FAILURE_CATEGORIES,
            index=FAILURE_CATEGORIES.index(default_failure) if default_failure in FAILURE_CATEGORIES else 0,
        )

    notes = st.text_area("Notes", value=default_notes, height=80)

    col1, col2, col3 = st.columns(3)
    if col1.button("Save Label", use_container_width=True):
        labels[row["scenario_id"]] = {
            "scenario_id": row["scenario_id"],
            "label": label,
            "failure_category": failure_category,
            "notes": notes,
        }
        st.session_state.labels_map = labels
        save_labels(LABELS_PATH, labels)
        st.success("Saved")

    if col2.button("Previous", use_container_width=True) and st.session_state.idx > 0:
        st.session_state.idx -= 1
        st.rerun()

    if col3.button("Next", use_container_width=True) and st.session_state.idx < total - 1:
        st.session_state.idx += 1
        st.rerun()


if __name__ == "__main__":
    main()
