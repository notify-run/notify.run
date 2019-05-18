Self-hosting `Notify.run <https://notify.run/>`__ (BETA)
========================================================

Introduction
------------

In addition to using the public `notify.run <https://notify.run/>`__ server, it is possible to host your own.

Quick Start
-----------

::

    pip install notify-run-server
    notify-run-server

Once the server is running, you can visit `localhost:5000 <http://localhost:5000>`_ to access a local version of notify.run.

Configuration
-------------

All configuration of ``notify-run-server`` is done through setting environment variables.

Database
~~~~~~~~

``notify-run-server`` needs a database backend to store subscription information and notification history. By default, it uses a sqlite database called ``notify.sqlite`` in the current working directory. All database access happens through `SQLAlchemy <https://www.sqlalchemy.org/>`_, so it is possible to replace sqlite with another supported backend like MySQL or Postgres. Note, however, that not all backends support the JSON field type, which is required by ``notify-run-server``.

To configure the database, set the environment variable ``NOTIFY_DB_URL`` to a URI that conforms to `SQLAlchemy’s URL schema <https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls>`_. The server will create the required tables the first time it connects to the database.

Alternatively, ``notify-run-server`` can use Amazon DynamoDB as a backend. This is used for the main production deployment, `notify.run <https://notify.run>`__. To use this option, create two DynamoDB tables for channels and messages (see `serverless.yml <https://github.com/paulgb/notify.run/blob/master/deployment/serverless.yml>`_ for the schema). Then set up the Python ``boto`` package with your AWS credentials and set the ``NOTIFY_DB_URL`` with the format ``dynamodb:<message_table_name>:<channel_table_name>``.

Server URL
~~~~~~~~~~

By default, ``notify-run-server`` assumes that it is running at the hostname given in the HTTP request. This breaks if it is running behind a reverse proxy or similar setup. In these cases, you can set the environment variable ``NOTIFY_WEB_SERVER`` to the root URL of the server, e.g. ``https://notify.run/``.

VAPID Configuration
~~~~~~~~~~~~~~~~~~~

The web push protocol used by `notify.run <http://notify.run>`__ uses public key encryption to authenticate subscriptions. ``notify-run-server`` includes a built-in key pair that is fine for personal use, but for public instances you should generate your own key pair (e.g. using `this tool <https://github.com/web-push-libs/web-push#command-line>`_) and pass them to ``notify-run-server`` with the ``NOTIFY_VAPID_PRIVKEY`` and ``NOTIFY_VAPID_PUBKEY`` environment variables, for the private and public keys, respectively.
