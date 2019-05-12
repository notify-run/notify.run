if [ -f .env ]; then
    echo "Loading .env file."
    set -a
    source .env
else
    echo "No .env found, skipping."
fi

source build.sh
