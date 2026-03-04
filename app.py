from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import requests

# 1. SETUP THE APP & DATABASE
app = Flask(__name__)
app.secret_key = "super_secret_qa_key" # Required for managing login sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # Creates a local app.db file
db = SQLAlchemy(app)

# 2. DEFINE THE DATABASE TABLE (Transaction History)
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_usd = db.Column(db.Float, nullable=False)
    target_currency = db.Column(db.String(3), nullable=False)
    converted_amount = db.Column(db.Float, nullable=False)

# Create the database file if it doesn't exist
with app.app_context():
    db.create_all()

# 3. ROUTES (The URLs of our website)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Hardcoded user for testing purposes
    valid_user = "qa_user"
    valid_pass = "password123"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == valid_user and password == valid_pass:
            session['logged_in'] = True # Create a login session
            return redirect('/dashboard')
        else:
            return render_template('login.html', error="Invalid Credentials")
            
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect('/') # Kick them out if not logged in

    message = None
    if request.method == 'POST':
        amount_usd = float(request.form['amount'])
        target_currency = request.form['currency']

        # 4. EXTERNAL API CALL
        # We use a free, open API to get live exchange rates
        api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(api_url).json()
        
        # Calculate the conversion
        exchange_rate = response['rates'][target_currency]
        converted_amount = round(amount_usd * exchange_rate, 2)

        # 5. SAVE TO DATABASE
        new_tx = Transaction(amount_usd=amount_usd, target_currency=target_currency, converted_amount=converted_amount)
        db.session.add(new_tx)
        db.session.commit()

        message = f"Successfully transferred {converted_amount} {target_currency}!"

    return render_template('dashboard.html', message=message)

@app.route('/history')
def history():
    if not session.get('logged_in'):
        return redirect('/')
    
    # Fetch all records from the database and send them to the HTML table
    all_transactions = Transaction.query.all()
    return render_template('history.html', transactions=all_transactions)

@app.route('/logout')
def logout():
    session.pop('logged_in', None) # Destroy the login session
    return redirect('/')

# 6. RUN THE SERVER
if __name__ == '__main__':
    app.run(debug=True, threaded=True)