# Generated by Django 3.2.5 on 2021-09-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
