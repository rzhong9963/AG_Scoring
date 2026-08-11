# AG Scoring
***
Re-creation of scoring system used in Academic Games. Currently designed for local use.

## How to Use
***
Save this repository in a folder of your choice. Make sure any dependencies are installed. To install, the command `python -m pip install -r requirements.txt` can be run. Once finished, to run the program, type `python main.py`. Make sure at least Python 3.10 is installed (3.14 preferred). As of now, the whole program is terminal-based.
#### Main Menu Options
All options return back to the main menu once finished (with the exception of `Exit`) in case another option is needed. Inputs are case-insensitive.
1. Register Players

    Self-explanatory. In this sub-menu, you'll be prompted to enter the player's first and last name separated by a single space. You'll then be prompted to enter their division as "M" for Middle, "J" for Junior, or "S" for Senior (case-insensitive). Once entered, that player's ID will then be displayed as confirmation. You'll also get a prompt to register another player if so desired.
2. Input/Get Scores

    This sub-menu has two options. `Get Scores` and `Input Scores`.
   1. The `Get Scores` menu takes a player ID as input and outputs the total scores for all games, including scaled scores for reading game. It also prompts for a round breakdown where you can see individual round scores.
   2. The `Input Scores` menu displays all the games and a single-letter code used to identify each game. You will be prompted to enter the game code and round number (space separated) to input scores. For example, to do On-Sets round 2, you would simply type `O 2`. The current game and round number will be displayed while you input scores based on player ID. After the ID is entered, the player name will appear as a verification. Once score input is finished, the program will automatically calculate totals and scale reading games scores.
3. Generate Results
   
    As of now, the generate results function generates both a PDF and CSV format for scores of all players separated by division sorted by rank based on overall score totals. The files are stored in a folder called `reports` in the same directory as this program. **<ins>When running this, please ensure all relevant files are closed or it will error out.</ins>**
4. Export Player List

    Also self-explanatory. This simply exports a CSV file of all players separated by division. The exported file can be modified however you like. However, if the function is run again, it will clear any additions made.
5. Exit

    Exits the program. That's it.

## Database Schema
***
The overall database design is shown below. The actual column names may differ, but the structure is the same overall.
```mermaid
    erDiagram
        players{
            integer id PK
            text first_name
            text last_name
            text division
        }
        onsets{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer round3_score
            integer round4_score
            integer total
        }
        equations{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer round3_score
            integer round4_score
            integer total
        }
        ling{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer round3_score
            integer round4_score
            integer total
        }
        prop{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer round3_score
            integer round4_score
            integer total
            integer scaled_score
        }
        pres{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer total
            integer scaled_score
        }
        ce{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer total
            integer scaled_score
        }
        theme{
            integer id PK,FK
            integer round1_score
            integer round2_score
            integer total
            integer scaled_score
        }
        overall{
            integer id PK,FK
            integer game1_score
            integer game2_score
            integer game3_score
            integer game4_score
            integer total
        }
        players ||--|| onsets : id
        players ||--|| equations : id
        players ||--|| ling : id
        players ||--|| prop: id
        players ||--|| pres : id
        players ||--|| ce : id
        players ||--|| theme : id
        players ||--|| overall : id
        onsets |o--o| overall : total_score
        equations |o--o| overall : total_score
        ling |o--o| overall : total_score
        prop |o--o| overall : scaled_score
        pres |o--o| overall : scaled_score
        ce |o--o| overall : scaled_score
        theme |o--o| overall : scaled_score
```
Everything is stored in a single database, with a division column to further sort players for rankings based on division. 
### Table Explanations
***
#### Players
Players are automatically assigned an ID number when added to the database. This ID is autoincremented per registered player and is referenced by all other games and the overall score tables.

#### Onsets, Equations, and Ling
References player ID from the players table, sorts individual scores for each round and stores the total score from all rounds.

#### Prop, Pres, CE, and Theme
Same as Onsets, Equations and Ling tables, but with a `scaled_total` column to scale the highest score to a max of 24.

#### Overall
Calculates the best game score from each subject area + next highest separately and also store the total combined score.


## TO-DO
***
- [x] Create Registration System 
  - [ ] Drop-down for GUI version
- [x] Implement Database 
- [x] Create CSV/PDF generator for scores
  - [x] Auto-sort by division
  - [ ] Switch to fpdf for finer PDF generation
- [x] Terminal based system
  - [ ] GUI version
    - [ ] Auto updating score viewer?
    - [ ] Tabs to switch between score input and registration
- [x] Score Calculation System
  - [x] Auto calculating scores
  - [x] Dynamic scaling reading games