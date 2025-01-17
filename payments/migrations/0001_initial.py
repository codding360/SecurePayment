# Generated by Django 4.2.17 on 2024-12-20 18:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='RUB', max_length=3)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('succeeded', 'Succeeded'), ('canceled', 'Canceled')], default='pending', max_length=10)),
                ('description', models.TextField()),
                ('confirmation_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
