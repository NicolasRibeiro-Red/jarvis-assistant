# /dash — Visual Kanban Dashboard (localhost, functional)

**Triggers**: `/dash`, `/dashboard`, `dashboard`, `dash`, `painel`, `kanban visual`

**Purpose**: Run a fully functional Kanban dashboard on `localhost` with drag-and-drop, real persistence to the task files, inline editing, and the Geist Design System styling (Vercel's open token library). The principal sees the same task data as `/tasks` Kanban — but in a real browser, with real interactions.

**Default browser endpoint**: `http://localhost:7321`

**Architecture**: Python stdlib server (`dashboard/server.py`) + static `dashboard/index.html`. Zero external dependencies (only Geist font via Google Fonts; falls back to system-ui offline).

---

## Why this exists

The terminal Kanban (`/tasks`) is fast but constrained. Some principals want a **visual, interactive** view — a real dashboard they can leave open on a second monitor, drag cards between columns, edit inline. `/dash` produces that.

The architecture has two pieces:

1. **`dashboard/server.py`** — Python stdlib HTTP server with a small REST API. Reads/writes the same `memory/tasks/*.md` files that `/tasks` uses. Zero external Python dependencies — pure standard library.
2. **`dashboard/index.html`** — single self-contained HTML with Geist tokens inlined as CSS variables and vanilla JS that talks to the server's API. No build step, no React, no framework.

The principal's task data lives in `memory/tasks/*.md` (markdown + YAML frontmatter). The dashboard is a view layer over those files. Every drag-and-drop, edit, or delete in the browser writes back to the same files immediately. The `/tasks` terminal command and `/dash` browser dashboard are always in sync because they share the source of truth.

---

## Workflow

### Step 1 — Verify pre-conditions

Both files must exist (they ship in the repo):
- `dashboard/server.py`
- `dashboard/index.html`

If either is missing: inform the principal *"Arquivos do dashboard ausentes. Reinstalar o JARVIS?"* and stop.

### Step 2 — Detect Python

Run `python --version 2>&1 || python3 --version 2>&1`. The server requires Python 3.8+. If neither is available, fall back gracefully (see Step 5b).

### Step 3 — Free port 7321 if in use

```bash
# Detect process on 7321 (cross-platform)
# Windows: netstat -ano | grep ":7321"
# macOS/Linux: lsof -ti:7321
```

If a process is bound to 7321 and it's an old `server.py` instance: kill it. If it's something unrelated: try port 7322 instead and inform the principal.

### Step 4 — Start the server

```bash
python dashboard/server.py
# or python3 if python -> Python 2
```

Use `run_in_background: true` on the Bash call so JARVIS doesn't block on the long-running server.

The server reads/writes from `memory/tasks/*.md` directly. No state migration needed.

### Step 5 — Verify health

Wait ~1 second, then probe:
```bash
curl -s http://localhost:7321/api/health
```

Expected: `{"ok": true, "tasks": N}`. If this fails, check the server's stdout (the background task output file) for the bind error.

### Step 5b — Fallback if Python missing

If no Python available:

#### Option A — Node http-server (no API, read-only)
```bash
npx --yes http-server dashboard -p 7321 -a 127.0.0.1 --silent
```
This serves the HTML but **the API will not respond** — drag-and-drop, edit, and create will fail with network errors. Inform the principal: *"Servidor estatico apenas (sem Python). Drag-and-drop indisponivel. Para edicao funcional, instalar Python 3."*

#### Option B — Open via `file://`
Last resort — same limitation as Option A:
- Windows: `start "" "C:/path/to/dashboard/index.html"`
- macOS: `open "/path/to/dashboard/index.html"`
- Linux: `xdg-open "/path/to/dashboard/index.html"`

### Step 6 — Open the browser

After health check passes:
- Windows: `start http://localhost:7321`
- macOS: `open http://localhost:7321`
- Linux: `xdg-open http://localhost:7321`

### Step 7 — Confirm to the principal

CLINICAL register, voice-matched. Short:

```
Dashboard rodando em http://localhost:7321, sir.

[N] tarefas. Arrastar entre colunas para mover. Clique no card para editar.

Para encerrar o servidor, encerre esta sessao do terminal.
```

If using fallback (Step 5b):
```
Sem Python — servindo HTML estatico em http://localhost:7321, sir.
Drag-and-drop indisponivel. Para edicao funcional, instalar Python 3.
```

### Step 8 — Run humanize-check

Apply on the confirmation message before delivery. Do not surface the check.

---

## Live behavior

The dashboard is **live**, not a snapshot. The principal interacts with it directly:

| Action in browser | Effect on filesystem |
|-------------------|---------------------|
| Drag card between columns | `PATCH /api/tasks/{id}` → server rewrites the .md file with new `column:` value (and sets `completed:` if moved to "feitos") |
| Click card → edit modal → Save | `PATCH /api/tasks/{id}` → server rewrites all changed fields |
| "+ Nova" → create modal → Save | `POST /api/tasks` → server creates a new `T-{date}-{seq}.md` |
| `×` button on hovered card | `DELETE /api/tasks/{id}` → server removes the file |
| `✓` button on hovered card | shortcut for "move to feitos" |
| `−` button on hovered card | shortcut for "move to descartado" |

Every action triggers an immediate refetch from `GET /api/tasks` so the visible state matches the filesystem.

The principal does NOT need to rerun `/dash` to see updates. The browser is always live as long as the server is running.

---

## Server lifecycle

`dashboard/server.py` runs in the foreground of a Bash background process and keeps the port bound until:
1. The principal closes the terminal where JARVIS is running
2. The principal sends Ctrl+C to the server process
3. The Claude Code session ends and the background process is reaped
4. The OS reboots

If the principal runs `/dash` again while a server is already on 7321: detect the bind conflict, kill the old process, restart fresh. This pattern handles stale servers from prior sessions.

To detect if 7321 is in use:
```bash
# Windows
netstat -ano | grep ":7321 "
# macOS/Linux
lsof -ti:7321
```

---

## API contract

The server exposes:

| Method | Path | Body | Returns |
|--------|------|------|---------|
| GET | `/` | — | `index.html` |
| GET | `/api/tasks` | — | `[{id, title, column, priority, project, due, created, completed}, ...]` |
| GET | `/api/health` | — | `{ok: true, tasks: N}` |
| POST | `/api/tasks` | `{title, column?, priority?, project?, due?}` | `{ok: true, id: "T-..."}` (201) |
| PATCH | `/api/tasks/{id}` | `{column?, title?, priority?, project?, due?}` | `{ok: true}` |
| DELETE | `/api/tasks/{id}` | — | `{ok: true}` |

Valid `column` values: `a-fazer`, `fazendo`, `feitos`, `descartado`. Legacy values from v1.6/v2.0 (`backlog`, `hoje`, `doing`, `done`) are auto-mapped on read.

Valid `priority` values: `high`, `medium`, `low`.

`due` must be ISO date `YYYY-MM-DD` or `null`.

When a task moves to `feitos`, the server auto-sets `completed` to today's date if not already set.

---

## Anti-patterns

- **Do NOT** use any external library (Tailwind, React, Vue, jQuery) in the HTML — auto-contained, zero dependencies beyond the Google Font
- **Do NOT** add Python packages (Flask, FastAPI, etc.) to the server — stdlib only
- **Do NOT** include emoji in the rendered output — Geist surface is monochrome-first, accent blue only for emphasis
- **Do NOT** add a "Generated with..." footer — the dashboard is the principal's, not branded
- **Do NOT** add a 5th column — keep 4 (A Fazer, Fazendo, Feitos, Descartado)
- **Do NOT** include the principal's data in any chat output — the data lives in the browser, JARVIS does not echo it back

---

## Failure modes

- **Port 7321 in use by old server.py** → kill old process, restart
- **Port 7321 in use by something else** → try 7322, inform principal
- **No Python at all** → fallback to static serve (file:// or Node http-server), warn the principal that drag-and-drop is disabled
- **dashboard/ directory missing** → reinstall is needed; cannot self-heal because the HTML/server.py are templates that ship in the repo
- **No tasks at all** → empty kanban renders with `vazio` placeholder in each column
- **Frontmatter parse error in a task** → server skips that task with a stderr log, continues with the rest

---

## Length budget

The skill file itself is long (because the HTML template is embedded). The OUTPUT to the principal — confirmation message — is short:

- Confirmation: 3-5 lines max
- Server URL or file path: 1 line
- Update instructions: 1-2 lines

---

## Integration

- **/tasks**: Same data source. Different rendering. The principal can use both — terminal-native for fast scan, browser for visual.
- **/wrap-up**: The dashboard reflects the post-wrap-up state of tasks. Always regenerate after a wrap-up that changed task statuses.
- **/briefing**: Briefing remains terminal-only. The dashboard is a complement, not a replacement.

---

## Reference files (ship in the repo)

The dashboard is composed of two files that ship in the repo and should not be regenerated by JARVIS in normal operation:

- **`dashboard/server.py`** — Python stdlib REST server. Reads/writes `memory/tasks/*.md`. ~270 lines. Stateless beyond the filesystem.
- **`dashboard/index.html`** — Geist-styled SPA. Vanilla JS with drag-and-drop, modal editing, toast notifications. ~470 lines. No build step.

If either file is missing, the principal needs to reinstall the JARVIS template (e.g. clone the repo again and re-run `install.sh`). JARVIS does not regenerate them inline — they are part of the static distribution.

---

## Quick command reference

```bash
# Start (background)
python dashboard/server.py

# Health check
curl -s http://localhost:7321/api/health

# Manual API examples (for debugging only — the browser does this automatically)
curl -X PATCH http://localhost:7321/api/tasks/T-2026-05-01-1 \
  -H "Content-Type: application/json" \
  -d '{"column":"feitos"}'

curl -X POST http://localhost:7321/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Nova tarefa","priority":"high"}'

curl -X DELETE http://localhost:7321/api/tasks/T-2026-05-01-1
```

The `JARVIS_DASH_PORT` environment variable overrides the default port if 7321 is unavailable:

```bash
JARVIS_DASH_PORT=7322 python dashboard/server.py
```
