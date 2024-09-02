from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

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
        net_income = gross_income-expenses
        if net_income <= 12750:
            tax = 0
        elif net_income <= 50270:
            tax = (net_income-12750)*0.2
        elif net_income <= 125140:
            tax = (50270-12750)*0.2+(net_income-50270)*0.4
        else:
            tax = (50270-12750)*0.2+(125140-50270)*0.4+(net_income-125140)*0.45
        
        return render_template('result.html', income=gross_income, expenses=expenses, tax=tax, first_name=first_name, last_name=last_name)
    except ValueError:
        return "Please enter a valid number for income."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

