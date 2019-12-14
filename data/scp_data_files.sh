#!/bin/bash

pi_ip="10.24.53.102"

data_files="
all_coldtimes.csv
all_tests.csv
all_tests_join_timings.csv
all_timings.csv
concurrent.csv
times_linked_coldstart.csv
weakest_link.csv
coldstartlog_128_1.txt
coldstartlog_128_2.txt
coldstartlog_1536.txt
coldstartlog_512.txt
"

for file in $data_files; do
  scp pi@$pi_ip:/home/pi/data/$file .
done
