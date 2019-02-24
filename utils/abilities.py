'''Utility functions used to populate ability db information
'''

import os

import requests
from bs4 import BeautifulSoup

from utils import db_utils


def get_ability_info():
    '''Function that creates a generator of BeautifulSoup objects correspondoning to an individual ability
    '''

    url = os.environ.get('ABILITY_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for ability in soup.find('table').tbody.find_all('tr'):
        yield ability


def build_abilities_db():
    '''Updates or creates ability based on info from supplied by get_ability_info()
    '''

    from pokemon.models import Ability

    for ability in get_ability_info():
        fields = ability.find_all('td')
        name = fields[0].a.string
        description = db_utils.parse_content(fields[2])
        defaults = {
            'name': name,
            'description': description
        }
        obj, created = Ability.objects.update_or_create(
            name=name, defaults=defaults)
        if not created:
            print(obj)
