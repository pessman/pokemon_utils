from rest_framework import viewsets

from pokemon.models import Ability, Item, Move, Pokemon, Type
from pokemon.serializers import (AbilitySerializer, ItemSerializer,
                                 MoveSerializer, PokemonSerializer,
                                 TypeSerializer)


class AbilityViewSet(viewsets.ModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class MoveViewSet(viewsets.ModelViewSet):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer

class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
