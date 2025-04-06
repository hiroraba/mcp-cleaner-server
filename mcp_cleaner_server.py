# file_cleaner_mcp_server.py

from mcp.server.fastmcp import FastMCP
from pathlib import Path
import time
import shutil
from send2trash import send2trash  # pip install send2trash

app = FastMCP("File Cleaner MCP")

# サポートする拡張子と分類
FILE_TYPES = {
    "image": [".png", ".jpg", ".jpeg", ".gif"],
    "pdf": [".pdf"],
    "video": [".mov", ".mp4", ".avi"],
}

# ユーティリティ関数：対象ファイルを探す
def find_files(folder: Path, file_type: str, older_than_days: int = 0, min_size_mb: float = 0.0):
    ext_list = FILE_TYPES.get(file_type, [])
    now = time.time()
    matched = []

    for f in folder.glob("**/*"):
        if not f.is_file():
            continue
        if ext_list and f.suffix.lower() not in ext_list:
            continue
        if older_than_days > 0:
            age_days = (now - f.stat().st_mtime) / (60 * 60 * 24)
            if age_days < older_than_days:
                continue
        if min_size_mb > 0.0:
            size_mb = f.stat().st_size / (1024 * 1024)
            if size_mb < min_size_mb:
                continue
        matched.append(str(f))
    
    return matched

@app.tool()
def clean_files(
    action: str,
    file_type: str = "image",
    folder: str = str(Path.home() / "Downloads"),
    older_than_days: int = 0,
    min_size_mb: float = 0.0
):
    """
    指定条件でファイルを検索し、削除または一覧表示を行う
    """
    folder_path = Path(folder).expanduser()
    files = find_files(folder_path, file_type, older_than_days, min_size_mb)

    if action == "delete":
        for f in files:
            send2trash(f)  # 安全に削除（ゴミ箱へ）
        return {
            "status": "deleted",
            "count": len(files),
            "files": files
        }
    else:
        return {
            "status": "listed",
            "count": len(files),
            "files": files
        }

# MCPサーバー起動
if __name__ == "__main__":
    app.run()
