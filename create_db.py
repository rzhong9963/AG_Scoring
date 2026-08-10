import sqlite3
from sqlite3 import Error

# Create DB connection
def create_conn(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn

# Execute SQL statements to create tables
def create_tables(conn, sql):
    try:
        c = conn.cursor()
        c.executescript(sql)
    except Error as e:
        print(e)

# Create db connection and then create tables for scores and players
# CREATE TABLE IF NOT EXISTS <new> AS SELECT * FROM <old>; Creates NULL values instead.
# Manually doing all columns individually works better
def create_db():
    db = "scores.db"
    conn = create_conn(db)
    conn.execute("PRAGMA foreign_keys = ON;")
    if conn is not None:
        tables = """
        CREATE TABLE IF NOT EXISTS players(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            division TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS onsets(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            r3 INTEGER NOT NULL DEFAULT 0,
            r4 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS equations(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            r3 INTEGER NOT NULL DEFAULT 0,
            r4 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ling(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            r3 INTEGER NOT NULL DEFAULT 0,
            r4 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS prop(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            r3 INTEGER NOT NULL DEFAULT 0,
            r4 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0,
            scaled INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS theme(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0,
            scaled INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ce(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0,
            scaled INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS pres(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER NOT NULL DEFAULT 0,
            r2 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0,
            scaled INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS overall(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            g1 INTEGER NOT NULL DEFAULT 0,
            g2 INTEGER NOT NULL DEFAULT 0,
            g3 INTEGER NOT NULL DEFAULT 0,
            g4 INTEGER NOT NULL DEFAULT 0,
            total INTEGER NOT NULL DEFAULT 0
        );
        """
        create_tables(conn, tables)
        conn.close()
    else:
        print("Error connecting to the database")
    return db
