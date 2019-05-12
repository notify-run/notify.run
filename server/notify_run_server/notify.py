import json
from multiprocessing import Pipe, Process
from urllib.parse import urlparse

from pywebpush import WebPushException, webpush
from requests.exceptions import ConnectTimeout

from notify_run_server.params import VAPID_EMAIL, VAPID_PRIVKEY


def parallel_notify(subscriptions, message, channel_id, data, **params):
    message_json = json.dumps({
        'message': message,
        'channel': channel_id,
        'data': data,
        **params
    })

    procs = list()
    pipes = list()

    for subscription_id, subscription_spec in subscriptions.items():
        result_pipe, child_pipe = Pipe()
        proc = Process(target=notify, args=(subscription_id,
                                            subscription_spec, message_json, child_pipe))
        proc.start()
        procs.append(proc)
        pipes.append(result_pipe)

    result = list()

    for proc, pipe in zip(procs, pipes):
        result.append(pipe.recv())
        proc.join()

    return result


def notify(subscription_id, subscription_spec, message_json, pipe):
    vapid_params = {
        'vapid_private_key': VAPID_PRIVKEY,
        'vapid_claims': {'sub': 'mailto:{}'.format(VAPID_EMAIL)}
    }

    endpoint_domain = urlparse(subscription_spec['endpoint']).netloc
    try:
        result = webpush(
            subscription_info=subscription_spec,
            data=message_json,
            timeout=10,
            **vapid_params
        )

        pipe.send({
            'subscription': subscription_id,
            'endpoint_domain': endpoint_domain,
            'result_status': str(result.status_code),
            'result_message': result.text or None
        })
    except WebPushException as err:
        pipe.send({
            'subscription': subscription_id,
            'endpoint_domain': endpoint_domain,
            'result_status': 'WebPush Exception',
            'result_message': str(err)
        })
    except ConnectTimeout as err:
        pipe.send({
            'subscription': subscription_id,
            'endpoint_domain': endpoint_domain,
            'result_status': 'Connection Timeout',
            'result_message': str(err)
        })
