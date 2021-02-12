#!/bin/bash
set -Ceu

function logger() {
    case ${1} in
        ERROR)
            color=31
        ;;
        WARN)
            color=33
        ;;
        INFO)
            color=32
        ;;
        *)
            color=37
        ;;
    esac
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') \e[${color}m$1\e[m ${@:2}"
}

function main() {
    logger INFO "Docker-composeを停止します"
    docker-compose down
    if [ $# -eq 0 ]; then
        docker-compose up -d
    else
        if [ "${1}" = "build" ]; then
            docker-compose up --build -d
        fi
    fi
    logger INFO "Docker-composeは起動しました"
    docker-compose exec node bash
}

main $@

