import sqlite3
from datetime import datetime

def get_connection():
    conn = sqlite3.connect('crm_database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT UNIQUE,
            email TEXT,
            address TEXT,
            registration_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            order_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Новый',
            total_amount REAL DEFAULT 0.0,
            description TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            interaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
            interaction_type TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()