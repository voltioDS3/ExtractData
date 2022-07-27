import json
import os
import time
from argparse import RawDescriptionHelpFormatter
from email.policy import HTTP
from msilib.schema import Error
from time import process_time_ns
from types import NoneType
from urllib import response
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import requests
from requests.exceptions import HTTPError


class Error(Exception):
    """Base class for other exceptions"""

    pass


class BLANKError(Error):
    """Raised when the input value is too small"""

    pass


class IDError(Error):
    """Raised when the input value is too large"""

    pass


class MATCHESError(Error):
    """Raised when the input value is too large"""

    pass


class GETTINGMATCHError(Error):
    """Raised when the input value is too large"""

    pass


class LolViego:
    # the idea of this module is that , whatever tier or division you add, it will continue all the way from that specific division to diamond I or IV idk yet
    x = 0
    
    TIER_MAPPING = {
        "GOLD": ["DIAMOND", "PLATINUM", "GOLD"],
        "PLATINUM": ["DIAMOND", "PLATINUM"],
        "DIAMOND": ["DIAMOND"],
    }

    DIVISION_MAPPING = {
        "IV": ["IV", "III", "II", "I"],
        "III": ["III", "II", "I"],
        "II": ["II", "I"],
        "I": ["I"],
    }

    CONTINENTS_MAPPING = {
        "br1": "americas",
        "eun1": "europe",
        "euw1": "europe",
        "jp1": "asia",
        "kr": "asia",
        "la1": "americas",
        "la2": "americas",
        "na1": "americas",
        "oc1": "sea",
        "ru": "europe",
    }

    DATA_ESTRUCTURE = {
        "championId": [0],
        "championName": [0],
        "item0": [0],
        "item1": [0],
        "item2": [0],
        "item3": [0],
        "item4": [0],
        "item5": [0],
        "spell1": [0],
        "spell2": [0],
        "perk0": [0],
        "perk1": [0],
        "perk2": [0],
        "perk3": [0],
        "perk4": [0],
        "perk5": [0],
        "role": [0],
        "lane": [0],
        "win": [0],
        "tier": [0],
        "division": [0],
    }

    def __init__(self, region, division, tier, page):
        self.requests = 0
        self.division_list = LolViego.DIVISION_MAPPING[division]
        self.tier_list = LolViego.TIER_MAPPING[tier]
        self.page_list = [x for x in range(page, 10000)]
        self.region = region  # BR1, EUN1, EUW1, JP1, KR, LA1, LA2, NA1, OC1, RU
        self.region_continent = LolViego.CONTINENTS_MAPPING[region]

        self.folder_name = self.region + "_data"
        self.csv_name = self.region + "_data.csv"
        self.recovery_name = self.region + "_recovery.txt"

        with open("./api_key.txt") as f:  # keep this secret
            contents = f.readline()
            self.api_key = contents

        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)

        if not os.path.isfile(self.folder_name + "/" + self.recovery_name):
            with open(self.folder_name + "/" + self.recovery_name, "w+") as f:
                f.write("first")
        else:
            self.recovery_name = self.folder_name + "/" + self.recovery_name

        if not os.path.isfile(self.folder_name + "/" + self.csv_name):
            self.csv_name = self.folder_name + "/" + self.csv_name
            self.lol_data = pd.DataFrame(LolViego.DATA_ESTRUCTURE, index=["championId"])
            self.lol_data.to_csv(self.csv_name, index=False)
        else:
            self.csv_name = self.folder_name + "/" + self.csv_name
            self.lol_data = pd.read_csv(self.csv_name)

    def get_data(
        self,
    ):  # this is for getting a list of players by tier, i will start at platinum and beyond

        for division in self.division_list:
            for tier in self.tier_list:
                for page in self.page_list:
                    time.sleep(1.2)
                    # print(tier)
                    # print(division)
                    # print(page)
                    players_entries = self.leaguev4_get_entries(tier, division, page)
                    time.sleep(1.2)
                    self.requests  +=1
                    for player in players_entries:
                        summoner_id = player["summonerId"]
                        puuid = self.summonerv4_get_summoner_by_id(summoner_id)
                        self.requests  +=1
                        matches = self.matchv5_matchlist(puuid)
                        self.requests  +=1
                        # print(matches)
                        # print(puuid)
                        # print(games)

                        try:

                            for match in matches:
                                # print(match)
                                match_info = self.matchv5_match_info(match)
                                self.requests  +=1
                                print(f'this is request n{self.requests}')
                                for participant in match_info["participants"]:
                                    perks = participant["perks"]
                                    styles = perks["styles"]
                                    perks = []

                                    for style in styles:
                                        selections = style["selections"]
                                        for selection in selections:
                                            perks.append(selection["perk"])

                                    try:
                                        league_data = {
                                            "championId": [participant["championId"]],
                                            "championName": [
                                                participant["championName"]
                                            ],
                                            "item0": [participant["item0"]],
                                            "item1": [participant["item1"]],
                                            "item2": [participant["item2"]],
                                            "item3": [participant["item3"]],
                                            "item4": [participant["item4"]],
                                            "item5": [participant["item5"]],
                                            "spell1": [participant["summoner1Id"]],
                                            "spell2": [participant["summoner2Id"]],
                                            "perk0": [perks[0]],
                                            "perk1": [perks[1]],
                                            "perk2": [perks[2]],
                                            "perk3": [perks[3]],
                                            "perk4": [perks[4]],
                                            "perk5": [perks[5]],
                                            "role": [participant["individualPosition"]],
                                            "lane": [participant["lane"]],
                                            "win": [participant["win"]],
                                            "tier": tier,
                                            "division": division,
                                        }
                                        aux_df = pd.DataFrame(
                                            league_data, index=["championId"]
                                        )
                                        self.lol_data = self.lol_data.append(
                                            aux_df, ignore_index=True
                                        )

                                    except Exception:
                                        print("passing because list out of index")
                                        pass
                                LolViego.x += 1
                                if LolViego.x == 50:
                                    self.lol_data.to_csv(self.csv_name, index=False)
                                    LolViego.x = 0
                                    print("writted after 50")
                                    print(f"{tier}, {division}, {page}")
                                    pass

                        except TypeError as non_iterable:
                            print("[error] matches list was empty")
                            continue

    def leaguev4_get_entries(
        self, tier, division, page
    ):  # returns a list with player info from differents soloq rankeds

        url = f"https://{self.region}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}&api_key={self.api_key}"

        try:
            response = requests.get(url)

            if len(response.json()) == 0:  #  means there was an empty response
                raise BLANKError
            print(f"[success] entries gotten")
            return response.json()

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f"[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}")
            pass

        except BLANKError:  #  response was blank, which could mean that we have reached last page
            print("[error] response was empty, likely last page")
            pass

    def summonerv4_get_summoner_by_id(self, summoner_id):

        url = f"https://{self.region}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={self.api_key}"
        try:
            response = requests.get(url)

            if response.status_code == 400:
                raise IDError
            print(f"[success] puuid gotten")
            # print(response.json()["puuid"])
            return response.json()["puuid"]

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f"[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}")
            pass

        except IDError:
            print("[error] id not found or other error")
            pass

    def matchv5_matchlist(
        self, puuid, count=40
    ):  # this is matches by puuid amd returns a list of ids with
        start_time = int(time.time()) - 604800 * 2  # two weeks from today

        # url = f'https://{self.region_continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&endTime={end_time}&count={count}&api_key={self.api_key}'
        url = f"https://{self.region_continent}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={start_time}&endTime={int(time.time())}&queue=420&type=ranked&start=0&count={count}&api_key={self.api_key}"
        try:
            response = requests.get(url)

            if len(response.json()) == 1:
                print("[warning] did not found recent games")
                return
            if response.status_code != 200:
                raise MATCHESError
            print(f"[success] match list retrived")
            return response.json()

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f"[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}")
            pass

        except MATCHESError:
            print("[error] matches id ")
            pass

    def matchv5_match_info(self, match_id):
        url = f"https://{self.region_continent}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={self.api_key}"
        try:
            response = requests.get(url)

            if response.status_code != 200:
                raise GETTINGMATCHError

            print(f"[success] match info gotten")
            return response.json()["info"]
        except GETTINGMATCHError:
            print("[error] could not get match info")

        except HTTPError as http_err:  #  some serious error like no internet, server error, bad url ec
            print(f"[error] HTTP ERROR OCCURRED(SERIOUS): {http_err}")
            pass


america = LolViego("na1", "I", "DIAMOND", 1)
america.get_data()
