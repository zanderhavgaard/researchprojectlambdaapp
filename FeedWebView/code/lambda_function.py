import sys
import jinja2
import json


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

    content_dict = parse_feed_json(event)

    html = fill_html_template(html_template, content_dict)

    if local_test:
        print(build_return(html))
    else:
        return build_return(html)


def parse_feed_json(feed_json):
    if local_test:
        feed_json_dict = json.loads(feed_json)
    else:
        feed_json_dict = feed_json
    feed_dict = {}
    if feed_json_dict["StatusCode"] == 200:
        for file_name, file_path in feed_json_dict["feed"].items():
            feed_dict[file_name] = file_path
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


# >>>>> testing <<<<<

local_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False

if local_test:
    test_dict = {
        "file_one.png": "https://via.placeholder.com/150",
        "file_two.png": "https://via.placeholder.com/250",
        "file_thre.png": "https://via.placeholder.com/350"
    }
    test_json = """
{
    "StatusCode": 200,
    "feed": {
        "file_one.png": "https://via.placeholder.com/150",
        "file_two.png": "https://via.placeholder.com/250",
        "file_thre.png": "https://via.placeholder.com/350"
    }
}
"""
    # test_event = json.dumps(test_json)
    test_event = test_json
    test_context = None
    lambda_handler(test_event, test_context)
