"""Contains services for the MCP Tool"""

import os 

DEFAULT_DIR = ""

def search_files(query: str, directory: str = DEFAULT_DIR):
    res = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith('.txt') or name.endswith('.md'):
                full_path = os.path.join(root, name)
                
                try:
                    with open(full_path) as f:
                        line_match = f.readlines()
                except FileNotFoundError:
                    print("File not found, continuing...")
                    continue
                
                for line in line_match:
                    if query in line:
                        res.append([name, full_path])
                        break     
    return res
            
        
# testing purposes: print(search_files("brown fox", "F:/coding/projects/kb-mcp-server/test"))