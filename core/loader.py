# core/loader.py
import os
# Allowed file extensions
CODE_EXTENSIONS = ('.py', '.js', '.ts', '.html', '.css', '.md', '.txt')
def load_code_files(folder_path: str):
    """
    Recursively loads code files from a folder.
    Args:
        folder_path (str): Path to the target directory
    Returns:
        List[dict]: List of {"filename": str, "content": str}
    """
    code_files = []
    for root, dirs, files in os.walk(folder_path):
         dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules', 'chroma_db']]
    for filename in files:
            if filename.endswith(CODE_EXTENSIONS):
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if not content.strip():
                            continue  # skip empty files
                        
                    code_files.append({
                        "filename": os.path.relpath(file_path, folder_path),
                        "content": content
                    })
                except (UnicodeDecodeError, PermissionError, OSError):
                    # Skip unreadable files silently
                    continue
    return code_files