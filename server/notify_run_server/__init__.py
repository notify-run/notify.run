import os

from datetime import datetime
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from pyqrcode import QRCode
from io import BytesIO

from notify_run_server.model import NotifyModel, NoSuchChannel
from notify_run_server.params import VAPID_PUBKEY, URL_BASE
from notify_run_server.notify import notify

app = Flask(__name__)
CORS(app)

model = NotifyModel()


@app.route('/api/pubkey', methods=['GET'])
def get_pubkey():
    return jsonify({'pubKey': VAPID_PUBKEY})


@app.route('/api/register_channel', methods=['POST'])
def register_channel():
    channelId = model.register_channel({
        'ip': request.remote_addr,
        'agent': request.headers.get('User-Agent')
    })
    return jsonify({'channelId': channelId, 'pubKey': VAPID_PUBKEY})


@app.route('/<channel_id>/subscribe', methods=['POST'])
def subscribe(channel_id):
    model.add_subscription(channel_id, request.get_json())
    return '{}'


@app.route('/<channel_id>/qr.svg', methods=['GET'])
def qr(channel_id):
    buffer = BytesIO()
    QRCode(URL_BASE + '/c/' + channel_id).svg(buffer, 6)
    return Response(buffer.getvalue().decode('utf-8'), mimetype='text/xml')


@app.route('/<channel_id>', methods=['GET'])
def get_channel(channel_id):
    try:
        return jsonify(model.get_messages(channel_id))
    except NoSuchChannel as e:
        return 'no such channel: {}'.format(e.channel_id), 404


@app.route("/<channel_id>", methods=['POST'])
def post_channel(channel_id):
    message = request.get_data().decode('utf-8')
    channel = model.get_channel(channel_id)
    for sub in channel['subscriptions']:
        print(sub)
        notify(sub, message)

    try:
        model.put_message(channel_id, message)
    except NoSuchChannel as e:
        return 'no such channel: {}'.format(e.channel_id), 404
    return '{}'


@app.route("/")
def index():
    return '{}'
