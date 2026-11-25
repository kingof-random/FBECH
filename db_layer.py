# PostgreSQL adapter for F-BECH. SQLite remains available for local development.
import os
import re
import sqlite3

class Row(dict):
    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)

class Cursor:
    def __init__(self, cur, lastrowid=None):
        self.cur = cur
        self.lastrowid = lastrowid
    def _row(self, row):
        return Row(row) if row is not None and isinstance(row, dict) else row
    def fetchone(self):
        return self._row(self.cur.fetchone())
    def fetchall(self):
        return [self._row(r) for r in self.cur.fetchall()]
    def __iter__(self):
        for r in self.cur:
            yield self._row(r)

class PGConnection:
    def __init__(self, con):
        self.con = con
    def execute(self, sql, params=()):
        q = sql.strip()
        if q.upper().startswith("INSERT OR REPLACE INTO META"):
            q = "INSERT INTO meta (key,value) VALUES (%s,%s) ON CONFLICT (key) DO UPDATE SET value=EXCLUDED.value"
            params = tuple(params)
        else:
            q = q.replace("?", "%s")
        wants_id = bool(re.match(r"(?is)^INSERT\\s+INTO\\s+(evidence|docs|issues|revisions)\\b", q))
        if wants_id and "RETURNING" not in q.upper():
            q += " RETURNING id"
        cur = self.con.cursor()
        cur.execute(q, params)
        lastrowid = None
        if wants_id:
            row = cur.fetchone()
            if row:
                lastrowid = row["id"] if isinstance(row, dict) else row[0]
        return Cursor(cur, lastrowid)
    def commit(self): self.con.commit()
    def close(self): self.con.close()

def connect():
    url = os.environ.get("DATABASE_URL", "").strip()
    if not url:
        return None
    import psycopg
    from psycopg.rows import dict_row
    # Supabase may supply postgres://; psycopg accepts postgresql://.
    url = url.replace("postgres://", "postgresql://", 1)
    return PGConnection(psycopg.connect(url, row_factory=dict_row))
