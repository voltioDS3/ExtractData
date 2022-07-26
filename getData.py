from tkinter import PAGES
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time
import keyboard
import os
from viego import LolViego

class LeagueData:
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

    def __init__(self, PAGES, REGION):
        self.PAGES = PAGES
        self.REGION = REGION
        self.REGION_NAME = LeagueData.REGION_MAP[self.REGION]
        self.folder_region = self.REGION + "_DATA"
        self.csv_name = self.REGION + "_DATA.csv"
        self.recovery_name = self.REGION + "_RECOVERY.txt"

        