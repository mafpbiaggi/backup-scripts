# backup.py
# Author: Marco Aurélio Fernandes Piton Biaggi
# E-mail: mafpbiaggi@gmail.com

from email.mime.text import MIMEText
from datetime import date
import smtplib, os

# SMTP config data
SMTP_SERVER = ""
SMTP_PORT = ""
SMTP_USERNAME = ""
SMTP_PASSWORD = ""

EMAIL_TO = ""
EMAIL_FROM = ""
EMAIL_SUBJECT = "[<companyname>] - BACKUP SERVIDOR: <servername>"

# Date format for logging
DATE_FORMAT = "%d/%m/%Y"

# Sources
SRC1 = "/etc"
SRC2 = "/dados"

# Destination
DEST = "/mnt/backup"

# Log file
LOG_FILE = "/etc/scripts/backup.log"

# Start backup routine
os.system("echo > " + LOG_FILE)

# Check if external disk is mounted. If not, then mount it.
if os.path.ismount("/mnt") is False:
    os.system("mount -t ext4 /dev/disk/by-uuid/<UUID> /mnt")

# Copy only differential data from sources to destination using rsync
os.system("rsync -aAr --log-file '" + LOG_FILE + "' --delete-excluded " + SRC1 + " " + DEST)
os.system("rsync -aAr --log-file '" + LOG_FILE + "' --delete-excluded " + SRC2 + " " + DEST)

# After copy, umount destination mount point
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