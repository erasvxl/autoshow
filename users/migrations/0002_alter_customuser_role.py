# Generated by Django 5.2 on 2025-04-24 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Администратор'), ('manager', 'Менеджер'), ('client', 'Клиент')], default='client', max_length=10),
        ),
    ]
