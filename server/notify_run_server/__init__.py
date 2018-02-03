import os

from datetime import datetime
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from pyqrcode import QRCode
from io import BytesIO
import json

from notify_run_server.model import NotifyModel, NoSuchChannel
from notify_run_server.params import VAPID_PUBKEY, API_SERVER, WEB_SERVER
from notify_run_server.notify import notify

app = Flask(__name__)
CORS(app)

model = NotifyModel()


def channel_page_url(channel_id):
    return WEB_SERVER + '/c/' + channel_id


def channel_endpoint(channel_id):
    return API_SERVER + '/' + channel_id


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


@app.route('/<channel_id>/subscribe', methods=['POST'])
def subscribe(channel_id):
    model.add_subscription(channel_id, request.get_json())
    return '{}'


@app.route('/<channel_id>/qr.svg', methods=['GET'])
def qr(channel_id):
    buffer = BytesIO()
    qr_for_channel(channel_id).svg(buffer, 6)
    return Response(buffer.getvalue().decode('utf-8'), mimetype='text/xml')


@app.route('/<channel_id>/info', methods=['GET'])
def info(channel_id):
    channel = model.get_channel(channel_id)

    return jsonify({
        'channel_page': channel_page_url(channel_id),
        'endpoint': channel_endpoint(channel_id),
    })


@app.route('/<channel_id>', methods=['GET'])
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
    except NoSuchChannel as e:
        return 'no such channel: {}'.format(e.channel_id), 404


@app.route("/<channel_id>", methods=['POST'])
def post_channel(channel_id):
    message = request.get_data().decode('utf-8')
    channel = model.get_channel(channel_id)
    for sub in channel['subscriptions'].values():
        message_json = json.dumps({
            'message': message,
            'channel': channel_id,
        })
        try:
            notify(sub, message_json)
        except:
            pass

    try:
        model.put_message(channel_id, message)
    except NoSuchChannel as e:
        return 'no such channel: {}'.format(e.channel_id), 404
    return '{}'


@app.route("/")
def index():
    return '{}'


if __name__ == '__main__':
    app.run(threaded=True)
