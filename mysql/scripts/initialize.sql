-- DSA Related tables
drop table dsa.academy;

CREATE TABLE dsa.academy
(
  user_id    int(10) unsigned NOT NULL,
  course_id int(10) unsigned NOT NULL,
  title   varchar(255) NOT NULL COLLATE utf8_general_ci,
  email   varchar(254) NOT NULL COLLATE utf8_general_ci,
  sfdc_id varchar(18),
  start_ts  TIMESTAMP NOT NULL,
  finish_ts TIMESTAMP,
  progress  int NOT NULL,
  role   varchar(254) COLLATE utf8_general_ci,
  dsa_last_updated_ts TIMESTAMP,
  last_updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, course_id)
);

-- Load the initial dump provided by Sar.
LOAD DATA LOCAL INFILE '/Users/jega/projects/hawkeye/datastax/data/dsa/user_resource_progress-5.csv'
INTO TABLE dsa.academy
CHARACTER SET UTF8
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY  '"'
LINES TERMINATED BY '\r'
IGNORE 1 LINES
(user_id, email, course_id, title, @epoch_start_ts, @epoch_finish_ts, progress, @epoch_dsa_last_updated_ts)
set start_ts = IF (@epoch_start_ts = 0, NULL, FROM_UNIXTIME(@epoch_start_ts)),
  finish_ts = IF ( @epoch_finish_ts = 0, NULL, FROM_UNIXTIME(@epoch_finish_ts)),
  dsa_last_updated_ts = IF (@epoch_dsa_last_updated_ts = 0, NULL, FROM_UNIXTIME(@epoch_dsa_last_updated_ts));