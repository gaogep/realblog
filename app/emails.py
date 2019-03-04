import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail


def send_email(subject, to, body):
    sg = sendgrid.SendGridAPIClient(api=os.environ.get('MAIL_API'))
    form_email = Email('noreply@zpf.com')
    to_email = Email(to)
    message = Content("text/plain", body)
    complete_mail = Mail(form_email, subject, to_email, message)
    response = sg.client.send.post(request_body=complete_mail.get())
    return response
