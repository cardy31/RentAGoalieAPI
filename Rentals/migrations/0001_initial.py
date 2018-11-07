# Generated by Django 2.1.3 on 2018-11-07 03:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('game_time', models.DateTimeField(default='1970-01-01T00:00:00.000000Z')),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('two_goalies_needed', models.BooleanField(default=False)),
                ('applied_goalies', models.ManyToManyField(related_name='goalieQueued', to=settings.AUTH_USER_MODEL)),
                ('goalie_one', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goalieOne', to=settings.AUTH_USER_MODEL)),
                ('goalie_two', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='goalieTwo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='No name given', max_length=64)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(default='', max_length=5000)),
                ('creation_time', models.DateTimeField(auto_now=True)),
                ('sender_is_goalie', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rentals.Game')),
                ('goalie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameGoalie', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('games_played', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('is_goalie', models.BooleanField(default=True)),
                ('picture', models.ImageField(max_length=255, null=True, upload_to='media/')),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('reset_token', models.CharField(default='0', max_length=64)),
                ('skill_level', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('access_token', models.CharField(default='0', max_length=64)),
                ('locations', models.ManyToManyField(to='Rentals.Location')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rentals.Location'),
        ),
        migrations.AddField(
            model_name='game',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gameUser', to=settings.AUTH_USER_MODEL),
        ),
    ]
