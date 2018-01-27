#!/bin/sh

source venv/bin/activate

set -a
source .env

export FLASK_APP=notify_run_server/__init__.py
flask run
