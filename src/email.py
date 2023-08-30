from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from src import models
from src.config import settings
from jinja2 import Environment, select_autoescape, PackageLoader

env = Environment(
    loader=PackageLoader('src', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Email:
    def __init__(self, user: models.User, url: str, email: List[EmailStr]):
        self.name = user.name
        self.sender = 'Codevo <admin@admin.com>'
        self.email = email
        self.url = url
        pass

    async def sendMail(self, subject, template):
        # Define the config
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_USERNAME,
            MAIL_PASSWORD=settings.EMAIL_PASSWORD,
            MAIL_FROM=settings.EMAIL_FROM,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        # Generate the HTML template base on the template name
        template = env.get_template(f'{template}.html')

        html = template.render(
            url=self.url,
            first_name=self.name,
            subject=subject
        )

        # Define the message options
        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            body=html,
            subtype="html"
        )

        # Send the email
        fm = FastMail(conf)
        await fm.send_message(message)

    async def sendVerificationCode(self, template_name):
        if template_name == 'verification':
            code_name = 'email'
        else:
            code_name = 'password'
        await self.sendMail(f'Your {code_name} code (Valid for 10min)', f"{template_name}")

