from collections import OrderedDict
from math import floor

from rest_framework import serializers
from rest_framework.relations import PKOnlyObject

from pokemon.models import Ability, Item, Move, Nature, Pokemon, Type

POKEMON_STATS = ['hit_points', 'attack', 'defense',
                 'special_attack', 'special_defense', 'speed']


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
            check_for_none = attribute.pk if isinstance(
                attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            elif type(attribute) is str:
                ret[field.field_name] = field.to_representation(
                    attribute.title())
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


class NatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nature
        fields = '__all__'


class BaseStatSerializer(serializers.Serializer):
    hit_points = serializers.IntegerField()
    attack = serializers.IntegerField()
    defense = serializers.IntegerField()
    special_attack = serializers.IntegerField()
    special_defense = serializers.IntegerField()
    speed = serializers.IntegerField()


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
        if sum([data[key] for key in data if key in POKEMON_STATS]) > 510:
            raise serializers.ValidationError(
                "Effort Values total more than 510.")
        return data


class StatsSerializer(serializers.Serializer):
    base_stats = BaseStatSerializer()
    ivs = InternalValueSerializer()
    evs = EfforValueSerializer()
    level = serializers.IntegerField(min_value=1, max_value=100)
    nature = serializers.CharField()

    def validate_nature(self, nature):
        from pokemon.models import Nature

        validated_nature = Nature.objects.filter(name__iexact=nature)
        if not validated_nature or not validated_nature.count() == 1:
            raise serializers.ValidationError(
                "Invalid nature of {} provided".format(nature))

        return nature

    def get_level_contribution(self, base, iv, ev, level):
        return floor(level * (2 * base + iv + floor(ev / 4)) / 100)

    def get_hp(self, base, iv, ev, level):
        return {'hit_points': self.get_level_contribution(base, iv, ev, level) + level + 10}

    def get_other_stats(self, base, iv, ev, level, nature, stat):
        from pokemon.models import Nature
        nat = Nature.objects.get(name__iexact=nature)
        if not nat:
            raise StatsError("No nature found with name {}".format(nat))

        return {stat: floor((self.get_level_contribution(base, iv, ev, level) + 5) * nat.modifier(stat))}

    def get_stats(self):

        stats = {
            **self.get_hp(self.validated_data['base_stats'].get('hit_points'), self.validated_data['ivs'].get('hit_points'), self.validated_data['evs'].get('hit_points'), self.validated_data.get('level'))
        }

        for stat in POKEMON_STATS[1:]:
            stats = {
                **stats,
                **self.get_other_stats(self.validated_data['base_stats'].get(stat), self.validated_data['ivs'].get(stat), self.validated_data['evs'].get(stat), self.validated_data.get('level'), self.validated_data.get('nature'), stat)
            }

        return stats
