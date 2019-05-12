#!/bin/sh

set -a
source .env

./build.sh
./node_modules/.bin/webpack-dev-server
