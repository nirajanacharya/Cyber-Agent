"""Agent behavior tests."""

import pytest


class TestAgentBehavior:
    """Test suite for agent behavior and responses."""
    
    @pytest.mark.asyncio
    async def test_agent_responds_to_query(self, agent):
        """Test that agent can respond to a basic query."""
        agent.clear_history()
        
        result = await agent.query(
            "What is phishing?",
            verbose=False
        )
        
        assert "answer" in result
        assert len(result["answer"]) > 50
        assert "question" in result
        assert result["question"] == "What is phishing?"
    
    @pytest.mark.asyncio
    async def test_agent_uses_tools(self, agent):
        """Test that agent calls appropriate tools."""
        agent.clear_history()
        
        result = await agent.query(
            "What are the penalties for hacking?",
            verbose=False
        )
        
        assert "tools_used" in result
        assert len(result["tools_used"]) > 0
    
    @pytest.mark.asyncio
    async def test_agent_legal_query_uses_legal_tools(self, agent):
        """
        Test Scenario 1: Tool Selection for Legal Queries
        
        When users ask about laws or regulations, agent should use
        search_laws_tool or check_penalty_tool.
        """
        agent.clear_history()
        
        result = await agent.query(
            "What does Nepal's IT Act say about data privacy?",
            verbose=False
        )
        
        legal_tools = ['search_laws_tool', 'check_penalty_tool']
        assert any(tool in result['tools_used'] for tool in legal_tools), \
            f"Expected legal tools {legal_tools}, got {result['tools_used']}"
        
        assert len(result['sources_used']) > 0
        legal_doc_names = ['act', 'law', '2063', '2024']
        has_legal_source = any(
            any(name in source.lower() for name in legal_doc_names)
            for source in result['sources_used']
        )
        assert has_legal_source, f"Expected legal sources, got {result['sources_used']}"
    
    @pytest.mark.asyncio
    async def test_agent_awareness_query_uses_awareness_tools(self, agent):
        """
        Test Scenario 3: Awareness Tool Selection
        
        Security advice questions should use search_awareness_tool.
        """
        agent.clear_history()
        
        result = await agent.query(
            "How can I protect myself from phishing attacks?",
            verbose=False
        )
        
        assert 'search_awareness_tool' in result['tools_used'], \
            f"Expected search_awareness_tool, got {result['tools_used']}"
    
    @pytest.mark.asyncio
    async def test_agent_penalty_query_uses_penalty_tool(self, agent):
        """
        Test Scenario 5: Penalty Tool Sequence
        
        Penalty queries should call check_penalty_tool.
        """
        agent.clear_history()
        
        result = await agent.query(
            "What is the punishment for hacking in Nepal?",
            verbose=False
        )
        
        assert 'check_penalty_tool' in result['tools_used'], \
            f"Expected check_penalty_tool in {result['tools_used']}"
    
    @pytest.mark.asyncio
    async def test_agent_retrieves_sufficient_context(self, agent):
        """
        Test Scenario 4: Context Relevance
        
        Agent should retrieve adequate context documents.
        """
        agent.clear_history()
        
        result = await agent.query(
            "What are cyber security best practices?",
            n_context_docs=5,
            verbose=False
        )
        
        assert result['num_context_docs'] >= 3, \
            f"Expected at least 3 context docs, got {result['num_context_docs']}"
        
        for search_result in result['search_results']:
            assert search_result['relevance_score'] > 0.3, \
                f"Low relevance score: {search_result['relevance_score']}"
