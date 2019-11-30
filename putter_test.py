import sys
import base64
import json
import requests
import os

url = os.environ['aws_api_gateway'] + '/live/putter'
token = os.environ['aws_api_key']

print('Testing put function')
image_path = sys.argv[1]
file_name = sys.argv[2]
print('image path:',image_path)

with open(image_path, mode='rb') as file:
    img = file.read()
    image_64_encode = base64.encodebytes(img).decode("utf-8")

    json_object = {
        "HTTPMethod":"POST",
        "StatusCode":200,
        "body": {
            "title":file_name,
            "img":image_64_encode
        }
    }

    data = json.dumps(json_object)

    headers = {'x-api-key':token, 'Content-Type':'application/json'}

    response = requests.post(url, data=data,headers=headers)

    print(response.status_code)

    print(response.text)
    # h = response.headers
    # print(type(response))


    # response_json = response.json()

    # keys = list(response_json.keys())

    # for i in h:
    #     print(i)
    #     print(h[i])

    # print('StatusCode:',response.status_code,'message:',response_json['message'])
    # print(response.status_code,response.text)
