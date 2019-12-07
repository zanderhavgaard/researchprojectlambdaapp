from benchmarker import Benchmarker
from sql_interface import SQL_interface
from datetime import datetime
import sys
import json
import time

class Experiements:
    
    def __init__(self,cutoff:int):
        self.benchmarker = Benchmarker() 
        self.SQL = SQL_interface()
        self.timestamp = datetime.fromtimestamp(time.time())
        self.cold_cutoff = cutoff # get from sql when done testing local
        self.avg_exe_time = 0.4 # get from sql 
       
        

    def run(self,fux_name:str,command:str,iterations:int,accuracy:int,extra=None,):
        self.accuracy = accuracy 
        self.iter = iterations

        return

        for i in range(iterations):
            time.sleep(self.cold_cutoff)
            data = function_call(fux_name,command,extra)
            

    
    def function_call(self,name:str,command:str,extra=None):
        switcher = {
        'getter': self.benchmarker.request_getter(),
        'putter': self.benchmarker.request_putter(),
        'feed':   self.benchjmarker.request_feed_generator(),
        'webview':self.benchmarker.request_feed_webview()
        }

        return switcher.get(name)
    











