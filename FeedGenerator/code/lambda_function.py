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

client = boto3.client('lambda')
getter_fx_name = 'Getter'
get_all_payload = '{"StatusCode": 200, "command":"list"}'
feed = {}

def lambda_handler(event, context):

    timer = Timer()

    if event['StatusCode'] != 200:
        raise Exception("Something went wrong ...")

    # create feed object from all available items
    if event['num_items'] == 'all':
        response_list = get_file_names_as_list()
        feed = create_feed(response_list=response_list, limit=len(response_list))

    elif event['num_items'] is not None:
        response_list = get_file_names_as_list()
        feed = create_feed(response_list=response_list, limit=event['num_items'])

    else:
        raise Exception('You must provide a num_items argument of either an integer or "all".')

    return_obj = make_return_obj(filename_urls_dict=feed)

    return_obj = timer.add_time_to_return_obj(return_obj, "feed_generator", time_dict)

    if local_test:
        print(return_obj)
    else:
        return return_obj

def make_return_obj(filename_urls_dict:dict):
    return {"StatusCode":200, "feed":filename_urls_dict}

def get_file_names_as_list():
    response = client.invoke(
        FunctionName=getter_fx_name,
        InvocationType='RequestResponse', # syncrhonous
        # InvocationType='Event', # asynchronous
            Payload=get_all_payload
    )
    payload = json.load(response['Payload'])
    ptime = payload['time']
    for identifier, val in ptime.items():
        time_dict[identifier] = val
    return payload['filenames']

def create_feed(response_list:list, limit:int):
    return_dict = {}
    count = 0
    for filename in response_list:
        return_dict[filename] = get_file_url_by_filename(filename=filename)
        count += 1
        if count >= limit:
            break
    return return_dict

def get_file_url_by_filename(filename:str):
    response = client.invoke(
        FunctionName=getter_fx_name,
        InvocationType='RequestResponse',
        Payload=make_get_filename_url_payload(filename=filename)
    )
    payload = json.load(response['Payload'])
    ptime = payload['time']
    for identifier, val in ptime.items():
        time_dict[identifier] = val
    return payload['filename']

def make_get_filename_url_payload(filename:str):
    test = '{"StatusCode":200, "command":"get_file_url", "filename":"' + filename + '"}'
    return test

# call the method if running locally
local_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False
if local_test:
    test_event = {"StatusCode":200,"num_items":"all"}
    # test_event = {"StatusCode":200,"num_items":1}
    test_context = None
    lambda_handler(test_event, test_context)
    # lambda_handler(test_event_limit, test_context)
