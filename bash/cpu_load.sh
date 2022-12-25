#!/bin/bash
DEFAULT_HOST=127.0.0.1
DEFAULT_PORT=8001

while getopts h:p: option
do 
    case "${option}"
        in
        h)HOST=${OPTARG};;
        p)PORT=${OPTARG};;
    esac
done

CLIENT_NAME=$(hostname)
CLIENT_IP=$(hostname -i | awk '{print $1}')

while :; do
    CLIENT_CPU=$(top -bn2 | grep -i 'Cpu(s)' | tail -1 | sed "s/.*, *\([0-9]*[.|,][0-9]\)[%| ]id.*/\1/" | sed "s/,/./" | awk '{print 100-$1}')

    CLIENT_INFO="{\"name\" : \"$CLIENT_NAME\", \"ip\" : \"$CLIENT_IP\", \"load\" : \"$CLIENT_CPU\"}"
    curl -H "Content-Type: application/json" --request POST --data "$CLIENT_INFO" http://${HOST:-$DEFAULT_HOST}:${PORT:-$DEFAULT_PORT}/api/v1/clients/cpu_load/
    
    sleep 10
done
