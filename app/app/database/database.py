import databases
import os
import asyncpg

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = 'postgresql://postgres:postgres@0.0.0.0:5432/' if DATABASE_URL is None else DATABASE_URL
database = databases.Database(DATABASE_URL)

async def startup():
    # Start database on app startup.
    try:
        await database.connect()
        print("INFO:     Successfully connected to database.")
    except ConnectionRefusedError:
        print("ERROR:    Could not connect to database.")
        raise 
    # now make the tables (bootstrap) or version the database as needed
    await create_database()

async def shutdown():
    # Stop database on shutdown.
    print("INFO:     Disconnecting from database.")
    await database.disconnect()

def provide_connection() -> databases.Database:
    return database

# will attempt to create; will quietly stop on a database error
# but will do nothing if the tables all exist (unless told to regen)
# all workers try this at startup, so run with REGEN only ONCE
# then run again without it. That ensure the tables are correct.
async def create_database():
    DATABASE_REGEN = os.environ.get('DATABASE_REGEN')
    regen = False if DATABASE_REGEN is None else True

    if (regen):
        print("regenerating database, bye-bye data...")
        sql = [
            "DROP TABLE IF EXISTS users CASCADE;",
            "DROP TABLE IF EXISTS jaminfo CASCADE;",
            "DROP TABLE IF EXISTS robot CASCADE;",
            "DROP TABLE IF EXISTS control CASCADE;",
            "DROP TABLE IF EXISTS dbver CASCADE;",
            ]
    else:
        sql = []

    sql2=["CREATE EXTENSION IF NOT EXISTS pgcrypto;",
            'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',

            """CREATE TABLE IF NOT EXISTS users (
                    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT UNIQUE NOT NULL
            );""",

            """CREATE TABLE IF NOT EXISTS robot (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                alias TEXT NOT NULL
            );""",

            """CREATE TABLE IF NOT EXISTS jaminfo (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                lat DOUBLE PRECISION,
                lng DOUBLE PRECISION,
                intensity DOUBLE PRECISION,
                robotId UUID REFERENCES robot(id),
                logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );""",

            "CREATE INDEX IF NOT EXISTS jaminfo_robot_idx ON jaminfo(robotId);",

            """CREATE TABLE IF NOT EXISTS control (
                id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                userId UUID,
                robotId UUID,
                FOREIGN KEY(userId) REFERENCES users(id),
                FOREIGN KEY(robotId) REFERENCES robot(id)
            );""",
            # make sure we only create red robot one time:
            "INSERT INTO robot(alias) SELECT 'Red Robot' EXCEPT SELECT alias FROM robot",
            "CREATE TABLE IF NOT EXISTS dbver(dbver int);",
            # first insert ...
            "INSERT INTO dbver SELECT 1 EXCEPT SELECT COUNT(dbver) FROM dbver;"
            ]
    sql.extend(sql2)
    stmt = ""
    try:
        for s in sql:
            stmt = s
            await database.execute(s)
        print("INFO:     Database bootstrapped")
    except asyncpg.exceptions.PostgresError:
        print("INFO:     Restart without DATABASE_REGEN; bootstrap failure on: ",stmt)
    # now we can do any updates here...
    # select dbver from dbver, use the value to drive further alterations
    # then update dbver to the next value. (TODO)
    dbver = await database.fetch_one("SELECT dbver FROM dbver");
    print("INFO:     Database version: ",dbver["dbver"])
    # if (dbver == 1): # base version needs to go to 2...
    #   set up 1->2 changes and execute
    #   first stmt is update dbver set dbver = 2 so later workers skip
    #   dbver = 2
    # if (dbver == 2):
    #   set up 2->3 changes and execute
    #   first stmt is update dbver set dbver = 3
    #   dbver = 3
    # you get the idea ...
