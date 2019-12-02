class Timing:

    def __init__(
            self,
            test_uuid:str,
            function_name:str,
            function_id:int,
            total_time:float,
            exe_time:float,
            latency:float,
            memory_limit:int
    ):
        self.test_uuid = test_uuid
        self.function_name = function_name
        self.function_id = function_id
        self.total_time = total_time
        self.exe_time = exe_time
        self.latency = latency
        self.memory_limit = memory_limit

    def set_test_id(self, test_id:int):
        self.test_id = test_id

    def print_data(self):
        print('Timing:',
              'test_uuid', self.test_uuid,
              'fx_name', self.function_name,
              'fx_id', self.function_id,
              'total_time', self.total_time,
              'exe_time', self.exe_time,
              'latency', self.latency,
              'memory_limit', self.memory_limit
        )
