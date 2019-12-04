import json
import uuid
import re
from timing import Timing

class TestData:

    def __init__(
            self,
            complete_json:dict,
            description:str='',
            concurrent=False,
            thread_num=1,
            num_threads=1
    ):
        self.fx_name_to_id = {
            "Putter": 1,
            "Getter": 2,
            "Feed-Generator": 3,
            "Feed-WebView": 4
        }
        self.uuid = uuid.uuid1()

        self.json_dict = complete_json
        self.complete_json = json.dumps(complete_json)
        self.description = description

        self.total_time = complete_json['time'][complete_json['identifier']]['total_time']
        self.total_latency = self.compute_total_latency(complete_json['time'])

        self.timings = self.parse_timings(time_dict=self.json_dict['time'])

        self.concurrent = concurrent
        self.thread_num = thread_num
        self.num_threads = num_threads

    def compute_total_latency(self, time_dict:dict):
        latency = 0.0
        for key in time_dict.keys():
            latency += time_dict[key]['latency']
        return latency

    def parse_timings(self, time_dict:dict):
        timings = []
        for key in time_dict.keys():
            timing = Timing(
                test_uuid=self.uuid,
                function_name=key,
                function_id=self.find_lambda_id(key),
                total_time=time_dict[key]['total_time'],
                exe_time=time_dict[key]['exe_time'],
                latency=time_dict[key]['latency'],
                memory_limit=time_dict[key]['memory'],
                log_stream_name=self.parse_log_stream_name(time_dict[key]['log_stream_name'])
            )
            timings.append(timing)
        return timings

    def parse_log_stream_name(self, log_stream_name:str):
        return re.findall(pattern='.*\]([a-zA-Z0-9]+)', string=log_stream_name)


    def find_lambda_id(self, fx_name:str):
        for key in self.fx_name_to_id.keys():
            if key in fx_name:
                return self.fx_name_to_id[key]
        return None

    def print_data(self):
        print('TestData obj:')
        print('total_time', self.total_time,
              'total_latency', self.total_latency,
              'concurrent', self.concurrent,
              'thread_num', self.thread_num,
              'num_threads', self.num_threads,
              'uuid', self.uuid
        )

        print('description', self.description)
        print('complete_json', self.complete_json)

        print('Timings:')
        for t in self.timings:
            t.print_data()
