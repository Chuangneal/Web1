# Generated by Django 3.2.5 on 2022-05-17 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_alter_emailhistory_send_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poster',
            old_name='count_ticket',
            new_name='number_ticket',
        ),
        migrations.AddField(
            model_name='poster',
            name='total_ticket',
            field=models.IntegerField(default=0),
        ),
    ]