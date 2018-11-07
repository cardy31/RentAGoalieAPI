from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Game, Location, Message, Profile


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'skill_level', 'location',
                  'game_time', 'creation_time', 'goalie_one',
                  'goalie_two', 'two_goalies_needed')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'game', 'body', 'goalie', 'creation_time', 'sender_is_goalie')


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'games_played', 'is_goalie',
                  'locations', 'picture', 'rating', 'reset_token',
                  'access_token', 'skill_level')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_staff', 'is_active')
