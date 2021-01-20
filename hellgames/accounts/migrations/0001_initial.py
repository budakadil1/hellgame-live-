# Generated by Django 3.0.6 on 2020-08-19 21:25

from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='gameIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=48)),
                ('game_choice', models.CharField(choices=[('default', 'NO CATEGORY'), ('MOBA', 'MOBA'), ('FPS', 'FPS'), ('MMORPG', 'MMORPG'), ('Adventure', 'Adventure'), ('TPS', 'TPS'), ('MMO', 'MMO'), ('2D', '2D')], default='default', max_length=72)),
                ('game_slug', models.SlugField(max_length=48, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='gamePost',
            fields=[
                ('post_title', models.CharField(max_length=32)),
                ('post_text', models.TextField()),
                ('slug', models.SlugField(max_length=32, unique=True)),
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('USD', 'US Dollar')], default='USD', editable=False, max_length=3)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=4, default_currency='USD', max_digits=19)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.gameIdentifier')),
            ],
        ),
    ]