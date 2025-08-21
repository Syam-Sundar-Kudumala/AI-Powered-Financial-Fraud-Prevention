import os
import secrets
import logging
import csv
import io
import random
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, Response


# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import utilities
from utils.twilio_helper import send_otp, verify_otp, DEFAULT_RECIPIENT
from utils.session_manager import init_session, add_transaction, get_transactions
from models.fraud_detection import predict_fraud

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-dev")

# Routes
@app.route('/')
def index():
    # Initialize session if it doesn't exist
    init_session()
    return render_template('index.html')

@app.route('/online_shopping', methods=['GET', 'POST'])
def online_shopping():
    init_session()
    
    if request.method == 'POST':
        # Get form data
        amount = float(request.form.get('amount', 0))
        merchant = request.form.get('merchant', '')
        card_number = request.form.get('card_number', '')
        expiry = request.form.get('expiry', '')
        cvv = request.form.get('cvv', '')
        phone = request.form.get('phone', '')
        location = request.form.get('location', '')
        
        # Validate form data (basic validation)
        if not amount or not merchant or not card_number or not expiry or not cvv or not phone:
            flash('Please fill in all required fields', 'danger')
            return render_template('online_shopping.html')
        
        # Check if amount is greater than threshold
        if amount > 10000:
            # Generate OTP and store in session
            session['pending_transaction'] = {
                'type': 'Online Shopping',
                'amount': amount,
                'merchant': merchant,
                'card_number': card_number[-4:],  # Store only last 4 digits
                'location': location,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'phone': phone
            }
            
            # Send OTP
            otp = send_otp(phone)
            if otp:
                session['otp'] = otp
                return redirect(url_for('otp_verification'))
            else:
                flash('Failed to send OTP. Please try again.', 'danger')
                return render_template('online_shopping.html')
        
        # Process transaction directly if amount is below threshold
        transaction = {
            'type': 'Online Shopping',
            'amount': amount,
            'merchant': merchant,
            'card_number': card_number[-4:],  # Store only last 4 digits
            'location': location,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check for fraud
        is_fraud = predict_fraud(transaction)
        transaction['fraud'] = is_fraud
        
        # Add transaction to session
        add_transaction(transaction)
        
        # Show success message
        status = 'warning' if is_fraud else 'success'
        message = 'Transaction completed but flagged as suspicious' if is_fraud else 'Transaction completed successfully'
        flash(message, status)
        
        return redirect(url_for('dashboard'))
    
    return render_template('online_shopping.html')

@app.route('/fund_transfer', methods=['GET', 'POST'])
def fund_transfer():
    init_session()
    
    if request.method == 'POST':
        # Get form data
        amount = float(request.form.get('amount', 0))
        sender_account = request.form.get('sender_account', '')
        recipient_account = request.form.get('recipient_account', '')
        bank_name = request.form.get('bank_name', '')
        description = request.form.get('description', '')
        phone = request.form.get('phone', '')
        location = request.form.get('location', '')
        
        # Validate form data
        if not amount or not sender_account or not recipient_account or not bank_name or not phone:
            flash('Please fill in all required fields', 'danger')
            return render_template('fund_transfer.html')
        
        # Check if amount is greater than threshold
        if amount > 10000:
            # Generate OTP and store in session
            session['pending_transaction'] = {
                'type': 'Fund Transfer',
                'amount': amount,
                'sender_account': sender_account[-4:],  # Store only last 4 digits
                'recipient_account': recipient_account[-4:],  # Store only last 4 digits
                'bank_name': bank_name,
                'description': description,
                'location': location,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'phone': phone
            }
            
            # Send OTP
            otp = send_otp(phone)
            if otp:
                session['otp'] = otp
                return redirect(url_for('otp_verification'))
            else:
                flash('Failed to send OTP. Please try again.', 'danger')
                return render_template('fund_transfer.html')
        
        # Process transaction directly if amount is below threshold
        transaction = {
            'type': 'Fund Transfer',
            'amount': amount,
            'sender_account': sender_account[-4:],  # Store only last 4 digits
            'recipient_account': recipient_account[-4:],  # Store only last 4 digits
            'bank_name': bank_name,
            'description': description,
            'location': location,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check for fraud
        is_fraud = predict_fraud(transaction)
        transaction['fraud'] = is_fraud
        
        # Add transaction to session
        add_transaction(transaction)
        
        # Show success message
        status = 'warning' if is_fraud else 'success'
        message = 'Transaction completed but flagged as suspicious' if is_fraud else 'Transaction completed successfully'
        flash(message, status)
        
        return redirect(url_for('dashboard'))
    
    return render_template('fund_transfer.html')

@app.route('/atm_withdrawal', methods=['GET', 'POST'])
def atm_withdrawal():
    init_session()
    
    if request.method == 'POST':
        # Get form data
        amount = float(request.form.get('amount', 0))
        card_number = request.form.get('card_number', '')
        pin = request.form.get('pin', '')
        atm_location = request.form.get('atm_location', '')
        phone = request.form.get('phone', '')
        
        # Validate form data
        if not amount or not card_number or not pin or not atm_location or not phone:
            flash('Please fill in all required fields', 'danger')
            return render_template('atm_withdrawal.html')
        
        # Check if amount is greater than threshold
        if amount > 10000:
            # Generate OTP and store in session
            session['pending_transaction'] = {
                'type': 'ATM Withdrawal',
                'amount': amount,
                'card_number': card_number[-4:],  # Store only last 4 digits
                'location': atm_location,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'phone': phone
            }
            
            # Send OTP
            otp = send_otp(phone)
            if otp:
                session['otp'] = otp
                return redirect(url_for('otp_verification'))
            else:
                flash('Failed to send OTP. Please try again.', 'danger')
                return render_template('atm_withdrawal.html')
        
        # Process transaction directly if amount is below threshold
        transaction = {
            'type': 'ATM Withdrawal',
            'amount': amount,
            'card_number': card_number[-4:],  # Store only last 4 digits
            'location': atm_location,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check for fraud
        is_fraud = predict_fraud(transaction)
        transaction['fraud'] = is_fraud
        
        # Add transaction to session
        add_transaction(transaction)
        
        # Show success message
        status = 'warning' if is_fraud else 'success'
        message = 'Transaction completed but flagged as suspicious' if is_fraud else 'Transaction completed successfully'
        flash(message, status)
        
        return redirect(url_for('dashboard'))
    
    return render_template('atm_withdrawal.html')

@app.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    if 'pending_transaction' not in session or 'otp' not in session:
        flash('No pending transaction requiring OTP verification', 'warning')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        otp_input = request.form.get('otp', '')
        
        # Verify OTP
        if verify_otp(otp_input, session['otp']):
            # Get pending transaction
            transaction = session['pending_transaction']
            
            # Remove sensitive fields
            if 'phone' in transaction:
                del transaction['phone']
            
            # Check for fraud
            is_fraud = predict_fraud(transaction)
            transaction['fraud'] = is_fraud
            
            # Add transaction to session
            add_transaction(transaction)
            
            # Clear pending transaction and OTP
            del session['pending_transaction']
            del session['otp']
            
            # Show success message
            status = 'warning' if is_fraud else 'success'
            message = 'Transaction completed but flagged as suspicious' if is_fraud else 'Transaction completed successfully'
            flash(message, status)
            
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')
    
    return render_template('otp_verification.html')

@app.route('/dashboard')
def dashboard():
    init_session()
    transactions = get_transactions()
    return render_template('dashboard.html', transactions=transactions)

@app.route('/metrics')
def metrics():
    init_session()
    transactions = get_transactions()
    
    # Calculate metrics
    total_transactions = len(transactions)
    fraud_transactions = sum(1 for t in transactions if t.get('fraud', False))
    fraud_percentage = (fraud_transactions / total_transactions * 100) if total_transactions > 0 else 0
    
    # Group by transaction type
    types = {}
    for t in transactions:
        t_type = t.get('type', 'Unknown')
        if t_type not in types:
            types[t_type] = {'total': 0, 'fraud': 0}
        types[t_type]['total'] += 1
        if t.get('fraud', False):
            types[t_type]['fraud'] += 1
    
    # Calculate amount statistics
    amounts = [t.get('amount', 0) for t in transactions]
    avg_amount = sum(amounts) / len(amounts) if amounts else 0
    max_amount = max(amounts) if amounts else 0
    
    metrics = {
        'total_transactions': total_transactions,
        'fraud_transactions': fraud_transactions,
        'fraud_percentage': fraud_percentage,
        'types': types,
        'avg_amount': avg_amount,
        'max_amount': max_amount
    }
    
    return render_template('metrics.html', metrics=metrics, transactions=transactions)

@app.route('/export-csv')
def export_csv():
    init_session()
    transactions = get_transactions()
    
    # Create CSV data
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    header = ['Type', 'Amount', 'Timestamp', 'Location', 'Fraud Flag']
    writer.writerow(header)
    
    # Write transactions
    for t in transactions:
        row = [
            t.get('type', ''),
            t.get('amount', 0),
            t.get('timestamp', ''),
            t.get('location', ''),
            'Yes' if t.get('fraud', False) else 'No'
        ]
        writer.writerow(row)
    
    # Create response
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=transactions.csv'}
    )
    
    return response

@app.route('/reset-session')
def reset_session():
    session.clear()
    init_session()
    flash('Session has been reset', 'success')
    return redirect(url_for('index'))

from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
