def players_teams_clean(players_lst:list):

    players_lst = [p for p in players_lst if p not in ['',' ']] #Get rid of blank name cells (or just whitespace name)
    players_cnt = len(players_lst)
                   
    if players_cnt>=4 and players_cnt<=6:
        teams_cnt = 2
    elif players_cnt<=10:
        teams_cnt = 4
        if players_cnt == 7:
            players_lst.append('EmptySlot')
    elif players_cnt<=14:
        if players_cnt == 11:
            players_lst.append('EmptySlot')
        teams_cnt = 6
    else:
        teams_cnt = 6
        print('Too many or little players, please use 14 players maximum')

    return players_lst, teams_cnt


def get_opp_limit(n_rounds,n_players):

    if n_rounds <= 8 :
        same_opp_limit = 3
    elif n_rounds <=10:
        if n_players in [6,9,10]:
            same_opp_limit = 3
        else:
            same_opp_limit = 4
    else:
        same_opp_limit = 5

    return same_opp_limit


def adjust_solo_games(game_schedule):

    for key, inner_dict in game_schedule.items():
        for inner_key, value in inner_dict.items():
            # Check if 'EmptySlot' is in the tuple value
            if 'EmptySlot' in value:
                # Replace the whole tuple with a single string where 'EmptySlot' is replaced by 'Solo'
                game_schedule[key][inner_key] = ('solo ' + value[1] if value[0] == 'EmptySlot' else value[0] + ' solo')

    return game_schedule


def init_matrix(players,n_matrices=2):  

    import pandas as pd
    init_matrices = []

    for _ in range(n_matrices):
        matrix = pd.DataFrame(0, index=players, columns=players)
        init_matrices.append(matrix)

    # Fill diagonal elements for each matrix
    for m in init_matrices:
        for i in range(min(m.shape)):
            m.iloc[i, i] = 1

    return init_matrices

def df_custom_merge(df1,df2):

    import pandas as pd
    df_final = pd.DataFrame(index=df1.index, columns=df1.columns)

    for row_index, row in enumerate(df1.index):
        for col_index, col in enumerate(df1.columns):
            # Concatenate the values with a comma
            merged_value = str(df1.loc[row, col]) + ', ' + str(df2.loc[row, col])
            # Assign the merged value to the final DataFrame
            df_final.loc[row, col] = merged_value

    return df_final
