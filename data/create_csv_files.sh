#!/bin/bash

# all tests
mysql rp -u rp -prp -e "select id, uuid, total_time, total_latency, time_stamp, description, concurrent, thread_num, num_threads from tests;" | sed 's/\t/,/g' > all_tests.csv

# all timings
mysql rp -u rp -prp -e "select id, test_uuid, function_name, fx_id, total_time, exe_time, latency, memory_limit, log_stream_name from timings;" | sed 's/\t/,/g' > all_timings.csv

# all coldtimes
mysql rp -u rp -prp -e "select * from coldtimes;" | sed 's/\t/,/g' > all_coldtimes.csv

# all tests joined on timings
mysql rp -u rp -prp -e "select te.id, te.uuid, te.total_time as total_invoke_time, te.total_latency as total_invoke_latency, te.time_stamp, te.description, te.concurrent, te.thread_num, te.num_threads, ti.id, ti.test_uuid, ti.function_name, ti.fx_id, ti.total_time, ti.exe_time, ti.latency, ti.memory_limit, ti.log_stream_name
from tests te join timings ti on te.uuid=ti.test_uuid;"  | sed 's/\t/,/g' > all_tests_join_timings.csv

# get all concurrent results
mysql rp -u rp -prp -e "select te.id, te.uuid, te.total_time as total_invoke_time, te.total_latency as total_invoke_latency, te.time_stamp, te.description, te.concurrent, te.thread_num, te.num_threads, ti.id, ti.test_uuid, ti.function_name, ti.fx_id, ti.total_time, ti.exe_time, ti.latency, ti.memory_limit, ti.log_stream_name
from tests te join timings ti on te.uuid=ti.test_uuid where te.description like '%|concurrent%';"  | sed 's/\t/,/g' > concurrent.csv

# get all weakest link results
mysql rp -u rp -prp -e "select te.id, te.uuid, te.total_time as total_invoke_time, te.total_latency as total_invoke_latency, te.time_stamp, te.description, te.concurrent, te.thread_num, te.num_threads, ti.id, ti.test_uuid, ti.function_name, ti.fx_id, ti.total_time, ti.exe_time, ti.latency, ti.memory_limit, ti.log_stream_name
from tests te join timings ti on te.uuid=ti.test_uuid where te.description like '%|weakest_link_experiment%';"  | sed 's/\t/,/g' > weakest_link.csv

# get all times, dates, latency from tests that are bound to a coldtime test via UUID
mysql rp -u rp -prp -e "select description, date(time_stamp) as date, time(time_stamp) as invTime,total_latency from tests where description in (select uuid from coldtimes where date(time_stamp) > '2019-12-11');" | sed 's/\t/,/g' > times_linked_coldstart.csv
