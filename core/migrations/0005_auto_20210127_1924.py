# Generated by Django 3.1.5 on 2021-01-27 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['id']},
        ),
    ]
