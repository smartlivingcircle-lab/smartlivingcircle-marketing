#!/usr/bin/env python3
"""
Payhip Order Monitor & PDF Auto-Delivery System
Monitors email for Payhip orders and automatically sends the PDF
"""

import os
import sys
import time
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

WORKDIR = "C:/Users/INSPIRON/smartlivingcircle-marketing"
sys.path.insert(0, WORKDIR)

# Email credentials
GMAIL_USER = "smartlivingcircle@gmail.com"
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')  # Need 2FA app password

# Payhip product info
PAYPAL_EMAIL = "smartlivingcircle@gmail.com"
PAYHIP_LINK = "https://payhip.com/b/1vtcL"
PRODUCT_NAME = "Blockchain Technologies: How to Make Money with Flash Loans"

# Path to the PDF (need to download/upload it first)
PDF_PATH = os.path.join(WORKDIR, "blockchain_technologies_flash_loans.pdf")

# ============================================================
# EMAIL FUNCTIONS
# ============================================================

def decode_str(s):
    """Decode email header string"""
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = []
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

def send_email_with_pdf(to_email, subject, body_text):
    """Send email with PDF attachment"""
    if not GMAIL_APP_PASSWORD:
        print("ERROR: GMAIL_APP_PASSWORD not set - cannot send emails")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Body
        msg.attach(MIMEText(body_text, 'plain'))
        
        # Attach PDF if it exists
        if os.path.exists(PDF_PATH):
            with open(PDF_PATH, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{PRODUCT_NAME}.pdf"')
                msg.attach(part)
            print(f"  Attached PDF to email")
        else:
            print(f"  WARNING: PDF not found at {PDF_PATH} - sending text only")
        
        # Send via SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        print(f"  Email sent to {to_email}")
        return True
        
    except Exception as e:
        print(f"  ERROR sending email: {e}")
        return False

def check_payhip_orders():
    """Check Gmail for Payhip order notifications"""
    if not GMAIL_APP_PASSWORD:
        print("GMAIL_APP_PASSWORD not set - cannot check emails")
        return []
    
    orders = []
    
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select("inbox")
        
        # Search for Payhip emails (last 7 days)
        since_date = (datetime.now() - timedelta(days=7)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'SINCE {since_date} FROM "payhip.com" OR SUBJECT "order" OR SUBJECT "thank you for your purchase"')
        
        if status != "OK":
            print("No messages found")
            return []
        
        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} potential order emails")
        
        for eid in email_ids:
            try:
                status, msg_data = mail.fetch(eid, "(RFC822)")
                if status != "OK":
                    continue
                    
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                subject = decode_str(msg.get('Subject', ''))
                sender = decode_str(msg.get('From', ''))
                date = msg.get('Date', '')
                
                print(f"  Email: {subject} from {sender}")
                
                # Check if this is a new Payhip order (not yet processed)
                # Look for order confirmation patterns
                order_keywords = ['payhip', 'order', 'purchase', 'thank you', 'download', 'access']
                if any(kw in subject.lower() for kw in order_keywords):
                    # Extract buyer email if possible
                    # Send the PDF
                    print(f"  Processing order from {sender}")
                    
                    # Extract email from sender if possible
                    import re
                    email_match = re.search(r'<(.+@.+)>', sender)
                    buyer_email = email_match.group(1) if email_match else sender
                    
                    orders.append({
                        'subject': subject,
                        'sender': sender,
                        'buyer_email': buyer_email,
                        'date': date
                    })
                    
            except Exception as e:
                print(f"  Error processing email: {e}")
                continue
        
        mail.logout()
        
    except Exception as e:
        print(f"Error checking emails: {e}")
    
    return orders

def process_payhip_orders():
    """Main function: check orders and auto-deliver PDFs"""
    print("=" * 50)
    print("PAYPHP AUTO-DELIVERY SYSTEM")
    print("=" * 50)
    print(f"Product: {PRODUCT_NAME}")
    print(f"Payhip link: {PAYHIP_LINK}")
    print(f"PDF path: {PDF_PATH}")
    print(f"PDF exists: {os.path.exists(PDF_PATH)}")
    print()
    
    if not GMAIL_APP_PASSWORD:
        print("MISSING: GMAIL_APP_PASSWORD")
        print("To set up:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2FA")
        print("3. App passwords -> Generate new app password")
        print("4. Set: export GMAIL_APP_PASSWORD='your_app_password_here'")
        print()
        return
    
    # Check for orders
    orders = check_payhip_orders()
    
    if not orders:
        print("No new Payhip orders found")
        return
    
    print(f"\nFound {len(orders)} orders - sending PDFs...")
    
    # Email template
    email_body = f"""Hi!

Thank you for purchasing {PRODUCT_NAME}!

Your PDF is attached to this email.

Inside you'll find:
- 118 pages of DeFi & flash loan strategies
- Real code examples and mechanics
- Risk management frameworks
- Finding arbitrage opportunities

Remember: This is not financial advice. Always do your own research.

If you have any questions, reply to this email.

Best,
SmartLivingCircle

Get the latest updates: https://twitter.com/smartlivingcircle

---
You purchased via Payhip: {PAYHIP_LINK}
"""
    
    for order in orders:
        print(f"\nSending PDF to: {order['buyer_email']}")
        success = send_email_with_pdf(
            order['buyer_email'],
            f"Your {PRODUCT_NAME} - Download",
            email_body
        )
        if success:
            print(f"  DELIVERED!")
        else:
            print(f"  FAILED - check logs above")
    
    print(f"\nDone! Processed {len(orders)} orders")

def send_test_email():
    """Send a test email to verify Gmail setup"""
    if not GMAIL_APP_PASSWORD:
        print("GMAIL_APP_PASSWORD not set")
        return
    
    test_body = """This is a test email from the SmartLivingCircle marketing system.

If you receive this, the email system is working!

Best,
SmartLivingCircle Bot
"""
    
    success = send_email_with_pdf(
        GMAIL_USER,  # Send to ourselves
        "TEST: SmartLivingCircle Marketing System",
        test_body
    )
    
    if success:
        print("Test email sent successfully!")
    else:
        print("Test email failed - check GMAIL_APP_PASSWORD")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        send_test_email()
    else:
        process_payhip_orders()