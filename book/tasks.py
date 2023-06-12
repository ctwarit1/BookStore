from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(bind=True)
def send_mail_func(self, to_email, title):
    send_mail(
        subject=f"reminder for {title}",
        message=title,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return "Done"
