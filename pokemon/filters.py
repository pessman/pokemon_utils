from django_filters import rest_framework as filters

from pokemon.models import Ability, Item, Move, Nature, Pokemon, Type


class AbilityFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='name')

    class Meta:
        model = Ability
        fields = ['name']


class ItemFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='name')
    category = filters.CharFilter(
        field_name='category', lookup_expr='icontains', label='category')

    class Meta:
        model = Item
        fields = ['name', 'category']


class MoveFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='name')
    type = filters.CharFilter(
        field_name='type', lookup_expr='name__icontains', label='type')
    category = filters.CharFilter(
        field_name='category', lookup_expr='icontains', label='category')
    power_gte = filters.NumberFilter(
        field_name='power', lookup_expr='gte', label='power_gte')
    power_lte = filters.NumberFilter(
        field_name='power', lookup_expr='lte', label='power_lte')
    accuracy_gte = filters.NumberFilter(
        field_name='accuracy', lookup_expr='gte', label='accuracy_gte')
    accuracy_lte = filters.NumberFilter(
        field_name='accuracy', lookup_expr='lte', label='accuracy_lte')
    power_points_gte = filters.NumberFilter(
        field_name='power_points', lookup_expr='gte', label='power_points_gte')
    power_points_lte = filters.NumberFilter(
        field_name='power_points', lookup_expr='lte', label='power_points_lte')

    class Meta:
        model = Move
        fields = [
            'name', 'type', 'category', 'power', 'power_gte', 'power_lte',
            'accuracy', 'accuracy_gte', 'accuracy_lte', 'power_points',
            'power_points_gte', 'power_points_lte'
        ]


class NatureFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='name')
    positive_stat = filters.CharFilter(
        field_name='positive', lookup_expr='icontains', label='positive_stat')
    negative_stat = filters.CharFilter(
        field_name='negative', lookup_expr='icontains', label='negative_state')

    class Meta:
        model = Nature
        fields = ['name', 'positive_stat', 'negative_stat']


class PokemonFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='name')
    form = filters.CharFilter(
        field_name='form', lookup_expr='icontains', label='form')
    type = filters.CharFilter(
        field_name='types', lookup_expr='name__icontains', label='type')
    move = filters.CharFilter(
        field_name='moves', lookup_expr='name__icontains', label='type')
    ability = filters.CharFilter(
        field_name='abilities', lookup_expr='name__icontains', label='ability')
    hit_points_gte = filters.NumberFilter(
        field_name='hit_points', lookup_expr='gte', label='hit_points_gte')
    attack_gte = filters.NumberFilter(
        field_name='attack', lookup_expr='gte', label='attack_gte')
    defense_gte = filters.NumberFilter(
        field_name='defense', lookup_expr='gte', label='defense_gte')
    special_attack_gte = filters.NumberFilter(
        field_name='special_attack', lookup_expr='gte', label='special_attack_gte')
    special_defense_gte = filters.NumberFilter(
        field_name='special_defense', lookup_expr='gte', label='special_defense_gte')
    speed_gte = filters.NumberFilter(
        field_name='speed', lookup_expr='gte', label='speed_gte')
    hit_points_lte = filters.NumberFilter(
        field_name='hit_points', lookup_expr='lte', label='hit_points_lte')
    attack_lte = filters.NumberFilter(
        field_name='attack', lookup_expr='lte', label='attack_lte')
    defense_lte = filters.NumberFilter(
        field_name='defense', lookup_expr='lte', label='defense_lte')
    special_attack_lte = filters.NumberFilter(
        field_name='special_attack', lookup_expr='lte', label='special_attack_lte')
    special_defense_lte = filters.NumberFilter(
        field_name='special_defense', lookup_expr='lte', label='special_defense_lte')
    speed_lte = filters.NumberFilter(
        field_name='speed', lookup_expr='lte', label='speed_gte')

    class Meta:
        model = Pokemon
        fields = ['pokedex', 'name', 'type', 'move', 'ability', 'hit_points', 'hit_points_gte', 'hit_points_lte', 'attack', 'attack_gte', 'attack_lte', 'defense', 'defense_gte',
                  'defense_lte', 'special_attack', 'special_attack_gte', 'special_attack_lte', 'special_defense', 'special_defense_gte', 'special_defense_lte', 'speed', 'speed_gte', 'speed_lte']


class TypeFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains', label='name')

    class Meta:
        model = Type
        fields = ['name']
