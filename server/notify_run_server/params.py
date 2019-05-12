from os import environ
from string import ascii_letters, digits

DB_URI = environ.get('NOTIFY_DB_URI', 'sqlite:///notify.sqlite')

if DB_URI.startswith('dynamodb:'):
    _, MESSAGE_TABLE, CHANNEL_TABLE = DB_URI.split(':')
    DB_MODEL = 'boto'
else:
    DB_MODEL = 'sql'

VAPID_PRIVKEY = environ['NOTIFY_VAPID_PRIVKEY']
VAPID_PUBKEY = environ['NOTIFY_VAPID_PUBKEY']
VAPID_EMAIL = environ['NOTIFY_VAPID_EMAIL']

API_SERVER = environ['NOTIFY_API_SERVER']
WEB_SERVER = environ['NOTIFY_WEB_SERVER']

CHANNEL_ID_LENGTH = 16
CHANNEL_ID_CHARS = ascii_letters + digits
