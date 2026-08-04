import sqlite3
from sqlite3 import Error

def create_conn(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn

def create_tables(conn, sql):
    try:
        c = conn.cursor()
        c.executescript(sql)
    except Error as e:
        print(e)

def create_db():
    db = "scores.db"
    conn = create_conn(db)
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
            r1 INTEGER DEFAULT 0,
            r2 INTEGER DEFAULT 0,
            r3 INTEGER DEFAULT 0,
            r4 INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS equations AS SELECT * FROM onsets;
        CREATE TABLE IF NOT EXISTS ling AS SELECT * FROM onsets;
        CREATE TABLE IF NOT EXISTS prop AS SELECT * FROM onsets;
        ALTER TABLE prop ADD COLUMN scaled INTEGER DEFAULT 0;
        CREATE TABLE IF NOT EXISTS theme(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            r1 INTEGER DEFAULT 0,
            r2 INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0,
            scaled INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ce AS SELECT * FROM theme;
        CREATE TABLE IF NOT EXISTS pres AS SELECT * FROM theme;
        CREATE TABLE IF NOT EXISTS sweeps(
            id INTEGER PRIMARY KEY REFERENCES players(id),
            g1 INTEGER DEFAULT 0,
            g2 INTEGER DEFAULT 0,
            g3 INTEGER DEFAULT 0,
            g4 INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0
        );
        """
        create_tables(conn, tables)
    else:
        print("Error connecting to the database")
    return db
