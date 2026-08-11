import sqlite3
from sqlite3 import Error
import logging
import calculate

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
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout = 30000;")
    return conn

# Add player and print ID after
def register(fname, lname, div):
    insert = """
        INSERT INTO players(fname, lname, division) VALUES (?, ?, ?)
    """
    conn = create_conn()
    cur = conn.cursor()
    conn.execute("PRAGMA foreign_keys = ON;")
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
        conn.commit()
    conn.close()

# Returns list of players by ID
def get_players(div):
    search = """
        SELECT id, fname, lname FROM players WHERE division = ?
    """
    conn = create_conn()
    cur = conn.cursor()
    players = list(cur.execute(search, (div,)).fetchall())
    conn.close()
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

# Get all players without division separation
def get_all_players():
    search = """
        SELECT id FROM players
    """
    conn = create_conn()
    cur = conn.cursor()
    players = cur.execute(search).fetchall()
    conn.close()
    return players

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
    players = get_all_players()
    for p in players:
        conn = create_conn()
        cur = conn.cursor()
        os_get = """
            SELECT r1, r2, r3, r4 FROM onsets WHERE id = ?
        """
        os_set = """
            UPDATE onsets SET total = ? WHERE id = ?
        """
        eq_get = """
            SELECT r1, r2, r3, r4 FROM equations WHERE id = ?
        """
        eq_set = """
            UPDATE equations SET total = ? WHERE id = ?
        """
        ling_get = """
            SELECT r1, r2, r3, r4 FROM ling WHERE id = ?
        """
        ling_set = """
            UPDATE ling SET total = ? WHERE id = ?
        """
        pres_get = """
            SELECT r1, r2 FROM pres WHERE id = ?
        """
        pres_set = """
            UPDATE pres SET total = ? WHERE id = ?
        """
        prop_get = """
            SELECT r1, r2, r3, r4 FROM prop WHERE id = ?
        """
        prop_set = """
            UPDATE prop SET total = ? WHERE id = ?
        """
        theme_get = """
            SELECT r1, r2 FROM theme WHERE id= ?
        """
        theme_set = """
            UPDATE theme SET total = ? WHERE id = ?
        """
        ce_get = """
            SELECT r1, r2 FROM ce WHERE id = ?
        """
        ce_set = """
            UPDATE ce SET total = ? WHERE id = ?
        """
        os_scores = cur.execute(os_get, (p[0],)).fetchone()
        cur.execute(os_set, (os_scores[0]+os_scores[1]+os_scores[2]+os_scores[3],p[0],))
        eq_scores = cur.execute(eq_get, (p[0],)).fetchone()
        cur.execute(eq_set, (eq_scores[0]+eq_scores[1]+eq_scores[2]+eq_scores[3],p[0],))
        ling_scores = cur.execute(ling_get, (p[0],)).fetchone()
        cur.execute(ling_set, (ling_scores[0]+ling_scores[1]+ling_scores[2]+ling_scores[3],p[0],))
        pres_scores = cur.execute(pres_get, (p[0],)).fetchone()
        cur.execute(pres_set, (pres_scores[0]+pres_scores[1],p[0],))
        prop_scores = cur.execute(prop_get, (p[0],)).fetchone()
        cur.execute(prop_set, (prop_scores[0]+prop_scores[1]+prop_scores[2]+prop_scores[3],p[0],))
        theme_scores = cur.execute(theme_get, (p[0],)).fetchone()
        cur.execute(theme_set, (theme_scores[0]+theme_scores[1],p[0],))
        ce_scores = cur.execute(ce_get, (p[0],)).fetchone()
        cur.execute(ce_set, (ce_scores[0]+ce_scores[1],p[0],))
        conn.commit()
        conn.close()
        for g in ["P", "R", "C", "T"]:
            calculate.scaled(g)
        calculate.overall_scores()

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
            SELECT players.id, players.fname, players.lname, onsets.total, equations.total, ling.total, prop.total, 
            prop.scaled, pres.total, pres.scaled, ce.total, ce.scaled, theme.total, theme.scaled, overall.total
            FROM players 
            INNER JOIN onsets ON players.id = onsets.id
            INNER JOIN equations ON players.id = equations.id
            INNER JOIN ling ON players.id = ling.id
            INNER JOIN prop ON players.id = prop.id
            INNER JOIN pres ON players.id = pres.id
            INNER JOIN ce ON players.id = ce.id
            INNER JOIN theme ON players.id = theme.id
            INNER JOIN overall ON players.id = overall.id
            WHERE players.division = ?
            ORDER BY overall.total DESC
        """
        results = list(cur.execute(search, (d,)).fetchall())
        all_results.append(results)
    conn.close()
    return all_results
