import requests
import pandas as pd
import timeit

def go(username_list):
    total_data = []

    for i, username in enumerate(username_list[0:500]):
        response = requests.get(f"https://api.chess.com/pub/player/{username[1:-1]}/stats") if i == 0 else requests.get(f"https://api.chess.com/pub/player/{username[2:-1]}/stats")
        if response.status_code != (200):
            print(response.status_code, i)
            continue

        player_data_json = response.json()
        time_controls = ['chess_rapid', 'chess_blitz', 'chess_bullet']
        player_data = []
        total_wins = 0
        total_loses = 0

        for control in time_controls:
            try:
                time_control = player_data_json[control]
                player_data.extend([time_control['last']['rating'], time_control['last']['rd'], time_control['best']['rating']])
                total_wins += time_control['record']['win'] 
                total_loses += time_control['record']['loss'] 
            except Exception as e:
                player_data.extend([None, None, None])
        
        tactics = player_data_json['tactics']

        #There is a large contingent that will have done tactics but not puzzle rush, so we concider then seperately
        if tactics:
            player_data.append(tactics['highest']['rating'])
            try:
                player_data.append(player_data_json['puzzle_rush']['best']['score'])
                player_data.append(player_data_json['puzzle_rush']['best']['total_attepmts'])
            except:
                player_data.extend([None, None])
        else:
            player_data.extend([None, None, None])

        player_data.append(total_wins/(total_wins+total_loses))
        total_data.append(player_data)
    
    return(total_data)


# Achieves approximately 45.46 seconds for 100 examples with one thread
#print (timeit.timeit(stmt = go, number = 1))
usernames = pd.read_csv('Usernames.csv', index_col=0)
username_string = usernames['username']

headers = ['rapid_last_rating', 'rapid_last_rd', 'rapid_best_rating',
'blitz_last_rating', 'blitz_last_rd', 'blitz_best_rating',
'bullet_last_rating', 'bullet_last_rd', 'bullet_best_rating',
'puzzle_highest', 'puzzle_rush_score', 'puzzle_rush_attempts',
'winrate'
]

df = pd.DataFrame(go(username_string), columns = headers)
df.to_csv('player_data.csv', index=False)


