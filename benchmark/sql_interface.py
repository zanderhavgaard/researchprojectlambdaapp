import mysql.connector as mysql
from test_data import TestData
from timing import Timing

class SQL_Interface:

    def __init__(self):
        self.host = 'localhost'
        self.user = 'rp'
        self.password = 'rp'
        self.database = 'rp'

    def insert_query(self, query:str, values:tuple=None):
        connection = mysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database
        )
        try:
            cursor = connection.cursor()
            if values is None:
                cursor.execute(query)
            else:
                cursor.execute(query, values)
            connection.commit()
            return True
        except Exception as e:
            print('Caught an exception while executing query ...', str(e))
            return False

    def insert_test(self, td:TestData):
        query = "INSERT INTO tests (uuid, complete_json, total_time, total_latency, description, concurrent, thread_num, num_threads) VALUES ('{}', '{}', {}, {}, '{}', {}, {}, {})".format(
            td.uuid, td.complete_json, td.total_time, td.total_latency, td.description, int(td.concurrent), td.thread_num, td.num_threads
        )
        # print(query)

        self.insert_query(query=query)

        for timing in td.timings:
            self.insert_timing(timing)

    def insert_timing(self, t:Timing):
        query = "INSERT INTO timings (test_uuid, fx_id, total_time, exe_time, latency, memory_limit) VALUES ('{}', {}, {}, {}, {}, {})".format(
            t.test_uuid, t.function_id, t.total_time, t.exe_time, t.latency, t.memory_limit
        )
        # print(query)

        self.insert_query(query=query)

    def insert_coldtimes(arg):
        query = "INSERT INTO "
