import requests
import json
import ConfigParser
import smtplib
from email.mime.text import MIMEText


class NotificationMixin(object):

    def notify_by_email(self, email_to=[], email_from=None, body=None):

        msg = MIMEText(body, 'plain')
        msg['Subject'] = body
        msg['From'] = email_from
        msg['To'] = email_to

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()

        server.login(self.gmail_user, self.gmail_password)

        server.sendmail(self.email_from, self.email_to, msg.as_string())

