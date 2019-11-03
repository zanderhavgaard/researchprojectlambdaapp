#!/bin/bash

mkdir code

set -e

fn="FeedWebView"

url=$(aws lambda get-function --function-name $fn --query 'Code.Location' | jq -r)

wget -O "$fn.zip" "$url"

unzip "$fn.zip" -d code

rm "$fn.zip"
