-- all of this is now bootstrapped into the startup of the web server ...
-- can delete this file...
-- if still using this file, please see comments at end for
-- any changes made to existing tables (how to do them)
-- and any additional tables/db objects...

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- USER is a reserved word; changing to USERS...
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT UNIQUE NOT NULL
);

DROP TABLE IF EXISTS robot CASCADE;

CREATE TABLE robot (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    alias TEXT NOT NULL
);

DROP TABLE IF EXISTS jaminfo CASCADE;

CREATE TABLE jaminfo (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    intensity DOUBLE PRECISION,
    logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    robotId UUID REFERENCES robot(id)
);

CREATE INDEX jaminfo_robot_idx ON jaminfo(robotId);

CREATE TABLE control (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    userId UUID,
    robotId UUID,
    FOREIGN KEY(userId) REFERENCES user(id),
    FOREIGN KEY(robotId) REFERENCES robot(id)
);

-- only one Red Robot.
INSERT INTO robot (alias) SELECT 'Red Robot' EXCEPT SELECT alias FROM robot;

-- use this table to track database changes
CREATE TABLE IF NOT EXISTS dbver(dbver int);
-- only want one row, start at 1
-- this ensures we won't insert if there's already a row...
INSERT INTO dbver SELECT 1 EXCEPT SELECT COUNT(dbver) FROM dbver;

-- UPDATE dbver SET dbver = # of updates...
-- USE ALTER STATEMENTS to change the shape of existing tables
-- if you are still using this file, create_database in database.py also needs updating
-- for heroku to get the right shape of database.... and it must use dbver and alter,
-- because the database persists between builds. (still a TODO/work in progress)