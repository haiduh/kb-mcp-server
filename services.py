"""Contains services for the MCP Tool"""

from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

DEFAULT_DIR = ""
model = SentenceTransformer('sentence-transformers/msmarco-MiniLM-L6-cos-v5')
client = chromadb.PersistentClient(path=str(Path(__file__).parent / "chroma_db"))
collection = client.get_or_create_collection(name="my-notes")

def search_files(query: str, directory: str = DEFAULT_DIR):
    """Searches through local files for a query string and returns the filename and full path 
    for any file that contains a match.

    Args:
        query (str): The search string to look for within the files (case-insensitive).
        directory (str, optional): The root directory path to traverse. Defaults to DEFAULT_DIR.

    Returns:
        list[list[str]]: A list of matches, where each entry is a list containing 
        the filename and its full file path.
    """
    res = []
    query_lower = query.lower()

    for path in Path(directory).rglob("*"):
        if path.suffix not in (".txt", ".md"):
            continue

        try:
            with path.open(encoding="utf-8") as f:
                lines = f.readlines()
        except (FileNotFoundError, UnicodeError):
            print("File not found, continuing...")
            continue

        for line in lines:
            if query_lower in line.lower():
                res.append([path.name, str(path)])
                break

    return res

def read_file(file_path: str):
    """Reads and returns the complete text contents of a specified file.

    Args:
        file_path (str): The absolute or relative path to the target file.

    Returns:
        str: The full string content of the file if found, or an error message if not found.
    """
    try:
        with Path(file_path).open(encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, UnicodeError):
        return f"File not found at: {file_path}"

def write_file(content: str, file_path: str):
    """Writes text content to a specified file path, creating or overwriting the file.

    Args:
        content (str): The text content to write into the file.
        file_path (str): The path where the file will be saved.

    Returns:
        str: A success message or an error string if an OSError occurs.
    """
    try:
        with Path(file_path).open("w", encoding="utf-8") as f:
            f.write(content)
        return f"Content written complete: {file_path}"
    except OSError:
        return f"File does not exist at: {file_path}"

def index_files(directory):
    """Indexes text and Markdown files in a directory into the ChromaDB collection.

    Args:
        directory (str): The root directory path to index.
    """
    for path in Path(directory).rglob("*"):
            if path.suffix not in (".txt", ".md"):
                continue
            
            stat_result = path.stat()
            current_mtime = stat_result.st_mtime
            file_id = str(path)
            
            # Check if file already exists in ChromaDB and verify mtime
            existing = collection.get(ids=[file_id], include=["metadatas"])
            if existing and existing.get("metadatas") and len(existing["metadatas"]) > 0:
                stored_mtime = existing["metadatas"][0].get("mtime")
                if stored_mtime == current_mtime:
                    continue  # Skip embedding and updating if unchanged
            
            try:
                with path.open(encoding='utf-8') as f:
                    file_lines = f.readlines()
            except (FileNotFoundError, UnicodeError) as e:
                print("This was the error", e)
                continue
                
            joined_lines = "".join(file_lines)
            embeddings = model.encode(joined_lines)
            
            # Use upsert to safely insert or update without duplicate ID crashes
            collection.upsert(
                ids=[file_id],
                embeddings=embeddings,
                metadatas=[{
                    "filename": str(path.name),
                    "path": file_id,
                    "mtime": current_mtime,
                }],
            )

def semantic_search(query, directory):
    """Performs a semantic search across indexed files using embeddings.

    Args:
        query (str): The search query phrase.
        directory (str): The directory to index before searching.

    Returns:
        list[list[str]]: A list of matching filenames and paths.
    """
    total_files = []
    index_files(directory)
    embedded_query = model.encode(query)
    
    res = collection.query(
        query_embeddings=[embedded_query],
        n_results=min(10, collection.count())
    )
    
    for doc in res['metadatas'][0]:
        file_name = doc.get('filename')
        path = doc.get('path')
        total_files.append([file_name, path])
    
    return total_files

# testing purposes: print(search_files("brown fox", "F:/coding/projects/kb-mcp-server/test"))
print(semantic_search("brown fox", "F:/coding/projects/kb-mcp-server/test"))