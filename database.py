import sqlite3

def init_db():
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        regno TEXT,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        level TEXT,
        accuracy REAL,
        speed REAL, 
        time_taken REAL,
        grade TEXT
    )
    """)

    # Grade Column இல்லை என்றால் தானாகச் சேர்க்கும்
    try:
        cursor.execute("ALTER TABLE results ADD COLUMN grade TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

# Database Init
init_db()

def save_result(name, level, accuracy, speed, time_taken, grade):
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO results (name, level, accuracy, speed, time_taken, grade)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, level, accuracy, speed, time_taken, grade))

    conn.commit()
    conn.close()

def save_student(name, regno, password):
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (name, regno, password)
    VALUES (?, ?, ?)
    """, (name, regno, password))

    conn.commit()
    conn.close()

def verify_student(name, password):
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name FROM students
    WHERE name = ? AND password = ?
    """, (name, password))

    student = cursor.fetchone()
    conn.close()

    return student is not None

def get_results(name):
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, level, accuracy, speed, time_taken, grade
    FROM results
    WHERE name = ?
    """, (name,))

    results = cursor.fetchall()
    conn.close()
    return results

def update_password(name, new_password):
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students SET password = ?
    WHERE name = ?
    """, (new_password, name))

    conn.commit()
    conn.close()

    return cursor.rowcount > 0
def login_or_register(name, code):
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM students WHERE name = ?", (name,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            "INSERT INTO students (name, regno, password) VALUES (?, ?, ?)",
            (name, "", code),
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return row[0] == code
