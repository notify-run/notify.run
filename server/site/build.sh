#!/bin/sh

cd "$(dirname "$0")"
set -e

echo "Installing environment."
npm install

if [ -f .env ]; then
    echo "Loading .env file."
    set -a
    source .env
else
    echo "No .env found, skipping."
fi

echo "Bundling site."
./node_modules/.bin/webpack --display-error-details

echo "Merging with static files."
mkdir -p public/
cp -R dist/* static/* public/

