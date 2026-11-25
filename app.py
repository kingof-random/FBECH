# -*- coding: utf-8 -*-
import json, os, re, sqlite3, datetime, secrets, werkzeug
from flask import Flask, request, jsonify, send_from_directory, render_template, abort, session
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('FBECH_DATA_DIR', os.path.join(BASE, 'instance'))
os.makedirs(DATA_DIR, exist_ok=True)
DB = os.path.join(DATA_DIR, 'fbech.db')
UPLOAD = os.path.join(DATA_DIR, 'uploads', 'evidence')
SRC = os.path.join(BASE, 'static', 'src')
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(SRC, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'local-development-only-change-me'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('COOKIE_SECURE', '1' if os.environ.get('RENDER') else '0') == '1'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=12)

STATUSES = ['Not Started', 'In Progress', 'Pending Verification', 'Verified', 'Failed', 'Not Applicable']
SEVERITIES = ['Critical', 'High', 'Medium', 'Low']
DOC_CATS = ['Design Assumptions', 'CAD Measurements', 'Material Selection', 'Procurement Records',
            'Welding & Fabrication', 'Engineering Calculations', 'Inspection Records',
            'Evidence & Photographs', 'Design Revision History']

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_auth():
    con = db()
    con.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )""")
    # Bootstrap exactly one initial account when the database has no users.
    username = os.environ.get('FBECH_ADMIN_USERNAME', '').strip()
    password = os.environ.get('FBECH_ADMIN_PASSWORD', '')
    count = con.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if count == 0 and username and password:
        con.execute('INSERT INTO users (username,password_hash,created_at) VALUES (?,?,?)',
                    (username, generate_password_hash(password), datetime.datetime.now().isoformat(timespec='seconds')))
    con.commit()
    con.close()

init_auth()

@app.before_request
def protect_private_data():
    path = request.path
    public_paths = ('/api/login', '/api/session', '/api/logout')
    public_rulebook = path.startswith('/api/rules/') or path.startswith('/source/page/') or path in ('/figures.json',)
    if path.startswith('/api/') and path not in public_paths and not public_rulebook:
        if not session.get('user_id'):
            return jsonify({'error': 'Authentication required'}), 401
    if path.startswith('/uploads/') and not session.get('user_id'):
        return jsonify({'error': 'Authentication required'}), 401
    if request.method in ('POST', 'PUT', 'PATCH', 'DELETE') and path.startswith('/api/') and path != '/api/login':
        expected = session.get('csrf_token')
        supplied = request.headers.get('X-CSRF-Token', '')
        if not expected or not secrets.compare_digest(expected, supplied):
            return jsonify({'error': 'Invalid or missing CSRF token'}), 403

@app.route('/api/session')
def auth_session():
    if not session.get('user_id'):
        return jsonify({'authenticated': False})
    return jsonify({'authenticated': True, 'username': session.get('username'),
                    'csrf_token': session.get('csrf_token')})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get('username', '')).strip()
    password = str(data.get('password', ''))
    con = db()
    user = con.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    con.close()
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Incorrect username or password'}), 401
    session.clear()
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['csrf_token'] = secrets.token_urlsafe(32)
    session.permanent = True
    return jsonify({'ok': True, 'username': user['username'], 'csrf_token': session['csrf_token']})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})

def now():
    return datetime.datetime.now().isoformat(timespec='seconds')

def J(v):
    if v is None: return None
    try: return json.loads(v)
    except Exception: return v

def get_meta(con):
    return {r['key']: r['value'] for r in con.execute('SELECT key,value FROM meta')}

def check_row(r):
    d = dict(r)
    d['auto_result'] = evaluate(d, d.get('measured'))
    return d

def evaluate(c, measured):
    ev = c.get('eval') or 'none'
    if ev == 'none': return None
    if measured is None or str(measured).strip() == '': return None
    try:
        v = float(str(measured).strip())
    except Exception:
        return None
    if ev == 'min':
        return 'pass' if v >= c['min_val'] else 'fail'
    if ev == 'max':
        return 'pass' if v <= c['max_val'] else 'fail'
    if ev == 'range':
        return 'pass' if c['min_val'] <= v <= c['max_val'] else 'fail'
    return None

def load_rules(con, with_body=True):
    cols = 'id,part,article,number,title,kind,priority,page,status,article_title,part_title,components,xrefs,figures'
    if with_body:
        cols += ',body,plain,engineering,notes,table_data'
    out = []
    for r in con.execute(f'SELECT {cols} FROM rules ORDER BY page, id'):
        d = dict(r)
        for k in ('components','xrefs','figures','body','plain','engineering','notes','table_data'):
            if k in d: d[k] = J(d[k])
        out.append(d)
    return out

def load_checks(con):
    out = []
    for r in con.execute('SELECT * FROM checks ORDER BY sort_order, id'):
        out.append(check_row(r))
    return out

def stats(checks, issues, rules):
    total = len(checks)
    by = {s: 0 for s in STATUSES}
    for c in checks: by[c['status']] = by.get(c['status'], 0) + 1
    applicable = total - by.get('Not Applicable', 0)
    verified = by.get('Verified', 0)
    failed = by.get('Failed', 0)
    # article progress
    art = {}
    rule_art = {r['id']: r['article'] for r in rules}
    for c in checks:
        a = rule_art.get(c['rule_id'], '?')
        d = art.setdefault(a, {'article': a, 'total': 0, 'verified': 0, 'failed': 0, 'na': 0})
        d['total'] += 1
        if c['status'] == 'Verified': d['verified'] += 1
        if c['status'] == 'Failed': d['failed'] += 1
        if c['status'] == 'Not Applicable': d['na'] += 1
    for d in art.values():
        app = d['total'] - d['na']
        d['pct'] = round(100 * d['verified'] / app, 1) if app else 0.0
    # component progress
    comp = {}
    for c in checks:
        d = comp.setdefault(c['component'], {'component': c['component'], 'total': 0, 'verified': 0, 'failed': 0, 'na': 0})
        d['total'] += 1
        if c['status'] == 'Verified': d['verified'] += 1
        if c['status'] == 'Failed': d['failed'] += 1
        if c['status'] == 'Not Applicable': d['na'] += 1
    for d in comp.values():
        app = d['total'] - d['na']
        d['pct'] = round(100 * d['verified'] / app, 1) if app else 0.0
    # rules coverage
    rule_counts = {}
    for r in rules:
        a = r['article']
        d = rule_counts.setdefault(a, {'article': a, 'rules': 0, 'validated': 0, 'source_only': 0})
        d['rules'] += 1
        if r['status'] == 'validated': d['validated'] += 1
        else: d['source_only'] += 1
    return {
        'total_checks': total,
        'by_status': by,
        'applicable': applicable,
        'verified': verified,
        'failed': failed,
        'pending': by.get('Pending Verification', 0),
        'in_progress': by.get('In Progress', 0),
        'not_started': by.get('Not Started', 0),
        'not_applicable': by.get('Not Applicable', 0),
        'compliance_pct': round(100 * verified / applicable, 1) if applicable else 0.0,
        'worked_pct': round(100 * (applicable - by.get('Not Started', 0)) / applicable, 1) if applicable else 0.0,
        'evidence_pct': round(100 * sum(1 for c in checks if c.get('_evidence', 0) > 0) / total, 1) if total else 0.0,
        'article_progress': sorted(art.values(), key=lambda x: (x['article'].split('.')[0], int(x['article'].split('.')[1]))),
        'component_progress': sorted(comp.values(), key=lambda x: (-x['total'], x['component'])),
        'rule_coverage': sorted(rule_counts.values(), key=lambda x: (x['article'].split('.')[0], int(x['article'].split('.')[1]))),
        'open_issues': len([i for i in issues if i['status'] != 'Closed']),
        'critical_issues': len([i for i in issues if i['status'] != 'Closed' and i['severity'] in ('Critical', 'High')]),
        'total_rules': len(rules),
        'validated_rules': len([r for r in rules if r['status'] == 'validated']),
    }


@app.route('/healthz')
def healthz():
    return jsonify({'ok': True})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/figures.json')
def figures_json():
    return send_from_directory('static', 'figures.json')

@app.route('/api/bootstrap')
def bootstrap():
    con = db()
    rules = load_rules(con, True)
    checks = load_checks(con)
    ev = [dict(r) for r in con.execute('SELECT * FROM evidence ORDER BY id')]
    evcount = {}
    for e in ev: evcount[e['check_id']] = evcount.get(e['check_id'], 0) + 1
    for c in checks: c['_evidence'] = evcount.get(c['id'], 0)
    docs = [dict(r) for r in con.execute('SELECT * FROM docs ORDER BY id DESC')]
    issues = [dict(r) for r in con.execute('SELECT * FROM issues ORDER BY id DESC')]
    revisions = [dict(r) for r in con.execute('SELECT * FROM revisions ORDER BY id DESC')]
    meta = get_meta(con)
    st = stats(checks, issues, rules)
    con.close()
    return jsonify({'meta': meta, 'rules': rules, 'checks': checks, 'evidence': ev,
                    'docs': docs, 'issues': issues, 'revisions': revisions, 'stats': st})

@app.route('/api/rules/<rid>')
def rule(rid):
    con = db()
    r = con.execute('SELECT * FROM rules WHERE id=?', (rid,)).fetchone()
    con.close()
    if not r: abort(404)
    d = dict(r)
    for k in ('components','xrefs','figures','body','plain','engineering','notes','table_data'):
        d[k] = J(d[k])
    return jsonify(d)

@app.route('/api/checks/<cid>', methods=['POST'])
def update_check(cid):
    con = db()
    r = con.execute('SELECT * FROM checks WHERE id=?', (cid,)).fetchone()
    if not r:
        con.close(); abort(404)
    data = request.get_json(force=True, silent=True) or {}
    fields = {}
    if 'status' in data and data['status'] in STATUSES: fields['status'] = data['status']
    if 'measured' in data: fields['measured'] = data['measured'] if str(data['measured']).strip() != '' else None
    if 'remarks' in data: fields['remarks'] = data['remarks']
    if 'assignee' in data: fields['assignee'] = data['assignee']
    cur = dict(r)
    cur.update(fields)
    auto = evaluate(cur, cur.get('measured'))
    if 'status' not in fields and auto and cur.get('status') == 'Not Started':
        fields['status'] = 'Verified' if auto == 'pass' else 'Failed'
        cur['status'] = fields['status']
    if fields:
        sets = ', '.join(f'{k}=?' for k in fields)
        con.execute(f'UPDATE checks SET {sets}, updated_at=? WHERE id=?', list(fields.values()) + [now(), cid])
        con.commit()
    out = dict(con.execute('SELECT * FROM checks WHERE id=?', (cid,)).fetchone())
    out['auto_result'] = evaluate(out, out.get('measured'))
    evcount = con.execute('SELECT COUNT(*) FROM evidence WHERE check_id=?', (cid,)).fetchone()[0]
    con.close()
    return jsonify({'ok': True, 'check': out, 'evidence_count': evcount})

@app.route('/api/checks/<cid>/evidence', methods=['POST'])
def upload_evidence(cid):
    con = db()
    r = con.execute('SELECT id FROM checks WHERE id=?', (cid,)).fetchone()
    if not r:
        con.close(); abort(404)
    files = request.files.getlist('files')
    note = request.form.get('note', '')
    saved = []
    for f in files:
        if not f or f.filename == '': continue
        fn = werkzeug.utils.secure_filename(f.filename)
        ts = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        stored = f'{ts}_{fn}'
        f.save(os.path.join(UPLOAD, stored))
        cur = con.execute('INSERT INTO evidence (check_id,filename,stored,note,uploaded_at) VALUES (?,?,?,?,?)',
                          (cid, fn, stored, note, now()))
        saved.append(dict(con.execute('SELECT * FROM evidence WHERE id=?', (cur.lastrowid,)).fetchone()))
    con.commit()
    evcount = con.execute('SELECT COUNT(*) FROM evidence WHERE check_id=?', (cid,)).fetchone()[0]
    con.close()
    return jsonify({'ok': True, 'saved': saved, 'evidence_count': evcount})

@app.route('/api/evidence/<int:eid>', methods=['DELETE'])
def delete_evidence(eid):
    con = db()
    r = con.execute('SELECT * FROM evidence WHERE id=?', (eid,)).fetchone()
    if not r:
        con.close(); abort(404)
    try:
        os.remove(os.path.join(UPLOAD, r['stored']))
    except OSError:
        pass
    con.execute('DELETE FROM evidence WHERE id=?', (eid,))
    con.commit()
    evcount = con.execute('SELECT COUNT(*) FROM evidence WHERE check_id=?', (r['check_id'],)).fetchone()[0]
    con.close()
    return jsonify({'ok': True, 'evidence_count': evcount})

@app.route('/api/docs', methods=['POST'])
def add_doc():
    con = db(); data = request.get_json(force=True)
    cur = con.execute('INSERT INTO docs (category,title,body,ref,created_at,updated_at) VALUES (?,?,?,?,?,?)',
                      (data.get('category','Design Assumptions'), data.get('title',''), data.get('body',''), data.get('ref',''), now(), now()))
    con.commit()
    d = dict(con.execute('SELECT * FROM docs WHERE id=?', (cur.lastrowid,)).fetchone())
    con.close(); return jsonify({'ok': True, 'doc': d})

@app.route('/api/docs/<int:did>', methods=['PUT', 'DELETE'])
def edit_doc(did):
    con = db()
    if request.method == 'DELETE':
        con.execute('DELETE FROM docs WHERE id=?', (did,)); con.commit(); con.close()
        return jsonify({'ok': True})
    data = request.get_json(force=True)
    con.execute('UPDATE docs SET category=?,title=?,body=?,ref=?,updated_at=? WHERE id=?',
                (data.get('category'), data.get('title'), data.get('body'), data.get('ref'), now(), did))
    con.commit(); con.close(); return jsonify({'ok': True})

@app.route('/api/issues', methods=['POST'])
def add_issue():
    con = db(); data = request.get_json(force=True)
    cur = con.execute('INSERT INTO issues (title,detail,severity,status,rule_id,owner,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)',
                      (data.get('title',''), data.get('detail',''), data.get('severity','Medium'),
                       data.get('status','Open'), data.get('rule_id',''), data.get('owner',''), now(), now()))
    con.commit()
    d = dict(con.execute('SELECT * FROM issues WHERE id=?', (cur.lastrowid,)).fetchone())
    con.close(); return jsonify({'ok': True, 'issue': d})

@app.route('/api/issues/<int:iid>', methods=['PUT', 'DELETE'])
def edit_issue(iid):
    con = db()
    if request.method == 'DELETE':
        con.execute('DELETE FROM issues WHERE id=?', (iid,)); con.commit(); con.close()
        return jsonify({'ok': True})
    data = request.get_json(force=True)
    con.execute('UPDATE issues SET title=?,detail=?,severity=?,status=?,rule_id=?,owner=?,updated_at=? WHERE id=?',
                (data.get('title'), data.get('detail'), data.get('severity'), data.get('status'),
                 data.get('rule_id'), data.get('owner'), now(), iid))
    con.commit(); con.close(); return jsonify({'ok': True})

@app.route('/api/revisions', methods=['POST'])
def add_revision():
    con = db(); data = request.get_json(force=True)
    cur = con.execute('INSERT INTO revisions (rev,date,author,description) VALUES (?,?,?,?)',
                      (data.get('rev',''), data.get('date',''), data.get('author',''), data.get('description','')))
    con.commit()
    d = dict(con.execute('SELECT * FROM revisions WHERE id=?', (cur.lastrowid,)).fetchone())
    con.close(); return jsonify({'ok': True, 'revision': d})

@app.route('/api/revisions/<int:rid>', methods=['DELETE'])
def del_revision(rid):
    con = db(); con.execute('DELETE FROM revisions WHERE id=?', (rid,)); con.commit(); con.close()
    return jsonify({'ok': True})

@app.route('/api/meta', methods=['POST'])
def save_meta():
    con = db(); data = request.get_json(force=True)
    for k, v in data.items():
        con.execute('INSERT OR REPLACE INTO meta (key,value) VALUES (?,?)', (k, str(v)))
    con.commit(); con.close(); return jsonify({'ok': True})

@app.route('/api/dashboard')
def dashboard():
    con = db()
    rules = load_rules(con, False)
    checks = load_checks(con)
    ev = [dict(r) for r in con.execute('SELECT * FROM evidence')]
    evcount = {}
    for e in ev: evcount[e['check_id']] = evcount.get(e['check_id'], 0) + 1
    for c in checks: c['_evidence'] = evcount.get(c['id'], 0)
    issues = [dict(r) for r in con.execute('SELECT * FROM issues')]
    st = stats(checks, issues, rules)
    con.close()
    return jsonify(st)

@app.route('/source/page/<int:n>')
def source_page(n):
    if n < 1 or n > 100: abort(404)
    return send_from_directory(SRC, f'page-{n:03d}.jpg', max_age=86400)

@app.route('/uploads/<path:fn>')
def uploads(fn):
    return send_from_directory(UPLOAD, fn, as_attachment=True)

@app.route('/api/export')
def export():
    con = db()
    data = {
        'meta': get_meta(con),
        'rules': load_rules(con, True),
        'checks': load_checks(con),
        'evidence': [dict(r) for r in con.execute('SELECT * FROM evidence')],
        'docs': [dict(r) for r in con.execute('SELECT * FROM docs')],
        'issues': [dict(r) for r in con.execute('SELECT * FROM issues')],
        'revisions': [dict(r) for r in con.execute('SELECT * FROM revisions')],
    }
    con.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
