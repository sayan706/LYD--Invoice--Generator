from flask import Flask, render_template, request
from datetime import datetime
import random

import os

base_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, 
            static_folder=os.path.join(base_dir, 'static'),
            template_folder=os.path.join(base_dir, 'templates'))
@app.route('/', methods=['GET'])
def index():
    return render_template('invoice-form.html')

@app.route('/generate', methods=['POST'])
def generate_invoice():
    # Retrieve form data
    client_name = request.form.get('clientName', 'Client Name')
    pickup_date = request.form.get('pickupDate', '')
    client_email = request.form.get('clientEmail', '')
    client_phone = request.form.get('clientPhone', '')
    
    item_desc = request.form.get('itemDesc', '')
    per_head = request.form.get('perHead', '0')
    pax = request.form.get('pax', '0')
    item_total = request.form.get('itemTotal', '0')
    
    amount_words = request.form.get('amountWords', '')
    advance_amount = request.form.get('advanceAmount', '0')
    
    tour_plan = request.form.get('tourPlan', '')
    cancellation_policy = request.form.get('cancellationPolicy', '')
    tour_including = request.form.get('tourIncluding', '')
    tour_excluding = request.form.get('tourExcluding', '')
    tour_note = request.form.get('tourNote', '')
    
    # Calculate values that might have been processed by JS
    try:
        total_amount = int(item_total)
    except:
        total_amount = 0
        
    try:
        advance = int(advance_amount)
    except:
        advance = 0
        
    total_due = total_amount - advance
    
    # Format numbers to Indian Rupee strings
    def format_inr(number):
        return f"₹ {number:,}"
        
    total_amount_str = format_inr(total_amount)
    advance_str = format_inr(advance)
    total_due_str = format_inr(total_due)
    per_head_str = format_inr(int(per_head)) if per_head.isdigit() else f"₹ {per_head}"
    
    # Parse lines for lists
    tour_plan_lines = [line.strip() for line in tour_plan.split('\n') if line.strip()]
    cancellation_lines = [line.strip() for line in cancellation_policy.split('\n') if line.strip()]
    including_lines = [line.strip() for line in tour_including.split('\n') if line.strip()]
    excluding_lines = [line.strip() for line in tour_excluding.split('\n') if line.strip()]
    
    # Generate Invoice Number & Date
    invoice_no = request.form.get('invoiceNo', f"INV-{random.randint(1000, 9999)}")
    now = datetime.now()
    invoice_date = now.strftime("%d/%m/%Y")
    invoice_time = now.strftime("%H:%M:%S")
    
    return render_template('index.html', 
        client_name=client_name,
        pickup_date=pickup_date,
        client_email=client_email,
        client_phone=client_phone,
        item_desc=item_desc,
        per_head=per_head_str,
        pax=pax,
        total_amount=total_amount_str,
        amount_words=amount_words,
        advance=advance_str,
        total_due=total_due_str,
        tour_plan_lines=tour_plan_lines,
        cancellation_lines=cancellation_lines,
        including_lines=including_lines,
        excluding_lines=excluding_lines,
        tour_note=tour_note,
        invoice_no=invoice_no,
        invoice_date=invoice_date,
        invoice_time=invoice_time
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
