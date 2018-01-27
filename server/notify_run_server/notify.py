from pywebpush import webpush

from notify_run_server.params import VAPID_PRIVKEY, VAPID_EMAIL


def notify(subscription, data):
    VAPID_PARAMS = {
        'vapid_private_key': VAPID_PRIVKEY,
        'vapid_claims': {'sub': 'mailto:{}'.format(VAPID_EMAIL)}
    }

    print('trying', subscription)
    webpush(
        subscription_info=subscription,
        data=data,
        **VAPID_PARAMS
    )
