import db_utils

"""
    Calculator for scaling and total scores
"""

# Scale scores for reading games
def scaled(game):
    max = 0
    conn = db_utils.create_conn()
    cur = conn.cursor()
    # Get each player's total score
    match game:
        case "P":
            search = """
                SELECT id, total FROM {game}
            """.format(game="prop")
        case "R":
            search = """
                SELECT id, total FROM {game}
            """.format(game="pres")
        case "C":
            search = """
                SELECT id, total FROM {game}
            """.format(game="ce")
        case "T":
            search = """
                SELECT id, total FROM {game}
            """.format(game="theme")
    player_scores = cur.execute(search).fetchall()
    # Get highest score first to establish scale factor
    for player in player_scores:
        if player[1] > max:
            max = player[1]
    scale_factor = 24/max
    # Update with scaled scores
    match game:
        case "P":
            insert = """
                UPDATE prop SET scaled = ? WHERE id = ?
            """
        case "R":
            insert = """
                UPDATE pres SET scaled = ? WHERE id = ?
            """
        case "C":
            insert = """
                UPDATE ce SET scaled = ? WHERE id = ?
            """
        case "T":
            insert = """
                UPDATE theme SET scaled = ? WHERE id = ?
            """
    for player in player_scores:
        scaled_score = player[1] * scale_factor
        cur.execute(insert, (scaled_score, player[0]))
        conn.commit()
    conn.close()

# Overall score calculation
# Gets higher score between the two games in each category and gets the next highest by using the min from each category
# and getting the max from the remaining ones
def overall_scores():
    overall_score = 0
    conn = db_utils.create_conn()
    cur = conn.cursor()
    # Stores the lower unused score for comparison later
    math_min = 0
    lang_min = 0
    social_min = 0
    # Math game comparisons | OS and EQ

    # Social Studies game comparisons | Pres and CE

    # English game comparisons | Ling and Prop