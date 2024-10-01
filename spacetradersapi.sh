#!/usr/bin/env bash

token="$(head -1 "$HOME/.config/spacetraders/token")"
base_url=https://api.spacetraders.io/v2
endpoint='my/agent'
curl "$base_url/$endpoint" \
    --header "Authorization: Bearer $token" > /tmp/agent.json
system_symbol=$(cat /tmp/agent.json | jq ".data.headquarters" | sed "s/\"//g" | awk -F "-" '{out=$1"-"$2; print out}')
waypoint_symbol=$(cat /tmp/agent.json | jq ".data.headquarters" | sed "s/\"//g") 

endpoint="systems/$system_symbol/waypoints/$waypoint_symbol"

curl "$base_url/$endpoint" \
    --header "Authorization: Bearer $token" 

# endpoint='systems/'

# curl "$base_url/"

