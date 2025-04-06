import tkinter as tk
from tkinter import scrolledtext
import json
from mcp_cleaner_server import clean_files

# Claudeの代わりに構造化（手動マッピング）
def simulate_claude(natural_text: str) -> dict:
    if "pdf" in natural_text.lower() and "削除" in natural_text:
        return {
            "action": "delete",
            "file_type": "pdf",
            "folder": "/Users/matsuohiroki/Downloads",
            "older_than_days": 3
        }
    return {
        "action": "list",
        "file_type": "pdf",
        "folder": "/Users/matsuohiroki/Downloads",
        "older_than_days": 0
    }

# メイン処理
def run_command():
    user_input = input_box.get()
    output_box.delete("1.0", tk.END)

    output_box.insert(tk.END, f"🗣️ 入力: {user_input}\n")

    structured = simulate_claude(user_input)
    output_box.insert(tk.END, "📦 JSON構造:\n")
    output_box.insert(tk.END, json.dumps(structured, indent=2) + "\n")

    output_box.insert(tk.END, "\n🚀 実行中...\n")
    result = clean_files(**structured)
    output_box.insert(tk.END, "\n✅ 結果:\n")
    output_box.insert(tk.END, json.dumps(result, indent=2) + "\n")

# GUI構築
window = tk.Tk()
window.title("🧹 ファイル整理アシスタント")

# 入力欄
input_box = tk.Entry(window, width=60)
input_box.pack(pady=10)

# 実行ボタン
run_button = tk.Button(window, text="🟢 実行", command=run_command)
run_button.pack(pady=5)

# 結果表示欄
output_box = scrolledtext.ScrolledText(window, width=80, height=20)
output_box.pack(padx=10, pady=10)

# 起動
window.mainloop()
