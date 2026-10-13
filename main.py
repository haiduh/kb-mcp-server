from mcp.server import MCPServer
from services import search_files, read_file, write_file 

mcp = MCPServer("KnowBase")

@mcp.tool()
def search(query: str, directory: str = ".") -> list:
    """Searches through text and Markdown files for a query string."""
    return search_files(query, directory)

@mcp.tool()
def read(file_path: str) -> str:
    """Reads and returns the full text contents of a specified file."""
    return read_file(file_path)

@mcp.tool()
def write(content: str, file_path: str) -> str:
    """Writes text content to a specified file path."""
    return write_file(content, file_path)

if __name__ == "__main__":
    mcp.run(transport="stdio")
