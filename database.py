import sqlite3

conn = sqlite3.connect("reading_assessment.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        regno  TEXT,
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
        time_taken REAL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")

def save_result(name, level, accuracy, speed, time_taken):

    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO results (name, level, accuracy, speed, time_taken)
    VALUES (?, ?, ?, ?, ? )
    """,(name, level, accuracy, speed, time_taken))

    print("Insert Query Executed")

    conn.commit()

    print("Database Commit Successfully")

    conn.close()

def save_student(name, regno, password):
    
    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (name, regno, password)
    VALUES (?, ?, ? )
    """,(name, regno, password))

    conn.commit()
    conn.close()

def get_results(name):

    conn = sqlite3.connect("reading_assessment.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, level, accuracy, speed, time_taken
    FROM results
    WHERE name = ?
    """, (name,))

    results = cursor.fetchall()

    print(results)
    print("Total rows:", len(results))

    conn.close()

    return results
