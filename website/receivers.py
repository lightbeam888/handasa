import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail
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

        from_email = setting.email_sender
        to_email = setting.owner_mail

        # SMTP config
        smtp_host = setting.email_host
        smtp_port = setting.email_port
        smtp_user = setting.email_host_user
        smtp_password = setting.email_host_password

        try:
            # Create HTML-formatted email message
            msg = MIMEMultipart()
            msg.attach(MIMEText(message, 'html'))
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = to_email

            # Connect to smtp and send mail
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                # Send mail
                server.sendmail(from_email, [to_email], msg.as_string())
            print("Email sent successfully!")

        except Exception as e:
            print(f"An error occurred while sending the email: {e}")


post_save.connect(contact_form_signal, sender=FormSubmission)
