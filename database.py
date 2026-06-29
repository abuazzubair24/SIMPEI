import sqlite3

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

conn.commit()


def simpan_anggota(chat_id, nama, username, tanggal):
    cursor.execute("""
    INSERT OR IGNORE INTO anggota
    (chat_id, nama, username, tanggal)
    VALUES (?, ?, ?, ?)
    """, (
        chat_id,
        nama,
        username,
        tanggal
    ))
    conn.commit()


def get_semua_anggota():
    cursor.execute("""
    SELECT * FROM anggota
    """)
    return cursor.fetchall()