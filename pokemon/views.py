from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from pokemon.filters import (AbilityFilter, ItemFilter, MoveFilter,
                             NatureFilter, PokemonFilter, TypeFilter)
from pokemon.models import Ability, Item, Move, Nature, Pokemon, Type
from pokemon.pagination import PokemonPagination
from pokemon.permissions import IsAdminOrReadOnly
from pokemon.serializers import (AbilitySerializer, ItemSerializer,
                                 MoveSerializer, NatureSerialzier,
                                 PokemonSerializer, TypeSerializer)
from utils import abilities, items, moves, natures, pokemon, types


class BuildPokemonDbView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminOrReadOnly,)

    def post(self, request, format=None):
        pokemon.build_pokemon_db()
        return Response({"message": "Building pokemon database."}, status=status.HTTP_200_OK)


class AbilityViewSet(ModelViewSet):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = AbilityFilter


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = ItemFilter


class MoveViewSet(ModelViewSet):
    queryset = Move.objects.all()
    serializer_class = MoveSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = MoveFilter

class NatureViewSet(ModelViewSet):
    queryset = Nature.objects.all()
    serializer_class = NatureSerialzier
    pagination_class = PokemonPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = NatureFilter


class PokemonViewSet(ModelViewSet):
    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PokemonFilter


class TypeViewSet(ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    pagination_class = PokemonPagination
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TypeFilter
