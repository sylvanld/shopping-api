#!/bin/sh

case $1 in
    start)
        uvicorn --host 0.0.0.0 --port 8000 --reload --factory shopping.api.factory:create_api
        ;;
    *)
        echo "Command does not exists: $1"
        ;;
esac
