import psycopg2

DB_CONFIG = {
    "dbname": "smart_library",
    "user": "Mahima",
    "password": "",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        available BOOLEAN DEFAULT TRUE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        book_id INTEGER REFERENCES books(id),
        user_id INTEGER REFERENCES users(id),
        issue_date TIMESTAMP,
        return_date TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
