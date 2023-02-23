from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task

from DualViewProject.settings import EMAIL_HOST_USER


@shared_task
def send_verification_code(instance):
    html_message = render_to_string('email_verification.html', {
        'username': instance.username,
        'verification_code': instance.verification_code
    })
    plain_message = strip_tags(html_message)
    send_mail(
        'Verification code',
        plain_message,
        EMAIL_HOST_USER,
        [instance.email],
        html_message=html_message,
    )
