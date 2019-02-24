from rest_framework import serializers

from pokemon.models import Ability, Item, Move, Pokemon, Type


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

class AbilityNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = ('name',)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class TypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('name',)

class PokemonSerializer(serializers.ModelSerializer):
    abilities = AbilityNameSerializer(many=True, read_only=True)
    types = TypeNameSerializer(many=True, read_only=True)

    class Meta:
        model = Pokemon
        fields = '__all__'
