from os import environ
from os.path import expanduser
import json
from urllib.parse import urlparse
import requests
from pyqrcode import QRCode

DEFAULT_API_SERVER = 'https://notify.run/api/'
CONFIG_FILENAME = '~/.notify-run'


class Notify:
    def read_config(self):
        self.config_file_exists = False
        try:
            with open(self._config_file, 'r') as conffile:
                self.config_file_exists = True
                config = json.load(conffile)
                self.endpoint = config['endpoint']
        except FileNotFoundError:
            return
        except json.decoder.JSONDecodeError:
            print('Invalid JSON in {}'.format(self._config_file))
            return

    def __init__(self, api_server=None, endpoint=None):
        self.api_server = api_server or DEFAULT_API_SERVER
        self._config_file = expanduser(CONFIG_FILENAME)

        self.read_config()

        if endpoint is not None:
            parse_result = urlparse(endpoint)
            if parse_result.scheme not in ['http', 'https']:
                print('Endpoint should be a URL with an HTTP or HTTPS scheme (scheme was {}.)'.format(
                    parse_result.scheme))
            self.endpoint = endpoint

    def send(self, message):
        assert self.endpoint is not None
        requests.post(self.endpoint, message)

    def info(self):
        r = requests.get(self.endpoint + '/info').json()
        self.print_info(r)

    def print_info(self, r):
        print('Endpoint: {}'.format(self.endpoint))
        print('To subscribe, open: {}'.format(r['channel_page']))
        print('Or scan this QR code')
        print(QRCode(r['channel_page'], error='L').terminal(quiet_zone=1))

    def write_config(self):
        config = {
            'endpoint': self.endpoint,
        }
        try:
            with open(self._config_file, 'w') as conffile:
                json.dump(config, conffile)
        except Exception:
            raise

    def register(self):
        r = requests.post(self.api_server + 'register_channel').json()
        self.endpoint = r['endpoint']
        self.write_config()
        self.print_info(r)
