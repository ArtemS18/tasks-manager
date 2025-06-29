from email.message import EmailMessage


def hello_template(from_email:str, to_email:str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = "Hello World!"
    message.set_content("Sent via aiosmtplib")
    return message

def autho_email_template(from_email:str, to_email:str, password: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = "Confirm your email!"
    message.set_content(f"Password: {password}")