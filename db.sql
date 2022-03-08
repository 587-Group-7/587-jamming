CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
        id UUID default uuid_generate_v4() PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT UNIQUE NOT NULL
);

DROP TABLE IF EXISTS jaminfo CASCADE;

CREATE TABLE jaminfo (
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    intensity DOUBLE PRECISION,
    robot_id INTEGER REFERENCES robot(id));

CREATE INDEX jaminfo_robot_idx ON jaminfo(robot_id);

DROP TABLE IF EXISTS robot CASCADE;

CREATE TABLE robot (
    id SERIAL PRIMARY KEY
);

