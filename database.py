# database.py
import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'korgool.db'

def get_db_connection():
    # timeout=15 prevents "database is locked" errors
    # WAL mode allows reading and writing at the exact same time
    conn = sqlite3.connect(DB_NAME, timeout=15)
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
            message TEXT NOT NULL, severity TEXT NOT NULL, category TEXT,
            status TEXT DEFAULT 'new', callback_requested INTEGER DEFAULT 0,
            codeword TEXT DEFAULT NULL, registry_match INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT, codeword TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL, address TEXT, disability TEXT, safe_contact TEXT,
            registered_by TEXT, registered_at TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS callback_vault (
            case_id INTEGER PRIMARY KEY, phone_number TEXT NOT NULL,
            expires_at TEXT NOT NULL, FOREIGN KEY (case_id) REFERENCES cases(id))''')
    conn.commit()
    conn.close()

def insert_case(timestamp, message, severity, category, callback_requested=0, codeword=None, registry_match=0):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO cases (timestamp, message, severity, category, callback_requested, codeword, registry_match) VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (timestamp, message, severity, category, callback_requested, codeword, registry_match))
    conn.commit()
    case_id = c.lastrowid
    conn.close()
    return case_id

def get_all_cases():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT id, timestamp, message, severity, category, status, callback_requested, codeword, registry_match FROM cases ORDER BY id DESC''')
    rows = c.fetchall()
    conn.close()
    return rows

def get_active_case_by_codeword(codeword):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT id FROM cases WHERE codeword = ? AND status != 'resolved' ORDER BY id DESC LIMIT 1''', (codeword,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def update_case_repeat(case_id, timestamp):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''UPDATE cases SET timestamp = ?, message = REPLACE(message, ' (ПОВТОР)', '') || ' (ПОВТОР)' WHERE id = ?''', (timestamp, case_id))
    conn.commit()
    conn.close()

def resolve_case(case_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE cases SET status = "resolved" WHERE id = ?', (case_id,))
    c.execute('DELETE FROM callback_vault WHERE case_id = ?', (case_id,))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT severity, COUNT(*) FROM cases WHERE status != 'resolved' GROUP BY severity''')
    rows = c.fetchall()
    conn.close()
    stats = {'urgent': 0, 'high': 0, 'medium': 0, 'low': 0}
    for severity, count in rows:
        if severity in stats: stats[severity] = count
    return stats

def register_woman(codeword, name, address, disability, safe_contact, registered_by):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO registry (codeword, name, address, disability, safe_contact, registered_by, registered_at) VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (codeword, name, address, disability, safe_contact, registered_by, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def lookup_codeword(codeword):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT name, address, disability, safe_contact, registered_by FROM registry WHERE codeword = ?''', (codeword,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_registered():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''SELECT id, codeword, name, address, disability, safe_contact, registered_by, registered_at FROM registry ORDER BY id DESC''')
    rows = c.fetchall()
    conn.close()
    return [{'id': r[0], 'codeword': r[1], 'name': r[2], 'address': r[3], 'disability': r[4], 'safe_contact': r[5], 'registered_by': r[6], 'registered_at': r[7]} for r in rows]

def seed_demo_registry():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO registry (codeword, name, address, disability, safe_contact, registered_by, registered_at) VALUES (?, ?, ?, ?, ?, ?, ?)''',
        ('КЕРЕК', 'Айзада, 34 года', 'ул. Токтогула, 125, кв. 12', 'Моторная инвалидность', '+996 555 123 456 (сестра)', 'Nazik Kyz', '2026-01-15'))
    conn.commit()
    conn.close()

def store_callback_number(case_id, phone_number, minutes=30):
    expires = (datetime.now() + timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO callback_vault (case_id, phone_number, expires_at) VALUES (?, ?, ?)', (case_id, phone_number, expires))
    conn.commit()
    conn.close()

def get_callback_number(case_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT phone_number, expires_at FROM callback_vault WHERE case_id = ?', (case_id,))
    row = c.fetchone()
    if not row:
        conn.close()
        return None
    phone, expires = row
    if datetime.now() > datetime.strptime(expires, '%Y-%m-%d %H:%M:%S'):
        c.execute('DELETE FROM callback_vault WHERE case_id = ?', (case_id,))
        conn.commit()
        conn.close()
        return None
    conn.close()
    return phone

def purge_expired_callbacks():
    conn = get_db_connection()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('DELETE FROM callback_vault WHERE expires_at < ?', (now,))
    deleted = c.rowcount
    conn.commit()
    conn.close()
    return deleted

init_db()
seed_demo_registry()
purge_expired_callbacks()