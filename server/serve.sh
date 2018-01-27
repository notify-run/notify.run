#!/bin/sh

source venv/bin/activate

set -a
source .env

flask run
