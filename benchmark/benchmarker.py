#!/bin/python

import os
import time
import json
import requests

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

class Benchmarker:

    def __init__(self):
        self.api_key = os.environ['aws_api_key']
        self.api_gateway = os.environ['aws_api_gateway']
        self.url_prefix = self.api_gateway + '/live'
        self.auth_header = {'x-api-key':self.api_key, 'Content-Type':'application/json'}

    def benchmark(self):
        print('api_key:', self.api_key)
        print('api_gateway:', self.api_gateway)

    def request_getter(self, command, filename=''):
        url = self.url_prefix + '/getter'
        data = {'StatusCode': 200, 'command': command}
        if filename is not '':
            data['filename'] = filename
        response = requests.get(url=url, data=json.dumps(data), headers=self.auth_header)
        return response

    def request_putter(self):
        # TODO @Thomas
        raise NotImplementedError()

benchmarker = Benchmarker()
# benchmarker.benchmark()
print(benchmarker.request_getter(command='list').text)
print(benchmarker.request_getter(command='get_file_url',filename='green.png').text)
