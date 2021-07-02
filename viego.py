from time import process_time_ns
import requests
from requests.exceptions import HTTPError


class LolViego:

    def __init__(self, api_key):
        self.api_key = api_key
    
    def matchv5_matchlist(self,region,puuid,queue,type,start=0,count=20):
        def_game_id = []
        if region == 'AMERICAS':
            url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&type={type}&start={start}&count={count}&api_key={self.api_key}'
        elif region == 'EUROPE':
            url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&type={type}&start={start}&count={count}&api_key={self.api_key}'
        elif region == 'ASIA':
            url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue={queue}&type={type}&start={start}&count={count}&api_key={self.api_key}'
        response = requests.get(url)

        print(response)
        if response.status_code == 200:
            game_ids = response.text
            game_list = game_ids.strip('][').split(',')
            for game in game_list:
                def_game_id.append(game.replace('"',''))
            return def_game_id
        else: raise Exception
