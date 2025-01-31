#!/bin/python

import time 
import sys
import os
import json

from benchmarker import Benchmarker 
from sql_interface import SQL_Interface

class Max_warm_test:

    def __init__(self,fux,interval,offset,accuracy:float):
        self.lambda_function = fux
        self.interval = interval
        self.offset = offset
        self.accuracy = accuracy
        self.bench = Benchmarker()
        run()


        
    
        
        def compute_avg(l=list):
            total_value = 0
            for val in l:
                total_value += val
            
            return total_value / len(l)



        def avg_warm_time():

            avg_time_list = []

            for i in range(10):
            
                test_data = bench.request_getter(command='get_file_url',filename="blue.png") # arguments
                response_dict = test_data.json_dict
            
                latency= response_dict['time'][response_dict['identifier']]['latency']
            
                avg_time_list.append(latency)
            
            return avg_time_list
            
            

        def get_warm_cutoff(coldtime,avg_warm_time,min_start,interval,offs):
            # benchmark cold time
            cold = coldtime
            # excepted offset from cold 
            local_offset = offs
            # init with average warm time for call to function
            longest_meassured = avg_warm_time
            # minutes between calls
            increment = min_start
            # values gathered from for-loop
            vals = []

            for i in range(5):
                print()
                print('local increment',increment) #delete
                print('measure',longest_meassured) # delete
                print('cold - offset',cold,local_offset) # delete
                print('bool',longest_meassured < cold - local_offset) # delete
                print()
                # check if meassured time falls into span defined for cold
                while longest_meassured < cold - local_offset:
                    # compute latency of call after making the function sleep
                    print('sleeping for minutes',increment) # delete
                    time.sleep(60*increment)
                    test_data = self.bench.request_getter(command='get_file_url',filename="blue.png") 
                    response_dict = test_data.json_dict
                    latency = response_dict['time'][response_dict['identifier']]['latency']
                
                    # check if latency is higher then current high
                    if(latency > longest_meassured):
                        longest_meassured = latency
                    # avoid infinate loop 
                    if increment > 90:
                        local_offset += offs
                    
                    increment = increment + interval
                
                # print('increment in round',i,increment)
                vals.append( (longest_meassured, increment, local_offset))
                longest_meassured = 0
                increment = int(min_start / 2)
                # print('increment set for round',i+1,increment)
            
            return vals


        def output_reults(list1,cold_plus_risk,cold_minus_risk):

            # values to be outputted
            avg_time = 0
            avg_min = 0
            avg_offset = 0
            min_time = 1000
            max_time = 0
            min_min = 1000
            max_min = 0
            min_offset = 1000
            max_offset = 0

            plus_risk = True
            minus_risk = True

            print('values for each run')

            for i in range(len(list1)):
                (t,m,o) = list1[i]
                avg_time += t
                avg_min += m
                avg_offset = o
                print(t,m,o)

                if t < min_time:
                    min_time = t
                if t > max_time:
                    max_time = t
                if m < min_min:
                    min_min = m
                if m > max_min:
                    max_min = m
                if o < min_offset:
                    min_offset = o
                if o > max_offset:
                    max_offset = o
                
                if t > cold_plus_risk:
                    plus_risk = False
                if t < cold_minus_risk:
                    minus_risk = False

                print('Run:',i,'latency:',str(t),'minutes from warm to cold:',m,'ofsset used:',o,'within upper bound:',t > cold_plus_risk,'within lower bound',t < cold_minus_risk)

            print()
            print('Averaged values for all runs')
            print('latency:',str(avg_time/len(list1)),'minutes:',str(avg_min/len(list1)),'offset:',str(avg_offset/len(list1)))
            print()
            print('min time:',str(min_time),'max time:',str(max_time))
            print('min minutes:',min_min,'max minutes:',max_min)
            print('min offset:',min_offset,'max offset',max_offset)
            print('All rund within upper bound:',plus_risk)
            print('All rund within lower bound:',minus_risk)

            return (avg_time,avg_min,avg_offset,plus_risk and minus_risk)



    def run(self):

        test_data = self.bench.request_getter(command='get_file_url',filename="blue.png") 
        response_dict = test_data.json_dict
        cold_time = response_dict['time'][response_dict['identifier']]['latency']

        print('Time for cold function -',lambda_function,'- meassured time:',str(cold_time))

        avg_warm_time = self.compute_avg(avg_warm_time())

        print('Time for average warm function call:',avg_warm_time)

        print('warm function is',cold_time / avg_warm_time,'times faster')


        cold_plus_risk = cold_time * (1 + self.accuracy)
        cold_minus_risk = cold_time * self.accuracy

        if avg_warm_time > cold_minus_risk:
            print('Lambda seems to have been warm when experiment was started - coldtime:',cold_time,'warmtime:',avg_warm_time)

        # First run of meassurements
        print('interval',interval)
        first_run = self.get_warm_cutoff(cold_time,avg_warm_time,interval,interval,offset)

        (latency,minutes,ofset,b) = self.output_reults(first_run,cold_plus_risk,cold_minus_risk)
        print('first run was within expected bounds?',b)

        # Run again with inputs from first run and reduced interval and offset for greater accuracy 
        second_run = self.get_warm_cutoff(latency,avg_warm_time,minutes-interval,interval/2,offset/2)
        (l,m,o,b) = self.output_reults(second_run,latency* (1 + self.accuracy),latency * self.accuracy)

        print()
        print('final result')
        print('latency:',l,'minutes to cold:',m,'offset used:',o,'within expected bounds:',b,'bounds',(latency* (1 + self.accuracy)),(latency * self.accuracy))












