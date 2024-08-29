from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        income = float(request.form['income'])
        tax_rate = 0.15  # 15% tax rate for simplicity
        tax = income * tax_rate
        return render_template('result.html', income=income, tax=tax)
    except ValueError:
        return "Please enter a valid number for income."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)