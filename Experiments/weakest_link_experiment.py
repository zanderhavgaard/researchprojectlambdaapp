import sys
import uuid
import time
from benchmarker import Benchmarker
from sql_interface import SQL_Interface

# Weakest Link Experiment

class WeakestLinkExperiment:

  def __init__(self):
    self.bench = Benckmarker()
    self.sql_interface = SQL_Interface()
    self.exp_iterations = 5
    self.num_items_to_get = 1
    self.cold_time_secs = self.get_cold_time() 
    self.uuid = uuid.uuid1()
    self.test_datas = []

  # returns cold time from db in seconds
  def get_cold_time(self):
    return self.sql_interface.get_coldtime()

  def run_experiment(self):

    for i in range(self.exp_iterations):

      # initial invoke
      self.test_datas.append(benchmarker.request_feed_generator(num_items=self.num_items_to_get))
      
      # wait for lambda to be cold
      time.sleep(self.cold_time_secs)

      # make generator + getter hot
      self.test_datas.append(benchmarker.request_feed_generator(num_items=self.num_items_to_get))
      # webview lambda will be cold
      self.test_datas.append(benchmarker.request_feed_webview(num_items=self.num_items_to_get))
      
      # wait for lambda to be cold
      time.sleep(self.cold_time_secs)



      
    # save test data in db
    for td in self.test_datas:
      td.description = self.uuid + "|{}_weakest_link_experiment".format(i)
      self.sql_interface.insert_test(td)

# run class as self contained program
self_contained_test = bool(sys.argv[1]) if sys.argv[1] > len(sys.argv) else False 
if self_contained_test:
  wle = WeakestLinkExperiment()
  wle.run_experiment()
  
