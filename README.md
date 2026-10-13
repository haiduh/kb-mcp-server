# kb-mcp-server

A personal knowledge base MCP server that exposes search, read, and write tools over local files for MCP-compatible clients such as Claude Desktop.

## What it does

- **Search** — recursively searches `.txt` and `.md` files in a directory for a query string, returning matching filenames and paths
- **Read** — reads and returns the full contents of a specified file
- **Write** — writes text content to a specified file path, creating the file if it doesn't exist

## Requirements

- Windows (uses Windows paths; Linux/macOS not currently supported)
- Python 3.11+
- Claude Desktop (or any MCP-compatible client)

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/kb-mcp-server.git
cd kb-mcp-server
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Claude Desktop**

Open `%APPDATA%\Claude\claude_desktop_config.json` and add the following inside the root object:

```json
"mcpServers": {
  "kb-mcp-server": {
    "command": "C:\\path\\to\\kb-mcp-server\\venv\\Scripts\\python.exe",
    "args": ["C:\\path\\to\\kb-mcp-server\\main.py"]
  }
}
```

Replace the paths with the actual location of your cloned repo.

**5. Restart Claude Desktop**

Go to Settings → Developer and confirm the server shows as **Running**.

## Usage

In Claude Desktop, you can now ask things like:

- *"Search for 'password' in C:\Users\me\notes"*
- *"Read the file at C:\Users\me\notes\todo.md"*
- *"Write a new note to C:\Users\me\notes\ideas.md"*

Always provide the full Windows path to the directory or file.

## File support

| Format | Search | Read | Write |
|--------|--------|------|-------|
| `.txt` | ✅ | ✅ | ✅ |
| `.md` | ✅ | ✅ | ✅ |
| `.docx` | 🔜 | 🔜 | 🔜 |

## Roadmap

- [ ] `.docx` support via `python-docx`
- [ ] Case-insensitive search option