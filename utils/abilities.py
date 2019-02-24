import os

import requests
from bs4 import BeautifulSoup


def get_ability_info():
    url = os.environ.get('ABILITY_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    for tr in table.find_all('tr'):
        yield tr


def build_abilities_db():
    from pokemon.models import Ability

    for ability in get_ability_info():
        fields = ability.find_all('td')
        name = fields[0].a.string
        if len(fields[2]) > 1:
            # Special Case for Soundproof description
            description = fields[2].contents[0] + "'" + fields[2].q.string + "'" + fields[2].contents[2]
        else:
            description = fields[2].string
        defaults = {
            'description': description
        }
        obj, created = Ability.objects.update_or_create(name=name, defaults=defaults)
        if not created:
            print(obj)
