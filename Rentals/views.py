from datetime import datetime, timedelta, timezone

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser

from .serializers import *
from .tokens import account_activation_token

# Wait time in minutes
WAIT_TIME = 5
CURRENT_SITE = 'localhost:8000'


# Normal auth
# user: id of user
# game: id of game
# goalie: id of goalie
# Returns:
#     200 if added to queue
#     202 if given the game
#     410 if the game is already filled
# TODO: Add test to make sure ApplyForGame is working
class ApplyForGame(APIView):
    def post(self, request):
        print("Goalie applied!")
        print(request.data)
        data = request.data
        game_id = data["game"]
        goalie_id = data["goalie"]
        if not game_id:
            return Response("Field 'game' cannot be blank", status=status.HTTP_400_BAD_REQUEST)
        if not goalie_id:
            return Response("Field 'goalie' cannot be blank", status=status.HTTP_400_BAD_REQUEST)
        game = Game.objects.get(pk=game_id)
        goalie = User.objects.get(pk=goalie_id)

        # Removing logic to have a queue of possible goalies in favor of First Come First Served
        # if self.__game_was_recently_created(game.creation_time):
        #     new_entry = Game.objects.get()
        #     new_entry.applied_goalies.add(goalie)
        #     new_entry.save()
        #     return Response("Goalie {} queued for game {}".format(game_id, goalie_id), status=status.HTTP_200_OK)
        # else:
        #
        return self.__add_goalie_if_needed(game, goalie)

    @staticmethod
    def __add_goalie_if_needed(game, goalie):
        if not game.goalie_one:
            game.goalie_one = goalie
            game.save()
            # TODO: Add push notification
            return Response("Goalie saved", status=status.HTTP_202_ACCEPTED)
        elif not game.goalie_two and game.two_goalies_needed:
            game.goalie_two = goalie
            game.save()
            # TODO: Add push notification
            return Response("Goalie saved", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Game has already been filled", status=status.HTTP_410_GONE)

    @staticmethod
    def __game_was_recently_created(creation_time):
        return timezone.now() - creation_time > timedelta(minutes=WAIT_TIME)


class RemoveGoalieFromGame(APIView):
    def post(self, request):
        print("In RemoveGoalieFromGame")
        data = request.data
        print(data)
        game_id = data["game"]
        goalie_id = data["goalie"]
        game = Game.objects.get(pk=game_id)
        if game.goalie_one_id == goalie_id:
            game.goalie_one_id = None
            game.save()
            return Response("Attendance Cancelled", status=status.HTTP_202_ACCEPTED)
        elif game.goalie_two_id == goalie_id:
            game.goalie_two_id = None
            game.save()
            return Response("Attendance Cancelled", status=status.HTTP_202_ACCEPTED)
        return Response("Game could not be found", status=status.HTTP_400_BAD_REQUEST)


# TODO: Create an algorithm to pick the best goalie
# def __get_top_goalies(queryset):
#     if queryset.__len__() == 0:
#         return None, None
#     elif queryset.__len__() == 1:
#         return queryset[0], None
#     return queryset[0], queryset[1]


# TODO: Don't let users create games where they aren't the user
# TODO: Authorize credit card on create
# TODO: Charge credit care at game time iff there are adequate goalies for the game
# TODO: Deal with billing for the game
# Game Model Views
class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.filter(game_time__gt=timezone.now() - timedelta(days=1))
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # print(request.authenticators)
        # print('request.user.id: {}, request.data: {}'.format(request.user.id, request.data['user']))
        print("Printing request")
        print(request)
        print(request.data)
        # print(request.headers)
        if 'user' not in request.data or \
                (request.user.id != request.data['user'] and request.user.is_superuser is False):
            return Response('Game user must be same as user requesting create', status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# This one was being funny on the server. Commenting out the activate at the bottom seemed to fix it.
def activate(request, uidb64, token):
    print('uidb64 is {}, token is {}, request is {}'.format(uidb64, token, request))
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        print('UID decoded is: {}'.format(uid))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        print('Hit an error')
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class CheckUsernameUnique(APIView):
    permission_classes = (IsAdminUser,)

    @staticmethod
    def post(request):
        username = request.data['username']

        if username is None:
            return Response('Must provide username field', status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({'unique': True}, status.HTTP_200_OK)
        return Response({'unique': False}, status.HTTP_200_OK)


class CheckEmailUnique(APIView):
    permission_classes = (IsAdminUser,)

    @staticmethod
    def post(request):
        email = request.data['email']

        if email is None:
            return Response('Must provide email field', status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({'unique': True}, status.HTTP_200_OK)
        return Response({'unique': False}, status.HTTP_200_OK)


# Location Model Views
class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# Message Model Views
class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser is False:
            self.queryset = Message.objects.filter(game_user=request.user).__or__(
                Message.objects.filter(goalie_user=request.user))
        return super().get(request, *args, **kwargs)


class MessageDetail(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser is False:
            self.queryset = Message.objects.filter(game_user=request.user).__or__(
                Message.objects.filter(goalie_user=request.user))
        return super().get(request, *args, **kwargs)


# Profile Model Views
class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# User Model Views
# TODO: Throttle create requests
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser is False:
            self.queryset = User.objects.filter(id=request.user.id)
        return super().get(request, *args, **kwargs)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser is False:
            self.queryset = User.objects.filter(id=request.user.id)
        return super().get(request, *args, **kwargs)


# These become links visible on the homepage of the browseable API. Additional endpoints
# are defined in urls.py
@api_view(['GET'])
def api_root(request, given_format=None):
    return Response({
        # 'activate': reverse('activate-account', request=request, format=given_format),
        'apply': reverse('apply', request=request, format=given_format),
        'check-username': reverse('check-username', request=request, format=given_format),
        'check-email': reverse('check-email', request=request, format=given_format),
        'game': reverse('game-list', request=request, format=given_format),
        'location': reverse('location-list', request=request, format=given_format),
        'message': reverse('message-list', request=request, format=given_format),
        'profile': reverse('profile-list', request=request, format=given_format),
        'user': reverse('user-list', request=request, format=given_format),
    })
