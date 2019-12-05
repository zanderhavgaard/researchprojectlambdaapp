DROP DATABASE IF EXISTS rp;
CREATE DATABASE IF NOT EXISTS rp;

USE rp;

DROP TABLE IF EXISTS tests, timings, functions;

-- holds human readable names of fxs
CREATE TABLE functions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50)
);

-- holds metadata for each test run
CREATE TABLE tests (
       id INT AUTO_INCREMENT PRIMARY KEY,
       uuid VARCHAR(128),
       complete_json VARCHAR(5000),
       total_time DOUBLE,
       total_latency DOUBLE,
       time_stamp TIMESTAMP DEFAULT NOW(),
       description VARCHAR(1000),
       concurrent BOOLEAN DEFAULT FALSE,
       thread_num INT DEFAULT 1,
       num_threads INT DEFAULT 1
);

-- holds timings for each function invocation
CREATE TABLE timings (
       id INT AUTO_INCREMENT PRIMARY KEY,
       test_uuid VARCHAR(128),
       fx_id INT,
       total_time DOUBLE,
       exe_time DOUBLE,
       latency DOUBLE,
       memory_limit INT,
       log_stream_name VARCHAR(100),
       FOREIGN KEY (fx_id) REFERENCES functions (id)
);

-- Values for warm to cold experiments
-- IMPORTANT: pull max min
CREATE TABLE coldtimes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fx_id INT,
    uuid VARCHAR(128),
    time_stamp TIMESTAMP DEFAULT NOW(),
    numb_minutes INT,
    latency DOUBLE,
    offset DOUBLE,
    within_bounds BOOLEAN,
    final_result BOOLEAN,
    lower_bound DOUBLE DEFAULT NULL,
    upper_bound DOUBLE DEFAULT NULL,
    min_latency DOUBLE DEFAULT NULL,
    max_latency DOUBLE DEFAULT NULL,
    min_minutes INT DEFAULT NULL,
    min_offset DOUBLE DEFAULT NULL,
    max_offset DOUBLE DEFAULT NULL,

    FOREIGN KEY (fx_id) REFERENCES functions (id),
);

       




-- TODO fix
-- FOREIGN KEY (test_uuid) REFERENCES tests (uuid)

-- insert function names
INSERT INTO functions (name) VALUES
('putter'),('getter'),('feed_generator'),('feed_webview');
