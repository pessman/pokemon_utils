'''Utility functions used to populate item db information
'''

import os

import requests
from bs4 import BeautifulSoup


def get_item_info():
    '''Function that creates a generator of BeautifulSoup objects correspondoning to an individual item
    '''

    url = os.environ.get('ITEM_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.find('table').tbody.find_all('tr'):
        yield item


def build_items_db():
    '''Updates or creates item based on info from supplied by get_item_info()
    '''

    from pokemon.models import Item

    for item in get_item_info():
        fields = item.find_all('td')
        name = fields[0].a.string
        category = fields[1].string
        effect = fields[2].string
        defaults = {
            'name': name,
            'category': category.upper() if category is not None else None,
            'effect': effect
        }
        obj, created = Item.objects.update_or_create(name=name, defaults=defaults)
        if not created:
            print(obj)
