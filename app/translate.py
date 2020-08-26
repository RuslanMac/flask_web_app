import json
import requests

from app import app

def translate(text, destLanguage,  sourceLanguage):
    #if 'YANDEX_DICTIONARY_KEY' not in app.config or \
         #   not app.config['YANDEX_DICTIONARY_KEY']:
        #return ('Error: the translation service is not configured.')

        
    r = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=dict.1.1.20200813T170611Z.344edb4fae05f097.9f74cfd69db39bcd1d50fccb83112af2ba5e6290&lang={}-{}&text={}'.format(sourceLanguage, destLanguage, text))
    if r.status_code != 200:
        return ('Error: the translation service failed.')
    
    return json.loads(r.content.decode('utf-8-sig'))

