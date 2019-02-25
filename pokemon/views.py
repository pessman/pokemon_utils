from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from pokemon.models import Ability, Item, Move, Pokemon, Type
from pokemon.pagination import PokemonPagination
from pokemon.serializers import (AbilitySerializer, ItemSerializer,
                                 MoveSerializer, PokemonSerializer,
                                 TypeSerializer)


class AbilityViewSet(viewsets.ModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminUser,)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminUser,)


class MoveViewSet(viewsets.ModelViewSet):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminUser,)


class PokemonViewSet(viewsets.ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminUser,)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminUser,)
