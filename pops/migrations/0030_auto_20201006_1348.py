# Generated by Django 3.1.1 on 2020-10-06 17:48

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0029_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='count',
            field=models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='count'),
        ),
        migrations.AddField(
            model_name='point',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date'),
            preserve_default=False,
        ),
    ]
