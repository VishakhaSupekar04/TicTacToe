# Generated by Django 2.2.3 on 2019-07-23 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playGame', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='players',
            name='game_status',
            field=models.CharField(default='F', max_length=1),
        ),
    ]
