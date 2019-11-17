import sys
import json
import boto3

img_bucket = 'lambda-app-images'
s3 = boto3.client('s3')
img_url_prefix = 'https://lambda-app-images.s3.amazonaws.com/live/'

def lambda_handler(event, context):

    if event['StatusCode'] != 200:
        raise Exception("Something went wrong ...")

    command = event['command']

    # should list all avilable files, and return a list of filenames
    if command == 'list':

        # get data from bucket
        bucket_contents = s3.list_objects_v2(Bucket=img_bucket)

        file_names = []

        # create dict of filename:url
        for item in bucket_contents['Contents']:
            # filter out directory keys
            if item['Key'].endswith('/'):
                continue
            file_names.append(item['Key'])

        # create return json
        return_obj = make_return_dict(file_names=file_names)

    # should return an absolute url for the file with the filename
    elif command == 'get_file_url':

        if event['filename'] == None:
            raise Exception("No filename provided.")

        # create string of absolute url
        return_obj = img_url_prefix + event['filename']

    if local_test:
        print(return_obj)
    else:
        return return_obj

def make_return_dict(file_names:list):
    return {
        "StatusCode": 200,
        "feed": file_names
    }


# call the method if running locally
local_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False
if local_test:
    test_event = None
    test_context = None
    lambda_handler(test_event, test_context)
