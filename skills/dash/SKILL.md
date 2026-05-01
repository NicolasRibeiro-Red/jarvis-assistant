# /dash — Visual Kanban Dashboard (localhost)

**Triggers**: `/dash`, `/dashboard`, `dashboard`, `dash`, `painel`, `kanban visual`

**Purpose**: Generate a self-contained HTML dashboard styled with the Geist Design System (Vercel's open token library) and serve it on `localhost`. The principal sees the same task data as `/tasks` Kanban — but in a real browser, with real visual fidelity.

**Default browser endpoint**: `http://localhost:7321`

---

## Why this exists

The terminal Kanban (`/tasks`) is fast but constrained. Some principals want a **visual** at-a-glance view — a real dashboard they can leave open on a second monitor while they work. `/dash` produces that.

The output is a single self-contained `index.html` with Geist tokens inlined as CSS variables, task data injected as JSON, and minimal vanilla JS for rendering. No build step, no framework, no install. Open it in any browser.

---

## Workflow

### Step 1 — Load tasks

Read all files in `memory/tasks/` (skip `done/` archive — done tasks shown in dashboard but archive shown only in /review).

For each task, parse frontmatter → JSON object:
```json
{
  "id": "T-2026-05-01-1",
  "title": "Apresentacao quinta-feira",
  "column": "hoje",
  "priority": "high",
  "project": "Cliente X",
  "due": "2026-05-08",
  "created": "2026-05-01",
  "completed": null
}
```

Auto-map legacy v1.6 tasks (with `status:` field) using the same logic as `/tasks` LIST.

### Step 2 — Load principal context

Read `memory/context.md` to extract:
- Principal name (for header greeting)
- Profile profession (subhead context)

### Step 3 — Generate `dashboard/index.html`

Write the file at `dashboard/index.html` with:
1. Geist Design System CSS inline (full token block)
2. Geist font from Google Fonts (with system fallback for offline)
3. Task data injected as inline JSON
4. Vanilla JS render of the Kanban
5. No external dependencies beyond the font

**Use the template at the bottom of this skill file** (TEMPLATE section). Replace the placeholder slots:
- `{{PRINCIPAL_NAME}}` → e.g. *"Sr. Lucas"*
- `{{PRINCIPAL_PROFESSION}}` → e.g. *"Designer"* (or empty string if not set)
- `{{TODAY_DATE}}` → e.g. *"01 de Maio de 2026"* (compute via Bash `date`)
- `{{TASKS_JSON}}` → minified JSON array of all tasks

### Step 4 — Serve on localhost

Try in this order, use the first that works:

#### Option A — Python http.server (preferred — built-in on most systems)
```bash
# Detect Python
python --version 2>&1 || python3 --version 2>&1

# If found, serve:
python -m http.server 7321 --directory dashboard --bind 127.0.0.1
# OR
python3 -m http.server 7321 --directory dashboard --bind 127.0.0.1
```
Use `run_in_background: true` on the Bash call so JARVIS doesn't block.

#### Option B — Node http-server (fallback)
```bash
# If Python not found but Node is:
npx --yes http-server dashboard -p 7321 -a 127.0.0.1 --silent
```

#### Option C — Open via `file://` (fallback when no server runtime)
If neither Python nor Node available, fall back to opening the file directly:
- Windows: `start "" "C:/path/to/dashboard/index.html"`
- macOS: `open "/path/to/dashboard/index.html"`
- Linux: `xdg-open "/path/to/dashboard/index.html"`

Inform the principal: *"Sem Python ou Node disponivel — abrindo o dashboard direto no browser via arquivo local. Mesmo conteudo, sem servidor."*

### Step 5 — Open the browser

After server is up (or file:// fallback chosen), open the principal's default browser:
- Windows: `start http://localhost:7321` (or the file:// path)
- macOS: `open http://localhost:7321`
- Linux: `xdg-open http://localhost:7321`

### Step 6 — Confirm

Output to the principal (CLINICAL register, voice-matched):

```
Dashboard rodando em http://localhost:7321, sir.

[N] tarefas: [counts by column].

Para atualizar apos mudancas, rodar /dash novamente.
Para encerrar o servidor, pressione Ctrl+C neste terminal.
```

If file:// fallback was used:
```
Dashboard aberto em arquivo local, sir.

[N] tarefas: [counts by column].

Caminho: dashboard/index.html
Para atualizar apos mudancas, rodar /dash novamente.
```

### Step 7 — Run humanize-check

Apply on the confirmation message before delivery. Do not surface the check.

---

## Update behavior

The dashboard is a **snapshot**. Every `/dash` invocation regenerates `dashboard/index.html` with current task data. The principal must rerun `/dash` to see changes.

**Future enhancement** (not in v2.0): a watcher mode where the HTML auto-refreshes via SSE when task files change. Out of scope for now.

---

## Server lifecycle

The Python/Node server runs in the foreground of a Bash background process. It will continue running until:
1. The principal closes the terminal where JARVIS is running
2. The port (7321) is freed via Ctrl+C
3. The Claude Code session ends

If the principal runs `/dash` again while a server is already running on 7321: the second invocation will fail to bind. Handle gracefully:
1. Detect the bind error
2. Inform: *"Servidor ja ativo em 7321. Apenas regenerei o HTML — refresque a aba."*
3. Skip the server step, just regenerate HTML and report

To detect if 7321 is in use:
```bash
# Windows
netstat -ano | findstr :7321
# macOS/Linux
lsof -i :7321 || nc -z 127.0.0.1 7321
```

---

## Anti-patterns

- **Do NOT** use any external library (Tailwind, React, Vue, etc.) in the HTML — auto-contained, zero dependencies beyond the font
- **Do NOT** include emoji in the HTML — Geist surface is monochrome-first, accent blue only for emphasis
- **Do NOT** add a "Generated with..." footer — the dashboard is the principal's, not branded
- **Do NOT** use saturated colors beyond the Geist semantic palette (blue accent, amber/red/green for badges only)
- **Do NOT** add a 5th column — keep 4 (BACKLOG, HOJE, DOING, DONE)
- **Do NOT** include the principal's data in any logged output — the JSON is in the HTML, but JARVIS does not echo it back to the chat

---

## Failure modes

- **Port 7321 in use** → fall back to file:// open, OR inform and try port 7322
- **No tasks at all** → render empty Kanban with message *"Nenhuma tarefa registrada. Adicione com /tarefas."*
- **dashboard/ directory missing** → create it
- **Python and Node both missing** → file:// fallback, inform principal

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

## TEMPLATE — full HTML to write at `dashboard/index.html`

The HTML below is the canonical template. Replace `{{...}}` placeholders before writing.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>J.A.R.V.I.S. — Tarefas de {{PRINCIPAL_NAME}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=Geist+Mono:wght@100..900&display=swap" rel="stylesheet">
<style>
:root {
  --ds-gray-100: #f2f2f2;
  --ds-gray-200: #ebebeb;
  --ds-gray-700: #8f8f8f;
  --ds-gray-900: #4d4d4d;
  --ds-gray-1000: #171717;
  --ds-bg-100: #ffffff;
  --ds-bg-200: #fafafa;
  --ds-blue-700: #0070f5;
  --ds-blue-800: #0061d2;
  --ds-blue-200: #ade5ff;
  --ds-blue-900: #00407a;
  --ds-amber-700: #ffd60a;
  --ds-amber-900: #a35200;
  --ds-amber-200: #fff5cc;
  --ds-red-900: #cc2a2a;
  --ds-red-200: #ffe5e5;
  --ds-green-900: #297a3a;
  --ds-green-200: #d6f4dd;
  --ds-purple-900: #7820bb;
  --ds-purple-200: #ecd5ff;
  --ds-shadow-small: 0 2px 2px rgba(0,0,0,0.04);
  --ds-shadow-border: 0 0 0 1px var(--ds-gray-200);
  --ds-focus-ring: 0 0 0 2px var(--ds-bg-100), 0 0 0 4px var(--ds-blue-700);
  --geist-radius: 6px;
  --geist-radius-lg: 12px;
  --geist-gap: 24px;
  --geist-gap-half: 12px;
  --geist-gap-quarter: 6px;
  --font-sans: "Geist", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--ds-gray-1000);
  background: var(--ds-bg-100);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.5;
  letter-spacing: 0;
}
body { min-height: 100vh; padding: var(--geist-gap); }
.app { max-width: 1400px; margin: 0 auto; }
header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding-bottom: var(--geist-gap);
  border-bottom: 1px solid var(--ds-gray-200);
  margin-bottom: var(--geist-gap);
}
.title { font-size: 1.5rem; font-weight: 600; letter-spacing: -0.02em; }
.title strong { font-weight: 600; }
.subtitle { font-size: 0.875rem; color: var(--ds-gray-700); margin-top: 4px; }
.meta { font-family: var(--font-mono); font-size: 0.75rem; color: var(--ds-gray-700); text-align: right; }
.meta-stats { margin-top: 4px; color: var(--ds-gray-900); }
.kanban {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--geist-gap);
}
.column {
  background: var(--ds-bg-200);
  border: 1px solid var(--ds-gray-200);
  border-radius: var(--geist-radius-lg);
  padding: var(--geist-gap-half);
  min-height: 400px;
}
.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px var(--geist-gap-half) 8px;
  border-bottom: 1px solid var(--ds-gray-200);
  margin-bottom: var(--geist-gap-half);
}
.column-header.hoje::before {
  content: "";
  display: inline-block;
  width: 3px;
  height: 14px;
  background: var(--ds-blue-700);
  margin-right: 8px;
  vertical-align: middle;
  border-radius: 1px;
}
.column-name { font-size: 0.75rem; font-weight: 500; letter-spacing: 0.04em; text-transform: uppercase; color: var(--ds-gray-900); }
.column-count {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--ds-gray-700);
  background: var(--ds-bg-100);
  border: 1px solid var(--ds-gray-200);
  border-radius: var(--geist-radius);
  padding: 2px 6px;
}
.column-body { display: flex; flex-direction: column; gap: var(--geist-gap-half); }
.card {
  background: var(--ds-bg-100);
  border: 1px solid var(--ds-gray-200);
  border-radius: var(--geist-radius);
  padding: var(--geist-gap-half);
  box-shadow: var(--ds-shadow-small);
  transition: box-shadow 0.15s ease, transform 0.15s ease;
  cursor: default;
}
.card:hover {
  box-shadow: 0 0 0 1px var(--ds-gray-1000), 0 4px 8px -4px rgba(0,0,0,0.08);
  transform: translateY(-1px);
}
.card-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--ds-gray-1000);
  line-height: 1.4;
  margin-bottom: 8px;
}
.card-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  font-size: 0.75rem;
  color: var(--ds-gray-700);
}
.badge {
  font-family: var(--font-sans);
  font-size: 0.6875rem;
  font-weight: 500;
  letter-spacing: 0.0125em;
  height: 20px;
  line-height: 20px;
  padding: 0 6px;
  border-radius: var(--geist-radius);
  display: inline-flex;
  align-items: center;
}
.badge-priority-high { background: var(--ds-red-200); color: var(--ds-red-900); }
.badge-priority-medium { background: var(--ds-amber-200); color: var(--ds-amber-900); }
.badge-priority-low { background: var(--ds-gray-100); color: var(--ds-gray-900); }
.badge-project { background: var(--ds-purple-200); color: var(--ds-purple-900); }
.badge-overdue { background: var(--ds-red-900); color: var(--ds-bg-100); }
.badge-today { background: var(--ds-blue-200); color: var(--ds-blue-900); }
.due { font-family: var(--font-mono); }
.empty { color: var(--ds-gray-700); font-size: 0.875rem; padding: var(--geist-gap-half); text-align: center; }
.footer {
  margin-top: var(--geist-gap);
  padding-top: var(--geist-gap-half);
  border-top: 1px solid var(--ds-gray-200);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--ds-gray-700);
}
.footer-stats { display: flex; gap: 24px; }
.footer-stats span strong { color: var(--ds-gray-1000); font-weight: 500; }
@media (max-width: 1024px) {
  .kanban { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .kanban { grid-template-columns: 1fr; }
  header { flex-direction: column; align-items: flex-start; gap: 8px; }
  .meta { text-align: left; }
}
</style>
</head>
<body>
<div class="app">
  <header>
    <div>
      <div class="title">J.A.R.V.I.S. <strong>Tarefas</strong></div>
      <div class="subtitle">{{PRINCIPAL_NAME}}{{PRINCIPAL_PROFESSION_SUFFIX}}</div>
    </div>
    <div class="meta">
      <div>{{TODAY_DATE}}</div>
      <div class="meta-stats" id="meta-stats">— tarefas</div>
    </div>
  </header>

  <main class="kanban" id="kanban"></main>

  <div class="footer">
    <div class="footer-stats" id="footer-stats"></div>
    <div>http://localhost:7321 · /dash para atualizar</div>
  </div>
</div>

<script>
const TASKS = {{TASKS_JSON}};
const TODAY = new Date().toISOString().slice(0,10);

const COLUMNS = [
  { id: "hoje",    label: "Hoje",    accent: true },
  { id: "doing",   label: "Doing",   accent: false },
  { id: "backlog", label: "Backlog", accent: false },
  { id: "done",    label: "Done",    accent: false }
];

function isOverdue(task) {
  return task.due && task.due < TODAY && task.column !== "done";
}
function isDueToday(task) {
  return task.due === TODAY && task.column !== "done";
}
function priorityRank(p) {
  return p === "high" ? 0 : p === "medium" ? 1 : 2;
}
function sortTasks(tasks) {
  return [...tasks].sort((a, b) => {
    const aOver = isOverdue(a), bOver = isOverdue(b);
    if (aOver !== bOver) return aOver ? -1 : 1;
    const pr = priorityRank(a.priority) - priorityRank(b.priority);
    if (pr !== 0) return pr;
    if (a.due && b.due) return a.due.localeCompare(b.due);
    if (a.due) return -1;
    if (b.due) return 1;
    return 0;
  });
}
function formatDue(dueStr) {
  if (!dueStr) return "sem prazo";
  const [y, m, d] = dueStr.split("-");
  return d + "/" + m;
}
function renderCard(task) {
  const overdue = isOverdue(task);
  const today = isDueToday(task);
  const dueLabel = task.column === "done"
    ? (task.completed ? "concluida " + formatDue(task.completed) : "concluida")
    : formatDue(task.due);
  const dueBadge = overdue
    ? '<span class="badge badge-overdue">vencida</span>'
    : (today ? '<span class="badge badge-today">hoje</span>' : "");
  const projectBadge = task.project
    ? '<span class="badge badge-project">' + escapeHtml(task.project) + '</span>'
    : "";
  return `
    <div class="card">
      <div class="card-title">${escapeHtml(task.title)}</div>
      <div class="card-meta">
        <span class="badge badge-priority-${task.priority}">${task.priority}</span>
        ${projectBadge}
        ${dueBadge}
        <span class="due">${dueLabel}</span>
      </div>
    </div>
  `;
}
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
function renderKanban() {
  const counts = { hoje: 0, doing: 0, backlog: 0, done: 0 };
  const grouped = { hoje: [], doing: [], backlog: [], done: [] };
  for (const t of TASKS) {
    const col = grouped[t.column] ? t.column : "backlog";
    grouped[col].push(t);
    counts[col]++;
  }
  const recentDone = sortTasks(grouped.done.filter(t => {
    if (!t.completed) return false;
    const d = new Date(t.completed);
    const cutoff = new Date(); cutoff.setDate(cutoff.getDate() - 7);
    return d >= cutoff;
  }));
  grouped.done = recentDone;

  const root = document.getElementById("kanban");
  root.innerHTML = COLUMNS.map(col => {
    const tasks = sortTasks(grouped[col.id] || []);
    const cards = tasks.length
      ? tasks.map(renderCard).join("")
      : '<div class="empty">vazio</div>';
    const headerClass = col.accent ? "column-header hoje" : "column-header";
    return `
      <div class="column">
        <div class="${headerClass}">
          <span class="column-name">${col.label}</span>
          <span class="column-count">${tasks.length}</span>
        </div>
        <div class="column-body">${cards}</div>
      </div>
    `;
  }).join("");

  const total = TASKS.length;
  const overdue = TASKS.filter(isOverdue).length;
  document.getElementById("meta-stats").textContent =
    total + " tarefa" + (total === 1 ? "" : "s") + (overdue > 0 ? " · " + overdue + " vencida" + (overdue === 1 ? "" : "s") : "");

  const footer = document.getElementById("footer-stats");
  footer.innerHTML = `
    <span><strong>${counts.hoje}</strong> hoje</span>
    <span><strong>${counts.doing}</strong> doing</span>
    <span><strong>${counts.backlog}</strong> backlog</span>
    <span><strong>${counts.done}</strong> done</span>
  `;
}
renderKanban();
</script>
</body>
</html>
```

---

## Quick reference — server commands by OS

### Windows (PowerShell or Bash)
```powershell
# Start server in background (PowerShell)
Start-Process python -ArgumentList "-m","http.server","7321","--directory","dashboard","--bind","127.0.0.1" -NoNewWindow

# Open browser
start http://localhost:7321
```

### macOS / Linux
```bash
# Start server in background
python3 -m http.server 7321 --directory dashboard --bind 127.0.0.1 &

# Open browser
open http://localhost:7321         # macOS
xdg-open http://localhost:7321     # Linux
```

The Bash tool with `run_in_background: true` is the cleanest cross-platform path inside Claude Code.
