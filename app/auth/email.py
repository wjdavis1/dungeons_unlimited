from flask import render_template, current_app
from app.utilities import send_email


def password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[Dungeons Unlimited] Reset Your Password',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template(
            'reset_password_message.txt',
            user=user,
            token=token),
        html_body=render_template(
            'reset_password_message.html',
            user=user, token=token))
