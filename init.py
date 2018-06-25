import requests
import time
from requests_oauthlib import OAuth2Session

SEASON_INDEX = 'https://kr.api.battle.net/data/d3/season/'
CLIENT_ID = '5pwmkukwsnanwx57en88nfnxacvtrs2j'
CLIENT_SECRET = 'v5fhvAbgApQtAMhzhHcp5xxuW3ZvxeX6'
AUTH_CODE = 'f6tpcndqnp22c72y4e9w375s'
ACCESS_TOKEN = '8xbxxjd83xdh935gmwa7p3xg'
TOKEN_QUERY = '?access_token='+ACCESS_TOKEN
RIFT_LEADERBOARD = '/leaderboard/rift-'


def get_season_rift_leaderboard(season_index, class_id):
    full_url = SEASON_INDEX+str(season_index)+RIFT_LEADERBOARD+class_id+TOKEN_QUERY
    r = requests.get(url=full_url)
    payload = r.json()['row']
    parsing_result = []
    for x in payload:
        row = {
            'account_id': x['player'][0]['accountId'],
            'hero_class': x['player'][0]['data'][2]['string'],
            'battle_tag': x['player'][0]['data'][0]['string'],
            'paragon_level': x['player'][0]['data'][5]['number'],
            'grift_level': x['data'][1]['number'],
            'grift_time': x['data'][2]['timestamp'],
            'completed_time': x['data'][3]['timestamp'],
        }
        if len(x['player'][0]['data']) == 9:
            row['hero_id'] = x['player'][0]['data'][8]['number']
        else:
            row['hero_id'] = x['player'][0]['data'][6]['number']

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
    sorted_payload = sorted(payload, key=lambda k: (-(k['grift_level']), k['grift_time']))
    return {'count': total, 'payload': sorted_payload}


def get_hero_items(battle_tag, hero_id):
    full_url = 'https://kr.api.battle.net/d3/profile/'+battle_tag+'/hero/' + \
        str(hero_id)+'/items?locale=ko_KR&apikey=5pwmkukwsnanwx57en88nfnxacvtrs2j'
    r = requests.get(url=full_url)
    print(r.text)
    # Littleindian%233237
    # 70458621


def print_this(leaderboard_row):
    time_consumed = leaderboard_row['grift_time'] / 1000.0
    consumed_minute = int(time_consumed // 60)
    consumed_second = round(time_consumed % 60, 3)

    epoch_completed_time = leaderboard_row['completed_time']
    completed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_completed_time/1000))
    print("{battle_tag} ({paragon_level}) {hero_class}, RIFT {grift_level} {min}분{sec}초 ({completed_time})".format(
        battle_tag=leaderboard_row['battle_tag'],
        paragon_level=leaderboard_row['paragon_level'],
        hero_class=leaderboard_row['hero_class'],
        grift_level=leaderboard_row['grift_level'],
        grift_time=leaderboard_row['grift_time'],
        min=consumed_minute,
        sec=consumed_second,
        # completed_time=leaderboard_row['completed_time'],
        completed_time=completed_time
    ))


def main():
    r = get_season_rift_leaderboard_all(season_index=14)
    rows = r['payload']

    for x in rows:
        print_this(leaderboard_row=x)

    # r = get_season_rift_leaderboard(season_index=14, class_id='wizard')
    # for x in r['payload']:
    #     print(x)
    #     print_this(x)


if __name__ == '__main__':
    main()
