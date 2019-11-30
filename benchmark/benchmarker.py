#!/bin/python

import os
import time
import json
import requests

# aux class for handling timing of things
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

    def request_feed_generator(self, num_items='all'):
       url = self.url_prefix + '/feed-generator'
       data = {'StatusCode':200, 'num_items':num_items}
       response = requests.get(url=url, data=json.dumps(data), headers=self.auth_header)
       return response

    def request_feed_webview(self, num_items='all'):
        url = self.url_prefix + '/feed'
        data = {'StatusCode':200, 'num_items':num_items}
        response = requests.get(url=url, data=json.dumps(data), headers=self.auth_header)
        return response

    def test_methods(self):

        print('\n\tTesting Getter\n')
        getter_list = self.request_getter(command='list')
        print('getter - list', getter_list.text)
        getter_file_url = self.request_getter(command='get_file_url',filename='green.png')
        print('getter - file_url', getter_file_url.text)

        # test putter?
        # TODO ?

        print('\n\tTesting FeedGenerator\n')
        feed_generator_all = self.request_feed_generator()
        print('feed_generator - all', feed_generator_all.text)
        feed_generator_2 = self.request_feed_generator(num_items=2)
        print('feed_generator - 2', feed_generator_2.text)

        print('\n\tTesting FeedWebView\n')
        feed_all = self.request_feed_webview()
        print('feed - all', feed_all.text)
        feed_2 = self.request_feed_webview(num_items=2)
        print('feed - 2', feed_2.text)


    def benchmark(self):
        print('api_key:', self.api_key)
        print('api_gateway:', self.api_gateway)



# ==============================
# >>>>> run the benchmarks <<<<<

benchmarker = Benchmarker()

# test that methods work...
# benchmarker.test_methods()

# run benchmarks!
benchmarker.benchmark()
