import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
GMAIL_ADDRESS = 'sundaihack@gmail.com'
APP_PASSWORD = 'alsrrtxdvpejwvdw'  # Sin espacios, como se configuraría en Render

def send_test_email():
    """
    Send a test email via Gmail SMTP server using App Password authentication.
    """
    # Create a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = "Test Email from Tally Subscriber Manager"
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = GMAIL_ADDRESS  # Sending to ourselves for testing
    
    # Add body to email
    body = "This is a test email to verify the Gmail app password is working correctly."
    msg.attach(MIMEText(body, 'plain'))
    
    # Create SMTP session
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.ehlo()  # Identify yourself to the server
            smtp_server.login(GMAIL_ADDRESS, APP_PASSWORD)  # Login with app password
            smtp_server.sendmail(GMAIL_ADDRESS, [GMAIL_ADDRESS], msg.as_string())
        
        print("Test email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending test email: {e}")
        return False

if __name__ == "__main__":
    send_test_email()
