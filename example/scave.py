from tinderapi import Scavenger
import json

ACCOUNT = json.loads(open('account.json', 'r').read())

scavenger = Scavenger('Photos', ACCOUNT['telegram_bot_access_token'], ACCOUNT['chat_id'])
