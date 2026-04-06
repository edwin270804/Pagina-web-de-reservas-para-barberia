import sqlite3

DB_NAME = "barberia.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT NOT NULL UNIQUE
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS barberos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        barbero_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        hora TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'activa',

        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (barbero_id) REFERENCES barberos(id),

        UNIQUE (barbero_id, fecha, hora)
    )
    """)

    db.commit()
    db.close()


def insertar_barberos():
    db = get_db()

    barberos = [
        ("Erick",),
        ("Emerson",)
    ]

    db.executemany("INSERT INTO barberos (nombre) VALUES (?)", barberos)
    db.commit()
    db.close()