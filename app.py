from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})  # Restrict to specific frontend origin

# Database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', '172.27.107.31'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'Sanskruti@123'),
    'database': os.getenv('DB_NAME', 'student_db')
}

def setup_database():
    """Sets up the database and student table if they don't exist."""
    try:
        conn = mysql.connector.connect(host=db_config['host'], user=db_config['user'], password=db_config['password'])
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        cursor.close()
        conn.close()

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            grade VARCHAR(50) NOT NULL,
            interests TEXT NOT NULL,
            about TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

@app.route('/add_student', methods=['POST'])
def add_student():
    """API to add a new student to the database."""
    try:
        data = request.json
        required_fields = ['name', 'email', 'age', 'grade', 'interests', 'about']

        if any(not data.get(field) for field in required_fields):
            return jsonify({'success': False, 'message': 'All fields are required!'}), 400

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO students (name, email, age, grade, interests, about)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (data['name'], data['email'], data['age'], data['grade'], data['interests'], data['about']))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Student added successfully!'}), 201
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'message': f'Database Error: {err}'}), 500

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
