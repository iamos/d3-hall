import requests
from requests_oauthlib import OAuth2Session

SEASON_INDEX = 'https://kr.api.battle.net/data/d3/season/'
CLIENT_ID = '5pwmkukwsnanwx57en88nfnxacvtrs2j'
CLIENT_SECRET = 'v5fhvAbgApQtAMhzhHcp5xxuW3ZvxeX6'
AUTH_CODE = 'f6tpcndqnp22c72y4e9w375s'
ACCESS_TOKEN = '8xbxxjd83xdh935gmwa7p3xg'
TOKEN_QUERY = '?access_token=8xbxxjd83xdh935gmwa7p3xg'
RIFT_LEADERBOARD = '/leaderboard/rift-'

'https://kr.api.battle.net/data/d3/season/14/leaderboard/rift-barbarian'


def get_season_rift_leaderboard(season_index, class_id):
    full_url = SEASON_INDEX+str(season_index)+RIFT_LEADERBOARD+class_id+TOKEN_QUERY
    r = requests.get(url=full_url)
    payload = r.json()['row']
    parsing_result = []
    for x in payload:
        row = {
            'player_account_id': x['player'][0]['accountId'],
            'player_hero_class': x['player'][0]['data'][2]['string'],
            'player_battle_tag': x['player'][0]['data'][0]['string'],
            'player_paragon_level': x['player'][0]['data'][5]['number'],
            'data_rift_level': x['data'][1]['number'],
            'data_rift_time': x['data'][2]['timestamp'],
            'data_completed_time': x['data'][3]['timestamp'],
        }
        if len(x['player'][0]['data']) == 9:
            row['player_hero_id'] = x['player'][0]['data'][8]['number']
        else:
            row['player_hero_id'] = x['player'][0]['data'][6]['number']

        parsing_result.append(row)
    ret = {'count': len(parsing_result), 'payload': parsing_result}
    return ret


def get_season_rift_leaderboard_all(season_index):
    barbarian = get_season_rift_leaderboard(season_index=season_index,
                                            class_id='barbarian')
    monk = get_season_rift_leaderboard(season_index=season_index,
                                       class_id='monk')
    wd = get_season_rift_leaderboard(season_index=season_index,
                                     class_id='wd')
    dh = get_season_rift_leaderboard(season_index=season_index,
                                     class_id='dh')
    wizard = get_season_rift_leaderboard(season_index=season_index,
                                         class_id='wizard')
    crusader = get_season_rift_leaderboard(season_index=season_index,
                                           class_id='crusader')
    necromancer = get_season_rift_leaderboard(season_index=season_index,
                                              class_id='necromancer')
    total = barbarian['count']+monk['count']+wd['count']+dh['count'] + \
        wizard['count']+crusader['count']+necromancer['count']
    payload = barbarian['payload']+monk['payload']+wd['payload'] + \
        dh['payload'] + wizard['payload']+crusader['payload'] + \
        necromancer['payload']
    return {'count': total, 'payload': payload}


def main():
    r = get_season_rift_leaderboard_all(season_index=14)
    print(r['count'])
    # for x in r['payload']:
    #     print(x)


if __name__ == '__main__':
    main()
