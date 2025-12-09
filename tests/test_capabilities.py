"""Tests for the Open Notebook MCP server."""

from open_notebook_mcp.server import CAPABILITIES, search_capabilities


def test_capabilities_defined():
    """Test that all capabilities are properly defined."""
    assert len(CAPABILITIES) > 0, "No capabilities defined"
    
    # Check that all capabilities have required fields
    for cap in CAPABILITIES:
        assert cap.name, f"Missing name for capability"
        assert cap.summary, f"Missing summary for {cap.name}"
        assert cap.tags, f"Missing tags for {cap.name}"
        assert cap.args is not None, f"Missing args for {cap.name}"
        assert cap.returns, f"Missing returns for {cap.name}"
        assert cap.example is not None, f"Missing example for {cap.name}"
        assert cap.typical_bytes > 0, f"Missing typical_bytes for {cap.name}"


def test_search_capabilities_basic():
    """Test basic search_capabilities functionality."""
    result = search_capabilities(query="", detail="name", limit=50)
    
    assert "request_id" in result
    assert "count" in result
    assert "matches" in result
    assert result["count"] > 0
    assert len(result["matches"]) == result["count"]


def test_search_capabilities_query():
    """Test search_capabilities with query."""
    # Search for notebook-related tools
    result = search_capabilities(query="notebook", detail="summary", limit=10)
    assert result["count"] > 0
    
    # All matches should have notebook-related content
    for match in result["matches"]:
        assert "name" in match
        assert "summary" in match
        assert "tags" in match


def test_search_capabilities_detail_levels():
    """Test different detail levels."""
    # Name only
    result = search_capabilities(query="", detail="name", limit=1)
    assert len(result["matches"]) == 1
    match = result["matches"][0]
    assert "name" in match
    assert "summary" not in match
    
    # Summary
    result = search_capabilities(query="", detail="summary", limit=1)
    match = result["matches"][0]
    assert "name" in match
    assert "summary" in match
    assert "tags" in match
    assert "args" not in match
    
    # Full
    result = search_capabilities(query="", detail="full", limit=1)
    match = result["matches"][0]
    assert "name" in match
    assert "summary" in match
    assert "tags" in match
    assert "args" in match
    assert "returns" in match
    assert "example" in match


def test_search_capabilities_limit():
    """Test that limit parameter is respected."""
    result = search_capabilities(query="", detail="name", limit=5)
    assert result["count"] <= 5
    assert len(result["matches"]) <= 5
    
    result = search_capabilities(query="", detail="name", limit=100)
    # Should be capped at 50
    assert result["count"] <= 50


if __name__ == "__main__":
    # Run tests
    test_capabilities_defined()
    print("✓ test_capabilities_defined passed")
    
    test_search_capabilities_basic()
    print("✓ test_search_capabilities_basic passed")
    
    test_search_capabilities_query()
    print("✓ test_search_capabilities_query passed")
    
    test_search_capabilities_detail_levels()
    print("✓ test_search_capabilities_detail_levels passed")
    
    test_search_capabilities_limit()
    print("✓ test_search_capabilities_limit passed")
    
    print("\n✅ All tests passed!")
