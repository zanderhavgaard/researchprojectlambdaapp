import sys
import json
import boto3

client = boto3.client('lambda')
getter_fx_name = 'Getter'
get_all_payload = '{"StatusCode": 200, "command":"list"}'
feed = {}

def lambda_handler(event, context):

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
        return json.load(response['Payload'])['filenames']

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
   return json.load(response['Payload'])

def make_get_filename_url_payload(filename:str):
    test = '{"StatusCode":200, "command":"get_file_url", "filename":"' + filename + '"}'
    return test

# call the method if running locally
local_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False
if local_test:
    test_event = {"StatusCode":200,"num_items":"all"}
    # test_event_limit = {"StatusCode":200,"num_items":2}
    test_context = None
    lambda_handler(test_event, test_context)
    # lambda_handler(test_event_limit, test_context)
