# Generated by Django 2.1.7 on 2019-02-24 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0008_auto_20190224_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='effect',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
