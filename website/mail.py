from django.core.mail.backends.smtp import EmailBackend

from website.models import CustomSetting


class CustomMailBackend(EmailBackend):
    custom_setting: CustomSetting

    def __init__(
        self,
        host=None,
        port=None,
        username=None,
        password=None,
        use_tls=None,
        use_ssl=None,
        **kwargs,
    ):
        self.custom_setting = CustomSetting.objects.first()
        super().__init__(
            host=self.custom_setting.email_host if host is None else host,
            port=self.custom_setting.email_port if port is None else port,
            username=self.custom_setting.email_host_user if username is None else username,
            password=self.custom_setting.email_host_password if password is None else password,
            use_tls=self.custom_setting.email_use_tls if use_tls is None else use_tls,
            use_ssl=self.custom_setting.email_use_ssl if use_ssl is None else use_ssl,
            **kwargs,
        )

    def _send(self, email_message):
        # Only override the sender if it's the default webmaster@localhost
        if email_message.from_email == 'webmaster@localhost':
            email_message.from_email = self.custom_setting.email_sender
        return super()._send(email_message)
