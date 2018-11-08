from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework.authtoken.models import Token

from .tokens import account_activation_token

CURRENT_SITE = 'localhost:8000'


class Game(models.Model):
    user = models.ForeignKey(User, related_name='gameUser', on_delete=models.CASCADE, null=True)
    skill_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)  # 1 is best
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    # Format is 2018-05-16 20:00:00
    game_time = models.DateTimeField(default='1970-01-01T00:00:00Z', validators=[])
    creation_time = models.DateTimeField(auto_now=True)
    goalie_one = models.ForeignKey(User, related_name='goalieOne', null=True, on_delete=models.CASCADE)
    goalie_two = models.ForeignKey(User, related_name='goalieTwo', null=True, on_delete=models.CASCADE)
    two_goalies_needed = models.BooleanField(default=False)
    applied_goalies = models.ManyToManyField(User, related_name='goalieQueued')

    def __str__(self):
        return "Id: {}, game_time: {}, location:" \
               " {} ({}, {}), skill_level: {}".format(self.id,
                                                      self.game_time,
                                                      self.location.name,
                                                      self.location.latitude,
                                                      self.location.longitude,
                                                      self.skill_level,)


class Location(models.Model):
    # Name of the location, if one was given
    name = models.CharField(max_length=64, default="No name given")
    # Runs North/South. But we're using decimal coordinates for this, so South is negative
    latitude = models.FloatField(default=0)
    # Runs East/West. But we're using decimal coordinates for this, so West is negative
    longitude = models.FloatField(default=0)

    def __str__(self):
        return "{} ({}, {})".format(self.name,
                                    self.latitude,
                                    self.longitude)


class Message(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    body = models.CharField(max_length=5000, default="")
    game_user = models.ForeignKey(User, related_name='gameRenter', on_delete=models.CASCADE)
    goalie_user = models.ForeignKey(User, related_name='gameGoalie', on_delete=models.CASCADE)
    sender_is_goalie = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    games_played = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_goalie = models.BooleanField(default=True, blank=False, null=False)
    locations = models.ManyToManyField('Location')
    picture = models.ImageField(upload_to='media/', null=True, max_length=255)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reset_token = models.CharField(max_length=64, default='0')
    skill_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                      default=5)  # 1 is the best
    access_token = models.CharField(max_length=64, default='0')

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            # Create a profile entry with the same primary key as the user entry
            Profile.objects.create(pk=instance.id)
            profile = Profile.objects.get(pk=instance.id)
            profile.reset_token = account_activation_token.make_token(User.objects.get(pk=instance.id))
            Token.objects.create(user=User.objects.get(pk=instance.id))
            profile.access_token = str(Token.objects.get(user=User.objects.get(pk=instance.id)))
            profile.save()

    @staticmethod
    @receiver(post_save, sender=User)
    def hash_user_password(sender, instance, created, **kwargs):
        if created:
            user = User.objects.get(pk=instance.id)
            if user.password[:6] != 'pbkdf2':
                user.set_password(user.password)
                user.save()

    @staticmethod
    @receiver(post_save, sender=User)
    def send_verification_email(sender, instance, created, **kwargs):
        if created:
            user = instance
            subject = 'Verify Your Rent A Goalie Account'
            body = render_to_string('activate_email.html', {
                'user': user,
                'domain': CURRENT_SITE,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': Profile.objects.get(pk=user.id).reset_token,
            })
            to_email = user.email
            email = EmailMessage(subject, body, to=[to_email])
            email.send()
