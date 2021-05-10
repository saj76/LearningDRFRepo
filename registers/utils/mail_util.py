from django.core.mail import EmailMessage


def send_email(subject, content, to_email):
    email = EmailMessage(
        subject,
        body=content,
        to=to_email
    )
    email.send()
