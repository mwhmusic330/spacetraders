!/usr/bin/env bash

    curl --request POST \
     --url 'https://api.spacetraders.io/v2/register' \
     --header 'Content-Type: application/json' \
     --data '{
         "symbol": "noob123456",
         "faction": "COSMIC"
     }' > /tmp/credentials.json

mkdir -p ~/.config/spacetraders

cat /tmp/credentials.json | jq ".data.token" | sed "s/\"//g" > ~/.config/spacetraders/token
