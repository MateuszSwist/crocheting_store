from smtplib import SMTPException
from django.core.mail import send_mail
from django.template.loader import get_template


def send_confirmation_email(email, token_id, user_id):
    data = {"token_id": str(token_id), "user_id": str(user_id)}
    message = get_template("confirmation.txt").render(data)
    try:
        send_mail(
            subject="Please confirm email",
            message=message,
            from_email=None,
            recipient_list=[email],
            fail_silently=True,
        )
    except SMTPException as e:
        (
            f" {e} Problem with mail confirmation, contact with crochetingstorewro@gmail.com"
        )
