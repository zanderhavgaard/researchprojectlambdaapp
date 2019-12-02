#!/bin/python

import os
import time
import json
import requests
from timer import Timer
from test_data import TestData
from timing import Timing
from sql_interface import SQL_Interface

class Benchmarker:

    def __init__(self):
        self.api_key = os.environ['aws_api_key']
        self.api_gateway = os.environ['aws_api_gateway']
        self.url_prefix = self.api_gateway + '/live'
        self.auth_header = {'x-api-key':self.api_key, 'Content-Type':'application/json'}

    def insert_timing_for_called_lambda(self, resp, total_time:float):
        resp = resp.json()
        identifier = resp['identifier']
        memory = resp['memory']
        latency = total_time - resp['time'][identifier]['exe_time']
        resp['time'][identifier]['latency'] = latency
        resp['time'][identifier]['total_time'] = total_time
        resp['time'][identifier]['memory'] = memory
        resp.pop('memory', None)
        return resp

    def request_getter(self, command, filename=''):
        url = self.url_prefix + '/getter'
        data = {'StatusCode': 200, 'command': command}
        if filename is not '':
            data['filename'] = filename
        total_time = Timer()
        response = requests.get(url=url, data=json.dumps(data), headers=self.auth_header)
        total_time = total_time.__exit__()
        response_dict = self.insert_timing_for_called_lambda(resp=response, total_time=total_time)
        return TestData(complete_json=response_dict)

    def request_putter(self):
        # TODO @Thomas
        raise NotImplementedError()

    def request_feed_generator(self, num_items='all'):
       url = self.url_prefix + '/feed-generator'
       data = {'StatusCode':200, 'num_items':num_items}
       total_time = Timer()
       response = requests.get(url=url, data=json.dumps(data), headers=self.auth_header)
       total_time = total_time.__exit__()
       response_dict = self.insert_timing_for_called_lambda(resp=response, total_time=total_time)
       return TestData(complete_json=response_dict)

    def request_feed_webview(self, num_items='all'):
        url = self.url_prefix + '/feed'
        data = {'StatusCode':200, 'num_items':num_items}
        total_time = Timer()
        response = requests.get(url=url, data=json.dumps(data), headers=self.auth_header)
        total_time = total_time.__exit__()
        response_dict = self.insert_timing_for_called_lambda(resp=response, total_time=total_time)
        return TestData(complete_json=response_dict)

    def test_methods(self):

        print('\n\tTesting Getter\n')
        getter_list = self.request_getter(command='list')
        print('getter - list', getter_list)
        getter_file_url = self.request_getter(command='get_file_url',filename='green.png')
        print('getter - file_url', getter_file_url)

        # test putter?
        # TODO ?

        print('\n\tTesting FeedGenerator\n')
        feed_generator_all = self.request_feed_generator()
        print('feed_generator - all', feed_generator_all)
        feed_generator_2 = self.request_feed_generator(num_items=2)
        print('feed_generator - 2', feed_generator_2)

        print('\n\tTesting FeedWebView\n')
        feed_all = self.request_feed_webview()
        print('feed - all', feed_all)
        feed_2 = self.request_feed_webview(num_items=2)
        print('feed - 2', feed_2)


    def benchmark(self):
        # print('api_key:', self.api_key)
        # print('api_gateway:', self.api_gateway)

        self.sql_interface = SQL_Interface()

        # r = self.request_getter('list')
        # print(r)
        # r.print_data()

        # self.sql_interface.insert_test(r)

        # r2 = self.request_feed_generator('all')
        # print(r2)
        # r2.print_data()
        # print()
        r3 = self.request_feed_webview('all')
        # print(r3)
        # r3.print_data()

        self.sql_interface.insert_test(r3)



# ==============================
# >>>>> run the benchmarks <<<<<

benchmarker = Benchmarker()

# test that methods work...
# benchmarker.test_methods()

# run benchmarks!
benchmarker.benchmark()
