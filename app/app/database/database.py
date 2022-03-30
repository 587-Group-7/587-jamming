import databases
import os
import asyncpg

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = 'postgresql://postgres:postgres@0.0.0.0:5432/dev' if DATABASE_URL is None else DATABASE_URL
database = databases.Database(DATABASE_URL)

async def startup():
    # Start database on app startup.
    try:
        await database.connect()
        print("INFO:     Successfully connected to database.")
    except ConnectionRefusedError:
        print("ERROR:    Could not connect to database.")
        raise 
    # now make the tables if it's the first time (bootstrap)
    await create_database()

async def shutdown():
    # Stop database on shutdown.
    print("INFO:     Disconnecting from database.")
    await database.disconnect()

def provide_connection() -> databases.Database:
    return database

# will attempt to create; only works if user table not already there
# otherwise just stops due to the error.
async def create_database():
    DATABASE_REGEN = os.environ.get('DATABASE_REGEN')
    regen = False if DATABASE_REGEN is None else True
    print("regen: ",regen)

    if (regen):
        sql = ["CREATE EXTENSION IF NOT EXISTS pgcrypto;",
            'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',
            "DROP TABLE IF EXISTS users CASCADE;",
            "DROP TABLE IF EXISTS jaminfo CASCADE;",
            "DROP TABLE IF EXISTS robot CASCADE;",
            "DROP TABLE IF EXISTS control CASCADE;",

            """CREATE TABLE users (
                    id UUID default uuid_generate_v4() PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT UNIQUE NOT NULL
            );""",

            """CREATE TABLE jaminfo (
                id UUID default uuid_generate_v4() PRIMARY KEY,
                lat DOUBLE PRECISION,
                lng DOUBLE PRECISION,
                intensity DOUBLE PRECISION,
                robot_id INTEGER REFERENCES robot(id));""",

            "CREATE INDEX jaminfo_robot_idx ON jaminfo(robot_id);",

            """CREATE TABLE robot (
                id SERIAL PRIMARY KEY,
                alias TEXT,
                userControlId UUID,
                FOREIGN KEY(userControlId) REFERENCES users(id)
            );""",

            """CREATE TABLE control (
                id UUID default uuid_generate_v4() PRIMARY KEY,
                userId UUID,
                robotId UUID,
                FOREIGN KEY(userId) REFERENCES users(id),
                FOREIGN KEY(robotId) REFERENCES robot(id)
            );"""]
    else:
        sql = ["CREATE EXTENSION IF NOT EXISTS pgcrypto;",
            'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',

            """CREATE TABLE users (
                    id UUID default uuid_generate_v4() PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT UNIQUE NOT NULL
            );""",

            """CREATE TABLE jaminfo (
                id UUID default uuid_generate_v4() PRIMARY KEY,
                lat DOUBLE PRECISION,
                lng DOUBLE PRECISION,
                intensity DOUBLE PRECISION,
                robot_id INTEGER REFERENCES robot(id));""",

            "CREATE INDEX jaminfo_robot_idx ON jaminfo(robot_id);",

            """CREATE TABLE robot (
                id SERIAL PRIMARY KEY,
                alias TEXT,
                userControlId UUID,
                FOREIGN KEY(userControlId) REFERENCES users(id)
            );""",

            """CREATE TABLE control (
                id UUID default uuid_generate_v4() PRIMARY KEY,
                userId UUID,
                robotId UUID,
                FOREIGN KEY(userId) REFERENCES users(id),
                FOREIGN KEY(robotId) REFERENCES robot(id)
            );"""]

    try:
        for s in sql:
            await database.execute(s)
        print("database created")
    except asyncpg.exceptions.DataError:
        print("database already created")

