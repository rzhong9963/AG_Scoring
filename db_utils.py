import sqlite3
from sqlite3 import Error
import logging

# DB name
db = "scores.db"

# Create DB connection
def create_conn():
    conn = None
    logging.basicConfig(level=logging.INFO)
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        logging.INFO(e)
    return conn

# Add player and print ID after
def register(fname, lname, div):
    insert = """
        INSERT INTO players(fname, lname, division) VALUES (?, ?, ?)
    """
    conn = create_conn()
    cur = conn.cursor()
    conn.execute(insert, (fname, lname, div))
    conn.commit()
    print(f"{fname} {lname}'s player ID is {get_id(fname, lname)}")
    # Add player to game tables
    games = [
        "INSERT INTO onsets(id) VALUES (?);",
        "INSERT INTO equations(id) VALUES (?);",
        "INSERT INTO ling(id) VALUES (?);",
        "INSERT INTO prop(id) VALUES (?);",
        "INSERT INTO pres(id) VALUES (?);",
        "INSERT INTO ce(id) VALUES (?);",
        "INSERT INTO theme(id) VALUES (?);",
        "INSERT INTO overall(id) VALUES (?);",
    ]
    for g in games:
        cur.execute(g, (get_id(fname, lname),))
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
    score = cur.execute(score, (id,)).fetchone()
    conn.close()
    # Returns a tuple since scaled score is included for reading games
    return score

# Get all game scores for a single player
def all_scores(id):
    search = """
        SELECT players.id, player.fname, player.lname, onsets.total, equations.total, ling.total, prop.total, 
        prop.scaled, pres.total, pres.scaled, ce.total, ce.scaled, theme.total, theme.scaled  
        FROM players 
        INNER JOIN onsets ON players.id = onsets.id
        INNER JOIN equations ON players.id = equations.id
        INNER JOIN ling ON players.id = ling.id
        INNER JOIN prop ON players.id = prop.id
        INNER JOIN pres ON players.id = pres.id
        INNER JOIN ce ON players.id = ce.id
        INNER JOIN theme ON players.id = theme.id
    """
    conn = create_conn()
    cur = conn.cursor()
    result = cur.execute(search, (id,)).fetchone()
    # Return tuple result
    return result

# Same as all_scores, but include each individual round
def all_round_scores(id):
    search = """
        SELECT players.id, player.fname, player.lname, onsets.r1, onsets.r2, onsets.r3, onsets.r4, onsets.total, 
        equations.r1, equations.r2, equations.r3, equations.r4, equations.total, ling.r1, ling.r2, ling.r3, ling.r4,
        ling.total, prop.r1, prop.r2, prop.r3, prop.r4, prop.total, prop.scaled, pres.r1, pres.r2, pres.total, 
        pres.scaled, ce.r1, ce.r2, ce.total, ce.scaled, theme.r1, theme.r2, theme.total, theme.scaled
        FROM players 
        INNER JOIN onsets ON players.id = onsets.id
        INNER JOIN equations ON players.id = equations.id
        INNER JOIN ling ON players.id = ling.id
        INNER JOIN prop ON players.id = prop.id
        INNER JOIN pres ON players.id = pres.id
        INNER JOIN ce ON players.id = ce.id
        INNER JOIN theme ON players.id = theme.id
    """
    conn = create_conn()
    cur = conn.cursor()
    result = cur.execute(search, (id,)).fetchone()
    # Return tuple result
    return result

# All information for reporting purposes
def all_info():
    divisions = ["M", "J", "S"]
    all_results = []
    conn = create_conn()
    cur = conn.cursor()
    for d in divisions:
        search = """
            SELECT players.id, player.fname, player.lname, onsets.total, equations.total, ling.total, prop.total, 
            prop.scaled, pres.total, pres.scaled, ce.total, ce.scaled, theme.total, theme.scaled 
            FROM players 
            INNER JOIN onsets ON players.id = onsets.id
            INNER JOIN equations ON players.id = equations.id
            INNER JOIN ling ON players.id = ling.id
            INNER JOIN prop ON players.id = prop.id
            INNER JOIN pres ON players.id = pres.id
            INNER JOIN ce ON players.id = ce.id
            INNER JOIN theme ON players.id = theme.id
            WHERE players.division = {div}
        """.format(div=d)
        results = cur.execute(search).fetchall()
        all_results.append(results)
    # Returns list of tuples
    return all_results
