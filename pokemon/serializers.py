from collections import OrderedDict

from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

from pokemon.models import Ability, Item, Move, Nature, Pokemon, Type


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'

    def to_internal_value(self, data):
        for key in [key for key in data if type(data[key]) is str]:
            data[key] = data[key].upper()

        return super().to_internal_value(data)

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            elif type(attribute) is str:
                ret[field.field_name] = field.to_representation(attribute.title())
            else:
                ret[field.field_name] = field.to_representation(attribute)


        return ret


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


class NatureSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Nature
        fields = '__all__'

class InternalValueSerializer(serializers.Serializer):
    hit_points = serializers.IntegerField(min_value=0, max_value=31)
    attack = serializers.IntegerField(min_value=0, max_value=31)
    defense = serializers.IntegerField(min_value=0, max_value=31)
    special_attack = serializers.IntegerField(min_value=0, max_value=31)
    special_defense = serializers.IntegerField(min_value=0, max_value=31)
    speed = serializers.IntegerField(min_value=0, max_value=31)


class EfforValueSerializer(serializers.Serializer):
    hit_points = serializers.IntegerField(min_value=0, max_value=255)
    attack = serializers.IntegerField(min_value=0, max_value=255)
    defense = serializers.IntegerField(min_value=0, max_value=255)
    special_attack = serializers.IntegerField(min_value=0, max_value=255)
    special_defense = serializers.IntegerField(min_value=0, max_value=255)
    speed = serializers.IntegerField(min_value=0, max_value=255)

    def validate(self, data):
        from pokemon.stats import STATS
        if sum([data[key] for key in data if key in STATS]) > 510:
            raise serializers.ValidationError("Effort Values total more than 510.")
        return data


class StatsSerializer(serializers.Serializer):
    pokemon_id = serializers.IntegerField(min_value=1)
    ivs = InternalValueSerializer()
    evs = EfforValueSerializer()
    level = serializers.IntegerField(min_value=1, max_value=100)
    nature = serializers.CharField()

    def validate_nature(self, nature):
        from pokemon.models import Nature
