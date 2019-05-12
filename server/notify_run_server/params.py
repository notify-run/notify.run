from os import environ
from string import ascii_letters, digits

DB_URI = environ.get('NOTIFY_DB_URI', 'sqlite:///notify.sqlite')

if DB_URI.startswith('dynamodb:'):
    _, MESSAGE_TABLE, CHANNEL_TABLE = DB_URI.split(':')
    DB_MODEL = 'boto'
else:
    DB_MODEL = 'sql'

try:
    VAPID_PRIVKEY = environ['NOTIFY_VAPID_PRIVKEY']
    VAPID_PUBKEY = environ['NOTIFY_VAPID_PUBKEY']
except KeyError:
    VAPID_PRIVKEY = 'iC1oJ5MJWgin6JTypILNugemG7YWDaLsn89i-8nE-8A'
    VAPID_PUBKEY = 'BHIFnSbJHMJfu_zSZ3--5CgzavDsQBsAs0nnfFrZ5s0RtddV6Jd8fs4nHylG4ktBTwJSL_lM5yl4eLJ9v6bshVU'
    print('WARNING: Built-in VAPID keys will be used. '
        'For public deployments, use the environment variables VAPID_PRIVKEY '
        'and VAPID_PUBKEY to pass your own.')

VAPID_EMAIL = environ.get('NOTIFY_VAPID_EMAIL', 'notify-server-default@paulbutler.org')

WEB_SERVER = environ.get('NOTIFY_WEB_SERVER', None)
API_SERVER = environ.get('NOTIFY_API_SERVER', WEB_SERVER)

CHANNEL_ID_LENGTH = 16
CHANNEL_ID_CHARS = ascii_letters + digits
