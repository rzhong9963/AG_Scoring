import db_utils
import calculate
import create_db
import generate_report
import os, sys

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

# Main menu
def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=======Main Menu=======")
    print("Options:")
    print("1. Register Players")
    print("2. Input/Get Scores")
    print("3. Generate Results")
    print("4. Export Player List")
    print("5. Exit")
    option = int(input("Enter selection number: "))
    match option:
        case 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            register_player()
        case 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=======Input Scores=======")
            print("Options:")
            print("1. Get Scores")
            print("2. Input Scores")
            option = int(input("Enter selection number: "))
            match option:
                case 1:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    get_scores()
                case 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    input_scores()
        case 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            generate_report.generate_csv()
            generate_report.generate_pdf()
            print("Results have been generated. All files located in the 'reports' folder.")
        case 4:
            generate_report.player_list()
            print("Player list has been generated. File is located in the 'reports' folder.")
        case 5:
            sys.exit()

# Input
def input_menu():
    pass

# Get Scores
def get_scores():
    print("=======Get Scores=======")
    player = int(input("Enter Player ID: "))
    scores = list(db_utils.all_scores(player))
    print(f"{scores[1]} {scores[2]}'s Scores: \nOn-Sets: {scores[3]}\nEquations: {scores[4]}\nLinguiSHTIK: {scores[5]}"
          f"\nPropaganda Total: {scores[6]} | Scaled: {scores[7]}\nPresidents Total: {scores[8]} | Scaled: {scores[9]}"
          f"\nCurrent Events Total: {scores[10]}\nScaled: {scores[11]} \nTheme Total: {scores[12]} | Scaled: {scores[13]}")
    breakdown = input("Do you want round breakdown? (Y/N): ")
    match breakdown.casefold():
        case "y":
            scores = db_utils.all_round_scores(player)
            print("=======Score Breakdown by Rounds=======")
            print(f"{scores[1]} {scores[2]}'s Scores: \nOn-Sets: Round 1: {scores[3]} | Round 2: {scores[4]} | "
                  f"Round 3: {scores[5]} | Round 4: {scores[6]} | Total: {scores[7]}\nEquations: Round 1: {scores[8]} | "
                  f"Round 2: {scores[9]} | Round 3: {scores[10]} | Round 4: {scores[11]} | Total: {scores[12]} \n"
                  f"LinguiSHTIK: Round 1: {scores[14]} | Round 2: {scores[15]} | Round 3: {scores[16]} | "
                  f"Round 4: {scores[17]} | Total: {scores[18]}\nPropaganda: Round 1: {scores[19]} | Round 2: "
                  f"{scores[20]} | Round 3: {scores[21]} | Round 4: {scores[22]} | Total: {scores[23]} | Scaled: "
                  f"{scores[24]} \nPresidents: Round 1: {scores[25]} | Round 2: {scores[26]} | Total: {scores[27]} | "
                  f"Scaled: {scores[28]} \nCurrent Events: Round 1: {scores[29]} | Round 2: {scores[30]} | Total: "
                  f"{scores[31]} | Scaled: {scores[32]}\nTheme: Round 1: {scores[33]} | Round 2: {scores[34]} | Total: "
                  f"{scores[35]} | Scaled: {scores[36]}")
        case "n":
            main_menu()

# Score Input
def input_scores():
    print("=======Input Scores=======")

# Player Registration
def register_player():
    print("=======Player Registration=======")

if __name__ == '__main__':
    create_db.create_db()
    main_menu()
