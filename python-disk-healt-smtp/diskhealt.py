#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from os import path, getlogin, system, listdir, getuid, environ
from psutil import disk_usage
from email.mime.text import MIMEText

class disk_healt:
    ruta_exec=path.dirname(path.realpath(__file__))
    directory_backups="backups"

    def check_disk(self, check_path = '/'):
        obj_Disk = disk_usage(check_path)

        total = int(obj_Disk.total / (1024.0 ** 3))
        used = int(obj_Disk.used / (1024.0 ** 3))
        free = int(obj_Disk.free / (1024.0 ** 3))
        percent_used = int(obj_Disk.percent)

        status_disk = """Check: %s
        Total disk: %sG
        Used: %sG
        Free: %sG
        Percent used: %s%%
        """ % (check_path, total, used, free, percent_used)

        print status_disk
        warning_percent = 80
        critical_percent = 90
        status = "OK"
        if percent_used > warning_percent:
            status = "WARNING"
        elif percent_used > critical_percent:
            status = "CRITICAL"

        if percent_used > warning_percent and environ['EMAIL_MODE'] != "OFF":
            print "Try send email..."
            self.send_mail("[BACKUP - %s] Status %s" % (environ['BACKUP_INFO'], status), status_disk)

    def send_mail(self, subject, body):
        send_to = environ['EMAIL_SEND_TO'].split(",")
        email_mode = environ['EMAIL_MODE']
        email_server = environ['EMAIL_SERVER']
        email_port = environ['EMAIL_PORT']
        email_user = environ['EMAIL_USER']
        email_password = str(environ['EMAIL_PASSWORD'].encode('utf-8'))

        server = smtplib.SMTP(email_server, email_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        try:
            server.login(email_user, email_password)

            msg = MIMEText(body, "html")
            msg['Subject'] = subject
            msg['From'] = email_user
            msg['To'] = ', '.join(send_to)

            try:
                for s in send_to:
                    server.sendmail(email_user, s, msg.as_string())
                print '[INFO] Email sent!'
            except Exception as e:  
                print '[ERROR] Email: %s' % (e)
        except Exception as e:  
                print '[ERROR] %s' % (e)

def main():
    dh = disk_healt()
    dh.check_disk(check_path=environ['BACKUP_DIR'])

if __name__ == '__main__':
    main()

