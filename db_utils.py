import sqlite3
from sqlite3 import Error

# DB name
db = "scores.db"

# Create DB connection
def create_conn():
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn

# Close DB connection
def close_conn(conn):
    conn.close()

# Add player and print ID after
def register(fname, lname, div):
    insert = """
        INSERT INTO players(fname, lname, division) VALUES (?, ?, ?)
    """
    conn = create_conn()
    cur = conn.cursor()
    match div:
        # Middle
        case div if div.upper() == "M":
            values = (fname, lname, "M")
            cur.execute(insert, values)
            conn.commit()
            print(f"{fname} {lname}'s player ID is {get_id(fname, lname)}")
        # Junior
        case div if div.upper() == "J":
            values = (fname, lname, "J")
            cur.execute(insert, values)
            conn.commit()
            print(f"{fname} {lname}'s player ID is {get_id(fname, lname)}")
        # Senior
        case div if div.upper() == "S":
            values = (fname, lname, "S")
            cur.execute(insert, values)
            conn.commit()
            print(f"{fname} {lname}'s player ID is {get_id(fname, lname)}")
    conn.close()

# Returns list of players by ID
def get_players(div):
    players = []
    return players

# Returns player ID from name
def get_id(fname, lname):
    search = """
        SELECT id FROM players WHERE fname = ? AND lname = ?
    """
    conn = create_conn()
    cur = conn.cursor()
    id = cur.execute(search, (fname, lname)).fetchone()[0]
    conn.close()
    return id

# Returns player name from ID
def get_player(id):
    search = """
        SELECT fname, lname FROM players WHERE id = ?
    """
    conn = create_conn()
    cur = conn.cursor()
    player_name = cur.execute(search, (id,)).fetchone()
    conn.close()
    player_name_str = player_name[0] + " " + player_name[1]
    return player_name_str

# Update round score for player
# Find a way to maybe use games as a variable instead of match like rounds
def update_score(score, id, round, game):
    match game:
        # On-Sets
        case game if game.upper() == "O":
            update = """
                UPDATE onsets SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
        # Equations
        case game if game.upper() == "E":
            update = """
                UPDATE equations SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
        # Ling
        case game if game.upper() == "L":
            update = """
                UPDATE ling SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
        # Current Events
        case game if game.upper() == "C":
            update = """
                UPDATE ce SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
        # Theme
        case game if game.upper() == "T":
            update = """
                UPDATE theme SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
        # Prop
        case game if game.upper() == "P":
            update = """
                UPDATE prop SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
        # Pres
        case game if game.upper() == "R":
            update = """
                UPDATE pres SET {round} = ? WHERE id = ?
            """.format(round="r"+str(round))
    conn = create_conn()
    cur = conn.cursor()
    cur.execute(update, (score, id))
    conn.commit()
    conn.close()

# Update totals
def update_totals():
    pass

# Get player score for a specific game based on ID
# Same as updating score. Find a way to maybe use game as a variable instead of match statement
def get_score(id, game):
    match game:
        # On-Sets
        case game if game.upper() == "O":
            score = """
                SELECT total FROM onsets WHERE id = ?
            """
        # Equations
        case game if game.upper() == "E":
            score = """
                SELECT total FROM equations WHERE id = ?
            """
        # Ling
        case game if game.upper() == "L":
            score = """
                SELECT total FROM ling WHERE id = ?
            """
        # Current Events
        case game if game.upper() == "C":
            score = """
                SELECT total, scaled FROM ce WHERE id = ?
            """
        # Theme
        case game if game.upper() == "T":
            score = """
                SELECT total, scaled FROM theme WHERE id = ?
            """
        # Prop
        case game if game.upper() == "P":
            score = """
                SELECT total, scaled FROM prop WHERE id = ?
            """
        # Pres
        case game if game.upper() == "R":
            score = """
                SELECT total, scaled FROM pres WHERE id = ?
            """
    conn = create_conn()
    cur = conn.cursor()
