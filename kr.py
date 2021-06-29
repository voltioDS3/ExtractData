from matchv5 import DataLeague
PAGES = {
    'DIAMOND': {
        'I': [x for x in range(1, 26)],
        'II': [x for x in range(1, 33)],
        'III': [x for x in range(1, 52)],
        'IV': [x for x in range(1, 119)],},
    'PLATINUM': {    
        'I': [x for x in range(1, 229)],
        'II': [x for x in range(1, 261)],
        'III': [x for x in range(1, 428)],
        'IV': [x for x in range(1, 1090)],},
    'GOLD': {
        'I': [x for x in range(1, 686)],
        'II': [x for x in range(1, 1129)],
        'III': [x for x in range(1, 1451)],
        'IV': [x for x in range(1, 2793)],
    },
}
 
euw = DataLeague(PAGES=PAGES, REGION='KR')
euw.get_data()