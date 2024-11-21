# Generated by Django 5.1.3 on 2024-11-21 18:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tgId', models.BigIntegerField(unique=True, verbose_name='Telegram ID')),
                ('userName', models.CharField(max_length=150, verbose_name='Username')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Name')),
                ('secondName', models.CharField(blank=True, max_length=150, null=True, verbose_name='Second Name')),
                ('registrationDate', models.DateField()),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userQuestion', models.TextField()),
                ('date', models.DateTimeField()),
                ('telegramUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='zoo.telegramuser', verbose_name='Telegram User')),
            ],
        ),
    ]