# AG Scoring
***
Recreation of scoring system used in Academic Games. Currently designed for local use.

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
- [ ] Create Registration System 
  - [ ] Drop-down for GUI version
- [x] Implement Database 
- [ ] Create CSV/PDF generator for scores
  - [ ] Auto-sort by division
- [ ] Terminal based system
  - [ ] GUI version
    - [ ] Auto updating score viewer?
    - [ ] Tabs to switch between score input and registration
- [x] Score Calculation System
  - [ ] Auto calculating scores
  - [x] Dynamic scaling reading games