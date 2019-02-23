from rest_framework import viewsets

from pokemon.models import (
    Type
)

from pokemon.serializers import (
    TypeSerializer
)

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer