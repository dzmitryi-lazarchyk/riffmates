# Generated by Django 5.1 on 2024-12-06 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promoters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='promoter',
            name='famous_for',
            field=models.CharField(default='', max_length=75),
            preserve_default=False,
        ),
    ]
