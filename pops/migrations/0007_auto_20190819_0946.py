# Generated by Django 2.2.4 on 2019-08-19 13:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0006_distancetoboundary'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeToBoundary',
            fields=[
                ('output', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Output', verbose_name='output')),
                ('west_time', models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in westerly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='westerly time to boundary')),
                ('east_time', models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in easterly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='easterly time to boundary')),
                ('north_time', models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in northerly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='northerly time to boundary')),
                ('south_time', models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in southerly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='southerly time to boundary')),
            ],
            options={
                'verbose_name': 'time to boundary',
                'verbose_name_plural': 'time to boundarys',
            },
        ),
        migrations.AlterField(
            model_name='distancetoboundary',
            name='east_distance',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in easterly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='easterly distance to boundary'),
        ),
        migrations.AlterField(
            model_name='distancetoboundary',
            name='north_distance',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in northerly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='northerly distance to boundary'),
        ),
        migrations.AlterField(
            model_name='distancetoboundary',
            name='south_distance',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in southerly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='southerly distance to boundary'),
        ),
        migrations.AlterField(
            model_name='distancetoboundary',
            name='west_distance',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Spread rate in westerly direction', max_digits=6, validators=[django.core.validators.MinValueValidator(0)], verbose_name='westerly distance to boundary'),
        ),
    ]
