import os

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

def parse_content(content):
    parsed_content = ""
    for item in content:
        if type(item) is NavigableString:
            parsed_content += item.string
        elif type(item) is Tag:
            parsed_content += parse_content(item)
        else:
            print('what is going on')
    return parsed_content

def get_type_info():
    url = os.environ.get('TYPE_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.body.main.p.find_all('a'):
        type = a.string
        yield type.lower()

def build_type_db():
    from pokemon.models import Type

    for type in get_type_info():
        url = os.environ.get('TYPE_URL') + '/' + type
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = parse_content(soup.body.main.p)
        defaults = {
            'description': description
        }
        obj, created = Type.objects.update_or_create(name=type, defaults=defaults)
        if not created:
            print(obj)