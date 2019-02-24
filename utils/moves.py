import os

import requests
from bs4 import BeautifulSoup


def get_move_info():
    url = os.environ.get('MOVE_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    for tr in table.find_all('tr'):
        yield tr


def build_move_db():
    from pokemon.models import Move, Type

    for move in get_move_info():
        fields = move.find_all('td')
        name = fields[0].string
        type = fields[1].string
        type_obj = Type.objects.get(name=type.lower())
        category = fields[2].span.attrs['title'] if fields[2].span is not None else None
        power = fields[3].string if fields[3].string != '—' else None
        accuracy = fields[4].string if fields[4].string != '—' else None
        if accuracy == '∞':
            accuracy = 9000
        power_points = fields[5].string if fields[5].string != '—' else 0
        tm = fields[6].string
        effect = fields[7].string
        effect_percent_chance = fields[8].string if fields[8].string != '—' else None
        defaults = {
            'type': type_obj,
            'category': category,
            'power': power,
            'accuracy': accuracy,
            'power_points': power_points,
            'tm': tm,
            'effect': effect,
            'effect_percent_chance': effect_percent_chance
        }
        obj, created = Move.objects.update_or_create(name=name, defaults=defaults)
        if not created:
            print(obj)
