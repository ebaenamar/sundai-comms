import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Email configuration
GMAIL_ADDRESS = os.environ.get('GMAIL_ADDRESS', 'sundaihack@gmail.com')
APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '')

def send_gmail(subject, body, recipients, attachment_path=None):
    """
    Send email via Gmail SMTP server using App Password authentication.

    Parameters:
    - subject: Email subject
    - body: Email body content (plain text)
    - recipients: List of recipient email addresses or single email as string
    - attachment_path: Optional path to file attachment
    """
    # Convert single recipient to list if needed
    if isinstance(recipients, str):
        recipients = [recipients]

    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = ', '.join(recipients)

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    # Add attachment if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))

        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
        msg.attach(part)

    # Create SMTP session
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.ehlo()  # Identify yourself to the server
            smtp_server.login(GMAIL_ADDRESS, APP_PASSWORD)  # Login with app password
            smtp_server.sendmail(GMAIL_ADDRESS, recipients, msg.as_string())

        logger.info(f"Email sent successfully to {len(recipients)} recipients!")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def send_newsletter(subject, content, recipients, attachment_path=None):
    """
    Send a newsletter to multiple recipients
    """
    return send_gmail(subject, content, recipients, attachment_path)

def send_welcome_email(recipient_email, recipient_name=None):
    """
    Send a welcome email to a new subscriber
    """
    subject = "Welcome to Our Newsletter!"
    name = recipient_name or "there"
    body = f"""
Hello {name},

Thank you for subscribing to our newsletter! We're excited to have you join our community.

You'll receive updates on our latest content, news, and special offers.

If you have any questions, feel free to reply to this email.

Best regards,
The Team
    """
    return send_gmail(subject, body, recipient_email)

def send_confirmation_email(recipient_email, recipient_name=None):
    """
    Send a confirmation email to a subscriber
    """
    subject = "Subscription Confirmed"
    name = recipient_name or "there"
    body = f"""
Hello {name},

Your subscription has been confirmed. Thank you for joining our newsletter!

Best regards,
The Team
    """
    return send_gmail(subject, body, recipient_email)
