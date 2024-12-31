import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.contrib.forms.models import FormSubmission

from website.models import CustomSetting


@receiver(post_save, sender=FormSubmission)
def contact_form_signal(sender, instance, created, **kwargs):
    if created:
        setting = CustomSetting.objects.first()
        subject = 'New Contact Form Received'

        message = "A new contact form has been filled out.<br>"
        form_data = instance.form_data
        for field, value in form_data.items():
            message += f"<strong>{field.capitalize()}</strong>: {value}<br>"

        to_email = setting.owner_mail
        print(to_email)
        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                to=[to_email],
            )
            msg.attach_alternative(message, "text/html")
            msg.send()

            print("Email sent successfully!")

        except Exception as e:
            print(f"An error occurred while sending the email: {e}")


post_save.connect(contact_form_signal, sender=FormSubmission)
