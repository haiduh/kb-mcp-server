from mcp.server import MCPServer
from services import search_files 

mcp = MCPServer("KnowBase")

@mcp.tool()
def wrapped_search_files(query: str, directory: str = ".") -> list:
    """Searches through local files for a query string and returns the filename + matching lines."""
    return search_files(query, directory)

if __name__ == "__main__":
    mcp.run(transport="stdio")