# Script requires libraries that are not installed with python by default (pandas, Flask)- see requierements.txt file
# You can install these libraries with following command:
    # pip install -r requirements.txt

from flask import Flask, render_template, request
import pandas as pd
import random 
from itertools import chain, combinations
from utils import get_opp_limit, players_teams_clean, adjust_solo_games, init_matrix

app = Flask(__name__)

# Function That creates game schedule and pairings 
def create_game_schedule(player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11,player12,player13,player14,
                         rounds=8):
    
    players_init = [player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11,player12,player13,player14]
    players, teams_cnt = players_teams_clean(players_lst=players_init)
    same_opp_limit = get_opp_limit(n_rounds=rounds,n_players=len(players))

    game_schedule = dict()
    rerun_all = True

    while rerun_all == True:
    
        game_schedule = dict()
        teammate_limit = 1

        matrices = init_matrix(players,n_matrices=2)
        matrix_teammates = matrices[0] 
        matrix_opponents = matrices[1] 
        
        singles, resting = {}, {}

        for r in range(0,rounds): # Itterate over number of rounds to create round's schedule 
            
            rerun_all = True
            counter_in_round = 0
            
            while counter_in_round<=50: # Bruteforcing with 50 attempts to meet conditions when creating round schedule (if fail try full schedule)
                
                teams = dict()            
                counter_in_round += 1            

                for i in range(0,teams_cnt): # Itterate to make correct number of teams
                    
                    rerun_round = True                    
                    if (matrix_teammates.min().min() == matrix_teammates.max().max()) or ((matrix_teammates==0).sum().sum()==2 and i==1):
                        teammate_limit= 2
                    
                    avail_teams = list(combinations([x for x in players if x not in list(chain.from_iterable(teams.values()))],2)) # All team combinations that exists                 
                    random.shuffle(avail_teams)

                    for team in avail_teams: # Itterate over all availabel teams (find team that has not played together before)
                        if matrix_teammates.loc[team[0],team[1]] < teammate_limit : # Condition if they played together 
                            teams[i] = team
                            rerun_round = False
                            break 

                    if rerun_round == True: # If previous itteration failed and we havent found suitable team, exit team loop and try to schedule the round again (50attemps)
                        break

                
                if rerun_round == False: # If find a suitable round schedule to meet conditions (in 50attempts), continue loop into text round
                    rerun_all = False
                    break
                                                
            if rerun_all==False: # Filling Teammates and Opponents matrix to keep track of history and for conditions                  
                for i in range(0,teams_cnt):
                    matrix_teammates.loc[teams[i][0],teams[i][1]] = matrix_teammates.loc[teams[i][0],teams[i][1]] + 1
                    matrix_teammates.loc[teams[i][1],teams[i][0]] = matrix_teammates.loc[teams[i][1],teams[i][0]] + 1

                    if i % 2 == 1:
                        matrix_opponents.loc[teams[i],teams[i-1]] = matrix_opponents.loc[teams[i],teams[i-1]] + 1
                        matrix_opponents.loc[teams[i-1],teams[i]] = matrix_opponents.loc[teams[i-1],teams[i]] + 1
                        
                if matrix_opponents.max().max()>same_opp_limit: # Condition to not play against someone too many times (could be improved by optimal pairing)
                    rerun_all = True
                    break

            else: #If we fail, rerunning whole schedule from round 1
                break

            # Check schedule if we have also some singles or players resting (based on number of players)        
            game_schedule[r] = teams
            if len([x for x in players if x not in list(chain.from_iterable(teams.values()))])==2:
                singles[r] = [x for x in players if x not in list(chain.from_iterable(teams.values()))]
            if len([x for x in players if x not in list(chain.from_iterable(teams.values()))])==1:
                resting[r] = [x for x in players if x not in list(chain.from_iterable(teams.values()))]
    
    if 'EmptySlot' in players: # Simple condition to print out schedule in nicer way
        game_schedule = adjust_solo_games(game_schedule)

    # Printed output to be displayed in HTML
    text_ouput = '\n'.join([f"Round {i+1}:\n" +
                        ''.join([f"\t{game_schedule[i][j]} vs. {game_schedule[i][j+1]}\n" for j in range(0, teams_cnt, 2)]) +
                        (f"\t{singles[i][0]} vs. {singles[i][1]}\n" if len(singles) > 0 else '') +
                        (f"\t{resting[i][0]} is resting\n" if len(resting) > 0 else '') +
                        f'==================================================' for i in range(rounds)])
    text_ouput = text_ouput.replace("'", "")
    
    return text_ouput, matrix_teammates, matrix_opponents

# Flask Defining for user's input interactively (Names, number of rounds)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the input values from the form
        player_inputs = {}
        for i in range(1, 15):
            player_inputs[f'player{i}'] = request.form.get(f'player{i}')
        rounds = int(request.form["rounds"])
        text_ouput, matrix_teammates, matrix_opponents = create_game_schedule(**player_inputs, rounds=rounds)

        return render_template("result.html", text_output=text_ouput,  df1=matrix_teammates, df2=matrix_opponents)
    else:
        # Render the form template
        return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)