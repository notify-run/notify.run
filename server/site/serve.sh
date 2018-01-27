#!/bin/sh

set -a
source .env

./node_modules/.bin/webpack-dev-server
