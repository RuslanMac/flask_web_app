import json
import requests

from app import app

def translate(  text, sourcelang, destlang):
    #if 'YANDEX_DICTIONARY_KEY' not in app.config or \
         #   not app.config['YANDEX_DICTIONARY_KEY']:
        #return ('Error: the translation service is not configured.')
   
    r = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='+'dict.1.1.20200605T183314Z.3f68bf85373047a7.106fe3bc6e45ae73303fc9e8dbb488a518f23588'+'&lang={}-{}&text={}'.format(sourcelang,destlang,text))
    
    if r.status_code != 200:
        return ('Error: the translation service failed.')
    
    return json.loads(r.content.decode('utf-8-sig'))

