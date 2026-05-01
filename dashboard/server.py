#!/usr/bin/env python3
"""J.A.R.V.I.S. Kanban Dashboard Server.

Single-file zero-dep server using Python stdlib only.

Endpoints:
- GET  /                  -> serves index.html
- GET  /api/tasks         -> list all tasks as JSON
- PATCH /api/tasks/<id>   -> update task field(s) (column, priority, etc)
- POST /api/tasks         -> create new task
- DELETE /api/tasks/<id>  -> delete task file

Run: python dashboard/server.py
"""

import http.server
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "memory" / "tasks"
DASHBOARD_DIR = ROOT / "dashboard"
PORT = int(os.environ.get("JARVIS_DASH_PORT", "7321"))

VALID_COLUMNS = {"a-fazer", "fazendo", "feitos", "descartado"}
VALID_PRIORITIES = {"high", "medium", "low"}

# Legacy column mapping (v1.6 -> v2.0 -> v2.1)
COLUMN_MAP = {
    "backlog": "a-fazer",
    "hoje": "a-fazer",
    "doing": "fazendo",
    "done": "feitos",
}


def parse_frontmatter(content: str):
    """Parse simple YAML frontmatter. Returns (dict, body_text)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")
    fm = {}
    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith('"') and v.endswith('"') and len(v) >= 2:
            v = v[1:-1]
        elif v == "null" or v == "":
            v = None
        fm[k] = v
    return fm, body


def serialize_frontmatter(fm: dict, body: str) -> str:
    """Re-serialize frontmatter back to file content."""
    lines = ["---"]
    # Preserve a stable order for known fields
    known_order = ["id", "title", "column", "priority", "project", "due", "created", "completed"]
    seen = set()
    for k in known_order:
        if k in fm:
            seen.add(k)
            lines.append(_render_kv(k, fm[k]))
    for k, v in fm.items():
        if k in seen:
            continue
        lines.append(_render_kv(k, v))
    lines.append("---")
    if not body.startswith("\n"):
        return "\n".join(lines) + "\n" + body
    return "\n".join(lines) + body


def _render_kv(k: str, v) -> str:
    if v is None:
        return f"{k}: null"
    if isinstance(v, str):
        # Always quote strings that contain special chars or are typical "text" fields
        if k in ("title", "project") or any(c in v for c in [":", "#", '"']):
            return f'{k}: "{v}"'
        return f"{k}: {v}"
    return f"{k}: {v}"


def normalize_column(col):
    if col is None:
        return "a-fazer"
    return COLUMN_MAP.get(col, col if col in VALID_COLUMNS else "a-fazer")


def task_from_file(path: Path):
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[server] Error reading {path.name}: {e}", file=sys.stderr)
        return None
    fm, _ = parse_frontmatter(content)
    if not fm.get("id"):
        return None
    col = fm.get("column")
    if not col:
        # legacy: derive from status
        st = fm.get("status", "pending")
        if st == "in-progress":
            col = "fazendo"
        elif st == "done":
            col = "feitos"
        else:
            col = "a-fazer"
    col = normalize_column(col)
    return {
        "id": fm.get("id"),
        "title": fm.get("title", ""),
        "column": col,
        "priority": fm.get("priority", "medium"),
        "project": fm.get("project") or "",
        "due": fm.get("due"),
        "created": fm.get("created"),
        "completed": fm.get("completed"),
    }


def load_all_tasks():
    if not TASKS_DIR.exists():
        return []
    out = []
    for f in sorted(TASKS_DIR.glob("T-*.md")):
        t = task_from_file(f)
        if t:
            out.append(t)
    return out


def update_task(task_id: str, updates: dict):
    f = TASKS_DIR / f"{task_id}.md"
    if not f.exists():
        return False, f"Task {task_id} not found"
    content = f.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    fm["id"] = task_id

    if "column" in updates:
        new_col = updates["column"]
        if new_col not in VALID_COLUMNS:
            return False, f"Invalid column: {new_col}"
        fm["column"] = new_col
        if new_col == "feitos" and not fm.get("completed"):
            fm["completed"] = date.today().isoformat()
        elif new_col != "feitos":
            fm["completed"] = None

    if "title" in updates and updates["title"]:
        fm["title"] = str(updates["title"]).strip()

    if "priority" in updates:
        p = updates["priority"]
        if p not in VALID_PRIORITIES:
            return False, f"Invalid priority: {p}"
        fm["priority"] = p

    if "project" in updates:
        fm["project"] = str(updates["project"]).strip() if updates["project"] else None

    if "due" in updates:
        d = updates["due"]
        if d in (None, ""):
            fm["due"] = None
        else:
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(d)):
                return False, "Invalid due date format (expect YYYY-MM-DD)"
            fm["due"] = d

    f.write_text(serialize_frontmatter(fm, body), encoding="utf-8")
    return True, "ok"


def create_task(data: dict):
    title = str(data.get("title", "")).strip()
    if not title:
        return False, "Title required", None
    today = date.today().isoformat()
    # Compute next sequence for today
    existing_today = list(TASKS_DIR.glob(f"T-{today}-*.md"))
    seq = len(existing_today) + 1
    task_id = f"T-{today}-{seq}"
    while (TASKS_DIR / f"{task_id}.md").exists():
        seq += 1
        task_id = f"T-{today}-{seq}"
    column = normalize_column(data.get("column", "a-fazer"))
    priority = data.get("priority", "medium")
    if priority not in VALID_PRIORITIES:
        priority = "medium"
    fm = {
        "id": task_id,
        "title": title,
        "column": column,
        "priority": priority,
        "project": str(data.get("project", "") or "").strip() or None,
        "due": data.get("due") or None,
        "created": today,
        "completed": None,
    }
    body = ""
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    (TASKS_DIR / f"{task_id}.md").write_text(serialize_frontmatter(fm, body), encoding="utf-8")
    return True, "created", task_id


def delete_task(task_id: str):
    f = TASKS_DIR / f"{task_id}.md"
    if not f.exists():
        return False, "Task not found"
    f.unlink()
    return True, "deleted"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def _send_json(self, status: int, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/tasks":
            self._send_json(200, load_all_tasks())
            return
        if path == "/api/health":
            self._send_json(200, {"ok": True, "tasks": len(load_all_tasks())})
            return
        # static files
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/tasks":
            data = self._read_json_body()
            if data is None:
                self._send_json(400, {"ok": False, "error": "Invalid JSON"})
                return
            ok, msg, task_id = create_task(data)
            if ok:
                self._send_json(201, {"ok": True, "id": task_id})
            else:
                self._send_json(400, {"ok": False, "error": msg})
            return
        self.send_error(404)

    def do_PATCH(self):
        path = urlparse(self.path).path
        m = re.match(r"^/api/tasks/(T-[\w-]+)$", path)
        if not m:
            self.send_error(404)
            return
        task_id = m.group(1)
        data = self._read_json_body()
        if data is None:
            self._send_json(400, {"ok": False, "error": "Invalid JSON"})
            return
        ok, msg = update_task(task_id, data)
        if ok:
            self._send_json(200, {"ok": True})
        else:
            self._send_json(400, {"ok": False, "error": msg})

    def do_DELETE(self):
        path = urlparse(self.path).path
        m = re.match(r"^/api/tasks/(T-[\w-]+)$", path)
        if not m:
            self.send_error(404)
            return
        task_id = m.group(1)
        ok, msg = delete_task(task_id)
        if ok:
            self._send_json(200, {"ok": True})
        else:
            self._send_json(404, {"ok": False, "error": msg})

    def log_message(self, format, *args):
        # Quiet logs (no per-request noise)
        pass


def main():
    if not DASHBOARD_DIR.exists():
        print(f"[server] Dashboard dir missing: {DASHBOARD_DIR}", file=sys.stderr)
        sys.exit(1)
    if not (DASHBOARD_DIR / "index.html").exists():
        print(f"[server] index.html missing in {DASHBOARD_DIR}", file=sys.stderr)
        sys.exit(1)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    addr = ("127.0.0.1", PORT)
    try:
        server = http.server.HTTPServer(addr, Handler)
    except OSError as e:
        print(f"[server] Could not bind {addr[0]}:{addr[1]}: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"J.A.R.V.I.S. Kanban running on http://localhost:{PORT}")
    print(f"Tasks dir: {TASKS_DIR}")
    print("Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[server] stopped.")


if __name__ == "__main__":
    main()
