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
    if max == 0:
        scale_factor = 1
    else:
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
    conn = db_utils.create_conn()
    cur = conn.cursor()
    # Stores score values
    math_min = {}
    lang_min = {}
    social_min = {}
    math_max = {}
    lang_max = {}
    social_max = {}
    other = {}
    theme_score = {}
    overall = """
        UPDATE overall SET g1 = ?, g2 = ?, g3 = ?, g4 = ?, total = ? WHERE id = ?
    """
    # Math game comparisons | OS and EQ
    onsets = """
        SELECT id, total FROM onsets
    """
    equations = """
        SELECT id, total FROM equations
    """
    os_scores = cur.execute(onsets).fetchall()
    eq_scores = cur.execute(equations).fetchall()
    for o in os_scores:
        for e in eq_scores:
            if o[0] == e[0]:
                if o[1] > e[1]:
                    math_max[o[0]] = o[1]
                    math_min[e[0]] = e[1]
                else:
                    math_max[o[0]] = e[1]
                    math_min[e[0]] = o[1]
            continue
        continue
    # Social Studies game comparisons | Pres and CE
    pres = """
        SELECT id, scaled FROM pres
    """
    ce = """
        SELECT id, scaled FROM ce
    """
    pres_scores = cur.execute(pres).fetchall()
    ce_scores = cur.execute(ce).fetchall()
    for p in pres_scores:
        for c in ce_scores:
            if p[0] == c[0]:
                if p[1] > c[1]:
                    social_max[p[0]] = p[1]
                    social_min[c[0]] = c[1]
                else:
                    social_max[p[0]] = c[1]
                    social_min[c[0]] = p[1]
            continue
        continue
    # English game comparisons | Ling and Prop
    ling = """
        SELECT id, total FROM ling
    """
    prop = """
        SELECT id, scaled FROM prop
    """
    prop_scores = cur.execute(prop).fetchall()
    ling_scores = cur.execute(ling).fetchall()
    for p in prop_scores:
        for l in ling_scores:
            if p[0] == l[0]:
                if p[1] > l[1]:
                    lang_max[p[0]] = p[1]
                    lang_min[l[0]] = l[1]
                else:
                    lang_max[p[0]] = l[1]
                    lang_min[l[0]] = p[1]
            continue
        continue
    # Comparison of remaining scores
    theme = """
        SELECT id, scaled FROM theme
    """
    theme_scores = cur.execute(theme).fetchall()
    for t in theme_scores:
        theme_score[t[0]] = t[1]
    for k in theme_score:
        other[k] = max(theme_score[k],math_min[k],lang_min[k],social_min[k])
    scores = {}
    for k in other:
        scores[k] = (lang_max[k], math_max[k], social_max[k], other[k])
        overall_score = sum(scores[k])
        scores[k] += (overall_score, k)
        cur.execute(overall, (scores[k]))
        conn.commit()
    conn.close()
