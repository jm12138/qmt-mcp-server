from .server import mcp


def run():
    """Run the MCP server."""
    mcp.run(transport="stdio")
