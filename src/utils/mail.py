import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig
load_dotenv()
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_ADDRESS,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_ADDRESS,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",  
    MAIL_FROM_NAME="Subnotifly",
    
    MAIL_STARTTLS=True,  
    MAIL_SSL_TLS=False,     
)

fm = FastMail(conf)
