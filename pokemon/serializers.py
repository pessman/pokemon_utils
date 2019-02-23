from rest_framework import serializers

from pokemon.models import Ability, Item, Move, Pokemon, Type


class AbilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class MoveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'

class PokemonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'

class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
