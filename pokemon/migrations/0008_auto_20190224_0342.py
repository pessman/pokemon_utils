# Generated by Django 2.1.7 on 2019-02-24 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0007_move_effect_percent_chance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pokemon.Type'),
        ),
    ]
