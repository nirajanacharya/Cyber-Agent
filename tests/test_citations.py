"""Source citation tests."""

import pytest


class TestSourceCitation:
    """
    Test Scenario 2: Source Citation Test
    
    Agent MUST cite sources in responses, especially for legal information.
    """
    
    @pytest.mark.asyncio
    async def test_agent_cites_sources_for_legal_query(self, agent):
        """Test that agent cites sources in legal answers."""
        agent.clear_history()
        
        result = await agent.query(
            "What are the penalties for unauthorized access to computer systems in Nepal?",
            verbose=False
        )
        
        answer = result["answer"]
        
        has_citation = (
            "[Source:" in answer or
            "[source:" in answer or
            "(Source:" in answer or
            "Source:" in answer
        )
        
        assert has_citation, \
            f"Answer should cite sources. Answer: {answer[:200]}..."
        
        assert len(result['sources_used']) > 0, \
            "Should have used at least one source"
    
    @pytest.mark.asyncio
    async def test_legal_answer_mentions_specific_law(self, agent):
        """Test that legal answers mention specific laws."""
        agent.clear_history()
        
        result = await agent.query(
            "What does the law say about cybercrime in Nepal?",
            verbose=False
        )
        
        answer_lower = result["answer"].lower()
        
        mentions_law = (
            "it act" in answer_lower or
            "information technology act" in answer_lower or
            "digital security act" in answer_lower or
            "2063" in answer_lower or
            "2024" in answer_lower
        )
        
        assert mentions_law, \
            f"Answer should mention specific Nepal cyber law. Answer: {result['answer'][:200]}..."
