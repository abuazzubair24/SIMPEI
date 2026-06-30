import sqlite3
from datetime import datetime

# Membuat / membuka database
conn = sqlite3.connect("simpei.db", check_same_thread=False)
cursor = conn.cursor()

# Tabel anggota
cursor.execute("""
CREATE TABLE IF NOT EXISTS anggota (
    chat_id INTEGER PRIMARY KEY,
    nama TEXT,
    username TEXT,
    tanggal TEXT
)
""")

# Tabel pembayaran (BARU)
cursor.execute("""
CREATE TABLE IF NOT EXISTS pembayaran (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    nama TEXT,
    username TEXT,
    photo_file_id TEXT,
    tanggal TEXT,
    status TEXT DEFAULT 'pending',
    verified_at TEXT
)
""")

conn.commit()


# ===== ANGGOTA =====

def simpan_anggota(chat_id, nama, username, tanggal):
    cursor.execute("""
    INSERT OR IGNORE INTO anggota
    (chat_id, nama, username, tanggal)
    VALUES (?, ?, ?, ?)
    """, (chat_id, nama, username, tanggal))
    conn.commit()


def get_semua_anggota():
    cursor.execute("SELECT * FROM anggota")
    return cursor.fetchall()


# ===== PEMBAYARAN (BARU) =====

def simpan_pembayaran(chat_id, nama, username, photo_file_id):
    """Simpan bukti transfer ke DB dengan status pending"""
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO pembayaran
    (chat_id, nama, username, photo_file_id, tanggal, status)
    VALUES (?, ?, ?, ?, ?, 'pending')
    """, (chat_id, nama, username, photo_file_id, tanggal))
    conn.commit()
    return cursor.lastrowid


def get_pending_pembayaran():
    """Ambil semua pembayaran yang belum di-verify"""
    cursor.execute("""
    SELECT id, chat_id, nama, username, photo_file_id, tanggal 
    FROM pembayaran 
    WHERE status = 'pending'
    """)
    return cursor.fetchall()


def approve_pembayaran(pembayaran_id):
    """Admin approve pembayaran"""
    verified_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    UPDATE pembayaran 
    SET status = 'approved', verified_at = ?
    WHERE id = ?
    """, (verified_at, pembayaran_id))
    conn.commit()


def reject_pembayaran(pembayaran_id):
    """Admin reject pembayaran"""
    cursor.execute("""
    UPDATE pembayaran 
    SET status = 'rejected'
    WHERE id = ?
    """, (pembayaran_id,))
    conn.commit()


def get_pembayaran_by_id(pembayaran_id):
    """Ambil detail pembayaran berdasarkan ID"""
    cursor.execute("""
    SELECT * FROM pembayaran WHERE id = ?
    """, (pembayaran_id,))
    return cursor.fetchone()