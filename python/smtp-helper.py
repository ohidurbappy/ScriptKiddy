import smtplib
from email import encoders as Encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


def send_mail(to,sender, subject, text,username="",password="",hostname="smtp.gmail.com",port=465, cc=None, bcc=None, reply_to=None, attach=None,
         html=None, pre=False, custom_headers=None):
    msg = MIMEMultipart()

    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject

    to = [to]

    if cc:
        # cc gets added to the text header as well as list of recipients
        if type(cc) in [str]:
            msg.add_header('Cc', cc)
            cc = [cc]
        else:
            cc = ', '.join(cc)
            msg.add_header('Cc', cc)
        to += cc

    if bcc:
        # bcc does not get added to the headers, but is a recipient
        if type(bcc) in [str]:
            bcc = [bcc]
        to += bcc

    if reply_to:
        msg.add_header('Reply-To', reply_to)

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to
    # display.

    if pre:
        html = "<pre>%s</pre>" % text
    if html:
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)

        msgText = MIMEText(text)
        msgAlternative.attach(msgText)

        # We reference the image in the IMG SRC attribute by the ID we give it
        # below
        msgText = MIMEText(html, 'html')
        msgAlternative.attach(msgText)
    else:
        msg.attach(MIMEText(text))

    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    if custom_headers:
        for k, v in custom_headers.iteritems():
            msg.add_header(k, v)

    mailServer = smtplib.SMTP_SSL(hostname, port=port)
    mailServer.ehlo()
    # mailServer.starttls()
    mailServer.login(username, password)
    mailServer.sendmail(username, to, msg.as_string())
    mailServer.close()
