from argparse import ArgumentParser

from .server import mcp


def stdio():
    """Run the MCP server."""
    mcp.run(transport="stdio")


def sse():
    """Run the MCP server."""

    parser = ArgumentParser(description='QMT MCP Server SSE mode')

    parser.add_argument('--port', type=int, default=8000,
                        help='Port number for SSE server')
    parser.add_argument('--host', type=str, default='0.0.0.0',
                        help='Host address for SSE server')

    args = parser.parse_args()

    mcp.settings.host = args.host
    mcp.settings.port = args.port

    mcp.run(transport="sse")
