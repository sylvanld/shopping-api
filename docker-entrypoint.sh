#!/bin/sh

case $1 in
    start)
        uvicorn --host 0.0.0.0 --port 8000 --reload shopping.__main__:api
        ;;
    healthcheck)
        http_status=$(wget --quiet --spider --server-response http://localhost:8000/healthcheck 2>&1 \
            | awk 'NR==1{print $2}')
        if [ "$http_status" = "200" ]; then
            echo "API healthcheck succeeded!";
        else
            echo "API healthcheck failed! Got HTTP $http_status";
            exit 1;
        fi
        ;;
    *)
        echo "Command does not exists: $1"
        ;;
esac
