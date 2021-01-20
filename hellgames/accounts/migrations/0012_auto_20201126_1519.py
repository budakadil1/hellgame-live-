# Generated by Django 3.0.6 on 2020-11-26 20:19

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_gamepost_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamepost',
            name='price_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='gamepost',
            name='price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='USD', max_digits=19),
        ),
    ]