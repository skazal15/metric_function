import sqlite3

def save_to_db(func_name, metrics):
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        function_name TEXT PRIMARY KEY,
        calls INTEGER,
        average_time REAL,
        errors INTEGER
    )
    ''')

    cursor.execute('''
    INSERT INTO metrics (function_name, calls, average_time, errors)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(function_name) 
    DO UPDATE SET calls=?, average_time=?, errors=?
    ''', (func_name, metrics['Number of calls'], metrics['Average execution time'], metrics['Number of errors'],
          metrics['Number of calls'], metrics['Average execution time'], metrics['Number of errors']))

    conn.commit()
    conn.close()
