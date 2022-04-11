import json
import os
import requests
from tinderapi import TinderDB


class Scavenger:
    def __init__(self, path: str, telegram_key: str, chat_id: str or int, run=True):
        self.path = path
        self.current_pic = None
        self.profile = None
        self.telegram_key = telegram_key
        self.last_message = None
        self.last_message_id = None
        self.current_data = []
        self.count = 0
        self.chat_id = chat_id
        if run:
            self.run()

    def count_photos(self):
        self.count = 0
        for folder in os.listdir(self.path):
            self.count += len(os.listdir(os.path.join(self.path, folder)))
        return self.count

    def run(self):
        db = TinderDB(scavenger=True)
        for folder in os.listdir(self.path):
            list_of_photos = os.listdir(os.path.join(self.path, folder))
            for photo in range(len(list_of_photos)):
                self.current_pic = os.path.join(self.path, folder, list_of_photos[photo])
                self.current_data = db.select_from_table_simple_id(folder, like_option=True)
                if len(self.current_data) == 0:
                    break
                if photo == len(list_of_photos) - 1:
                    self.send_photo(caption='Last Pic!')
                else:
                    self.send_photo(caption=f'{len(list_of_photos) - photo} Pics To Go!')
                self.check_update()
                if self.last_message == 'Like':
                    db.setLike(folder)
                    break
                elif self.last_message == 'Dislike':
                    db.setDislike(folder)
                    break

    def next_update(self):
        url = f'https://api.telegram.org/bot{self.telegram_key}/getUpdates?offset={self.last_message_id + 1}'
        response = requests.get(url)
        print(response.text)

    def check_update(self):
        while True:
            url = f'https://api.telegram.org/bot{self.telegram_key}/getUpdates'
            response = requests.get(url)
            if len(response.json()['result']) > 0:
                targeted_text = ['Like', 'Dislike', 'Next']
                self.last_message = response.json()['result'][len(response.json()['result']) - 1]['message']['text']
                self.last_message_id = response.json()['result'][len(response.json()['result']) - 1]['update_id']
                self.next_update()
                if self.last_message in targeted_text:
                    return 1

    def send_photo(self, caption=None):
        if self.chat_id is None:
            return print('Please add chat_id parameter..')

        url = f'https://api.telegram.org/bot{self.telegram_key}/sendPhoto'
        files = {
            'photo': open(self.current_pic, 'rb').read()
        }

        payload = {
            'chat_id': self.chat_id,
            'caption': self.current_data[0][4] + f' {caption}',
            'reply_markup': json.dumps({
                'keyboard': [
                    [{'text': 'Dislike'}],
                    [{'text': 'Like'}],
                    [{'text': 'Next'}],
                ],
                'resize_keyboard': True,
                'one_time_keyboard': True,
            })

        }

        response = requests.post(url, data=payload, files=files)

        print(response.text)

