# Generated by Django 3.2.5 on 2022-05-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_uicinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='first_prize_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='conference',
            name='second_prize_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='conference',
            name='third_prize_num',
            field=models.IntegerField(default=0),
        ),
    ]