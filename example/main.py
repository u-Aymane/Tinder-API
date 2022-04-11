import time
from tinderapi import Tinder, TinderProfile, TinderDB, Telegram
import random
import json

ACCOUNT = json.loads(open('account.json', 'r').read())

AUTH_TOKEN = ACCOUNT['tinder_auth']
DB = TinderDB()


def liker():
    while True:
        TinderAcc = Tinder(AUTH_TOKEN)
        telegram = Telegram(telegram_key=ACCOUNT['telegram_bot_access_token'], chat_id=ACCOUNT['group_id'])
        matches = TinderAcc.get_potential_matches(verbose=False)
        if matches == -1:
            break
        elif matches == 2:
            telegram.sendMessage('Timeout waiting 5 min')
            time.sleep(60 * 5)
        else:
            for potential_match in matches:
                profile = TinderProfile(potential_match, AUTH_TOKEN, save_pics=True)
                print(profile.getAll())
                profile.like()
                telegram.sendPhoto(f'{profile.name} - {profile.birth_date.split("-")[0]} - {profile.distance_km} KM',
                                   f'Photos/{profile.id}')
                DB.insert_into_table(profile)

                time.sleep(random.randint(1, 4))

        print('Searching New Matches...')
        telegram.sendMessage('Searching for new matches...')


if __name__ == '__main__':
    liker()
