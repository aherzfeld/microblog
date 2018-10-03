import json
import requests  # HTTP client for Python
from flask_babel import _
from app import app


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    # create dict with custom HTTP header info needed by API
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
    # sends HTTP request with GET arg to URL given as first arg
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    # json.loads decodes JSON into Python string
    # the content attribute of response object contains raw body of the response as a bytes object, which is converted to a UTF-8 string and sent to json.loads()
    return json.loads(r.content.decode('utf-8-sig'))
