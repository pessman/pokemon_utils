import os

import requests
from bs4 import BeautifulSoup


def get_pokemon_info():
    url = os.environ.get('POKEMON_URL')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    for table in tables:
        pokedex = table if table.attrs['id'] == 'pokedex' else None
        if pokedex:
            break
    for pokemon in pokedex.tbody.find_all('tr'):
        yield(pokemon)

def build_pokemon_db():
    from pokemon.models import Pokemon, Type

    for pokemon in get_pokemon_info():
        fields = pokemon.find_all('td')
        pokedex = fields[0].find_all('span')[2].string
        form = None
        if fields[1].find('small'):
            name = fields[1].a.string
            form = fields[1].small.string
        else:
            name = fields[1].string
        types = [field.string for field in fields[2].find_all('a')]
        hit_points = fields[4].string
        attack = fields[5].string
        defense = fields[6].string
        special_attack = fields[7].string
        special_defense = fields[8].string
        speed = fields[9].string
        defaults = {
            'hit_points': hit_points,
            'attack': attack,
            'defense': defense,
            'special_attack': special_attack,
            'special_defense': special_defense,
            'speed': speed
        }
        obj, created = Pokemon.objects.update_or_create(pokedex=pokedex, name=name, form=form, defaults=defaults)
        for type in types:
            obj.types.add(Type.objects.get(name=type).id)
        obj.save()
        if not created:
            print(obj)
