# Generated by Django 3.0.6 on 2020-10-29 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201028_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamepost',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
