'''Utility functions used to populate type db information
'''

import os

import requests
from bs4 import BeautifulSoup

from utils import db_utils


def get_type_info():
    '''Function that creates a generator of BeautifulSoup objects correspondoning to an individual type
    '''

    url = os.environ.get('TYPE_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.body.main.p.find_all('a'):
        yield str(a.string).lower()

def build_types_db():
    '''Updates or creates type based on info from supplied by get_type_info()
    '''

    from pokemon.models import Type

    for type in get_type_info():
        url = os.environ.get('TYPE_URL') + '/' + type
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = db_utils.parse_content(soup.body.main.p)
        defaults = {
            'name': type.upper(),
            'description': description.upper()
        }
        obj, created = Type.objects.update_or_create(name__iexact=type, defaults=defaults)
        if not created:
            print("Updated {} with {}".format(obj.name, defaults))
