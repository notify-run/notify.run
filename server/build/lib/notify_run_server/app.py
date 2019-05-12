from io import BytesIO

from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from pyqrcode import QRCode

from notify_run_server.model import NoSuchChannel, NotifyModel
from notify_run_server.notify import parallel_notify
from notify_run_server.params import (API_SERVER, DB_MODEL,
                                      VAPID_PUBKEY, WEB_SERVER, CHANNEL_ID_CHARS)

from werkzeug.routing import Rule, Map, BaseConverter, ValidationError

import pkg_resources

static_file_path = pkg_resources.resource_filename('notify_run_server', 'static')

class ChannelIDConverter(BaseConverter):
    def to_python(self, value):
        if not all(c in set(CHANNEL_ID_CHARS) for c in value):
            raise ValidationError()
        return value

try:
    from urllib.parse import parse_qs
except ImportError:
    from urlparse import parse_qs  # type: ignore


app = Flask(__name__, static_url_path='', static_folder=static_file_path)
print(app._static_folder)
CORS(app)
app.url_map.converters['chid'] = ChannelIDConverter

if DB_MODEL == 'boto':
    from notify_run_server.model_dynamodb import DynamodbNotifyModel
    model = DynamodbNotifyModel()  # type: NotifyModel
elif DB_MODEL == 'sql':
    from notify_run_server.model_sqlalchemy import SqlNotifyModel
    model = SqlNotifyModel()
else:
    raise NotImplementedError()


def channel_page_url(channel_id):
    return (WEB_SERVER or request.host) + '/c/' + channel_id


def channel_endpoint(channel_id):
    return (API_SERVER or request.host) + '/' + channel_id


def qr_for_channel(channel_id):
    return QRCode(channel_page_url(channel_id))


@app.route('/api/pubkey', methods=['GET'])
def get_pubkey():
    return jsonify({'pubKey': VAPID_PUBKEY})


@app.route('/api/register_channel', methods=['POST'])
def register_channel():
    channel_id = model.register_channel({
        'ip': request.remote_addr,
        'agent': request.headers.get('User-Agent'),
    })
    return jsonify({
        'channelId': channel_id,
        'pubKey': VAPID_PUBKEY,
        'messages': [],
        'channel_page': channel_page_url(channel_id),
        'endpoint': channel_endpoint(channel_id),
    })


@app.route('/<chid:channel_id>/subscribe', methods=['POST'])
def subscribe(channel_id):
    model.add_subscription(channel_id, request.get_json())
    return jsonify(dict())


@app.route('/<chid:channel_id>/qr.svg', methods=['GET'])
def get_qr(channel_id):
    buffer = BytesIO()
    qr_for_channel(channel_id).svg(buffer, 6)
    return Response(buffer.getvalue().decode('utf-8'), mimetype='text/xml')


@app.route('/<chid:channel_id>/info', methods=['GET'])
def info(channel_id):
    model.get_channel(channel_id) # Ensure the channel exists.

    return jsonify({
        'channel_page': channel_page_url(channel_id),
        'endpoint': channel_endpoint(channel_id),
    })


@app.route('/<chid:channel_id>', methods=['GET'])
def get_channel(channel_id):
    try:
        channel = model.get_channel(channel_id)
        messages = model.get_messages(channel_id)
        return jsonify({
            'messages': messages,
            'channelId': channel_id,
            'pubKey': VAPID_PUBKEY,
            'subscriptions': list(channel['subscriptions'].keys()),
        })
    except NoSuchChannel as err:
        return jsonify({'error': 'No such channel: {}'.format(err.channel_id)}), 404


@app.route("/<chid:channel_id>", methods=['POST'])
def post_channel(channel_id):
    message = request.get_data(as_text=True)

    parsed = parse_qs(message)
    if 'message' in parsed:
        message = parsed['message'][0]

    data = dict()
    params = dict()
    if 'action' in parsed:
        data = {'action': parsed['action'][0]}
    if 'vibrate' in parsed and parsed['vibrate'] != '0':
        params['vibrate'] = [200, 100, 200]
    if 'silent' in parsed and parsed['silent'] != '0':
        params['silent'] = True

    channel = model.get_channel(channel_id)
    print(channel)
    result = parallel_notify(channel['subscriptions'],
                             message, channel_id, data, **params)
    print('result', result)

    try:
        model.put_message(channel_id, message, data, result)
    except NoSuchChannel as err:
        return jsonify({'error': 'No such channel: {}'.format(err.channel_id)}), 404
    return '{}'


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/c/<chid:channel_id>')
def channel(channel_id):
    return app.send_static_file('channel.html')

def main():
    app.run(threaded=True)


if __name__ == '__main__':
    main()
