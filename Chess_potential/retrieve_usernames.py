import requests
import pandas as pd

#Firstly, we need to genrate random usernames to collect a sample of random users
#We accomplish this by collecting usernames from tournaments with predictable names 

#Chess.com runs a 3-0 arena every hour, with the name 30-blitz-2403{int}, where int is a 3 digit integer based sequentially on when the tournament was created 
# 30 denotes the specific time control - blitz the time mode and 2403{int} is the nth tournament on chess.com
# (Int is actually 7 digits, including 2403, but we need not consider those digits)
def get_usernames_from_scratch(num_requests, max_usernames):
    usernames = []
    viable_tournaments = []
    for i in range(num_requests, 900):
        query = f'30-blitz-2403{i:03d}'
        #Chess.Com takes around 400 queries before it disconnects you, so we sometimes need to run this many times
        response = requests.get(f"https://api.chess.com/pub/tournament/{query}")

        if response.status_code == 200:
            tournament = response.json()
            viable_tournaments.append(i)
            for player in tournament['players']:
                usernames.append(player['username'])
            print(viable_tournaments)
        else:
            print(i)
            continue

        if len(usernames) > max_usernames:
            break

    dict = {'username' : usernames}
    tournament_ids = {'tournament_id' : viable_tournaments}
    df = pd.DataFrame(dict) 
    tourney_ids = pd.DataFrame(tournament_ids) 
        
    df.to_csv('usernames3.csv') 
    tourney_ids.to_csv('viable3.csv')

get_usernames_from_scratch(600, 5000)
