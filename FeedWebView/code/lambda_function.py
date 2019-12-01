import sys
import jinja2
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
    def add_time_to_return_obj(self, return_dict, identifier, time_dict=None):
        # if the time key is not present
        if 'time' not in return_dict.keys():
            return_dict['time'] = {}

        # if we have saved some timings from other lambda invocations
        if time_dict is not None:
            for key, val in time_dict.items():
                return_dict['time'][key] = val

        # add new timing
        exe_time = self.__exit__()
        return_dict['time'][identifier] = {'exe_time': exe_time}

        return return_dict

time_dict = {}

client = boto3.client('lambda')

html_template = """
<html>
  <head>
    <title>feed_web_view</title>
  </head>
  <body>
    <h1>hello world</h1>
    {% for file_name, file_path in content.items() %}
      <h2>{{ file_name }}</h2>
      <img src="{{ file_path }}">
    {% endfor %}
  </body>
</html>
"""


def lambda_handler(event, context):

    timer = Timer()

    if event is not None:
        if event['StatusCode'] != 200:
            raise Exception("Something went wrong ...")
        num_items = event['num_items']
    else:
        num_items = "all"

    feed_json = get_feed(num_items)

    content_dict = parse_feed_json(feed_json)

    html = fill_html_template(html_template, content_dict)

    return_obj = build_return(html)

    identifier = 'Feed-WebView'
    return_obj = timer.add_time_to_return_obj(return_obj, identifier, time_dict)
    # add metadata to return_obj
    return_obj['identifier'] = identifier
    if context is not None:
        return_obj['memory'] = context.memory_limit_in_mb

    if local_test:
        print(return_obj)
    else:
        return return_obj


def parse_feed_json(feed_json_dict):
    feed_dict = {}
    if feed_json_dict["StatusCode"] == 200:
        for file_name, file_path in feed_json_dict["feed"].items():
            feed_dict[file_name] = file_path
    else:
        print("Error parsing response ...")
    return feed_dict


def fill_html_template(template, content_dict):
    html_template = jinja2.Template(template)
    return html_template.render(content=content_dict)


def build_return(html):
    return {
        "StatusCode": 200,
        "body": html,
        "headers": {
            "Content-Type": "text/html",
        }
    }

feed_generator_fx = "FeedGenerator"
feed_generator_payload = '{"StatusCode":200, "num_items":"all"}'

def create_feed_gen_payload(num_items):
    if num_items == "all":
        return '{"StatusCode":200, "num_items":"all"}'
    else:
        return '{"StatusCode":200, "num_items":' + str(num_items) + '}'

def get_feed(num_items):
    # response = client.invoke(
    #     FunctionName=feed_generator_fx,
    #     InvocationType='RequestResponse',
    #     Payload=create_feed_gen_payload(num_items)
    # )
    # payload = json.load(response['Payload'])
    # ptime = payload['time']
    # for identifier, val in ptime.items():
    #     time_dict[identifier] = val

    payload = invoke_lambda(lambda_name=feed_generator_fx, invoke_payload=create_feed_gen_payload(num_items))
    return payload

def invoke_lambda(lambda_name, invoke_payload):
    total_time = Timer()
    response = client.invoke(
        FunctionName=lambda_name,
        InvocationType='RequestResponse', # syncrhonous
        # InvocationType='Event', # asynchronous
        Payload=invoke_payload
    )
    total_time = total_time.__exit__()

    payload = json.load(response['Payload'])

    ptime = payload['time']

    for identifier, val in ptime.items():
        time_dict[identifier] = val

    latency = total_time - payload['time'][payload['identifier']]['exe_time']

    time_dict[payload['identifier']]['total_time'] = total_time
    time_dict[payload['identifier']]['latency'] = latency
    time_dict[payload['identifier']]['memory'] = payload['memory']

    return payload

# >>>>> testing <<<<<

test_dict = {
    "StatusCode": 200,
    "feed": {
        "file_one.png": "https://via.placeholder.com/150",
        "file_two.png": "https://via.placeholder.com/250",
        "file_thre.png": "https://via.placeholder.com/350"
    }
}

# call the method if running locally
local_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False
if local_test:
    # test_event = {"StatusCode":200, "num_items":"all"}
    # test_event = {"StatusCode":200, "num_items":1}
    test_event = None
    test_context = None
    lambda_handler(test_event, test_context)
