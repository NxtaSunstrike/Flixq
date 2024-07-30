from typing import Any
import os

import smtplib

from email.message import EmailMessage

from celery import Celery

from settings.AppSettings import FastAPI_Settings
from settings.TasksSettings import tasksSettings

from shemas.SendEmailShema import EmailTask


broker = os.environ.get(FastAPI_Settings.CELERY_BROKER_URL)
result = os.environ.get(FastAPI_Settings.CELERY_RESULT_BACKEND)

print(broker, result)

celery=Celery(__name__)
celery.conf.broker_url=broker
celery.conf.result_backend=result

@celery.task(name='send_email')
def send_email(
    content: str | Any,  email: str
) ->Any:
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = 'Confirmation code'
    msg['To'] = email
    with smtplib.SMTP_SSL(
            host=tasksSettings.EMAIL_HOST,
            port=tasksSettings.EMAIL_PORT
        ) as smtp:
        smtp.login(
                user=tasksSettings.EMAIL_USER,
                password=tasksSettings.EMAIL_PASSWORD
            )
        smtp.send_message(msg)