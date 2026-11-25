# -*- coding: utf-8 -*-
import json, os, re, sqlite3, sys, datetime
from b3_rules_a import B3_RULES_A
from b3_rules_b import B3_RULES_B
from b3_rules_c import B3_RULES_C
from b3_checks_a import CHECKS_A
from b3_checks_b import CHECKS_B

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('FBECH_DATA_DIR', os.path.join(BASE, 'instance'))
os.makedirs(DATA_DIR, exist_ok=True)
DB = os.path.join(DATA_DIR, 'fbech.db')

B3 = B3_RULES_A + B3_RULES_B + B3_RULES_C
CHECKS = CHECKS_A + CHECKS_B

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS rules (
  id TEXT PRIMARY KEY, part TEXT NOT NULL, article TEXT NOT NULL, number TEXT NOT NULL,
  title TEXT NOT NULL, kind TEXT, priority TEXT, page INTEGER, article_title TEXT, part_title TEXT,
  body TEXT, plain TEXT, engineering TEXT, notes TEXT, components TEXT,
  xrefs TEXT, figures TEXT, table_data TEXT, status TEXT, sort_order INTEGER
);
CREATE TABLE IF NOT EXISTS checks (
  id TEXT PRIMARY KEY, rule_id TEXT, title TEXT, component TEXT, criterion TEXT,
  method TEXT, evidence_required TEXT, eval TEXT, min_val REAL, max_val REAL,
  unit TEXT, label TEXT, priority TEXT, status TEXT, measured TEXT, remarks TEXT,
  assignee TEXT, updated_at TEXT, sort_order INTEGER
);
CREATE TABLE IF NOT EXISTS evidence (
  id INTEGER PRIMARY KEY AUTOINCREMENT, check_id TEXT, filename TEXT, stored TEXT,
  note TEXT, uploaded_at TEXT
);
CREATE TABLE IF NOT EXISTS docs (
  id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, title TEXT, body TEXT, ref TEXT,
  created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS issues (
  id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, detail TEXT, severity TEXT,
  status TEXT, rule_id TEXT, owner TEXT, created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS revisions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, rev TEXT, date TEXT, author TEXT, description TEXT
);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""

META = {
 'team': 'FEROX',
 'vehicle': 'FEROX 2027 ICE',
 'competition': 'BAJA SAEINDIA Chennai 2027 — ICE',
 'rulebook': 'BAJA SAEINDIA Chennai 2027 ICE Rulebook, Version 1.0, 01 September 2026',
 'event_dates': '19, 20 & 21 March 2027',
 'venue': 'Hindustan College of Engineering & Technology, Pollachi Highway, Coimbatore - 641 032, Tamil Nadu, INDIA',
 'car_number': '',
 'lead': '',
 'season': '2027',
 'generated': '2026-11-24',
 'source_pages': '100',
 'note': 'Team self-verification only. Official acceptance is determined by BSC Technical Inspection and the Technical Committee.'
}

def part_article(key):
    m = re.match(r'^([ABCD])\.(\d+)', key)
    if not m: return ('?', '?')
    return (m.group(1), m.group(1) + '.' + m.group(2))

def sort_key(key):
    nums = [int(x) for x in re.findall(r'\d+', key)]
    return tuple(nums)

def main():
    if '--reset' in sys.argv:
        for suffix in ('', '-wal', '-shm'):
            p = DB + suffix
            if os.path.exists(p):
                os.remove(p)
        print('Reset requested: database removed')
    sections = json.load(open(os.path.join(BASE, 'data', 'sections_auto.json')))
    b3_ids = {r['id'] for r in B3}
    rows = []
    order = 0
    for s in sections:
        order += 1
        if s['kind'] == 'part':
            continue
        if s['kind'] == 'article':
            continue
        key = s['key']
        if key in b3_ids:
            continue
        part, article = part_article(key)
        paras = [p for p in s['text'].split('\n') if p.strip()]
        rows.append(dict(id=key, part=part, article=article, number=key, title=s['title'],
                         kind='source_text', priority='Medium', page=s['page'], article_title='', part_title='',
                         body=json.dumps(paras, ensure_ascii=False),
                         plain=None, engineering=None, notes=None,
                         components=json.dumps([], ensure_ascii=False),
                         xrefs=None, figures=None, table_data=None,
                         status='source_only', sort_order=order))
    # curated B.3
    for i, r in enumerate(B3):
        part, article = part_article(r['id'])
        rows.append(dict(id=r['id'], part=part, article=article, number=r['id'], title=r['title'],
                         kind=r.get('kind','requirement'), priority=r.get('priority','Medium'),
                         page=r['page'], article_title='', part_title='', body=json.dumps(r['body'], ensure_ascii=False),
                         plain=json.dumps(r.get('plain',[]), ensure_ascii=False),
                         engineering=json.dumps(r.get('engineering',[]), ensure_ascii=False),
                         notes=json.dumps(r.get('notes',[]), ensure_ascii=False),
                         components=json.dumps(r.get('components',[]), ensure_ascii=False),
                         xrefs=None, figures=None,
                         table_data=json.dumps(r['table'], ensure_ascii=False) if r.get('table') else None,
                         status='validated', sort_order=100000+i))
    # article / part titles from the document outline
    part_titles = {}
    art_titles = {}
    for s in sections:
        if s['kind'] == 'part':
            part_titles[s['key']] = s['title']
        elif s['kind'] == 'article':
            pass
    # article titles need part context: use page order and the next part boundary
    cur_part = None
    for s in sections:
        if s['kind'] == 'part':
            cur_part = s['key']
        elif s['kind'] == 'article' and cur_part:
            art_titles[f'{cur_part}.{s["key"]}'] = s['title']
    for x in rows:
        x['part_title'] = part_titles.get(x['part'], '')
        x['article_title'] = art_titles.get(x['article'], '')
    # sort: by page then numeric id
    rows.sort(key=lambda x: (x['page'], sort_key(x['id']), x['id']))
    # xrefs + figures
    all_ids = {x['id'] for x in rows}
    for x in rows:
        text = ' '.join(json.loads(x['body'])) if x['body'] else ''
        refs = []
        for m in re.finditer(r'\b([ABCD]\.\d+(?:\.\d+)*)\b', text):
            ref = m.group(1)
            if ref == x['id']: continue
            if ref in [r['ref'] for r in refs]: continue
            if ref in all_ids:
                refs.append({'ref': ref, 'resolved': True, 'target': ref})
            else:
                # article-level reference (e.g. B.12) -> first rule of that article
                cands = [i for i in all_ids if i.startswith(ref + '.')]
                if cands:
                    target = sorted(cands, key=lambda i: (len(i.split('.')), [int(n) for n in i.split('.')[1:]]))[0]
                    refs.append({'ref': ref, 'resolved': True, 'target': target, 'indirect': True})
                else:
                    refs.append({'ref': ref, 'resolved': False})
        x['xrefs'] = json.dumps(refs, ensure_ascii=False)
        figs = sorted(set(re.findall(r'Figure\s+(B-\d+)', text)))
        x['figures'] = json.dumps(figs, ensure_ascii=False)

    database_url = os.environ.get('DATABASE_URL', '').strip()
    if database_url:
        import psycopg
        from psycopg.rows import dict_row
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        con = psycopg.connect(database_url, row_factory=dict_row)
        cur = con.cursor()
        for statement in SCHEMA.split(';'):
            statement = statement.strip()
            if not statement or statement.upper().startswith('PRAGMA'):
                continue
            cur.execute(statement)
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TEXT NOT NULL
        )""")
        cur.execute('SELECT COUNT(*) AS n FROM rules')
        if cur.fetchone()['n'] == 0:
            rule_sql = '''INSERT INTO rules (id,part,article,number,title,kind,priority,page,article_title,part_title,body,plain,engineering,notes,components,xrefs,figures,table_data,status,sort_order)
                          VALUES (%(id)s,%(part)s,%(article)s,%(number)s,%(title)s,%(kind)s,%(priority)s,%(page)s,%(article_title)s,%(part_title)s,%(body)s,%(plain)s,%(engineering)s,%(notes)s,%(components)s,%(xrefs)s,%(figures)s,%(table_data)s,%(status)s,%(sort_order)s)'''
            cur.executemany(rule_sql, rows)
            cur.execute('SELECT COUNT(*) AS n FROM checks')
            if cur.fetchone()['n'] == 0:
                check_sql = '''INSERT INTO checks (id,rule_id,title,component,criterion,method,evidence_required,eval,min_val,max_val,unit,label,priority,status,measured,remarks,assignee,updated_at,sort_order)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                check_rows = [(c['id'], c['rule'], c['title'], c['component'], c['criterion'], c['method'], c['evidence'],
                               c['eval'], c['min'], c['max'], c['unit'], c['label'], c['priority'], 'Not Started', None, '', '', None, i)
                              for i, c in enumerate(CHECKS)]
                cur.executemany(check_sql, check_rows)
            cur.executemany('INSERT INTO meta (key,value) VALUES (%s,%s) ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value',
                            [(k, str(v)) for k, v in META.items()])
            con.commit()
            print('Seeded', len(rows), 'rules and', len(CHECKS), 'checks into PostgreSQL')
        else:
            print('PostgreSQL database already populated; skipping seed')
        con.close()
        return

    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM rules')
    if cur.fetchone()[0] == 0:
        cur.executemany('''INSERT INTO rules (id,part,article,number,title,kind,priority,page,article_title,part_title,body,plain,engineering,notes,components,xrefs,figures,table_data,status,sort_order)
                           VALUES (:id,:part,:article,:number,:title,:kind,:priority,:page,:article_title,:part_title,:body,:plain,:engineering,:notes,:components,:xrefs,:figures,:table_data,:status,:sort_order)''', rows)
        cur.execute('SELECT COUNT(*) FROM checks')
        if cur.fetchone()[0] == 0:
            for i, c in enumerate(CHECKS):
                cur.execute('''INSERT INTO checks (id,rule_id,title,component,criterion,method,evidence_required,eval,min_val,max_val,unit,label,priority,status,measured,remarks,assignee,updated_at,sort_order)
                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                            (c['id'], c['rule'], c['title'], c['component'], c['criterion'], c['method'], c['evidence'],
                             c['eval'], c['min'], c['max'], c['unit'], c['label'], c['priority'], 'Not Started', None, '', '', None, i))
        for k, v in META.items():
            cur.execute('INSERT OR REPLACE INTO meta (key,value) VALUES (?,?)', (k, v))
        con.commit()
        print('Seeded', len(rows), 'rules and', len(CHECKS), 'checks')
    else:
        print('Database already populated; skipping seed')
    con.close()

if __name__ == '__main__':
    main()
