from django.core.mail import send_mail
from django.conf import settings

def send_email(subject,message,recipient_list):
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, recipient_list)

# Call the function to send the email
send_email()
