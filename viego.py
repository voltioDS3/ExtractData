from time import process_time_ns
import requests
from requests.exceptions import HTTPError


class LolViego:
    #the idea of this module is that , whatever tier or division you add, it will continue all the way from that specific division to diamond I or IV idk yet
    DIVISION_MAPPING = {
        'GOLD' : ['GOLD', 'PLATINUM', 'DIAMOND'],
        'PLATINUM' : ['PLATINUM', 'DIAMOND'],
        'DIAMOND' : ['DIAMOND']
    }

    TIER_MAPPING = {
        'IV' : ['IV', 'III', 'II', 'I'],
        'III': ['III', 'II', 'I'],
        'II' : ['II', 'I'],
        'I' : ['I']

    }

    PAGES_MAPPING ={

    }

    def __init__(self, api_key, division, tier, region, page):
        self.api_key = api_key
        self.division_list = LolViego.DIVISION_MAPPING[division]
        self.tier_list = LolViego.TIER_MAPPING[tier]
        self.page_list = [x for x in range(page, 10000)]

        self.current_division
    def leaguev4_player_entries(self, region, queue= 'RANKED_SOLO_5X5', tier= 'GOLD', divisions = ['IV', 'III', 'II', 'I'], page = [x for x in range(1, 10000)]): #this is for getting a list of players by tier, i will start at platinum and beyond 
        if type(divisions) is list:
            if type(page) is list:
                for division in divisions:

                    url = f'https://{region.lower()}.api.riotgames.com/lol/league/v4/entries/{queue}/DIAMOND/I?page=2&api_key=RGAPI-6790ab72-f889-4fe8-9129-fc969dccdc1f'
        pass


    def matchv5_matchlist(self,region,puuid,queue,type,start=0,count=20): # this is matches by puuid amd returns a list of ids with 
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
