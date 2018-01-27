from os import environ
from string import ascii_letters, digits

MESSAGE_TABLE = environ['MESSAGE_TABLE']
CHANNEL_TABLE = environ['CHANNEL_TABLE']

VAPID_PRIVKEY = environ['NOTIFY_VAPID_PRIVKEY']
VAPID_PUBKEY = environ['NOTIFY_VAPID_PUBKEY']
VAPID_EMAIL = environ['NOTIFY_VAPID_EMAIL']

CHANNEL_ID_LENGTH = 16
CHANNEL_ID_CHARS = ascii_letters + digits
