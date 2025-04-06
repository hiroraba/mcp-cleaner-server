import subprocess
import json

# MCPサーバーとの通信（JSON-RPC形式）を模倣
payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "clean_files",
    "params": {
        "action": "list",
        "file_type": "pdf",
        "folder": "~/Downloads",
        "older_than_days": 7,
        "min_size_mb": 0
    }
}

# MCPサーバーは STDIN/STDOUT で通信する
proc = subprocess.Popen(
    ["python", "file_cleaner_mcp_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# リクエスト送信
proc.stdin.write(json.dumps(payload) + "\n")
proc.stdin.flush()

# レスポンス受信
response = proc.stdout.readline()
print("📥 MCP Response:")
print(json.loads(response))
