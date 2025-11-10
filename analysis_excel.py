import requests
import json

url = "http://192.168.31.40:9000/mcp"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "X-Session-ID": "test-session"
}


payload = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "session": "test-session",
        "name": "detect_excel_tables",
        "arguments": {
            "excel_name": "example.xlsx"
        }
    },
    "id": "1"
}

response = requests.post(url, json=payload, headers=headers)
print(json.dumps(response.json(), ensure_ascii=False, indent=2))
