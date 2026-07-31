"""Console entry point for the local MCP server."""

from . import create_server


def main() -> None:
    """Run the MCP server over stdio."""
    create_server().run(transport="stdio")


if __name__ == "__main__":
    main()
