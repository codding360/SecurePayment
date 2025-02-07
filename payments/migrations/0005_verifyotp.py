# Generated by Django 4.2.17 on 2024-12-21 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_remove_payment_description_payment_card_cvv_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('succeeded', 'Succeeded'), ('wrong_otp', 'Wrong OTP')], default='pending', max_length=10)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
            ],
        ),
    ]
