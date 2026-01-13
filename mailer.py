import smtplib
from email.mime.text import MIMEText
from config import MAIL_SENDER, MAIL_RECEIVER, MAIL_PASSWORD
from logger import log

def send_mail(subject, body):
    try:
        msg = MIMEText(body, "html", "utf-8")
        msg['From'] = MAIL_SENDER
        msg['To'] = ", ".join(MAIL_RECEIVER)
        msg['Subject'] = subject

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(MAIL_SENDER, MAIL_PASSWORD)
        print("mail_receiver : ",MAIL_RECEIVER)
        server.sendmail(MAIL_SENDER, MAIL_RECEIVER, msg.as_string())
        server.quit()

        log("📧 Mail gönderildi.")
    except Exception as e:
        log(f"❌ Mail gönderilemedi: {str(e)}")
