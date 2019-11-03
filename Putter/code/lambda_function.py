import json
import urllib.parse
import boto3
import base64
import sys
import codecs
sys.path.append("/home/zander/Dropbox/ITU/Master/3_semester/rp/code")

debug = True

if debug:
    import gen_json_from_image

json_obj = gen_json_from_image.gen_json_from_image_file('../../random.png')
print('starting Put function')

bucket_name = 'lambda-app-images'
s3 = boto3.client('s3')

def lambda_handler(event, context):

    event = json.loads(event)

    # print(event)
    # print(event['httpMethod'])
    # print(event['body']['name'])

    if event['httpMethod'] == 'POST':

        # print(event['body'])

        data = event['body']
        name = data['name']
        image = data['file']

        # print(image)
        # image = image[image.find(",")+1:]

        # print(image)
        # dec = base64.b64decode(image)

        # print(dec)


        decoded_str = str(base64.b64decode(image),'utf-8')

        print(type(decoded_str))

        with open("randomer.png","w") as file:
            file.write(decoded_str)


        # s3.put_object(Bucket=bucket_name, Key=name, Body=dec)

        # return {
        #     'statusCode': 200,
        #     'body': json.dumps({
        #         'message': 'successful lambda function call'
        #     }),
        #     'headers': {
        #         'Access-Control-Allow-Origin': '*'
        #     }}

if debug:
    lambda_handler(event=json_obj, context="foo")
