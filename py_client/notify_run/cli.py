import argparse

from notify_run import Notify


def configure(notify, force):
    if notify.config_file_exists and not force:
        print(
            'Overwrite existing configuration ({})? [y/N]'.format(notify.endpoint))
        if input().lower() != 'y':
            return
    notify.write_config()


def info(notify):
    notify.info()


def register(notify, force):
    print('register')


def send(notify, message):
    notify.send(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-server', '-a')

    subparsers = parser.add_subparsers()

    # "send" command: send a message
    notify_parser = subparsers.add_parser('send')
    notify_parser.add_argument('message')
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
    func = args.pop('func')
    api_server = args.pop('api_server')
    notify = Notify(api_server, endpoint)
    func(notify, **args)
