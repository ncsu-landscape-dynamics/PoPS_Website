# Generated by Django 3.0 on 2020-01-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_auto_20200117_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(help_text="What is the team member's role in the project?", max_length=250, null=True, verbose_name='team member role'),
        ),
    ]
