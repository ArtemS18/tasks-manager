from email.message import EmailMessage

from app.auth.schemas.users import User
from app.projects.schemas.projects.projects import Project


def hello_template(from_email: str, to_email: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = "Hello World!"
    message.set_content("Sent via aiosmtplib")
    return message


def autho_email_template(from_email: str, to_email: str, password: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = "Confirm your email!"
    message.set_content(f"Password: {password}")
    return message


def joining_email_template(
    from_email: str,
    to_email: str,
    owner_user: User,
    joined_user: User,
    project: Project,
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = f"You has joined in project: {project.name}"
    message.set_content(
        f"Hello {joined_user.name}! {owner_user.name} join you in project: {project.name}"
    )
    return message
