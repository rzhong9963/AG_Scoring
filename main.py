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
                    input_scores()
        case 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            # Since PDF also generates CSV
#            generate_report.generate_csv()
            generate_report.generate_pdf()
            print("Results have been generated. All files located in the 'reports' folder.")
            os.system("pause")
            main_menu()
        case 4:
            generate_report.player_list()
            print("Player list has been generated. File is located in the 'reports' folder.")
            os.system("pause")
            main_menu()
        case 5:
            sys.exit()
        case _:
            print("Invalid selection.")
            os.system("pause")
            main_menu()

# Get Scores
def get_scores():
    print("=======Get Scores=======")
    player = int(input("Enter Player ID: "))
    scores = list(db_utils.all_scores(player))
    print(f"{scores[1]} {scores[2]}'s Scores: \nOn-Sets: {scores[3]}\nEquations: {scores[4]}\nLinguiSHTIK: {scores[5]}"
          f"\nPropaganda Total: {scores[6]} | Scaled: {scores[7]}\nPresidents Total: {scores[8]} | Scaled: {scores[9]}"
          f"\nCurrent Events Total: {scores[10]}\nScaled: {scores[11]} \nTheme Total: {scores[12]} | Scaled: {scores[13]}")
    breakdown = input("Do you want individual round breakdowns? (Y/N): ")
    match breakdown.upper():
        case "Y":
            scores = db_utils.all_round_scores(player)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=======Score Breakdown by Rounds=======")
            print(f"{scores[1]} {scores[2]}'s Scores: \nOn-Sets: Round 1: {scores[3]} | Round 2: {scores[4]} | "
                  f"Round 3: {scores[5]} | Round 4: {scores[6]} | Total: {scores[7]}\nEquations: Round 1: {scores[8]} | "
                  f"Round 2: {scores[9]} | Round 3: {scores[10]} | Round 4: {scores[11]} | Total: {scores[12]} \n"
                  f"LinguiSHTIK: Round 1: {scores[13]} | Round 2: {scores[14]} | Round 3: {scores[15]} | "
                  f"Round 4: {scores[16]} | Total: {scores[17]}\nPropaganda: Round 1: {scores[18]} | Round 2: "
                  f"{scores[19]} | Round 3: {scores[20]} | Round 4: {scores[21]} | Total: {scores[22]} | Scaled: "
                  f"{scores[23]} \nPresidents: Round 1: {scores[24]} | Round 2: {scores[25]} | Total: {scores[26]} | "
                  f"Scaled: {scores[27]} \nCurrent Events: Round 1: {scores[28]} | Round 2: {scores[29]} | Total: "
                  f"{scores[30]} | Scaled: {scores[31]}\nTheme: Round 1: {scores[32]} | Round 2: {scores[33]} | Total: "
                  f"{scores[34]} | Scaled: {scores[35]}")
            os.system("pause")
            main_menu()
        case "N":
            main_menu()
        case _:
            print("Unknown selection. Exiting to Main Menu")
            os.system("pause")
            main_menu()

# Score Input
def input_scores():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=======Score Input=======")
    print(f"Game Codes: {'O: On-Sets':20} {'E: Equations':20} {'L: LinguiSHTIK':20}"
          f"\n{'C: Current Events':20} {'T: Theme':15} {'P: Propaganda':20} {'R: Presidents':20}")
    game, round = input("Enter Game Code and Round number: ").split()
    if round not in {"1", "2", "3", "4"}:
        print("Invalid Round")
        os.system("pause")
        input_scores()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=======Score Input=======")
        match game.upper():
            case "O":
                print(f"Current Game: On-Sets | Round {round}")
            case "E":
                print(f"Current Game: Equations | Round {round}")
            case "L":
                print(f"Current Game: LinguiSHTIK | Round {round}")
            case "C":
                if round == "3" or round == "4":
                    print("Invalid Round")
                    os.system("pause")
                    input_scores()
                else:
                    print(f"Current Game: Current Events | Round {round}")
            case "T":
                if round == "3" or round == "4":
                    print("Invalid Round")
                    os.system("pause")
                    input_scores()
                else:
                    print(f"Current Game: Theme | Round {round}")
            case "P":
                print(f"Current Game: Propaganda | Round {round}")
            case "R":
                if round == "3" or round == "4":
                    print("Invalid Round")
                    os.system("pause")
                    input_scores()
                else:
                    print(f"Current Game: Presidents | Round {round}")
            case _:
                print("Invalid Game")
                os.system("pause")
                input_scores()
        id = int(input("Enter Player ID: "))
        player_name = db_utils.get_player(id)
        if player_name == "Player ID not Found":
            print("Player ID not Found")
            os.system("pause")
            continue
        else:
            print("Player: " + db_utils.get_player(id))
        score = int(input(f"Enter Round {round} Score: "))
        db_utils.update_score(score, id, round, game.upper())
        repeat = input("Enter scores for another player? (Y/N): ")
        match repeat.upper():
            case "Y":
                continue
            case "N":
                print("Updating Scores...")
                db_utils.update_totals()
                main_menu()
            case _:
                print("Unknown input. Exiting to Main Menu")
                os.system("pause")
                main_menu()

# Player Registration
def register_player():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=======Player Registration=======")
    fname, lname = input("Enter player's name: ").split()
    div = input("Enter Division (M/J/S): ").upper()
    db_utils.register(fname, lname, div)
    cont = input("Do you want to register another player? (Y/N): ")
    match cont.upper():
        case "Y":
            register_player()
        case "N":
            main_menu()

if __name__ == '__main__':
    create_db.create_db()
    main_menu()
