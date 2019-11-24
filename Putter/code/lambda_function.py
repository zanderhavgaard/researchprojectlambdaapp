import json
import boto3
import base64
import sys
import codecs
import urllib.parse
from PIL import Image
import io

s3 = boto3.client('s3')

print('Put function called')    


# def lambda_handler(event, context):
#     print event
#     if event['httpMethod'] == 'POST' : 
#         print event['body']
#         data = json.loads(event['body'])
#         name = data['name']
#         image = data['file']
#         image = image[image.find(",")+1:]
#         dec = base64.b64decode(image + "===")
#         s3.put_object(Bucket='upload-to-s3-project', Key=name, Body=dec)
#         return {'statusCode': 200, 'body': json.dumps({'message': 'successful lambda function call'}), 'headers': {'Access-Control-Allow-Origin': '*'}}


if (len(sys.argv) > 1) and bool(sys.argv[2]):
    image_path = sys.argv[1]
    print(image_path)
    # image_file = Image.open(image_path)
    # # image_file.show() 

    # with open(image_path , "wb") as fh:
    #     fh.write(base64.decodebytes(image_path))
    #     print("test")
    #     print(fh)

    data = {}
    with open(image_path, mode='rb') as file:
        img = file.read()
        print(type(img))
    data['img'] = base64.b64encode(img)
    print(type(data['img']))

    print(data['img'])
    val = base64.b64decode(data['img'])
    print(type(val))
    image = Image.open(io.BytesIO(val))
    image.show() 
    
    # data = image_file.read()
    # print (data.encode("base64"))
    # json_object = {'httpMethod':'POST','body':json.dumps('image': image)}
    # lambda_handler(event=json_object, context='foo')







# sys.path.append("/home/zander/Dropbox/ITU/Master/3_semester/rp/code")

# debug = True

# if debug:
#     import gen_json_from_image

# json_obj = gen_json_from_image.gen_json_from_image_file('../../random.png')
# print('starting Put function')

# bucket_name = 'lambda-app-images'
# s3 = boto3.client('s3')

# def lambda_handler(event, context):

#     event = json.loads(event)

#     # print(event)
#     # print(event['httpMethod'])
#     # print(event['body']['name'])

#     if event['httpMethod'] == 'POST':

#         # print(event['body'])

#         data = event['body']
#         name = data['name']
#         image = data['file']

#         # print(image)
#         # image = image[image.find(",")+1:]

#         # print(image)
#         # dec = base64.b64decode(image)

#         # print(dec)


#         decoded_str = str(base64.b64decode(image),'utf-8')

#         print(type(decoded_str))

#         with open("randomer.png","w") as file:
#             file.write(decoded_str)


#         # s3.put_object(Bucket=bucket_name, Key=name, Body=dec)

#         # return {
#         #     'statusCode': 200,
#         #     'body': json.dumps({
#         #         'message': 'successful lambda function call'
#         #     }),
#         #     'headers': {
#         #         'Access-Control-Allow-Origin': '*'
#         #     }}

# if debug:
#     lambda_handler(event=json_obj, context="foo")
