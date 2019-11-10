#!/bin/bash

set -e

fn="FeedGenerator"

cd code
zip "$fn.zip" *
cd ..
mv "code/$fn.zip" .

aws lambda update-function-code \
    --function-name "$fn" \
    --zip-file "fileb://$fn.zip"

rm "$fn.zip"
