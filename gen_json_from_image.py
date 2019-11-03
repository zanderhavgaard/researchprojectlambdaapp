import sys
import base64
import json

def gen_json_from_image_file(file_name:str):

    # file_name = sys.argv[1]

    with open(file_name, "rb") as file:
        read_stuff = str(file.read())
        encoded = base64.b64encode(read_stuff.encode('utf-8'))
        encoded_image = str(encoded,'utf-8')

    json_dict = {
        "httpMethod": "POST",
        "body": {
            "name": file_name,
            "file": encoded_image
        }
    }

    json_obj = json.dumps(json_dict)

    return json_obj

    # print(json_obj)
