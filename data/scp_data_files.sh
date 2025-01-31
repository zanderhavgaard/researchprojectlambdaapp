#!/bin/bash

set -e

# pi_ip="10.24.53.102"
pi_ip="87.104.29.153"

# port="22"
port="22222"

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
coldstartlog_3008.txt
rp.sql
"

for file in $data_files; do
  scp -P $port pi@$pi_ip:/home/pi/data/$file .
done
