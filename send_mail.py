#!/usr/bin/env python

import smtplib
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
import sys

now = datetime.datetime.now()
t8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
t6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)

if (now < t8am or now > t6pm):
    exit()

# me == my email address
# you == recipient's email address
me = sys.argv[1]
you = sys.argv[2]

author = formataddr((str(Header(u'Windalert Update','utf-8')),me))

print "Sending..."

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "--- Surfing Wind Has Been Detected! ---"
msg['From'] = author
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "none"
html = """\
    <html>
<head></head>
<body>
%s
</p>
</body>
</html>
""" % sys.argv[3]
# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP('smtpcorp.com', port=2525)
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
data=''
with open ("credentials.txt", "r") as myfile:
    data=myfile.read().replace('\n', '')
s.login('ariz',data)
s.sendmail(me, [you], msg.as_string())
print "Done!"
s.quit()
