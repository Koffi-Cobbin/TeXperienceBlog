__author__ = "Cobbin"
import os


URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')
FROM = os.environ.get('MAILGUN_FROM')
TO = None
SUBJECT = None
ALERT_TIMEOUT = 10
COLLECTION = "alerts"

#   "https://api.mailgun.net/v3/sandbox26656e57078b4b838ca8bf19932b2dc6.mailgun.org"
#   "key-3ax6xnjp29jd6fds4gc373sgvjxteol0"
#   "Mailgun Sandbox <postmaster@sandbox<26656e57078b4b838ca8bf19932b2dc6>.mailgun.org"
#
#   --# "cd02ea361ce7cd0df736d98c6dee95c6-a83a87a9-73b7b35b"