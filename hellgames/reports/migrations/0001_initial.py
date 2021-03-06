# Generated by Django 3.0.6 on 2020-11-21 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('post_title', models.CharField(max_length=32)),
                ('post_text', models.TextField()),
                ('post_status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('W', 'Waiting')], default='Waiting', max_length=72)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
