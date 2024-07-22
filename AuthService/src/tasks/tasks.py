from typing import Any
import smtplib

from settings.TasksSettings import tasksSettings

from email.message import EmailMessage

from shemas.SendEmailShema import EmailTask

from faststream.redis.fastapi import Logger

from faststream.redis.fastapi import RedisRouter

from settings.AppSettings import FastAPI_Settings

router = RedisRouter(
    url=FastAPI_Settings.REDIS
)

@router.subscriber('tasks')
async def send_email(
    content: EmailTask, logger: Logger
) ->Any:
    logger.info(content)
    msg = EmailMessage()
    msg.set_content(str(content.content))
    msg['Subject'] = 'Confirmation code'
    msg['To'] = content.email
    with smtplib.SMTP_SSL(
            host=tasksSettings.EMAIL_HOST,
            port=tasksSettings.EMAIL_PORT
        ) as smtp:
        smtp.login(
                user=tasksSettings.EMAIL_USER,
                password=tasksSettings.EMAIL_PASSWORD
            )
        smtp.send_message(msg)