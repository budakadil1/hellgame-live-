# Generated by Django 3.0.6 on 2020-11-22 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='post_status',
            field=models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('W', 'Waiting')], default='W', max_length=72),
        ),
    ]
