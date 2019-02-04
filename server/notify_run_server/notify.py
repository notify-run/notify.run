from pywebpush import webpush

from notify_run_server.params import VAPID_PRIVKEY, VAPID_EMAIL
from multiprocessing import Process
import json


def parallel_notify(subscriptions, message, channel_id, data):
    procs = list()
    for subscription in subscriptions:
        print(subscription)
        message_json = json.dumps({
            'message': message,
            'channel': channel_id,
            'data': data
        })

        p = Process(target=notify, args=(subscription, message_json))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()


def notify(subscription, data):
    VAPID_PARAMS = {
        'vapid_private_key': VAPID_PRIVKEY,
        'vapid_claims': {'sub': 'mailto:{}'.format(VAPID_EMAIL)}
    }

    r = webpush(
        subscription_info=subscription,
        data=data,
        timeout=10,
        **VAPID_PARAMS
    )
