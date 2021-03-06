# Generated by Django 3.2.7 on 2021-11-16 19:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manager', '0002_manager_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='food_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_title', models.CharField(max_length=150)),
                ('food_description', models.CharField(blank=True, max_length=250)),
                ('food_price', models.FloatField()),
                ('quantity', models.IntegerField(default=1)),
                ('image', models.ImageField(default='default.png', upload_to='images/')),
                ('date_of_creation', models.DateField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.manager_account')),
            ],
        ),
    ]
