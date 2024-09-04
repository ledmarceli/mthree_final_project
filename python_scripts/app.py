from flask import Flask, render_template, request, jsonify
from markupsafe import escape
import sqlite3

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gross_income REAL NOT NULL,
            expenses REAL NOT NULL,
            net_income REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        first_name = escape(request.form["first_name"])
        last_name = escape(request.form["last_name"])
        gross_income = float(request.form['income'])
        expenses = float(request.form['expenses'])
        net_income = gross_income - expenses

        # Tax calculation logic
        if net_income <= 12750:
            tax = 0
        elif net_income <= 50270:
            tax = (net_income - 12750) * 0.2
        elif net_income <= 125140:
            tax = (50270 - 12750) * 0.2 + (net_income - 50270) * 0.4
        else:
            tax = (50270 - 12750) * 0.2 + (125140 - 50270) * 0.4 + (net_income - 125140) * 0.45

        # Save the data to the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, gross_income, expenses, net_income)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, gross_income, expenses, net_income))
        conn.commit()
        conn.close()

        return render_template('result.html', income=gross_income, expenses=expenses, tax=tax, first_name=first_name, last_name=last_name)
    except ValueError:
        return "Please enter a valid number for income."
    

@app.route('/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()

    # Convert the rows to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "gross_income": row[3],
            "expenses": row[4],
            "net_income": row[5]
        })

    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
