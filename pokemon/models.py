from django.db import models

class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=1024)