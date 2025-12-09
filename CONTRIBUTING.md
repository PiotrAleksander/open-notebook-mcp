# Contributing to Open Notebook MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the Open Notebook MCP Server.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/PiotrAleksander/open-notebook-mcp.git
   cd open-notebook-mcp
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Open Notebook instance URL and password
   ```

## Project Structure

```
open-notebook-mcp/
├── src/
│   └── open_notebook_mcp/
│       ├── __init__.py         # Package entry point
│       └── server.py           # Main MCP server implementation
├── tests/
│   └── test_capabilities.py   # Tests for server capabilities
├── pyproject.toml              # Project dependencies and metadata
├── README.md                   # User documentation
├── .env.example                # Example environment configuration
└── AGENTS.md                   # MCP best practices guide
```

## Coding Standards

### Follow AGENTS.md Best Practices

This project adheres to the MCP best practices outlined in `AGENTS.md`. Key principles:

1. **Progressive Disclosure**: Always update the `CAPABILITIES` index when adding tools
2. **Context Efficiency**: Return small outputs by default, with `limit` parameters
3. **Naming Conventions**: Use `verb_noun` format (e.g., `list_notebooks`, `get_note`)
4. **Error Handling**: Provide structured errors with actionable hints
5. **Dual Transport**: Support both STDIO and Streamable HTTP

### Code Style

- **Type Hints**: Use type hints for all function parameters and return values
- **Docstrings**: Include docstrings with Args and Returns sections
- **Async**: Use `async def` for I/O operations
- **Error Handling**: Wrap API calls in try/except with informative messages

### Example Tool Implementation

```python
# 1. Add to CAPABILITIES index
Capability(
    name="my_new_tool",
    summary="Brief one-line description",
    tags=("category", "action", "type"),
    args={"param1": "str", "param2": "Optional[int]"},
    returns="dict[str, Any]",
    example={"param1": "value", "param2": 10},
    typical_bytes=500,
)

# 2. Implement the tool
@mcp.tool()
async def my_new_tool(param1: str, param2: Optional[int] = None) -> dict[str, Any]:
    """Brief one-line description.
    
    Args:
        param1: Description of param1
        param2: Optional description of param2
    
    Returns:
        Dictionary with result data
    """
    data = {"param1": param1}
    if param2 is not None:
        data["param2"] = param2
    
    result = await make_request("GET", "/api/endpoint", params=data)
    return {
        "request_id": str(uuid.uuid4()),
        "result": result,
    }
```

## Testing

### Running Tests

```bash
# Run all tests
uv run python tests/test_capabilities.py

# Test specific functionality
uv run python -c "from open_notebook_mcp.server import search_capabilities; print(search_capabilities('notebook'))"
```

### Manual Testing

Use the MCP Inspector for interactive testing:

```bash
# Note: This may not work if mcp dev has issues with the file structure
# Alternatively, just run the server directly
uv run open-notebook-mcp
```

Or test directly:

```bash
OPEN_NOTEBOOK_URL=http://localhost:5055 uv run open-notebook-mcp
```

### Test Checklist

Before submitting a pull request:

- [ ] All existing tests pass
- [ ] New functionality has corresponding `Capability` entry
- [ ] Tool names follow `verb_noun` convention
- [ ] Docstrings are complete and accurate
- [ ] Type hints are present
- [ ] Error handling is appropriate
- [ ] Manual testing with real Open Notebook instance (if possible)

## Adding New API Endpoints

When Open Notebook adds new API endpoints:

1. **Update CAPABILITIES**: Add a new `Capability` entry with appropriate metadata
2. **Implement Tool**: Create the `@mcp.tool()` function following existing patterns
3. **Test**: Verify the tool works with the actual API
4. **Document**: Update README.md if the new functionality is significant

## Common Patterns

### List Operations

```python
@mcp.tool()
async def list_items(
    filter_param: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Get items with filtering and pagination."""
    limit = max(1, min(limit, 100))  # Enforce limits
    params = {"limit": limit, "offset": offset}
    if filter_param is not None:
        params["filter"] = filter_param
    
    items = await make_request("GET", "/api/items", params=params)
    return {
        "request_id": str(uuid.uuid4()),
        "count": len(items) if isinstance(items, list) else 0,
        "items": items,
    }
```

### Create Operations

```python
@mcp.tool()
async def create_item(
    required_field: str,
    optional_field: Optional[str] = None,
) -> dict[str, Any]:
    """Create a new item."""
    data = {"required_field": required_field}
    if optional_field is not None:
        data["optional_field"] = optional_field
    
    item = await make_request("POST", "/api/items", json_data=data)
    return {
        "request_id": str(uuid.uuid4()),
        "item": item,
    }
```

### Update Operations

```python
@mcp.tool()
async def update_item(
    item_id: str,
    field1: Optional[str] = None,
    field2: Optional[str] = None,
) -> dict[str, Any]:
    """Update an item."""
    data = {}
    if field1 is not None:
        data["field1"] = field1
    if field2 is not None:
        data["field2"] = field2
    
    item = await make_request("PUT", f"/api/items/{item_id}", json_data=data)
    return {
        "request_id": str(uuid.uuid4()),
        "item": item,
    }
```

## Pull Request Process

1. **Fork and Branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make Changes**
   - Follow coding standards
   - Update CAPABILITIES index
   - Add tests if applicable

3. **Test Locally**
   ```bash
   uv run python tests/test_capabilities.py
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: add support for X endpoint"
   ```

5. **Push and PR**
   ```bash
   git push origin feature/my-new-feature
   ```
   Then create a pull request on GitHub

## Commit Message Format

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `chore:` Build process or auxiliary tool changes

Examples:
- `feat: add support for transformations API`
- `fix: handle empty response in delete operations`
- `docs: update README with chat examples`
- `test: add tests for search functionality`

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Be respectful and constructive in discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
