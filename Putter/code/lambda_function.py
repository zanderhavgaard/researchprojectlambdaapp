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
        
        image_64_decode = base64.b64decode(img)
        pil_image = Image.open(io.BytesIO(image_64_decode))
        in_mem_file = io.BytesIO()
        pil_image.save(in_mem_file, format=pil_image.format)
        in_mem_file.seek(0)
        file_name = "live/"+ title+".png"

       
        s3.upload_fileobj(in_mem_file, img_bucket, file_name)
        return {'statusCode': 200, 'body': json.dumps({'message': title}), 'headers': {'Access-Control-Allow-Origin': '*'}}




