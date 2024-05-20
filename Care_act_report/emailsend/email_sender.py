import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging

class EmailSender:
    def __init__(self, config):
        self.config = config

    def send_email(self, pdf_path, recipient_email, pdf_filename, body_content):
        msg = MIMEMultipart()
        msg['From'] = self.config['smtp_user']
        msg['To'] = recipient_email
        msg['Subject'] = 'Care Assessment Report'

        msg.attach(MIMEText(body_content, 'plain'))

        try:
            with open(pdf_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=pdf_filename)
            part['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
            msg.attach(part)
        except Exception as e:
            logging.error(f"Failed to attach PDF: {e}")
            return

        try:
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_user'], self.config['smtp_password'])
            server.sendmail(self.config['smtp_user'], recipient_email, msg.as_string())
            server.quit()
            logging.info(f"Email sent to {recipient_email}")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
