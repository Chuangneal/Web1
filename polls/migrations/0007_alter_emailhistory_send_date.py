# Generated by Django 3.2.5 on 2022-05-12 19:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_alter_emailhistory_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailhistory',
            name='send_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
    ]