import sys
import json
import boto3
import time

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
    def add_time_to_return_obj(self, return_dict, identifyer, time_dict=None):
        if 'time' not in return_dict.keys():
            return_dict['time'] = {}
        if time_dict is not None:
            for identifier, val in time_dict.items():
                return_dict['time'][identifier] = val
        return_dict['time'][identifyer] = self.__exit__()
        return return_dict

time_dict = {}

s3 = boto3.client('s3')
img_bucket = 'lambda-app-images'
img_url_prefix = 'https://lambda-app-images.s3.amazonaws.com/live/'

def lambda_handler(event, context):

    # start timer
    timer = Timer()

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
            file_names.append(item['Key'][5:])

        # create return json
        return_obj = make_return_dict_list(file_names=file_names)

        identifyer = "Getter_list"

    # should return an absolute url for the file with the filename
    elif command == 'get_file_url':

        if event['filename'] == None:
            raise Exception("No filename provided.")

        # create string of absolute url
        return_obj = make_return_dict_filename(img_url_prefix + event['filename'])

        identifyer = "Getter_" + event['filename']

    return_obj = timer.add_time_to_return_obj(return_obj, identifyer)

    if local_test:
        print(return_obj)
    else:
        return return_obj

def make_return_dict_list(file_names:list):
    return {
        "StatusCode": 200,
        "filenames": file_names
    }

def make_return_dict_filename(url:str):
    return {
        "StatusCode":200,
        "filename":url
    }

# call the method if running locally
local_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False
if local_test:
    # test_event = {"StatusCode":200, "command":"list"}
    test_event = {"StatusCode":200,
                  "command":"get_file_url",
                  "filename":"green.png"}
    test_context = None
    lambda_handler(test_event, test_context)
