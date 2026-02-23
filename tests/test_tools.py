"""Tool functionality tests."""

import pytest
from cyber_sachet.models.search_result import SearchResult


class TestTools:
    """Test suite for CyberSachetTools."""
    
    @pytest.mark.asyncio
    async def test_semantic_search_tool_basic(self, tools):
        """Test basic semantic search functionality."""
        results = await tools.semantic_search_tool("cyber security", n_results=3)
        
        assert len(results) > 0, "Should return at least one result"
        assert len(results) <= 3, "Should not exceed requested number of results"
        
        for result in results:
            assert isinstance(result, SearchResult)
            assert result.content
            assert result.source
            assert result.doc_type in ["cyber_law", "awareness"]
            assert 0 <= result.relevance_score <= 1
    
    @pytest.mark.asyncio
    async def test_search_laws_tool_filters_correctly(self, tools):
        """Test that search_laws_tool only returns legal documents."""
        results = await tools.search_laws_tool("penalty", n_results=5)
        
        for result in results:
            assert result.doc_type == "cyber_law", \
                f"Expected cyber_law, got {result.doc_type} from {result.source}"
    
    @pytest.mark.asyncio
    async def test_search_awareness_tool_filters_correctly(self, tools):
        """Test that search_awareness_tool only returns awareness documents."""
        results = await tools.search_awareness_tool("password security", n_results=5)
        
        for result in results:
            assert result.doc_type == "awareness", \
                f"Expected awareness, got {result.doc_type} from {result.source}"
    
    @pytest.mark.asyncio
    async def test_get_document_sources_tool(self, tools):
        """Test document sources metadata retrieval."""
        sources = await tools.get_document_sources_tool()
        
        assert "total_documents" in sources
        assert "total_chunks" in sources
        assert "sources" in sources
        assert sources["total_documents"] > 0
        assert sources["total_chunks"] > 0
        assert len(sources["sources"]) == sources["total_documents"]
    
    @pytest.mark.asyncio
    async def test_check_penalty_tool(self, tools):
        """Test penalty lookup tool."""
        penalty_info = await tools.check_penalty_tool("hacking")
        
        assert "crime_type" in penalty_info
        assert penalty_info["crime_type"] == "hacking"
        assert "found" in penalty_info
        assert "details" in penalty_info
        assert "sources" in penalty_info
        
        if penalty_info["found"]:
            assert len(penalty_info["details"]) > 0
            assert len(penalty_info["sources"]) > 0
    
    @pytest.mark.asyncio
    async def test_tool_call_logging(self, tools):
        """Test that tool calls are logged correctly."""
        tools.clear_history()
        
        await tools.semantic_search_tool("test query", n_results=2)
        
        history = tools.get_tool_call_history()
        assert len(history) == 1
        assert history[0].tool_name == "semantic_search_tool"
        assert "query" in history[0].args
        assert history[0].duration_ms > 0
    
    @pytest.mark.asyncio
    async def test_min_relevance_filter(self, tools):
        """Test minimum relevance score filtering."""
        results = await tools.semantic_search_tool(
            "irrelevant query xyz123abc",
            n_results=10,
            min_relevance=0.7
        )
        
        for result in results:
            assert result.relevance_score >= 0.7
