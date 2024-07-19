import sqlite3

def add_embedding_column():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Add the embedding column if it doesn't exist
    cursor.execute("ALTER TABLE uploads ADD COLUMN embedding TEXT")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_embedding_column()