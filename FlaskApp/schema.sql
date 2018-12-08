DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Job;
DROP TABLE IF EXISTS Manager;
DROP TABLE IF EXISTS Notification;

CREATE TABLE Employee (
    e_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    e_username TEXT UNIQUE NOT NULL, 
    e_password TEXT NOT NULL,
    e_fullname TEXT, 
    phone INTEGER,
    claimed_jobs INTEGER, 
    qualifications TEXT 
);

CREATE TABLE Job (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    m_id INTEGER NOT NULL, 
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    job_title TEXT NOT NULL, 
    job_desc TEXT NOT NULL, 
    job_credentials TEXT,
    job_date_beg TEXT,
    job_date_end TEXT,
    job_time_beg TEXT,
    job_time_end TEXT,
    job_city TEXT,
    job_state TEXT, 
    job_zip INTEGER,
    job_extra INTEGER,
    job_days TEXT,
    FOREIGN KEY (m_id) REFERENCES manager (m_id)
);

   
CREATE TABLE Manager (
    m_id INTEGER PRIMARY KEY UNIQUE,
    m_username TEXT UNIQUE NOT NULL,
    m_password TEXT NOT NULL,
    m_fullname TEXT,
    phone INTEGER
);


CREATE TABLE Notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    type  TEXT,
    message   TEXT,
    priority  TEXT,
    created  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tables to implement
-- jobsClaimed
-- jobCreated


