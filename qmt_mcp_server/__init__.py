from .server import mcp_server


def run():
    """Run the MCP server."""
    mcp_server.run(transport="stdio")
