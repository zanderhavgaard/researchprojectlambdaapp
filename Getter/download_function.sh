#!/bin/bash

set -e

fn="Getter"

url=$(aws lambda get-function --function-name $fn --query 'Code.Location')

wget -O "$fn.zip" "$url"

unzip "$fn.zip"

rm "$fn.zip"
