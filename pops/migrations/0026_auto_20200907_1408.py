# Generated by Django 3.1.1 on 2020-09-07 18:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0025_auto_20200904_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pestinformation',
            name='arrival_year',
            field=models.PositiveSmallIntegerField(blank=True, default=None, help_text='The first year that it was identified in the US.', null=True, validators=[django.core.validators.MinValueValidator(1700), django.core.validators.MaxValueValidator(2100)], verbose_name='first year found in US'),
        ),
    ]
