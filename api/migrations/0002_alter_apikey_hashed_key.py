# Generated by Django 5.1 on 2025-01-04 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='hashed_key',
            field=models.CharField(max_length=100),
        ),
    ]
