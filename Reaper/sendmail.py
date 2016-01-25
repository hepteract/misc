import smtplib

from email.mime.text import MIMEText

import sys
import imaplib
import getpass
import email
import datetime

username = 'grimreaper.client@gmail.com'
password = 'iAMaBADpassword'

def send(toaddrs, msg, subject = "", fromname = username, fromaddr = username, raw = False):
    if not raw:
        msg = MIMEText(msg)
        msg["Subject"] = subject
        msg["From"] = fromname
        msg["To"] = toaddrs
        msg = msg.as_string()
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
    
    return True

def update_imap():
    global imap
    
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(username, password)
    imap.select("INBOX")
update_imap()

seen = []
def recv():
    update_imap()
    
    rv, data = imap.search(None, "ALL")
    if rv != 'OK':
        return []

    ret = []

    for num in data[0].split():
        rv, data = imap.fetch(num, '(RFC822)')
        if rv != 'OK':
            return

        ret.append( email.message_from_string(data[0][1]) )
    
    global seen

    final = [item for item in ret if item.as_string() not in seen]
    seen += [item.as_string() for item in final]
    
    return final
