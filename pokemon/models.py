from django.db import models

class Ability(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)

class Item(models.Model):
    ITEM_CATEGORY_CHOICES = (
        ('BATTLE_ITEMS', 'Battle Items'),
        ('BERRIES', 'Berries'),
        ('GENERAL_ITEMS', 'General Items'),
        ('HOLD_ITEMS', 'Hold Items'),
        ('MACHINES', 'Machines'),
        ('MEDICINE', 'Medicine'),
        ('POKEBALLS', 'Pokeballs'),
        ('UNKOWN', 'Uknown')
    )
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=16, choices=ITEM_CATEGORY_CHOICES)
    effect = models.CharField(max_length=256)

class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=512)

class Move(models.Model):
    MOVE_CATEGORY_CHOICES = (
        ('PHYSICAL', 'Physical'),
        ('SPECIAL', 'Special'),
        ('STATUS', 'Status')
    )
    name = models.CharField(max_length=64)
    type = models.OneToOneField(Type, null=True, on_delete=models.SET_NULL)
    category = models.CharField(max_length=16, choices=MOVE_CATEGORY_CHOICES, null=True)
    power = models.IntegerField(null=True)
    accuracy = models.IntegerField(null=True)
    power_points = models.IntegerField()
    tm = models.CharField(max_length=8, null=True)
    effect = models.CharField(max_length=256)

class Pokemon(models.Model):
    pokedex = models.IntegerField()
    name = models.CharField(max_length=32)
    form = models.CharField(max_length=32)
    types = models.ManyToManyField(Type, related_name='pokemon', related_query_name='pokemon')
    moves = models.ManyToManyField(Move, related_name='pokemon', related_query_name='pokemon')
    abilities = models.ManyToManyField(Ability, related_name='pokemon', related_query_name='pokemon')
    hit_points = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()