# Generated by Django 3.2.7 on 2021-12-08 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_manager_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager_account',
            name='man_pass',
            field=models.CharField(max_length=10000),
        ),
    ]
