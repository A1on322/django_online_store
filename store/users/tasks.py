from celery import shared_task
import logging

from django.core.mail import EmailMultiAlternatives
from django.template import loader

logger = logging.getLogger("django.contrib.auth")


@shared_task
def send_password_reset_email(subject_template_name,
                              email_template_name,
                              context,
                              from_email,
                              to_email,
                              html_email_template_name=None,
                              ):
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = "".join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, "text/html")

    try:
        email_message.send()
    except Exception:
        logger.exception(
            "Failed to send password reset email to %s", context["user"].pk
        )
