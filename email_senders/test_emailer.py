import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mako.template import Template


def main():
    sender = 'TacticDebug@2gdigital.com'
    recipient = 'tyler.standridge@2gdigital.com'

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Testing'
    message['From'] = sender
    message['To'] = recipient

    smtp_server_name = 'mail.2gdigital.com'

    smtp_server = smtplib.SMTP(smtp_server_name)

    plain_text_template = Template(filename='templates/generic_internal_message.txt')
    html_template = Template(filename='templates/generic_internal_message.html')

    plain_text = MIMEText(plain_text_template.render(message='Testing the email sender'), 'plain')
    html_text = MIMEText(html_template.render(message='Testing the email sender.'), 'html')

    message.attach(plain_text)
    message.attach(html_text)

    smtp_server.sendmail(sender, recipient, message.as_string())
    smtp_server.quit()


if __name__ == '__main__':
    main()