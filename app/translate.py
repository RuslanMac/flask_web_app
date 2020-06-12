import json
import requests

from app import app

def translate(  text):
    if 'YANDEX_DICTIONARY_KEY' not in app.config or \
            not app.config['YANDEX_DICTIONARY_KEY']:
        return ('Error: the translation service is not configured.')
   
    r = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='+str(YANDEX_DICTIONARY_KEY)+'&lang=en-ru&text={}'.format(text))
    
    if r.status_code != 200:
        return ('Error: the translation service failed.')
    
    return json.loads(r.content.decode('utf-8-sig'))

