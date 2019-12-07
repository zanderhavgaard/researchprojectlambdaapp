from benchmarker import Benchmarker 
from sql_interface import SQL_Interface
from test_data import TestData


sql = SQL_Interface()

print('testing avg run')

# sql.insert_coldtimes_run_avg(1,'TEST',64,1.0,2.0,True,1.0,2.0,2.0,64.0,64,4.0,4.0) 

#  fx_id,uuid,minutes,latency,offset,in_bound,low_b,up_b,min_la,max_la,min_minu,max_minu,min_off,max_off) 

print('not final')

# sql.insert_coldtimes_finalrun(2,'TEST not final',100,1.0,1.0,True,False)

print('Test final run')

sql.insert_coldtimes_finalrun(10,'TEST final',100,1.0,1.0,True,True)

# +---------------+--------------+------+-----+---------------------+----------------+
# | Field         | Type         | Null | Key | Default             | Extra          |
# +---------------+--------------+------+-----+---------------------+----------------+
# | id            | int(11)      | NO   | PRI | NULL                | auto_increment |
# | fx_id         | int(11)      | YES  | MUL | NULL                |                |
# | uuid          | varchar(128) | YES  |     | NULL                |                |
# | time_stamp    | timestamp    | NO   |     | current_timestamp() |                |
# | numb_minutes  | int(11)      | YES  |     | NULL                |                |
# | latency       | double       | YES  |     | NULL                |                |
# | offset        | double       | YES  |     | NULL                |                |
# | within_bounds | tinyint(1)   | YES  |     | NULL                |                |
# | final_result  | tinyint(1)   | YES  |     | NULL                |                |
# | lower_bound   | double       | YES  |     | NULL                |                |
# | upper_bound   | double       | YES  |     | NULL                |                |
# | min_latency   | double       | YES  |     | NULL                |                |
# | max_latency   | double       | YES  |     | NULL                |                |
# | min_minutes   | int(11)      | YES  |     | NULL                |                |
# | min_offset    | double       | YES  |     | NULL                |                |
# | max_offset    | double       | YES  |     | NULL                |                |
# +---------------+--------------+------+-----+---------------------+----------------+
