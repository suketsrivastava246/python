import smtplib
import ssl
from email.message import EmailMessage

EMAIL="suketsrivastava246@gmail.com"
APP_PASSWORD="qkmp ctei xjtz edcl"
RECEIVER="24tec2aids071@vgu.ac.in"

msg=EmailMessage()

msg["From"]=EMAIL
msg["To"]=RECEIVER
msg["Subject"]="Hello From Python code......"

msg.set_content("This email was shared by python code .....")

context = ssl.create_default_context()

with smtplib.SMTP_SSl("smtp.gmail.com",465,context=context) as server:
    server.login(EMAIL,APP_PASSWORD)
    server.send_message(msg)

print("Email sent successfully")