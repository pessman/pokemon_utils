import pytest
from django.test import TestCase
from rest_framework import serializers as drf_serializers

from pokemon import models, serializers


@pytest.mark.django_db
class StatsSerializer(TestCase):
    """
    Test Module for StatsSerializer

    """

    def setUp(self):
        models.Nature.objects.create(
            name="Adamant",
            positive="attack",
            negative="special_attack"
        )

        self.valid_base_stats = {
            "hit_points": 108,
            "attack": 130,
            "defense": 95,
            "special_attack": 80,
            "special_defense": 85,
            "speed": 102
        }

        self.valid_ivs = {
            "hit_points": 24,
            "attack": 12,
            "defense": 30,
            "special_attack": 16,
            "special_defense": 23,
            "speed": 5
        }

        self.invalid_ivs_high = {
            "hit_points": 33,
            "attack": 12,
            "defense": 30,
            "special_attack": 16,
            "special_defense": 23,
            "speed": 5
        }

        self.invalid_ivs_low = {
            "hit_points": -1,
            "attack": 12,
            "defense": 30,
            "special_attack": 16,
            "special_defense": 23,
            "speed": 5
        }

        self.valid_evs = {
            "hit_points": 74,
            "attack": 190,
            "defense": 91,
            "special_attack": 48,
            "special_defense": 84,
            "speed": 23
        }

        self.invalid_evs_high_individual = {
            "hit_points": 0,
            "attack": 300,
            "defense": 0,
            "special_attack": 0,
            "special_defense": 0,
            "speed": 0
        }

        self.invalid_evs_high_total = {
            "hit_points": 74,
            "attack": 190,
            "defense": 91,
            "special_attack": 48,
            "special_defense": 84,
            "speed": 100
        }

        self.invalid_evs_low_individual = {
            "hit_points": 0,
            "attack": -10,
            "defense": 0,
            "special_attack": 0,
            "special_defense": 0,
            "speed": 0
        }


        self.valid_level = 78
        self.invalid_level_high = 110
        self.invalid_level_low = 0
        self.valid_nature = "adamant"
        self.invalid_nature = "thisisntanature"

    def test_stats_serializer(self):
        serializer = serializers.StatsSerializer(data={
            "base_stats": self.valid_base_stats,
            "evs": self.valid_evs,
            "ivs": self.valid_ivs,
            "level": self.valid_level,
            "nature": self.valid_nature
        })
        serializer.is_valid(raise_exception=True)
        stats = serializer.get_stats()
        self.assertEqual(stats["hit_points"], 289)
        self.assertEqual(stats["attack"], 278)
        self.assertEqual(stats["defense"], 193)
        self.assertEqual(stats["special_attack"], 135)
        self.assertEqual(stats["special_defense"], 171)
        self.assertEqual(stats["speed"], 171)

    def test_invalid_nature(self):
        with pytest.raises(drf_serializers.ValidationError) as exc:
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.valid_evs,
                "ivs": self.valid_ivs,
                "level": self.valid_level,
                "nature": self.invalid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_level_high(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.valid_evs,
                "ivs": self.valid_ivs,
                "level": self.invalid_level_high,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_level_low(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.valid_evs,
                "ivs": self.valid_ivs,
                "level": self.invalid_level_low,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_ivs_low(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.valid_evs,
                "ivs": self.invalid_ivs_low,
                "level": self.valid_level,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_ivs_high(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.valid_evs,
                "ivs": self.invalid_ivs_high,
                "level": self.valid_level,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_evs_high_total(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.invalid_evs_high_total,
                "ivs": self.valid_ivs,
                "level": self.valid_level,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_evs_high_individual(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.invalid_evs_high_individual,
                "ivs": self.valid_ivs,
                "level": self.valid_level,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)

    def test_invalid_evs_low_individual(self):
        with pytest.raises(drf_serializers.ValidationError):
            serializer = serializers.StatsSerializer(data={
                "base_stats": self.valid_base_stats,
                "evs": self.invalid_evs_low_individual,
                "ivs": self.valid_ivs,
                "level": self.valid_level,
                "nature": self.valid_nature
            })
            serializer.is_valid(raise_exception=True)
