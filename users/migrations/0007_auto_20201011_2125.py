# Generated by Django 3.1.2 on 2020-10-12 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201011_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massemail',
            name='message',
            field=models.TextField(help_text='Body of the email. Can include html tags such as <br> and <img>', verbose_name='email message'),
        ),
    ]
