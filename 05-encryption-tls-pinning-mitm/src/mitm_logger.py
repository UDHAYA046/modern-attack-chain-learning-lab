import json
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "sample-data"
OUTPUT_FILE = DATA_DIR / "intercepted_requests.json"

DATA_DIR.mkdir(exist_ok=True)


def load_existing_logs():
    if OUTPUT_FILE.exists():
        try:
            return json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def save_logs(logs):
    OUTPUT_FILE.write_text(json.dumps(logs, indent=4), encoding="utf-8")


def response(flow):
    logs = load_existing_logs()

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "method": flow.request.method,
        "url": flow.request.pretty_url,
        "host": flow.request.host,
        "path": flow.request.path,
        "request_headers": dict(flow.request.headers),
        "status_code": flow.response.status_code,
        "response_headers": dict(flow.response.headers),
        "content_type": flow.response.headers.get("content-type", "unknown"),
        "response_size_bytes": len(flow.response.content or b"")
    }

    logs.append(entry)
    save_logs(logs)

    print(f"[LOGGED] {entry['method']} {entry['url']} -> {entry['status_code']}")