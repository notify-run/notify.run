#!/bin/sh

source activate notify

set -a
source .env

python -m notify_run_server.app

