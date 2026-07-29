import os
import tempfile
import shutil
from git import Repo

CODE_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
)


def load_code_files(folder_path: str):
    code_files = []

    for root, dirs, files in os.walk(folder_path):

        dirs[:] = [
            d for d in dirs
            if d not in [
                "venv",
                "__pycache__",
                ".git",
                "node_modules",
                "chroma_db",
                ".vscode",
            ]
        ]

        for filename in files:
            
            
            if filename in ["challenge1.py", "challeneg1.py"]:
                continue

            if filename.endswith(CODE_EXTENSIONS):

                file_path = os.path.join(root, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    if content.strip():

                        code_files.append(
                            {
                                "filename": os.path.relpath(file_path, folder_path),
                                "content": content,
                            }
                        )

                except Exception:
                    continue

    return code_files


def load_github_repo(repo_url: str):
    """
    Clone a GitHub repository into a temporary folder,
    read all supported files and clean up afterwards.
    """

    temp_dir = tempfile.mkdtemp()

    try:

        Repo.clone_from(repo_url, temp_dir)

        files = load_code_files(temp_dir)

        return files

    finally:

        shutil.rmtree(temp_dir, ignore_errors=True)