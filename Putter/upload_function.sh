#!/bin/bash

fn="Putter"

cd code
zip "$fn.zip" *
cd ..
mv "code/$fn.zip" .

aws lambda update-function-code \
    --function-name "$fn" \
    --zip-file "fileb://$fn.zip"

rm "$fn.zip"
