from pywebpush import webpush, WebPushException

from notify_run_server.params import VAPID_PRIVKEY, VAPID_EMAIL
from multiprocessing import Pool
import json
from urllib.parse import urlparse
from collections import namedtuple
from requests.exceptions import ConnectTimeout

MessageSpec = namedtuple('MessageSpec', ['subscription_id', 'subscription_spec', 'message_json'])

def parallel_notify(subscriptions, message, channel_id, data, **params):
    message_json = json.dumps({
        'message': message,
        'channel': channel_id,
        'data': data,
        **params
    })
    
    pool = Pool(processes=5)

    messages = [
        MessageSpec(subscription_id, subscription_spec, message_json)
        for subscription_id, subscription_spec in subscriptions.items()
    ]

    print(messages)

    return pool.map(notify, messages)

def notify(message_spec: MessageSpec):
    VAPID_PARAMS = {
        'vapid_private_key': VAPID_PRIVKEY,
        'vapid_claims': {'sub': 'mailto:{}'.format(VAPID_EMAIL)}
    }

    endpoint_domain = urlparse(message_spec.subscription_spec['endpoint']).netloc
    try:
        r = webpush(
            subscription_info=message_spec.subscription_spec,
            data=message_spec.message_json,
            timeout=10,
            **VAPID_PARAMS
        )

        return {
            'subscription': message_spec.subscription_id,
            'endpoint_domain': endpoint_domain,
            'result_status': str(r.status_code),
            'result_message': r.text or None
        }
    except WebPushException as e:
        return {
            'subscription': message_spec.subscription_id,
            'endpoint_domain': endpoint_domain,
            'result_status': 'WebPush Exception',
            'result_message': str(e)
        }
    except ConnectTimeout as e:
        return {
                    'subscription': message_spec.subscription_id,
                    'endpoint_domain': endpoint_domain,
                    'result_status': 'Connection Timeout',
                    'result_message': str(e)
                }
