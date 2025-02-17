# Generated by Django 3.0.2 on 2020-01-31 17:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pops', '0018_session_max_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runcollection',
            name='name',
            field=models.CharField(default='Default_name', max_length=45, verbose_name='run name'),
        ),
        migrations.CreateModel(
            name='AllowedUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.Session', verbose_name='session id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user id')),
            ],
            options={
                'verbose_name': 'allowed user',
                'verbose_name_plural': 'allowed users',
            },
        ),
    ]
