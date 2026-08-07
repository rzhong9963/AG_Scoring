import db_utils
import register
import create_db

"""
    Terminal-based version of this program implementation.
    Main Menu options:
        - Register Players
        - Input Scores
            - Game Selection
            - Round Selection
        - Output Scores (by division)
            - CSV output
            - PDF output
    Player division for registration will take only single characters.
        M = Middle
        J = Junior
        S = Senior
    Games will also take single characters for identifier.
        O = On-Sets
        E = Equations
        L = Ling
        C = Current Events
        T = Theme
        P = Prop
        R = Pres
"""

def main_menu():
    print()

if __name__ == '__main__':
    create_db.create_db()
    main_menu()
