
import sys
import base64
import json
import requests

url = "https://42u1uyqaj4.execute-api.eu-central-1.amazonaws.com/live/putter"
token = "CmUJkL6EJr9TOiaBNJdmh1BYlKc0VS54a1GHrXFo"

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

    # print(response.status_code,response.text)
   
    
  


