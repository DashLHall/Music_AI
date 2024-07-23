from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
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
    processed_data = process_question(question)

    # Serialize the processed_data list to a JSON string
    processed_data_str = json.dumps(processed_data)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO uploads (question, processedData) VALUES (?, ?)", (question, processed_data_str))
    conn.commit()
    upload_id = cursor.lastrowid
    conn.close()

    print(f"Processed Data: {processed_data}")  # Debugging: Print processed data
    return jsonify({'id': upload_id, 'question': question, 'processedData': processed_data}), 201

@app.route('/uploads', methods=['GET'])
def get_uploads():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM uploads')
    uploads = cursor.fetchall()
    conn.close()

    # Deserialize the processedData JSON string back to a list
    uploads = [{'id': row[0], 'question': row[1], 'processedData': json.loads(row[2])} for row in uploads]
    return jsonify(uploads)

@app.route('/clear', methods=['POST'])
def clear_uploads():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM uploads')
    conn.commit()
    conn.close()
    return jsonify({'status': 'database cleared'}), 200

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)

