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
    def add_time_to_return_obj(self, return_dict, identifyer):
        if 'time' not in return_dict.keys():
            return_dict['time'] = {}
        return_dict['time'][identifyer] = self.__exit__()
        return return_dict
