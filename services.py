"""Contains services for the MCP Tool"""

import os 

DEFAULT_DIR = ""

def search_files(query: str, directory: str = DEFAULT_DIR):
    """Searches through local files for a query string and returns the filename and full path 
    for any file that contains a match.

    This function recursively traverses the specified directory, filtering for text and 
    Markdown files (.txt and .md), and checks their contents line by line for the given query.

    Args:
        query (str): The search string to look for within the files.
        directory (str, optional): The root directory path to traverse. Defaults to DEFAULT_DIR.

    Returns:
        list[list[str]]: A list of matches, where each entry is a list containing 
        the filename and its full file path.

    Raises:
        FileNotFoundError: Handled internally if a file disappears during directory traversal.
    """
    res = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.txt') or name.endswith('.md'):
                full_path = os.path.join(root, name)
                
                try:
                    with open(full_path, encoding="utf-8") as f:
                        line_match = f.readlines()
                except (FileNotFoundError, UnicodeError):
                    print("File not found, continuing...")
                    continue
                
                for line in line_match:
                    if query in line:
                        res.append([name, full_path])
                        break     
    return res

def read_file(file_path: str):
    """Reads and returns the complete text contents of a specified file.

    Args:
        file_path (str): The absolute or relative path to the target file.

    Returns:
        str: The full string content of the file if found.
        str: An error message string if the file is not found.

    Raises:
        FileNotFoundError: Caught internally to return a user-friendly error string instead of crashing.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            file_read = f.read()
        return file_read
    except (FileNotFoundError, UnicodeError):
        return f"File not found at: {file_path}"
    
def write_file(content: str, file_path: str):
    """Writes text content to a specified file path, creating or overwriting the file.

    Args:
        content (str): The text content to write into the file.
        file_path (str): The path (relative or absolute) where the file will be saved.

    Returns:
        str: A success message including the file path if the write operation succeeds, 
        or an error message string if an OSError occurs.

    Raises:
        OSError: Caught internally to return a user-friendly error message instead of crashing.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Content written complete: {file_path}"
    except OSError:
        return f"File does not exist at: {file_path}"
        
# testing purposes: print(search_files("brown fox", "F:/coding/projects/kb-mcp-server/test"))