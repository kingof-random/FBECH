# F-BECH — FEROX BAJA Engineering & Compliance Hub

**Platform:** FEROX BAJA Engineering & Compliance Hub (F-BECH)  
**Team:** FEROX  
**Competition:** BAJA SAEINDIA Chennai 2027 — ICE  
**Controlling source:** BAJA SAEINDIA Chennai 2027 ICE Rulebook, Version 1.0, dated 01 September 2026 (100 PDF pages)

F-BECH is a FEROX-specific engineering and rule-compliance workspace. It converts the official rulebook into an interactive rule navigator, a measurable verification workspace, an evidence register and a printable compliance report. It is deliberately **not** a generic rulebook summariser.

---

## 1. Quick start

```bash
cd fbech
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 seed.py          # creates instance/fbech.db (skips if already seeded)
python3 app.py           # http://localhost:8000
```

or simply:

```bash
./run.sh
```

Runtime dependency: **Flask** only. `pypdf` and `pymupdf` are used by the extraction/validation scripts, not by the running app.

### Persistent storage

- SQLite database: `instance/fbech.db`
- Uploaded evidence: `uploads/evidence/`
- Rendered rulebook pages: `static/src/page-001.jpg … page-100.jpg`

All user-entered measurements, statuses, remarks, evidence metadata, documents, issues and revisions persist in SQLite. Uploaded files remain associated with their check through the `evidence.check_id` foreign key.

### Backup

`GET /api/export` downloads a JSON snapshot of meta, rules, checks, evidence metadata, docs, issues and revisions. The evidence files themselves are in `uploads/evidence/`.

---

## 2. Architecture

```
browser (single-page app, vanilla JS)
   │  fetch /api/bootstrap, /api/checks/:id, /api/checks/:id/evidence, …
   ▼
Flask app (app.py)
   ├── JSON API
   ├── SQLite (instance/fbech.db)
   ├── evidence file store (uploads/evidence/)
   └── static rulebook page images (static/src/)
```

### Why this stack

- **Flask + SQLite** — small, auditable, zero external services. The database is a single file the team can back up or inspect.
- **Vanilla JS SPA** — no build step, no CDN dependency, works in the preview iframe and offline. The UI is a single `static/app.js` with hash routing.
- **Data-driven rules and checks** — the core tables (`rules`, `checks`) are independent of the UI. Adding an article means adding rows, not rewriting components.

### Data model

| Table | Purpose |
|---|---|
| `rules` | One row per numbered clause. Official wording (JSON paragraphs), rule number, part/article, PDF page, plain-English layer, engineering layer, ambiguity notes, components, cross-references, figures, tables, extraction status. |
| `checks` | One row per engineering verification check. Rule link, exact criterion, method, evidence required, numeric evaluation config, measured value, status, remarks, assignee. |
| `evidence` | Uploaded files linked to a check. |
| `docs` | Engineering documentation entries by category. |
| `issues` | Outstanding issues with severity, status, rule link, owner. |
| `revisions` | Design revision history. |
| `meta` | Team, vehicle, competition, report header fields. |

### API

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/bootstrap` | Full app payload: rules, checks, evidence, docs, issues, revisions, meta, computed stats. |
| GET | `/api/rules/<id>` | One rule, full layers. |
| POST | `/api/checks/<id>` | Update measured value / status / remarks / assignee. Server recomputes the automatic result. |
| POST | `/api/checks/<id>/evidence` | Multipart upload; saves files and links them to the check. |
| DELETE | `/api/evidence/<id>` | Remove an evidence file and its row. |
| POST/PUT/DELETE | `/api/docs`, `/api/issues`, `/api/revisions` | Documentation, issue and revision CRUD. |
| POST | `/api/meta` | Project settings. |
| GET | `/api/dashboard` | Recomputed dashboard statistics. |
| GET | `/source/page/<n>` | Rendered PDF page image. |
| GET | `/uploads/<file>` | Evidence download. |
| GET | `/api/export` | JSON backup. |

---

## 3. Extraction pipeline (Phase 1)

1. `extract_outline.py` reads `data/pages.json` (produced from the PDF with `pypdf`), detects every `Part`, `Article` and numbered `B.x.y` heading, and captures the body text until the next heading.
2. It writes `data/sections_auto.json`: **512 numbered rules** across Parts A–D, each with its PDF page.
3. Every PDF page was rendered to `static/src/page-NNN.jpg` with PyMuPDF for visual verification and the in-app “View PDF page” feature.
4. Part B Article 3 was then **manually curated** in `b3_rules_a/b/c.py` against the page images:
   - official wording transcribed clause by clause;
   - plain-English and engineering layers written as separate fields;
   - tables (Figure B-9), figures, notes and exceptions preserved;
   - ambiguous sentences recorded, not “fixed”;
   - 127 engineering checks defined in `b3_checks_a/b.py` (RC-001…RC-127).
5. `validate_b3.py` compares the curated B.3 wording against the page-extracted text (token coverage) and checks every rule has a check or is a parent heading.
6. `crop_figures.py` pairs each `Figure B-n:` caption with the image block directly above it in the PDF, renders that region at 3× and writes `static/img/fig-B-nn.png` plus `static/figures.json` (52 figures, B-4 … B-63). Figures whose caption is really a table (e.g. B-9, B-58) are not cropped as images — the table itself is stored in `table_data`.

### Source-integrity rules applied

- Official wording is reproduced **verbatim**. Only PDF line-break hyphenation artefacts are normalised (e.g. `front- half` → `front-half`, `Figure B- 12` → `Figure B-12`).
- No dimension, material, tolerance, exception or acceptance criterion has been invented.
- Where the printed source is grammatically defective, the defect is preserved and flagged on the rule’s **Ambiguities** tab.
- Numeric auto-evaluation exists only where the rule states a threshold. Qualitative requirements remain manual.
- Official wording, plain-English explanation and engineering interpretation are stored and rendered as separate layers.

---

## 4. Current coverage

| Scope | Rules | Status |
|---|---|---|
| Full rulebook inventory (Parts A–D) | 512 | Exact source text, PDF page, cross-references — searchable |
| Part B, Article 3 — Roll Cage | 38 | **Fully validated:** plain-English + engineering layers, 127 checks, numeric evaluation, evidence |
| Rulebook figures | 52 | Cropped verbatim from the PDF at 3×, linked from the rules that reference them |
| All other articles | 474 | Source text only; interpretation and checks pending Phase 5 |

**Not implemented by design:** Part B Article 14 (Electric Powertrain) is listed in the Table of Contents with “Error! Bookmark not defined.” and has no corresponding article in the 100-page document. It is flagged in the Coverage Matrix, not fabricated.

---

## 5. How to extend to the remaining articles

The core architecture does not need to change:

1. Create `b4_rules.py` (or extend the existing pattern) with the official text, page, plain and engineering layers for Article 4.
2. Create `b4_checks.py` with the verification checks and numeric thresholds.
3. Add them to `seed.py` (`B4` list and `CHECKS` list).
4. Run `python3 seed.py --reset` (or delete `instance/fbech.db` and re-run `seed.py`) to rebuild the rules/checks tables. **Note:** deleting the database also deletes user-entered verification data — export first.
5. The navigator, dashboard, workspace, evidence, report and coverage views update automatically from the data.

---

## 6. Validation and known limitations

- `python3 validate_b3.py` reports token-coverage differences and structural gaps (currently: 0 structural problems, 1 known token difference). The only remaining token difference is B.3.2.16, where the printed equations (`kb = E·I`, `Sb = Sy·I / c`) are reproduced from the equation images and `Nm2` is typeset as `Nm²`.
- Parent headings (B.3.2.14, B.3.3, B.3.6, B.3.7) intentionally have no body text; their subsections carry the requirements.
- The BSC Roll Cage Specification Sheet template, cost forms and official submission portal are external documents and are not reproduced.
- “Verified” is always **team self-verification**, never official technical inspection.
- The app is a single-team internal tool; it has no authentication. Do not expose it to the public internet without adding authentication and a production WSGI server.

---

## 7. Directory map

```
fbech/
├── app.py                  Flask app and JSON API
├── seed.py                 builds instance/fbech.db from the rule/check data
├── extract_outline.py      PDF text → structured rule inventory
├── validate_b3.py          Phase 3 validation
├── crop_figures.py         crops Figure B-n images out of the PDF
├── b3_rules_a/b/c.py       curated B.3 rules (official / plain / engineering / notes)
├── b3_checks_a/b.py        127 B.3 engineering checks
├── templates/index.html    SPA shell
├── static/app.js           UI (hash routing, dashboard, navigator, workspace, report)
├── static/app.css          FEROX visual system
├── static/src/             rendered PDF pages 1–100
├── static/img/             cropped rulebook figures (fig-B-nn.png)
├── static/figures.json     figure → file + page index
├── data/pages.json         page-by-page extracted text
├── data/sections_auto.json full rulebook inventory
├── instance/fbech.db       SQLite database (created by seed.py)
└── uploads/evidence/       uploaded evidence files
```

---

## 8. FEROX verification workflow

1. Open **Rulebook Navigator**, select the rule, read the **Official requirement** and the **Engineering interpretation**. Figures cited by the clause appear cropped from the PDF below the text.
2. Follow cross-references inline; the referenced rule expands below with a return trail.
3. Open **Compliance Workspace**, filter by component or subsystem.
4. Enter the measured value (or record the qualitative inspection result), attach the evidence, set the responsible member and write the remarks.
5. Watch the dashboard and article/component progress update from the recorded checks.
6. Print the **Compliance Report** for the design review or technical inspection file.

### Responsive behaviour

The layout is a fixed sidebar + fluid content area. Below 900 px the sidebar becomes a slide-in drawer (☰), grids collapse to one column, tables scroll inside their cards and the printable report scrolls horizontally inside its sections. Verified with no horizontal page overflow at 1500 px, 1024 px and 390 px.

**Reminder:** a complete checklist is not a compliant vehicle. Technical Inspection and the BSC Technical Committee decide acceptance at the event.


## Production deployment (Render)

Create a **Web Service** from this repository and select branch `feature/auth-render-deployment` (merge to `main` only when ready).

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `python seed.py && gunicorn --workers 1 --threads 4 --timeout 120 --bind 0.0.0.0:$PORT app:app`
- Add a persistent disk mounted at `/var/data` (at least 1 GB).
- Environment variables:
  - `FBECH_DATA_DIR=/var/data`
  - `SECRET_KEY` = a long random secret
  - `FBECH_ADMIN_USERNAME` = chosen admin username
  - `FBECH_ADMIN_PASSWORD` = strong initial admin password
  - `COOKIE_SECURE=1`

The first deployment creates the initial admin account only if the database has no users. There is no public registration. Keep one Gunicorn worker because SQLite is stored on the persistent disk. Back up `/var/data/fbech.db` and `/var/data/uploads/evidence/` regularly.

Rulebook pages, figures and individual rule lookups remain public. Workspace APIs, exports and evidence downloads require login. Do not expose a production instance without setting the environment variables above.
