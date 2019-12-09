from benchmarker import Benchmarker
from sql_interface import SQL_interface
from datetime import datetime
import uuid
import sys
import json
import time

class ConcurrentExperiment:

    def __init__(self,numb_threads):
        self.threads = numb_threads
        self.exp_iterations = 5
        self.SQL = SQL_interface()
        self.bench = Benchmarker()
        self.uuid = uuid.uuid1() 
        self.cold_time_secs = self.get_cold_time()
        self.test_data_lists = []

    # returns cold time from db in seconds
    def get_cold_time(self):
        return self.sql_interface.get_coldtime() 
    
    def run_experiment(self):

        for i in range(self.exp_iterations):
            # invoke lambdas concurrently
            self.test_data_lists.append(self.bench.run_method_concurrently('Getter',{'command':'get_file_url','filename':'red.png'},self.threads))
            # wait for lambdas to be cold
            time.sleep(self.cold_time_secs)

        # add data to db
        for td_list in test_data_lists:   
          for td in td_list:
            td.description = self.uuid + "|{}_concurrent_experiment".format(i)
            self.SQL.inser_data(td)
          

# run class as self contained program
self_contained_test = bool(sys.argv[1]) if len(sys.argv) > 1 else False 
if self_contained_test:
  ce = ConcurrentExperiment()
  ce.run_experiment()





    
     
