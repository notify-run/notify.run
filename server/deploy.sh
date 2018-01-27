#!/bin/sh

set -a
source .env.prod

sls deploy

