#!/bin/sh

source venv/bin/activate

set -a
source .env

python -m notify_run_server.__init__

