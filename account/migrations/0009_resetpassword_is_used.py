# Generated by Django 3.1.5 on 2021-02-05 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_resetpassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='resetpassword',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
