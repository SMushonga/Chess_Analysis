import requests
import pandas as pd
import threading
import timeit
import time

#There are more efficient storage methods but csv is my preference for readability and export 
usernames = pd.read_csv('Usernames.csv', index_col=0)

username_list = usernames['username'].values.tolist()

#This is the data we plan on extracting from chess.com
headers = ['rapid_last_rating', 'rapid_last_rd', 'rapid_best_rating',
'blitz_last_rating', 'blitz_last_rd', 'blitz_best_rating',
'bullet_last_rating', 'bullet_last_rd', 'bullet_best_rating',
'puzzle_highest', 'puzzle_rush_score', 'puzzle_rush_attempts',
'win_rate'
]

#Function to make a request with the username as input and the list and index to which we will push the data to given multithreading   
def make_request(username, empty_list, i):
    response = requests.get(f"https://api.chess.com/pub/player/{username[2:-1]}/stats")
    time.sleep(0.2)
    try:
        empty_list[i] = response.json()
    except Exception as e:
        print(e, username, response.status_code)
        #In case the user deletes the account, we just request my data instead
        backup_request = requests.get(f"https://api.chess.com/pub/player/Shingai17/stats")
        empty_list[i] = backup_request.json()

#We organise and handle the data here
def handle_data(player_data_json_list, total_data, i):
    time_controls = ['chess_rapid', 'chess_blitz', 'chess_bullet']
    total_wins = 0
    total_loses = 0
    player_data = []
    player_data_json = player_data_json_list[i]

    for control in time_controls:
        try:
            time_control = player_data_json[control]
            player_data.extend([time_control['last']['rating'], time_control['last']['rd'], time_control['best']['rating']])
            total_wins += time_control['record']['win'] 
            total_loses += time_control['record']['loss'] 
        except Exception as e:
            player_data.extend([None, None, None])
    try:
        tactics = player_data_json['tactics']
        player_data.append(tactics['highest']['rating'])
    except:
        player_data.append(None)
    try:
        player_data.append(player_data_json['puzzle_rush']['best']['score'])
        player_data.append(player_data_json['puzzle_rush']['best']['total_attepmts'])
    except:
        player_data.extend([None, None])

    try:
        player_data.append(total_wins/(total_wins+total_loses))
    except:
        player_data.append(0)
    total_data.append(player_data)

total_data = []

#n is 1/5th of the samples you want to include
def run(username_list, n=20):
    deposit_data=[None, None, None, None, None]
    extract_data=[None, None, None, None, None]
    # Querying the Api takes time and introduces latency, so to optimise on waiting time, we can multithread 
    # While we wait for the query for entry i - we can handle the data for entry i-1
    for i in range(n):
        if i == 0:
            for j in range(5):
                make_request(username_list[j*n], deposit_data, j)
                extract_data[j]=deposit_data[j]
            
            #We have now requested i = 0
            continue

        #First things first, we must analyse our data from the previous loop
        t1 = threading.Thread(target=make_request, args=(username_list[i], deposit_data, 0, ))
        t2 = threading.Thread(target=make_request, args=(username_list[i+n], deposit_data, 1, ))
        t3 = threading.Thread(target=make_request, args=(username_list[i+2*n], deposit_data, 2, ))
        t4 = threading.Thread(target=make_request, args=(username_list[i+3*n], deposit_data, 3, ))
        t5 = threading.Thread(target=make_request, args=(username_list[i+4*n], deposit_data, 4, ))

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

        for j in range(5):
            handle_data(extract_data, total_data, j)
        
        #before we go to the next loop, we must close the thread requesting data to make sure we have it
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        
        for j in range(5):
            extract_data[j]=deposit_data[j]
    else:
        for j in range(5):
            handle_data(extract_data, total_data, j)

def go():
    run(username_list, 100)


go()
#While this is more efficient, artificially increase its runtime using time.sleep to not encounter a 429 error from Chess.com
df = pd.DataFrame(total_data, columns = headers)
df.to_csv('player_data.csv', index=False)
 