import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

def send_application_email(to_email, subject, body, cv_path, cover_letter_path):
    """
    Send job application email with CV and cover letter attachments via Gmail
    """
    # Gmail credentials from .env
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not gmail_user or not gmail_password:
        print("❌ Gmail credentials not found in .env file!")
        print("   Add: GMAIL_USER=your.email@gmail.com")
        print("   Add: GMAIL_APP_PASSWORD=your_app_password")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CV
        if os.path.exists(cv_path):
            with open(cv_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cv_path)}')
                msg.attach(part)
        
        # Attach Cover Letter
        if os.path.exists(cover_letter_path):
            with open(cover_letter_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(cover_letter_path)}')
                msg.attach(part)
        
        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent to: {to_email}")
        return True
        
    except smtplib.SMTPRecipientsRefused as e:
        print(f"❌ SMTP Recipient refused: {e}")
        print(f"   Email address '{to_email}' may be invalid or rejected")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to send email: {type(e).__name__}: {e}")
        return False


def test_gmail_connection():
    """
    Test Gmail connection
    """
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    if not gmail_user or not gmail_password:
        print("❌ Gmail credentials not found!")
        return False
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.quit()
        print("✅ Gmail connection successful!")
        return True
    except Exception as e:
        print(f"❌ Gmail connection failed: {e}")
        return False


if __name__ == "__main__":
    print("\n🔧 Testing Gmail Connection...\n")
    test_gmail_connection()
