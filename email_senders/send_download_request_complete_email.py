import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mako.template import Template


def main(name, task_code, description, recipient, sender='TacticDebug@2gdigital.com',
         smtp_server_name='mail.2gdigital.com'):
    if name and task_code and description and recipient:
        recipient = 'tyler.standridge@2gdigital.com'

        message = MIMEMultipart('alternative')
        message['Subject'] = 'Download Request Complete: {0}'.format(name)
        message['From'] = sender
        message['To'] = recipient

        smtp_server = smtplib.SMTP(smtp_server_name)

        directory_path = os.path.dirname(os.path.realpath(__file__))
        templates_path = os.path.join(directory_path, 'templates/')

        plain_text_file = os.path.join(templates_path, 'download_request_complete.txt')
        html_file = os.path.join(templates_path, 'download_request_complete.html')

        plain_text_template = Template(filename=plain_text_file)
        html_template = Template(filename=html_file)

        kwargs = {
            'name': name,
            'task_code': task_code,
            'description': description
        }

        plain_text = MIMEText(plain_text_template.render(**kwargs), 'plain')
        html_text = MIMEText(html_template.render(**kwargs), 'html')

        message.attach(plain_text)
        message.attach(html_text)

        smtp_server.sendmail(sender, recipient, message.as_string())
        smtp_server.quit()


if __name__ == '__main__':
    main('Testing', 'TestTask123', 'This is a test', 'tyler.standridge@2gdigital.com')
