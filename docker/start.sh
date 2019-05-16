#!/usr/bin/env bash

set -e
env=${DOCKER_APP_ENV:-local}
postgres=${DB_HOST:-airflow_postgres}
redis=${REDIS_HOST:-airflow_redis}
queue=${WORKER_QUEUE:-default_queue}
cmd=${1:-webserver}

waitForPostgres() {
    echo "+ Waiting until Postgres is ready to accept connections."
	/usr/local/bin/wait-for-it $postgres:5432 -t 60
}

waitForRedis() {
    echo "+ Waiting until Redis is ready to accept connections."
	/usr/local/bin/wait-for-it $redis:6379 -t 60
}

InitDatabase() {
    echo "+ Creating database if it doesn't already exist."
    airflow initdb
}

KeepRunning() {
    while true; do
    sleep 3600
    done
}

echo "+ The run environment is $env."

if [[ "$env" = "local" ]]; then
    waitForPostgres
    waitForRedis

    echo $cmd

    if [[ $cmd == "webserver" ]]; then
        InitDatabase
    fi

    if [[ $cmd == "worker" ]]; then
        airflow worker -q $queue
    else
        echo "+ Starting $cmd..."
        airflow $cmd
    fi
fi