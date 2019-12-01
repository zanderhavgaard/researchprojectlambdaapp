import time

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

    # add time to a return obj
    def add_time_to_return_obj(self, return_dict, identifier, time_dict=None):
        # if the time key is not present
        if 'time' not in return_dict.keys():
            return_dict['time'] = {}

        # if we have saved some timings from other lambda invocations
        if time_dict is not None:
            for key, val in time_dict.items():
                return_dict['time'][key] = val

        # add new timing
        exe_time = self.__exit__()
        return_dict['time'][identifier] = {'exe_time': exe_time}

        return return_dict
