import sys
import jinja2
import json
import boto3

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

    # TODO get from feedGenerator
    # feed_json = test_dict
    feed_json = get_feed()

    content_dict = parse_feed_json(feed_json)

    html = fill_html_template(html_template, content_dict)

    response = build_return(html)

    if local_test:
        print(response)
    else:
        return response


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

def get_feed():
    response = client.invoke(
        FunctionName=feed_generator_fx,
        InvocationType='RequestResponse',
        Payload=feed_generator_payload
    )
    return json.load(response['Payload'])

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
    test_event = None
    test_context = None
    lambda_handler(test_event, test_context)
