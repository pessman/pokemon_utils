# Generated by Django 2.1.7 on 2019-02-23 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0002_auto_20190223_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ability',
            options={'verbose_name': 'ability', 'verbose_name_plural': 'abilities'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'item', 'verbose_name_plural': 'items'},
        ),
        migrations.AlterModelOptions(
            name='move',
            options={'verbose_name': 'move', 'verbose_name_plural': 'moves'},
        ),
        migrations.AlterModelOptions(
            name='pokemon',
            options={'verbose_name': 'pokemon', 'verbose_name_plural': 'pokemon'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'types'},
        ),
    ]