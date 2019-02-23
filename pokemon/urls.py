from django.urls import include, path
from rest_framework import routers

from pokemon.views import (AbilityViewSet, ItemViewSet, MoveViewSet,
                           PokemonViewSet, TypeViewSet)

router = routers.DefaultRouter()
router.register(r'abilities', AbilityViewSet)
router.register(r'info', PokemonViewSet)
router.register(r'items', ItemViewSet)
router.register(r'moves', MoveViewSet)
router.register(r'types', TypeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
