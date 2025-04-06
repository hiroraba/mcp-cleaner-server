# run_tool_direct.py
from mcp_cleaner_server import clean_files

res = clean_files(
    action="list",
    file_type="pdf",
    folder="/Users/matsuohiroki/Downloads",
    older_than_days=7
)

print(res)
