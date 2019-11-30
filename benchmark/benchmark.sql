DROP DATABASE IF EXISTS rp;
CREATE DATABASE IF NOT EXISTS rp;

USE rp;

DROP TABLE IF EXISTS tests, timings, functions;

-- holds metadata for each test run
CREATE TABLE tests (
       id INT AUTO_INCREMENT PRIMARY KEY,
       complete_json VARCHAR(1000),
       total_elapsed_time INT,
       total_calculated_latency INT,
       description VARCHAR(1000),
       concurrent BOOLEAN DEFAULT FALSE,
       thread_num INT DEFAULT 1,
       num_threads INT DEFAULT 1
);

-- holds human readable names of fxs
CREATE TABLE functions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(50)
);

-- holds timings for each function invocation
CREATE TABLE timings (
       id INT AUTO_INCREMENT PRIMARY KEY,
       fx_id INT,
       test_id INT,
       total_time INT,
       exe_time INT,
       latency INT,
       FOREIGN KEY (fx_id) REFERENCES functions (id),
       FOREIGN KEY (test_id) REFERENCES tests (id)
);

-- insert function names
INSERT INTO functions (name) VALUES
('putter'),('getter'),('feed_generator'),('feed_webview');
