"""LLM judge for good/bad response quality classification."""

import json
from dataclasses import dataclass

from openai import AsyncOpenAI


@dataclass
class JudgeOutput:
    reasoning: str
    label: str


def build_judge_prompt(version: str, frequent_failures: list[str] | None = None) -> str:
    base = (
        "You are an evaluation judge for a Cyber Security + Nepal cyber law assistant. "
        "Return JSON with fields: reasoning, label. Label must be 'good' or 'bad'. "
        "A good response is accurate, in-scope, useful, and avoids fabrication. "
        "A bad response includes wrong legal claims, missing key action steps, wrong scope, "
        "unsafe advice, or unsupported certainty."
    )
    if version == "v1":
        return base

    failures = ", ".join(frequent_failures or [])
    return (
        base
        + " Prioritize these frequent failure types seen in human labels: "
        + (failures if failures else "hallucination, wrong_scope, incomplete")
        + ". Be strict about legal certainty and source-grounded claims."
    )


async def judge_response(
    client: AsyncOpenAI,
    question: str,
    answer: str,
    prompt_version: str = "v1",
    frequent_failures: list[str] | None = None,
    model: str = "gpt-4o-mini",
) -> JudgeOutput:
    system_prompt = build_judge_prompt(prompt_version, frequent_failures)
    user_prompt = f"Question:\n{question}\n\nResponse:\n{answer}"

    resp = await client.chat.completions.create(
        model=model,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    payload = json.loads(resp.choices[0].message.content)
    label = payload.get("label", "bad").strip().lower()
    if label not in {"good", "bad"}:
        label = "bad"

    return JudgeOutput(
        reasoning=payload.get("reasoning", ""),
        label=label,
    )
