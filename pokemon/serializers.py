from rest_framework import serializers

from pokemon import models

class TypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Type
        fields = '__all__'