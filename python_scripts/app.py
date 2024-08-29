from flask import Flask, request, render_template

app = Flask(__name__)

def calculate_tax(income):
    """
    Calculate the tax owed based on income and predefined tax brackets.
    """
    if income <= 10000:
        return 0
    elif income <= 50000:
        return (income - 10000) * 0.10
    else:
        return (income - 50000) * 0.20 + (50000 - 10000) * 0.10

@app.route('/', methods=['GET', 'POST'])
def index():
    tax_owed = None
    if request.method == 'POST':
        try:
            income = float(request.form['income'])
            tax_owed = calculate_tax(income)
        except ValueError:
            tax_owed = "Invalid input. Please enter a valid number for income."
    
    return render_template('index.html', tax_owed=tax_owed)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0")
