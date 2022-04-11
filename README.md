## Tinder API Reverse Engineering

Tinder API is a library that helps you deal with tinder without using the browser also in future version it will have an AI class that will help you train/test your model with simple steps

## Installation

Use the package manager [tinder-api](https://pypi.org/project/tinderapi/) to install foobar.

```bash
pip install tinderapi
```

## The Purpose Of The Library

Create an AI Model that decide a binary choice 1 = Like and 0 = Dislike based on a database created using tinder database. This library will create a database using SQLite by delaut called Tinder.db were all the data will be stored

To prepare your database for training you can use ```scave.py``` 

```python
from tinderapi import Scavenger
import json

ACCOUNT = json.loads(open('account.json', 'r').read())

scavenger = Scavenger('Photos', ACCOUNT['telegram_bot_access_token'], ACCOUNT['chat_id'])
```

When ```scave.py``` is running you'll receive one picture for a random user and you'll get 3 choices (like, dislike and next)

- Like: change like stat in the DB to 1
- Dislike: change like stat in the DB to -1
- Next: get the next picture (if it's the last photo it will skip the user)



## Usage

Change Tinder X-AUTH-TOKEN and create a Telegram Bot to receive LIVE Update in ```account.json```

- tinder_auth: open google chrome devtool and search into request headers for x-auth-token

- telegram_bot_access_token: create a bot using bot father https://web.telegram.org/z/#93372553

- chat_id: send a message to the bot and check your is in api.telegram.org/bot{your_access_token}/getUpdates 

- group_id: create a group and add the bot to it you'll find the group_id in api.telegram.org/bot{your_access_token}/getUpdates (it's always a negative number)

```json 
{
  "tinder_auth": "cb10ca8b-xxxx-xxxx-xxxx",
  "telegram_bot_access_token": "51xxx83571:xxxxxxxxxxxxxxx",
  "chat_id": 543000000,
  "group_id": -718000000
}
```

## Example

```python
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
                profile.like() # for dislike profile.dislike()
                telegram.sendPhoto(f'{profile.name} - {profile.birth_date.split("-")[0]} - {profile.distance_km} KM',
                                   f'Photos/{profile.id}')
                DB.insert_into_table(profile)

                time.sleep(random.randint(1, 4))

        print('Searching New Matches...')
        telegram.sendMessage('Searching for new matches...')


if __name__ == '__main__':
    liker()


```

## To-Do

 - Add TensorFlow simplfied classes for Tinder
 - Finish first Ai Model
 - Host The app on a Django server
 - much more

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
