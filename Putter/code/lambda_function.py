import json
import boto3
import base64
import sys

import urllib.parse
from PIL import Image
import io
from array import array

s3 = boto3.client('s3')
img_bucket = 'lambda-app-images' 



def lambda_handler(event, context):

    if event['StatusCode'] != 200:
        raise Exception("Error")

    if event['HTTPMethod'] == 'POST' : 
        data = event['body']
        title = data['title']
        img = data['img']
        image_64_decode = base64.decodestring(img) 
        array = bytearray(image_64_decode)
        image = Image.open(io.BytesIO(array))
       
        s3.put_object(Bucket=img_bucket, Key=title, Body=image)
        return {'statusCode': 200, 'body': json.dumps({'message': 'successful image upload'}), 'headers': {'Access-Control-Allow-Origin': '*'}}




