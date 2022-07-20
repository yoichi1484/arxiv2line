import requests

DEEPL_FREE_PLAN = False
with open("deepl-api-key.txt") as f:
    AUTH_KEY = f.read()

def deepl(txt, target_lang="JA"):
    """
        Example:
        >>> txt = "Hello world"
        >>> deepl(txt)
        {'translations': [{'detected_source_language': 'EN', 'text': 'ハロー、ワールド'}]}
    """
    assert AUTH_KEY != "", "Create DeepL API account in https://www.deepl.com/docs-api/ \
                            and get the authentication key"
    
    target_lang = "JA"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = 'auth_key={}&text={}&target_lang={}'.format(AUTH_KEY, txt, target_lang)
    
    if DEEPL_FREE_PLAN:
        response = requests.post('https://api-free.deepl.com/v2/translate', headers=headers, data=data) #.json()
    else:
        response = requests.post('https://api.deepl.com/v2/translate', headers=headers, data=data)
        
    assert response != "<Response [403]>"
    response = response.json()
    
    if "message" in response.keys():
        assert response["message"] != "Quota Exceeded", "Quota Exceeded. See https://www.deepl.com/ja/account/usage"
    return response

