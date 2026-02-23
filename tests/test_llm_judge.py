

import pytest
import json
from typing import List, Dict, Any
from openai import AsyncOpenAI


async def assert_criteria(
    result: str,
    criteria: List[str],
    context: Dict[str, Any],
    openai_client: AsyncOpenAI
) -> Dict[str, Any]:
    """
    LLM judge to evaluate if result meets specified criteria.
    
    Args:
        result: The text to evaluate (agent's answer)
        criteria: List of criteria to check
        context: Context information (query metadata, tool calls, etc.)
        openai_client: AsyncOpenAI client
    
    Returns:
        Dict with evaluation results
    
    Raises:
        AssertionError: If any criteria not met
    """
    context_str = f"\n\nContext Information:\n{json.dumps(context, indent=2, default=str)}"
    criteria_text = "\n".join([f"{i+1}. {c}" for i, c in enumerate(criteria)])
    
    eval_prompt = f"""You are an expert evaluator for an AI agent. Evaluate if the following result meets ALL specified criteria.

RESULT TO EVALUATE:
{result}
{context_str}

CRITERIA TO CHECK:
{criteria_text}

For each criterion, determine if it is MET or NOT MET. Be strict and precise in your evaluation.

Respond in JSON format:
{{
  "overall_pass": true/false,
  "criteria_results": [
    {{
      "criterion": "<criterion text>",
      "met": true/false,
      "explanation": "<detailed explanation of why it passed or failed>"
    }}
  ],
  "summary": "<overall assessment>"
}}"""
    
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": eval_prompt}],
        temperature=0.2,
        response_format={"type": "json_object"}
    )
    
    evaluation = json.loads(response.choices[0].message.content)
    
    if not evaluation["overall_pass"]:
        failed_criteria = [c for c in evaluation["criteria_results"] if not c["met"]]
        raise AssertionError(
            "Criteria not met:\n" +
            "\n".join([
                f"  X {c['criterion']}\n    Reason: {c['explanation']}"
                for c in failed_criteria
            ])
        )
    
    return evaluation


class TestLLMJudge:
    """
    LLM Judge Tests - Question 3
    
    Tests using LLM judge with specific, concrete criteria.
    """
    
    @pytest.mark.asyncio
    async def test_legal_query_with_llm_judge(self, agent, openai_client):
        """
        Test legal query response quality with LLM judge.
        
        Uses 4 specific, concrete criteria to evaluate if the agent
        properly handles legal questions.
        """
        agent.clear_history()
        
        # Execute query
        result = await agent.query(
            "What are the penalties for unauthorized access to computer systems in Nepal?",
            verbose=False
        )
        
        criteria = [
            "The answer cites at least one source document in the format '[Source: filename]' or similar citation format",
            "The agent used either search_laws_tool or check_penalty_tool (not just generic semantic_search_tool) since this is a legal question about penalties",
            "The answer specifically mentions Nepal's cyber law (IT Act 2063 or Digital Security Act 2024) by name or year",
            "The answer provides specific penalty information (such as fines, imprisonment duration, etc.) not just generic statements about punishments"
        ]
        
        judge_context = {
            "tools_used": result['tools_used'],
            "sources_used": result['sources_used'],
            "question": result['question'],
            "num_context_docs": result['num_context_docs']
        }
        
        evaluation = await assert_criteria(
            result['answer'],
            criteria,
            judge_context,
            openai_client
        )
        
        assert evaluation["overall_pass"]
        
        assert len(evaluation["criteria_results"]) == len(criteria)
        for criterion_result in evaluation["criteria_results"]:
            assert criterion_result["met"], \
                f"Criterion failed: {criterion_result['criterion']}\n{criterion_result['explanation']}"
    
    @pytest.mark.asyncio
    async def test_awareness_query_with_llm_judge(self, agent, openai_client):
        """
        Test awareness query response quality with LLM judge.
        
        Uses specific criteria for security advice questions.
        """
        agent.clear_history()
        
        result = await agent.query(
            "How can I protect my online accounts from hackers?",
            verbose=False
        )
        
        criteria = [
            "The agent used search_awareness_tool (not search_laws_tool) since this is asking for practical security advice",
            "The answer provides at least 3 specific, actionable security recommendations",
            "The answer uses clear, non-technical language that a general user can understand",
            "The answer cites the source document where the advice comes from"
        ]
        
        judge_context = {
            "tools_used": result['tools_used'],
            "sources_used": result['sources_used'],
            "question": result['question']
        }
        
        evaluation = await assert_criteria(
            result['answer'],
            criteria,
            judge_context,
            openai_client
        )
        
        assert evaluation["overall_pass"]
    
    @pytest.mark.asyncio
    async def test_tool_selection_with_llm_judge(self, agent, openai_client):
        """
        Test that agent selects appropriate tools with LLM judge.
        
        Focuses on correct tool selection behavior.
        """
        agent.clear_history()
        
        result = await agent.query(
            "What is the punishment for stealing personal data in Nepal?",
            verbose=False
        )
        
        criteria = [
            "The agent called check_penalty_tool since the question explicitly asks about 'punishment'",
            "The agent used legal document search (search_laws_tool or check_penalty_tool) not awareness search",
            "The sources used include at least one legal document (containing 'act', 'law', '2063', or '2024' in filename)"
        ]
        
        judge_context = {
            "tools_used": result['tools_used'],
            "sources_used": result['sources_used'],
            "search_results": result['search_results'][:2]
        }
        
        evaluation = await assert_criteria(
            result['answer'],
            criteria,
            judge_context,
            openai_client
        )
        
        assert evaluation["overall_pass"]
