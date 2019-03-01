from django.db import models


class Ability(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'ability'
        verbose_name_plural = 'abilities'

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    ITEM_CATEGORY_CHOICES = (
        ('BATTLE ITEMS', 'Battle Items'),
        ('BERRIES', 'Berries'),
        ('GENERAL ITEMS', 'General Items'),
        ('HOLD ITEMS', 'Hold Items'),
        ('MACHINES', 'Machines'),
        ('MEDICINE', 'Medicine'),
        ('POKEBALLS', 'Pokeballs'),
        ('UNKOWN', 'Uknown')
    )
    name = models.CharField(max_length=32, unique=True)
    category = models.CharField(
        max_length=16, null=True, choices=ITEM_CATEGORY_CHOICES)
    effect = models.CharField(max_length=256, null=True)

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'

    def __str__(self):
        return str(self.name)


class Type(models.Model):
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=512)

    class Meta:
        verbose_name = 'type'
        verbose_name_plural = 'types'

    def __str__(self):
        return str(self.name)


class Move(models.Model):
    MOVE_CATEGORY_CHOICES = (
        ('PHYSICAL', 'Physical'),
        ('SPECIAL', 'Special'),
        ('STATUS', 'Status')
    )
    name = models.CharField(max_length=64, unique=True)
    type = models.ForeignKey(Type, null=True, on_delete=models.SET_NULL)
    category = models.CharField(
        max_length=16, choices=MOVE_CATEGORY_CHOICES, null=True)
    power = models.IntegerField(null=True)
    accuracy = models.IntegerField(null=True)
    power_points = models.IntegerField()
    tm = models.CharField(max_length=8, null=True)
    effect = models.CharField(max_length=256, null=True)
    effect_percent_chance = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'move'
        verbose_name_plural = 'moves'

    def __str__(self):
        return str(self.name)


class Pokemon(models.Model):
    pokedex = models.IntegerField()
    name = models.CharField(max_length=32)
    form = models.CharField(max_length=32, null=True)
    types = models.ManyToManyField(
        Type, related_name='pokemon', related_query_name='pokemon')
    moves = models.ManyToManyField(
        Move, related_name='pokemon', related_query_name='pokemon')
    abilities = models.ManyToManyField(
        Ability, related_name='pokemon', related_query_name='pokemon')
    hit_points = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()

    class Meta:
        ordering = ['pokedex', 'form']
        verbose_name = 'pokemon'
        verbose_name_plural = 'pokemon'

    def __str__(self):
        return "{}: {}".format(self.pokedex, self.name)


class Nature(models.Model):
    NATURE_MODIFIER_CHOICES = (
        ('+', 1.1),
        ('-', 0.9)
    )
    name = models.CharField(max_length=32, unique=True)
    attack = models.CharField(max_length=1, null=True,
                              choices=NATURE_MODIFIER_CHOICES)
    defense = models.CharField(
        max_length=1, null=True, choices=NATURE_MODIFIER_CHOICES)
    special_attack = models.CharField(
        max_length=1, null=True, choices=NATURE_MODIFIER_CHOICES)
    special_defense = models.CharField(
        max_length=1, null=True, choices=NATURE_MODIFIER_CHOICES)
    speed = models.CharField(max_length=1, null=True,
                             choices=NATURE_MODIFIER_CHOICES)

    def modifiers(self):
        MODIFIERS = {
            '+': 1.1,
            '-': 0.9
        }
        return [MODIFIERS[mod] if mod in MODIFIERS else 1 for mod in [self.attack, self.defense, self.special_attack, self.special_defense, self.speed]]
