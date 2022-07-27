from argparse import RawDescriptionHelpFormatter
from email.policy import HTTP
from time import process_time_ns
import time
from urllib import response
import requests
import json
from requests.exceptions import HTTPError
class BLANKError(Exception):
    """Base class for other exceptions"""
    pass

class IDError(Exception):
    """Base class for other exceptions"""
    pass

class MATCHESError(Exception):
    """Base class for other exceptions"""
    pass





class LolViego:
    #the idea of this module is that , whatever tier or division you add, it will continue all the way from that specific division to diamond I or IV idk yet
    TIER_MAPPING = {
        'GOLD' : ['DIAMOND', 'PLATINUM', 'GOLD' ],
        'PLATINUM' : ['DIAMOND', 'PLATINUM'],
        'DIAMOND' : ['DIAMOND']
    }

    DIVISION_MAPPING = {
        'IV' : ['IV', 'III', 'II', 'I'],
        'III': ['III', 'II', 'I'],
        'II' : ['II', 'I'],
        'I' : ['I']

    }

    CONTINENTS_MAPPING ={
        'br1': 'americas',
        'eun1' : 'europe',
        'euw1' : 'europe',
        'jp1': 'asia',
        'kr' : 'asia',
        'la1' : 'americas',
        'la2' : 'americas',
        'na1' : 'americas',
        'oc1' : 'sea',
        'ru'  : 'europe'
    }

    def __init__(self, api_key,region, division, tier, page):
        self.api_key = api_key
        self.division_list = LolViego.DIVISION_MAPPING[division]
        self.tier_list = LolViego.TIER_MAPPING[tier]
        self.page_list = [x for x in range(page, 10000)]
        self.region = region #BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, RU
        self.region_continent = LolViego.CONTINENTS_MAPPING[region]
        self.api_key = api_key
        
    def get_data(self):  #this is for getting a list of players by tier, i will start at platinum and beyond 
        
        
        for division in self.division_list:
            for tier in self.tier_list:
                for page in self.page_list:
                    # print(tier)
                    # print(division)
                    # print(page)
                    players_entries = self.leaguev4_get_entries(tier,division,page)
                    for player in players_entries:
                        summoner_id = player['summonerId']
                        puuid = self.summonerv4_get_summoner_by_id(summoner_id)
                        matches = self.matchv5_matchlist(puuid)
                        # print(puuid)
                        # print(games)
                        for match in matches:
                            match_info = self.matchv5_match_info()
                            

                        



    def leaguev4_get_entries(self,tier, division, page):  #returns a list with player info from differents soloq rankeds
     
        url = f'https://{self.region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}&api_key={self.api_key}'
        
        try:
            response = requests.get(url)
            
            if len(response.json()) == 0:  #  means there was an empty response
                raise BLANKError
            print(f'[success] entries gotten')
            return response.json()

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f'[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}')
            pass
        
        except BLANKError as blank:  #  response was blank, which could mean that we have reached last page
            print('[error] response was empty, likely last page')
            pass


    def summonerv4_get_summoner_by_id(self, summoner_id):

        url = f'https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={self.api_key}'
        try:
            response = requests.get(url)
            
            if response.status_code == 400:
                raise IDError
            print(f'[success] puuid gotten')
            return response.json()['puuid']

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f'[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}')
            pass

        except IDError as id_error:
            print('[error] id not found or other error')
            pass



    def matchv5_matchlist(self,puuid, count=40 ):  # this is matches by puuid amd returns a list of ids with 
        start_time = int(time.time()) - 604800*2  # two weeks from today
        
        # url = f'https://{self.region_continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&endTime={end_time}&count={count}&api_key={self.api_key}'
        url = f'https://{self.region_continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={start_time}&endTime={int(time.time())}&queue=420&type=ranked&start=0&count={count}&api_key={self.api_key}'
        try:
            response = requests.get(url)
            print(response.status_code)
            
            if len(response.json()) == 0:
                print('[warning] did not found recent games')
                return
            if response.status_code != 200:
                raise MATCHESError
            
            return response.json()

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f'[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}')
            pass

        except MATCHESError() as match_error:
            print('[error] matches id ')
            pass



america = LolViego('RGAPI-c74d120c-a58a-4e1a-9b65-718e895e7793', 'na1', 'I','DIAMOND', 1)
america.get_data()