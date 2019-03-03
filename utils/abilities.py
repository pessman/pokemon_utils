'''Utility functions used to populate ability db information
'''

import os

import requests
from bs4 import BeautifulSoup

from utils import db_utils

def get_ability(url):
    response = requests.get(url)
    if response.status_code != 200:
        return (None, None)
    soup = BeautifulSoup(response.text, 'html.parser')
    for table in [table for table in soup.find_all('table') if table.attrs.get('class') and 'dextable' in table.attrs.get('class')][1:2]:
        rows = table.find_all('tr')
        return(rows[1].find_all('td')[0].string, ' '.join([item.encode('ascii', 'ignore').decode('utf-8') for item in rows[3].find_all('td')[0].string.split()]))




def get_ability_info():
    '''Function that creates a generator of BeautifulSoup objects correspondoning to an individual ability
    '''

    url = os.environ.get('ABILITY_URL')
    response = requests.get(url)
    if response.status_code != 200:
        yield None
    soup = BeautifulSoup(response.text, 'html.parser')
    for ability_list in [form for form in soup.find_all('form') if form.attrs.get('name') and form.attrs.get('name').upper() in ['ABILITY', 'ABILITY2']]:
        for ability in ability_list.find_all('option')[1:]:
            ability_url = url + ability.attrs.get('value').split('/')[2]
            yield get_ability(ability_url)





def build_abilities_db():
    '''Updates or creates ability based on info from supplied by get_ability_info()
    '''

    from pokemon.models import Ability

    for ability in get_ability_info():
        if ability[0] is None or ability[1] is None:
            continue
        name = ability[0]
        description = ability[1]
        defaults = {
            'name': name,
            'description': description
        }
        obj, created = Ability.objects.update_or_create(
            name=name, defaults=defaults)
        if not created:
            print("Updated {} with {}".format(obj.name, defaults))
