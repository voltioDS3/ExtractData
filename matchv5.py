
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time
import keyboard
import os

# first do a entries like normal and get the summoner id
# then with the summoner id do a summoner.by encrypted summoner id, and get de puuid




                    




class DataLeague:
    x = 0
    REGION_MAP ={
        'EUW1': 'EUROPE',
        'LA2': 'AMERICAS',
        'NA1': 'AMERICAS',
        'KR' : 'ASIA',
    }

    data_structure = {
    'championId': [0], 
    'championName': [0],
    'item0': [0],
    'item1': [0],
    'item2': [0],
    'item3': [0],
    'item4': [0],
    'item5': [0],
    'spell1': [0],
    'spell2': [0],
    'perk0': [0],
    'perk1': [0],
    'perk2': [0],
    'perk3': [0],
    'perk4': [0],
    'perk5': [0],
    'role': [0],
    'lane': [0],
    'win': [0],
}
    tries = 5
    def __init__(self, PAGES, REGION):
        self.PAGES = PAGES
        self.REGION = REGION
        self.REGION_NAME = DataLeague.REGION_MAP[self.REGION]
        self.folder_name = self.REGION + "_DATA"
        self.csv_name = self.REGION + "_DATA.csv"
        self.recovery_name = self.REGION + "_RECOVERY.txt"
        with open('api_key.txt', 'r') as f:
            key = f.read()
            self.lol_watcher = LolWatcher(key)
        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)
        
        if not os.path.isfile(self.folder_name+'/'+self.recovery_name):
            with open(self.folder_name+'/'+self.recovery_name, 'w+') as f:
                f.write('first')
        else:
            self.recovery_name = self.folder_name+'/'+self.recovery_name
        
        if not os.path.isfile(self.folder_name+'/'+self.csv_name):
            self.csv_name = self.folder_name+'/'+self.csv_name
            self.lol_data = pd.DataFrame(DataLeague.data_structure, index=['championId'])
            self.lol_data.to_csv(self.csv_name,index=False)
        else:
            self.csv_name = self.folder_name+'/'+self.csv_name
            self.lol_data = pd.read_csv(self.csv_name)
    
    def change_key(self):
        with open('api_key.txt', 'r') as f:
            key = f.read()
            self.lol_watcher = LolWatcher(key)
    
    def check(self):
            if keyboard.is_pressed('ctrl+alt+0'):
                print('time to change the key, please, DO NOTPRESS ESC AND EDIT THE FILE WITH THE API KEY ON IT')
                keyboard.wait('esc')
                with open('api_key.txt', 'r') as f:
                    key = f.read()
                    self.lol_watcher = LolWatcher(key)
                time.sleep(10)

    def get_data(self):
        for TIER in self.PAGES.keys():
            for DIVISION in self.PAGES[TIER].keys():
                for PAGE in self.PAGES[TIER][DIVISION]:
                    self.check()
                    time.sleep(1.2)
                    players = self.get_players(TIER, DIVISION, PAGE)

                    for player in players:
                        self.check()
                        time.sleep(1.2)
                        summoner_id = player['summonerId']
                        self.check()
                        puuid = self.get_puuid(summoner_id=summoner_id)
                        time.sleep(1.2)
                        matches = self.get_matches(puuid=puuid)

                        for match in matches:
                                self.check()
                                match_data = self.get_match_info(match)
                                if match_data != False:
                                    self.check()
                                    for participant in match_data['participants']:
                                        # print(participant['championName'])
                                        perks = participant['perks']
                                        styles = perks['styles']
                                        perks = []
                                        self.check()
                                       
                                        for style in styles:
                                            selections = style['selections']
                                            for selection in selections:
                                                perks.append(selection['perk'])
                                        try:
                                            league_data = {
                                                'championId': [participant['championId']],        
                                                'championName': [participant['championName']],
                                                'item0': [participant['item0']],
                                                'item1': [participant['item1']],
                                                'item2': [participant['item2']],
                                                'item3': [participant['item3']],
                                                'item4': [participant['item4']],
                                                'item5': [participant['item5']],
                                                'spell1': [participant['summoner1Id']],
                                                'spell2': [participant['summoner2Id']],
                                                'perk0': [perks[0]],
                                                'perk1': [perks[1]],
                                                'perk2': [perks[2]],
                                                'perk3': [perks[3]],
                                                'perk4': [perks[4]],
                                                'perk5': [perks[5]],
                                                'role': [participant['role']],
                                                'lane': [participant['lane']],
                                                'win': [participant['win']],
                                                            }
                                          
                                            aux_df = pd.DataFrame(league_data, index=['championId'])
                                            self.lol_data = self.lol_data.append(aux_df, ignore_index=True)
                                            print(league_data)
                                            league_data.clear()
                                            print(f'{league_data} this is after the clear')
                                            
                                            self.check()
                                        except Exception:
                                            print('passing because list out of index')
                                            pass
                                    DataLeague.x += 1
                                    if DataLeague.x == 50:
                                        self.lol_data.to_csv(self.csv_name, index=False)
                                        DataLeague.x = 0
                                        print('writted after 5')
                                        print(f'{TIER}, {DIVISION}, {PAGE}')
                                    
                                else:
                                    print('passing to other thing man')
                                    pass                  
                                
                                    

    def get_players(self, tier, division, page):
        while True:
            for i in range(DataLeague.tries):
                try:
                    players = self.lol_watcher.league.entries(region=self.REGION, queue='RANKED_SOLO_5x5', tier=tier, division=division, page=page)
                    print('[succes] players')
                    return players
                except Exception:
                    if i < DataLeague.tries - 1:
                        continue
                    else:
                        print('[error] players')
                        a = input('type something and enter to continue')
                        self.change_key()
                break
    
    def get_puuid(self, summoner_id):
        while True:
            for i in range(DataLeague.tries):
                try:
                    puuid = self.lol_watcher.summoner.by_id(region=self.REGION, encrypted_summoner_id=summoner_id)['puuid']
                    print('[succes] puuid')
                    return puuid
                except Exception:
                    if i < DataLeague.tries - 1:
                        continue
                    else:
                        print('[error] puuid')
                        a = input('type something and enter to continue')
                        self.change_key()
                break

    def get_matches(self, puuid):
        while True:
            for i in range(DataLeague.tries):
                try:
                    matches = self.lol_watcher.matchv5.matchlist_by_puuid(region=self.REGION_NAME, puuid=puuid)
                    print('[succes] matches')
                    return matches
                except Exception:
                    if i < DataLeague.tries - 1:
                        continue
                    else:
                        print('[error] matches')
                        a = input('type something and enter to continue')
                        self.change_key()
                        
                break

    def get_match_info(self, match):
        while True:
            for i in range(DataLeague.tries):
                try:
                    match_data = self.lol_watcher.matchv5.by_id(region=self.REGION_NAME, match_id=match)['info']
                    print('[succes] match_data')
                    return match_data
                except Exception:
                    if i < DataLeague.tries - 1:
                        continue
                    else:
                        print('[error] match_data')
                        
                        self.change_key()
                        return False
                break
                
                

        
        







