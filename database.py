import sqlite3

def connect():
    conn = sqlite3.connect("patients.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_db():
    conn = connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            dob TEXT,
            email TEXT,
            glucose REAL,
            haemoglobin REAL,
            cholesterol REAL,
            remarks TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_all():
    conn = connect()
    data = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return data

def get_one(id):
    conn = connect()
    row = conn.execute("SELECT * FROM patients WHERE id = ?", (id,)).fetchone()
    conn.close()
    return row

def add_patient(name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = connect()
    existing = conn.execute("SELECT id FROM patients WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return False
    conn.execute("""
        INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks))
    conn.commit()
    conn.close()
    return True

def update_patient(id, name, dob, email, glucose, haemoglobin, cholesterol, remarks):
    conn = connect()
    conn.execute("""
        UPDATE patients
        SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=?
        WHERE id=?
    """, (name, dob, email, glucose, haemoglobin, cholesterol, remarks, id))
    conn.commit()
    conn.close()

def delete_patient(id):
    conn = connect()
    conn.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    conn.close()
