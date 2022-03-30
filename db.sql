CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- USER is a reserved word; changing to USERS...
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
        id UUID default uuid_generate_v4() PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT UNIQUE NOT NULL
);

DROP TABLE IF EXISTS jaminfo CASCADE;

CREATE TABLE jaminfo (
    id UUID default uuid_generate_v4() PRIMARY KEY,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    intensity DOUBLE PRECISION,
    robot_id INTEGER REFERENCES robot(id));

CREATE INDEX jaminfo_robot_idx ON jaminfo(robot_id);

DROP TABLE IF EXISTS robot CASCADE;

CREATE TABLE robot (
    id SERIAL PRIMARY KEY,
    alias TEXT,
    userControlId UUID,
    FOREIGN KEY(userControlId) REFERENCES user(id)
);

CREATE TABLE control (
    id UUID default uuid_generate_v4() PRIMARY KEY,
    userId UUID,
    robotId UUID,
    FOREIGN KEY(userId) REFERENCES user(id),
    FOREIGN KEY(robotId) REFERENCES robot(id)
)

