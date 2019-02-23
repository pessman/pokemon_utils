from django.contrib import admin

from pokemon.models import Ability, Item, Move, Pokemon, Type

admin.site.register(Ability)
admin.site.register(Item)
admin.site.register(Move)
admin.site.register(Pokemon)
admin.site.register(Type)
