# Generated by Django 2.1.3 on 2018-11-14 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Rentals', '0004_profile_credit_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profileUser', to=settings.AUTH_USER_MODEL),
        ),
    ]