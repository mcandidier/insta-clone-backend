# Generated by Django 3.1.5 on 2021-01-27 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_user_privacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
    ]
