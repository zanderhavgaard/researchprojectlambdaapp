import json
from flask import Flask

# def lambda_handler(event, context):
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
    app.run()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello world"

if __name__ == '__main__':
    app.run()
