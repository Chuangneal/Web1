# Generated by Django 3.2.5 on 2022-05-18 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20220518_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='conference',
            name='name',
            field=models.CharField(default='CMS', max_length=100),
        ),
    ]
