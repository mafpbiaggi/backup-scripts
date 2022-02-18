# backup.py
# Author: Marco Aurélio Fernandes Piton Biaggi
# E-mail: mafpbiaggi@gmail.com

from email.mime.text import MIMEText
from datetime import date
import smtplib, os

# Define all variables
SMTP_SERVER = ""
SMTP_PORT = ""
SMTP_USERNAME = ""
SMTP_PASSWORD = ""

EMAIL_TO = ""
EMAIL_FROM = ""
EMAIL_SUBJECT = "[<companyname>] - BACKUP SERVIDOR: <servername>"

DATE_FORMAT = "%d/%m/%Y"

# Data sources
SRC1 = "/etc"
SRC2 = "/dados"

# Destination
DEST = "/mnt/backup"

# Log file
LOG_FILE = "/etc/scripts/backup.log"

# Synchronize data
os.system("echo > " + LOG_FILE)

if os.path.ismount("/mnt") is False:
    os.system("mount -t ext4 /dev/disk/by-uuid/<UUID> /mnt")

os.system("rsync -aAr --log-file '" + LOG_FILE + "' --delete-excluded " + SRC1 + " " + DEST)
os.system("rsync -aAr --log-file '" + LOG_FILE + "' --delete-excluded " + SRC2 + " " + DEST)

os.system("umount /mnt")

# Open log file and append to message
LOG = open(LOG_FILE)
DATA = LOG.read()

# Send email function using smtplib
def send_email():
    msg = MIMEText(DATA)
    LOG.close()
    msg['Subject'] = EMAIL_SUBJECT + " - [%s]" % (date.today().strftime(DATE_FORMAT))
    msg['To'] = EMAIL_TO
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()

# main
if __name__=='__main__':
    send_email()