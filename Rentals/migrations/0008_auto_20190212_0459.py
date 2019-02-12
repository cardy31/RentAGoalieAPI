# Generated by Django 2.1.3 on 2019-02-12 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Rentals', '0007_auto_20190126_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='locations',
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profileLocation', to='Rentals.Location'),
        ),
    ]
