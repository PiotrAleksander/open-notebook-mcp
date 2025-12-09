#!/usr/bin/env python3
"""
Example usage of the Open Notebook MCP Server tools.

This script demonstrates how to use the server's tools programmatically.
Note: This requires a running Open Notebook instance.
"""

import asyncio
import os
from open_notebook_mcp.server import (
    search_capabilities,
    list_notebooks,
    create_notebook,
    list_models,
)


async def main():
    """Run examples."""
    print("=== Open Notebook MCP Server Examples ===\n")
    
    # Check configuration
    base_url = os.getenv("OPEN_NOTEBOOK_URL", "http://localhost:5055")
    print(f"📍 Connecting to: {base_url}")
    print(f"🔐 Authentication: {'Enabled' if os.getenv('OPEN_NOTEBOOK_PASSWORD') else 'Disabled'}")
    print()
    
    # Example 1: Discover available tools
    print("--- Example 1: Discover Tools ---")
    result = search_capabilities(query="", detail="name", limit=10)
    print(f"Found {result['count']} tools:")
    for tool in result['matches']:
        print(f"  - {tool['name']}")
    print()
    
    # Example 2: Search for specific functionality
    print("--- Example 2: Search for Notebook Tools ---")
    result = search_capabilities(query="notebook", detail="summary", limit=5)
    print(f"Found {result['count']} notebook-related tools:")
    for tool in result['matches']:
        print(f"  - {tool['name']}: {tool['summary']}")
    print()
    
    # Example 3: Get detailed information about a tool
    print("--- Example 3: Get Tool Details ---")
    result = search_capabilities(query="create_notebook", detail="full", limit=1)
    if result['matches']:
        tool = result['matches'][0]
        print(f"Tool: {tool['name']}")
        print(f"Summary: {tool['summary']}")
        print(f"Arguments: {tool['args']}")
        print(f"Example: {tool['example']}")
    print()
    
    # Example 4: List notebooks (requires Open Notebook to be running)
    print("--- Example 4: List Notebooks ---")
    print("Note: This requires a running Open Notebook instance")
    try:
        result = await list_notebooks(limit=5)
        print(f"Found {result['count']} notebooks")
        if result['notebooks']:
            for nb in result['notebooks'][:3]:
                print(f"  - {nb.get('name', 'Unnamed')}: {nb.get('id', 'No ID')}")
        else:
            print("  (No notebooks found)")
    except Exception as e:
        print(f"  ⚠️  Could not connect: {e}")
        print(f"  Make sure Open Notebook is running at {base_url}")
    print()
    
    # Example 5: List models (requires Open Notebook to be running)
    print("--- Example 5: List AI Models ---")
    try:
        result = await list_models(limit=5)
        print(f"Found {result['count']} models")
        if result['models']:
            for model in result['models'][:3]:
                print(f"  - {model.get('name', 'Unnamed')}: {model.get('provider', 'Unknown provider')}")
        else:
            print("  (No models configured)")
    except Exception as e:
        print(f"  ⚠️  Could not connect: {e}")
    print()
    
    print("=== Examples Complete ===")
    print("\nTip: Set OPEN_NOTEBOOK_URL and OPEN_NOTEBOOK_PASSWORD environment variables")
    print("     to connect to your Open Notebook instance.")


if __name__ == "__main__":
    asyncio.run(main())
