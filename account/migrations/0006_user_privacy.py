# Generated by Django 2.2 on 2020-11-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_delete_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='privacy',
            field=models.CharField(choices=[(0, 'Public'), (1, 'Private')], default=0, max_length=1),
        ),
    ]
