from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from processed_data import process_question

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            processedData TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    question = data.get('question')
    processed_data = process_question(question)  # Use the processing module

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO uploads (question, processedData) VALUES (?, ?)", (question, processed_data))
    conn.commit()
    upload_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': upload_id, 'question': question, 'processedData': processed_data}), 201

@app.route('/uploads', methods=['GET'])
def get_uploads():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM uploads')
    uploads = cursor.fetchall()
    conn.close()
    return jsonify([{'id': row[0], 'question': row[1], 'processedData': row[2]} for row in uploads])

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)