from matchv5 import DataLeague
PAGES = {
    'DIAMOND': {
        'I': [x for x in range(1, 45)],
        'II': [x for x in range(1, 45)],
        'III': [x for x in range(1, 59)],
        'IV': [x for x in range(1, 102)],},
    'PLATINUM': {    
        'I': [x for x in range(1, 218)],
        'II': [x for x in range(1, 216)],
        'III': [x for x in range(1, 300)],
        'IV': [x for x in range(1, 719)],},
    'GOLD': {
        'I': [x for x in range(1, 511)],
        'II': [x for x in range(1, 735)],
        'III': [x for x in range(1, 841)],
        'IV': [x for x in range(1, 1700)],
    },
}
 
euw = DataLeague(PAGES=PAGES, REGION='EUW1')
euw.get_data()