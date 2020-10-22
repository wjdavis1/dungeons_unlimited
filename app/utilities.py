import base64
import os
from threading import Thread
from flask import current_app, url_for
from flask_mail import Message
from app import mail

# Email settings


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    if sync:
        mail.send(msg)
    else:
        Thread(
            target=send_async_email,
            args=(
                current_app._get_current_object(),
                msg)).start()


# Profile image utility

def image_file_picker(image):
    pass


def image_to_string():
    pass


def byte_to_image(byte):
    pass
