'''Utility functions used to populate pokemon db information
'''
import os

import requests
from bs4 import BeautifulSoup


def get_pokemon_info():
    '''Function that creates a generator of BeautifulSoup objects correspondoning to an individual pokemon
    '''

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
    '''Updates or creates pokemon based on info from supplied by get_pokemon_info()
    '''

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
        obj.type.clear()
        for type in types:
            obj.types.add(Type.objects.get(name=type.lower()))
        obj.save()
        if not created:
            print(obj)


def get_abilities():
    '''Updated pokemon objects to have a relationship with their respective abilities
    '''

    from pokemon.models import Ability, Pokemon

    abilities = Ability.objects.all()
    for ability in abilities:
        url = os.environ.get('ABILITY_URL') + '/' + ability.name.replace(' ', '-')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        print(ability)
        for table in tables:
            if 'data-table' in table.attrs['class']:
                if ability.name in ['Iron Fist', 'Mega Launcher', 'Multitype', 'Reckless', 'Simple', 'Strong Jaw']:
                    if table.thead.tr.th.string in ['Name', 'Plate', 'Stage']:
                        continue
                rows = table.tbody.find_all('tr')
                for row in rows:
                    fields = row.find_all('td')
                    pokedex = fields[0].find_all('span')[2].string
                    form = None
                    if fields[1].find('small'):
                        name = fields[1].a.string
                        form = fields[1].small.string
                    else:
                        name = fields[1].string
                    pokemon = Pokemon.objects.get(pokedex=pokedex, name=name, form=form)
                    pokemon.abilities.add(ability)
                    print(pokemon)


def reset_pokemon_relations():
    '''Reset the many to many field relations for all pokemon
    '''

    from pokemon.models import Pokemon
    for pokemon in Pokemon.objects.all():
        pokemon.abilities.clear()
        pokemon.types.clear()
        pokemon.moves.clear()
        pokemon.save()