import argparse

import requests

from notify_run import Notify, NotConfigured


def check_existing(notify, force):
    if notify.config_file_exists and not force:
        print(
            'Overwrite existing configuration ({})? [y/N]'.format(notify.endpoint))

        try:
            # Python 2.x
            input_fn = raw_input
        except NameError:
            input_fn = input

        return input_fn().lower() == 'y'
    return True


def configure(notify, force):
    if check_existing(notify, force):
        notify.write_config()


def info(notify):
    print(notify.info())


def register(notify, force):
    if check_existing(notify, force):
        print(notify.register())


def send(notify, message, action):
    notify.send(message, action)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-server', '-a')

    subparsers = parser.add_subparsers()

    # "send" command: send a message
    notify_parser = subparsers.add_parser('send')
    notify_parser.add_argument('message',
                               help='The message text to be sent.')
    notify_parser.add_argument('--action', '-a', default=None,
                               help='An optional URL to open if the notification is clicked.')
    notify_parser.add_argument('--endpoint', '-e')
    notify_parser.set_defaults(func=send)

    # "configure" command: configure to an existing endpoint
    conf_parser = subparsers.add_parser('configure')
    conf_parser.add_argument('endpoint')
    conf_parser.add_argument('--force', '-f', action='store_true')
    conf_parser.set_defaults(func=configure)

    # "info" command: get information for subscribing to an endpoint
    info_parser = subparsers.add_parser('info')
    info_parser.add_argument('--endpoint', '-e')
    info_parser.set_defaults(func=info)

    # "register" command: register a new endpoint
    register_parser = subparsers.add_parser('register')
    register_parser.add_argument('--force', '-f', action='store_true')
    register_parser.set_defaults(func=register)

    args = vars(parser.parse_args())
    endpoint = None
    if 'endpoint' in args:
        endpoint = args.pop('endpoint')
    if 'func' in args:
        func = args.pop('func')
    else:
        parser.print_usage()
        return
    api_server = args.pop('api_server')

    try:
        notify = Notify(api_server, endpoint)
        func(notify, **args)
    except NotConfigured:
        print('Run "notify-run register" or "notify-run configure <endpoint>" first.')
    except ValueError as ve:
        print(ve)
    except requests.exceptions.ConnectionError as ce:
        print('Error connecting. Check configuration and internet connection.')
        print(ce)
