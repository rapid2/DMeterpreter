# This file contains only utility and helper functions
import json
import re
import requests
from lxml import html, etree


def load_json(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data


def normalize_text(_text):
    _text = re.sub('\t', ' ', _text)
    _text = re.sub('\n', ' ', _text)
    _text = re.sub('\r', ' ', _text)
    _text = re.sub('\xa0', ' ', _text)
    _text = re.sub('&nbsp;', ' ', _text)
    _text = re.sub('&nbsp', ' ', _text)
    _text = re.sub('\u200b', ' ', _text)
    _text = re.sub(' +', ' ', _text)
    _text = _text.strip()
    return _text


def dom_from_url(_url, params=None, preferred_encoding=None):
    try:
        with requests.get(
                _url,
                allow_redirects=True,
                params=params,
                headers={
                    'Accept': '*/*',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/84.0.4147.89 Safari/537.36'
                },
                timeout=90
        ) as response:
            # if urlparse(response.url).netloc != urlparse(_url).netloc:
            #     return False

            _content = response.content
    except Exception as e:
        print(e)
        return False

    try:
        _content = _content.decode(get_encoding(response, preferred_encoding), 'ignore')
    except UnicodeDecodeError:
        pass
    except Exception as e:
        print(e)
        return False

    _dom = html.document_fromstring(_content)
    return _dom


def get_encoding(response, preferred_encoding=None):
    # checking following types
    # header "Content-Type": "text/html; charset=UTF-8"
    # <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    # <meta charset="UTF-8">

    encoding_types = ['utf-8', 'UTF-8', 'windows-1251', 'WINDOWS-1251', 'ISO-8859-1', 'iso-8859-1']

    if preferred_encoding and preferred_encoding in encoding_types:
        return preferred_encoding

    for encoding_type in encoding_types:
        if encoding_type in response.headers['Content-Type']:
            return encoding_type.lower()

    dom = html.document_fromstring(response.content)

    meta_tag = dom.cssselect('meta[http-equiv="Content-Type"]')
    if meta_tag:
        for encoding_type in encoding_types:
            if encoding_type in meta_tag[0].get('content'):
                return encoding_type.lower()

    meta_tag = dom.cssselect('meta[charset]')
    if meta_tag:
        for encoding_type in encoding_types:
            if encoding_type in meta_tag[0].get('charset'):
                return encoding_type.lower()

    # default charset before html5 was 'windows-1251'
    return 'windows-1251'

