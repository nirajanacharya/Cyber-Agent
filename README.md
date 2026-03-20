# Cyber Sachet

Cyber Sachet is a bilingual AI assistant focused on cyber security awareness and Nepal cyber law guidance. It answers user questions in English and Nepali with retrieval-augmented generation (RAG), cites sources from a local knowledge base, tracks usage with monitoring, and includes a full evaluation pipeline with human labels and an LLM judge.

## Problem Statement: Current Condition in Nepal

Nepal is experiencing rapid digital adoption through smartphones, social media, digital payments, online services, and remote communication. This has improved access and convenience, but it has also expanded the cyber risk surface for everyday users, students, small businesses, and first-time internet users.

Current on-ground challenges include:
- low practical awareness of phishing, account takeover, social engineering, and online fraud patterns,
- fragmented and inconsistent cyber safety guidance across sources,
- legal confusion around what is punishable under Nepal cyber law,
- language accessibility gaps where many users understand advice better in Nepali than in English-only technical explanations,
- delayed or missing incident reporting because users are unsure what happened, what evidence to keep, and what legal path to follow.

At the same time, legal references such as the Information Technology Act, 2063 and newer digital security-related provisions are not always easy to interpret for non-legal audiences. Users often need clear, context-aware, and locally relevant explanations rather than generic global cyber tips.

This project solves that by:
- grounding responses in a domain knowledge base,
- selecting tools based on user intent (awareness vs legal/penalty),
- responding bilingually (English and Nepali) based on user preference,
- generating clear responses with source references,
- evaluating quality using a gold-style scenario set, manual labels, and a judge model.

## Key Features

- Multi-tool agent with intent-based tool selection
- Bilingual response capability (English and Nepali)
- Knowledge base retrieval from local domain documents
- Structured response metadata (sources, tools used, context docs, timing)
- Monitoring with Logfire spans, token/cost estimation, and user feedback hooks
- Evaluation pipeline:
  - scenario dataset
  - batch run outputs
  - manual labeling app
  - judge validation with accuracy/precision/recall and iteration report

## Project Structure

- cyber_sachet/: core agent, tools, database utilities, models
- docs/: source knowledge documents
- streamlit_app/: main interactive app UI
- monitoring/: observability wrappers and dashboard integration
- evaluation/: scenario, labeling, judge, and reports
  - data/: scenarios, batch outputs, human labels
  - scripts/: modular evaluation scripts
  - reports/: judge metrics and iteration artifacts
  - notebooks/: notebook-first workflow
- tests/: unit and judge-oriented tests

## Knowledge Base and Retrieval

Knowledge base files:
- docs/cyber_awareness_guide.txt
- docs/nepal_information_technology_act_2063.txt
- docs/nepal_digital_security_act_2024.txt

Retrieval setup:
- Vector store: ChromaDB
- Embeddings: text-embedding-3-small
- Tools:
  - semantic_search_tool (general)
  - search_laws_tool (law-filtered)
  - search_awareness_tool (awareness-filtered)
  - check_penalty_tool (penalty-focused helper)

Current best operational approach in this codebase:
- use intent-based tool selection (legal and penalty queries route to legal tools, awareness queries route to awareness tools),
- fallback to semantic search for broad/unclear queries.

This approach is used by the active agent pipeline and validated through test coverage and evaluation outputs.

## Agent and Tools

LLM:
- OpenAI chat model (default gpt-4o-mini)

Agent workflow:
1. Detect intent from question
2. Select one or more retrieval tools
3. Build grounded context
4. Generate answer with citations
5. Return metadata for tracing/evaluation

## Setup

### Prerequisites

- Python 3.13+
- OpenAI API key
- Logfire token (for monitoring)

### Environment

Create .env in project root:
- OPENAI_API_KEY=your_openai_key_here
- LOGFIRE_TOKEN=your_logfire_write_token_here

A template is provided in .env.example.

### Install

Option A: pip

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Option B: uv (already present in project)

```powershell
uv sync
```

## Run the Main App

```powershell
python run_app.py
```

Or:

```powershell
streamlit run streamlit_app/app.py
```

## Monitoring

Monitoring is implemented in monitoring/ using Logfire:
- query spans and timing
- estimated tokens/cost
- session-level stats
- feedback collector hooks

Quick check:

```powershell
python check_monitoring.py
```

If configured, logs are visible in the Logfire dashboard associated with your token.

## Testing

Run tests:

```powershell
pytest -q
```

Test categories include:
- agent behavior tests
- tool/citation tests
- LLM judge-oriented tests

## Evaluation Pipeline

### 1) Scenario Design and Batch Run

```powershell
python -m evaluation.scripts.batch_run --scenarios evaluation/data/scenarios.csv --out evaluation/data
```

Outputs:
- evaluation/data/results.jsonl
- evaluation/data/results.csv

### 2) Manual Labeling Tool (Streamlit)

```powershell
streamlit run evaluation/scripts/label_evals.py
```

Label each response as good/bad, assign failure category for bad rows, and save to:
- evaluation/data/labels.csv

### 3) Judge Validation

```powershell
python -m evaluation.scripts.validate_judge --results evaluation/data/results.jsonl --labels evaluation/data/labels.csv --out evaluation/reports
```

Outputs:
- evaluation/reports/judge_metrics.json
- evaluation/reports/judge_iteration_report.json
- evaluation/reports/judge_predictions_v1.csv
- evaluation/reports/judge_predictions_v2.csv

### 4) Label Summary

```powershell
python -m evaluation.scripts.summarize_labels
```

## Current Evaluation Snapshot

From current reports:
- v1: accuracy 0.75, precision_bad 1.00, recall_bad 0.1667
- v2: accuracy 0.70, precision_bad 0.50, recall_bad 0.3333
- fixed disagreement example recorded in judge_iteration_report.json

## Reproducibility Notes

- All required local data files are included in docs/ and evaluation/data/
- .env is ignored by git; use .env.example for template
- Evaluation and app commands are listed above for end-to-end rerun

