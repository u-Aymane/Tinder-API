import os
import requests


class Telegram:
    def __init__(self, telegram_key: str, chat_id: str or int):
        self.telegram_key = telegram_key
        self.chat_id = chat_id

    def sendPhoto(self, caption, photo_path, verbose=False):
        url = f'https://api.telegram.org/bot{self.telegram_key}/sendPhoto'
        try:
            files = {
                'photo': open(f'{photo_path}/{os.listdir(photo_path)[0]}', 'rb').read()
            }
        except Exception as e:
            if verbose:
                print(f'error: {e}')
            return 2

        payload = {
            'chat_id': self.chat_id,
            'caption': caption,
        }

        response = requests.post(url, data=payload, files=files)
        print('Message sent...')
        return response.text

    def sendMessage(self, message):
        url = f'https://api.telegram.org/bot{self.telegram_key}/sendMessage'

        payload = {
            'chat_id': self.chat_id,
            'text': message,
        }

        response = requests.post(url, data=payload)
        print('Message sent...')
        return response.text
