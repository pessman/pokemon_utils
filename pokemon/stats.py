import operator
from math import floor

from django.forms.models import model_to_dict

STATS = ['hit_points', 'attack', 'defense',
         'special_attack', 'special_defense', 'speed']


class InternalValues:

    def __init__(self, ivs):
        for key in ivs:
            assert key in STATS, "Invalid IV key, possible keys: {}".format(
                STATS)
            assert ivs[key] >= 0 and ivs[key] <= 31, "Invalid IV value, must be between 0 and 31"

        self.hit_points = ivs.get('hit_points')
        self.attack = ivs.get('attack')
        self.defense = ivs.get('defense')
        self.special_attack = ivs.get('special_attack')
        self.special_defense = ivs.get('special_defense')
        self.speed = ivs.get('speed')

    def get_attr(self, attribute):
        return getattr(self, attribute, None)


class EffortValues:

    def __init__(self, evs):
        for key in evs:
            assert key in STATS, "Invalid EV key, possible keys: {}".format(
                STATS)
            assert evs[key] >= 0 and evs[key] <= 255, "Invalid IV value, must be between 0 and 255"
        self.hit_points = evs.get('hit_points')
        self.attack = evs.get('attack')
        self.defense = evs.get('defense')
        self.special_attack = evs.get('special_attack')
        self.special_defense = evs.get('special_defense')
        self.speed = evs.get('speed')

    def get_attr(self, attribute):
        return getattr(self, attribute, None)


class Stats:

    def __init__(self, pokemon_id, ivs, evs, level, nature):

        self.pokemon_id = pokemon_id
        self.ivs = ivs
        self.evs = evs
        self.level = level
        self.nature = nature
        self.values = self.get_stats(pokemon_id, ivs, evs, level, nature)

    @classmethod
    def get_level_contribution(self, pokemon_base, iv, ev, level):
        return floor(level * (2 * pokemon_base + iv + floor(ev / 4)) / 100)

    @classmethod
    def get_hp(self, pokemon_base, iv, ev, level):
        free_stats = level + 10
        level_stats = self.get_level_contribution(pokemon_base, iv, ev, level)
        return level_stats + free_stats

    @classmethod
    def get_other_stats(self, pokemon_base, iv, ev, level, nature, stat):
        from pokemon.models import Nature
        nat = Nature.objects.get(name=nature)
        if not nat:
            raise StatsError("No nature found with name {}".format(nat))

        level_stats = self.get_level_contribution(pokemon_base, iv, ev, level)

        return {stat: floor((level_stats + 5) * nat.modifier(stat))}

    @classmethod
    def get_stats(self, pokemon_id, ivs, evs, level, nature):
        from pokemon.models import Pokemon
        pokemon = Pokemon.objects.filter(id=pokemon_id).first()
        if not pokemon:
            raise StatsError("No pokemon found with id {}".format(pokemon_id))

        pokemon_base = model_to_dict(pokemon, fields=[field.lower() for field in STATS])
        values ={
            'hit_points': self.get_hp(pokemon.hit_points, ivs.hit_points, evs.hit_points, level)
        }

        for stat in STATS[1:]:
            other_value = self.get_other_stats(pokemon_base.get(stat.lower()), ivs.get_attr(stat.lower()), evs.get_attr(stat.lower()), level, nature, stat.title())
            values = {
                **values,
                **other_value
            }

        return values
