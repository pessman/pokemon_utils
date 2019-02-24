import os

import requests
from bs4 import BeautifulSoup


def get_item_info():
    url = os.environ.get('ITEM_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    for tr in table.find_all('tr'):
        yield tr

def build_items_db():
    from pokemon.models import Item

    for item in get_item_info():
        fields = item.find_all('td')
        name = fields[0].a.string
        category = fields[1].string
        effect = fields[2].string
        defaults = {
            'category': category.upper() if category is not None else None,
            'effect': effect
        }
        obj, created = Item.objects.update_or_create(name=name, defaults=defaults)
        if not created:
            print(obj)
