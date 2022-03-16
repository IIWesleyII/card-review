import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv
load_dotenv()

# send email of the transaction report
def send_email_report():
    #Setup the MIME
    message = MIMEMultipart()
    sender = os.getenv('EMAIL_ADDRESS_SENDER')
    receiver = os.getenv('EMAIL_ADDRESS_RECEIVER')
    password = os.getenv('EMAIL_PASSWORD')
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'Transaction Report'
    
    pdf_path = 'transaction_reports/TransactionReport.pdf'
    binary_pdf = open(pdf_path, 'rb')
 
    payload = MIMEBase('application', 'octate-stream', Name=pdf_path)
    payload.set_payload((binary_pdf).read())
    encoders.encode_base64(payload)

    payload.add_header('Content-Decomposition', 'attachment', filename=pdf_path)
    message.attach(payload)
    
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent')