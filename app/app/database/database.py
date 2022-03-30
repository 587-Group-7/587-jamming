import databases
import os
import asyncpg

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = 'postgresql://postgres:postgres@0.0.0.0:5432/dev' if DATABASE_URL is None else DATABASE_URL
database = databases.Database(DATABASE_URL)
created = False

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
    if (created):
        print("already ran this")
    else:
        created = True
        DATABASE_REGEN = os.environ.get('DATABASE_REGEN')
        regen = False if DATABASE_REGEN is None else True

        if (regen):
            print("regenerating database, bye-bye data...")
            sql = [
                "DROP TABLE IF EXISTS users CASCADE;",
                "DROP TABLE IF EXISTS jaminfo CASCADE;",
                "DROP TABLE IF EXISTS robot CASCADE;",
                "DROP TABLE IF EXISTS control CASCADE;",
                ]
        else:
            sql = []
        sql2=["CREATE EXTENSION IF NOT EXISTS pgcrypto;",
                'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',

                """CREATE TABLE users (
                        id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT UNIQUE NOT NULL
                );""",

                """CREATE TABLE robot (
                    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                    alias TEXT,
                    userControlId UUID,
                    FOREIGN KEY(userControlId) REFERENCES users(id)
                );""",

                """CREATE TABLE jaminfo (
                    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                    lat DOUBLE PRECISION,
                    lng DOUBLE PRECISION,
                    intensity DOUBLE PRECISION,
                    robotId UUID REFERENCES robot(id));""",

                "CREATE INDEX jaminfo_robot_idx ON jaminfo(robotId);",

                """CREATE TABLE control (
                    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                    userId UUID,
                    robotId UUID,
                    FOREIGN KEY(userId) REFERENCES users(id),
                    FOREIGN KEY(robotId) REFERENCES robot(id)
                );"""]
        sql.extend(sql2)

        try:
            for s in sql:
                await database.execute(s)
            print("database created")
        except asyncpg.exceptions.DataError:
            print("database already created")

`