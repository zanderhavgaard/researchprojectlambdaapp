import json
import boto3
import base64
import sys

import urllib.parse
from PIL import Image
import io
from array import array
import time

s3 = boto3.client('s3')
img_bucket = 'lambda-app-images' 

class Timer:

    def __init__(self):
        # get current time
        self.start_time = time.time()
        self.end_time:int

    def __exit__(self):
        # get end time
        self.end_time = time.time()
        # return time diff
        return self.end_time - self.start_time

    # add time to a return obj
    def add_time_to_return_obj(self, return_dict, identifyer):
        if 'time' not in return_dict.keys():
            return_dict['time'] = {}
        return_dict['time'][identifyer] = self.__exit__()
        return return_dict

time_dict = {}

def lambda_handler(event, context):

    # start timer
    timer = Timer()

    if event['StatusCode'] != 200:
        raise Exception("Error")

    if event['HTTPMethod'] == 'POST' : 
        data = event['body']
        title = data['title']
        img = data['img']

        # decode image file from JSON
        image_64_decode = base64.b64decode(img)
        # crete image object for S3
        pil_image = Image.open(io.BytesIO(image_64_decode))
        in_mem_file = io.BytesIO()
        pil_image.save(in_mem_file, format=pil_image.format)
        in_mem_file.seek(0)
        # add prefix to locate correct folder in bucket
        file_name = "live/"+ title+".png"

        # upload image file and return new JSON file with metadata and time messurements    
        s3.upload_fileobj(in_mem_file, img_bucket, file_name)
        
        identifyer = "Putter-" + title 
        return_obj = {'statusCode': 200, 'body': {'message': title}, 'headers': {'Access-Control-Allow-Origin': '*'}}
        return_obj = timer.add_time_to_return_obj(return_obj, identifyer)
        
        return return_obj



